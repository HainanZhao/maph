from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cycle39_audit", ROOT / "proof/check_cycle_39_priority_routing.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Cycle39PriorityRoutingTest(unittest.TestCase):
    def test_exact_priority_span_obstruction(self) -> None:
        result = MODULE.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["roots"], 13)
        self.assertEqual(result["priority_columns"], 53248)
        self.assertEqual(result["selected_rank_two_rows"], 573)


if __name__ == "__main__":
    unittest.main()
