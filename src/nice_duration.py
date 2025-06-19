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
    """Given a values dict, which is an ordered mapping from unit to
    amount, return a values dict that has leading zeroes removed (if
    requested), trailing zeroes removed (if requested) and infix
    zeroes remove (if requested).
    """

    values = values.copy()

    if not leading_zeroes:
        # Remove all values that are 0 from the beginning of the values dict
        for unit, value in values.copy().items():
            if value:
                break
            else:
                del values[unit]

    if not trailing_zeroes:
        # Remove all values that are 0 from the end of the values dict
        for unit, value in reversed(values.copy().items()):
            if value:
                break
            else:
                del values[unit]

    # Removing infix zeroes only makes sense when there are more than
    # 2 values left
    if not infix_zeroes and len(values) > 2:
        # We transform the values dictionary to a list of pairs
        values_list = [[k, v] for k, v in values.items()]

        # We split off potential leading zeroes
        leading_zeroes = []
        for e in values_list:
            if e[1]:
                break
            else:
                leading_zeroes.append(e)

        # We split off potential trailing zeroes
        trailing_zeroes = []
        for e in reversed(values_list):
            if e[1]:
                break
            else:
                trailing_zeroes.insert(0, e)

        # Check whether there are enough elements left between leading
        # zeroes and trailing zeroes. If there are less than 3
        # elements beteen leading and trailing zeroes, we know for
        # sure there are no infix zeroes, because an infix zero needs
        # values on both sides.
        if len(values_list) - len(leading_zeroes) - len(trailing_zeroes) > 2:
            # Remove leading and trailing zeroes from values_list
            values_list = values_list[
                len(leading_zeroes) : len(values_list) - len(trailing_zeroes)
            ]

            # In this remaining list we can remove all zero values
            values_list = [e for e in values_list if e[1]]

            # Infix zeroes are removed. Now re-attach leading and trailing zeroes
            new_list = leading_zeroes + values_list + trailing_zeroes

            # We convert the list of pairs back to a dictionary
            return {e[0]: e[1] for e in new_list}

    return values


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

    values = {}
    remainder = total_seconds

    for unit, seconds_per_unit in SECONDS_PER_UNIT.items():
        value, remainder = divmod(remainder, seconds_per_unit)
        values[unit] = value

    values = _keep_specified_zeroes(
        values,
        leading_zeroes=leading_zeroes,
        trailing_zeroes=trailing_zeroes,
        infix_zeroes=infix_zeroes,
    )

    if not values:
        values["second"] = 0

    parts = [f"{value}{UNIT_ABBREVIATIONS[unit]}" for unit, value in values.items()]
    duration_string = separator.join(parts)

    if is_negative and duration_string != "0s":
        duration_string = "-" + duration_string

    return duration_string
