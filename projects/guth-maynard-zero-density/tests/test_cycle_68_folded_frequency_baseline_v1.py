from fractions import Fraction as Q
import unittest

from conventions.folded_frequency_baseline_v1 import baseline, verify_all


class Cycle68FoldedFrequencyBaselineTests(unittest.TestCase):
    def test_smallest_scale(self) -> None:
        row = baseline(Q(0))
        self.assertEqual(row["generic_large_sieve_exponent"], Q(13, 10))
        self.assertEqual(row["saving_required"], Q(3, 50))

    def test_largest_scale(self) -> None:
        row = baseline(Q(11, 25))
        self.assertEqual(row["generic_large_sieve_exponent"], Q(87, 50))
        self.assertEqual(row["saving_required"], Q(1, 2))

    def test_middle_scale(self) -> None:
        row = baseline(Q(1, 5))
        self.assertEqual(row["saving_required"], Q(13, 50))

    def test_invalid_scale(self) -> None:
        with self.assertRaises(ValueError):
            baseline(Q(1, 2))

    def test_verification(self) -> None:
        rows = verify_all()
        self.assertIn("tau", rows["coefficient_bound"])
        self.assertIn("Mobius", rows["gate"])


if __name__ == "__main__":
    unittest.main()
