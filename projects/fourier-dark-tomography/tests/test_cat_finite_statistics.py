import math
import unittest

from scripts.analyze_cat_finite_statistics import (
    OUTPUTS,
    PROBE_X,
    PROBE_Y,
    frobenius_relative_error,
    information_root_condition,
    limiting_contrast_jacobian,
    multinomial_information,
    probabilities,
    probability_jacobian_at_zero,
    selected_contrast_jacobian,
    selected_poisson_information,
)


class CatFiniteStatisticsTests(unittest.TestCase):
    def test_finite_angle_probabilities_normalize(self):
        theta = [0.002 * math.cos(index + 1) for index in range(12)]
        for probe, epsilon in ((PROBE_X, 0.13), (PROBE_Y, -0.17)):
            self.assertAlmostEqual(
                sum(probabilities(theta, probe, epsilon)), 1.0, places=12
            )

    def test_analytic_probability_derivative(self):
        epsilon = 0.119
        coordinate = 7
        step = 2e-6
        zero = [0.0] * 12
        positive = zero.copy()
        negative = zero.copy()
        positive[coordinate] = step
        negative[coordinate] = -step
        numerical = [
            (plus - minus) / (2 * step)
            for plus, minus in zip(
                probabilities(positive, PROBE_Y, epsilon),
                probabilities(negative, PROBE_Y, epsilon),
            )
        ]
        analytic = probability_jacobian_at_zero(PROBE_Y, epsilon)
        for output_index in range(len(OUTPUTS)):
            self.assertAlmostEqual(
                numerical[output_index],
                analytic[output_index][coordinate],
                places=8,
            )

    def test_contrast_bias_is_second_order(self):
        reference = limiting_contrast_jacobian()
        errors = [
            frobenius_relative_error(
                selected_contrast_jacobian(epsilon), reference
            )
            for epsilon in (0.04, 0.02, 0.01)
        ]
        self.assertGreater(errors[0] / errors[1], 3.9)
        self.assertGreater(errors[1] / errors[2], 3.9)

    def test_background_information_is_finite_full_rank(self):
        for information in (
            selected_poisson_information(0.05, 1e-5),
            multinomial_information(0.05, 1e-3),
        ):
            condition = information_root_condition(information)
            self.assertTrue(math.isfinite(condition))
            self.assertGreater(condition, 1)


if __name__ == "__main__":
    unittest.main()
