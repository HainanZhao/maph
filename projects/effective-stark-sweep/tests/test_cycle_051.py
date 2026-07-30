"""Regression tests for the theorem-value closure selection."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class Cycle051Test(unittest.TestCase):
    def test_exponent_pilot_was_frozen_and_completed(self) -> None:
        freeze_path = (
            ROOT / "data" / "theorem-value-exponent-pilot-v1.json"
        )
        result = json.loads(
            (
                ROOT / "artifacts"
                / "theorem-value-exponent-pilot-v1.json"
            ).read_text()
        )
        self.assertEqual(result["record_count"], 9)
        self.assertEqual(
            result["freeze_sha256"],
            hashlib.sha256(freeze_path.read_bytes()).hexdigest(),
        )
        measured = {
            (row["case_id"], row["route_label"]): row["safe_exponent"]
            for row in result["records"]
        }
        self.assertEqual(measured[("RQ-000021", "selected")], 2016)
        self.assertEqual(measured[("RQ-002057", "selected")], 2592)
        self.assertEqual(
            measured[("RQ-000108", "sqrt_minus_15")], 2880
        )
        self.assertEqual(measured[("RQ-007487", "selected")], 3840)
        self.assertEqual(measured[("RQ-002955", "selected")], 4032)
        self.assertEqual(measured[("RQ-006512", "selected")], 12096)
        self.assertEqual(measured[("RQ-000686", "selected")], 12096)
        self.assertEqual(measured[("RQ-001107", "selected")], 15840)

    def test_generic_engine_matches_banked_controls(self) -> None:
        controls = (
            ROOT / "artifacts"
            / "theorem-value-exponent-controls-v1.txt"
        ).read_text()
        self.assertIn("generic safe exponent      = 4032", controls)
        self.assertIn("generic safe exponent      = 13810176", controls)
        self.assertIn("GENERIC_EXPONENT_CONTROLS_MATCH=1", controls)
        failed = (
            ROOT / "artifacts"
            / "theorem-value-exponent-control-failed-v0.txt"
        ).read_text()
        self.assertIn("incorrectly printed a", failed)
        self.assertIn("success marker afterward", failed)

    def test_five_closure_portfolio(self) -> None:
        selection = json.loads(
            (
                ROOT / "artifacts" / "theorem-value-selection-v1.json"
            ).read_text()
        )
        selected = selection["additional_selected"]
        self.assertEqual(selection["additional_selected_count"], 5)
        self.assertEqual(
            [row["case_id"] for row in selected],
            [
                "RQ-000108",
                "RQ-000021",
                "RQ-002057",
                "RQ-002955",
                "RQ-001107",
            ],
        )
        self.assertEqual(
            [row["safe_exponent"] for row in selected],
            [2880, 2016, 2592, 4032, 15840],
        )
        self.assertEqual(
            selection["explicitly_deprioritized"][0]["case_id"],
            "RQ-004467",
        )
        self.assertEqual(
            selection["explicitly_deprioritized"][0]["safe_exponent"],
            13810176,
        )
        self.assertEqual(
            selection["execution_order"][:2],
            ["RQ-000129", "RQ-000419"],
        )


if __name__ == "__main__":
    unittest.main()
