import math
import unittest

from conventions.projective_integer_jet_v1 import JetData, theorem_record


class ProjectiveIntegerJetTests(unittest.TestCase):
    def assert_bound(self, row: JetData) -> None:
        self.assertTrue(row.sector_condition())
        self.assertGreaterEqual(abs(row.residual) + 1e-14, row.proved_lower_bound())

    def test_nonzero_constant_jet(self) -> None:
        row = JetData(A=8, B=3, C=2, a=1, b=-1, x=0.01)
        self.assertEqual(row.case(), "NONZERO_CONSTANT_JET")
        self.assert_bound(row)

    def test_negative_monotone_linear_jet(self) -> None:
        row = JetData(A=5, B=3, C=2, a=1, b=0, x=0.2)
        self.assertEqual(row.j0, 0)
        self.assertGreater(row.j1, 0)
        self.assert_bound(row)

    def test_positive_controlled_linear_jet(self) -> None:
        row = JetData(A=5, B=3, C=2, a=-1, b=0, x=0.01)
        self.assertLess(row.j1, 0)
        self.assert_bound(row)

    def test_quadratic_concavity_jet(self) -> None:
        row = JetData(A=5, B=3, C=2, a=2, b=-3, x=0.1)
        self.assertEqual((row.j0, row.j1), (0, 0))
        self.assertEqual(row.s2, 30)
        self.assert_bound(row)

    def test_exhaustive_finite_scan(self) -> None:
        seen = set()
        for A in range(1, 10):
            for B in range(1, 6):
                for C in range(1, 6):
                    for a in range(-3, 4):
                        for b in range(-3, 4):
                            if a == b == 0:
                                continue
                            row = JetData(A, B, C, a, b, 1e-4)
                            seen.add(row.case())
                            if row.sector_condition():
                                self.assert_bound(row)
        self.assertEqual(
            seen,
            {
                "NONZERO_CONSTANT_JET",
                "NEGATIVE_MONOTONE_LINEAR_JET",
                "POSITIVE_CONTROLLED_LINEAR_JET",
                "QUADRATIC_CONCAVITY_JET",
            },
        )

    def test_entropy_substitution_and_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("p0*n", record["actual_substitution"])
        self.assertIn("no claim", record["boundary"])
        with self.assertRaises(ValueError):
            JetData(1, 1, 1, 0, 0, 0.1)


if __name__ == "__main__":
    unittest.main()
