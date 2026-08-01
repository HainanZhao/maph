#!/usr/bin/env python3
"""Replay the OA/CC source-access closure for the Stream-C formula node."""
from __future__ import annotations

import hashlib
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "artifacts/sources/kedlaya-2007-errorbounds-author.pdf": "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d",
    "artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf": "43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def text_of_pdf(relative: str) -> str:
    """Extract text from a pinned PDF using the system renderer, fail closed if absent."""
    result = subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", "-", str(ROOT / relative)],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def main() -> int:
    failures: list[str] = []
    for relative, expected in HASHES.items():
        if sha256(ROOT / relative) != expected:
            failures.append(f"hash mismatch: {relative}")
    formula = text_of_pdf("artifacts/sources/kedlaya-2007-errorbounds-author.pdf")
    proof = text_of_pdf("artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf")
    required_formula = [
        "For x ≥ 2 and T > 0",
        "n<x\nΛ(n) + 1\n\n2Λ(x).",
        "x log2(xT)",
        "distance from x to the nearest prime power other than possibly x itself",
    ]
    required_proof = [
        "For x ≥ 2 and T > 0",
        "every zero ρ of\nζ (counted with multiplicity)",
        "We are done!",
    ]
    for needle in required_formula:
        if needle not in formula:
            failures.append(f"missing formula-PDF anchor: {needle!r}")
    for needle in required_proof:
        if needle not in proof:
            failures.append(f"missing proof-PDF anchor: {needle!r}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 5 frozen hashes and 7 Kedlaya formula/proof anchors verified")
    print("LICENSE PROVENANCE: MIT OCW 18.785 handle 1721.1/101679; CC BY-NC-SA 4.0, source paths recorded in ledger v2.")
    print("RETRIEVAL CONTAINMENT: DSpace WAF 405/403 blocks direct fetch; pinned author-hosted course mirrors provide byte replay.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
