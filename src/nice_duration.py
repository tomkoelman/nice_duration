from datetime import timedelta

amount_of_seconds = {
    "week": 604800,
    "day": 86400,
    "hour": 3600,
    "minute": 60,
    "second": 1,
}
unit_names = {"week": "w", "day": "d", "hour": "h", "minute": "m", "second": "s"}


def duration_string(
    duration: timedelta | int | float,
    separator="",
    leading_zeroes=False,
    trailing_zeroes=False,
    infix_zeroes=False,
    all_zeroes=False,
) -> str:
    """Convert a timedelta object to a string.

    Examples:
    duration_string(timedelta(hours=3, minutes=20)) = "3h20m"
    duration_string(timedelta(hours=3, minutes=20), separator=" ") = "3h 20m"
    duration_string(timedelta(hours=3, minutes=20), all_zeroes=True) = "0w0d3h20m0s"
    """

    if all_zeroes:
        leading_zeroes = True
        infix_zeroes = True
        trailing_zeroes = True

    if type(duration) is int:
        remainder = duration
    elif type(duration) is float:
        remainder = int(duration)
    else:
        remainder = int(duration.total_seconds())

    values = {}

    for field in amount_of_seconds.keys():
        value, remainder = divmod(remainder, amount_of_seconds[field])
        values[field] = value

    if not leading_zeroes:
        for field in values.copy():
            if values[field]:
                break
            else:
                del values[field]

    if not trailing_zeroes:
        for field in reversed(values.copy()):
            if values[field]:
                break
            else:
                del values[field]

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
        # sure there are no infix zeroes.
        if len(values_list) - len(leading_zeroes) - len(trailing_zeroes) > 2:
            # Remove leading and trailing zeroes from values_list
            values_list = values_list[
                len(leading_zeroes) : len(values_list) - len(trailing_zeroes)
            ]

            # In this remaining list we can remove all zero values
            values_list = [e for e in values_list if e[1]]

            # Infix zeroes are removed. Now re-attach leading and trailing zeroes
            new_list = leading_zeroes
            new_list.extend(values_list)
            new_list.extend(trailing_zeroes)

            # We convert the list of pairs back to a dictionary
            values = {e[0]: e[1] for e in new_list}

    if not values:
        values["second"] = 0

    string = ""
    for field in values:
        string += separator + str(values[field]) + unit_names[field]

    string = string[len(separator) :]
    return string
