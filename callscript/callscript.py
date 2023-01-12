from pathlib import Path
from typing import Any, Dict, List, Optional, TypedDict, Union
from redbaron import RedBaron, AssignmentNode, Node


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:

    code = comment_out_ignored_lines(code)

    # Get/Replace Marked Inputs
    red = RedBaron(code)

    include = list(kwargs.keys())
    lines2 = extract_info(red, "input")
    for line2 in lines2:
        name = line2['final_name']
        if not include or name in include:
            line2['node'].value = munge_name(name)
    inputs = {munge_name(name): value for name, value in kwargs.items()}

    # Run Code
    all_vars = exec_locally(red.dumps(), inputs)

    # Extract Outputs
    lines = extract_info(red, "output")
    outputs = {line['final_name']: all_vars[line['name']] for line in lines}
    return outputs
    

def exec_locally(code, inputs: dict = None) -> Dict[str, Any]:
    names = inputs or {}
    exec(code, {}, names)
    return names


def munge_input_values(code: str, substr: str = "input", include: Optional[List[str]] = None) -> str:
    red = RedBaron(code)
    lines = extract_info(red, substr)
    for line in lines:
        name = line['replacement_name'] or line['name']
        if not include or name in include:
            munged_name = munge_name(name)
            line['node'].value = munged_name
    return red.dumps()


def comment_out_ignored_lines(code: str, substr: str = 'ignore') -> str:
    red = RedBaron(code)
    lines = code.splitlines(keepends=True)
    comment_line_info = extract_info(red, substr)
    for info in reversed(comment_line_info):
        idx = info['line_num'] - 1
        lines[idx] = '# ' + lines[idx]
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
    final_name: Optional[str]



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



