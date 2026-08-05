#!/usr/bin/env python3
"""Audit the frozen C65 direct 2x2 step-graphon packet."""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery" / "out" / "cycle65-step-graphon"
SEEDS = (650651, 650652, 650653)


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def audit() -> dict[str, object]:
    best_scores = []
    total_trials = 0
    for seed in SEEDS:
        summary = load(OUT / "search" / f"summary-{seed}.json")
        assert summary["seed"] == seed
        assert summary["population"] == 256
        assert summary["generations"] == 4000
        assert summary["trial_evaluations"] == 1_024_000
        assert summary["retained_distinct"] == 32
        total_trials += summary["trial_evaluations"]
        best_scores.append(summary["best_log_ratio"])
        with (OUT / "search" / f"candidates-{seed}.tsv").open(
            newline="", encoding="utf-8"
        ) as handle:
            rows = list(csv.DictReader(handle, delimiter="\t"))
        assert len(rows) == 32
        assert all(int(row["seed"]) == seed for row in rows)

    exact = load(OUT / "exact" / "exact-summary.json")
    assert exact == {
        "status": "PASS",
        "epistemic_status": "PROVED",
        "grid_rows": 3125,
        "grid_negative": 0,
        "grid_zero": 809,
        "grid_zero_constant_effective_support": 809,
        "grid_zero_other": 0,
        "grid_positive": 2316,
        "candidate_rows": 96,
        "candidate_negative": 0,
        "candidate_zero": 0,
        "candidate_positive": 96,
        "independent_direct_controls": 3,
    }
    with (OUT / "exact" / "exact-candidates.tsv").open(
        newline="", encoding="utf-8"
    ) as handle:
        exact_rows = list(csv.DictReader(handle, delimiter="\t"))
    assert len(exact_rows) == 96
    assert all(row["sign"] == "1" for row in exact_rows)
    for path in (OUT / "runtime").glob("search-*.txt"):
        text = path.read_text(encoding="utf-8")
        assert "Maximum resident set size" in text
        assert "Exit status: 0" in text
    exact_runtime = (OUT / "runtime" / "exact.txt").read_text(encoding="utf-8")
    assert "Maximum resident set size" in exact_runtime
    assert "Exit status: 0" in exact_runtime
    assert (OUT / "runtime" / "compiler.txt").read_text(encoding="utf-8").startswith("g++")

    return {
        "status": "PASS",
        "bounded_search": {
            "epistemic_status": "OBSERVED",
            "streams": 3,
            "aggregate_trials": total_trials,
            "best_log_ratio_by_seed": best_scores,
            "interpretation": "All apparent floating negatives are cancellation-scale and fail exact negative replay.",
        },
        "exact_finite_checks": {
            "epistemic_status": "PROVED",
            **{key: value for key, value in exact.items()
               if key not in {"status", "epistemic_status"}},
        },
        "claim_boundary": (
            "No counterexample occurs on the complete denominator-4 grid or among "
            "the 96 rounded retained candidates. This is not positivity on the "
            "continuous 2x2 family and gives no Sidorenko theorem."
        ),
    }


def main() -> int:
    result = audit()
    (OUT / "packet-audit.json").write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
