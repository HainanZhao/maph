from __future__ import annotations

import unittest

from proof.verify_cycle_209_fixed_diagonal_projective_interface import run


class FixedDiagonalProjectiveInterfaceTests(unittest.TestCase):
    def setUp(self):
        self.result = run()

    def test_source_ratio_holds_on_all_channels(self):
        audit = self.result["source_ratio_audit"]
        self.assertEqual(len(audit["records"]), 6)
        self.assertEqual(audit["all_h_ratio"], "t^4")

    def test_exact_witnesses_are_distinct(self):
        witnesses = self.result["fixed_diagonal_contradiction"]["witnesses"]
        self.assertEqual(witnesses, [{"t": "2", "t_to_fourth": "16"}, {"t": "3", "t_to_fourth": "81"}])
        self.assertTrue(self.result["fixed_diagonal_contradiction"]["contradiction"])

    def test_scope_retains_broader_interfaces(self):
        self.assertEqual(
            self.result["gate_outcome"]["fixed_diagonal_all_source_family_interface"],
            "FALSIFIED",
        )


if __name__ == "__main__":
    unittest.main()
