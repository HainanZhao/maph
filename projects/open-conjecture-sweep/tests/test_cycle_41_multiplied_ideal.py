from __future__ import annotations

import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("cycle41_audit", ROOT / "proof/check_cycle_41_multiplied_ideal.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class Cycle41MultipliedIdealTest(unittest.TestCase):
    def test_exact_first_multiplied_layer(self) -> None:
        result = MODULE.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["small_type_triples"], 11279048)
        self.assertEqual(result["exact_relation_evaluations"], 1808327)
        self.assertEqual(result["dense_support_minimum"], 9)


if __name__ == "__main__":
    unittest.main()
