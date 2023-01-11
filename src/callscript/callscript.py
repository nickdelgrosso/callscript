from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union
from redbaron import RedBaron, AssignmentNode, Node


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:
    output_vars = get_output_var_names(code)
    code = strip_ignored_lines(code)
    new_code = munge_input_values(code)

    inputs = {munge_name(name): value for name, value in kwargs.items()}
    all_vars = exec_locally(new_code, inputs)
    outputs = {output_var: all_vars[var] for output_var, var in output_vars.items()}
    return outputs
    

def exec_locally(code, inputs: dict = None) -> Dict[str, Any]:
    names = inputs or {}
    exec(code, {}, names)
    return names


def get_output_var_names(code: str, substr: str = "output") -> Dict[str, Any]:
    red = RedBaron(code)
    lines = extract_info(red, substr)
    full_names = dict((line['replacement_name'] or line['name'], line['name']) for line in lines)
    return full_names


def munge_input_values(code: str, substr: str = "input") -> str:
    red = RedBaron(code)
    lines = extract_info(red, substr)
    for line in lines:
        munged_name = munge_name(line['replacement_name'] or line['name'])
        line['node'].value = munged_name
    return red.dumps()


def strip_ignored_lines(code: str, substr: str = 'ignore') -> str:
    red = RedBaron(code)
    lines = code.splitlines(keepends=True)
    comment_line_info = extract_info(red, substr)
    for line in reversed(comment_line_info):
        del lines[line['line_num'] - 1]
    new_code = ''.join(lines)
    return new_code


def munge_name(name):
    return f'__{name}'





## Info Extraction

class CommentedAssignment(TypedDict):
    line_num: int
    node: Node
    name: Optional[str]
    comment: str
    comment_cmd: str
    replacement_name: Optional[str]



def extract_info(red: RedBaron, substr: str) -> List[CommentedAssignment]:
    lines = []
    comment_nodes = red.node_list.find_all('comment', value=lambda s: substr in s)
    for comment_node in comment_nodes:
        comment = comment_node.dumps()
        line_num = comment_node.absolute_bounding_box.top_left.line
        assignment_node = red.at(line_num)
        name = assignment_node.target.dumps() if isinstance(assignment_node, AssignmentNode) else None
        cmd, *newname = comment.replace('#', '').strip().split(':', 1)

        line: CommentedAssignment = {
            'line_num': line_num, 
            'node': assignment_node, 
            'name': name, 
            'comment': comment,
            'comment_cmd': cmd,
            'replacement_name': newname[0] if newname else None,
        }
        lines.append(line)
    return lines



