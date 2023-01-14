[![PyPI version](https://badge.fury.io/py/callscript.svg)](https://badge.fury.io/py/callscript)
[![Python package](https://github.com/nickdelgrosso/callscript/actions/workflows/python-package.yml/badge.svg)](https://github.com/nickdelgrosso/callscript/actions/workflows/python-package.yml)
[![Coverage Status](https://coveralls.io/repos/github/nickdelgrosso/callscript/badge.svg?branch=main)](https://coveralls.io/github/nickdelgrosso/callscript?branch=main)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)


# Callscript

Not worth it to refactor your script into a bunch of functions?  This is a simple python library that lets you run your script as though you had, so you can
call `results = callscript('myscript.py', x=3, y=4)`.  Just add comments in your scirpt to show where the inputs and outputs are, and `callscript` will
make the function work properly:

```python
# myscript.py
x = 1      # input
y = 2      # input
w = x * y
v = x / y  # output
z = x + y  # output
print(z)   # ignore
```

Why does this exist?  Because sometimes you don't want to touch your old code or want to keep working with it using an interactive coding tool like Spyder, VSCode's interactive mode, or Jupyter, but you still want to be able to test your script using new parameters, or wrap it with a user interface. 

Or maybe you're not sure how to go about changing the script's code to make it work in a new context and don't have a lot of time at the moment to work it out, or maybe you're collaborating with someone who isn't ready to refactor the script yet.  

In any case,  with `callscript`, you can leave the original script alone and wrap it with your new functionality.




## Installation

Install `callscript` with PyPI

```bash
  pip install callscript
```
    
## Usage / Examples


### Simple Input-Output Labeling

If you label your script with the "input" or "output" comments, `callscript` can call it!


```python
# examples/script.py
x = 3  # input
y = 5  # input
z = x + y  # output
```

Then from your other code, you can call it with the `callscript()` function:

```python
>>> from callscript import callscript
>>> callscript('examples/script.py', x=10, y=20)
{'z': 30}

```

### Modifying Input-Output Variable Names for your Function's API

Want to change your variable names? You can do that, too!

```python
# examples/script2.py
x = 3  # input:FirstWeek
y = 5  # input:SecondWeek
z = x + y  # output:sum
```

```python
>>> callscript('examples/script2.py', FirstWeek=10, SecondWeek=20)
{'sum': 30}

```


### Ignoring Lines When the Script is Called as a Function

Want some lines to be ignored when being called by `callscript()`?  Use the `# ignore` tag!

```python
# examples/script3.py
x = 3  # input
y = 5  # input
input('What is your name?')  # ignore
z = x + y  # output
z = 100000   # ignore
```

```python
>>> callscript('examples/script3.py', x=10, y=20)
{'z': 30}

```

### Using the Orignal Script Values as Function Defaults

`callscript()` will automatically use the original values of the inputs in the script as defaults.

```python
# examples/script4.py
name = 'Nick'          # input
greeting = 'Hello, '   # input
msg = greeting + name  # output
```

```python
>>> callscript('examples/script4.py', name='Emma')
{'msg': 'Hello, Emma'}

```
## Authors

- [Nicholas A. Del Grosso](https://www.github.com/nickdelgrosso)

## Running Tests

To run tests, run the following command

```bash
  tox
```



## Contributing

### Adding to the Changelog
  
Don't modify the `CHANGELOG.rst` file directly!  Instead, use`scriv create` make a new entry for the changelog.  After you've written a contribution, add the entry and write what  you did into the template.   When we are ready to make a release, we'll use the `scriv collect` command to aggregate these fragments into a new changeelog entry.