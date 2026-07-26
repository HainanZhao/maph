import math
import unittest

from src.phase_projection import (
    balanced_triangle_projection,
    best_tree_triangle_projection,
    conditioned_triangle_projection,
    grid_optimal_conditioned_triangle_projection,
    grid_optimal_triangle_projection,
    phase_linearization_factor,
    triangle_linear_worst_bus_bound,
    triangle_worst_bus_bound,
)


class PhaseProjectionTests(unittest.TestCase):
    def test_balanced_is_grid_optimal_for_equal_weights(self):
        delta = 0.6
        balanced = balanced_triangle_projection(delta)
        optimized = grid_optimal_triangle_projection(delta, grid_steps=300)
        self.assertAlmostEqual(
            optimized.worst_bus_bound,
            balanced.worst_bus_bound,
            places=12,
        )
        for value in optimized.allocation:
            self.assertAlmostEqual(value, delta / 3.0, places=12)

    def test_balanced_beats_tree_for_equal_weights(self):
        delta = 0.6
        balanced = balanced_triangle_projection(delta)
        tree = best_tree_triangle_projection(delta)
        self.assertLess(balanced.worst_bus_bound, tree.worst_bus_bound)

    def test_weighted_grid_search_beats_fixed_recoveries(self):
        delta = 0.6
        weights = (5.0, 1.0, 1.0)
        optimized = grid_optimal_triangle_projection(
            delta, weights, grid_steps=300
        )
        balanced = balanced_triangle_projection(delta, weights)
        tree = best_tree_triangle_projection(delta, weights)
        self.assertLessEqual(
            optimized.worst_bus_bound, balanced.worst_bus_bound + 1e-12
        )
        self.assertLessEqual(
            optimized.worst_bus_bound, tree.worst_bus_bound + 1e-12
        )
        self.assertLess(optimized.allocation[0], delta / 3.0)

    def test_conditioning_aware_search_avoids_singular_tree_recovery(self):
        delta = 0.18
        measured = (-math.pi / 2.0, 0.0, math.pi / 2.0 + delta)
        singular_tree = conditioned_triangle_projection(
            measured, (0.0, 0.0, delta)
        )
        optimized = grid_optimal_conditioned_triangle_projection(
            measured, grid_steps=120
        )
        self.assertTrue(math.isinf(singular_tree.h_bound))
        self.assertTrue(math.isfinite(optimized.h_bound))
        self.assertNotEqual(optimized.allocation, singular_tree.allocation)

    def test_conditioning_changes_certification_threshold(self):
        base = 1.3
        small = grid_optimal_conditioned_triangle_projection(
            (-base, 0.0, base + 0.01), grid_steps=120
        )
        larger = grid_optimal_conditioned_triangle_projection(
            (-base, 0.0, base + 0.03), grid_steps=120
        )
        self.assertLessEqual(small.h_bound, 0.5)
        self.assertGreater(larger.h_bound, 0.5)

    def test_linear_surrogate_bounds_exact_certificate(self):
        allocation = (0.05, 0.2, 0.35)
        weights = (5.0, 1.5, 0.7)
        gamma = max(allocation)
        exact = triangle_worst_bus_bound(allocation, weights)
        linear = triangle_linear_worst_bus_bound(allocation, weights)
        factor = phase_linearization_factor(gamma)
        self.assertLessEqual(exact, linear + 1e-12)
        self.assertGreaterEqual(exact + 1e-12, factor * linear)


if __name__ == "__main__":
    unittest.main()
