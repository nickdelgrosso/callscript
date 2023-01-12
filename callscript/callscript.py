from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union, Iterable, Literal
from redbaron import RedBaron, AssignmentNode, Node


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


def get_assignment_name(node: AssignmentNode) -> str:
    return node.target.dumps()


def replace_right_side(node: Node, value: str) -> None:
    node.value = value


def comment_out(red, node) -> None:
    red.insert(get_line_num(node), '# ' + node.dumps())
    red.remove(node)


def munge_name(name) -> str:
    return f'__{name}'


class CallscriptCommand(TypedDict):
    node: Node
    name: Optional[str]
    command: Literal['input', 'output', 'ignore']


def find_commands(red: RedBaron, substrings: Iterable[str] = ('input', 'output', 'ignore')) -> List[CallscriptCommand]:
    all_info = []
    for substr in substrings:
        infos = extract_info(red, substr=substr)
        all_info.extend(infos)
    return all_info


def extract_info(red: RedBaron, substr: str) -> List[CallscriptCommand]:
    lines = []
    comment_nodes = red.node_list.find_all('comment', value=lambda s: substr in s)
    for comment_node in comment_nodes:
        comment = comment_node.dumps()
        line_num = get_line_num(comment_node)
        assignment_node = red.at(line_num)
        name = assignment_node.target.dumps() if isinstance(assignment_node, AssignmentNode) else None
        cmd, *newname = comment.replace('#', '').strip().split(':', 1)

        line: CallscriptCommand = {
            'node': assignment_node, 
            'name': (newname[0] if newname else name) or name,
            'command': cmd,
        }
        lines.append(line)
    return lines


def get_line_num(node: Node) -> int:
    line_num = node.absolute_bounding_box.top_left.line
    return line_num



