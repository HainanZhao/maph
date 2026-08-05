import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
from check_cycle_49_relative_diagonal import audit


class Cycle49RelativeDiagonalTest(unittest.TestCase):
    def test_complete_domain_boundary(self):
        checked = audit()
        self.assertEqual(checked["status"], "PASS")
        self.assertEqual(checked["raw_valid_type_triples"], 382_453_319)
        self.assertEqual(checked["frozen_formula_closed"], 382_453_314)
        self.assertEqual(checked["buffer_incomplete"], 5)

    def test_generic_controls(self):
        controls = json.loads((ROOT / "discovery/out/cycle49-relative-diagonal/generic-controls.json").read_text())
        self.assertEqual(controls["triple_packet_support_checks"], 7680)
        self.assertEqual(controls["pair_packet_support_checks"], 2520)
        self.assertEqual(controls["support_five_buffer_checks"], 1296)
        self.assertTrue(controls["repeated_buffer_spill_detected"])

    def test_independent_exception_labels(self):
        checked = audit()
        self.assertEqual(checked["exception_types"], [
            [4, 4, 5], [4, 4, 6], [4, 4, 64], [4, 5, 35], [4, 6, 35],
        ])
        self.assertEqual(checked["first_terminal_classification"], "BUFFER_INCOMPLETE")


if __name__ == "__main__":
    unittest.main()
