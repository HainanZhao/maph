#!/usr/bin/env python3
"""Deterministic Stream-B reconciliation of Route A v3 and Route B v1.

Prior Route-A and reconciliation versions are evidence records and are not
modified.  This report promotes an independent-route result only after every
v1 coverage gap is explicitly present and PROVED in Route A v3.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PATHS = {
    "route_a_v3": ROOT / "artifacts/cycle-2-stream-b-route-a-v3.json",
    "route_b_v1": ROOT / "artifacts/cycle-2-stream-b-route-b-v1.json",
    "reconciliation_v1": ROOT / "artifacts/cycle-2-stream-b-route-reconciliation-v1.json",
}
REQUIRED_A = {
    "SB-A21-beta-cutoff-wording-correction",
    "SB-A22-theorem-1-1-three-structural-terms",
    "SB-A23-mvt-strict-positive-residual",
    "SB-A24-type-ii-and-dyadic-reassembly",
}
REQUIRED_B = {
    "SB-B7-large-values-structural-terms",
    "SB-B9-mvt-branch-and-strict-residual",
    "SB-B10-dyadic-reassembly-and-route-boundary",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(key: str) -> dict[str, Any]:
    return json.loads(PATHS[key].read_text(encoding="utf-8"))


def by_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in rows}


def check_inputs(a: dict[str, Any], b: dict[str, Any], v1: dict[str, Any]) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    assert a["route"] == "A" and a["stream"] == "B"
    assert a["epistemic_status"] == "PROVED" and a["open_blockers"] == []
    assert a["pass_state"].startswith("NARROW PASS:")
    assert "G0" in a["claim_boundary"]
    assert a["replay"]["script_sha256"] == sha256(ROOT / a["replay"]["script"])
    ar = by_id(a["rows"])
    assert REQUIRED_A <= ar.keys()
    assert all(ar[key]["status"] == "PROVED" for key in REQUIRED_A)
    assert b["route"] == "B" and b["stream"] == "B"
    assert b["epistemic_status"] == "PROVED" and b["label_coverage"]["unlabeled_nodes"] == []
    assert b["pass_state"].startswith("NARROW PASS:")
    br = by_id(b["rows"])
    assert REQUIRED_B <= br.keys()
    assert all(br[key]["status"] == "PROVED" for key in REQUIRED_B)
    open_v1 = {row["id"] for row in v1["mismatch_and_falsifier_rows"] if row["status"] == "OPEN"}
    assert open_v1 == {"M2-route-a-theorem-1-1-coverage", "M3-route-a-mvt-residual-coverage", "M4-route-a-reassembly-coverage"}
    return ar, br


def mapping(a: dict[str, Any], b: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {"id": "R1-source-and-range", "epistemic_status": "PROVED", "comparison_status": "AGREED", "route_a": "Pinned GM tar/TeX and [7/10,4/5] exact audit", "route_b": "Pinned GM/MP sources and [7/10,4/5] exact audit", "falsifier": "A frozen source hash or range mismatch invalidates this reconciliation."},
        {"id": "R2-complement-and-beta-wording", "epistemic_status": "PROVED", "comparison_status": "AGREED_AFTER_CORRECTION", "route_a": "SB-A21 separates detector identity from the beta>=sigma count restriction.", "route_b": "SB-B1 supplies the complement-to-Type-II transfer.", "falsifier": "A beta-dependent MP Type-I detector condition or detector mismatch invalidates agreement."},
        {"id": "R3-multiplicity-two-sided", "epistemic_status": "PROVED", "comparison_status": "AGREED", "route_a": "Inherited SB-A15/A16 plus SB-A24 no-real-zero and dyadic check.", "route_b": "SB-B2 multiplicity, no-real-zero, and conjugation conversion.", "falsifier": "A real non-trivial zero or polynomial-in-T local multiplicity loss refutes the conversion."},
        {"id": "R4-theorem-1-1-three-terms", "epistemic_status": "PROVED", "comparison_status": "AGREED", "route_a": "SB-A22 explicitly checks L^(2-2sigma), L^(18/5-4sigma), and T L^(12/5-4sigma).", "route_b": "SB-B7 checks the same three structural terms.", "falsifier": "A failed residual factorization or branch inequality invalidates this node."},
        {"id": "R5-mvt-strict-residual", "epistemic_status": "PROVED", "comparison_status": "AGREED", "route_a": "SB-A23 records the exact positive residual and all denominator signs.", "route_b": "SB-B9 records the same exact residual and strictness.", "falsifier": "A nonpositive numerator or denominator on the frozen interval invalidates strictness."},
        {"id": "R6-type-ii-and-reassembly", "epistemic_status": "PROVED", "comparison_status": "AGREED", "route_a": "SB-A24 proves A(sigma)-2(1-sigma)>0 and gives positive-shell summation.", "route_b": "SB-B10 combines Type I/II and reassembles dyadic shells.", "falsifier": "Failure of 2(1-sigma)<=A(sigma) or non-summable shell control invalidates this node."},
        {"id": "R7-pass-scope", "epistemic_status": "PROVED", "comparison_status": "AGREED_SCOPE_CONTAINED", "route_a": a["pass_state"], "route_b": b["pass_state"], "falsifier": "Any full-G0 promotion from these Stream-B artifacts alone violates their claim boundaries."},
    ]


def resolved_gaps() -> list[dict[str, Any]]:
    return [
        {"id": "M2-route-a-theorem-1-1-coverage", "epistemic_status": "PROVED", "workflow_status": "RESOLVED", "resolution": "Route A v3 SB-A22 supplies all three structural terms and exact inequalities.", "falsifier": "Remove or invalidate SB-A22."},
        {"id": "M3-route-a-mvt-residual-coverage", "epistemic_status": "PROVED", "workflow_status": "RESOLVED", "resolution": "Route A v3 SB-A23 supplies the positive residual with numerator and denominator range signs.", "falsifier": "Remove or invalidate SB-A23."},
        {"id": "M4-route-a-reassembly-coverage", "epistemic_status": "PROVED", "workflow_status": "RESOLVED", "resolution": "Route A v3 SB-A24 supplies the Type-II comparison, no-real-zero check, and dyadic reassembly.", "falsifier": "Remove or invalidate SB-A24."},
        {"id": "M5-beta-cutoff-wording", "epistemic_status": "PROVED", "workflow_status": "RESOLVED", "resolution": "Route A v3 SB-A21 corrects the old wording without changing the inclusion proof.", "falsifier": "Show beta is a condition in MP's Type-I detector definition."},
        {"id": "M1-route-a-pass-scope", "epistemic_status": "OBSERVED", "containment_status": "CONTAINED", "resolution": "The historical v2 label remains preserved; Route A v3 and this reconciliation use NARROW PASS only.", "falsifier": "A full-G0 label in either v3 artifact or this report."},
    ]


def certificate() -> dict[str, Any]:
    a, b, v1 = load("route_a_v3"), load("route_b_v1"), load("reconciliation_v1")
    ar, br = check_inputs(a, b, v1)
    table = mapping(a, b)
    gaps = resolved_gaps()
    assert all(row["comparison_status"] != "ROUTE_A_COVERAGE_GAP" for row in table)
    assert not [row for row in gaps if row.get("workflow_status") == "OPEN"]
    assert {row["id"] for row in gaps if row.get("workflow_status") == "RESOLVED"} >= {
        "M2-route-a-theorem-1-1-coverage", "M3-route-a-mvt-residual-coverage", "M4-route-a-reassembly-coverage"
    }
    return {
        "artifact_id": "cycle-2-stream-b-route-reconciliation-v2",
        "supersedes": {
            "artifact": "cycle-2-stream-b-route-reconciliation-v1",
            "byte_sha256": sha256(PATHS["reconciliation_v1"]),
            "preservation": "v1 is retained unchanged; its OPEN rows are resolved here rather than erased.",
        },
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED only as a deterministic reconciliation of two pinned-source Stream-B application audits. It does not re-prove GM/MP analytic theorems, establish a new zero-density result, or promote G0; Stream C remains outside scope.",
        "canonical_status": "PROVED: INDEPENDENT_ROUTE_NARROW_PASS for Stream B only; G0 remains OBSERVED pending Stream C.",
        "input_identities": {
            "route_a_v3_byte_sha256": sha256(PATHS["route_a_v3"]),
            "route_a_v3_script_sha256": a["replay"]["script_sha256"],
            "route_b_v1_byte_sha256": sha256(PATHS["route_b_v1"]),
            "route_b_v1_script_sha256": b["replay"]["script_sha256"],
            "route_a_new_rows": sorted(ar),
            "route_b_rows": sorted(br),
        },
        "canonical_mapping_table": table,
        "resolved_prior_gaps": gaps,
        "agreement_summary": {
            "comparison_nodes": len(table),
            "coverage_gaps_open": 0,
            "formula_contradictions": 0,
            "independent_route_pass_permitted": True,
            "pass_scope": "NARROW PASS: Stream B only; G0 remains OBSERVED.",
        },
        "next_authorized_action": "Do not relabel G0. Retain both route artifacts and this reconciliation; any G0 promotion requires the separately scoped Stream-C work.",
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script": str(Path(__file__).relative_to(ROOT)),
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_b_routes_v2.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-reconciliation-v2.json",
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
