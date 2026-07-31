#!/usr/bin/env python3
"""Regression checks for the successor Engine-B member ledger."""

from __future__ import annotations

import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EngineBTransportLedgerTest(unittest.TestCase):
    def test_only_first_member_is_promoted(self) -> None:
        ledger = json.loads((ROOT / "artifacts/engine-b-transport-ledger-v1.json").read_text())
        self.assertEqual(ledger["counts"], {
            "v5_engine_b_rows": 232,
            "member_transport_completed": 1,
            "member_transport_open": 231,
        })
        completed = [row for row in ledger["members"]
                     if row["transport_status"] == "PROVED_EXACT_MEMBER_TRANSPORT"]
        self.assertEqual(len(completed), 1)
        self.assertEqual(completed[0]["case_id"], "RQ-000039")
        self.assertEqual(completed[0]["source_case_id"], "RQ-000021")


if __name__ == "__main__":
    unittest.main()
