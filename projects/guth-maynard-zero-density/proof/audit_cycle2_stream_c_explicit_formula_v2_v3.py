#!/usr/bin/env python3
"""Audit the official-SWORD correction to the Stream-C source closure."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    "adversarial_audit_v1": (
        "artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json",
        "04df15499e7440022a438368af28b9804f5eb9987456ba5eab8c6220725271a7",
    ),
    "adversarial_audit_v2": (
        "artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v2.json",
        "c3aab9e64469ac180ba2eec88a7a50d2a239085f6402c512e8bf197af4db015e",
    ),
    "source_closure_v4": (
        "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json",
        "1c4ecc54be6f681be788084c3637f1101996869e09015edac8cf41e6ab39d5f0",
    ),
    "source_check_v4": (
        "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py",
        "72107f1f31e51d2aa9d0ea0eb22c247a1643e58a898232a7fd02c3dee5508064",
    ),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def certificate() -> dict[str, Any]:
    hashes: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"hash mismatch: {relative}"
        hashes[name] = actual
    subprocess.run(
        ["python3", str(ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py")],
        check=True,
        capture_output=True,
        text=True,
    )
    old = json.loads(
        (ROOT / "artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v2.json").read_text()
    )
    source = json.loads(
        (ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v4.json").read_text()
    )
    assert old["distribution_caveat"]["status"] == "OBSERVED"
    assert source["official_source"]["status"] == "PROVED"
    assert source["official_sword_bitstream"]["status"] == "PROVED"
    return {
        "artifact_type": "adversarial-stream-c-explicit-formula-v2-v3-official-source-correction",
        "certificate_version": 3,
        "supersedes": "adversarial audit v2 for official licensed-source provenance only; v1 and v2 remain preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": "PROVED that direct official licensed PDFs now close the distribution/provenance caveat recorded in v2. This correction does not establish G0 PASS.",
        "official_access": {
            "status": "PROVED",
            "result": "The pinned MIT DSpace SWORD bitstream directly contains both checked source PDFs; their extracted bytes equal the stated archive members.",
            "evidence": "source-closure v4 pins the bitstream UUID and URL, archive hash and size, member hashes and sizes, official course metadata, exact PDF anchors, and mutool 1.23.10."
        },
        "license_correction": {
            "status": "PROVED",
            "result": "The official course metadata records CC BY-NC-SA 3.0. V2's CC 4.0/author-byte license inference is withdrawn.",
            "non_claim": "This audit does not claim that any author-hosted bytes are byte-identical to, or licensed as, the official archive members."
        },
        "withdrawn_distribution_caveat": {
            "status": "PROVED",
            "result": "The v2 distribution caveat is resolved for the official source route: no author/DSpace byte identity is necessary once the official PDFs themselves are frozen and checked."
        },
        "mathematical_source_authority": {
            "status": "PROVED",
            "result": "The theorem hypotheses, half-weight convention, remainder, and multiplicity proof are directly sourced from official licensed PDF members."
        },
        "preregistration_effect": {
            "status": "PROVED",
            "result": "The explicit-formula source-authority and official-distribution subgates are closed. This correction alone does not establish G0 PASS, which still requires all Stream-A and Stream-C route reconciliation gates."
        },
        "frozen_hashes": hashes,
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v3.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v3.json"
        },
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
    elif args.check.read_text(encoding="utf-8") != output:
        raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")


if __name__ == "__main__":
    main()
