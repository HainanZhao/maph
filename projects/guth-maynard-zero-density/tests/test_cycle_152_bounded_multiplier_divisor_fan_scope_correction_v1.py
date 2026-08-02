import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class BoundedMultiplierDivisorFanScopeCorrectionTests(unittest.TestCase):
    def test_original_record_is_preserved_and_conditional(self) -> None:
        original = json.loads((ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1.json").read_text())
        self.assertEqual(original["epistemic_status"], "PROVED")
        self.assertIn("conditional", original["claim_boundary"])

    def test_corrected_status_is_narrow(self) -> None:
        corrected = json.loads(
            (ROOT / "artifacts/cycle-152-bounded-multiplier-divisor-fan-v1-scope-correction.json").read_text()
        )
        self.assertEqual(corrected["status"], "SEALED_CONDITIONAL_BOUNDED_MULTIPLIER_DIVISOR_FAN_INVERSE")
        self.assertIn("actual complement", corrected["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
