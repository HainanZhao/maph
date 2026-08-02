import unittest
from fractions import Fraction
from math import gcd

from conventions.beta_free_saturation_v1 import (
    RationalScaleOrbit,
    paired_beta_witness,
    theorem_record,
)
from conventions.cross_valuation_inverse_v1 import extract_cross_core
from conventions.radical_alias_separation_v1 import RadicalAliasCore


class BetaFreeSaturationTests(unittest.TestCase):
    def test_small_perfect_power_cores(self) -> None:
        checked = 0
        for W in range(2, 9):
            for N in range(1, 65):
                for R in range(1, 65):
                    if gcd(N, R) != 1:
                        continue
                    for s in range(1, W):
                        core = extract_cross_core(w=W, N=N, R=R, Q=80, s=s)
                        radical = RadicalAliasCore.from_cross_core(core)
                        if not radical.rational_alias:
                            continue
                        orbit = RationalScaleOrbit.from_radical(radical)
                        orbit.verify_against(radical)
                        checked += 1
        self.assertGreater(checked, 100)

    def test_nontrivial_all_scale_saturator(self) -> None:
        orbit = RationalScaleOrbit(u=2, v=1, d=3, x=2, y=1, n0=3, r0=2)
        self.assertEqual(orbit.K, 27)
        record = orbit.tight_hits(Lambda=12, epsilon=Fraction(0))
        self.assertTrue(record["all_scales"])
        self.assertEqual(record["count"], 12)
        self.assertEqual(record["scales"], tuple(range(1, 13)))

    def test_nonintegral_exact_progression(self) -> None:
        orbit = RationalScaleOrbit(u=1, v=2, d=3, x=1, y=2, n0=2, r0=3)
        self.assertEqual(orbit.K, Fraction(27, 1))
        # A deliberately abstract valid orbit with denominator two.
        orbit = RationalScaleOrbit(u=1, v=2, d=3, x=1, y=4, n0=2, r0=3)
        self.assertEqual(orbit.K, Fraction(27, 2))
        record = orbit.tight_hits(Lambda=9, epsilon=Fraction(1, 3))
        self.assertEqual(record["scales"], (2, 4, 6, 8))
        self.assertEqual(record["count"], 4)

    def test_tolerance_gate_rejects_boundary(self) -> None:
        orbit = RationalScaleOrbit(u=1, v=2, d=3, x=1, y=4, n0=2, r0=3)
        with self.assertRaises(ValueError):
            orbit.tight_hits(Lambda=5, epsilon=Fraction(1, 2))

    def test_paired_beta_nonimplication(self) -> None:
        record = paired_beta_witness(
            alpha=Fraction(7, 5), h0=11, j0=15, strip_radius=Fraction(1, 100)
        )
        self.assertTrue(record["seeded"])
        self.assertFalse(record["unseeded"])
        self.assertEqual(record["seeded_residual"], 0)
        self.assertEqual(record["unseeded_residual"], Fraction(1, 2))

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("S0|lambda", record["tight_hits"])
        self.assertIn("beta-free", record["boundary"])
        self.assertIn("payload", record["positive_interface"])


if __name__ == "__main__":
    unittest.main()
