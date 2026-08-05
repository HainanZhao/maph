import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from check_cycle_50_deletion_aware_packet import audit


class Cycle50DeletionAwarePacketTest(unittest.TestCase):
    def test_theorem_falsifier_is_exact_and_replayed(self):
        result = audit()
        self.assertEqual(result["status"], "THEOREM_FAIL")
        self.assertEqual(result["selected_type_triples"], 29050)
        self.assertEqual(result["buffer_incomplete"], 2)


if __name__ == "__main__":
    unittest.main()
