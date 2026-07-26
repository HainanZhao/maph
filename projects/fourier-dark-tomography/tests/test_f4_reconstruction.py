import unittest
import random

from scripts.simulate_f4_reconstruction import (
    exact_response,
    linearity_radius_scan,
    optimal_pair_fraction,
    poisson_sample,
    weighted_estimate,
)
from scripts.analyze_cat_finite_statistics import selected_contrast_jacobian


class F4ReconstructionTests(unittest.TestCase):
    def test_optimal_fraction_is_interior(self):
        fraction, trace_value = optimal_pair_fraction(0.05, 1e-5)
        self.assertAlmostEqual(fraction, 0.5163513, places=7)
        self.assertAlmostEqual(trace_value, 16.8225306185, places=7)
        self.assertGreater(trace_value, 0)

    def test_noiseless_local_estimator(self):
        epsilon = 0.02
        theta = [1e-6 * (index - 5.5) for index in range(12)]
        jacobian = selected_contrast_jacobian(epsilon)
        estimate, _ = weighted_estimate(
            exact_response(theta, epsilon),
            jacobian,
            [1.0] * 12,
        )
        error = sum(
            (value - target) ** 2
            for value, target in zip(estimate, theta)
        ) ** 0.5
        self.assertLess(error, 1e-9)

    def test_poisson_sampler_moments(self):
        rng = random.Random(700)
        for mean in (5.0, 100.0):
            samples = [poisson_sample(mean, rng) for _ in range(20_000)]
            empirical_mean = sum(samples) / len(samples)
            empirical_variance = sum(
                (value - empirical_mean) ** 2 for value in samples
            ) / len(samples)
            self.assertLess(abs(empirical_mean - mean), 0.08 * mean)
            self.assertLess(abs(empirical_variance - mean), 0.12 * mean)

    def test_small_radius_is_locally_linear(self):
        scan = linearity_radius_scan(
            0.05, radii=(1e-5,), directions=16, seed=1
        )
        self.assertLess(scan[0][2], 1e-3)


if __name__ == "__main__":
    unittest.main()
