#!/usr/bin/env python3
"""Regression checks for the corrected B5-025 transport batch ledger."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EngineBTransportLedgerV2Test(unittest.TestCase):
    def test_five_named_promotions_only(self) -> None:
        ledger = json.loads((ROOT / "artifacts/engine-b-transport-ledger-v2.json").read_text())
        self.assertEqual(ledger["counts"], {
            "v5_engine_b_rows": 232,
            "member_transport_completed": 5,
            "member_transport_open": 227,
        })
        completed = sorted(row["case_id"] for row in ledger["members"]
                           if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT")
        self.assertEqual(completed, ["RQ-000039", "RQ-000195", "RQ-000200", "RQ-000205", "RQ-000213"])


if __name__ == "__main__":
    unittest.main()
