import unittest
from fractions import Fraction

from conventions.perfect_power_split_sum_v1 import (
    finite_falsifier,
    mode_bound,
    split_record,
    split_sum,
    theorem_record,
)


class PerfectPowerSplitSumTests(unittest.TestCase):
    def test_cycle_106_saturator_product(self) -> None:
        row = split_record(u=2, v=1, n0=3, r0=2)
        self.assertEqual(row["x"], 2)
        self.assertEqual(row["y"], 1)
        self.assertEqual(row["K"], Fraction(27))
        self.assertEqual((row["B0"], row["C0"]), (4, 27))
        self.assertEqual(row["weight_squared"], Fraction(1, 54**2))

    def test_unit_base(self) -> None:
        self.assertLess(split_sum(d=37, n0=1, r0=1), 4.0)

    def test_finite_falsifier(self) -> None:
        record = finite_falsifier(max_degree=80, max_base=12)
        self.assertGreater(record["rows"], 1000)
        self.assertLess(record["maximum"], record["threshold"])

    def test_divisor_aggregation(self) -> None:
        self.assertEqual(mode_bound(12), 24)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("less than 4", record["uniform_split_sum"])
        self.assertIn("4*tau(W)", record["degree_aggregation"])
        self.assertIn("anchor prefactor", record["boundary"])


if __name__ == "__main__":
    unittest.main()
