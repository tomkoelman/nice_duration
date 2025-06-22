from datetime import timedelta

SECONDS_PER_UNIT = {
    "week": 604800,
    "day": 86400,
    "hour": 3600,
    "minute": 60,
    "second": 1,
}
UNIT_ABBREVIATIONS = {
    "week": "w",
    "day": "d",
    "hour": "h",
    "minute": "m",
    "second": "s",
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

    # Return what's left
    return leading + infix + trailing


def duration_string(
    duration: timedelta | int | float,
    separator="",
    leading_zeroes=False,
    trailing_zeroes=False,
    infix_zeroes=False,
    all_zeroes=False,
) -> str:
    """Convert a timedelta object or numeric seconds to a human-readable string.

    Examples:
    duration_string(timedelta(hours=3, minutes=20)) = "3h20m"
    duration_string(timedelta(hours=3, minutes=20), separator=" ") = "3h 20m"
    duration_string(timedelta(hours=3, minutes=20), all_zeroes=True) = "0w0d3h20m0s"
    duration_string(131) = "2m11s"
    duration_string(131.9) = "2m11s"
    duration_string(-131) = "-2m11s"
    duration_string(timedelta(seconds=-75)) = "-1m15s"
    """

    if all_zeroes:
        leading_zeroes = True
        infix_zeroes = True
        trailing_zeroes = True

    if isinstance(duration, timedelta):
        total_seconds = int(duration.total_seconds())
    else:
        total_seconds = int(duration)

    is_negative = total_seconds < 0
    total_seconds = abs(total_seconds)

    values = []
    remainder = total_seconds

    for unit, seconds_per_unit in SECONDS_PER_UNIT.items():
        value, remainder = divmod(remainder, seconds_per_unit)
        values.append([unit, value])

    values = _keep_specified_zeroes(
        values,
        leading_zeroes=leading_zeroes,
        trailing_zeroes=trailing_zeroes,
        infix_zeroes=infix_zeroes,
    )

    if not values:
        values = [["second", 0]]

    parts = [f"{e[1]}{UNIT_ABBREVIATIONS[e[0]]}" for e in values]
    duration_string = separator.join(parts)

    if is_negative and duration_string != "0s":
        duration_string = "-" + duration_string

    return duration_string
