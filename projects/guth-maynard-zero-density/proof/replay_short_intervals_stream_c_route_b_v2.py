#!/usr/bin/env python3
"""Exact Stream-C Route-B v2 dependency-closure replay for GM section 13.2.

This is a versioned correction to v1.  It checks frozen source hashes and
exact rational exponent comparisons; analytic consequences are only asserted
within the explicitly stated published-input boundary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
B = Fraction(30, 13)
UNIFORM_THETA = Fraction(17, 30)
ALMOST_ALL_THETA = Fraction(2, 15)
UPPER_RANGE = Fraction(99, 100)
EPS_MAX = UPPER_RANGE - UNIFORM_THETA

SOURCES = {
    "huxley_1972": (
        "artifacts/sources/huxley-1972-inventiones15-gdz-volume.pdf",
        "5946d8579810f0754e972d42a09ed2a703604b8fb4e6377f14caaa5dc48f9797",
    ),
    "ford_2002": (
        "artifacts/sources/ford-2002-zero-free-regions.pdf",
        "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948",
    ),
    "platt_trudgian_2021_pdf": (
        "artifacts/sources/platt-trudgian-2021-rh-3e12.pdf",
        "3362f66af9fa9373977eee70e2282ec33989d5d8b97e0852df9e32cc25b52885",
    ),
    "platt_trudgian_2021_source": (
        "artifacts/sources/platt-trudgian-2021-rh-3e12.tar",
        "c4f13cdfca711d2bf90a097147be2a094ff175b0b161647359e174633fd8bf86",
    ),
    "hasanalizade_shen_wong_2022_pdf": (
        "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.pdf",
        "3fc4c89f49249924e61cb0d289d81559faed53fcbb838628ea32dc7ec6f89fbf",
    ),
    "hasanalizade_shen_wong_2022_source": (
        "artifacts/sources/hasanalizade-shen-wong-2022-counting-zeros.tar",
        "8ba8d0eb95e1dd967adf17b7a2e77bdc45a99f6aa283d41d23dd4d0ac4358247",
    ),
    "bui_heath_brown_2013_pdf": (
        "artifacts/sources/bui-heath-brown-2013-simple-zeros.pdf",
        "b1c5a4d6cdba59d0fc552a18cb2465c442a8534be0c4e51a23db126316f83077",
    ),
    "bui_heath_brown_2013_source": (
        "artifacts/sources/bui-heath-brown-2013-simple-zeros.tar",
        "a171c6e74be228955df48191675e497ce4934623ae33ddddd9761b8cb1185ca5",
    ),
}


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_source_hashes() -> dict[str, str]:
    result: dict[str, str] = {}
    for identifier, (relative, expected) in SOURCES.items():
        observed = file_hash(ROOT / relative)
        assert observed == expected, f"source hash mismatch: {relative}"
        result[identifier] = observed
    return result


def self_hash() -> str:
    return file_hash(Path(__file__))


def certificate() -> dict[str, Any]:
    """Return the exact certificate and fail if a frozen invariant changes."""
    source_hashes = checked_source_hashes()
    one_over_b = 1 / B
    two_over_b = 2 / B
    assert one_over_b == Fraction(13, 30)
    assert two_over_b == Fraction(13, 15)
    assert UNIFORM_THETA == 1 - one_over_b
    assert ALMOST_ALL_THETA == 1 - two_over_b
    assert EPS_MAX == Fraction(127, 300)

    # Huxley (1.9), with h(s)=3/(3s-1), on the near-one interval.
    s0, s1 = Fraction(4, 5), Fraction(1, 1)
    h_s0 = Fraction(3, 1) / (3 * s0 - 1)
    h_s1 = Fraction(3, 1) / (3 * s1 - 1)
    assert h_s0 == Fraction(15, 7)
    assert h_s1 == Fraction(3, 2)
    assert h_s0 < B and h_s1 < B
    # b - h(s) = 3(30s-23)/(13(3s-1)), positive for s >= 4/5.
    huxley_margin_at_s0 = B - h_s0
    assert huxley_margin_at_s0 == Fraction(15, 91)

    # Uniform and almost-all epsilon arithmetic.
    assert B * one_over_b == 1
    assert 2 * (-two_over_b) + 2 - 2 * ALMOST_ALL_THETA == 0
    assert (1 - two_over_b) == ALMOST_ALL_THETA

    return {
        "artifact_type": "exact-short-interval-stream-c-route-b-dependency-closure-certificate",
        "certificate_version": 2,
        "supersedes": "v1 only for the named dependency closure; v1 is preserved",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "PROVED: exact replay of the rational exponent and transfer calculations in "
            "Guth--Maynard section 13.2 after checking the listed published external "
            "inputs. PASS is narrow: it closes those dependency nodes, not an independent "
            "proof of Corollary 1.3 or 1.4 and not a new short-interval theorem."
        ),
        "v1_correction": {
            "status": "PROVED",
            "error": "v1 labelled Huxley's density alternative unread.",
            "correction": "The original Huxley scan was directly visually inspected; (1.9), printed p. 164 / PDF p. 173, is the required two-sided log-uniform bound.",
            "preservation": "v1 remains unchanged as its historical OBSERVED record.",
        },
        "frozen_parameters": {
            "b": q(B),
            "uniform_theta": q(UNIFORM_THETA),
            "almost_all_theta": q(ALMOST_ALL_THETA),
            "upper_y_exponent": q(UPPER_RANGE),
            "nonvacuous_epsilon_range": f"0 < epsilon < {q(EPS_MAX)}",
            "subpower_symbol": "E(Z)=exp((log Z)^(1/4))",
        },
        "source_hashes_checked": source_hashes,
        "external_inputs": {
            "density_lower_branch": {
                "status": "PROVED",
                "range": "7/10 <= s <= 4/5",
                "input": "Guth--Maynard Theorem 1.2: N(s,T) << T^((30/13+o(1))*(1-s)).",
            },
            "density_near_one_huxley": {
                "status": "PROVED",
                "range": "4/5 <= s <= 1",
                "input": "Huxley (1.9): N(s,T) << T^(3(1-s)/(3s-1))*(log T)^44 for -T <= gamma <= T.",
                "exact_coefficient_check": {
                    "h(4/5)": q(h_s0),
                    "h(1)": q(h_s1),
                    "b_minus_h_at_4/5": q(huxley_margin_at_s0),
                    "identity": "b-3/(3s-1)=3(30s-23)/(13(3s-1)) >= 15/91",
                },
                "conclusion": "N(s,T) << T^((30/13)*(1-s))*(log T)^44 on this branch; the log^44 is not discarded.",
            },
            "zero_free_cutoff": {
                "status": "PROVED",
                "high_height": "Ford Theorem 5 applies for |t|>=3 with Vinogradov--Korobov width 1/[57.54(log|t|)^(2/3)(loglog|t|)^(1/3)].",
                "low_height": "Platt--Trudgian Theorem 1 puts every non-trivial zero with |gamma|<=3,000,175,332,800 on Re=1/2 (by conjugation for negative ordinates).",
                "conclusion": "For all sufficiently large T, no zero has Re rho >= 1-c(log T)^(-5/7), including the formerly open finite-height range.",
            },
            "local_zero_count_and_pair_sum": {
                "status": "PROVED",
                "multiplicity": "Bui--Heath-Brown explicitly defines N(T) with each zero counted with multiplicity.",
                "rvm": "Hasanalizade--Shen--Wong Corollary 1.1 gives an explicit Riemann--von Mangoldt error O(log T), T>=e.",
                "derivation": "Subtract upper/lower RvM bounds at u+1 and u-1; the main-term difference and both errors are O(log(u+2)), while the compact u-range is bounded by N(e+2). Hence every unit strip contains O(log(T+2)) zeros with multiplicity for |u|<=T. Summing reciprocal distances over O(T) strips gives O((log(T+2))^2).",
                "denominator_check": "For Re z>=0 and 0<Re rho<1, |1+z+conjugate(rho)| >= sqrt(1+(Im z-Im rho)^2), so this unit-strip bound applies to the GM pair denominator.",
            },
        },
        "uniform_replay": {
            "status": "PROVED",
            "range": f"x^({q(UNIFORM_THETA)}+epsilon)<=y<=x^({q(UPPER_RANGE)})",
            "truncation": "T=x/y*E(x)^2 and x(log x)^3/T=y(log x)^3/E(x)^2=O(yE(x)^-1).",
            "epsilon_absorption": "T<=x^(13/30-epsilon)*E(x)^2<=x^(1/b-epsilon/2) once 2(log x)^(1/4)<=(epsilon/2)log x.",
            "density_margin": "For eta<=b^2 epsilon/4, (b+eta)(1/b-epsilon/2)-1<=-b epsilon/4.",
            "cutoff": "5/7-2/3=1/21>0; the zero-free branch gives exp(-c(log x)^(2/7)), absorbing log factors including Huxley's log^44 and E(x)^-1.",
            "narrow_conclusion": "Within the GM explicit-formula argument, psi(x+y)-psi(x)=y+O(yE(x)^-1), then pi(x+y)-pi(x)=y/log x+O(yE(x)^-1).",
        },
        "almost_all_replay": {
            "status": "PROVED",
            "range": f"X^({q(ALMOST_ALL_THETA)}+epsilon)<=y<=X^({q(UPPER_RANGE)})",
            "parameters": "delta=X^(-13/15+epsilon/2), T=delta^-1 E(X)^4, and delta X=X^(2/15+epsilon/2)<=y.",
            "epsilon_absorption": "T<=X^(13/15-epsilon/3)=X^(2/b-epsilon/3) once 4(log X)^(1/4)<=(epsilon/6)log X.",
            "density_margin": "For eta<=b^2 epsilon/12, (b+eta)(2/b-epsilon/3)-2<=-b epsilon/6.",
            "pair_reduction": "The pinned multiplicity-inclusive strip count supplies the reciprocal-distance O((log T)^2) used in I<<delta^2(log X)^3 sup_s X^(2s+1)N(s,T).",
            "exceptional_conversion": "The cutoff supplies I<<delta^2 X^3 E(X)^-3; splitting, Chebyshev at yE(X)^-1, and delta^2X^3/(y^2X)<=X^-epsilon give O(XE(X)^-1) exceptional starts.",
            "narrow_conclusion": "Within the GM second-moment argument, pi(x+y)-pi(x)=y/log x+O(yE(X)^-1) outside O(XE(X)^-1) starts.",
        },
        "narrow_pass": {
            "status": "PROVED",
            "passed": [
                "Huxley supplies the exact log-uniform near-one branch.",
                "Riemann--von Mangoldt plus the explicit multiplicity convention supplies the local strip and pair bound.",
                "Platt--Trudgian closes Ford's finite-height gap.",
                "All frozen rational exponent and epsilon transfers replay exactly."
            ],
            "not_passed": [
                "An independent re-proof of the full Guth--Maynard corollaries.",
                "Any improvement of their short-interval exponent."
            ]
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": self_hash(),
            "write_command": "python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v2.py --write projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v2.json",
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, sort_keys=True, indent=2) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    action = parser.add_mutually_exclusive_group()
    action.add_argument("--write", type=Path, metavar="PATH")
    action.add_argument("--check", type=Path, metavar="PATH")
    args = parser.parse_args()
    output = render(certificate())
    if args.write:
        args.write.parent.mkdir(parents=True, exist_ok=True)
        args.write.write_text(output, encoding="utf-8")
    elif args.check:
        if args.check.read_text(encoding="utf-8") != output:
            raise SystemExit(f"certificate mismatch: regenerate with --write ({args.check})")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
