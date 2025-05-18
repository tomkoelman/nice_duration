from datetime import timedelta as td
from nice_duration import duration_string as ds
import unittest


class TestDurationStringMethods(unittest.TestCase):
    def test_empty_timedelta(self):
        delta = td(seconds=0)
        self.assertEqual(ds(delta), "0s")
        self.assertEqual(ds(delta, keep_zeroes=True), "0w0d0h0m0s")

    def test_separator(self):
        delta = td(hours=300, minutes=70)
        self.assertEqual(ds(delta, separator=" "), "1w 5d 13h 10m")

    def test_keeping_zeroes(self):
        delta = td(days=3, minutes=12)
        self.assertEqual(ds(delta), "3d12m")
        self.assertEqual(ds(delta, keep_infix_zeroes=True), "3d0h12m")
        self.assertEqual(ds(delta, keep_leading_zeroes=True), "0w3d12m")
        self.assertEqual(ds(delta, keep_trailing_zeroes=True), "3d12m0s")
        self.assertEqual(
            ds(delta, keep_leading_zeroes=True, keep_trailing_zeroes=True), "0w3d12m0s"
        )
        self.assertEqual(
            ds(
                delta,
                keep_leading_zeroes=True,
                keep_trailing_zeroes=True,
                keep_infix_zeroes=True,
            ),
            "0w3d0h12m0s",
        )
        self.assertEqual(ds(delta, keep_zeroes=True), "0w3d0h12m0s")

    def test_call_with_number_of_seconds(self):
        self.assertEqual(ds(70), "1m10s")


if __name__ == "__main__":
    unittest.main()
