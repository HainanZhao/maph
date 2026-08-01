#!/usr/bin/env python3
"""Pinned primary-source and tool audit for the Stream-C formula node."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess


ROOT = Path(__file__).resolve().parents[1]
MUTOOL_VERSION = "mutool version 1.23.10"
HASHES = {
    "artifacts/sources/kedlaya-2007-errorbounds-author.pdf": "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d",
    "artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf": "43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05",
    "artifacts/sources/mit-dspace-1721.1-101679-metadata.json": "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def mutool_text(relative: str) -> str:
    result = subprocess.run(
        ["mutool", "draw", "-F", "txt", "-o", "-", str(ROOT / relative)],
        check=True, capture_output=True, text=True,
    )
    return result.stdout


def main() -> int:
    failures: list[str] = []
    for relative, expected in HASHES.items():
        if sha256(ROOT / relative) != expected:
            failures.append(f"hash mismatch: {relative}")
    version = subprocess.run(["mutool", "-v"], check=True, capture_output=True, text=True)
    reported = (version.stdout + version.stderr).strip()
    if reported != MUTOOL_VERSION:
        failures.append(f"mutool version mismatch: {reported!r}")
    metadata = json.loads((ROOT / "artifacts/sources/mit-dspace-1721.1-101679-metadata.json").read_text())
    if metadata.get("handle") != "1721.1/101679" or metadata.get("name") != "18.785 Analytic Number Theory, Spring 2007":
        failures.append("DSpace course identity mismatch")
    author = metadata["metadata"].get("dc.contributor.author", [{}])[0].get("value")
    rights = [entry.get("value") for entry in metadata["metadata"].get("dc.rights.uri", [])]
    if author != "Kedlaya, Kiran":
        failures.append("DSpace author mismatch")
    if "Usage Restrictions: Attribution-NonCommercial-ShareAlike 3.0 Unported" not in rights:
        failures.append("DSpace course-specific CC BY-NC-SA 3.0 right missing")
    formula = mutool_text("artifacts/sources/kedlaya-2007-errorbounds-author.pdf")
    proof = mutool_text("artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf")
    for anchor in ("18.785: Analytic Number Theory, MIT, spring 2007 (K.S. Kedlaya)", "For x ≥ 2 and T > 0", "n<x\nΛ(n) + 1\n\n2Λ(x).", "x log2(xT)", "distance from x to the nearest prime power other than possibly x itself"):
        if anchor not in formula:
            failures.append(f"missing formula anchor: {anchor!r}")
    for anchor in ("18.785: Analytic Number Theory, MIT, spring 2007 (K.S. Kedlaya)", "For x ≥ 2 and T > 0", "ζ (counted with multiplicity) contributes −xρ/ρ.", "We are done!"):
        if anchor not in proof:
            failures.append(f"missing proof anchor: {anchor!r}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 6 frozen hashes, DSpace course/author/CC metadata, 9 PDF anchors, and mutool 1.23.10 verified")
    print("SCOPE: author-hosted PDFs are treated as K. S. Kedlaya's direct primary course sources; no byte identity with DSpace objects is asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
