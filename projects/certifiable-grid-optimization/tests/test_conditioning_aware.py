import unittest

from src.conditioning_aware import solve_conditioning_aware_sweep
from src.sparse_phase_lp import (
    PhaseEdge,
    solve_weighted_phase_least_squares,
)


class ConditioningAwareTests(unittest.TestCase):
    def test_zero_radius_reproduces_reference(self):
        edges = (
            PhaseEdge(0, 1, 0.1, 1.0),
            PhaseEdge(1, 2, 0.1, 2.0),
            PhaseEdge(2, 0, -0.18, 0.5),
        )
        reference = solve_weighted_phase_least_squares(3, edges)
        result = solve_conditioning_aware_sweep(
            3, edges, reference.theta, (0.0,)
        )
        for actual, expected in zip(result.projection.theta, reference.theta):
            self.assertAlmostEqual(actual, expected)

    def test_sweep_is_no_worse_than_zero_radius_reference(self):
        edges = (
            PhaseEdge(0, 1, 0.3, 1.0),
            PhaseEdge(1, 2, 0.4, 2.0),
            PhaseEdge(2, 0, -0.6, 0.5),
        )
        reference = solve_weighted_phase_least_squares(3, edges)
        zero = solve_conditioning_aware_sweep(
            3, edges, reference.theta, (0.0,)
        )
        sweep = solve_conditioning_aware_sweep(
            3, edges, reference.theta, (0.0, 0.01, 0.05, 0.2)
        )
        self.assertLessEqual(sweep.score.h_bound, zero.score.h_bound)


if __name__ == "__main__":
    unittest.main()
