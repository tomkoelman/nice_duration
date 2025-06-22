from datetime import timedelta

UNITS = {
    "weeks": {"abbreviation": "w", "μs_per_unit": 7 * 24 * 60 * 60 * 1000 * 1000},
    "days": {"abbreviation": "d", "μs_per_unit": 24 * 60 * 60 * 1000 * 1000},
    "hours": {"abbreviation": "h", "μs_per_unit": 60 * 60 * 1000 * 1000},
    "minutes": {"abbreviation": "m", "μs_per_unit": 60 * 1000 * 1000},
    "seconds": {"abbreviation": "s", "μs_per_unit": 1000 * 1000},
    "milliseconds": {"abbreviation": "ms", "μs_per_unit": 1000},
    "microseconds": {"abbreviation": "μs", "μs_per_unit": 1},
}


def _keep_specified_zeroes(
    values, leading_zeroes=False, trailing_zeroes=False, infix_zeroes=False
):
    """Given a values list, which is a list of pairs of units and amounts,
    return a values list that has leading zeroes removed (if
    requested), trailing zeroes removed (if requested) and infix
    zeroes remove (if requested).
    """

    leading = []
    trailing = []

    # Find index for first pair where value is non-zero
    first_non_zero_index = next((i for i, e in enumerate(values) if e[1]), 0)

    # Find index for last pair where value is non-zero
    last_non_zero_index = len(values) - next(
        (i for i, e in enumerate(reversed(values)) if e[1]), 0
    )

    if leading_zeroes:
        # Put leading zeroes in `leading`
        leading = values[:first_non_zero_index]

    if trailing_zeroes:
        # Put trailing zeroes in `trailing`
        trailing = values[last_non_zero_index:]

    # Infix is the bit in between the found indices
    infix = values[first_non_zero_index:last_non_zero_index]

    # Remove all zeroes from infix if we are not interested in them
    if not infix_zeroes:
        infix = [e for e in infix if e[1]]

    return leading + infix + trailing


def duration_string(
    duration: timedelta = None,
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
    """Convert a timedelta object or numeric seconds to a human-readable string.

    When `duration` is a float, it is truncated to an `int`.

    Examples:
    duration_string(timedelta(hours=3, minutes=20)) = "3h20m"
    duration_string(timedelta(hours=3, minutes=20), separator=" ") = "3h 20m"
    duration_string(timedelta(hours=3, minutes=20), all_zeroes=True) = "0w0d3h20m0s"
    duration_string(timedelta(hours=3, minutes=20), precision="hours") = "3h"
    duration_string(seconds=131) = "2m11s"
    duration_string(seconds=131.9) = "2m11s"
    duration_string(seconds=-131) = "-2m11s"
    duration_string(timedelta(seconds=-75)) = "-1m15s"
    """

    if duration and not isinstance(duration, timedelta):
        raise TypeError(
            f"Expected timedelta for duration, got {type(duration).__name__}"
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
        [p for p in [duration, seconds, milliseconds, microseconds] if p]
    )
    if amount_of_durations == 0:
        raise TypeError(
            "Expected one of duration, seconds, milliseconds of microseconds to have a value."
        )

    if amount_of_durations > 1:
        raise TypeError(
            "Expected only one of duration, seconds, milliseconds of microseconds to have a value."
        )

    if precision not in UNITS:
        raise TypeError(f"Expected precision to be one of {', '.join(UNITS)}.")

    if all_zeroes:
        leading_zeroes = True
        infix_zeroes = True
        trailing_zeroes = True

    if duration:
        total_microseconds = int(duration.total_seconds()) * 1000 * 1000 + int(
            duration.microseconds
        )
    elif seconds:
        total_microseconds = int(seconds * 1000 * 1000)
    elif milliseconds:
        total_microseconds = int(milliseconds * 1000)
    else:
        total_microseconds = microseconds

    is_negative = total_microseconds < 0
    total_microseconds = abs(total_microseconds)

    values = []
    remainder = total_microseconds

    for unit, unit_info in UNITS.items():
        value, remainder = divmod(remainder, unit_info["μs_per_unit"])
        values.append([unit, value])
        if unit == precision:
            break

    values = _keep_specified_zeroes(
        values,
        leading_zeroes=leading_zeroes,
        trailing_zeroes=trailing_zeroes,
        infix_zeroes=infix_zeroes,
    )

    if len(values) == 0:
        values = [[precision, 0]]

    parts = [f"{e[1]}{UNITS[e[0]]['abbreviation']}" for e in values]
    duration_string = separator.join(parts)

    if is_negative and duration_string != "0s":
        duration_string = "-" + duration_string

    return duration_string
