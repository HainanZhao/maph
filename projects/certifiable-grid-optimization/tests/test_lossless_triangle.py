import math
import unittest

from src.lossless_triangle import (
    injections,
    kantorovich_certificate,
    newton_solve,
)


class LosslessTriangleTests(unittest.TestCase):
    def test_small_target_has_certified_nearby_solution(self):
        initial = (0.0, 0.0)
        target = (0.01, -0.006)
        certificate = kantorovich_certificate(initial, target)
        self.assertTrue(certificate.certified)
        solution = newton_solve(initial, target)
        distance = max(
            abs(solution[0] - initial[0]),
            abs(solution[1] - initial[1]),
        )
        self.assertLessEqual(distance, certificate.radius + 1e-12)
        solved = injections(solution)
        self.assertAlmostEqual(solved[0], target[0])
        self.assertAlmostEqual(solved[1], target[1])

    def test_zero_residual_has_zero_radius(self):
        theta = (0.2, -0.1)
        certificate = kantorovich_certificate(theta, injections(theta))
        self.assertTrue(certificate.certified)
        self.assertAlmostEqual(certificate.radius, 0.0)

    def test_voltage_collapse_point_is_singular(self):
        theta = (math.pi / 2.0, math.pi / 2.0)
        target = injections(theta)
        certificate = kantorovich_certificate(theta, target)
        self.assertFalse(certificate.certified)
        self.assertTrue(math.isinf(certificate.inverse_jacobian_inf))

    def test_arbitrarily_small_residual_can_be_infeasible(self):
        theta = (math.pi / 2.0, math.pi / 2.0)
        epsilon = 1e-9
        impossible_target = (1.0 + epsilon, 1.0 + epsilon)
        certificate = kantorovich_certificate(theta, impossible_target)
        self.assertAlmostEqual(certificate.residual_inf, epsilon)
        self.assertFalse(certificate.certified)
        # For every pair of angles, p1+p2=sin(theta1)+sin(theta2)<=2.
        self.assertGreater(sum(impossible_target), 2.0)


if __name__ == "__main__":
    unittest.main()
