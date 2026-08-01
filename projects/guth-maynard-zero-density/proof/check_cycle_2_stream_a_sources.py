#!/usr/bin/env python3
"""Replay Cycle-2 Stream-A frozen-source integrity checks."""
from __future__ import annotations
import hashlib
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CHECKS = {
    "artifacts/sources/maynard-pratt-2206.11729.pdf": "e6407c953c4ddcbf9daa2fa941d1a84bf9db90f19a96e50ee8796bf9aea5947a",
    "artifacts/sources/maynard-pratt-2206.11729.tar": "b81dbb3bb8bed014588294b5c6d7e8e4b5a14798f445baecb6680b7a9df967d3",
    "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex": "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426",
    "artifacts/sources/arxiv-2405.20552v2.pdf": "915392cf7d0ecd108479814a9a1481e23423ef63415776471cec3975ae482cae",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    "artifacts/sources/montgomery-1969-inventiones8-gdz-volume.pdf": "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e",
}
ANCHORS = {
    "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex": [r"We write $n \sim N$ for the condition $N < n \leq 2N$.", r"\label{lmm:TypeIIIZeros}", r"\label{lem:TypeIIZeroBound}", r"R_{II}(\sigma,T) \ll T^{2(1-\sigma)}(\log T)^{O(1)}", r"We say $\rho$ is a `Type II zero'"],
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": [r"Given an integer $N\in \mathbb{N}$ and a sequence $(b_n)_{N<n\le 2N}$", r"If it is not a Type I zero then it is a `Type II zero'", r"If instead we have $N^k>T^\alpha$", r"|W|\lessapprox N^{2k-2k\sigma}+TN^{k-2k\sigma}"],
}

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main() -> int:
    failures = []
    for relative, expected in CHECKS.items():
        observed = digest(ROOT / relative)
        if observed != expected:
            failures.append(f"hash mismatch: {relative}: {observed}")
    for relative, anchors in ANCHORS.items():
        text = (ROOT / relative).read_text(encoding="utf-8")
        for anchor in anchors:
            if anchor not in text:
                failures.append(f"missing source anchor: {relative}: {anchor}")
    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 6 frozen hashes and 9 source anchors verified")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
