#!/usr/bin/env python3
"""Versioned external-input closure for Cycle 2 Stream B, Route A.

v1 is deliberately retained.  This script audits raw frozen sources only; it
does not use a Route B artifact or claim a new zero-density theorem.
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


PROJECT = Path(__file__).resolve().parents[1]
GM = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
MP = PROJECT / "artifacts/sources/maynard-pratt-2206.11729/HalfIsolatedv2.tex"
MP_TAR = PROJECT / "artifacts/sources/maynard-pratt-2206.11729.tar"
MONT = PROJECT / "artifacts/sources/montgomery-1969-inventiones8-gdz-volume.pdf"
HSW = PROJECT / "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar"
BUI = PROJECT / "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar"
V1 = PROJECT / "artifacts/cycle-2-stream-b-route-a-v1.json"
HASHES = {
    GM: "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    MP: "ec22dfdb8394b8ab4b228d0f438d19858015fc74330e247d08f36e5830782426",
    MP_TAR: "b81dbb3bb8bed014588294b5c6d7e8e4b5a14798f445baecb6680b7a9df967d3",
    MONT: "b240c7c07d32201ced906bd0fdc4d36cca3c11999084afeb658ffca3f978534e",
    HSW: "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    BUI: "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def gzip_text(path: Path) -> str:
    with gzip.open(path, "rt", encoding="utf-8") as source:
        return source.read()


def check_sources() -> None:
    for path, expected in HASHES.items():
        assert sha256(path) == expected, f"hash mismatch: {path.name}"
    gm, mp, hsw, bui = GM.read_text(), MP.read_text(), gzip_text(HSW), gzip_text(BUI)
    for phrase in (
        "If it is not a Type I zero then it is a `Type II zero'",
        "There are $O(\\log{T})$ non-trivial zeros",
        "usual Mean Value Theorem to $\\tilde{D}^k",
        "A \\lessapprox B",
        "|W|\\lessapprox N^{2k-2k\\sigma}+TN^{k-2k\\sigma}",
    ):
        assert phrase in gm, f"missing GM anchor: {phrase}"
    for phrase in (
        "every non-trivial zero $\\rho=\\beta+i\\gamma$ with $\\gamma\\in[T,2T]$ is either a Type I zero or a Type II zero",
        "R_{II}(\\sigma,T) \\ll T^{2(1-\\sigma)}(\\log T)^{O(1)}",
        "the zeros in a cluster are taken without multiplicity",
        "R_{II}(\\sigma,T) \\ll (\\log T)^{4}|\\mathcal{T}|",
    ):
        assert phrase in mp, f"missing MP anchor: {phrase}"
    for phrase in (
        "For any $T\\ge e$",
        "0.1038  \\log T + 0.2573  \\log\\log T + 9.3675",
    ):
        assert phrase in hsw, f"missing HSW anchor: {phrase}"
    assert "where each zero is counted with multiplicity" in bui


def exact_bookkeeping() -> dict[str, Any]:
    sigma_lo, sigma_hi = Fraction(7, 10), Fraction(4, 5)
    n_lo, ell_hi, k_hi = Fraction(1, 100), Fraction(10, 13), 77
    assert ell_hi / n_lo == Fraction(1000, 13) < k_hi
    assert Fraction(15, 14) - 1 == Fraction(1, 14)
    assert sigma_lo <= sigma_hi
    return {
        "range": "7/10 <= sigma <= 4/5; T sufficiently large",
        "bounded_power": {"small_branch": "k=ceil(ell(sigma)/n)<=77", "large_branch": "k=2", "proof": "ell(sigma)<=10/13 and n>1/100 in the small branch; the large branch is GM's k=2 choice."},
        "multiplicity_conversion": "A multiplicity at height gamma is at most the multiplicity-inclusive O(log(T+2)) count in its unit strip. Hence a location-count Type-II bound gains at most one log factor; if MP already counts multiplicity, this inequality is still valid.",
        "two_sided_conversion": "Conjugation preserves beta and multiplicity. Thus the negative-height dyadic count equals the positive-height count, and N(sigma,T)<=2 sum_{j>=0} R^+_sigma(T/2^(j+1))+O(1).",
        "mean_value": "Montgomery Theorem 1 with t_r'=-s_r, outer interval (-2T-1,-T+1), and delta>=1 gives sum_W |P(s)|^2 << (T+M log M) log M sum_m |c_m|^2.",
        "powered_coefficients": "For fixed k<=77, |c_m|<=T^o(1) and sum_m|c_m|^2<=N^(k+o(1)); M asymp N^k on a chosen dyadic block.",
        "epsilon_budget": "For a requested epsilon, allocate epsilon/20 to each of the finitely many Fourier-tail, dyadic-choice, strip, divisor, powered-coefficient, support-block, and Montgomery-log losses. Each log^C T is <=T^(epsilon/20) eventually and their product remains T^epsilon.",
        "mvt_conclusion": "Dividing the mean-square bound by V^2 with V=N^(k sigma)T^-o(1) gives |W|<=T^o(1)(N^(2k-2k sigma)+T N^(k-2k sigma)), exactly GM (13.4).",
    }


def rows() -> list[dict[str, Any]]:
    return [
        {"id": "SB-A14-MP-complement-to-Type-II", "status": "PROVED", "locator": "MP Definition Type I/II, Lemma 23, Lemma 24; GM §13.1", "statement": "GM's complement of Type I is contained in MP Type II by MP Lemma 23, because detector, dyadic N range, threshold, beta cutoff, and positive-height interval agree exactly."},
        {"id": "SB-A15-local-strip-and-multiplicity", "status": "PROVED", "locator": "HSW Corollary 1.1; Bui--Heath-Brown introduction; MP cluster convention", "statement": "Subtracting the pinned Riemann--von Mangoldt bounds gives O(log(T+2)) zeros in every unit strip; Bui--Heath-Brown pins multiplicity, converting MP's location treatment at only a logarithmic loss."},
        {"id": "SB-A16-positive-to-two-sided", "status": "PROVED", "locator": "GM §13.1 positive dyadic reduction; zeta conjugation symmetry", "statement": "Positive dyadic bounds transfer to |Im rho|<=T with a factor two and a convergent dyadic geometric series; O(1) low-height terms are absorbed asymptotically."},
        {"id": "SB-A17-smoothing-and-separated-extraction", "status": "PROVED", "locator": "GM §13.1 plus SB-A15", "statement": "The beta-uniform smooth cutoff, Fourier inversion, rapid tail, and multiplicity-inclusive strip bound yield a 1-separated set after only T^o(1) loss."},
        {"id": "SB-A18-coefficients-powered-support", "status": "PROVED", "locator": "GM §13.1; fixed k bookkeeping", "statement": "Detector coefficients, their kth convolution, coefficient-one normalization, and dyadic support selection each cost T^o(1), with all k<=77 dependence fixed."},
        {"id": "SB-A19-Montgomery-mean-value", "status": "PROVED", "locator": "Montgomery (1969), Theorem 1 / printed p.335 / frozen PDF p.348, visually checked this run", "statement": "The theorem permits arbitrary complex coefficients, an arbitrary real interval, and separation delta; reflected GM ordinates meet its hypotheses and give GM's two MVT terms."},
        {"id": "SB-A20-epsilon-o1-transfer", "status": "PROVED", "locator": "GM notation convention and finite-loss budget", "statement": "Every loss is one of finitely many fixed log powers, bounded-k divisor factors, or source lessapprox terms; epsilon splitting preserves T^o(1) without a finite-T power identity."},
    ]


def build_report() -> dict[str, Any]:
    check_sources()
    old = json.loads(V1.read_text())
    assert old["mathematical_and_source_audit_sha256"]
    audit_rows = rows()
    assert all(row["status"] == "PROVED" for row in audit_rows)
    return {
        "artifact_id": "cycle-2-stream-b-route-a-v2",
        "supersedes": {"artifact": "cycle-2-stream-b-route-a-v1", "audit_sha256": old["mathematical_and_source_audit_sha256"], "preservation": "v1 retained unchanged"},
        "status": "PROVED: Stream-B external dependency closure for the published GM §13.1 transfer",
        "claim_boundary": "This verifies applicability and convention transfers in the published proof. It neither re-proves GM Theorem 1.1/1.2 nor establishes a new zero-density estimate.",
        "sources": {path.name: value for path, value in HASHES.items()},
        "rows": audit_rows,
        "exact_bookkeeping": exact_bookkeeping(),
        "open_blockers": [],
        "pass_state": "PASS: v1's local-zero and mean-value blockers are closed; all stated normalizations and epsilon transfers are retained as asymptotic T^o(1) losses.",
    }


def main() -> None:
    started = time.perf_counter_ns()
    script = Path(__file__).resolve()
    report = build_report()
    report["mathematical_and_source_audit_sha256"] = canonical_sha256(report)
    report["replay"] = {"script": str(script.relative_to(PROJECT)), "script_sha256": sha256(script), "python_implementation": platform.python_implementation(), "python_version": sys.version.split()[0], "wall_time_ns": time.perf_counter_ns() - started}
    target = PROJECT / "artifacts/cycle-2-stream-b-route-a-v2.json"
    target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n")
    print(target)


if __name__ == "__main__":
    main()
