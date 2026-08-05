#!/usr/bin/env python3
"""Lightweight audit for Cycle 28's portfolio-selected cyclic LP census."""
from __future__ import annotations

from collections import Counter
import csv
import json
import math
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_portfolio_cyclic_width_five as portfolio

OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def audit() -> dict[str, object]:
    sources = portfolio.load_sources()
    controls = portfolio.source_control(sources)
    expected_controls = {
        "c21_b3_l94": {"base_index": 3, "leaf_ordinal": 94, "W": 4107, "U": 4080, "margin": 27},
        "c21_b4_l104": {"base_index": 4, "leaf_ordinal": 104, "W": 65539, "U": 65448, "margin": 91},
        "c21_b4_l83": {"base_index": 4, "leaf_ordinal": 83, "W": 4091, "U": 4090, "margin": 1},
        "c22_b4_l952": {"base_index": 4, "leaf_ordinal": 952, "W": 65528, "U": 65440, "margin": 88},
    }
    assert controls == expected_controls
    assert json.loads((OUT / "control.json").read_text(encoding="utf-8")) == expected_controls

    selection = rows(OUT / "selection.tsv")
    results = rows(OUT / "results.tsv")
    targets = portfolio.targets()
    assert len(selection) == len(results) == len(targets) == 60
    assert [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in selection] == targets
    assert [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in results] == targets
    assert all(row["status"] == "SELECTED" for row in selection)
    assert all(row["status"] == "UNRESOLVED" for row in results)

    baseline = portfolio.partition_text(portfolio.cyclic_partitions()[0][1])
    assert all(row["partition"] != baseline for row in selection)
    rotations = Counter(int(row["selected_rotation"]) for row in selection)
    assert rotations == Counter({2: 6, 3: 20, 4: 17, 5: 17})

    rounds: list[int] = []
    cuts: list[int] = []
    objectives: list[float] = []
    for chosen, result in zip(selection, results, strict=True):
        assert (
            result["selected_rotation"],
            result["partition"],
            result["selector_score"],
            result["selector_capacities"],
        ) == (
            chosen["selected_rotation"],
            chosen["partition"],
            chosen["score"],
            chosen["capacities"],
        )
        objective = float(result["objective"])
        assert math.isfinite(objective) and objective >= 1 - portfolio.TOL
        assert result["denominator"] == result["support"] == result["W"] == result["U"] == "0"
        rounds.append(int(result["separation_rounds"]))
        cuts.append(int(result["cuts"]))
        objectives.append(objective)
    assert (min(rounds), max(rounds), min(cuts), max(cuts)) == (20, 117, 58, 236)

    coarse = json.loads((OUT / "independent-replay-error-tranche2.json").read_text(encoding="utf-8"))
    assert coarse["status"] == "FAIL" and coarse["error"] == "LP mismatch"
    assert "replay_cycle_28_portfolio_independent.py" in coarse["traceback"]

    diagnostic = json.loads((OUT / "independent-lp-diagnostic.json").read_text(encoding="utf-8"))
    diagnostic_rows = rows(OUT / "independent-lp-diagnostic.tsv")
    classes = Counter(row["classification"] for row in diagnostic_rows)
    assert diagnostic["status"] == "MISMATCH"
    assert diagnostic["matched_rows"] == 35 and diagnostic["persisted_rows"] == 36
    assert classes == Counter({"MATCH": 35, "MISMATCH": 1})
    mismatch = [row for row in diagnostic_rows if row["classification"] == "MISMATCH"]
    assert len(mismatch) == 1
    assert mismatch[0] == {
        "base_index": "3", "leaf_ordinal": "91", "classification": "MISMATCH",
        "expected_objective": "1", "observed_objective": "1", "objective_delta": "0",
        "expected_rounds": "28", "observed_rounds": "26",
        "expected_cuts": "80", "observed_cuts": "74", "detail": "",
    }
    assert diagnostic["terminal_row"] == {
        "base_index": 3, "leaf_ordinal": 91, "classification": "MISMATCH",
        "expected_objective": "1", "observed_objective": "1", "objective_delta": "0",
        "expected_rounds": "28", "observed_rounds": 26,
        "expected_cuts": "80", "observed_cuts": 74, "detail": "",
    }
    for row in diagnostic_rows:
        key = (int(row["base_index"]), int(row["leaf_ordinal"]))
        assert key in targets
        if row["classification"] == "MATCH":
            expected = results[targets.index(key)]
            assert row["expected_objective"] == row["observed_objective"] == expected["objective"]
            assert row["expected_rounds"] == row["observed_rounds"] == expected["separation_rounds"]
            assert row["expected_cuts"] == row["observed_cuts"] == expected["cuts"]

    thread = json.loads((OUT / "thread-trace-control.json").read_text(encoding="utf-8"))
    assert thread["status"] == "PASS" and thread["epistemic_status"] == "OBSERVED"
    assert (thread["base_index"], thread["leaf_ordinal"], thread["objective"], thread["rounds"], thread["cuts"]) == (3, 91, 1.0, 28, 80)
    assert thread["matches_primary_trace"] is True
    assert thread["matches_unpinned_independent_trace"] is False
    return {
        "status": "PASS",
        "epistemic_status": "OBSERVED",
        "source_controls": expected_controls,
        "targets": 60,
        "nonbaseline_selections": 60,
        "rotation_counts": {str(key): rotations[key] for key in sorted(rotations)},
        "fully_separated_unresolved": 60,
        "rounds_min": min(rounds),
        "rounds_max": max(rounds),
        "cuts_min": min(cuts),
        "cuts_max": max(cuts),
        "objective_float_min": min(objectives),
        "objective_float_max": max(objectives),
        "certified_leaves": [],
        "closure_status": "INCOMPLETE_AUDIT_CONTAINMENT",
        "independent_lp_trace_matches": 35,
        "independent_lp_trace_mismatches": 1,
        "independent_lp_traces_unconfirmed": 24,
        "thread_classification": "ONE_THREAD_REPRODUCES_PRIMARY_28_ROUNDS_80_CUTS",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
