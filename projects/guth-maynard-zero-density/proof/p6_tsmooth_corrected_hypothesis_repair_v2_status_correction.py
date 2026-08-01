#!/usr/bin/env python3
"""Seal canonical epistemic statuses for the immutable P6 F08 v1 repair."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
V1 = ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v1.json"
V1_DOC = ROOT / "docs/p6-tsmooth-corrected-hypothesis-repair-v1.md"
DOC = ROOT / "docs/p6-tsmooth-corrected-hypothesis-repair-v2-status-correction.md"
OUT = ROOT / "artifacts/p6-tsmooth-corrected-hypothesis-repair-v2-status-correction.json"
V1_HASH = "5097609783b4e076b268255445e94caeb08bc23f93ad2540703c43e1401ca8af"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    require(digest(V1) == V1_HASH, "immutable F08 v1 artifact changed")
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    require(v1["epistemic_status"] == "PROVED_CONDITIONAL", "recorded v1 aggregate tag changed")
    require(v1["corrected_theorem"]["divisor_chain_lemma"]["epistemic_status"] == "PROVED", "v1 divisor-chain status changed")
    require("`PROVED_CONDITIONAL`" in V1_DOC.read_text(encoding="utf-8"), "recorded v1 document tag missing")
    return {
        "artifact_id": "p6-tsmooth-corrected-hypothesis-repair-v2-status-correction",
        "epistemic_status": "OBSERVED",
        "correction": "Replace v1 noncanonical aggregate tags by PROVED deductions conditional on their explicit hypothesis lists.",
        "corrected_claims": {
            "divisor_and_subdivision": {
                "epistemic_status": "PROVED",
                "conditional_on": ["AMENDED_T_SMOOTH_HYPOTHESIS", "DISPLAYED_PRIMITIVE_LARGE_VALUE_SUBDIVISION_INEQUALITY"],
            },
            "smooth_density_envelope": {
                "epistemic_status": "PROVED",
                "conditional_on": ["PRIMITIVE_LARGE_VALUE_INPUT", "QT_DETECTOR_AND_NAMED_EXTERNAL_MULTIPLICITY_INPUTS", "COMPARISON_ENVELOPES_IN_EXACT_RANGES", "PRIMITIVE_TO_ALL_TRANSFER"],
                "not_promoted": "No unconditional density theorem and no validation of CGL-v2's undefined F08 wording.",
            },
        },
        "immutable_v1": {"path": str(V1.relative_to(ROOT)), "sha256": V1_HASH},
        "immutable_v1_document": {"path": str(V1_DOC.relative_to(ROOT)), "sha256": digest(V1_DOC)},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/p6_tsmooth_corrected_hypothesis_repair_v2_status_correction.py --check",
    }


def render(value: dict[str, object]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def main() -> int:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    encoded = render(payload())
    if args.write:
        require(not OUT.exists(), "refusing to overwrite F08 status correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "F08 status-correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
