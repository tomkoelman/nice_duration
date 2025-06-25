from datetime import timedelta as td
from nice_duration import duration_string as ds
from nice_duration import _keep_specified_zeroes as _ks0
import pytest


def test_empty_timedelta():
    delta = td(seconds=0)
    assert ds(timedelta=delta) == "0s"
    assert ds(timedelta=delta, precision="hours") == "0h"
    assert ds(timedelta=delta, all_zeroes=True) == "0w0d0h0m0s"


def test_separator():
    delta = td(hours=300, minutes=70)
    assert ds(timedelta=delta, separator=" ") == "1w 5d 13h 10m"


def test_keeping_zeroes():
    delta = td(days=3, minutes=12)
    assert ds(timedelta=delta) == "3d12m"
    assert ds(timedelta=delta, infix_zeroes=True) == "3d0h12m"
    assert ds(timedelta=delta, leading_zeroes=True) == "0w3d12m"
    assert ds(timedelta=delta, trailing_zeroes=True) == "3d12m0s"
    assert ds(timedelta=delta, leading_zeroes=True, trailing_zeroes=True) == "0w3d12m0s"
    assert (
        ds(
            timedelta=delta,
            leading_zeroes=True,
            trailing_zeroes=True,
            infix_zeroes=True,
        )
        == "0w3d0h12m0s"
    )
    assert ds(timedelta=delta, all_zeroes=True) == "0w3d0h12m0s"


def test_call_with_number_of_seconds_float():
    assert ds(seconds=70.4) == "1m10s"
    assert ds(seconds=70.9) == "1m10s"


def test_call_with_negative_number():
    assert ds(seconds=-61) == "-1m1s"
    assert ds(seconds=-0) == "0s"


def test_keep_specified_zeroes():
    assert _ks0([["week", 0], ["hour", 1], ["minute", 1]]) == [
        ["hour", 1],
        ["minute", 1],
    ]
    assert _ks0([["week", 0], ["hour", 1], ["minute", 1]], leading_zeroes=True) == [
        ["week", 0],
        ["hour", 1],
        ["minute", 1],
    ]
    assert _ks0([["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]]) == [
        ["b", 1],
        ["e", 1],
    ]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]],
        leading_zeroes=True,
    ) == [["a", 0], ["b", 1], ["e", 1]]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]],
        trailing_zeroes=True,
    ) == [["b", 1], ["e", 1], ["f", 0]]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]], infix_zeroes=True
    ) == [["b", 1], ["c", 0], ["d", 0], ["e", 1]]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]],
        leading_zeroes=True,
        infix_zeroes=True,
    ) == [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1]]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]],
        trailing_zeroes=True,
        infix_zeroes=True,
    ) == [["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]]
    assert _ks0(
        [["a", 0], ["b", 1], ["c", 0], ["d", 0], ["e", 1], ["f", 0]],
        trailing_zeroes=True,
        leading_zeroes=True,
    ) == [["a", 0], ["b", 1], ["e", 1], ["f", 0]]


def test_precision_parameter():
    delta = td(weeks=2, days=3, hours=4, minutes=5, seconds=30, microseconds=500000)

    # Test precision at different levels
    assert ds(timedelta=delta, precision="weeks") == "2w"
    assert ds(timedelta=delta, precision="days") == "2w3d"
    assert ds(timedelta=delta, precision="hours") == "2w3d4h"
    assert ds(timedelta=delta, precision="minutes") == "2w3d4h5m"
    assert ds(timedelta=delta, precision="seconds") == "2w3d4h5m30s"
    assert ds(timedelta=delta, precision="milliseconds") == "2w3d4h5m30s500ms"

    delta = td(weeks=2, days=3, hours=4, minutes=5, seconds=30, microseconds=500)
    assert ds(timedelta=delta, precision="microseconds") == "2w3d4h5m30s500µs"


def test_precision_with_zero_values():
    delta = td(seconds=0)
    assert ds(timedelta=delta, precision="weeks") == "0w"
    assert ds(timedelta=delta, precision="days") == "0d"
    assert ds(timedelta=delta, precision="hours") == "0h"
    assert ds(timedelta=delta, precision="minutes") == "0m"
    assert ds(timedelta=delta, precision="seconds") == "0s"
    assert ds(timedelta=delta, precision="milliseconds") == "0ms"
    assert ds(timedelta=delta, precision="microseconds") == "0µs"


def test_milliseconds_parameter_float():
    assert (
        ds(milliseconds=1500.7, precision="milliseconds") == "1s500ms"
    )  # Should truncate
    assert ds(milliseconds=999.9, precision="milliseconds") == "999ms"


def test_microseconds_parameter():
    assert ds(microseconds=0, precision="microseconds") == "0µs"
    assert ds(microseconds=500, precision="microseconds") == "500µs"
    assert ds(microseconds=1000, precision="microseconds") == "1ms"
    assert ds(microseconds=1500, precision="microseconds") == "1ms500µs"
    assert ds(microseconds=1000000, precision="microseconds") == "1s"
    assert ds(microseconds=1001500, precision="microseconds") == "1s1ms500µs"
    assert ds(microseconds=61001500, precision="microseconds") == "1m1s1ms500µs"


def test_microseconds_parameter_float():
    assert ds(microseconds=1500.7, precision="microseconds") == "1ms500µs"
    assert ds(microseconds=999.9, precision="microseconds") == "999µs"


def test_multiple_timedelta_parameters_error():
    with pytest.raises(TypeError):
        ds(seconds=60, milliseconds=1000)

    with pytest.raises(TypeError):
        ds(seconds=60, microseconds=1000000)

    with pytest.raises(TypeError):
        ds(milliseconds=1000, microseconds=1000000)

    with pytest.raises(TypeError):
        ds(timedelta=td(seconds=60), milliseconds=1000)


def test_invalid_precision():
    with pytest.raises(TypeError):
        ds(seconds=60, precision="invalid_unit")

    with pytest.raises(TypeError):
        ds(seconds=60, precision="nanoseconds")


def test_edge_cases_small_values():
    assert ds(milliseconds=0.5, precision="milliseconds") == "0ms"
    assert ds(microseconds=0.9, precision="microseconds") == "0µs"
    assert ds(microseconds=1500, precision="milliseconds") == "1ms"


def test_no_input_error():
    with pytest.raises(TypeError):
        ds()


def test_invalid_timedelta_type_error():
    with pytest.raises(TypeError):
        ds(timedelta="not a timedelta")
