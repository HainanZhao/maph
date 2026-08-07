"""Regression tests for the exact 5x3x3 held-out Lane B test."""

import unittest

from proof.verify_lane_b_heldout import verify


class LaneBHeldoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = verify()

    def test_minimum_genus_and_frontier(self) -> None:
        self.assertEqual(
            self.result["minimum_genus_certificate"]["minimum_orientable_genus"],
            4,
        )
        self.assertEqual(self.result["sector_count"], 256)
        self.assertEqual(self.result["maximum_frontier_states"], 65536)

    def test_direct_extension_is_exactly_falsified(self) -> None:
        self.assertEqual(
            self.result["generic_TT_profile_over_Q(t)"],
            [2, 4, 8, 16, 8, 4, 2],
        )
        self.assertEqual(self.result["gate_outcome"], "DIRECT_HANDLE_EXTENSION_FALSIFIED")

    def test_polynomial_equalities_are_exact_symmetry_orbits(self) -> None:
        self.assertEqual(self.result["exact_distinct_F_polynomials"], 76)
        self.assertEqual(self.result["spin_structure_orbits"], 76)
        self.assertTrue(self.result["F_polynomial_equalities_equal_symmetry_orbits"])


if __name__ == "__main__":
    unittest.main()
