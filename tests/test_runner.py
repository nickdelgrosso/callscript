

from textwrap import dedent
from callscript.callscript import get_output_var_names, replace_inputs, call

def test_get_output_names():
    script = dedent("""
    start = "hello"
    x = 3 # output
    y = 5 # This code does nothing
    final = "done!"  # output
    """)
    expected_outputs = {'x': 'x', 'final': 'final'}
    outputs = get_output_var_names(script)
    assert outputs == expected_outputs


def test_specify_output_variables_gets_new_varnames():
    script = dedent("""
        x = 3 # output:First
        y = 5 # output:Second
    """)
    outputs = get_output_var_names(script)
    assert outputs == {'First': 'x', 'Second': 'y'}



def test_replace_input_variables():
    code = dedent("""
    x = 3  # input
    y = 5
    """)
    replacement = {'x': 10}
    expected_result = dedent("""
    x = 10  # input
    y = 5
    """)
    result = replace_inputs(code, replacement, 'input')
    assert result == expected_result

def test_replace_input_variables_with_new_varnames():
    code = dedent("""
    x = 3  # input:First
    y = 5  # input:Second
    z = 1  # input
    """)
    replacement = {'First': 10, 'Second': 50, 'z': 30}
    expected_result = dedent("""
    x = 10  # input:First
    y = 50  # input:Second
    z = 30  # input
    """)
    result = replace_inputs(code, replacement, 'input')
    assert result == expected_result


def test_call_on_general_script():
    code = dedent("""
    x = 3  # input
    y = 4  # input
    z = x + y  # output
    """)
    results = call(code, x=10, y=20)
    assert results['z'] == 30


def test_call_on_general_script_has_original_values_as_defaults():
    code = dedent("""
    x = 3  # input
    y = 4  # input
    z = x + y  # output
    """)
    results = call(code, x=10)
    assert results['z'] == 14

