# callscript

Want to add a GUI, CLI, or simply test your script, but you don't want to modify your code?  Call a script as though it were a function!  

## Installation

`pip install callscript`


## Usage:

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

`callscript()` will use the original values of the inputs in the script as defaults.

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