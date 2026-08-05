from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import check_cycle_30_crt_synchronization as check


class Cycle30CRTSynchronizationTest(unittest.TestCase):
    def test_exact_audit(self):
        result = check.audit()
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["p199_atoms"], 1390)
        self.assertEqual(result["p199_beyond_negation_reduction"], 4)


if __name__ == "__main__":
    unittest.main()
