#!/usr/bin/env python3
"""Adjudicate only the zero-retained branch of the frozen G1 decision."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import platform
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
INPUTS = {
    "preregistration_document": (ROOT / "docs/cycle-3-g1-atlas-preregistration-v1.md", "0510bb5ced5b3a5fd4377dea57216b226b58b49158ad6ddb6185775c967bfd72"),
    "preregistration_artifact": (ROOT / "artifacts/cycle-3-g1-atlas-preregistration-v1.json", "227ec1c66b2e109653354b6c3245b4e809fe52692c01514ac10064c23db2b6f8"),
    "exact_atlas_v2": (ROOT / "artifacts/cycle-3-g1-exact-structural-atlas-v2.json", "fd66d17664ca921795617c6bfca76c3be49246ea9351644848a2aadf9e680b08"),
    "envelope_sensitivity_v1": (ROOT / "artifacts/g1-envelope-sensitivity-reconciliation-v1.json", "850b825698722d628340b762867c98774dae53443aecde581138c6830993b60e"),
    "energy_no_retention_v3": (ROOT / "artifacts/g1-energy-no-retention-audit-v3.json", "bf050f6186ab2bab247cfb18bc628168149354cc64da8773879e95e56a991fc6"),
    "empirical_reconciliation_v1": (ROOT / "artifacts/cycle-3-g1-atlas-empirical-reconciliation-v1.json", "4e3adc2885a9c441d0006633355b8be87d39599bc93ca68d1270475b27111a88"),
    "literature_audit_v1": (ROOT / "artifacts/g1-current-literature-audit-v1.json", "49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be"),
    "literature_correction_v2": (ROOT / "artifacts/g1-current-literature-audit-v2-correction.json", "f56529c5919971385cc583b51255636022a5b33fb0cfd4857a587f1d3e099076"),
    "superseded_v1_adjudicator": (ROOT / "proof/adjudicate_g1_route_selection_v1.py", "5879cadd61bf23015cbc27ed00d049f3a8792dc75dd09e835dd7321aa307d355"),
    "superseded_v1_artifact": (ROOT / "artifacts/cycle-3-g1-route-decision-v1.json", "a54115024a6dd1eae5cff7653b1488d9cde05d8063f4769e27eeda7aec702d6b"),
    "v1_hostile_audit_script": (ROOT / "proof/audit_g1_route_decision_v1_hostile.py", "bc35a83080b1d1a4d584b7a8665dd846c3c7cb6fe697a8b37f5b2f19eb197e2d"),
    "v1_hostile_audit_artifact": (ROOT / "artifacts/g1-route-decision-v1-hostile-audit-v1.json", "98e2019f25ea357221826195c3497984b6213fe29545f05d2135d6b5b706040b"),
}
EXPECTED_PYTHON = "3.12.3"
RULE_FRAGMENTS = (
    "choose P2A only if retained rows isolate a trace feature absent from the",
    "choose P2B only if the active obstruction is consistently energy/affine",
    "choose P2C only if the exact transfer map identifies a named decomposition",
    "choose a combination only with separate labeled evidence for each route",
    "otherwise record `NO_SELECTION` and every rejected route",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def check_runtime() -> dict[str, Any]:
    record = {
        "implementation": platform.python_implementation(),
        "python": platform.python_version(),
        "optimization_level": sys.flags.optimize,
    }
    require(
        record == {"implementation": "CPython", "python": EXPECTED_PYTHON, "optimization_level": 0},
        "G1 route adjudication v2 requires non-optimized CPython 3.12.3",
    )
    return record


def adjudicate() -> dict[str, Any]:
    runtime = check_runtime()
    adjudicator = {
        "path": str(SELF.relative_to(ROOT)),
        "sha256": sha256(SELF),
    }
    frozen_hashes: dict[str, dict[str, str]] = {}
    for label, (path, expected_hash) in INPUTS.items():
        require(path.is_file(), f"missing frozen input: {path}")
        actual_hash = sha256(path)
        require(actual_hash == expected_hash, f"frozen input hash mismatch: {label}")
        frozen_hashes[label] = {"path": str(path.relative_to(ROOT)), "sha256": actual_hash}

    prereg_text = INPUTS["preregistration_document"][0].read_text(encoding="utf-8")
    for fragment in RULE_FRAGMENTS:
        require(fragment in prereg_text, f"missing frozen route-selection clause: {fragment}")

    hostile = load_json(INPUTS["v1_hostile_audit_artifact"][0])
    require(hostile.get("status") == "FAIL_ROUTE_PREDICATE_COMPLETENESS", "v1 hostile-audit status mismatch")
    require(hostile.get("findings", {}).get("route_predicates", {}).get("status") == "FAIL", "v1 predicate defect is not sealed")
    require(hostile.get("findings", {}).get("adjudicator_identity", {}).get("status") == "FAIL", "v1 identity defect is not sealed")

    exact = load_json(INPUTS["exact_atlas_v2"][0])
    envelope = load_json(INPUTS["envelope_sensitivity_v1"][0])
    energy = load_json(INPUTS["energy_no_retention_v3"][0])
    empirical = load_json(INPUTS["empirical_reconciliation_v1"][0])
    require(exact.get("epistemic_status") == "PROVED", "exact-atlas status mismatch")
    require(exact.get("counts", {}).get("local_total") == 7744, "exact local-row count mismatch")
    require(exact.get("counts", {}).get("transfer_total") == 560, "exact transfer-row count mismatch")
    transfer = exact.get("mandatory_anchors", {}).get("transfer", {})
    require(transfer.get("B_minus_source_term", {}).get("LV3") == "0/1", "critical LV3 residual mismatch")
    require(envelope.get("contained_no_effect", {}).get("epistemic_status") == "PROVED", "envelope no-effect status mismatch")
    require(energy.get("epistemic_status") == "CERTIFIED_NUMERICAL", "energy certificate status mismatch")
    require(energy.get("summary", {}).get("scheduled_rows") == 588, "energy schedule mismatch")
    require(energy.get("summary", {}).get("feasible_rows") == 434, "energy feasible-row mismatch")
    require(energy.get("summary", {}).get("energy_retention_eligible_rows") == 0, "energy-eligible row survived")
    require(empirical.get("status") == "EMPIRICALLY_RECONCILED", "empirical reconciliation status mismatch")
    agreement = empirical.get("agreement", {})
    summary = empirical.get("screen_outcome_summary", {})
    require(agreement.get("screen_rows") == 588, "empirical screen coverage mismatch")
    require(summary.get("completed_rows") == 429 and summary.get("failed_rows") == 159, "empirical outcome counts mismatch")
    require(summary.get("failure_code_counts") == {"INFEASIBLE_CARDINALITY": 154, "NONPOSITIVE_VALUE_RATIO": 5}, "empirical failure ledger mismatch")
    require(summary.get("retained_row_ids") == [], "retained-row list is not empty")

    retained_rows = agreement.get("retained_rows")
    validation_rows = agreement.get("validation_rows")
    require(
        retained_rows == 0 and validation_rows == 0,
        "positive feature adjudication required: v2 supports only zero retained and zero validation rows",
    )

    # This adjudicator intentionally has no affirmative route predicates.
    # A future positive decision requires a separately sealed labeled-evidence schema.
    routes = {
        "P2A": {"selected": False, "status": "NOT_SELECTED", "reason": "The frozen screen retained no row, so no trace feature absent from the cubic terms was evidenced."},
        "P2B": {"selected": False, "status": "NOT_SELECTED", "reason": "The frozen screen retained no row establishing a consistent energy/affine obstruction; finite-scale energy non-retention is not asymptotic classification."},
        "P2C": {"selected": False, "status": "NOT_SELECTED", "reason": "LV3 is the exact zero-residual transfer term, but the frozen screen supplies no retained local candidate to propagate."},
        "COMBINATION": {"selected": False, "status": "NOT_SELECTED", "reason": "No constituent route has separate affirmative labeled evidence."},
    }

    return {
        "artifact_id": "cycle-3-g1-route-decision-v2",
        "epistemic_status": "OBSERVED",
        "claim_boundary": "No-selection-only bounded program decision for the sealed zero-retained G1 branch. It is not a theorem, asymptotic obstruction, saturation result, density improvement, or refutation of P2A/P2B/P2C.",
        "decision": "NO_SELECTION",
        "gate_status": "G1_CLOSED_NO_SELECTION",
        "adjudicator": adjudicator,
        "frozen_hashes": frozen_hashes,
        "runtime": runtime,
        "correction": {
            "supersedes_for_promotion": "cycle-3-g1-route-decision-v1",
            "contained_defects": ["incomplete affirmative route predicates", "missing adjudicator identity"],
            "positive_case_policy": "FAIL_CLOSED_REQUIRES_SEPARATELY_SEALED_LABELED_EVIDENCE",
        },
        "evidence_summary": {
            "exact_local_rows": 7744,
            "exact_transfer_rows": 560,
            "screen_rows": 588,
            "completed_rows": 429,
            "failed_rows": 159,
            "failure_code_counts": summary["failure_code_counts"],
            "retained_rows": 0,
            "validation_rows": 0,
            "finite_energy_feasible_rows": 434,
            "finite_energy_retention_eligible_rows": 0,
            "critical_zero_residual_term": "LV3",
        },
        "routes": routes,
        "preservation": {
            "failed_rows_retained": True,
            "rejected_means_not_selected_not_refuted": True,
            "retuning_permitted": False,
            "v1_preserved_as_failed_audit_path": True,
        },
        "next_action_boundary": "A new PLAN-authorized preregistration is required before any P2 theorem search or replacement screen; this decision itself authorizes none.",
        "falsifier": "Any frozen hash/count/rule mismatch or any retained/validation row invalidates this no-selection-only decision; positive route evidence requires a different sealed adjudicator.",
    }


def render(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args()
    result = adjudicate()
    if args.write is not None:
        require(not args.write.exists(), "refusing to overwrite G1 route-decision v2 artifact")
        args.write.parent.mkdir(parents=True, exist_ok=True)
        with args.write.open("xb") as stream:
            stream.write(render(result))
    else:
        require(args.check.is_file(), "route-decision v2 artifact is absent")
        recorded = load_json(args.check)
        require(recorded.get("adjudicator") == result["adjudicator"], "recorded adjudicator identity mismatch")
        require(args.check.read_bytes() == render(result), "route-decision v2 artifact mismatch")
    print(json.dumps({"decision": result["decision"], "gate_status": result["gate_status"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
