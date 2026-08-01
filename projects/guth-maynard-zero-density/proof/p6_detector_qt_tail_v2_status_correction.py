#!/usr/bin/env python3
"""Correct the noncanonical epistemic tag in the immutable P6 tail v1."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
V1 = ROOT / "artifacts/p6-detector-qt-tail-v1.json"
DOC = ROOT / "docs/p6-detector-qt-tail-v2-status-correction.md"
OUT = ROOT / "artifacts/p6-detector-qt-tail-v2-status-correction.json"
V1_HASH = "c672dc559dbbd81b2b30f1a0c8e37354517e43af8da389b89a055504778a118d"
DOC_HASH = "c67c39b46782def0d45374bb3e91dd9cebfc52957e74477d8beffec1ad499d61"


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "status correction rejects optimized Python")
    require(digest(V1) == V1_HASH, "immutable tail-v1 artifact changed")
    require(digest(DOC) == DOC_HASH, "status-correction document changed")
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    require(v1["epistemic_status"] == "PROVED_CONDITIONAL", "v1 no longer has the recorded noncanonical tag")
    inputs = v1["lemma"]["conditional_inputs"]
    require(set(("L_POLY_A", "FOURTH_MOMENT_H", "LOW_HEIGHT_MULTIPLICITY_COUNT")).issubset(inputs), "v1 conditional inputs changed")
    return {
        "artifact_id": "p6-detector-qt-tail-v2-status-correction",
        "epistemic_status": "OBSERVED",
        "correction": "Replace v1's noncanonical aggregate tag PROVED_CONDITIONAL by PROVED deductions conditional on explicitly CONJECTURED/external analytic premises.",
        "corrected_claim": {
            "epistemic_status": "PROVED",
            "conditional_on": ["L_POLY_A", "FOURTH_MOMENT_H", "LOW_HEIGHT_MULTIPLICITY_COUNT"],
            "conclusion": "The amended qT-dependent cutoff removes Z03 as an independent obstruction; the named premises and S06/S03/F08/q1-sensitive obligations remain open.",
            "not_promoted": "No CGL theorem, density estimate, or short-interval result.",
        },
        "immutable_v1": {"path": str(V1.relative_to(ROOT)), "sha256": V1_HASH},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": DOC_HASH},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/p6_detector_qt_tail_v2_status_correction.py --check",
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
        require(not OUT.exists(), "refusing to overwrite status correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "status-correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
