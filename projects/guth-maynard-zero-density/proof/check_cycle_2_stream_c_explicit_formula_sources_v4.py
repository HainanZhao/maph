#!/usr/bin/env python3
"""Replay the official MIT OCW archive closure for Stream-C's formula source."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import zipfile


ROOT = Path(__file__).resolve().parents[1]
MUTOOL_VERSION = "mutool version 1.23.10"
HASHES = {
    "artifacts/sources/mit-ocw-18-785-2007-sword-official.zip": "d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57",
    "artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf": "b8b2acfbc4b22b25c898c0af8f74692a0d31bd6cf302e9f2d772d33a34fdd3e4",
    "artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf": "5f705a6d3804d555944298f87a8a53e2e4e5a13188a717679f8fb8b73095210a",
    "artifacts/sources/mit-dspace-1721.1-101679-metadata.json": "4c1f262bc51efa23993a561f908871d35245ca462df90271d0bf2127283f24c7",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
}
MEMBERS = {
    "18-785-spring-2007/contents/lecture-notes/errorbounds.pdf": "b8b2acfbc4b22b25c898c0af8f74692a0d31bd6cf302e9f2d772d33a34fdd3e4",
    "18-785-spring-2007/contents/lecture-notes/von_mangoldt.pdf": "5f705a6d3804d555944298f87a8a53e2e4e5a13188a717679f8fb8b73095210a",
}


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def text(relative: str) -> str:
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
    with zipfile.ZipFile(ROOT / "artifacts/sources/mit-ocw-18-785-2007-sword-official.zip") as archive:
        for member, expected in MEMBERS.items():
            if sha256_bytes(archive.read(member)) != expected:
                failures.append(f"official archive member mismatch: {member}")
    version = subprocess.run(["mutool", "-v"], check=True, capture_output=True, text=True)
    if (version.stdout + version.stderr).strip() != MUTOOL_VERSION:
        failures.append("mutool version mismatch")
    metadata = json.loads((ROOT / "artifacts/sources/mit-dspace-1721.1-101679-metadata.json").read_text())
    rights = [item["value"] for item in metadata["metadata"]["dc.rights.uri"]]
    if metadata.get("handle") != "1721.1/101679" or metadata.get("withdrawn"):
        failures.append("official item identity/status mismatch")
    if "Usage Restrictions: Attribution-NonCommercial-ShareAlike 3.0 Unported" not in rights:
        failures.append("course-specific CC BY-NC-SA 3.0 right missing")
    formula, proof = text("artifacts/sources/mit-ocw-18-785-2007-errorbounds-official.pdf"), text("artifacts/sources/mit-ocw-18-785-2007-von-mangoldt-official.pdf")
    for anchor in ("Theorem 1 (von Mangoldt’s formula). For x ∼ 2 and T > 0", "n<x", "x log2(xT )", "nearest prime power other than possibly x itself"):
        if anchor not in formula:
            failures.append(f"missing official formula anchor: {anchor!r}")
    # The Ghostscript-reprocessed proof member maps the displayed \(\geq\)
    # glyph differently from the formula member; pin each literal extraction.
    for anchor in ("Theorem 1 (von Mangoldt’s formula). For x √ 2 and T > 0", "counted with multiplicity", "We are done!"):
        if anchor not in proof:
            failures.append(f"missing official proof anchor: {anchor!r}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 7 frozen hashes, 2 official archive-member hashes, course CC metadata, 7 official-PDF anchors, and mutool 1.23.10 verified")
    print("OFFICIAL ACCESS: SWORD archive bitstream UUID 7292f134-d4a7-4063-bd7e-2084259b8fa9; author-copy byte identity is neither needed nor asserted.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
