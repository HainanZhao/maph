import math
import unittest

from conventions.projective_algebraic_root_v1 import RootData, theorem_record


class ProjectiveAlgebraicRootTests(unittest.TestCase):
    def test_polynomial_contract_exhaustive(self) -> None:
        for A in range(1, 5):
            for B in range(1, 5):
                for C in range(1, 5):
                    for a in range(-4, 5):
                        for b in range(-4, 5):
                            if a == b == 0:
                                continue
                            row = RootData(A, B, C, a, b)
                            poly = row.polynomial()
                            self.assertTrue(poly)
                            self.assertLessEqual(row.polynomial_degree(), 2 * row.mode_radius)
                            self.assertLessEqual(row.polynomial_l1(), row.weight)

    def test_clearing_identity(self) -> None:
        row = RootData(7, 3, 2, -2, 3)
        for t in (-0.7, 0.0, 0.4):
            y = math.exp(t)
            polynomial_value = sum(c * y**j for j, c in row.polynomial().items())
            self.assertAlmostEqual(row.value(t), math.exp(-row.shift * t) * polynomial_value)

    def test_critical_point(self) -> None:
        row = RootData(5, 3, 2, 2, -3)
        contract = row.critical_contract()
        self.assertTrue(contract["exists"])
        self.assertAlmostEqual(row.derivative(contract["t_star"]), 0.0, places=12)
        self.assertLess(row.second_derivative(contract["t_star"]), 0.0)
        self.assertFalse(RootData(5, 3, 2, 2, 1).critical_contract()["exists"])

    def test_simple_root_newton_branch(self) -> None:
        row = RootData(3, 1, 1, 1, 0)
        root = math.log(2.0)
        x = root + 1e-6
        inverse = row.local_inverse(x)
        self.assertEqual(inverse["branch"], "SIMPLE_ALGEBRAIC_ROOT")
        self.assertLessEqual(abs(root - x), inverse["root_distance_bound"] + 1e-14)

    def test_near_double_branch(self) -> None:
        row = RootData(5, 2, 3, 2, -3)
        x = row.critical_contract()["t_star"]
        inverse = row.local_inverse(x)
        self.assertEqual(inverse["branch"], "NEAR_DOUBLE_ROOT")
        self.assertTrue(inverse["localized_critical"])

    def test_theorem_boundary(self) -> None:
        record = theorem_record()
        self.assertIn("2*M", record["polynomial_contract"]["degree"])
        self.assertIn("no effective lower bound", record["boundary"])


if __name__ == "__main__":
    unittest.main()
