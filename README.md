# nice_duration

A Python library for formatting durations in a human-readable way. Convert `timedelta` objects or numeric time values into readable strings like `3h20m` or `2w5d`. This module features optional micro-second precision, configurable separators and flexible handling of zero-values.

## Quick Start

```python
from datetime import timedelta
from nice_duration import duration_string

# From timedelta objects
duration_string(timedelta(hours=3, minutes=20))  # "3h20m"

# From seconds (int or float)
duration_string(seconds=200)    # "3m20s"
duration_string(seconds=200.9)  # "3h20m" (truncated)

# From milliseconds or microseconds
duration_string(milliseconds=1500)  # "1s" (with default precision)
duration_string(microseconds=1500000)  # "1s"
```

## Precision Control
Control the smallest unit displayed. The `precision` parameter can be one of `weeks`,
`days`, `hours`, `minutes`, `seconds`, `milliseconds` or `microseconds`.

```python
delta = timedelta(weeks=2, days=3, hours=4, minutes=5, seconds=30, microseconds=500000)

duration_string(delta, precision="weeks")        # "2w"
duration_string(delta, precision="minutes")      # "2w3d4h5m"
duration_string(delta, precision="seconds")      # "2w3d4h5m30s"
duration_string(delta, precision="milliseconds") # "2w3d4h5m30s500ms"

```

## Flexible Zero Handling
By default, zero values are omitted, but zeroes can be left alone when leading, trailing or infix.

```python
delta = timedelta(days=3, minutes=12)  # Note: no hours

duration_string(delta)                          # "3d12m"
duration_string(delta, infix_zeroes=True)       # "3d0h12m"
duration_string(delta, leading_zeroes=True)     # "0w3d12m"
duration_string(delta, trailing_zeroes=True)    # "3d12m0s"
duration_string(delta, all_zeroes=True)         # "0w3d0h12m0s"
```

##  Custom Separators
Add spacing or custom separators between units:

```python
delta = timedelta(hours=3, minutes=20)

duration_string(delta, separator=" ")     # "3h 20m"
```

## Limitations

- Maximum unit is weeks (because bigger units have no fixed length)
- Float values are truncated

## License

This project is licensed under the MIT License.
