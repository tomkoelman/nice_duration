from datetime import timedelta as td
from nice_duration import duration_string as ds


def test_empty_timedelta():
    delta = td(seconds=0)
    assert ds(delta) == "0s"
    assert ds(delta, all_zeroes=True) == "0w0d0h0m0s"


def test_separator():
    delta = td(hours=300, minutes=70)
    assert ds(delta, separator=" ") == "1w 5d 13h 10m"


def test_keeping_zeroes():
    delta = td(days=3, minutes=12)
    assert ds(delta) == "3d12m"
    assert ds(delta, infix_zeroes=True) == "3d0h12m"
    assert ds(delta, leading_zeroes=True) == "0w3d12m"
    assert ds(delta, trailing_zeroes=True) == "3d12m0s"
    assert ds(delta, leading_zeroes=True, trailing_zeroes=True) == "0w3d12m0s"
    assert (
        ds(
            delta,
            leading_zeroes=True,
            trailing_zeroes=True,
            infix_zeroes=True,
        )
        == "0w3d0h12m0s"
    )
    assert ds(delta, all_zeroes=True) == "0w3d0h12m0s"


def test_call_with_number_of_seconds():
    assert ds(70) == "1m10s"

def test_call_with_number_of_seconds_float():
    assert ds(70.4) == "1m10s"
    assert ds(70.9) == "1m10s"
