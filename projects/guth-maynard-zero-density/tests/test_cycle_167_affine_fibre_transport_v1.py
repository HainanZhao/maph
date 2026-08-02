import unittest
from fractions import Fraction as Q
from itertools import combinations
from math import comb

from conventions.affine_fibre_transport_v1 import (
    direct_map_coefficients,
    distinct_parameter_lower_bound,
    divisibility_residue,
    eligible_parameters,
    primitive_parent_count,
    transport_balance,
    transport_edge,
    verify_all,
)


class Cycle167AffineFibreTransportTests(unittest.TestCase):
    def test_deconvolution_on_all_small_parameter_sets(self):
        for size in range(4, 8):
            for parameters in combinations(range(-3, 5), size):
                parents = primitive_parent_count(parameters)
                self.assertLessEqual(parents, comb(len(parameters), 4))
                self.assertLessEqual(distinct_parameter_lower_bound(parents), len(parameters))

    def test_divisibility_classifier_including_zero_slope(self):
        self.assertEqual(divisibility_residue(26, 1, 5), (4, 5))
        self.assertIsNone(divisibility_residue(1, 2, 4))
        self.assertEqual(divisibility_residue(12, 0, 3), (0, 1))
        self.assertIsNone(divisibility_residue(13, 0, 3))
        self.assertEqual(
            eligible_parameters((0, 1, 2, 3, 4), h0=25, r=1, a=5, q=4, h_scale=20),
            (0,),
        )

    def test_residue_and_range_obstructions_are_distinct(self):
        self.assertEqual(
            eligible_parameters((0, 1, 2, 3), h0=26, r=1, a=5, q=4, h_scale=20), ()
        )
        self.assertEqual(
            eligible_parameters((0, 1, 2, 3), h0=21, r=3, a=3, q=2, h_scale=21), ()
        )

    def test_direct_map_is_exact_and_unique_coefficients_are_rational(self):
        self.assertEqual(direct_map_coefficients(5, 3), (Q(3, 5), Q(2, 5)))
        edge = transport_edge(h=10, j=5, beta=Q(0), y=Q(3, 2), q=3, a=5, shift_error=Q(1, 30))
        self.assertEqual(edge["h_plus"], 6)
        self.assertEqual(edge["j_plus"], 9)
        self.assertEqual(edge["error_increment"], Q(-1, 10))
        self.assertEqual(transport_balance(100, 5, 20, Q(3, 2)), Q(3, 1))

    def test_complete_classifier(self):
        checked = verify_all()
        self.assertIn("single cross-label edge", checked["boundary"])


if __name__ == "__main__":
    unittest.main()
