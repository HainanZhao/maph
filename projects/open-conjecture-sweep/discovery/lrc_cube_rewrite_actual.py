#!/usr/bin/env python3
"""Cycle 48 exact Möbius/cube repair and critical-diamond classification."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path
import time

from lrc_cube_rewrite import cell_allowed, clean, mobius_tensor, normal_form, pair_marginals, serialize_tensor, subtract_normalized, triangular_choices

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle48-cube-rewrite"


def parse_tensor(rows):
    return {tuple(cell): Fraction(numerator, denominator) for cell, numerator, denominator in rows}


def classify(row):
    types = tuple(row["types"])
    supports = tuple(tuple(values) for values in row["supports"])
    distinguished = tuple(row["distinguished"])
    pair_deleted = {(left, right): deleted for left, right, deleted in row["pair_deleted"]}
    triple_deleted = row["triple_deleted"]
    pair_flows = {(left, right): parse_tensor(values) for left, right, values in row["pair_flows"]}
    mobius = mobius_tensor(pair_flows, distinguished)
    if pair_marginals(mobius) != pair_flows:
        raise AssertionError("Möbius marginal failure")
    forbidden = {cell for cell in itertools.product(*supports) if not cell_allowed(types, cell, pair_deleted, triple_deleted)}
    defects = {cell: value for cell, value in mobius.items() if cell in forbidden and value}
    if len(defects) != row["mobius_defects"]:
        raise AssertionError("frozen defect descriptor mismatch")

    choices_by_pivot = {}
    reducers = {}
    cube_candidates = 0
    for pivot in sorted(forbidden):
        choices = triangular_choices(pivot, supports, forbidden)
        choices_by_pivot[pivot] = choices
        reducers[pivot] = choices[0][1] if choices else None
        cube_candidates += len(choices)
    repaired = normal_form(mobius, forbidden, reducers)
    if repaired["status"] == "REPAIRED":
        if pair_marginals(repaired["tensor"]) != pair_flows:
            raise AssertionError("repair marginal failure")
        if set(repaired["tensor"]) & forbidden:
            raise AssertionError("forbidden repaired support")
        repair_status = "STRONG_REPAIR" if all(reducers.values()) else "TARGETED_REPAIR"
    else:
        repair_status = "UNREPAIRED"

    first_diamond = None
    diamonds = 0
    if repaired["status"] == "REPAIRED":
        for pivot, _scale in repaired["steps"]:
            chosen = reducers[pivot]
            for alternatives, candidate in choices_by_pivot[pivot][1:]:
                diamonds += 1
                difference = subtract_normalized(candidate, chosen, pivot)
                normalized = normal_form(difference, forbidden, reducers)
                if normalized["status"] == "UNREPAIRED" or normalized["tensor"]:
                    first_diamond = {
                        "pivot": list(pivot), "alternative_owners": list(alternatives),
                        "status": "UNJOINABLE" if normalized["status"] == "REPAIRED" else "UNREPAIRED_BRANCH_DIFFERENCE",
                        "difference": serialize_tensor(difference),
                        "normal_form": serialize_tensor(normalized["tensor"]),
                        "first_missing": list(normalized["first_missing"]) if normalized["first_missing"] else None,
                    }
                    if any(pair_marginals(difference).values()) or any(pair_marginals(normalized["tensor"]).values()):
                        raise AssertionError("diamond marginal failure")
                    break
            if first_diamond:
                break

    result = {
        "types": list(types), "selection_hash": row["selection_hash"],
        "support_sizes": row["support_sizes"], "forbidden_cells": len(forbidden),
        "mobius": serialize_tensor(mobius), "mobius_defects": len(defects),
        "repair_status": repair_status, "repair_steps": len(repaired["steps"]),
        "first_missing": list(repaired["first_missing"]) if repaired["first_missing"] else None,
        "repaired_tensor": serialize_tensor(repaired["tensor"]),
        "cube_candidates": cube_candidates, "critical_diamonds_tested": diamonds,
        "confluence_status": "NONCONFLUENT" if first_diamond else "NO_NONJOINABLE_REACHED_DIAMOND",
        "first_diamond": first_diamond,
    }
    return result


def main():
    started = time.monotonic()
    selection_path = OUT / "selection.json"
    selection = json.loads(selection_path.read_text())
    selector_hash = hashlib.sha256(selection_path.read_bytes()).hexdigest()
    rows = []
    checkpoint_path = OUT / "actual-checkpoint.json"
    if checkpoint_path.is_file():
        checkpoint = json.loads(checkpoint_path.read_text())
        if checkpoint["selector_hash"] != selector_hash:
            raise AssertionError("checkpoint selector mismatch")
        rows = checkpoint["records"]
        if [row["selection_hash"] for row in rows] != [row["selection_hash"] for row in selection["selected"][:len(rows)]]:
            raise AssertionError("checkpoint prefix mismatch")
    for ordinal, source in enumerate(selection["selected"][len(rows):], start=len(rows)):
        row = classify(source)
        row["ordinal"] = ordinal
        rows.append(row)
        if (ordinal + 1) % 16 == 0:
            checkpoint = {"status": "LIVE", "selector_hash": selector_hash, "records": rows}
            temporary = checkpoint_path.with_suffix(".json.tmp")
            temporary.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
            temporary.replace(checkpoint_path)
        if (ordinal + 1) % 16 == 0:
            print(json.dumps({"completed": ordinal + 1, "repair_status": row["repair_status"], "confluence_status": row["confluence_status"]}), flush=True)

    checkpoint = {"status": "LIVE", "selector_hash": selector_hash, "records": rows}
    temporary = checkpoint_path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(checkpoint, indent=2, sort_keys=True) + "\n")
    temporary.replace(checkpoint_path)

    overlap = {tuple(row["triple"]): parse_tensor(row["coefficients"]) for row in json.loads((ROOT / "discovery/out/cycle47-affine-descent/canonical-section-localized.json").read_text())["face_tensors"]}
    comparisons = []
    for row in rows:
        types = tuple(row["types"])
        if types not in overlap or row["repair_status"] == "UNREPAIRED":
            continue
        repaired = parse_tensor(row["repaired_tensor"])
        difference = defaultdict(Fraction, repaired)
        for cell, value in overlap[types].items():
            difference[cell] -= value
        difference = clean(difference)
        if any(pair_marginals(difference).values()):
            raise AssertionError("comparison difference has nonzero pair marginal")
        comparisons.append({"types": list(types), "equal": not difference, "difference_nonzero": len(difference)})

    first_unrepaired = next((row for row in rows if row["repair_status"] == "UNREPAIRED"), None)
    first_nonconfluent = next((row for row in rows if row["first_diamond"]), None)
    result = {
        "status": "PASS", "epistemic_status": "PROVED", "stage": "MOBIUS_TRIANGULAR_CUBE_REWRITE",
        "selected_faces": len(rows),
        "repair_status_counts": dict(sorted(Counter(row["repair_status"] for row in rows).items())),
        "confluence_status_counts": dict(sorted(Counter(row["confluence_status"] for row in rows).items())),
        "mobius_defect_faces": sum(bool(row["mobius_defects"]) for row in rows),
        "aggregate_forbidden_cells": sum(row["forbidden_cells"] for row in rows),
        "aggregate_cube_candidates": sum(row["cube_candidates"] for row in rows),
        "aggregate_repair_steps": sum(row["repair_steps"] for row in rows),
        "aggregate_critical_diamonds": sum(row["critical_diamonds_tested"] for row in rows),
        "first_unrepaired": first_unrepaired,
        "first_nonconfluent": first_nonconfluent,
        "comparison_overlap": len(comparisons), "comparison_equal": sum(row["equal"] for row in comparisons),
        "comparison_zero_marginal_differences": sum(not row["equal"] for row in comparisons),
        "comparisons": comparisons, "records": rows,
        "claim_boundary": "Exact formula-and-rewrite classification of the frozen face corpus only; no universal p199, degree-four, leaf, or LRC conclusion.",
        "wall_seconds": time.monotonic() - started,
    }
    if result["aggregate_cube_candidates"] > 500_000_000 or result["aggregate_repair_steps"] > 2_000_000 or result["aggregate_critical_diamonds"] > 10_000_000:
        raise RuntimeError("Cycle 48 aggregate cap")
    path = OUT / "actual.json"
    temporary = path.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    temporary.replace(path)
    print(json.dumps({key: result[key] for key in result if key not in ("records", "comparisons", "first_unrepaired", "first_nonconfluent", "claim_boundary")}, sort_keys=True))


if __name__ == "__main__":
    main()
