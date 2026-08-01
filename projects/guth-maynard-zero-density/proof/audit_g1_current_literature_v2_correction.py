#!/usr/bin/env python3
"""Seal/check the v2 presentation correction for the G1 literature audit.

The v1 report is historical evidence and is intentionally read-only.  This
successor records one byte-level rendering defect in that report, supplies a
clean correction notice, and verifies that the v1 JSON audit and its bounded
claims are unchanged.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


PROJECT = Path(__file__).resolve().parents[1]
V1_REPORT = PROJECT / "docs" / "g1-current-literature-audit-v1.md"
V1_ARTIFACT = PROJECT / "artifacts" / "g1-current-literature-audit-v1.json"
CORRECTION_REPORT = PROJECT / "docs" / "g1-current-literature-audit-v2-correction.md"
ARTIFACT = PROJECT / "artifacts" / "g1-current-literature-audit-v2-correction.json"

V1_REPORT_SHA256 = "3fe0fc50a9ea2ff56c1f5b9ec3422a1675a34b4ab6641453bd9aff1058407a2c"
V1_ARTIFACT_SHA256 = "49da2e838ce60699ba870e0c532aab5ec8ba564c560811d9683ac92f0afbe6be"
DEFECT_OFFSET = 1421
BAD_FRAGMENT = b"S_{M_{" + bytes((13,)) + b"m Dir},3}"
CORRECTED_FRAGMENT = b"S_{M_{\\rm Dir},3}"


def require(condition: bool, detail: str) -> None:
    if not condition:
        raise RuntimeError(detail)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_runtime() -> dict[str, object]:
    require(sys.implementation.name == "cpython", "requires CPython")
    require(sys.version_info[:3] == (3, 12, 3), "requires CPython 3.12.3")
    require(sys.flags.optimize == 0, "optimized Python is not permitted")
    return {
        "implementation": sys.implementation.name,
        "version": ".".join(map(str, sys.version_info[:3])),
        "optimize": sys.flags.optimize,
    }


def verify_v1_preservation() -> dict[str, object]:
    require(V1_REPORT.is_file(), f"missing preserved v1 report {V1_REPORT}")
    require(V1_ARTIFACT.is_file(), f"missing preserved v1 artifact {V1_ARTIFACT}")
    report_bytes = V1_REPORT.read_bytes()
    require(digest(V1_REPORT) == V1_REPORT_SHA256, "preserved v1 report hash mismatch")
    require(digest(V1_ARTIFACT) == V1_ARTIFACT_SHA256, "preserved v1 artifact hash mismatch")
    require(report_bytes.count(bytes((13,))) == 1, "v1 report no longer has exactly one 0x0d byte")
    require(report_bytes.find(bytes((13,))) == DEFECT_OFFSET, "v1 report 0x0d byte moved")
    require(report_bytes.count(BAD_FRAGMENT) == 1, "v1 report defect fragment mismatch")

    v1 = json.loads(V1_ARTIFACT.read_text(encoding="utf-8"))
    trace = next(
        row
        for row in v1["sources"]["guth_2503_07410v1"]["anchors"]
        if row["id"] == "GUTH-TRACE"
    )
    require("S_{M_Dir,3}" in trace["finding"], "v1 JSON trace identity unexpectedly changed")
    require(v1["route_decision"].startswith("NOT_MADE:"), "v1 route boundary unexpectedly changed")
    return {
        "v1_report": {
            "relative_path": "docs/g1-current-literature-audit-v1.md",
            "sha256": V1_REPORT_SHA256,
            "byte_length": len(report_bytes),
            "carriage_return_count": 1,
            "carriage_return_offset_zero_based": DEFECT_OFFSET,
            "preservation": "v1 is verified byte-for-byte and remains unmodified",
        },
        "v1_artifact": {
            "relative_path": "artifacts/g1-current-literature-audit-v1.json",
            "sha256": V1_ARTIFACT_SHA256,
            "preservation": "v1 JSON claims and route boundary are verified unchanged",
        },
    }


def verify_correction_report() -> dict[str, str]:
    require(CORRECTION_REPORT.is_file(), f"missing correction report {CORRECTION_REPORT}")
    report_bytes = CORRECTION_REPORT.read_bytes()
    require(bytes((13,)) not in report_bytes, "correction report contains a carriage-return byte")
    require(CORRECTED_FRAGMENT in report_bytes, "correction report omits corrected tensor rendering")
    require(b"mathematical, provenance, overlap, route-selection, or novelty claim changes." in report_bytes,
            "correction report omits unchanged-claims boundary")
    return {
        "relative_path": "docs/g1-current-literature-audit-v2-correction.md",
        "sha256": digest(CORRECTION_REPORT),
    }


def build() -> dict[str, Any]:
    runtime = verify_runtime()
    v1 = verify_v1_preservation()
    correction_report = verify_correction_report()
    return {
        "artifact_id": "g1-current-literature-audit-v2-correction",
        "schema": 1,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "OBSERVED byte-level presentation correction only. It changes no source, theorem, provenance, overlap, novelty, route-selection, or G1/P2 claim.",
        "supersedes": {
            "artifact": "g1-current-literature-audit-v1",
            "scope": "presentation of the named cubic-tensor identifier in the companion Markdown report only",
            "preservation": "the v1 report and v1 JSON artifact remain byte-pinned and unmodified",
        },
        "correction": {
            "status": "OBSERVED",
            "affected_document": "docs/g1-current-literature-audit-v1.md",
            "location": "Cubic and higher tensors table row; byte offset 1421 (zero-based)",
            "defect": "A literal 0x0d carriage-return byte replaced the intended two-byte backslash-r sequence in S_{M_{\\rm Dir},3}.",
            "cause": "The immediate byte-level cause is established; the upstream authoring mechanism is not determined by this correction.",
            "corrected_rendering": "S_{M_{\\rm Dir},3}",
            "affected_claims": "None. The v1 JSON anchor already records S_{M_Dir,3}; the underlying pinned Guth TeX and all v1 source checks are unchanged.",
            "non_promotion": "This correction is not a theorem, source re-audit, novelty determination, G1 route decision, or P2 authorization.",
        },
        "integrity": {
            "runtime": runtime,
            "preserved_v1": v1,
            "correction_report": correction_report,
        },
        "replay": {
            "builder": "proof/audit_g1_current_literature_v2_correction.py",
            "builder_sha256": digest(Path(__file__).resolve()),
            "write_command": "python3 proof/audit_g1_current_literature_v2_correction.py --write",
            "check_command": "python3 proof/audit_g1_current_literature_v2_correction.py --check",
            "test_command": "python3 -m unittest tests/test_g1_current_literature_audit_v2_correction.py -v",
        },
    }


def encoded(value: dict[str, Any]) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    action = parser.add_mutually_exclusive_group(required=True)
    action.add_argument("--write", action="store_true")
    action.add_argument("--check", action="store_true")
    args = parser.parse_args()
    payload = encoded(build())
    if args.write:
        ARTIFACT.write_bytes(payload)
        print(f"wrote {ARTIFACT.relative_to(PROJECT)}")
        return 0
    require(ARTIFACT.is_file(), f"missing correction artifact {ARTIFACT}")
    require(ARTIFACT.read_bytes() == payload, "correction artifact differs; rerun --write only after reviewing the correction")
    print(json.dumps({"verified": True, "artifact": ARTIFACT.name}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
