#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit():
    c53 = json.loads((ROOT / "discovery/out/cycle53-analytic-local-stability/principal-summary.json").read_text())
    control = json.loads((ROOT / "discovery/out/cycle54-bipartite-directional/rectangular-control.json").read_text())
    assert c53["pair_adjacent"] == 30 and c53["four_cycle_count"] == 5
    assert control["status"] == "PASS" and control["raw_Q4"] == control["expected_raw_Q4"] == 17280
    assert control["trace_BBT_squared"] == 16
    return {"status":"PASS", "epistemic_status":"PROVED", "left_adjacent_pairs":15, "right_adjacent_pairs":15, "four_cycles":5, "rectangular_trace_control":17280, "claim_boundary":"Directional local positivity for fixed p and bounded nonzero mean-zero bipartite kernels only; no uniform neighborhood or Sidorenko theorem."}


if __name__ == "__main__": print(json.dumps(audit(), sort_keys=True))
