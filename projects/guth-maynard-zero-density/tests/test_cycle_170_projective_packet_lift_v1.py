import unittest
from fractions import Fraction as Q

from conventions.projective_packet_lift_v1 import (
    depth_ledger,
    certifies_reduced_packet,
    error_load,
    lift_identity,
    obstruction_reason,
    projective_data,
    transported_seed_residual,
    verify_all,
)


class Cycle170ProjectivePacketLiftTests(unittest.TestCase):
    def test_signed_reduction_and_exact_lift(self):
        self.assertEqual(projective_data(d=2, b=1, q=2, a=3), {"D": 4, "N": 5, "g": 1, "Q": 4, "A": 5})
        self.assertEqual(projective_data(d=-2, b=-1, q=2, a=3), {"D": -4, "N": -5, "g": 1, "Q": 4, "A": 5})
        self.assertEqual(lift_identity(alpha_source=Q(1, 2), alpha_target=Q(5, 4), edge_ratio=Q(3, 2), d=2, b=1, q=2, a=3), 0)
        self.assertEqual(
            transported_seed_residual(h=30, j=15, beta=Q(0), alpha_source=Q(1, 2), alpha_target=Q(5, 4), edge_ratio=Q(3, 2), q=2, a=3),
            {"h_plus": 20, "j_plus": 25, "source_residual": Q(0), "target_residual": Q(0)},
        )
        with self.assertRaises(ValueError):
            lift_identity(alpha_source=Q(1, 2), alpha_target=Q(1), edge_ratio=Q(3, 2), d=2, b=1, q=2, a=3)

    def test_error_and_two_depth_limits(self):
        load = error_load(a=3, d=2, b=1, source_constant=Q(1), source_depth=2, edge_constant=Q(1), edge_depth=3)
        self.assertEqual(load, Q(17, 6))
        self.assertEqual(depth_ledger(content=17, load=load, h_cap=20, denominator=4), {"error_depth": 6, "capacity_depth": 5, "target_depth": 5})
        self.assertEqual(depth_ledger(content=17, load=Q(0), h_cap=20, denominator=4), {"error_depth": None, "capacity_depth": 5, "target_depth": 5})
        self.assertTrue(certifies_reduced_packet(load=Q(17, 6), content=17, depth=5, denominator=4, h_cap=20))
        self.assertTrue(certifies_reduced_packet(load=Q(0), content=17, depth=5, denominator=4, h_cap=20))
        self.assertFalse(certifies_reduced_packet(load=Q(17, 6), content=17, depth=6, denominator=4, h_cap=20))

    def test_exhaustive_obstruction_order(self):
        base = {"seed_integral_and_in_range": True, "content": 17, "minimum_content": 1, "error_depth": 6, "capacity_depth": 5, "critical_depth": 5}
        self.assertEqual(obstruction_reason(**base), "seeded_deep_packet")
        self.assertEqual(obstruction_reason(**{**base, "seed_integral_and_in_range": False}), "seed_integrality_or_range")
        self.assertEqual(obstruction_reason(**{**base, "content": 0}), "projective_content")
        self.assertEqual(obstruction_reason(**{**base, "error_depth": 4}), "error_supported_depth")
        self.assertEqual(obstruction_reason(**{**base, "capacity_depth": 4}), "denominator_capacity")

    def test_complete_ledger(self):
        checked = verify_all()
        self.assertIn("separate", checked["depth"])
        self.assertIn("finite projective-lift classifier", checked["boundary"])


if __name__ == "__main__":
    unittest.main()
