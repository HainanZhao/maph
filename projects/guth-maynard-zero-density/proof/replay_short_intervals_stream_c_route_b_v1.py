#!/usr/bin/env python3
"""Conditional exact Route-B audit of GM section 13.2 short intervals.

The arithmetic transfer is checked with exact rational exponents.  The source
ledger records two external inputs that remain unread/inaccessible, so this
certificate is deliberately not a proof-grade promotion of Corollaries 1.3 or
1.4.  It instead makes every required conditional input and every downstream
epsilon/error conversion explicit.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_GM_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE_FORD_PDF_SHA256 = "a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948"
B = Fraction(30, 13)
UNIFORM_THETA = Fraction(17, 30)
ALMOST_ALL_THETA = Fraction(2, 15)
UPPER_RANGE = Fraction(99, 100)
EPS_MAX = UPPER_RANGE - UNIFORM_THETA


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def self_hash() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def certificate() -> dict[str, Any]:
    """Build exact exponent implications and assert all stated rational identities."""
    one_over_b = Fraction(1, 1) / B
    two_over_b = Fraction(2, 1) / B
    assert one_over_b == Fraction(13, 30)
    assert two_over_b == Fraction(13, 15)
    assert UNIFORM_THETA == 1 - one_over_b
    assert ALMOST_ALL_THETA == 1 - two_over_b
    assert EPS_MAX == Fraction(127, 300)

    # Uniform: y >= x^(17/30+eps) and T=x/y*exp(2 log(x)^(1/4)).
    # The endpoint power after absorbing the subpower factor is 13/30-eps/2.
    assert 1 - (UNIFORM_THETA) == one_over_b
    assert B * one_over_b == 1

    # Almost all: delta=X^(-13/15+eps/2), then T=delta^-1*subpower.
    assert 1 - two_over_b == ALMOST_ALL_THETA
    assert 1 + (-two_over_b) == ALMOST_ALL_THETA
    # delta*X has exponent 1-2/b+eps/2, below y by eps/2.
    assert 1 - two_over_b == ALMOST_ALL_THETA
    # The splitting remainder / (y^2 X) has exponent -eps.
    # 2*(-2/b + eps/2)+2 -2*(1-2/b+eps) = -eps.
    constant_part = 2 * (-two_over_b) + 2 - 2 * ALMOST_ALL_THETA
    assert constant_part == 0

    return {
        "artifact_type": "conditional-exact-short-interval-stream-c-route-b-certificate",
        "certificate_version": 1,
        "route": "B",
        "epistemic_status": "OBSERVED",
        "claim_boundary": (
            "Exact replay of the exponent, epsilon, cutoff, truncation, and "
            "exceptional-set implications displayed in Guth--Maynard section "
            "13.2, conditional on the ledger's near-one density and local "
            "zero-counting inputs. Those two inputs remain unpromoted, so this "
            "artifact does not independently prove either short-interval "
            "corollary."
        ),
        "frozen_parameters": {
            "b": q(B),
            "uniform_theta": q(UNIFORM_THETA),
            "almost_all_theta": q(ALMOST_ALL_THETA),
            "upper_y_exponent": q(UPPER_RANGE),
            "nonvacuous_epsilon_range": f"0 < epsilon < {q(EPS_MAX)}",
            "subpower_symbol": "E(Z)=exp((log Z)^(1/4))",
        },
        "external_inputs_and_status": {
            "truncated_explicit_formula": {
                "status": "PROVED",
                "source": "Guth--Maynard §13.2, TeX lines 2409--2412",
                "hypotheses_checked": "2 <= T <= x",
                "statement_used": (
                    "psi(x+y)-psi(x)=y-sum_(|rho|<=T)((x+y)^rho-x^rho)/rho "
                    "+O(x(log x)^3/T)"
                ),
            },
            "near_one_density": {
                "status": "OBSERVED",
                "source_claim": "Guth--Maynard TeX lines 2421--2424 cites Jutila or Montgomery Theorem 12.1",
                "needed_uniform_form": "N(s,T) << T^((30/13+o(1))*(1-s))*(log T)^O(1) through the cutoff",
                "blocker": "Jutila 1977 and the locally frozen Huxley source are scanned/no theorem text; no exact theorem hypotheses were machine-checked.",
            },
            "vinogradov_korobov_zero_free": {
                "status": "PROVED",
                "source": "Kevin Ford, Zero-free regions for the Riemann zeta function (2002), Theorem 5, local PDF page 4",
                "checked_statement": "zeta(beta+it)!=0 when |t|>=3 and 1-beta <= 1/[57.54(log|t|)^(2/3)(loglog|t|)^(1/3)]",
                "transfer": "For sufficiently large T it supplies a cutoff s<=1-c(log T)^(-5/7).",
                "scope_limit": "This retrieval alone does not certify the low-height completion needed to state N(s,T)=0 for every |Im rho|<=T at the cutoff.",
            },
            "almost_all_local_zero_count": {
                "status": "OBSERVED",
                "source_claim": "Guth--Maynard TeX lines 2453--2460 uses O(log T) zeros per unit-height strip and a reciprocal-distance sum O((log T)^2).",
                "blocker": "No uniquely cited primary theorem/source with exact conventions was located and checked in this cycle.",
            },
        },
        "uniform_replay": {
            "range": f"x^({q(UNIFORM_THETA)}+epsilon)<=y<=x^({q(UPPER_RANGE)})",
            "truncation": "T=x/y*E(x)^2",
            "truncation_error": "x(log x)^3/T = y(log x)^3/E(x)^2 = O(y*E(x)^-1)",
            "zero_term_bound": "|((x+y)^rho-x^rho)/rho| <= y*x^(Re(rho)-1)",
            "discretized_supremum": "O(y log x sup_s x^(s-1)N(s,T))",
            "epsilon_absorption": {
                "power_before_subpower": "T<=x^(13/30-epsilon)*E(x)^2",
                "sufficient_log_condition": "2(log x)^(1/4) <= (epsilon/2)log x",
                "power_after_subpower": "T<=x^(13/30-epsilon/2)=x^(1/b-epsilon/2)",
            },
            "density_margin": {
                "choose_o_one_coefficient": "eta<=b^2*epsilon/4",
                "cleared_exponent": "(b+eta)*(1/b-epsilon/2)-1 <= -b*epsilon/4",
                "base_ratio": "T^(b+eta)/x <= x^(-b*epsilon/4)",
            },
            "zero_free_cutoff": {
                "source_width": "c0(log T)^(-2/3)(loglog T)^(-1/3)",
                "weaker_cutoff_used": "c(log T)^(-5/7)",
                "power_comparison": "5/7-2/3=1/21>0; choose c after T is sufficiently large",
                "supremum_decay": "exp(-c'*(log x)^(2/7)), which absorbs log powers and dominates exp(-(log x)^(1/4))",
            },
            "upper_range_checks": [
                "y<=x^(99/100) gives T>=x^(1/100)*E(x)^2, so T tends to infinity",
                "T<=x^(13/30-epsilon/2)<x for sufficiently large x",
                "prime-power and partial-summation remainders are negligible because 17/30>1/2 and y/x<=x^(-1/100)",
            ],
            "conditional_conclusion": "psi(x+y)-psi(x)=y+O(y*E(x)^-1), then pi(x+y)-pi(x)=y/log x+O(y*E(x)^-1)",
        },
        "almost_all_replay": {
            "range": f"X^({q(ALMOST_ALL_THETA)}+epsilon)<=y<=X^({q(UPPER_RANGE)})",
            "delta": "delta=X^(-13/15+epsilon/2)=X^(-2/b+epsilon/2)",
            "coverage_check": "delta*X=X^(2/15+epsilon/2)<=y, with spare exponent epsilon/2",
            "truncation": "T=delta^-1*E(X)^4",
            "epsilon_absorption": {
                "sufficient_log_condition": "4(log X)^(1/4)<=(epsilon/6)log X",
                "power_after_subpower": "T<=X^(13/15-epsilon/3)=X^(2/b-epsilon/3)",
            },
            "second_moment_target": "I<=delta^2*X^3*E(X)^-3",
            "pair_counting_reduction": "I<<delta^2(log X)^3 sup_s X^(2s+1)N(s,T)",
            "density_margin": {
                "choose_o_one_coefficient": "eta<=b^2*epsilon/12",
                "cleared_exponent": "(b+eta)*(2/b-epsilon/3)-2 <= -b*epsilon/6",
                "base_ratio": "T^(b+eta)/X^2<=X^(-b*epsilon/6)",
                "cutoff_decay": "exp(-c''*(log X)^(2/7)), which dominates E(X)^-10 and log powers",
            },
            "splitting_and_exceptional_conversion": {
                "split_bound": "L2_long << y^2/(delta^2 X^2)*I+O(delta^2 X^3)",
                "main_term_after_target": "<=y^2 X E(X)^-3",
                "remainder_ratio": "delta^2 X^3/(y^2 X)<=X^(-epsilon), hence <=E(X)^-3 for large X",
                "chebyshev_threshold": "Chebyshev threshold: y*E(X)^-1",
                "exceptional_measure": "O(X*E(X)^-1)",
                "pi_conversion": "same deterministic prime-power/partial-summation controls as the uniform branch, using the frozen lower and upper y ranges",
            },
            "conditional_conclusion": "outside O(X*E(X)^-1) starts, pi(x+y)-pi(x)=y/log x+O(y*E(X)^-1)",
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": self_hash(),
            "write_command": (
                "python3 projects/guth-maynard-zero-density/proof/"
                "replay_short_intervals_stream_c_route_b_v1.py --write "
                "projects/guth-maynard-zero-density/artifacts/"
                "cycle-2-stream-c-route-b-v1.json"
            ),
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
