import unittest

from conventions.changing_color_walk_v1 import (
    logarithmic_chain_ceiling,
    recurrence_density_ledger,
    reduction_step,
    theorem_record,
    valuation_update,
)


class ChangingColorWalkTests(unittest.TestCase):
    def test_exact_reduction_walk(self) -> None:
        pp, qq, z = reduction_step(15, 14, 35, 9)
        self.assertEqual((pp, qq, z), (25, 6, 21))

    def test_primewise_update(self) -> None:
        # l divides A with exponent 2 and the old denominator with exponent 1.
        self.assertEqual(valuation_update(2, 0, 3, 1), (4, 0, 1))
        # l divides B with exponent 2 and the old numerator with exponent 1.
        self.assertEqual(valuation_update(0, 2, 1, 3), (0, 4, 1))

    def test_density_approaches_one(self) -> None:
        ceiling = logarithmic_chain_ceiling(1024)
        row = recurrence_density_ledger(10000, ceiling)
        self.assertEqual(row["forbidden_depth"], ceiling + 1)
        self.assertGreater(row["required_density"], 0.95)
        self.assertLess(row["allowed_edge_deficit"], 500)

    def test_record_is_scoped_to_recurrence(self) -> None:
        row = theorem_record()
        self.assertIn("1-O(1/log N)", row["density_gate"])
        self.assertIn("no fixed-power saving", row["scoped_saturation"])
        self.assertIn("not a no-go", row["boundary"])


if __name__ == "__main__":
    unittest.main()
