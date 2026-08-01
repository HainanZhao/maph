import importlib.util
from pathlib import Path
import unittest


PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "proof" / "audit_cycle1_routes.py"
SPEC = importlib.util.spec_from_file_location("cycle1_reconciliation", SCRIPT)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class Cycle1ReconciliationTests(unittest.TestCase):
    def test_routes_agree_with_integrity(self) -> None:
        result = MODULE.audit()
        self.assertTrue(result["passed"])
        self.assertTrue(all(result["integrity"].values()))
        for comparison in result["labeled_comparisons"].values():
            self.assertTrue(comparison["agree"])

    def test_routes_do_not_claim_shared_implementation(self) -> None:
        result = MODULE.audit()
        self.assertFalse(result["route_independence"]["shared_implementation"])


if __name__ == "__main__":
    unittest.main()

