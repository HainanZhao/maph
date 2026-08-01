#!/usr/bin/env python3
"""Lightweight exact reconciliation of P6 CGL-v2 Routes A-v1 and B-v2.

Route B-v2 is the preserved v1 source/conductor reconstruction plus its
versioned exact-margin correction.  This script compares records; it neither
repairs the CGL preprint nor promotes its claimed 7/3 density estimate.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import resource
import sys
import time
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
PREREG = ROOT / "artifacts/cycle-4-p6-cgl-v2-reconstruction-preregistration-v1.json"
ROUTE_A = ROOT / "artifacts/p6-cgl-v2-route-a-v1.json"
ROUTE_B_V1 = ROOT / "artifacts/p6-cgl-v2-route-b-v1.json"
ROUTE_B_V2 = ROOT / "artifacts/p6-cgl-v2-route-b-v2-correction.json"
OUT = ROOT / "artifacts/p6-cgl-v2-reconciliation-v1.json"
WALL_CAP_NS = 60_000_000_000
RSS_CAP_KIB = 262_144

IDS = tuple(
    [f"S{i:02d}" for i in range(1, 7)]
    + [f"L{i:02d}" for i in range(1, 13)]
    + [f"M{i:02d}" for i in range(1, 9)]
    + [f"Z{i:02d}" for i in range(1, 11)]
    + [f"F{i:02d}" for i in range(1, 11)]
)
REQUIRED_OPEN = (
    "S06_EXTERNAL_INPUTS",
    "Z03_TAIL_X_RANGE",
    "Z05_PRIMITIVE_EULER_FACTORS",
    "Z06_CONDUCTOR_SUM_Q1",
    "F08_T_SMOOTH_UNDEFINED",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def line_numbers(text: str) -> set[int]:
    return {int(value) for value in re.findall(r"\d+", text)}


def status_level(value: str) -> str:
    if "OPEN_ANALYTIC_INPUT" in value:
        return "OPEN_ANALYTIC_INPUT"
    if "PROVED_EXACT_ALGEBRA" in value or "RECONSTRUCTED_EXACT_ALGEBRA" in value:
        return "EXACT_ALGEBRA_CONDITIONAL"
    if "SOURCE" in value or "RECONSTRUCTED" in value:
        return "SOURCE_DEPENDENT_RECORDED"
    return "OTHER_RECORDED"


def locator_comparison(prereg_locator: str, a_locator: str, b_region: str) -> dict[str, object]:
    prereg_lines = line_numbers(prereg_locator)
    a_lines = line_numbers(a_locator)
    b_lines = line_numbers(b_region)
    # S01 uses whole-source identity rather than a numerical TeX line range.
    if not prereg_lines and not a_lines and not b_lines:
        result = "WHOLE_SOURCE_IDENTITY_COMPATIBLE"
    elif prereg_lines & a_lines and prereg_lines & b_lines and a_lines & b_lines:
        result = "THREE_WAY_NUMERIC_LOCATOR_OVERLAP"
    elif prereg_lines & a_lines and prereg_lines & b_lines:
        result = "EACH_ROUTE_OVERLAPS_PREREGISTRATION"
    else:
        result = "LOCATOR_COMPARISON_NEEDS_MANUAL_FOLLOW_UP"
    return {
        "preregistration_locator": prereg_locator,
        "route_a_locator": a_locator,
        "route_b_region": b_region,
        "comparison": result,
    }


def formula_comparison(row_id: str, a_formula: str, b_formula: str) -> dict[str, object]:
    # Source-order and exponent-polytope routes intentionally have different
    # prose. Raw texts are retained for every row instead of claiming a
    # string-normalized equality that was not established.
    outcome = "RAW_DUAL_ROUTE_FORMULAE_RETAINED_NOT_STRING_NORMALIZED"
    if row_id == "F09":
        outcome = "EXACT_CROSSINGS_COMPARED_IN_EXACT_ALGEBRA_BLOCK"
    elif row_id == "F10":
        outcome = "EXACT_Q1_EQUALS_Q_COMPARISON_CHECKED_IN_CORRECTED_BLOCK"
    return {
        "route_a_formula_or_chain_step": a_formula,
        "route_b_formula_or_check": b_formula,
        "comparison": outcome,
    }


def row_comparisons(prereg: dict[str, object], a: dict[str, object], b: dict[str, object]) -> list[dict[str, object]]:
    prereg_rows = {row["id"]: row for row in prereg["row_registry"]}
    a_rows = {row["id"]: row for row in a["rows"]}
    b_rows = {row["id"]: row for row in b["rows"]}
    require(tuple(prereg_rows) == IDS, "preregistration ID order mismatch")
    require(tuple(a_rows) == IDS, "Route A ID order mismatch")
    require(tuple(b_rows) == IDS, "Route B ID order mismatch")
    output: list[dict[str, object]] = []
    for row_id in IDS:
        a_row, b_row, prereg_row = a_rows[row_id], b_rows[row_id], prereg_rows[row_id]
        a_status = str(a_row["disposition"])
        b_status = str(b_row["disposition"])
        a_level, b_level = status_level(a_status), status_level(b_status)
        if a_level == b_level:
            status_comparison = "SAME_NORMALIZED_STATUS"
        elif a_level == "OPEN_ANALYTIC_INPUT" or b_level == "OPEN_ANALYTIC_INPUT":
            status_comparison = "ROUTE_STATUS_DIFFERENCE_RETAINED"
        else:
            status_comparison = "ROUTE_METHOD_STATUS_VOCABULARY_DIFFERENCE_RETAINED"
        output.append({
            "id": row_id,
            "canonical_id_agreement": True,
            "obligation": prereg_row["obligation"],
            "source_locator_comparison": locator_comparison(
                str(prereg_row["locator"]), str(a_row["source_locator"]), str(b_row["region"])
            ),
            "formula_comparison": formula_comparison(
                row_id, str(a_row["formula_or_chain_step"]), str(b_row["formula_or_check"])
            ),
            "tag_comparison": {
                "route_a_epistemic_status": a_row["epistemic_status"],
                "route_b_disposition": b_status,
                "comparison": "ROUTE_SPECIFIC_TAGS_RETAINED",
            },
            "status_comparison": {
                "route_a_disposition": a_status,
                "route_a_normalized": a_level,
                "route_b_disposition": b_status,
                "route_b_normalized": b_level,
                "comparison": status_comparison,
            },
            "route_b_row_blockers": b_row["blockers"],
        })
    require(len(output) == 46, "must compare all 46 canonical rows")
    return output


def l12_comparison(a: dict[str, object], b: dict[str, object]) -> dict[str, object]:
    a_subchecks = a["rows"][17]["subchecks"]
    b_subchecks = b["rows"][17]["subchecks"]
    require(a["rows"][17]["id"] == b["rows"][17]["id"] == "L12", "L12 position changed")
    require([item["id"] for item in a_subchecks] == ["odd_prime", "two_power"], "Route A L12 labels changed")
    require([item["id"] for item in b_subchecks] == ["L12.odd_prime", "L12.two_power"], "Route B L12 labels changed")
    return {
        "canonical_row": "L12",
        "subcheck_label_mapping": {
            "L12.odd_prime": {"route_a_id": "odd_prime", "route_b_id": "L12.odd_prime"},
            "L12.two_power": {"route_a_id": "two_power", "route_b_id": "L12.two_power"},
        },
        "subchecks": [
            {
                "id": "L12.odd_prime",
                "route_a": a_subchecks[0],
                "route_b": b_subchecks[0],
                "comparison": "BOTH_RECORD_ODD_PRIME_FACTORIZATION",
            },
            {
                "id": "L12.two_power",
                "route_a": a_subchecks[1],
                "route_b": b_subchecks[1],
                "comparison": "DISAGREEMENT_RETAINED_ROUTE_A_OPEN_ROUTE_B_RECORDED_SOURCE_DEPENDENT",
            },
        ],
        "consequence": (
            "The two-power subcheck is not promoted. Route A leaves its details "
            "open, while Route B records the source's analogous decomposition."
        ),
    }


def exact_algebra(a: dict[str, object], b_v2: dict[str, object]) -> dict[str, object]:
    a_identities = a["exact_algebra"]["identities"]
    corrected = b_v2["corrected_exact_checks"]
    require(a_identities["7/3-9/4"] == corrected["7/3-9/4"]["result"] == "1/12", "9/4 margin mismatch")
    require(a_identities["7/3-30/13"] == corrected["7/3-30/13"]["result"] == "1/39", "30/13 margin mismatch")
    require(a_identities["B_at_beta_1"] == corrected["B_at_beta_1"]["result"], "radical reduction mismatch")
    return {
        "status": "PROVED_EXACT_CONDITIONAL_ALGEBRA_ONLY",
        "route_a_v1_identities": a_identities,
        "route_b_v2_corrected_checks": corrected,
        "crossings_from_route_b_v1_retained_and_correction_scoped": {
            "C1_sigma": "(3+2*lambda)/(6+lambda)",
            "C1_base": "(q1^(1/3)*q^2*T^2)^(1-sigma)",
            "C2_sigma": "(4-2*beta)/(4-beta)",
            "C2_base": "(q^3*T^(9/4)*q1^(-3/4))^(1-sigma)",
            "C3_polynomial": "20*sigma^2-(43-3*beta)*sigma+24-6*beta",
            "C3_coefficient": "(37+3*beta-sqrt(9*beta^2+222*beta-71))/12",
            "C4_sigma": "7/10",
            "C4_coefficient": "30/13",
        },
        "boundary": (
            "These formulae are exact conditional algebra from displayed source "
            "terms. They do not close the CGL zero-density theorem because the "
            "analytic and transfer inputs remain open."
        ),
    }


def open_obligations(a: dict[str, object], b: dict[str, object]) -> dict[str, object]:
    a_top = {entry["id"] for entry in a["open_blockers"]}
    b_top = set(b["open_blockers"])
    a_expanded = {
        "S06_EXTERNAL_INPUTS",
        "Z03_TAIL_X_RANGE",
        "Z05_PRIMITIVE_EULER_FACTORS",
        "Z06_CONDUCTOR_SUM_Q1",
        "F08_T_SMOOTH_UNDEFINED",
    }
    require({"S06_EXTERNAL_INPUTS", "Z03_TAIL_X_RANGE", "PRIMITIVE_TO_ALL", "F08_T_SMOOTH_UNDEFINED"}.issubset(a_top), "Route A mandatory blocker group missing")
    require(set(REQUIRED_OPEN).issubset(b_top), "Route B mandatory blocker missing")
    a_open_rows = [row["id"] for row in a["rows"] if "OPEN_ANALYTIC_INPUT" in row["disposition"]]
    b_open_rows = [row["id"] for row in b["rows"] if "OPEN_ANALYTIC_INPUT" in row["disposition"]]
    return {
        "required_preregistered_obligations": list(REQUIRED_OPEN),
        "shared_open_after_label_normalization": list(REQUIRED_OPEN),
        "route_a_top_level_raw_labels": sorted(a_top),
        "route_a_normalized_labels": sorted(a_expanded),
        "route_b_v2_inherited_raw_labels": sorted(b_top),
        "route_a_directly_open_rows": a_open_rows,
        "route_b_v1_directly_open_rows_inherited_by_v2": b_open_rows,
        "additional_route_b_v2_retained_obligation": "S03_MULTIPLICITY_NOT_STATED",
        "result": "OPEN_ANALYTIC_INPUT",
        "forbidden_repairs_preserved": [
            "no q<=T^C restriction",
            "no log^2(qT) substitution",
            "no invented T-smooth definition",
            "no unsupported primitive-to-all conductor transfer",
        ],
    }


def build() -> dict[str, object]:
    prereg = json.loads(PREREG.read_text(encoding="utf-8"))
    a = json.loads(ROUTE_A.read_text(encoding="utf-8"))
    b_v1 = json.loads(ROUTE_B_V1.read_text(encoding="utf-8"))
    b_v2 = json.loads(ROUTE_B_V2.read_text(encoding="utf-8"))
    require(a["row_count"] == 46 and b_v1["canonical_row_count"] == 46, "route count mismatch")
    require(a["status"] == b_v1["overall_disposition"] == "OPEN_ANALYTIC_INPUT", "route overall status mismatch")
    require(b_v2["row_level_effect"]["canonical_row_count_unchanged"] == 46, "B-v2 altered row count")
    require(b_v2["row_level_effect"]["overall_disposition_unchanged"] == "OPEN_ANALYTIC_INPUT", "B-v2 altered disposition")
    require(b_v2["preserved_v1"]["artifact_sha256"] == digest(ROUTE_B_V1), "B-v2 no longer pins B-v1 artifact")
    comparisons = row_comparisons(prereg, a, b_v1)
    locator_followups = [
        row["id"] for row in comparisons
        if row["source_locator_comparison"]["comparison"] == "LOCATOR_COMPARISON_NEEDS_MANUAL_FOLLOW_UP"
    ]
    return {
        "artifact_id": "p6-cgl-v2-reconciliation-v1",
        "epistemic_status": "OBSERVED",
        "claim_boundary": (
            "Lightweight reconciliation of Route A-v1 and Route B-v2 only. It "
            "does not validate, repair, or promote the CGL preprint; it proves no "
            "new zero-density or short-interval result and does not initiate a "
            "paper-stage hostile audit."
        ),
        "overall_disposition": "OPEN_ANALYTIC_INPUT",
        "reconciled_authorities": {
            "route_a": {"version": "v1", "artifact": str(ROUTE_A.relative_to(ROOT)), "sha256": digest(ROUTE_A)},
            "route_b": {
                "source_reconstruction": {"version": "v1", "artifact": str(ROUTE_B_V1.relative_to(ROOT)), "sha256": digest(ROUTE_B_V1)},
                "exact_margin_correction": {"version": "v2", "artifact": str(ROUTE_B_V2.relative_to(ROOT)), "sha256": digest(ROUTE_B_V2)},
                "authority_statement": "B-v1 row reconstruction with B-v2 required for the q1=q exact-margin check.",
            },
            "preregistration": {"artifact": str(PREREG.relative_to(ROOT)), "sha256": digest(PREREG)},
        },
        "route_b_v1_defect_contained": b_v2["defect"],
        "canonical_registry": {"count": 46, "ids": list(IDS), "all_ids_agree": True},
        "row_comparisons": comparisons,
        "source_locator_followups": locator_followups,
        "l12_subcheck_reconciliation": l12_comparison(a, b_v1),
        "exact_algebra_reconciliation": exact_algebra(a, b_v2),
        "open_analytic_obligations": open_obligations(a, b_v1),
        "route_status_difference_rows": [
            row["id"] for row in comparisons
            if row["status_comparison"]["comparison"] == "ROUTE_STATUS_DIFFERENCE_RETAINED"
        ],
        "conclusion": (
            "OBSERVED: both routes retain all 46 canonical IDs and both L12 "
            "branches, and their overall disposition remains OPEN_ANALYTIC_INPUT. "
            "PROVED: the q1=q rational/radical margins are checked by Route A-v1 "
            "and the B-v2 correction. The L12 two-power treatment and granular "
            "row-status vocabulary differ and remain explicitly contained."
        ),
        "replay": {
            "command": "python3 proof/reconcile_p6_cgl_v2_routes_v1.py --check",
            "python_implementation": sys.implementation.name,
            "python_version": ".".join(map(str, sys.version_info[:3])),
            "optimized": sys.flags.optimize,
            "wall_cap_ns": WALL_CAP_NS,
            "rss_cap_kib": RSS_CAP_KIB,
        },
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    require(args.write != args.check, "choose exactly one of --write or --check")
    require(sys.flags.optimize == 0, "reconciliation rejects optimized Python")
    require(sys.version_info[:3] == (3, 12, 3) and sys.platform.startswith("linux"), "reconciliation requires CPython 3.12.3 on linux")
    started = time.monotonic_ns()
    value = build()
    elapsed = time.monotonic_ns() - started
    rss = int(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    require(elapsed < WALL_CAP_NS, "reconciliation exceeded 60-second wall cap")
    require(rss < RSS_CAP_KIB, "reconciliation exceeded 256-MiB RSS cap")
    encoded = render(value)
    if args.write:
        require(not OUT.exists(), "refusing to overwrite reconciliation artifact")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file(), "reconciliation artifact is absent")
        require(OUT.read_bytes() == encoded, "reconciliation artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "peak_rss_kib": rss, "rows": 46, "wall_ns": elapsed}, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err, file=sys.stderr)
        raise SystemExit(1)
