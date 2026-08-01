#!/usr/bin/env python3
"""Scope correction to the adversarial explicit-formula audit v1."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    "adversarial_audit_v1": ("artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json", "04df15499e7440022a438368af28b9804f5eb9987456ba5eab8c6220725271a7"),
    "source_closure_v3": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v3.json", ""),
    "source_check_v3": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v3.py", "0ccb071e86f84e9c5eacffac47f503c1520c73395eb05406123937b4ae7e49f8"),
    "dspace_metadata": ("artifacts/sources/mit-dspace-1721.1-101679-metadata.json", "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate() -> dict[str, Any]:
    hashes: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        if expected:
            assert actual == expected, f"hash mismatch: {relative}"
        hashes[name] = actual
    subprocess.run(["python3", str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v3.py")], check=True, capture_output=True, text=True)
    old = json.loads((ROOT / "artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json").read_text())
    source = json.loads((ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v3.json").read_text())
    assert old["licensing_and_provenance"]["status"] == "OBSERVED"
    assert source["primary_source_scope"]["status"] == "PROVED"
    return {
        "artifact_type": "adversarial-stream-c-explicit-formula-v2-v2-scope-correction",
        "certificate_version": 2,
        "supersedes": "adversarial audit v1 only for its interpretation of the preregistered source-authority clause; v1 remains preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED scope adjudication: author-hosted primary course sources satisfy the Cycle-2 reachable-primary-source requirement. No byte-identity or author-byte OCW-license claim is made, and G0 is not declared PASS.",
        "withdrawn_v1_inference": {
            "status": "PROVED",
            "statement": "V1 treated missing byte identity between author-hosted copies and DSpace objects as a mathematical source-authority blocker.",
            "correction": "The preregistration requires a reachable primary source, not byte identity or proof that author-hosted bytes inherit an OCW license. Kedlaya's direct course-hosted PDFs are primary sources; official DSpace metadata independently identifies the same course and author."
        },
        "mathematical_source_authority": {
            "status": "PROVED",
            "result": "No mathematical source-authority blocker remains for the explicit-formula theorem, its all-T range, half-weight convention, remainder, or multiplicity proof under the stated preregistration.",
            "evidence": "source-closure v3 pins both direct author course PDFs, official course/author metadata, all theorem anchors, and mutool 1.23.10."
        },
        "distribution_caveat": {
            "status": "OBSERVED",
            "statement": "Direct DSpace bitstream retrieval and author/DSpace byte identity remain unverified. This concerns distribution/provenance, not the required mathematical primary-source authority.",
            "non_claim": "No assertion is made that the frozen author-hosted PDF bytes are OCW-licensed bytes."
        },
        "preregistration_effect": {
            "status": "PROVED",
            "result": "The explicit-formula source-authority subgate is closed. This correction alone does not establish G0 PASS, which still requires all Stream-A and Stream-C route reconciliation gates."
        },
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v2.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v2.json"
        }
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", type=Path)
    mode.add_argument("--check", type=Path)
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.write_text(output, encoding="utf-8")
    else:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")


if __name__ == "__main__":
    main()
