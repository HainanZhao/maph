#!/usr/bin/env python3
"""Regression checks for the B5-025 label-aware successor ledger."""
from __future__ import annotations
import json
from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class EngineBTransportLedgerV4Test(unittest.TestCase):
 def test_twelve_named_promotions_only(self):
  ledger=json.loads((ROOT/"artifacts/engine-b-transport-ledger-v4.json").read_text())
  self.assertEqual(ledger["counts"],{"v5_engine_b_rows":232,"member_transport_completed":12,"member_transport_open":220})
  done=sorted(r["case_id"] for r in ledger["members"] if r["transport_status"]=="PROVED_EXACT_MEMBER_TRANSPORT")
  self.assertEqual(done,["RQ-000039","RQ-000195","RQ-000200","RQ-000205","RQ-000213","RQ-000221","RQ-000228","RQ-000425","RQ-000436","RQ-000457","RQ-000459","RQ-000465"])
if __name__=="__main__":unittest.main()
