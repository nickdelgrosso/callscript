

from textwrap import dedent

import pytest
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



def test_call_can_override_names():
    code = dedent("""
    x = 3  # input:hi
    y = 4  # input: bye
    z = x - y  # output:diff
    w = x + y  # output: sum
    """)
    results = call(code, hi=10, bye=6)
    assert 'z' not in results
    assert results['diff'] == 4
    assert results['sum'] == 16


def test_callscript1():
    results = callscript('examples/script.py', x=10, y=30)
    assert results == {'z': 40}


def test_ignores_lines():
    code = dedent("""
    x = 3  # input
    y = 5  # input
    z = x + y  # output
    z += 1  # ignore
    """)
    results = call(code, x=10, y=20)
    assert results['z'] == 30


def test_typeerror_on_nonmatching_inputs():
    code = dedent("""
    x = 3  # input
    """)
    with pytest.raises(TypeError) as exc:
        call(code, y=10)
    

def test_typeerror_on_nonmatching_inputs_for_newnames():
    code = dedent("""
    x = 3  # input: y
    """)
    call(code, y=10)
    with pytest.raises(TypeError) as exc:
        call(code, x=10)
    assert f"got an unexpected keyword argument 'x'" in str(exc.value)
    call(code, y=10)


def test_typeerror_lists_possible_inputs():
    code = dedent("""
    monty = 3  # input
    python = 4  # input: crazy
    circus = 5
    show = 6  # output
    """)
    with pytest.raises(TypeError) as exc:
        call(code, x=10)
    for name in ['monty', 'crazy']:
        assert name in str(exc.value)
    for name in ['circus', 'show']:
        assert name not in str(exc.value)



# def test_namerror_shows_proper_traceback_with_source_code_for_debugging():
#     code = dedent("""
#     x = 4 # input
#     z = g + x  # output
#     """)
#     with pytest.raises(NameError) as exc:
#         call(code, x=5)
#     for tb in exc.traceback:
#         assert tb.frame.code.fullsource  # All levels of traceback should show source code, for debugging