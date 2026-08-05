#!/usr/bin/env python3
"""Verify Cycle 162's immutable evidence and accelerated-plan boundary."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

EXPECTED_LEGACY_HASHES = {
    "docs/sic-stark-cycle157.md": "72149e87781915319f6e82ea9218e92ab748714666ba8d37e67334dd572c977e",
    "docs/sic-stark-cycle161.md": "6b6e1150fd4863970f118b74c470d0cba9bc3a65739d95ee93e6733d3c0ed07d",
    "certificates/dimension-six-cycle157-fourier-normalization-audit.json": "f5dd1d19e4fdbcdf74c0744835fe68ed47721f7577b408aba12e910c8b693fdb",
    "certificates/dimension-seven-cycle161-discriminant-eight-closure.json": "49fdbeaeecba0802e0b54cbb2e404cfb2c6fac2112d814de700dd6e9a12129cf",
}
EFFECTIVE_STARK_CONTEXT = "docs/effective-stark-sweep-context-v1.md"
EXPECTED_EFFECTIVE_STARK_CONTEXT_HASH = (
    "1963372c6e82b068844cc9469ddea2e39647d0b7e05e5c9aa4744bed814b7853"
)
MUTABLE_WORKFLOW_PATHS = {
    "PROGRAM.md",
    "STATUS.md",
    "research-records.json",
    "research_index_legacy_exceptions.json",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict[str, object]:
    for relative, expected in EXPECTED_LEGACY_HASHES.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"legacy evidence hash mismatch: {relative}")

    if sha256(ROOT / EFFECTIVE_STARK_CONTEXT) != EXPECTED_EFFECTIVE_STARK_CONTEXT_HASH:
        raise RuntimeError("Effective Stark Sweep dependency context hash mismatch")
    effective_stark_context = (ROOT / EFFECTIVE_STARK_CONTEXT).read_text()
    for phrase in (
        "10.5281/zenodo.21713178",
        "RQ-000692",
        "P_SIC(X)=P_census(-X)",
        "theorem-hypothesis boundary",
    ):
        if phrase not in effective_stark_context:
            raise RuntimeError(f"Effective Stark Sweep context missing: {phrase}")

    cycle157 = json.loads(
        (ROOT / "certificates/dimension-six-cycle157-fourier-normalization-audit.json").read_text()
    )
    gates = cycle157["normalization_gates"]
    required_missing = {
        "identification_with_AFK_cocycle_values",
        "logarithm_branch_and_boundary_subtraction",
        "map_from_36_additive_coefficients_to_3_ray_classes",
        "map_from_additive_values_to_logarithms_P_j",
    }
    if {key for key in required_missing if gates[key] == "MISSING"} != required_missing:
        raise RuntimeError("Cycle-157 interface boundary changed")

    preregistration = (
        ROOT / "docs/cycle-162-workflow-migration-preregistration-v1.md"
    ).read_text()
    if preregistration.count("research-freeze-v1") != 1:
        raise RuntimeError("Cycle 162 must have exactly one embedded freeze")
    for phrase in (
        "operational coefficient-to-cocycle/ray-log interface",
        "100",
        "new Zenodo version",
        "RQ-000692",
    ):
        if phrase not in preregistration:
            raise RuntimeError(f"accelerated preregistration missing: {phrase}")

    document = (ROOT / "docs/cycle-162-workflow-migration-v1.md").read_text()
    for phrase in (
        "interface-first Phase 0",
        "CONDITIONAL_0_OF_100",
        "10.5281/zenodo.21682631",
        "10.5281/zenodo.21713178",
        "PHASE0_PARALLEL_DESIGN",
    ):
        if phrase not in document:
            raise RuntimeError(f"accelerated decision document missing: {phrase}")

    return {
        "legacy_hashes": EXPECTED_LEGACY_HASHES,
        "legacy_noncycle_artifacts": sorted(
            path.name for path in (ROOT / "artifacts").glob("tcc-*.json")
        ),
        "mutable_workflow_paths_excluded": sorted(MUTABLE_WORKFLOW_PATHS),
        "effective_stark_dependency": {
            "context_path": EFFECTIVE_STARK_CONTEXT,
            "context_sha256": EXPECTED_EFFECTIVE_STARK_CONTEXT_HASH,
            "results_doi": "10.5281/zenodo.21713178",
            "shared_object": "RQ-000692",
            "boundary": "wild_3_sextic_hypothesis_failure_not_tcc_no_go",
        },
        "phase0_order": "interface_then_fusion_continuity",
        "q4_campaign_cap": 100,
        "status": "ACCELERATED_WORKFLOW_ATTACHMENT_VERIFIED",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
