from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_199_full_phase_abel_boundary import (  # noqa: E402
    boundary_character_rank,
    c198_character_labels,
    no_linear_all36_intertwiner,
    paired_i0_boundary,
    run,
)


class FullPhaseAbelBoundaryTests(unittest.TestCase):
    def test_c198_has_36_distinct_target_labels(self) -> None:
        self.assertEqual(len(c198_character_labels()), 36)

    def test_paired_i0_limit_is_six_channel_delta_comb(self) -> None:
        result = paired_i0_boundary()
        self.assertEqual(result["six_channels"], [0, 4, 8, 12, 16, 20])
        self.assertIn("12*i/r_beta", result["three_class_sum_boundary_distribution"])

    def test_full_character_comb_loses_b_at_boundary(self) -> None:
        result = boundary_character_rank()
        self.assertEqual(result["distinct_boundary_character_vectors"], 6)
        self.assertEqual(result["boundary_rank_upper_bound"], 6)
        self.assertIn("b labels collapse", result["loss"])

    def test_no_all36_linear_intertwiner_in_declared_class(self) -> None:
        result = no_linear_all36_intertwiner()
        self.assertTrue(result["impossible"])
        self.assertEqual(result["C198_target_basis_dimension"], 36)

    def test_scope_leaves_new_continuations_open(self) -> None:
        result = run()
        self.assertIn("does not rule out", result["claim_boundary"])
        self.assertIn("different source-derived endpoint object", result["gate_outcome"]["remaining_design_problem"])


if __name__ == "__main__":
    unittest.main()
