# nice_duration

This is a Python module that introduces a way of formatting a
`timedelta` instance like so: `3h12m`. It can also format an `int` or
a `float` representing a number of seconds in the same way. A `float`
is just converted to an `int`, so `70.9` is converted to `70`.

The `separator` parameter, which defaults to the empty string,
determines what the individual components are concatenated with.
Setting `separator` to a single space changes the above example to
`3h 12m`.

Components with value 0 are left out. That can be changed by setting
 - `leading_zeroes`
 - `trailing_zeroes`
 - `infix_zeroes`

For example, by setting `trailing_zeroes` to `True`, the example `duration_string` is
changed to `3h12m0s`.

For convenience, setting `all_zeroes` to `True` will set all three to `True`.

## Examples
```python
>>> from datetime import timedelta
>>> from nice_duration import duration_string
>>> delta = timedelta(hours=3, minutes=20)
>>> duration_string(delta)
'3h20m'
```

```python
>>> duration_string(200) # When an int is given, it is interpreted as a number of seconds
'3h20m'
```

```python
>>> duration_string(200.3) # When a float is given, it is converted to an int and interpreted as a number of seconds
'3h20m'
```

Setting `separator`:

```python
>>> duration_string(delta, separator=" ")
'3h 20m'
```

Setting `all_zeroes`:

```python
>>> duration_string(delta, all_zeroes=True)
'0w0d3h20m0s'
```

Setting `trailing_zeroes`:
```python
>>> duration_string(delta, trailing_zeroes=True)
'3h20m0s'
```

Setting `leading_zeroes`:
```python
>>> duration_string(delta, leading_zeroes=True)
'0w0d3h20m'
```

Setting `infix_zeroes`:
```python
>>> duration_string(timedelta(hours=3, seconds=11), infix_zeroes=True)
'3h0m11s'
```

Return value when `timedelta` is 0:
```python
>>> duration_string(timedelta())
'0s'
```
