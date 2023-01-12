

from textwrap import dedent
from callscript.callscript import call, callscript



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


def test_callscript_ignores_lines():
    code = dedent("""
    x = 3  # input
    y = 5  # input
    z = x + y  # output
    z += 1  # ignore
    """)
    results = call(code, x=10, y=20)
    assert results['z'] == 30