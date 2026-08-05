#!/usr/bin/env python3
"""Persist the first row-local discrepancy from Cycle 28's failed LP audit."""
from __future__ import annotations

import csv
import json
import multiprocessing
from pathlib import Path
import sys
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
import replay_cycle_28_portfolio_independent as independent

OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"
ROWS = OUT / "independent-lp-diagnostic.tsv"
RESULT = OUT / "independent-lp-diagnostic.json"
WALL_SECONDS = 2700
FIELDS = (
    "base_index", "leaf_ordinal", "classification", "expected_objective",
    "observed_objective", "objective_delta", "expected_rounds",
    "observed_rounds", "expected_cuts", "observed_cuts", "detail",
)


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def write_rows(records: dict[tuple[int, int], dict[str, object]], order: list[tuple[int, int]]) -> None:
    temporary = ROWS.with_suffix(".tsv.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for key in order:
            if key in records:
                writer.writerow(records[key])
    temporary.replace(ROWS)


def write_result(value: dict[str, object]) -> None:
    temporary = RESULT.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(RESULT)


def worker(job: tuple[dict[str, str], float]) -> dict[str, object]:
    row, deadline = job
    try:
        base, leaf, objective, rounds, cuts = independent.solve((row, deadline))
        return {
            "base_index": base,
            "leaf_ordinal": leaf,
            "observed_objective": objective,
            "observed_rounds": rounds,
            "observed_cuts": cuts,
            "error": "",
        }
    except Exception as error:  # Persist worker-local evidence before propagating.
        return {
            "base_index": int(row["base_index"]),
            "leaf_ordinal": int(row["leaf_ordinal"]),
            "error": f"{type(error).__name__}: {error}",
            "traceback": traceback.format_exc(),
        }


def classify(expected: dict[str, str], observed: dict[str, object]) -> dict[str, object]:
    base, leaf = int(expected["base_index"]), int(expected["leaf_ordinal"])
    if observed["error"]:
        return {
            "base_index": base, "leaf_ordinal": leaf, "classification": "ERROR",
            "expected_objective": expected["objective"], "observed_objective": "",
            "objective_delta": "", "expected_rounds": expected["separation_rounds"],
            "observed_rounds": "", "expected_cuts": expected["cuts"],
            "observed_cuts": "", "detail": observed["error"],
        }
    value = float(observed["observed_objective"])
    delta = abs(value - float(expected["objective"]))
    same_rounds = int(observed["observed_rounds"]) == int(expected["separation_rounds"])
    same_cuts = int(observed["observed_cuts"]) == int(expected["cuts"])
    classification = "MATCH" if (
        expected["status"] == "UNRESOLVED"
        and value >= 1 - independent.TOL
        and delta <= 1e-8
        and same_rounds
        and same_cuts
    ) else "MISMATCH"
    return {
        "base_index": base, "leaf_ordinal": leaf, "classification": classification,
        "expected_objective": expected["objective"],
        "observed_objective": f"{value:.17g}", "objective_delta": f"{delta:.17g}",
        "expected_rounds": expected["separation_rounds"],
        "observed_rounds": observed["observed_rounds"], "expected_cuts": expected["cuts"],
        "observed_cuts": observed["observed_cuts"], "detail": "",
    }


def main() -> int:
    started = time.monotonic()
    expected_rows = independent.read(independent.RESULTS)
    order = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in expected_rows]
    expected = {key: row for key, row in zip(order, expected_rows, strict=True)}
    if len(expected) != len(order) != 0 or len(order) != 60:
        raise AssertionError("target census")
    recorded: dict[tuple[int, int], dict[str, object]] = {}
    if ROWS.is_file():
        for row in read_rows(ROWS):
            key = (int(row["base_index"]), int(row["leaf_ordinal"]))
            if key not in expected or row["classification"] != "MATCH":
                raise AssertionError("invalid resumable diagnostic row")
            recorded[key] = row
    pending = [row for key, row in zip(order, expected_rows, strict=True) if key not in recorded]
    deadline = started + WALL_SECONDS
    pool = multiprocessing.Pool(processes=3)
    terminal: dict[str, object] | None = None
    try:
        for observed in pool.imap_unordered(worker, [(row, deadline) for row in pending], chunksize=1):
            key = (int(observed["base_index"]), int(observed["leaf_ordinal"]))
            row = classify(expected[key], observed)
            recorded[key] = row
            write_rows(recorded, order)
            if row["classification"] != "MATCH":
                terminal = row
                pool.terminate()
                break
        else:
            pool.close()
    finally:
        pool.join()
    elapsed = time.monotonic() - started
    if terminal is not None:
        status = "MISMATCH" if terminal["classification"] == "MISMATCH" else "ERROR"
    elif len(recorded) == 60:
        status = "NO_MISMATCH_REPRODUCED"
    else:
        status = "CAP"
    outcome = {
        "status": status,
        "epistemic_status": "OBSERVED",
        "matched_rows": sum(row["classification"] == "MATCH" for row in recorded.values()),
        "persisted_rows": len(recorded),
        "terminal_row": terminal,
        "wall_seconds": elapsed,
    }
    write_result(outcome)
    print(json.dumps(outcome, indent=2, sort_keys=True))
    return 0 if status in {"MISMATCH", "NO_MISMATCH_REPRODUCED"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
