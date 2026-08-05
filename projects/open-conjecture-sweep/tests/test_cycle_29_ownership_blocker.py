from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_29_ownership_blocker as check


class Cycle29OwnershipBlockerTest(unittest.TestCase):
    def test_exact_audit(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["independent_replay"], "PASS")
        self.assertEqual(result["p199_max_rank"], 3)


if __name__ == "__main__":
    unittest.main()
