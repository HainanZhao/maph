import unittest

from src.lossless_graph import (
    jacobian_lipschitz_bound,
    reference_conditioning_bound,
    reduced_jacobian,
    score_projection,
)
from src.sparse_phase_lp import (
    PhaseEdge,
    solve_minimax_phase_lp,
    solve_weighted_phase_least_squares,
)


class LosslessGraphTests(unittest.TestCase):
    def test_triangle_matches_previous_jacobian_and_lipschitz(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 1.0),
            PhaseEdge(1, 2, 0.0, 1.0),
            PhaseEdge(2, 0, 0.0, 1.0),
        )
        matrix = reduced_jacobian(3, edges, (0.0, 0.0, 0.0))
        self.assertEqual(matrix.tolist(), [[2.0, -1.0], [-1.0, 2.0]])
        self.assertAlmostEqual(jacobian_lipschitz_bound(3, edges), 5.0)

    def test_small_cycle_defect_is_certified(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 1.0),
            PhaseEdge(1, 2, 0.0, 1.0),
            PhaseEdge(2, 0, 0.01, 1.0),
        )
        projection = solve_minimax_phase_lp(3, edges)
        score = score_projection(3, edges, projection)
        self.assertTrue(score.certified)

    def test_smaller_residual_need_not_give_better_certificate(self):
        """Conditioning can reverse the residual-only ranking."""

        pairs = ((0, 1), (1, 2), (2, 3), (3, 0), (0, 2))
        phases = (
            0.07174283148410128,
            -0.6000636417879502,
            1.2868594767766794,
            -0.7038597627832773,
            -0.5328325736648674,
        )
        weights = (
            0.5949593987814837,
            0.5346125006161954,
            0.7588295035739211,
            0.7638047259537938,
            1.2140368522590534,
        )
        edges = tuple(
            PhaseEdge(u, v, phase, weight)
            for (u, v), phase, weight in zip(pairs, phases, weights)
        )
        minimax = solve_minimax_phase_lp(4, edges)
        least_squares = solve_weighted_phase_least_squares(4, edges)
        minimax_score = score_projection(4, edges, minimax)
        least_squares_score = score_projection(4, edges, least_squares)

        self.assertLess(
            minimax_score.residual_bound,
            least_squares_score.residual_bound,
        )
        self.assertGreater(minimax_score.h_bound, 0.5)
        self.assertLess(least_squares_score.h_bound, 0.5)
        self.assertFalse(minimax_score.certified)
        self.assertTrue(least_squares_score.certified)

    def test_reference_bound_dominates_nearby_inverse_norm(self):
        edges = (
            PhaseEdge(0, 1, 0.0, 1.0),
            PhaseEdge(1, 2, 0.0, 1.0),
            PhaseEdge(2, 0, 0.0, 1.0),
        )
        reference = (0.0, 0.1, -0.1)
        nearby = (0.0, 0.105, -0.095)
        bound = reference_conditioning_bound(
            3, edges, reference, radius=0.005
        )
        nearby_projection = solve_minimax_phase_lp(
            3,
            (
                PhaseEdge(0, 1, -nearby[1], 1.0),
                PhaseEdge(1, 2, nearby[1] - nearby[2], 1.0),
                PhaseEdge(2, 0, nearby[2], 1.0),
            ),
        )
        nearby_score = score_projection(3, edges, nearby_projection)
        self.assertLessEqual(
            nearby_score.inverse_jacobian_inf,
            bound.inverse_jacobian_upper_bound,
        )


if __name__ == "__main__":
    unittest.main()
