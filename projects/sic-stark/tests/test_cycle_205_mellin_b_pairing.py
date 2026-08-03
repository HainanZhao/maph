from __future__ import annotations

import unittest

from proof.verify_cycle_205_mellin_b_pairing import run


class MellinBPairingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.result = run()

    def test_local_pole_is_forced_and_weight_one(self) -> None:
        pole = self.result["local_mellin_singularity"]
        self.assertEqual(pole["forced_pole"], "z=-1")
        self.assertEqual(pole["forced_residue_abel_rate_weight"], 1)
        self.assertEqual(pole["leading_term_laurent_finite_coefficient"], "0")

    def test_residue_ledger_keeps_all_rows_but_not_target_weight(self) -> None:
        rows = self.result["all_row_residue_ledger"]
        self.assertEqual(rows["row_count"], 36)
        self.assertEqual(rows["rate_weight"], 1)

    def test_only_boundary_can_survive_rate_invariance(self) -> None:
        result = self.result["local_operation_consequence"]
        combination = result["candidate_3_rate_independent_linear_combination_with_B"]
        self.assertEqual(combination["surviving_boundary_rank_upper_bound"], 30)
        self.assertEqual([row["q"] for row in result["contradictions"]], [2, 3, 5])

    def test_scope_keeps_global_pairing_open(self) -> None:
        self.assertIn("does not exclude", self.result["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
