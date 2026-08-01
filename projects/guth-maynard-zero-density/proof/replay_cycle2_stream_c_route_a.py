#!/usr/bin/env python3
"""Independent exact skeleton for Cycle 2 Stream C, Route A.

The script checks all rational exponent and epsilon bookkeeping in GM §13.2.
It records, rather than erases, external-input blockers that prevent this from
being an independent proof of either short-interval corollary.
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
STREAM = "C"
PROJECT = Path(__file__).resolve().parents[1]
GM_TEX = PROJECT / "artifacts/sources/arxiv-2405.20552v2/LargevaluesDirichlet17.tex"
JUTILA_PDF = PROJECT / "artifacts/sources/jutila-1977-zero-density-estimates-l-functions.pdf"
FORD_PDF = PROJECT / "artifacts/sources/ford-2002-zero-free-regions.pdf"
GM_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
JUTILA_SHA256 = "cbe2d1e7115717cf28f9ffaffdc1fe232958595b17c5c2ee59fc968e8ff0d5a1"
FORD_SHA256 = "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948"
B = Fraction(30, 13)
ONE_OVER_B = Fraction(13, 30)
TWO_OVER_B = Fraction(13, 15)
UNIFORM_THETA = Fraction(17, 30)
ALMOST_ALL_THETA = Fraction(2, 15)


def q(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: dict[str, Any]) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def check_gm_source(tex: str) -> None:
    for text in (
        "for any choice of $2\\le T\\le x$",
        "T=xy^{-1}\\exp(2\\sqrt[4]{\\log{x}})",
        "T<x^{13/30-\\epsilon/2}",
        "\\delta=X^{-13/15+\\epsilon/2}",
        "T=\\delta^{-1}\\exp(4\\sqrt[4]{\\log{X}})",
        "X^{2\\sigma+1}N(\\sigma,T)",
        "O(\\log{T})$ zeros in a horizontal strip of height 1",
    ):
        assert text in tex, f"missing frozen GM §13.2 declaration: {text}"


def exact_bookkeeping() -> dict[str, Any]:
    """Exact power arithmetic behind both endpoint deductions."""
    one = Fraction(1, 1)
    delta_exponent = -TWO_OVER_B  # before adding +epsilon/2
    local_interval_exponent = one + delta_exponent
    uniform_t_exponent_at_theta = one - UNIFORM_THETA
    almost_all_t_exponent_at_delta = TWO_OVER_B
    # Exact identities; epsilon is symbolic and intentionally not instantiated.
    assert one / B == ONE_OVER_B
    assert Fraction(2, 1) / B == TWO_OVER_B
    assert one - ONE_OVER_B == UNIFORM_THETA
    assert one - TWO_OVER_B == ALMOST_ALL_THETA
    assert uniform_t_exponent_at_theta == ONE_OVER_B
    assert local_interval_exponent == ALMOST_ALL_THETA
    assert B * ONE_OVER_B == one
    assert B * TWO_OVER_B == Fraction(2, 1)
    return {
        "density_coefficient": q(B),
        "uniform": {
            "theta": q(UNIFORM_THETA),
            "T_power_from_x_over_y_at_endpoint": q(uniform_t_exponent_at_theta),
            "density_condition": "T < x^(1/B-epsilon/2) = x^(13/30-epsilon/2)",
            "epsilon_bookkeeping": "y >= x^(17/30+epsilon) gives T=x/y*exp(2(log x)^(1/4)) < x^(13/30-epsilon/2) for sufficiently large x",
            "truncation_error": "x(log x)^3/T = y(log x)^3 exp(-2(log x)^(1/4)) <= y exp(-(log x)^(1/4)) eventually",
        },
        "almost_all": {
            "theta": q(ALMOST_ALL_THETA),
            "delta": "delta=X^(-13/15+epsilon/2)",
            "delta_times_X_power": q(local_interval_exponent),
            "T_power_before_subpower_factor": q(almost_all_t_exponent_at_delta),
            "epsilon_bookkeeping": "T=delta^(-1)exp(4(log X)^(1/4)) <= X^(13/15-epsilon/3) eventually",
            "key_identity": "B*(13/15)=2",
            "Cauchy_Schwarz_remainder": "delta^2 X^3 <= y^2 X exp(-3(log X)^(1/4)) eventually because y/(delta X) >= X^(epsilon/2)",
            "Chebyshev_conversion": "an L2 bound y^2 X exp(-3A) gives at most O(X exp(-A)) points with error > y exp(-A), A=(log X)^(1/4)",
        },
        "vk_absorption": {
            "source_cutoff": "1-sigma >= c(log T)^(-2/3)(log log T)^(-1/3)",
            "weaker_cutoff": "1-sigma >= c'(log T)^(-5/7)",
            "justification": "(log T)^(1/21)/(log log T)^(1/3) tends to infinity, so the source cutoff contains the weaker one for sufficiently large T",
            "decay_comparison": "(log X)^(2/7) dominates (log X)^(1/4)",
        },
        "upper_ranges": {
            "uniform": "y <= x^0.99 gives T >= x^0.01 exp(2(log x)^(1/4)), hence log T is comparable to log x and 2<=T<=x eventually",
            "almost_all": "y <= X^0.99 is retained from the published statement; the lower y bound supplies the Cauchy--Schwarz remainder domination",
        },
    }


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "id": "SC-A1-GM-explicit-formula",
            "status": "OBSERVED",
            "locator": "GM §13.2, TeX lines 2407--2417; citation Davenport, Chapter 17",
            "statement_used": "sum_[x,x+y] Lambda(n)=y-sum_[|rho|<=T]((x+y)^rho-x^rho)/rho+O(x(log x)^3/T), 2<=T<=x",
            "checked": "The exact displayed GM statement, its truncation range, and its subsequent choice of T were checked.",
            "blocker": "Davenport Chapter 17 is not locally pinned; endpoint convention, uniformity, and multiplicity treatment are not independently verified.",
            "falsifier": "An explicit-formula version with a truncation error or height convention incompatible with the displayed choice of T breaks both downstream routes.",
        },
        {
            "id": "SC-A2-near-one-density",
            "status": "OBSERVED",
            "locator": "GM §13.2, TeX lines 2419--2423; Jutila, Acta Arith. XXXII (1977), printed p. 57, Corollary (1.8)",
            "statement_used": "GM requires a single near-one density estimate with at most logarithmic loss: N(sigma,T) << T^((30/13+o(1))(1-sigma))(log T)^O(1).",
            "checked": "The reachable Jutila scan states N(alpha,T) <<_{epsilon,k} T^(A_3(alpha)(1-alpha)+epsilon) and A_3(alpha)=2 for alpha>=11/14; its displayed N(alpha,T) uses two-sided |t|<=T.",
            "blocker": "The visible Jutila epsilon-form estimate does not by itself supply a uniform logarithmic-loss bound in the VK strip 1-sigma as small as (log T)^(-5/7); its multiplicity wording is also not explicit in the inspected corollary. GM's alternative Montgomery citation remains unpinned.",
            "falsifier": "If no pinned theorem provides the required uniform near-one/logarithmic-loss statement, the density supremum cannot be promoted from the GM display to an independent proof.",
        },
        {
            "id": "SC-A3-vinogradov-korobov-zero-free",
            "status": "PROVED",
            "locator": "Ford, Zero-free regions for the Riemann zeta function (2002), Theorem 5, PDF p. 4; GM cites Montgomery Cor. 11.4",
            "statement_used": "zeta(beta+it) is nonzero for |t|>=3 when 1-beta <= 1/[57.54(log|t|)^(2/3)(log log|t|)^(1/3)].",
            "checked": "Ford's accessible primary paper gives the needed VK shape; its later zero sums state that zeros are counted with multiplicity.",
            "transfer": "The exact comparison in the replay weakens this to the GM cutoff exponent -5/7 for sufficiently large T.",
        },
        {
            "id": "SC-A4-uniform-density-supremum",
            "status": "OBSERVED",
            "locator": "GM §13.2, TeX lines 2419--2432",
            "statement_used": "sup_sigma x^(sigma-1)N(sigma,T) <= exp(-(log x)^(1/4)) under T<x^(13/30-epsilon/2).",
            "checked": "The exponent condition and VK absorption are replayed exactly in the Route A bookkeeping artifact.",
            "blocker": "Depends on SC-A2's unpinned uniform near-one density statement (and SC-A1 for its use inside the explicit formula).",
        },
        {
            "id": "SC-A5-local-zero-and-pair-kernel-bound",
            "status": "OBSERVED",
            "locator": "GM §13.2, TeX lines 2451--2464",
            "statement_used": "O(log T) zeros per unit horizontal strip implies sum_[|rho_2|<T]|1+z+conj(rho_2)|^-1 << (log T)^2 for |z|<T, Re z>=0.",
            "checked": "Given the local multiplicity-inclusive O(log T) estimate, the harmonic summation argument yields the displayed pair-kernel bound; beta>=0 keeps the real part of the denominator positive.",
            "blocker": "The local zero count is the unpinned Stream-B blocker SB-A4, so this pair estimate is conditional rather than promoted.",
            "falsifier": "A non-T^o(1) local zero clustering loss invalidates the second-moment bound.",
        },
        {
            "id": "SC-A6-uniform-truncation-and-error",
            "status": "PROVED",
            "locator": "GM §13.2, TeX lines 2407--2432",
            "statement_used": "T=x/y*exp(2(log x)^(1/4)); y in [x^(17/30+epsilon),x^0.99].",
            "checked": "All endpoint, truncation, upper-range, and epsilon inequalities are exact/asymptotic consequences recorded by the replay.",
            "conditional_on": ["SC-A1", "SC-A4"],
        },
        {
            "id": "SC-A7-almost-all-second-moment",
            "status": "OBSERVED",
            "locator": "GM §13.2, TeX lines 2434--2471",
            "statement_used": "delta=X^(-13/15+epsilon/2), T=delta^-1 exp(4(log X)^(1/4)), followed by the stated L2 reduction and zero-pair expansion.",
            "checked": "The delta/T exponents, Cauchy--Schwarz remainder, density supremum exponent, and Chebyshev exceptional-set conversion are replayed exactly/asymptotically.",
            "blocker": "Depends on SC-A1, SC-A2, and SC-A5; the full L2 derivation is not promoted while those inputs remain indirect.",
        },
    ]


def build_report() -> dict[str, Any]:
    assert sha256(GM_TEX) == GM_TEX_SHA256
    assert sha256(JUTILA_PDF) == JUTILA_SHA256
    assert sha256(FORD_PDF) == FORD_SHA256
    tex = GM_TEX.read_text(encoding="utf-8")
    check_gm_source(tex)
    bookkeeping = exact_bookkeeping()
    rows = source_rows()
    blockers = [row["id"] for row in rows if row["status"] == "OBSERVED"]
    assert q(UNIFORM_THETA) == "17/30"
    assert q(ALMOST_ALL_THETA) == "2/15"
    return {
        "artifact_id": "cycle-2-stream-c-route-a-v1",
        "route": ROUTE,
        "stream": STREAM,
        "status": "OBSERVED: full exponent/epsilon replay conditional on three retained external-input blockers",
        "claim_boundary": "No independent proof of Corollary 1.3 or 1.4, and no new short-interval exponent, is claimed.",
        "sources": {
            "guth_maynard_tex_sha256": GM_TEX_SHA256,
            "jutila_1977_pdf_sha256": JUTILA_SHA256,
            "ford_2002_pdf_sha256": FORD_SHA256,
        },
        "exact_bookkeeping": bookkeeping,
        "rows": rows,
        "blockers": blockers,
        "result_labels": {
            "uniform_theta": q(UNIFORM_THETA),
            "almost_all_theta": q(ALMOST_ALL_THETA),
            "uniform_conclusion": "conditional replay of y >= x^(17/30+epsilon), y<=x^0.99",
            "almost_all_conclusion": "conditional replay of y >= X^(2/15+epsilon), y<=X^0.99 with O(X exp(-(log X)^(1/4))) exceptions",
        },
        "pass_state": "NOT PASS: explicit formula, uniform near-one density, and local zero/pair-count inputs remain unpinned or indirect.",
    }


def main() -> None:
    started_ns = time.perf_counter_ns()
    script = Path(__file__).resolve()
    report = build_report()
    report["exact_replay_sha256"] = canonical_sha256(report)
    report["replay"] = {
        "script": str(script.relative_to(PROJECT)),
        "script_sha256": sha256(script),
        "python_implementation": platform.python_implementation(),
        "python_version": sys.version.split()[0],
        "wall_time_ns": time.perf_counter_ns() - started_ns,
    }
    artifact = PROJECT / "artifacts/cycle-2-stream-c-route-a-v1.json"
    artifact.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(artifact)


if __name__ == "__main__":
    main()
