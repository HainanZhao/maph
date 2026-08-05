#!/usr/bin/env python3
"""Audit the exact C53 directional-local-stability inputs."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle53-analytic-local-stability"


def audit():
    a = json.loads((OUT / "principal-summary.json").read_text())
    b = json.loads((OUT / "independent-summary.json").read_text())
    assert a["status"] == b["status"] == "PASS"
    for key in ("edge_count", "subsets", "pair_adjacent", "pair_disjoint", "minimum_degree_two_by_edges", "four_cycle_count"):
        assert a[key] == b[key]
    assert a["edge_count"] == 15 and a["subsets"] == 32768
    assert (a["pair_adjacent"], a["pair_disjoint"], a["four_cycle_count"]) == (30, 75, 5)
    assert a["minimum_degree_two_by_edges"].get("3", 0) == 0
    control = a["trace_control"]
    assert control["raw_Q4"] == a["four_cycle_count"] * control["q"] ** 6 * control["trace_B4"]
    return {"status": "PASS", "epistemic_status": "PROVED", "edge_count": 15,
            "subsets": 32768, "adjacent_pairs": 30, "disjoint_pairs": 75,
            "four_cycles": 5, "kernel_cubic_survivors": 0,
            "claim_boundary": "Directional local stability only for nonzero bounded symmetric zero-mean kernels at W=1/2; no uniform neighborhood, other density, or Sidorenko theorem."}


if __name__ == "__main__":
    print(json.dumps(audit(), sort_keys=True))
