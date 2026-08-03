"""Regression checks for Cycle 225's reflection-root branch."""
from __future__ import annotations

import sys
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from verify_cycle_225_reflection_root_branch import run  # noqa: E402


class ReflectionRootBranchTests(unittest.TestCase):
    def test_local_branch_closes_but_factorization_states_are_missing(self) -> None:
        result = run()
        roots = result["root_branch_audit"]
        self.assertEqual(roots["candidate_count"], 4)
        self.assertEqual(roots["roots"], ["+i", "-i"])
        self.assertTrue(all(row["first_shift"] and row["second_shift"] for row in roots["rows"]))
        action = result["double_sign_action_audit"]
        self.assertTrue(all(row["conjugate_action_involutive"] for row in action["rows"]))
        self.assertTrue(all(not row["preserve_action_involutive"] for row in action["rows"]))
        factors = result["factorization_state_audit"]
        self.assertFalse(factors["equation_16_pullback_defined"])
        self.assertFalse(factors["equation_17_pullback_defined"])
        self.assertFalse(result["acceptance_audit"]["accepted_signed_extension"])


if __name__ == "__main__":
    unittest.main()
