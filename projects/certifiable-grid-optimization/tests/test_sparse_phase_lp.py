import math
import unittest

from src.phase_projection import phase_linearization_factor
from src.sparse_phase_lp import (
    PhaseEdge,
    solve_minimax_phase_lp,
    solve_weighted_phase_least_squares,
)


class SparsePhaseLPTests(unittest.TestCase):
    def test_equal_triangle_matches_balanced_theorem(self):
        delta = 0.6
        edges = (
            PhaseEdge(0, 1, 0.0),
            PhaseEdge(1, 2, 0.0),
            PhaseEdge(2, 0, delta),
        )
        result = solve_minimax_phase_lp(3, edges)
        for correction in result.corrections:
            self.assertAlmostEqual(correction, -delta / 3.0)
        self.assertAlmostEqual(result.linear_bound, 2.0 * delta / 3.0)
        self.assertAlmostEqual(
            result.exact_bound, 4.0 * math.sin(delta / 6.0)
        )

    def test_general_cycle_is_consistent_after_projection(self):
        edges = (
            PhaseEdge(0, 1, 0.1, 1.0),
            PhaseEdge(1, 2, -0.2, 2.0),
            PhaseEdge(2, 3, 0.15, 0.7),
            PhaseEdge(3, 0, 0.25, 1.4),
        )
        result = solve_minimax_phase_lp(4, edges)
        self.assertAlmostEqual(sum(result.corrections), -0.3)
        for edge, correction in zip(edges, result.corrections):
            recovered = (
                result.theta[edge.u]
                - result.theta[edge.v]
                - edge.phase
            )
            self.assertAlmostEqual(recovered, correction)

    def test_physical_approximation_bound(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 5.0),
            PhaseEdge(1, 2, 0.0, 1.0),
            PhaseEdge(2, 0, 0.6, 1.0),
        )
        result = solve_minimax_phase_lp(3, edges)
        gamma = max(abs(value) for value in result.corrections)
        factor = phase_linearization_factor(gamma)
        self.assertLessEqual(result.exact_bound, result.linear_bound + 1e-10)
        self.assertGreaterEqual(
            result.exact_bound + 1e-10,
            factor * result.linear_bound,
        )

    def test_bus_offsets_change_the_minimax_allocation(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 1.0),
            PhaseEdge(1, 2, 0.0, 1.0),
            PhaseEdge(2, 0, 0.3, 1.0),
        )
        without_offsets = solve_minimax_phase_lp(3, edges)
        with_offsets = solve_minimax_phase_lp(
            3, edges, bus_offsets=(0.25, 0.0, 0.0)
        )
        self.assertNotEqual(
            tuple(round(value, 8) for value in without_offsets.corrections),
            tuple(round(value, 8) for value in with_offsets.corrections),
        )
        self.assertGreaterEqual(with_offsets.linear_bound, 0.25)

    def test_lp_can_improve_worst_bus_over_least_squares_when_weighted(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 4.0),
            PhaseEdge(1, 2, 0.0, 2.0),
            PhaseEdge(2, 0, 0.6, 1.0),
        )
        lp = solve_minimax_phase_lp(3, edges)
        least_squares = solve_weighted_phase_least_squares(3, edges)
        self.assertLess(lp.linear_bound, least_squares.linear_bound)
        self.assertLess(lp.exact_bound, least_squares.exact_bound)

    def test_multicycle_lp_improves_worst_bus_over_least_squares(self):
        edges = (
            PhaseEdge(0, 1, -0.398762714628607, 1.8777619718248755),
            PhaseEdge(1, 2, 0.13805742727380532, 3.8179158780898836),
            PhaseEdge(2, 3, 0.20456510735442823, 0.3587290609873123),
            PhaseEdge(3, 0, -0.2324453891644651, 0.24490378763107223),
            PhaseEdge(0, 2, -0.1435126283081648, 4.904896640517616),
        )
        lp = solve_minimax_phase_lp(4, edges)
        least_squares = solve_weighted_phase_least_squares(4, edges)
        self.assertLess(lp.linear_bound, 0.9 * least_squares.linear_bound)
        self.assertLess(lp.exact_bound, 0.9 * least_squares.exact_bound)


if __name__ == "__main__":
    unittest.main()
