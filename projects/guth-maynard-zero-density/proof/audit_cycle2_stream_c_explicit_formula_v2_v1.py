#!/usr/bin/env python3
"""Adversarial audit of Stream-C's v2 formula ledger and Route-B v4 use."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FROZEN = {
    "ledger_v2": ("artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json", "3433e974b9751d310447847d75abbf529e5b4ed7e21e87a0224e4efb8ea0fde3"),
    "ledger_v2_check": ("proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py", "346a7beb7a5c2387b99f5a3e03a78bd0bf9856b38ce0e6bd4da0192d95b95f27"),
    "route_b_v4": ("artifacts/cycle-2-stream-c-route-b-v4.json", "a8c7be629b8bff5cce4ce4a7ee5e5c1e52969b0681a45008834f7e548a8db249"),
    "route_b_v4_replay": ("proof/replay_short_intervals_stream_c_route_b_v4.py", "1be7195a890046e7aff63069137a5ab224bd2496f180fb87f12de9410723882a"),
    "formula_pdf": ("artifacts/sources/kedlaya-2007-errorbounds-author.pdf", "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d"),
    "proof_pdf": ("artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf", "43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05"),
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_text(relative: str) -> str:
    completed = subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", "-", str(ROOT / relative)],
        check=True, capture_output=True, text=True,
    )
    return completed.stdout


def verify() -> dict[str, str]:
    observed: dict[str, str] = {}
    for name, (relative, expected) in FROZEN.items():
        actual = sha256(ROOT / relative)
        assert actual == expected, f"hash mismatch: {relative}"
        observed[name] = actual
    formula = pdf_text("artifacts/sources/kedlaya-2007-errorbounds-author.pdf")
    proof = pdf_text("artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf")
    for anchor in ("For x ≥ 2 and T > 0", "n<x\nΛ(n) + 1\n\n2Λ(x).", "x log2(xT)", "distance from x to the nearest prime power other than possibly x itself"):
        assert anchor in formula, f"missing formula anchor: {anchor!r}"
    for anchor in ("For x ≥ 2 and T > 0", "ζ (counted with multiplicity) contributes −xρ/ρ.", "We are done!"):
        assert anchor in proof, f"missing proof anchor: {anchor!r}"
    return observed


def certificate() -> dict[str, Any]:
    hashes = verify()
    ledger = json.loads((ROOT / "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v2.json").read_text())
    route = json.loads((ROOT / "artifacts/cycle-2-stream-c-route-b-v4.json").read_text())
    check_script = (ROOT / "proof/check_cycle_2_stream_c_explicit_formula_sources_v2.py").read_text()
    assert ledger["ocw_license"]["status"] == "PROVED"
    assert "HTTP 405/403" in ledger["course_provenance"]["retrieval_status"]
    assert route["external_truncated_explicit_formula"]["status"] == "PROVED"
    assert "mutool" in check_script and "--version" not in check_script
    return {
        "artifact_type": "adversarial-stream-c-explicit-formula-v2-v1-audit",
        "certificate_version": 1,
        "epistemic_status": "OBSERVED",
        "claim_boundary": "Adversarial source/hypothesis audit only. It does not change ledger v2 or Route B v4, does not declare G0 PASS, and does not dispute the mathematical formula read from the pinned bytes.",
        "frozen_hashes": hashes,
        "mathematical_hypotheses": {
            "status": "PROVED conditional on the pinned Kedlaya theorem text",
            "theorem_range": "The pinned formula and proof PDFs state x>=2 and T>0, so both GM choices 2<=T<=x are within their displayed range.",
            "half_weight": "The formula defines psi with half weight at integral prime powers.",
            "remainder": "The stated remainder has x log^2(xT)/T plus the distance-to-other-prime-power term.",
            "multiplicity": "The pinned proof explicitly says that every zero contribution is counted with multiplicity.",
            "proof_completion": "The pinned proof reaches 'We are done!'."
        },
        "transfer_audit": {
            "status": "PROVED conditional on the pinned formula theorem and HSW+Bui local-count node",
            "endpoint": "For u=ceil(x)-1 and v=floor(x+y), psi_0(v)-psi_0(u) differs from the integer sum on [x,x+y] by at most half endpoint weights, O(log x); v-u=y+O(1).",
            "prime_power_distance": "At integral u,v, every distinct prime power is an integer at distance at least one. The source distance term is therefore O(log x).",
            "constant_terms": "The constant -zeta'(0)/zeta(0) cancels under subtraction; the remaining elementary logarithm changes by O(y/x^3) for u,v asymp x and is harmless.",
            "height_boundary": "With 0<beta<1 and T>=2, the symmetric difference between |Im rho|<T and literal |rho|<=T lies in unit strips about +/-T. A multiplicity-inclusive O(log T) local count gives O(x log T/T), absorbed by O(x(log x)^3/T)."
        },
        "licensing_and_provenance": {
            "status": "OBSERVED",
            "official_license_fact": "MIT OCW's official terms state CC BY-NC-SA 4.0 for OCW materials; this general license statement was checked separately.",
            "formula_provenance": "The official DSpace indexed errorbounds path was identified, but direct DSpace retrieval returned 405/403 in this run.",
            "mirror_identity": "The frozen formula and proof bytes were downloaded from the author-hosted course mirrors. Byte identity with the inaccessible official DSpace formula object was not established.",
            "proof_provenance": "No official DSpace/OCW object locator for the frozen von-mangoldt.pdf proof byte was located in this audit; the author course calendar links it, which is evidence of course association but not a byte-level OCW provenance proof.",
            "license_scope": "No course-specific exception was observed, but absence from inspected pages is not proof that the OCW license applies to each author-hosted mirror byte."
        },
        "replay_hygiene": {
            "status": "OBSERVED",
            "finding": "The v2 source checker invokes mutool but does not record or verify its version. This run used mutool 1.23.10. The PDF hashes are pinned; the renderer version remains an unpinned extraction dependency."
        },
        "route_b_v4_adjudication": {
            "status": "OBSERVED",
            "finding": "Route B v4 labels the licensed source closure PROVED. Its theorem-content and transfer claims are PROVED conditional on the pinned text, but its archival license/mirror-provenance premise remains OBSERVED on the evidence currently recorded.",
            "effect": "A source-authority strict reading does not license a standalone PROVED archival-source closure from v4. This does not falsify the explicit formula or its endpoint/convention mathematics.",
            "blockers": [
                "Obtain a retrievable official OCW/DSpace proof-unit locator or a signed/official manifest tying von-mangoldt.pdf to handle 1721.1/101679.",
                "Establish byte identity (or official hash) between the frozen author formula mirror and the official DSpace formula object.",
                "Pin the mutool version or replace renderer-dependent string checks with a version-pinned extraction artifact."
            ]
        },
        "preregistration_effect": {
            "status": "OBSERVED",
            "result": "The formula theorem/range/error/endpoint/multiplicity/height mathematics has no newly found mathematical counterexample, but the reachable-primary/archival provenance subgate remains open under this hostile audit. G0 is not PASS."
        },
        "replay": {
            "script_sha256": sha256(Path(__file__)),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v1.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v1.json"
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
