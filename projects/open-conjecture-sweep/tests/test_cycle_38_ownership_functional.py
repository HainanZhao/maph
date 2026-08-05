from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cycle38_audit", ROOT / "proof/check_cycle_38_ownership_functional.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Cycle38OwnershipFunctionalTest(unittest.TestCase):
    def test_exact_rooted_span_obstruction(self) -> None:
        result = MODULE.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["roots"], 13)
        self.assertEqual(result["concrete_blockers"], 190867444)
        self.assertEqual(result["augmented_left_null_rhs"], 300)


if __name__ == "__main__":
    unittest.main()
