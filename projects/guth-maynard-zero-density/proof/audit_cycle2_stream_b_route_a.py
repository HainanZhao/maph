#!/usr/bin/env python3
"""Source-level Stream B Route A audit for Guth--Maynard §13.1.

The output distinguishes direct exact transfers from steps that still depend
on an unpinned external input.  It is not a reproof of Theorem 1.2.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
import time
from fractions import Fraction
from pathlib import Path
from typing import Any


VERSION = 1
ROUTE = "A"
STREAM = "B"
TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE = Path(__file__).resolve().parents[1] / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def require_source_declarations(tex: str) -> None:
    """Pin the exact §13.1 declarations used by this audit."""
    required = (
        "b_n&:=\\Bigl(\\sum_{\\substack{d|n\\\\ d\\le 2T^{1/100}}}\\mu(d)\\Bigr)",
        "is called a `Type I zero'",
        "Type II zero', and the number of Type II zeros is $\\le T^{2-2\\sigma}",
        "let $\\psi(u)$ be a smooth function equal to $e^{u(\\sigma-\\beta)}$",
        "D(\\rho)=\\sum_{n\\sim N}b_n n^{-\\sigma-i\\gamma}\\psi(\\log{n})",
        "Since $\\widehat{\\psi}$ is rapidly decreasing",
        "There are $O(\\log{T})$ non-trivial zeros",
        "\\tilde{b}_n:=\\Bigl(\\frac{N}{n}\\Bigr)^\\sigma b_n",
        "Theorem \\ref{thrm:LargeValues} to the Dirichlet polynomial $\\tilde{D}^k$",
        "usual Mean Value Theorem to $\\tilde{D}^k",
    )
    for phrase in required:
        assert phrase in tex, f"frozen source declaration missing: {phrase}"


def audit_rows() -> list[dict[str, Any]]:
    """List every preregistered Stream B transfer and its evidence status."""
    sigma_min = Fraction(7, 10)
    sigma_max = Fraction(4, 5)
    n_min = Fraction(1, 100)
    l_max = Fraction(10, 13)
    k_max = 77

    # Exact arithmetic controlling the bounded-k and interval repairs.
    assert l_max / n_min == Fraction(1000, 13) < k_max
    assert Fraction(15, 14) - 1 == Fraction(1, 14)
    assert sigma_min <= sigma_max < 1

    return [
        {
            "id": "SB-A1-smoothing-identity",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2319--2329",
            "hypotheses_checked": [
                "rho=beta+i gamma is Type I with beta>=sigma",
                "psi(u)=exp(u(sigma-beta)) on [log N,log 2N]",
                "n is in the detector support n~N",
            ],
            "exact_transfer": "n^(-beta-i gamma)=n^(-sigma-i gamma)psi(log n), hence the displayed Fourier identity has the required integrand.",
            "loss": "none in the pointwise algebra",
        },
        {
            "id": "SB-A2-uniform-smooth-cutoff-and-fourier-tail",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2320--2331; notation at lines 288--290",
            "hypotheses_checked": [
                "nontrivial zeta zero has sigma<=beta<=1",
                "a=beta-sigma is nonnegative and bounded",
                "a smooth cutoff eta(u/log N) is supported in [log N/2,2 log N] and equals one on [log N,log 2N]",
            ],
            "exact_transfer": "For u>0, sup_(a>=0) a^j exp(-a u)=(j/u)^j exp(-j) for j>=1. Leibniz with the scaled cutoff gives ||psi^(j)||_infinity <<_j (log N)^(-j), uniformly in beta. Repeated integration by parts yields a rapidly decaying Fourier tail.",
            "loss": "||hat(psi)||_1=O(log N); truncating at |xi|<=T^epsilon with sufficiently many integrations by parts costs O(T^-100), for each fixed epsilon>0.",
            "falsifier": "Failure of beta<=1 or of the stated cutoff derivative bounds would invalidate the uniform tail claim.",
        },
        {
            "id": "SB-A3-type-I-threshold-after-fourier",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2315--2331",
            "hypotheses_checked": [
                "Type-I input |D(rho)|>=1/(3 log T)",
                "SB-A2 L1 Fourier bound and O(T^-100) tail",
            ],
            "exact_transfer": "The triangle inequality for the truncated Fourier integral gives some t=gamma-2pi xi with |D(sigma+i t)| >= T^(-o(1)).",
            "loss": "the Type-I 1/log T threshold and ||hat(psi)||_1=O(log N) combine to T^(-o(1)); this is not replaced by a fixed positive constant.",
        },
        {
            "id": "SB-A4-local-zero-count-and-separated-extraction",
            "status": "OBSERVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2331--2337",
            "hypotheses_checked": [
                "GM explicitly states O(log T) nontrivial zeros in each unit horizontal strip",
                "the primary local zero-count theorem, its multiplicity convention, and its uniformity have not yet been pinned",
            ],
            "conditional_transfer": "Given the stated unit-strip estimate, a maximal 1-separated subset loses at most T^epsilon(log T) points per selected value because the Fourier shift has |xi|<=T^epsilon. Thus R is at least the dyadic Type-I count times T^(-o(1)).",
            "loss": "T^epsilon log T, absorbed only in the source's lessapprox/T^o(1) notation.",
            "blocker": "Full analytic G0 remains blocked until a primary source for the local zero count is pinned and checked.",
            "falsifier": "A local multiplicity-inclusive zero count larger than T^c for a fixed c>0 would destroy the claimed T^o(1) extraction loss.",
        },
        {
            "id": "SB-A5-height-interval-translation",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2329--2337; Theorem 1.1, TeX lines 68--81",
            "hypotheses_checked": [
                "gamma in [T,2T]",
                "Fourier truncation |xi|<=T^epsilon",
                "Theorem 1.1 permits a 1-separated set in an interval [0,H]",
            ],
            "exact_transfer": "Selected heights lie in [T-O(T^epsilon),2T+O(T^epsilon)], an interval of length H<=2T for large T. Translation t=t0+u replaces each coefficient a_n by a_n n^(i t0), preserving its modulus and every large-value modulus.",
            "loss": "Replacing H by a constant multiple of T changes only constants and T^o(1), not a finite-T power identity.",
        },
        {
            "id": "SB-A6-dyadic-detector-choice",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2315--2319",
            "hypotheses_checked": ["there are O(log T) dyadic choices of N in the Type-I definition"],
            "exact_transfer": "Pigeonhole selects one N supporting at least an O(1/log T) proportion of Type-I zeros.",
            "loss": "O(log T)=T^o(1)",
        },
        {
            "id": "SB-A7-original-detector-coefficients",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2310--2318 and 2334--2337",
            "hypotheses_checked": [
                "N>=T^(1/100); for N<T^(1/100) every divisor of n~N is included and sum_(d|n)mu(d)=0",
                "|sum_(d|n,d<=2T^(1/100)) mu(d)|<=tau(n)",
                "the elementary fixed-order divisor bound tau(n)=n^o(1), uniformly for n<=T^O(1)",
                "(N/n)^sigma<=1 on n in [N,2N]",
            ],
            "exact_transfer": "|tilde b_n|<=tau(n)=T^o(1); after a T^o(1) normalization the original detector has coefficient sup norm at most one.",
            "loss": "T^o(1), retained explicitly; no fixed finite-T coefficient-one claim is made before normalization.",
        },
        {
            "id": "SB-A8-bounded-k-small-regime",
            "status": "PROVED",
            "scope": "small-n regime",
            "locator": "GM §13.1, TeX lines 2339--2345; Cycle-1 case-split v4",
            "hypotheses_checked": ["n>1/100", "n<=5/(6+10sigma)", "7/10<=sigma<=4/5"],
            "exact_transfer": "k=ceil(l(sigma)/n) obeys k<=77 because l(sigma)<=10/13 and n>1/100. Hence every k-dependent divisor and dyadic loss remains T^o(1).",
            "loss": "bounded constants depending on k<=77, hence T^o(1)",
        },
        {
            "id": "SB-A9-bounded-k-large-regime",
            "status": "PROVED",
            "scope": "large-n regime",
            "locator": "GM §13.1, TeX lines 2342--2345; Cycle-1 case-split v4",
            "hypotheses_checked": ["n>5/(6+10sigma)", "N<=T^(1/2)(log T)^2", "u(sigma)>=15/14"],
            "exact_transfer": "k=2. Thus q=2n>l(sigma), while q<=1+o(1)<=u(sigma)+o(1). The uniform 1/14 gap is retained rather than turned into a finite-T equality.",
            "loss": "the (log T)^2 upper range is an explicit o(1) in q", 
        },
        {
            "id": "SB-A10-powered-coefficients-and-normalization",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "GM §13.1, TeX lines 2349--2358; Theorem 1.1 coefficient hypothesis at lines 68--81",
            "hypotheses_checked": [
                "k<=77 from SB-A8/SB-A9",
                "each original tilde coefficient is T^o(1)",
                "a coefficient of tilde D^k is a sum over at most d_k(m) factorizations, with d_k(m)=m^o(1) for fixed k",
                "m<=T^O(1) on the chosen k window",
            ],
            "exact_transfer": "Every coefficient of tilde D^k is T^o(1). Divide the powered polynomial by its coefficient sup norm to meet Theorem 1.1's |b_m|<=1 hypothesis; the value threshold is multiplied by T^(-o(1)).",
            "loss": "T^o(1) normalization, retained in V=L^sigma T^(-o(1)).",
            "falsifier": "An unbounded k or a coefficient convolution larger than T^o(1) would invalidate this normalization step.",
        },
        {
            "id": "SB-A11-support-dyadic-decomposition-and-threshold-transfer",
            "status": "PROVED",
            "scope": "both k regimes",
            "locator": "implicit application of Theorem 1.1 at GM §13.1 lines 2349--2358",
            "hypotheses_checked": [
                "supp(tilde D^k) is contained in [L,2^k L], L=N^k",
                "k<=77",
                "Theorem 1.1 is stated for one block [M,2M]",
            ],
            "exact_transfer": "Partition [L,2^kL] into O(k) dyadic blocks. If the powered sum is >=L^sigma T^(-o(1)), one block is >=L^sigma T^(-o(1))/O(k). Pigeonhole one fixed block over W. Since M/L is bounded by 2^k, this is M^sigma T^(-o(1)).",
            "loss": "O(k) block count and constant comparability 2^k, both T^o(1).",
            "falsifier": "If k were not uniformly bounded, either the block count or M/L comparability could create a non-o(1) loss.",
        },
        {
            "id": "SB-A12-theorem-1-1-hypotheses-after-transfer",
            "status": "PROVED",
            "scope": "q<=alpha regime",
            "locator": "GM Theorem 1.1, TeX lines 68--81; GM §13.1 lines 2349--2358",
            "hypotheses_checked": [
                "normalized single dyadic block has coefficient sup norm <=1",
                "extracted subset is 1-separated",
                "SB-A5 translates it into [0,H] with H=O(T)",
                "transferred threshold is V=M^sigma T^(-o(1))",
            ],
            "exact_transfer": "All displayed Theorem 1.1 hypotheses are met after the stated normalizations, conditional only on SB-A4's unpinned local-zero-count extraction.",
            "loss": "all prior log, divisor, block, and interval losses are T^o(1).",
            "blocker": "Conditional on SB-A4; no new blocker is introduced by the Theorem 1.1 application itself.",
        },
        {
            "id": "SB-A13-mean-value-branch-hypotheses",
            "status": "OBSERVED",
            "scope": "q>alpha regime",
            "locator": "GM §13.1, TeX lines 2353--2364",
            "hypotheses_checked": [
                "the same normalized, dyadic, 1-separated polynomial preparation as SB-A10--SB-A11",
                "GM calls the external input the 'usual Mean Value Theorem' without a locator",
            ],
            "conditional_transfer": "The prepared polynomial has the standard bounded-coefficient and separation hypotheses expected for a mean-square large-values estimate, but the exact theorem, support convention, and uniform T^o(1) treatment remain unpinned.",
            "loss": "not promotable until a precise mean-value theorem is frozen.",
            "blocker": "Full analytic G0 remains blocked on the q>alpha branch.",
            "falsifier": "A pinned mean-value theorem with incompatible support, coefficient, or separation hypotheses would invalidate this branch.",
        },
    ]


def build_report() -> dict[str, Any]:
    tex = SOURCE.read_text(encoding="utf-8")
    assert sha256(SOURCE) == TEX_SHA256
    require_source_declarations(tex)
    rows = audit_rows()
    blockers = [row["id"] for row in rows if row["status"] != "PROVED"]
    assert blockers == ["SB-A4-local-zero-count-and-separated-extraction", "SB-A13-mean-value-branch-hypotheses"]
    return {
        "artifact_id": "cycle-2-stream-b-route-a-v1",
        "route": ROUTE,
        "stream": STREAM,
        "status": "OBSERVED: partial source-level audit; two external-input blockers remain",
        "claim_boundary": "No new zero-density theorem or independent proof of Guth--Maynard Theorem 1.2 is claimed.",
        "frozen_source": {
            "arxiv": "2405.20552v2",
            "tex_path": str(SOURCE.relative_to(SOURCE.parents[3])),
            "tex_sha256": TEX_SHA256,
            "notation_locator": "TeX lines 288--290: lessapprox permits T^epsilon for every fixed epsilon and o(1) is T->infinity",
        },
        "rows": rows,
        "blockers": blockers,
        "pass_state": "NOT PASS: local zero count and mean-value theorem still require pinned primary sources.",
    }


def main() -> None:
    started_ns = time.perf_counter_ns()
    script = Path(__file__).resolve()
    project = script.parent.parent
    report = build_report()
    report["mathematical_and_source_audit_sha256"] = canonical_sha256(report)
    report["replay"] = {
        "script": str(script.relative_to(project)),
        "script_sha256": sha256(script),
        "python_implementation": platform.python_implementation(),
        "python_version": sys.version.split()[0],
        "wall_time_ns": time.perf_counter_ns() - started_ns,
    }
    artifact = project / "artifacts" / "cycle-2-stream-b-route-a-v1.json"
    artifact.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(artifact)


if __name__ == "__main__":
    main()
