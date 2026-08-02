import unittest
from fractions import Fraction
from math import gcd

from conventions.cross_valuation_inverse_v1 import extract_cross_core
from conventions.radical_alias_separation_v1 import (
    RadicalAliasCore,
    is_perfect_power,
    theorem_record,
)


class RadicalAliasSeparationTests(unittest.TestCase):
    def test_perfect_power_classifier(self) -> None:
        for degree in range(1, 8):
            for base in range(1, 20):
                self.assertTrue(is_perfect_power(base**degree, degree))
        self.assertFalse(is_perfect_power(12, 2))
        self.assertFalse(is_perfect_power(64, 5))

    def test_small_core_radical_collapse(self) -> None:
        checked = 0
        for W in range(2, 15):
            for N in range(1, 15):
                for R in range(1, 15):
                    if gcd(N, R) != 1:
                        continue
                    for s in range(1, W):
                        core = extract_cross_core(w=W, N=N, R=R, Q=50, s=s)
                        radical = RadicalAliasCore.from_cross_core(core)
                        record = radical.record()
                        self.assertEqual(record["d"], W // gcd(s, W - s))
                        self.assertEqual(
                            record["rational_alias"],
                            is_perfect_power(N, record["d"])
                            and is_perfect_power(R, record["d"]),
                        )
                        checked += 1
        self.assertGreater(checked, 2000)

    def test_nontrivial_rational_alias_constructed(self) -> None:
        radical = RadicalAliasCore(
            h=1, u=1, v=1, d=2, x=1, y=1, s2=1, t2=1,
            N=9, R=4, R2=4, B0=4,
        )
        self.assertTrue(radical.rational_alias)
        self.assertEqual(radical.K_power, Fraction(144, 1))

    def test_exact_norm_numerator_and_safe_bound(self) -> None:
        radical = RadicalAliasCore(
            h=1, u=1, v=1, d=2, x=1, y=1, s2=1, t2=1,
            N=2, R=1, R2=1, B0=1,
        )
        self.assertFalse(radical.rational_alias)
        self.assertNotEqual(radical.exact_norm_numerator(3, 8), 0)
        bound = radical.safe_norm_bound(5)
        self.assertGreater(bound, 0)
        self.assertTrue(radical.separation_closes(bound / 4, 5))
        self.assertFalse(radical.separation_closes(bound, 5))

    def test_unit_label_is_rational(self) -> None:
        radical = RadicalAliasCore(
            h=2, u=1, v=0 + 1, d=2, x=1, y=1, s2=1, t2=1,
            N=1, R=1, R2=1, B0=1,
        )
        self.assertTrue(radical.rational_alias)

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("K=(W/t)*B0", record["single_radical"])
        self.assertIn("perfect dth powers", record["rational_classification"])
        self.assertIn("large radical degree", record["boundary"])


if __name__ == "__main__":
    unittest.main()
