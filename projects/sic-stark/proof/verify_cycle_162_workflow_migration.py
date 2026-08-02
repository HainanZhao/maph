#!/usr/bin/env python3
"""Verify the Cycle-162 workflow boundary without changing any record."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REPOSITORY_ROOT = ROOT.parents[1]

EXPECTED_LEGACY_HASHES = {
    "docs/sic-stark-cycle157.md": "72149e87781915319f6e82ea9218e92ab748714666ba8d37e67334dd572c977e",
    "docs/sic-stark-cycle161.md": "6b6e1150fd4863970f118b74c470d0cba9bc3a65739d95ee93e6733d3c0ed07d",
    "certificates/dimension-six-cycle157-fourier-normalization-audit.json": "f5dd1d19e4fdbcdf74c0744835fe68ed47721f7577b408aba12e910c8b693fdb",
    "certificates/dimension-seven-cycle161-discriminant-eight-closure.json": "49fdbeaeecba0802e0b54cbb2e404cfb2c6fac2112d814de700dd6e9a12129cf",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify() -> dict[str, object]:
    for relative, expected in EXPECTED_LEGACY_HASHES.items():
        actual = sha256(ROOT / relative)
        if actual != expected:
            raise RuntimeError(f"legacy evidence hash mismatch: {relative}")
    profile = json.loads((ROOT / "research-records.json").read_text())
    legacy = json.loads((ROOT / "research_index_legacy_exceptions.json").read_text())
    handoff = profile["cold_start_handoff"]
    if profile["artifact_glob"] != "artifacts/cycle-*.json":
        raise RuntimeError("profile must exclude legacy non-cycle artifacts")
    if legacy["untagged_artifacts"] or legacy["evidence_exceptions"]:
        raise RuntimeError("Cycle 162 expects an explicit empty legacy exception list")
    if handoff["project_outcome"]["epistemic_status"] != "PROVED":
        raise RuntimeError("project outcome tag changed")
    if handoff["progress_criterion"]["epistemic_status"] != "CONJECTURED":
        raise RuntimeError("interface criterion must remain conjectural")
    gate_text = handoff["why_active_gate_matters"]["statement"]
    if "36 additive spectral coefficients" not in gate_text or "ray-class logarithms" not in gate_text:
        raise RuntimeError("dimension-six interface gate is incomplete")
    deferred = handoff["deferred_work"]
    if "Paper III" not in deferred or "boundary-packet numerics" not in deferred:
        raise RuntimeError("deferred-work boundary is incomplete")
    return {
        "legacy_hashes": EXPECTED_LEGACY_HASHES,
        "legacy_noncycle_artifacts": sorted(path.name for path in (ROOT / "artifacts").glob("tcc-*.json")),
        "profile_artifact_glob": profile["artifact_glob"],
        "status": "WORKFLOW_MIGRATION_VERIFIED",
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
