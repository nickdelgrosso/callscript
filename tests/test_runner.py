

from textwrap import dedent
from callscript.runner import get_output_var_names, replace_inputs

def test_get_output_names():
    script = dedent("""
    start = "hello"
    x = 3 # :output:
    y = 5 # This code does nothing
    final = "done!"  # :output:
    """)
    expected_outputs = ['x', 'final']
    outputs = get_output_var_names(script, ':output:')
    assert outputs == expected_outputs


def test_replace_input_variables():
    code = dedent("""
    x = 3  # :input:
    y = 5
    """)
    replacement = {'x': 10}
    expected_result = dedent("""
    x = 10  # :input:
    y = 5
    """)
    result = replace_inputs(code, replacement, ':input:')
    assert result == expected_result


