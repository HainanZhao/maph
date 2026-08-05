from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cycle40_audit", ROOT / "proof/check_cycle_40_signed_moments.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Cycle40SignedMomentsTest(unittest.TestCase):
    def test_exact_signed_degree_three_construction(self) -> None:
        result = MODULE.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["pair_classes"], 694912)
        self.assertEqual(result["triple_classes"], 693)
        self.assertEqual(result["unresolved"], 0)


if __name__ == "__main__":
    unittest.main()
