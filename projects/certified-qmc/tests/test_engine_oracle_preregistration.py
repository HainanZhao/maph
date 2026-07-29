from __future__ import annotations

from hashlib import sha256
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
PREREG = ROOT / "data" / "engine-oracle-set-v1.json"


class EngineOraclePreregistrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = json.loads(PREREG.read_text())

    def test_selection_self_hash_and_counts(self):
        payload = dict(self.payload)
        supplied = payload.pop("selection_sha256")
        canonical = json.dumps(
            payload, sort_keys=True, separators=(",", ":")
        )
        self.assertEqual(
            supplied, sha256(canonical.encode()).hexdigest()
        )
        self.assertEqual(
            payload["selection_status"],
            "PREREGISTERED_BEFORE_VALUE_EXTRACTION",
        )
        self.assertEqual(
            payload["selection_counts"],
            {
                "table_merits": 290,
                "adversarial_decision_cases": 8,
                "total_oracle_cases": 298,
            },
        )

    def test_table_selection_is_unique_and_structurally_complete(self):
        rows = self.payload["table_merits"]
        keys = {
            (
                row["source_id"],
                row["N"],
                row["dimension"],
                row["weight_power"],
            )
            for row in rows
        }
        self.assertEqual(len(keys), 290)
        families = {
            "unsw-fixed-29102",
            "unsw-extensible-39102",
        }
        for family in families:
            low_prefix = {
                row["dimension"]
                for row in rows
                if row["source_id"] == family
                and row["N"] == 1024
                and row["weight_power"] == 2
                and row["dimension"] <= 64
            }
            self.assertEqual(low_prefix, set(range(1, 65)))
            for power in (1, 2, 3):
                self.assertTrue(
                    any(
                        row["source_id"] == family
                        and row["weight_power"] == power
                        for row in rows
                    )
                )
            for exponent in range(10, 21):
                self.assertTrue(
                    any(
                        row["source_id"] == family
                        and row["N"] == 1 << exponent
                        for row in rows
                    )
                )

    def test_adversarial_cases_include_ties_and_precision_stress(self):
        cases = self.payload["adversarial_decision_cases"]
        purposes = " ".join(case["purpose"] for case in cases)
        self.assertIn("exact", purposes)
        self.assertIn("tiny", purposes)
        self.assertIn("denominator", purposes)
        self.assertTrue(
            any("0" in case["weights"] for case in cases)
        )


if __name__ == "__main__":
    unittest.main()
