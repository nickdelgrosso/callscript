# callscript

Want to add a GUI, CLI, or simply test your script, but you don't want to modify your code?  Call a script as though it were a function!  

## Usage:

If you label your script with the "input" or "output" comments, `callscript` can call it!


```python
# script.py
x = 3  # input
y = 5  # input
z = 10 + 5  # output
```

Then from your other code, you can call it with the `callscript()` function:

```python
>>> from callscript import callscript
>>> callscript('script.py', x=10, y=20)
{'z': 30}
```

Want to change your variable names? You can do that, too!

```python
# script.py
x = 3  # input:FirstWeek
y = 5  # input:SecondWeek
z = 10 + 5  # output:sum
```

```python
>>> from callscript import callscript
>>> callscript('script.py', FirstWeek=10, SecondWeek=20)
{'sum': 30}
```


## Installation

`pip install callscript`



