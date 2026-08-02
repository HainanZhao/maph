import unittest
from fractions import Fraction

from conventions.generic_critical_packing_v1 import (
    aggregate_generic_bound,
    packing_record,
    reduced_compact_labels,
    theorem_record,
)


class GenericCriticalPackingTests(unittest.TestCase):
    def test_exhaustive_compact_families(self) -> None:
        for height in range(1, 35):
            labels = reduced_compact_labels(height, 0.7)
            record = packing_record(labels, 0.7)
            self.assertTrue(record["passes"])

    def test_duplicate_rejected(self) -> None:
        with self.assertRaises(ValueError):
            packing_record([Fraction(2, 3), Fraction(2, 3)], 1.0)

    def test_aggregate_constants(self) -> None:
        record = aggregate_generic_bound(Q=20, M=30, L=1.0, label_count=75)
        self.assertLessEqual(record["count_sensitive_bound"], record["uniform_bound"])
        self.assertEqual(record["actual_exponent"].split("=")[-1], "19/30")

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("sqrt(J)", record["aggregate"])
        self.assertIn("excluded", record["boundary"])


if __name__ == "__main__":
    unittest.main()
