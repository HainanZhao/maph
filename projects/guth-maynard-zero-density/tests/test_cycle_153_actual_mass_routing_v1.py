import unittest
from fractions import Fraction

from conventions.actual_mass_routing_v1 import (
    routing_dichotomy,
    theorem_record,
    validate_partition,
)


class ActualMassRoutingTests(unittest.TestCase):
    def test_strict_route(self) -> None:
        row = routing_dichotomy(
            post_error_negative_mass=Fraction(1),
            strict_real_correlations=[Fraction(-3, 5), Fraction(1, 7)],
        )
        self.assertEqual(row["route"], "STRICT_LABELLED_MASS")
        self.assertGreaterEqual(row["strict_negative_mass"], row["threshold"])

    def test_escape_route(self) -> None:
        row = routing_dichotomy(
            post_error_negative_mass=Fraction(1),
            strict_real_correlations=[Fraction(-1, 3), Fraction(1, 9)],
        )
        self.assertEqual(row["route"], "LABELLED_ESCAPE_OBLIGATION")
        self.assertGreaterEqual(row["escape_correlation_lower_bound"], row["threshold"])

    def test_partition_audit(self) -> None:
        validate_partition(
            strict_ids=["s1", "s2"],
            escape_rows=[("e1", "boundary_denominator"), ("e2", "unbounded_tau")],
        )
        with self.assertRaises(ValueError):
            validate_partition(strict_ids=["s1"], escape_rows=[("s1", "nonsmooth_payload")])

    def test_record_keeps_cycle152_boundary(self) -> None:
        row = theorem_record()
        self.assertIn("mu_*-N_S", row["routing_identity"])
        self.assertIn("Cycle 152", row["cycle152_interface"])
        self.assertIn("proves no", row["boundary"])


if __name__ == "__main__":
    unittest.main()
