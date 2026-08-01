#!/usr/bin/env python3
"""Seal the canonical-tag correction for P7 norm aggregation v2."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SELF = Path(__file__).resolve()
V2 = ROOT / "artifacts/p7-norm-aggregation-v2-correction.json"
V2_DOC = ROOT / "docs/p7-norm-aggregation-v2-correction.md"
DOC = ROOT / "docs/p7-norm-aggregation-v3-status-correction.md"
OUT = ROOT / "artifacts/p7-norm-aggregation-v3-status-correction.json"
V2_HASH = "200f4328c72e2af2ffe08a9fd3b9901bbbf6b2977c18a34e20a20fb020f033d0"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)


def payload() -> dict[str, object]:
    require(sys.flags.optimize == 0, "optimized Python is rejected")
    require(digest(V2) == V2_HASH, "immutable P7 norm v2 artifact changed")
    old_doc = V2_DOC.read_text(encoding="utf-8")
    require("`PROVED_CONDITIONAL_ON_LENGTH_HEIGHT_RELATION`" in old_doc, "recorded v2 tag defect missing")
    v2 = json.loads(V2.read_text(encoding="utf-8"))
    require(v2["reconciliation"]["normalization"]["covered_regime"] == "N<=T^C fixed C, including the source proof's N<T reduction", "v2 covered regime changed")
    return {
        "artifact_id": "p7-norm-aggregation-v3-status-correction",
        "epistemic_status": "OBSERVED",
        "correction": "Replace the v2 document's noncanonical compound tag by PROVED conditional on the explicit hypothesis N<=T^C for fixed C.",
        "corrected_claim": {
            "epistemic_status": "PROVED",
            "hypothesis": "N<=T^C for a fixed C",
            "conclusion": "The recorded divisor normalization is exponent-harmless in the cited single-polynomial theorem, including the pinned N<T regime.",
            "uncovered": "No unrestricted independent-(N,T) absorption or Hecke-family density theorem.",
        },
        "immutable_v2": {"path": str(V2.relative_to(ROOT)), "sha256": V2_HASH},
        "immutable_v2_document": {"path": str(V2_DOC.relative_to(ROOT)), "sha256": digest(V2_DOC)},
        "document": {"path": str(DOC.relative_to(ROOT)), "sha256": digest(DOC)},
        "sealer": {"path": str(SELF.relative_to(ROOT)), "sha256": digest(SELF)},
        "hostile_audit": "DEFERRED_TO_PAPER_STAGE",
        "replay": "python3 proof/p7_norm_aggregation_v3_status_correction.py --check",
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
        require(not OUT.exists(), "refusing to overwrite P7 status correction")
        OUT.write_bytes(encoded)
    else:
        require(OUT.is_file() and OUT.read_bytes() == encoded, "P7 status-correction artifact mismatch")
    print(json.dumps({"artifact": OUT.name, "status": "ok"}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
