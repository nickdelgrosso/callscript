from typing import Any, List, Dict
from redbaron import RedBaron, AssignmentNode


def get_output_var_names(code: str, substr: str = ":output:") -> List[str]:
    red = RedBaron(code)
    nodes = red.node_list
    output_comment_nodes = nodes.find_all('comment', value = lambda s: substr in s)
    output_line_nums = [node.absolute_bounding_box.top_left.line for node in output_comment_nodes]
    output_nodes = [red.at(line_num) for line_num in output_line_nums]
    assert all(isinstance(node, AssignmentNode) for node in output_nodes)
    output_names = [node.target.dumps() for node in output_nodes]
    return output_names


def replace_inputs(code: str, replacements: Dict[str, Any], substr: str = ":input:") -> str:
    red = RedBaron(code)
    nodes = red.node_list
    input_comment_nodes = nodes.find_all('comment', value=lambda s: substr in s)
    input_line_nums = [node.absolute_bounding_box.top_left.line for node in input_comment_nodes]
    input_nodes = [red.at(line_num) for line_num in input_line_nums]
    for node in input_nodes:
        node.value = str(replacements[node.target.dumps()])
    new_code = red.dumps()
    return new_code
    