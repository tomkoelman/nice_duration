from datetime import timedelta as td
from nice_duration import duration_string as ds


def test_examples_from_docstring():
    """This tests the examples from the nice_duration docstring"""
    assert (ds(timedelta=td(hours=3, minutes=20))) == "3h20m"
    assert (ds(timedelta=td(hours=3, minutes=20), separator=" ")) == "3h 20m"
    assert (
        ds(timedelta=td(hours=3, minutes=20), all_zeroes=True, precision="microseconds")
    ) == "0w0d3h20m0s0ms0µs"
    assert (ds(timedelta=td(hours=3, minutes=20), precision="hours")) == "3h"
    assert (ds(seconds=-131.9)) == "-2m11s"
    assert (ds(milliseconds=1500, precision="milliseconds")) == "1s500ms"
    assert (ds(microseconds=1500000, precision="milliseconds")) == "1s500ms"
