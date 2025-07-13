from datetime import timedelta as td

UNITS = {
    "weeks": {"abbreviation": "w", "µs_per_unit": 7 * 24 * 60 * 60 * 1000 * 1000},
    "days": {"abbreviation": "d", "µs_per_unit": 24 * 60 * 60 * 1000 * 1000},
    "hours": {"abbreviation": "h", "µs_per_unit": 60 * 60 * 1000 * 1000},
    "minutes": {"abbreviation": "m", "µs_per_unit": 60 * 1000 * 1000},
    "seconds": {"abbreviation": "s", "µs_per_unit": 1000 * 1000},
    "milliseconds": {"abbreviation": "ms", "µs_per_unit": 1000},
    "microseconds": {"abbreviation": "µs", "µs_per_unit": 1},
}


def _keep_specified_zeroes(
    values, leading_zeroes=False, trailing_zeroes=False, infix_zeroes=False
):
    """Given a values list, which is a list of pairs of units and amounts,
    return a values list that has leading zeroes removed (if
    requested), trailing zeroes removed (if requested) and infix
    zeroes remove (if requested).
    """

    non_zero_indices = [i for i, (_, value) in enumerate(values) if value]

    if not non_zero_indices:
        # If all values are zero, keep them all if any flag is set.
        return values if any([leading_zeroes, trailing_zeroes, infix_zeroes]) else []

    first_non_zero_index = non_zero_indices[0]
    last_non_zero_index = non_zero_indices[-1]

    result = []
    for i, pair in enumerate(values):
        if pair[1] != 0:
            result.append(pair)
            continue

        # It's a zero value, decide whether to keep it.
        is_leading = i < first_non_zero_index
        is_trailing = i > last_non_zero_index
        is_infix = first_non_zero_index < i < last_non_zero_index

        if (
            (is_leading and leading_zeroes)
            or (is_trailing and trailing_zeroes)
            or (is_infix and infix_zeroes)
        ):
            result.append(pair)

    return result


def duration_string(
    *,
    timedelta: td = None,
    seconds: int | float = None,
    milliseconds: int | float = None,
    microseconds: int | float = None,
    separator="",
    leading_zeroes=False,
    trailing_zeroes=False,
    infix_zeroes=False,
    all_zeroes=False,
    precision="seconds",
) -> str:
    """Convert a timedelta object or numeric time value to a human-readable string.

    Accepts exactly one duration input: either a timedelta object, or a numeric value
    in seconds, milliseconds, or microseconds. Float values are truncated to integers.

    Args:
        timedelta: A timedelta object
        seconds: Number of seconds (int or float)
        milliseconds: Number of milliseconds (int or float)
        microseconds: Number of microseconds (int or float)
        separator: String to insert between time units (default: "")
        leading_zeroes: Include leading zero values
        trailing_zeroes: Include trailing zero values
        infix_zeroes: Include zero values apart from leading and trailing
        all_zeroes: Include all zero values (equivalent to all three zero options)
        precision: Stop conversion at this unit ("weeks", "days", "hours",
                  "minutes", "seconds", "milliseconds", "microseconds")

    Returns:
        Nice duration string

    Raises:
        TypeError: If invalid input types are provided, multiple time inputs are
                  given, no time input is provided, or invalid precision unit is specified

    Examples:
        duration_string((timedelta=td(hours=3, minutes=20)) -> "3h20m"
        duration_string((timedelta=td(hours=3, minutes=20), separator=" ") -> "3h 20m"
        duration_string((timedelta=td(hours=3, minutes=20), all_zeroes=True, precision="microseconds") -> "0w0d3h20m0s0ms0µs"
        duration_string((timedelta=td(hours=3, minutes=20), precision="hours") -> "3h"
        duration_string((seconds=-131.9) -> "-2m11s"
        duration_string((milliseconds=1500, precision="milliseconds") -> "1s500ms"
        duration_string((microseconds=1500000, precision="milliseconds") -> "1s500ms"
    """
    if timedelta and not isinstance(timedelta, td):
        raise TypeError(
            f"Expected timedelta for timedelta, got {type(timedelta).__name__}"
        )

    if seconds and not isinstance(seconds, (int, float)):
        raise TypeError(
            f"Expected int or float for seconds, got {type(seconds).__name__}"
        )

    if milliseconds and not isinstance(milliseconds, (int, float)):
        raise TypeError(
            f"Expected int or float for milliseconds, got {type(milliseconds).__name__}"
        )

    if microseconds and not isinstance(microseconds, (int, float)):
        raise TypeError(
            f"Expected int or float for microseconds, got {type(microseconds).__name__}"
        )

    amount_of_durations = len(
        [p for p in [timedelta, seconds, milliseconds, microseconds] if p is not None]
    )
    if amount_of_durations == 0:
        raise TypeError(
            "Expected one of timedelta, seconds, milliseconds or microseconds to have a value."
        )

    if amount_of_durations > 1:
        raise TypeError(
            "Expected only one of timedelta, seconds, milliseconds or microseconds to have a value."
        )

    if precision not in UNITS:
        raise TypeError(f"Expected precision to be one of {', '.join(UNITS)}.")

    if all_zeroes:
        leading_zeroes = True
        infix_zeroes = True
        trailing_zeroes = True

    if timedelta is not None:
        total_microseconds = int(timedelta.total_seconds()) * 1000 * 1000 + int(
            timedelta.microseconds
        )
    elif seconds is not None:
        total_microseconds = int(seconds * 1000 * 1000)
    elif milliseconds is not None:
        total_microseconds = int(milliseconds * 1000)
    else:
        total_microseconds = int(microseconds)

    is_negative = total_microseconds < 0
    total_microseconds = abs(total_microseconds)

    values = []
    remainder = total_microseconds

    for unit, unit_info in UNITS.items():
        value, remainder = divmod(remainder, unit_info["µs_per_unit"])
        values.append([unit, value])
        if unit == precision:
            break

    values = _keep_specified_zeroes(
        values,
        leading_zeroes=leading_zeroes,
        trailing_zeroes=trailing_zeroes,
        infix_zeroes=infix_zeroes,
    )

    if not values:
        values = [[precision, 0]]

    parts = [f"{e[1]}{UNITS[e[0]]['abbreviation']}" for e in values]
    duration_string = separator.join(parts)

    has_non_zero_values = any(v[1] for v in values)
    if is_negative and has_non_zero_values:
        duration_string = "-" + duration_string

    return duration_string
