import unittest

from scripts.analyze_general_resource_scaling import (
    alpha_squared,
    cramer_rao_trace,
    normalized_reference_probabilities,
    optimal_pair_allocation,
    trials_for_reference_counts,
)


class GeneralResourceScalingTests(unittest.TestCase):
    def test_alpha_scaling_at_n_equals_m(self):
        for modes in range(3, 11):
            self.assertAlmostEqual(
                alpha_squared(modes, modes), modes ** (2 - modes)
            )

    def test_reported_probability_orders(self):
        p8 = min(normalized_reference_probabilities(8, 8, 0.05))
        p10 = min(normalized_reference_probabilities(10, 10, 0.05))
        self.assertGreater(p8, 1e-9)
        self.assertLess(p8, 1e-8)
        self.assertGreater(p10, 1e-11)
        self.assertLess(p10, 1e-10)

    def test_optimal_allocation(self):
        real, imaginary = optimal_pair_allocation(5, 5)
        self.assertAlmostEqual(real, 0.5)
        self.assertAlmostEqual(imaginary, 0.5)
        real, imaginary = optimal_pair_allocation(4, 4)
        self.assertLess(real, imaginary)
        self.assertAlmostEqual(real + imaginary, 1.0)

    def test_cramer_rao_and_count_requirements_scale_with_trials(self):
        first = cramer_rao_trace(4, 4, 1e5)
        second = cramer_rao_trace(4, 4, 2e5)
        self.assertAlmostEqual(first, 2 * second)
        count_trials = trials_for_reference_counts(4, 4, 0.05, 10)
        doubled = trials_for_reference_counts(4, 4, 0.05, 20)
        self.assertAlmostEqual(doubled, 2 * count_trials)


if __name__ == "__main__":
    unittest.main()
