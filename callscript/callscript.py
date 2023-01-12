from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union, Iterable, Literal
from redbaron import RedBaron, AssignmentNode, Node

from .redbaron_utils import get_assignment_name, replace_right_side, comment_out, get_node_at_start_of_line


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:

    red = RedBaron(code)
    output_names = {}  # callscript name -> original name
    for command in find_commands(red):
        if 'input' in command['command']:
            name = command['name']
            if not kwargs or name in kwargs:
                replace_right_side(command['node'], munge_name(name))
        elif 'ignore' in command['command']:
            comment_out(red, command['node'])
        elif 'output' in command['command']:
            node = command['node']
            assert isinstance(node, AssignmentNode)
            name = command['name']
            assert isinstance(name, str)
            output_names[name] = get_assignment_name(node)

    new_code = red.dumps()
    all_vars = {munge_name(name): value for name, value in kwargs.items()}
    exec(new_code, {}, all_vars)
    outputs = {final_name: all_vars[orig_name] for final_name, orig_name in output_names.items()}
    return outputs


def munge_name(name) -> str:
    return f'__{name}'


class CallscriptCommand(TypedDict):
    node: Node
    name: Optional[str]
    command: Literal['input', 'output', 'ignore']


def find_commands(red: RedBaron, substrings: Iterable[str] = ('input', 'output', 'ignore')) -> List[CallscriptCommand]:

    infos = []
    command_nodes = red.node_list.find_all('comment', value=lambda s: any(substr in s for substr in substrings))
    for command_node in command_nodes:
        comment = command_node.dumps()
        assignment_node = get_node_at_start_of_line(red, command_node)
        name = get_assignment_name(assignment_node) if isinstance(assignment_node, AssignmentNode) else None
        cmd, *newname = comment.replace('#', '').strip().split(':', 1)

        info: CallscriptCommand = {
            'node': assignment_node,
            'name': (newname[0] if newname else name) or name,
            'command': cmd,
        }
        infos.append(info)
    return infos



