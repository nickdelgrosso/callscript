from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Union
from redbaron import RedBaron, AssignmentNode


def callscript(script: Union[str, Path], **kwargs) -> Dict[str, Any]:
    code = Path(script).read_text()
    return call(code, **kwargs)


def call(code: str, **kwargs) -> Dict[str, Any]:
    output_vars = get_output_var_names(code)
    new_code = replace_inputs(code, replacements=kwargs)
    all_vars = exec_locally(new_code)
    outputs = {output_var: all_vars[var] for output_var, var in output_vars.items()}
    return outputs
    


def get_output_var_names(code: str, substr: str = "output") -> Dict[str, Any]:
    red = RedBaron(code)
    lines = extract_info(red, substr)
    
    full_names = {}
    for line in lines:
        cmd, *newname = line['comment'].split(':', 1)
        name = line['name']
        full_name = newname[0] if newname else name
        full_names[full_name] = name

    return full_names


def replace_inputs(code: str, replacements: Dict[str, Any], substr: str = "input") -> str:
    red = RedBaron(code)
    lines = extract_info(red, substr)
    
    for line in lines:
        cmd, *newname = line['comment'].split(':', 1)
        name = line['name']
        full_name = newname[0].strip() if newname else name
        if full_name in replacements:
            new_value = replacements[full_name]
            line['node'].value = str(new_value)
    new_code = red.dumps()
    return new_code



def extract_info(red: RedBaron, substr: str) -> Dict[str, Any]:
    lines = []
    for comment_node in red.node_list.find_all('comment', value=lambda s: substr in s):
        comment = comment_node.dumps()
        line_num = comment_node.absolute_bounding_box.top_left.line
        assignment_node = red.at(line_num)
        name = assignment_node.target.dumps()
        assert isinstance(assignment_node, AssignmentNode)
        line = dict(line_num=line_num, node=assignment_node, name=name, comment=comment)
        lines.append(line)
    return lines



def exec_locally(code) -> Dict[str, Any]:
    names = {}
    exec(code, {}, names)
    return names