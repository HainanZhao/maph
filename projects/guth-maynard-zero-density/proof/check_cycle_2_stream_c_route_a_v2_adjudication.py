#!/usr/bin/env python3
"""Replay the independent containment audit of Stream-C Route-A v2.

This is deliberately a negative check: it verifies the frozen text that
prevents CHJ-I Theorem 1.2 from being used at the Route-A almost-all height.
It does not edit or replay Route-A v2 itself.
"""
from __future__ import annotations

import hashlib
import json
from fractions import Fraction
from pathlib import Path
import tarfile


ROOT = Path(__file__).resolve().parents[1]
HASHES = {
    "artifacts/sources/cully-hugill-johnston-2023-rvm-i.tar": "53f5380061ab371849f4805deed7884b887134cc586fbeec18f2ab444cb84953",
    "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    "artifacts/sources/kedlaya-2007-errorbounds-author.pdf": "375d96e65a99d7dbfbdc9ca51aa286bb53af7e77dfffa59e167dfcd9b18b919d",
    "artifacts/sources/kedlaya-2007-von-mangoldt-author.pdf": "43cbe51ee69fe552078d90d0c21b165456f3ad67ad64c83df71b9cce3d56ae05",
    "artifacts/cycle-2-stream-c-explicit-formula-source-closure-v1.json": "24248e58028651ba2903b023fe2b9f660ab5dff9606b2ca2c879f462dd94b297",
    "proof/check_cycle_2_stream_c_explicit_formula_sources.py": "2a7191d966c7c3717f88829111dd63ea8449981c65f5b7be6eb2f7381d07f46c",
    "docs/cycle-2-stream-c-route-a-v2.md": "4423b10307dfa318ee82bb4742119f6123ae972ebf4cabd24ac740a8a37f1b1f",
    "proof/replay_cycle2_stream_c_route_a_v2.py": "5d0c939b8ce7e06f25da4790a05f52a5fd92b754d8b60d4dddee2c3e3a6a1f54",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def chj_tex() -> str:
    archive = ROOT / "artifacts/sources/cully-hugill-johnston-2023-rvm-i.tar"
    with tarfile.open(archive, "r:gz") as handle:
        member = handle.extractfile("main.tex")
        assert member is not None
        return member.read().decode("utf-8")


def main() -> int:
    failures: list[str] = []
    for relative, expected in HASHES.items():
        if digest(ROOT / relative) != expected:
            failures.append(f"hash mismatch: {relative}")

    chj = chj_tex()
    gm = (ROOT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex").read_text()
    route_a_v2 = json.loads((ROOT / "artifacts/cycle-2-stream-c-route-a-v2.json").read_text())
    required_chj = [
        r"For any $\alpha\in(0,1/2]$",
        r"\max\{51,\log x\}<T<(x^{\alpha}-2)/2",
        r"where the sum is over all non-trivial zeros",
        r"Note we cannot take $\alpha>1/2$",
        r"N(t+1)-N(t-1)<\log t",
    ]
    required_gm = [
        r"T=xy^{-1}\exp(2\sqrt[4]{\log{x}})",
        r"\delta=X^{-13/15+\epsilon/2}",
        r"T=\delta^{-1}\exp(4\sqrt[4]{\log{X}})",
        r"\sum_{|\rho|\le T}",
    ]
    for needle in required_chj:
        if needle not in chj:
            failures.append(f"missing CHJ-I anchor: {needle}")
    for needle in required_gm:
        if needle not in gm:
            failures.append(f"missing GM anchor: {needle}")
    if route_a_v2.get("exact_replay_sha256") != "3e0e194aab6810a2697f7951058c3ee407fa3dc47e9ce91ba96139f037fc3970":
        failures.append("Route-A-v2 semantic replay identity changed")

    # T_a = X^(13/15-epsilon/2) exp(4 log(X)^(1/4)).  The exponent
    # exceeds 1/2 whenever epsilon < 11/15; epsilon=1/100 is one
    # permitted small-epsilon instance and suffices to refute a universal
    # claim that CHJ-I alone covers the Route-A almost-all branch.
    epsilon = Fraction(1, 100)
    almost_exponent = Fraction(13, 15) - epsilon / 2
    if not almost_exponent > Fraction(1, 2):
        failures.append("almost-all height exponent unexpectedly fits CHJ-I")
    if Fraction(13, 30) >= Fraction(1, 2):
        failures.append("uniform height exponent unexpectedly fails CHJ-I")
    if "multiplicity" in chj.lower():
        failures.append("audit premise changed: CHJ-I now explicitly mentions multiplicity")

    if failures:
        print("FAIL")
        print("\n".join(failures))
        return 1
    print("PASS: 8 frozen hashes, 1 semantic Route-A-v2 identity, and 9 primary-text anchors verified")
    print("CONTAINMENT: CHJ-I Theorem 1.2 covers the eventual uniform-height branch, not Route-A's almost-all height.")
    print("CONVENTION GAP: CHJ-I says all zeros but does not state multiplicity; GM prints |rho| while CHJ-I uses |gamma|.")
    print("COMMON NODE: use the archived Kedlaya course proof plus the existing Iwaniec/HSW/Bui ledger; the archival published-primary subgate remains open.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
