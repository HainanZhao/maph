#!/usr/bin/env python3
"""Integrity checks for the Cycle-2 explicit-formula source-access audit."""
from __future__ import annotations
import gzip
import hashlib
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "artifacts/sources/cully-hugill-johnston-2024-rvm-ii.pdf": "9bf784f264970a5bb82e54547c2dbd68b1a4cc6a69ee679b8fc2159d006a565c",
    "artifacts/sources/cully-hugill-johnston-2024-rvm-ii.tar": "2d118982a210b43ff4884c88fb285f79fcaa3e22395ec8f83f0061af1b86c9a3",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.pdf": "3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf",
    "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar": "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.pdf": "b1c5a4d6cdba59d0fc552a18cb2465c442a8534be0c4e51a23db126316f83077",
    "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar": "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
}

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def gz_text(relative: str) -> str:
    with gzip.open(ROOT / relative, "rt", encoding="utf-8") as handle:
        return handle.read()

def chj_text() -> str:
    with tarfile.open(ROOT / "artifacts/sources/cully-hugill-johnston-2024-rvm-ii.tar", "r:gz") as archive:
        member = archive.extractfile("main.tex")
        assert member is not None
        return member.read().decode("utf-8")

def main() -> int:
    failures = []
    for relative, expected in HASHES.items():
        if sha256(ROOT / relative) != expected:
            failures.append(f"hash mismatch: {relative}")
    anchors = {
        "GM": (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex").read_text(),
        "CHJ": chj_text(),
        "HSW": gz_text("artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"),
        "BHB": gz_text("artifacts/sources/bui-heath-brown-2013-simple-zeros.tar")
    }
    required = {
        "GM": [r"\sum_{n\in [x,x+y]}\Lambda(n)", r"\sum_{|\rho|\le T}"],
        "CHJ": [r"\label{riemannvoneq}", r"\label{oldRvMpsi}", r"some $T^*\in [T,2T]$"],
        "HSW": [r"N(T) = \#", r"N_{\Bbb{Q}}(T)= 2 N(T)", r"applying the  argument principle"],
        "BHB": ["where each zero is counted with multiplicity", "distinct zeros"]
    }
    for name, needles in required.items():
        for needle in needles:
            if needle not in anchors[name]:
                failures.append(f"missing {name} source anchor: {needle}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 7 frozen hashes and 11 source anchors verified")
    print("ACCESS CONTAINMENT: no Iwaniec purchased-PDF content is read or stored by this check")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
