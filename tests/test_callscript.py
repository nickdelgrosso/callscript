

from textwrap import dedent
from callscript.callscript import get_output_var_names, munge_input_values, call, callscript, strip_ignored_lines

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



def test_call_on_general_script():
    code = dedent("""
    x = 3  # input
    y = 4  # input
    z = x + y  # output
    """)
    results = call(code, x=10, y=20)
    assert results['z'] == 30


def test_call_on_general_script_strings():
    code = dedent("""
    x = 3  # input
    y = 4  # input
    z = x + y  # output
    """)
    results = call(code, x='Hello', y='World')
    assert results['z'] == 'HelloWorld'


def test_call_on_general_script_has_original_values_as_defaults():
    code = dedent("""
    x = 3  # input
    y = 4  # input
    z = x + y  # output
    """)
    results = call(code, x=10)
    assert results['z'] == 14



def test_callscript1():
    results = callscript('examples/script.py', x=10, y=30)
    assert results == {'z': 40}


def test_munging():
    code = dedent("""
    x = 3  # input
    y = 5
    """)
    new_code = munge_input_values(code, "input")
    expected_result = dedent("""
    x = __x  # input
    y = 5
    """)
    assert new_code == expected_result


def test_munging_varname_change():
    code = dedent("""
    x = 3  # input:Hello
    y = 5  # input:World
    """)
    new_code = munge_input_values(code, "input")
    expected_result = dedent("""
    x = __Hello  # input:Hello
    y = __World  # input:World
    """)
    assert new_code == expected_result


def test_ignore_specified_lines():
    code = dedent("""
    a = 5  # ignore
    b = "hello"  # input:Hello
    c = "world" # ignore
    d = 8
    e = 4.2  # output
    """)
    new_code = strip_ignored_lines(code, "ignore")
    expected_result = dedent("""
    b = "hello"  # input:Hello
    d = 8
    e = 4.2  # output
    """)
    assert new_code == expected_result


def test_callscript_ignores_lines():
    code = dedent("""
    x = 3  # input
    y = 5  # input
    z = x + y  # output
    z += 1  # ignore
    """)
    results = call(code, x=10, y=20)
    assert results['z'] == 30