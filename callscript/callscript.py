from pathlib import Path
from textwrap import dedent
from typing import Any, Dict, List, Optional, TypedDict, Union, Iterable, Literal
from redbaron import RedBaron, AssignmentNode, Node

from .redbaron_utils import get_assignment_name, prepend, get_node_at_start_of_line


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:

    script = modify_code(code)
    new_code = script['code']

    for name in kwargs:
        if name not in script['input_names']:
            raise TypeError(f"script got an unexpected keyword argument '{name}'.  Possible arguments: {script['input_names']}")

    all_vars = {munge_name(name): value for name, value in kwargs.items()}
    
    
    exec(new_code, {}, all_vars)
    fun = all_vars['fun']
    outputs = fun(**kwargs)
    return outputs


class ScriptMetadata(TypedDict):
    code: str
    input_names: List[str]
    output_name: str
    

def modify_code(code, output_name: str = '__return') -> ScriptMetadata:
    red = RedBaron(code)
    input_names = []
    output_names = {}  # callscript name -> original name
    for command in find_commands(red):
        if 'input' in command['command']:
            name = command['name']
            input_names.append(name)
            node = command['node']
            # node.insert_before(f"{munge_name(name)} = {munge_name(name)} if '{munge_name(name)}' in vars() else None")
            node.replace(f"{node.target.dumps()} = {munge_name(name)} if {munge_name(name)} != None else {node.value}")
        elif 'ignore' in command['command']:
            prepend(red, command['node'], '# ')
        elif 'output' in command['command']:
            node = command['node']
            assert isinstance(node, AssignmentNode)
            name = command['name']
            assert isinstance(name, str)
            output_names[name] = get_assignment_name(node)

    for name in input_names:
        red[0].insert_before(f"{munge_name(name)} = {name}")

    gg = ", ".join(f"{name}=None" for name in input_names)
    red[0].insert_before(f"def fun({gg}):\n    ")  # extra newline and four spaces somehow get around a redbaron parsing error.
    
    red[-1].insert_after(f'return dict({", ".join(f"{k}={v}" for k, v in output_names.items())})')
    for node in red[1:]:
        node.increase_indentation(4)
        
    # red[-1].insert_after(f'{output_name} = fun(')

    
    
    
    new_code = red.dumps()
    results: ScriptMetadata = {
        'code': new_code,
        'input_names': input_names,
        'output_name': output_name,
    }
    return results



def munge_name(name) -> str:
    return f'__{name}'


class CallscriptCommand(TypedDict):
    node: Node
    name: str
    command: Literal['input', 'output', 'ignore']


def find_commands(red: RedBaron, substrings: Iterable[str] = ('input', 'output', 'ignore')) -> List[CallscriptCommand]:

    infos = []
    command_nodes = red.node_list.find_all('comment', value=lambda s: any(substr in s for substr in substrings))
    for command_node in command_nodes:
        comment = command_node.dumps()
        assignment_node = get_node_at_start_of_line(red, command_node)
        name = get_assignment_name(assignment_node) if isinstance(assignment_node, AssignmentNode) else ""
        cmd, *newname = comment.replace('#', '').strip().split(':', 1)

        info: CallscriptCommand = {
            'node': assignment_node,
            'name': (newname[0].strip() if newname else name) or name,
            'command': cmd,
        }
        infos.append(info)
    return infos



