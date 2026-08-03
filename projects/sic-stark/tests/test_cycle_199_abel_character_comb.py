from __future__ import annotations

import sys
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_199_abel_character_comb import (  # noqa: E402
    endpoint_strip_and_poles,
    formal_support_rank_test,
    run,
    triple_step_character_ratio,
)


class AbelCharacterCombTests(unittest.TestCase):
    def test_three_step_phase_is_exact(self) -> None:
        result = triple_step_character_ratio()
        self.assertEqual(result["source_phase_mod_24"], 5)
        self.assertIn("i^m", result["full_ratio"])

    def test_six_and_only_six_contour_pole_channels(self) -> None:
        result = endpoint_strip_and_poles()
        self.assertFalse(result["global_central_contour_absolute_convergence"])
        self.assertEqual(
            result["six_meromorphic_contour_pole_channels"],
            [0, 4, 8, 12, 16, 20],
        )

    def test_naive_support_loses_b_dependence(self) -> None:
        result = formal_support_rank_test()
        self.assertEqual(result["all_rows_and_residues_checked"], 108)
        self.assertEqual(result["rank_upper_bound"], 6)
        self.assertIn("only on a", result["dependence_after_naive_support_replacement"])

    def test_scope_excludes_general_no_go(self) -> None:
        result = run()
        self.assertEqual(
            result["gate_outcome"]["literal_symmetric_abel_character_insertion"],
            "OBSTRUCTED_ON_ENDPOINT_CENTRAL_CONTOUR",
        )
        self.assertIn("does not exclude", result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
