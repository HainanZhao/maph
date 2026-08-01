#!/usr/bin/env python3
"""Versioned v2 closure audit for Cycle 2, Stream C, Route A.

This record supersedes no prior artifact: v1 is retained unchanged.  It pins
the Huxley near-one input and the Cully--Hugill--Johnston inputs which close
the three external-input blockers in v1.  It does not claim a new theorem.
"""

from __future__ import annotations

import gzip
import hashlib
import json
import platform
import sys
import tarfile
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


VERSION = 2
PROJECT = Path(__file__).resolve().parents[1]
GM = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
HUXLEY = PROJECT / "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf"
LEDGER = PROJECT / "docs/literature-ledger-classical-inputs.md"
FORD = PROJECT / "artifacts/sources/ford-2002-zero-free-regions.pdf"
CHJ_I = PROJECT / "artifacts/sources/cully-hugill-johnston-2023-rvm-i.tar"
CHJ_II = PROJECT / "artifacts/sources/cully-hugill-johnston-2024-rvm-ii.tar"
PLATT = PROJECT / "artifacts/sources/platt-trudgian-2021-rh-3e12.tar"
V1 = PROJECT / "artifacts/cycle-2-stream-c-route-a-v1.json"

HASHES = {
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    HUXLEY: "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    FORD: "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948",
    CHJ_I: "53f5380061ab371849f4805deed7884b887134cc586fbeec18f2ab444cb84953",
    CHJ_II: "2d118982a210b43ff4884c88fb285f79fcaa3e22395ec8f83f0061af1b86c9a3",
    PLATT: "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86",
}
B = Fraction(30, 13)
HUXLEY_AT_FOUR_FIFTHS = Fraction(15, 7)


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    encoded = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def tar_member_text(path: Path, member: str) -> str:
    with tarfile.open(path, "r:gz") as archive:
        handle = archive.extractfile(member)
        assert handle is not None
        return handle.read().decode("utf-8")


def gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as handle:
        return handle.read()


def check_sources() -> None:
    for path, expected in HASHES.items():
        assert sha256(path) == expected, f"hash mismatch: {path.name}"
    ledger = LEDGER.read_text(encoding="utf-8")
    gm = GM.read_text(encoding="utf-8")
    chj_i = tar_member_text(CHJ_I, "main.tex")
    chj_ii = tar_member_text(CHJ_II, "main.tex")
    platt = gzip_text(PLATT)
    for snippet in (
        "N(\\alpha,T)\\ll T^{3(1-\\alpha)/(3\\alpha-1)}\\ell^{44}",
        "3/4\\le\\alpha\\le1",
        "two-sided height",
    ):
        assert snippet in ledger, f"missing Huxley ledger declaration: {snippet}"
    for snippet in (
        "T^{15(1-\\sigma)/(3+5\\sigma)+o(1)}",
        "O(\\log{T})$ zeros in a horizontal strip of height 1",
        "T<x^{13/30-\\epsilon/2}",
    ):
        assert snippet in gm, f"missing GM declaration: {snippet}"
    for snippet in (
        "where the sum is over all non-trivial zeros",
        "For any $\\alpha\\in(0,1/2]$ there exist constants $M$ and $x_M$",
        "N(t+1)-N(t-1)<\\log t",
        "If $\\zeta(\\beta+i t)=0$ for any $|t|\\leq 3\\cdot 10^{12}$ then $\\beta=\\frac{1}{2}$",
    ):
        assert snippet in chj_i, f"missing CHJ-I declaration: {snippet}"
    for snippet in (
        "where the sum is over all non-trivial zeros",
        "some $T^*\\in [T,2T]$",
        "The most recent estimate for $N(T)$",
    ):
        assert snippet in chj_ii, f"missing CHJ-II declaration: {snippet}"
    assert "all zeroes $\\beta + i\\gamma$" in platt
    assert "$\\beta = 1/2$" in platt


def exact_closures() -> dict[str, Any]:
    assert HUXLEY_AT_FOUR_FIFTHS == Fraction(3, 1) / (3 * Fraction(4, 5) - 1)
    assert B - HUXLEY_AT_FOUR_FIFTHS == Fraction(15, 91)
    ratio = HUXLEY_AT_FOUR_FIFTHS / B
    assert ratio == Fraction(13, 14)
    return {
        "huxley_near_one": {
            "theorem": "N(s,T) << T^(3(1-s)/(3s-1))(log T)^44 for 3/4 <= s <= 1",
            "two_sided_to_gm": "The ledger checked that Huxley's N(alpha,T) is two-sided, matching GM's |Im rho| <= T convention.",
            "split": "Use GM's zero-density theorem through s=4/5 and Huxley for 4/5 <= s < 1.",
            "h_4_5": q(HUXLEY_AT_FOUR_FIFTHS),
            "B_minus_h_4_5": q(B - HUXLEY_AT_FOUR_FIFTHS),
            "h_over_B_max": q(ratio),
            "power_margin": "T <= x^(1/B-o(1)) gives T^h/x <= x^(-1/14+o(1)) on the Huxley range.",
            "vk_result": "At 1-s >= c(log T)^(-5/7), this power margin is exp(-c'(log x)^(2/7)); log^44 T is absorbed.",
        },
        "local_count_and_kernel": {
            "local_count": "CHJ-I Lemma plus1minus1lem: N(t+1)-N(t-1)<log t for t>1; a height-one strip is contained in such a length-two window.",
            "multiplicity_convention": "Ford p. 5 explicitly fixes that every summation over zeta zeros counts multiplicity; CHJ-I applies its N-bound to the same zero sums in its contour proof.",
            "pair_kernel": "For Re z >= 0, Re(1+z+conj rho)>=1. Partition gamma into unit strips about Im z; the local O(log T) count and harmonic sum over O(T) strips give O((log T)^2).",
            "source_crosscheck": "CHJ-II separately writes its Riemann--von Mangoldt zero sum over all non-trivial zeros and uses N(T), N(s,T) in its pair/zero-sum reduction.",
        },
        "ford_low_heights": {
            "low_height": "Platt--Trudgian rigorously verify beta=1/2 for every non-trivial zero with |gamma| <= 3*10^12.",
            "high_height": "Ford Theorem 5 applies for |t| >= 3 with the VK region.",
            "closure": "The low-height verification and Ford overlap, so no unhandled 0 < |gamma| < 3 range remains. Monotonicity of the Ford width transfers its cutoff to all 3 <= |gamma| <= T.",
        },
        "explicit_formula": {
            "published_source": "Cully-Hugill--Johnston, International Journal of Number Theory 19 (2023), 1205--1228, Theorem 1.2; frozen arXiv v5 source 2111.10001v5.",
            "statement": "For max{51,log x}<T<(x^alpha-2)/2, psi(x)=x-sum_{|gamma|<=T}x^rho/rho+O*(M x log x/T).",
            "GM_match": "Take alpha=1/2. GM's T=x/y*exp(2(log x)^(1/4)) is between log x and x^(1/2)/2 eventually; applying the theorem at x and x+y with the same T gives the interval formula and the stronger O(x log x/T) error.",
            "endpoint": "Subtracting psi(x+y)-psi(x) gives the half-open interval (x,x+y], compatible with GM's displayed prime sum after endpoint conventions are fixed.",
        },
    }


def source_rows() -> list[dict[str, Any]]:
    return [
        {"id": "SC-A1-explicit-formula-CHJ-I", "status": "PROVED", "locator": "CHJ-I (published 2023), Theorem 1.2; frozen arXiv v5 source", "closure": "Matches GM's selected height and is stronger by two log powers after endpoint subtraction."},
        {"id": "SC-A2-near-one-density-Huxley", "status": "PROVED", "locator": "Huxley (1972), (1.9), ledger HUX-1.9", "closure": "The log^44 two-sided bound covers s>=4/5 with h(s)<=15/7<30/13."},
        {"id": "SC-A3-VK-and-low-height", "status": "PROVED", "locator": "Ford (2002), Theorem 5; Platt--Trudgian (2021), Theorem 1", "closure": "Combining them closes the formerly omitted low-height range."},
        {"id": "SC-A5-local-zero-and-pair-kernel", "status": "PROVED", "locator": "CHJ-I Lemma plus1minus1lem and zero-sum proof; CHJ-II zero-sum cross-check; Ford p. 5 convention", "closure": "Multiplicity-inclusive O(log T) local count yields the O((log T)^2) kernel by elementary harmonic summation."},
        {"id": "SC-A5b-CHJ-II-scope", "status": "OBSERVED", "locator": "CHJ-II Theorem mainthm", "finding": "Its new O(x/T) theorem selects some T* in [T,2T], so it is not substituted for GM's fixed-height formula; CHJ-I is the fixed-height published input."},
    ]


def build_report() -> dict[str, Any]:
    check_sources()
    v1 = json.loads(V1.read_text(encoding="utf-8"))
    rows = source_rows()
    assert v1["exact_replay_sha256"] == "7aa44f69a585ea5b984ef027e8ace496ae1134e55e8a06b24ea51abbe509f729"
    return {
        "artifact_id": "cycle-2-stream-c-route-a-v2",
        "supersedes": {"artifact": "cycle-2-stream-c-route-a-v1", "exact_replay_sha256": v1["exact_replay_sha256"], "preservation": "v1 is retained unchanged"},
        "status": "PROVED: external-input closure for the published GM §13.2 deduction; no new theorem or exponent claimed",
        "claim_boundary": "This audits the stated ingredients and their compatibility. It does not independently reprove the Guth--Maynard zero-density theorem or claim any improvement below theta=17/30 and theta=2/15.",
        "sources": {path.name: digest for path, digest in HASHES.items()},
        "exact_closures": exact_closures(),
        "rows": rows,
        "open_blockers": [],
        "contained_finding": "CHJ-II's some-T* theorem cannot replace a prescribed truncation height; this is contained by using published CHJ-I Theorem 1.2 instead.",
        "result_labels": {"uniform_theta": "17/30", "almost_all_theta": "2/15", "uniform_conclusion": "PROVED deduction conditional only on GM's published zero-density theorem", "almost_all_conclusion": "PROVED deduction conditional only on GM's published zero-density theorem"},
        "pass_state": "PASS: v1 external-input blockers SC-A1, SC-A2, SC-A3 low-height scope, and SC-A5 are closed by pinned sources and explicit convention checks.",
    }


def main() -> None:
    started_ns = time.perf_counter_ns()
    script = Path(__file__).resolve()
    report = build_report()
    report["exact_replay_sha256"] = canonical_sha256(report)
    report["replay"] = {"script": str(script.relative_to(PROJECT)), "script_sha256": sha256(script), "python_implementation": platform.python_implementation(), "python_version": sys.version.split()[0], "wall_time_ns": time.perf_counter_ns() - started_ns}
    artifact = PROJECT / "artifacts/cycle-2-stream-c-route-a-v2.json"
    artifact.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(artifact)


if __name__ == "__main__":
    main()
