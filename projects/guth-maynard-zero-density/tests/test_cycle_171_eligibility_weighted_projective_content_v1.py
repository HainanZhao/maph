from fractions import Fraction as Q
import unittest

from conventions.eligibility_weighted_projective_content_v1 import (
    factor_allocation,
    factor_content,
    cycle170_depth_failure,
    divisor_content,
    is_deep,
    low_content_reason,
    moment_population_lower_bound,
    normalized_cap,
    required_content,
    verify_weighted_transfer,
    verify_all,
)


class Cycle171EligibilityWeightedProjectiveContentTests(unittest.TestCase):
    def test_signed_factorization_and_exact_coprimality(self) -> None:
        self.assertEqual(
            factor_content(d=6, b=9, q=10, a=21),
            {"D": 60, "N": 255, "g": 15, "c": 3, "u": 1, "v": 5},
        )
        self.assertEqual(
            factor_content(d=-6, b=-9, q=10, a=21),
            {"D": -60, "N": -255, "g": 15, "c": 3, "u": 1, "v": 5},
        )
        # The source core may share primes with an edge factor; only u and v
        # are universally coprime.
        self.assertEqual(
            factor_content(d=4, b=2, q=1, a=2),
            {"D": 4, "N": 8, "g": 4, "c": 2, "u": 2, "v": 1},
        )

    def test_required_content_including_zero_load(self) -> None:
        self.assertEqual(required_content(load=Q(17, 6), D=60, critical_depth=5, height_cap=20), 15)
        self.assertEqual(required_content(load=Q(0), D=60, critical_depth=5, height_cap=20), 15)
        self.assertTrue(is_deep(content=15, load=Q(17, 6), D=60, critical_depth=5, height_cap=20))
        self.assertFalse(is_deep(content=14, load=Q(17, 6), D=60, critical_depth=5, height_cap=20))
        self.assertEqual(cycle170_depth_failure(content=14, load=Q(17, 6), D=60, critical_depth=5, height_cap=20), "error_supported_depth")
        self.assertEqual(cycle170_depth_failure(content=15, load=Q(17, 6), D=60, critical_depth=5, height_cap=20), "seeded_deep_packet")

    def test_allocation_is_exhaustive(self) -> None:
        allocation = factor_allocation(15)
        self.assertGreaterEqual(allocation["c_min"] * allocation["u_min"] * allocation["v_min"], 15)
        self.assertEqual(low_content_reason(c=3, u=1, v=5, required=15), "deep_content")
        self.assertEqual(low_content_reason(c=1, u=1, v=1, required=15), "source_core")
        self.assertEqual(low_content_reason(c=3, u=1, v=1, required=15), "numerator_absorption")
        self.assertEqual(low_content_reason(c=3, u=3, v=1, required=15), "denominator_absorption")

    def test_sharp_moment_transfer(self) -> None:
        self.assertEqual(normalized_cap(D=60, required=15, critical_depth=5, height_cap=20), Q(4))
        self.assertEqual(moment_population_lower_bound(weighted_content=Q(1), eligible_mass=Q(1), critical_depth=5, height_cap=20), 0)
        self.assertEqual(moment_population_lower_bound(weighted_content=Q(4), eligible_mass=Q(1), critical_depth=5, height_cap=20), 1)
        self.assertEqual(divisor_content(60), 60)
        self.assertEqual(
            verify_weighted_transfer(rows=[(Q(1, 2), Q(99, 100)), (Q(1, 2), Q(4))], cap=Q(4)),
            {"mass": Q(1), "moment": Q(499, 200), "deep_mass": Q(1, 2), "lower_bound": Q(299, 600)},
        )
        self.assertIn("exhaustive_cases", verify_all())
