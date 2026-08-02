import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "conventions"))

from log_crossing_occupancy_v1 import (  # noqa: E402
    Q_EXP,
    XI_MAX,
    XI_MIN,
    crossing_exponent,
    dominance_margins,
    dyadic_l1_exponent,
    hs_terms,
    verify_all,
)

Q = Fraction


class LogCrossingOccupancyTests(unittest.TestCase):
    def test_hs_terms(self) -> None:
        row = hs_terms(XI_MIN, Q_EXP)
        self.assertEqual(row["derivative"], Q(4, 15))
        self.assertEqual(row["tube"], Q(52, 225))
        self.assertEqual(row["ratio"], Q(7, 225))

    def test_symbolic_dominance_margin(self) -> None:
        margins = dominance_margins(XI_MIN, Q_EXP)
        self.assertEqual(margins["over_tube"], Q(8, 225))
        self.assertTrue(all(value > 0 for value in margins.values()))

    def test_trivial_hs_splice(self) -> None:
        self.assertEqual(crossing_exponent(XI_MIN, Q(1, 10)), Q(1, 10))
        self.assertEqual(crossing_exponent(XI_MIN, Q_EXP), Q(4, 15))

    def test_endpoint_and_width(self) -> None:
        self.assertEqual(XI_MAX - XI_MIN, Q(1, 15))
        self.assertEqual(dyadic_l1_exponent(XI_MAX, Q_EXP), Q(31, 25))
        self.assertLess(dyadic_l1_exponent(XI_MIN, Q_EXP), Q(31, 25))

    def test_verification(self) -> None:
        row = verify_all()
        self.assertEqual(row["new_cutoff"], "16/25")
        self.assertEqual(row["band_width"], "1/15")
        self.assertIn("signed", row["gate"])


if __name__ == "__main__":
    unittest.main()

