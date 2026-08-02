import unittest
from fractions import Fraction
from math import gcd

from conventions.cross_valuation_inverse_v1 import extract_cross_core
from conventions.critical_scale_alias_v1 import (
    CriticalScalePhase,
    critical_value_tolerance,
    nearest_integer_distance,
    scale_alias_inverse,
    theorem_record,
)


class CriticalScaleAliasTests(unittest.TestCase):
    def test_small_core_identities(self) -> None:
        checked = 0
        for W in range(2, 13):
            for N in range(1, 13):
                for R in range(1, 13):
                    if gcd(N, R) != 1:
                        continue
                    for s in range(1, W):
                        core = extract_cross_core(w=W, N=N, R=R, Q=40, s=s)
                        phase = CriticalScalePhase.from_cross_core(core)
                        record = phase.verify()
                        self.assertTrue(record["positive"])
                        self.assertEqual(record["degree_bound"], W)
                        checked += 1
        self.assertGreater(checked, 1000)

    def test_near_double_tolerance_exact(self) -> None:
        value = critical_value_tolerance(
            Fraction(1, 100), Fraction(1, 20), Fraction(1, 2), Fraction(3, 2)
        )
        self.assertEqual(value, Fraction(1, 20))

    def test_alias_inverse_exact_hits(self) -> None:
        record = scale_alias_inverse(
            theta=Fraction(1, 3),
            epsilon=Fraction(0),
            Lambda=10,
            hits=[(3, 1), (6, 2), (9, 3)],
        )
        self.assertEqual(record["least_alias"], 3)
        self.assertEqual(record["support_bound"], 4)
        self.assertEqual(record["witness"]["q"], 3)
        self.assertEqual(record["witness"]["distance"], 0)

    def test_no_alias_allows_one_hit(self) -> None:
        record = scale_alias_inverse(
            theta=Fraction(1, 3),
            epsilon=Fraction(1, 100),
            Lambda=3,
            hits=[],
        )
        self.assertIsNone(record["least_alias"])
        self.assertEqual(record["support_bound"], 1)

    def test_tolerance_and_tie(self) -> None:
        theta = Fraction(49, 100)
        epsilon = Fraction(1, 50)
        self.assertEqual(nearest_integer_distance(2 * theta), epsilon)
        record = scale_alias_inverse(
            theta=theta,
            epsilon=epsilon,
            Lambda=100,
            hits=[(2, 1), (100, 49)],
        )
        self.assertLessEqual(record["witness"]["distance"], 2 * epsilon)

    def test_rejects_false_hit(self) -> None:
        with self.assertRaises(ValueError):
            scale_alias_inverse(
                theta=Fraction(2, 7), epsilon=Fraction(1, 100), Lambda=5, hits=[(1, 0)]
            )

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("f(t*)=A-lambda*K", record["homogeneity"])
        self.assertIn("||qK||<=2epsilon", record["inverse"])
        self.assertIn("no useful irrationality measure", record["boundary"])


if __name__ == "__main__":
    unittest.main()
