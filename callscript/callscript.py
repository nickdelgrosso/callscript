from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union, Iterable
from redbaron import RedBaron, AssignmentNode, Node


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:
    include = list(kwargs.keys())
    inputs = {munge_name(name): value for name, value in kwargs.items()}

    # Get/Replace Marked Inputs
    red = RedBaron(code)
    commands = find_commands(red)
    output_names = {}  # callscript name -> original name
    for command in commands:
        if 'input' in command['comment_cmd']:
            name = command['final_name']
            if not include or name in include:
                command['node'].value = munge_name(name)
        elif 'ignore' in command['comment_cmd']:
            red.insert(command['line_num'], '# ' + command['node'].dumps())
            red.remove(command['node'])
        elif 'output' in command['comment_cmd']:
            output_names[command['final_name']] = command['name']

    new_code = red.dumps()
    all_vars = inputs or {}
    exec(new_code, {}, all_vars)
    outputs = {final_name: all_vars[orig_name] for final_name, orig_name in output_names.items()}
    return outputs
    


def munge_name(name):
    return f'__{name}'


class CommentedAssignment(TypedDict):
    line_num: int
    node: Node
    name: Optional[str]
    comment: str
    comment_cmd: str
    replacement_name: Optional[str]
    final_name: Optional[str]


def find_commands(red: RedBaron, substrings: Iterable[str] = ('input', 'output', 'ignore')) -> List[CommentedAssignment]:
    all_info = []
    for substr in substrings:
        infos = extract_info(red, substr=substr)
        all_info.extend(infos)
    all_info_sorted = list(sorted(all_info, key=lambda info: info['line_num']))
    return all_info_sorted


def extract_info(red: RedBaron, substr: str) -> List[CommentedAssignment]:
    lines = []
    comment_nodes = red.node_list.find_all('comment', value=lambda s: substr in s)
    for comment_node in comment_nodes:
        comment = comment_node.dumps()
        line_num = comment_node.absolute_bounding_box.top_left.line
        assignment_node = red.at(line_num)
        name = assignment_node.target.dumps() if isinstance(assignment_node, AssignmentNode) else None
        cmd, *newname = comment.replace('#', '').strip().split(':', 1)

        replacement_name = newname[0] if newname else None
        line: CommentedAssignment = {
            'line_num': line_num, 
            'node': assignment_node, 
            'name': name, 
            'comment': comment,
            'comment_cmd': cmd,
            'replacement_name': replacement_name,
            'final_name': replacement_name or name,
        }
        lines.append(line)
    return lines



