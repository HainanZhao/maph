#!/usr/bin/env python3
"""Exact Route-B v3 audit of the Guth--Maynard Theorem 1.2 case split.

This certificate uses cleared denominators and factored/expanded residual
polynomials. It is conditional on the zero-detecting input, Theorem 1.1, and
the mean-value theorem used in Guth--Maynard's proof; it does not reprove
those analytic ingredients.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SOURCE_TEX_SHA256 = "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428"
SOURCE_TARBALL_SHA256 = "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc"
LO = Fraction(7, 10)
HI = Fraction(4, 5)


def q(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def hash_self() -> str:
    return hashlib.sha256(Path(__file__).read_bytes()).hexdigest()


def denominator(s: Fraction) -> Fraction:
    return 6 + 10 * s


def lower_q(s: Fraction) -> Fraction:
    return Fraction(10, 1) / denominator(s)


def upper_q(s: Fraction) -> Fraction:
    return Fraction(15, 1) / denominator(s)


def density_exponent(s: Fraction) -> Fraction:
    return 15 * (1 - s) / (3 + 5 * s)


def d(s: Fraction) -> Fraction:
    return Fraction(18, 5) - 4 * s


def alpha(s: Fraction) -> Fraction:
    return density_exponent(s) / d(s)


def strict_margin(s: Fraction) -> Fraction:
    return density_exponent(s) - (1 + (1 - 2 * s) * alpha(s))


def certificate() -> dict[str, Any]:
    """Return the deterministic exact certificate; assertions are exhaustive labels."""
    # Endpoint checks are not numerical sampling: every displayed residual is
    # affine or a positive-denominator quadratic with an explicit factorization
    # recorded below. They merely catch transcription errors in the identities.
    for s in (LO, HI):
        assert denominator(s) > 0
        assert 3 + 5 * s > 0
        assert d(s) > 0
        assert 1 - s > 0
        assert 9 - 10 * s > 0
        assert 20 * s - 12 > 0
        assert 2 * s - 1 > 0
        assert lower_q(s) <= upper_q(s)
        assert density_exponent(s) - 2 * upper_q(s) * (1 - s) == 0
        assert density_exponent(s) - d(s) * alpha(s) == 0
        assert density_exponent(s) - (1 + (Fraction(12, 5) - 4 * s) * lower_q(s)) == 0
        assert alpha(s) <= upper_q(s)
        assert strict_margin(s) > 0

    # Frozen identities that make the signs branch-independent.
    assert lower_q(LO) == Fraction(10, 13)
    assert upper_q(HI) == Fraction(15, 14)
    assert upper_q(HI) - 1 == Fraction(1, 14)
    assert density_exponent(LO) == Fraction(9, 13)
    assert alpha(LO) == Fraction(45, 52)
    assert strict_margin(LO) == Fraction(1, 26)
    assert strict_margin(Fraction(3, 4)) == Fraction(1, 54)
    assert strict_margin(HI) == Fraction(1, 14)

    return {
        "artifact_type": "exact-rational-theorem-1-2-case-split-certificate",
        "certificate_version": 3,
        "route": "B",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Exact exponent audit conditional on the cited zero-detecting "
            "lemma, Theorem 1.1, and mean-value theorem. It neither proves "
            "those analytic inputs nor converts log factors into exact "
            "finite-T power inequalities."
        ),
        "source_inputs": {
            "arxiv_version": "2405.20552v2",
            "source_tarball_sha256": SOURCE_TARBALL_SHA256,
            "tex_member": "LargevaluesDirichlet17.tex",
            "tex_member_sha256": SOURCE_TEX_SHA256,
            "checked_locations": [
                "Theorem 1.2 proof, TeX lines 2307--2380",
                "equation (kDef), TeX lines 2352--2358",
                "mean-value strict-margin identity, TeX lines 2375--2379",
            ],
        },
        "frozen_range": {
            "s": "[7/10,4/5]",
            "n": "log(N)/log(T)",
            "q": "log(N^k)/log(T) = k*n",
            "D_s": "6+10*s",
            "l_s": "10/D(s)",
            "u_s": "15/D(s)",
            "B_s": "15*(1-s)/(3+5*s)",
            "d_s": "18/5-4*s",
            "alpha_s": "B(s)/d(s)",
        },
        "positive_denominator_and_residual_certificates": [
            {
                "label": "base denominators",
                "positive_on_range": ["D(s)=6+10*s", "3+5*s", "d(s)=(18-20*s)/5"],
                "endpoint_minima": {"D": "13", "3+5*s": "13/2", "5*d": "2"},
            },
            {
                "label": "Type II residual B(s)-2(1-s)",
                "denominator": "3+5*s > 0",
                "factored_numerator": "(1-s)*(9-10*s)",
                "expanded_numerator": "10*s^2-19*s+9",
                "sign": ">= 0 on [7/10,4/5] (indeed through s=9/10)",
            },
            {
                "label": "large-n endpoint gap u(s)-1",
                "denominator": "D(s)>0",
                "factored_numerator": "9-10*s",
                "expanded_numerator": "9-10*s",
                "sign": ">= 1/14 on [7/10,4/5] after division by D(s)",
            },
            {
                "label": "Theorem 1.1 third-term direction",
                "quantity": "-(12/5-4*s)=(20*s-12)/5",
                "sign": ">=2/5>0 on [7/10,4/5]",
            },
            {
                "label": "Guth--Maynard branch endpoint containment alpha(s)<=u(s)",
                "denominator": "3+5*s > 0",
                "factored_numerator_for_d(s)*u(s)-B(s)": "3*(4-5*s)",
                "expanded_numerator": "12-15*s",
                "sign": ">=0 on [7/10,4/5], with equality only at s=4/5",
            },
            {
                "label": "mean-value strict residual",
                "denominator": "2*(3+5*s)*(9-10*s) > 0",
                "factored_numerator": "250*(s-3/4)^2+3/8",
                "expanded_numerator": "250*s^2-375*s+141",
                "sign": ">=3/8>0 on [7/10,4/5]",
            },
        ],
        "type_ii": {
            "input": "number of Type II zeros <= T^(2-2*s)*(log T)^O(1)",
            "target": "T^(B(s)+o(1))",
            "cleared_relation": "B(s)-2*(1-s)=(1-s)*(9-10*s)/(3+5*s)",
            "conclusion": "2*(1-s) <= B(s)",
        },
        "integer_choice_regimes": {
            "small_n": {
                "condition": "1/100 < n <= 5/D(s) = l(s)/2",
                "choice": "k=ceil(l(s)/n)",
                "bounded_integer_certificate": "l(s)/n <= 1000/13 <77, hence 1<=k<=77",
                "lower_residual": "q-l(s)=n*ceil(l(s)/n)-l(s) >=0",
                "upper_residual": (
                    "q-u(s) < n-(u(s)-l(s)); after multiplying by D(s), "
                    "D(s)*n <=5=D(s)*(u(s)-l(s)), hence q<=u(s)"
                ),
                "conclusion": "l(s)<=q<=u(s) exactly at power scale",
            },
            "large_n": {
                "condition": "n > 5/D(s)",
                "choice": "k=2",
                "lower_residual": "q-l(s)=2*n-10/D(s)>0",
                "source_upper_input": "n<=1/2+o(1), from N<=T^(1/2)(log T)^2",
                "endpoint_containment": (
                    "q<=1+o(1), while u(s)-1=(9-10*s)/D(s)>=1/14; "
                    "therefore q<=u(s)+o(1). This is not asserted as an "
                    "unqualified finite-T inequality."
                ),
                "conclusion": "l(s)<q<=u(s)+o(1) at power scale",
            },
        },
        "guth_maynard_branch_q_le_alpha": {
            "condition": "q<=alpha(s)",
            "term_1": {
                "residual": "B(s)-2*q*(1-s)=2*(1-s)*(u(s)-q)",
                "sign_source": "q<=alpha(s)<=u(s), 1-s>0",
                "conclusion": "2*q*(1-s)<=B(s)",
            },
            "term_2": {
                "residual": "B(s)-d(s)*q=d(s)*(alpha(s)-q)",
                "sign_source": "d(s)>0",
                "conclusion": "d(s)*q<=B(s)",
            },
            "term_3": {
                "residual": "B(s)-[1+(12/5-4*s)*q]=(4*s-12/5)*(q-l(s))",
                "sign_source": "4*s-12/5>0 and q>=l(s)",
                "conclusion": "1+(12/5-4*s)*q<=B(s)",
            },
        },
        "mean_value_branch_q_gt_alpha": {
            "condition": "q>alpha(s)",
            "term_1": {
                "residual": "B(s)-2*q*(1-s)=2*(1-s)*(u(s)-q)",
                "sign_source": "q<=u(s)+o(1)",
                "conclusion": "2*q*(1-s)<=B(s)+o(1)",
            },
            "term_2_strict": {
                "residual_decomposition": (
                    "B(s)-[1+(1-2*s)*q] = M(s)+(2*s-1)*(q-alpha(s))"
                ),
                "M_factored": "[250*(s-3/4)^2+3/8]/[2*(3+5*s)*(9-10*s)]",
                "M_expanded_numerator": "250*s^2-375*s+141",
                "sign_source": "M(s)>0, 2*s-1>0, q-alpha(s)>0",
                "conclusion": "1+(1-2*s)*q<B(s)",
            },
        },
        "endpoint_slack_policy": {
            "exact_power_relations": "All rational relations that use l,u,B,d,alpha are exact.",
            "logarithmic_upper_endpoint": (
                "The source N<=T^(1/2)(log T)^2 is represented only as "
                "n<=1/2+o(1), hence q<=u+o(1) in the k=2 regime."
            ),
            "no_silent_upgrade": True,
        },
        "replay": {
            "interpreter_requirement": "Python 3 standard library only",
            "script_sha256": hash_self(),
            "write_command": (
                "python3 projects/guth-maynard-zero-density/proof/"
                "replay_theorem_1_2_case_split_route_b_v3.py --write "
                "projects/guth-maynard-zero-density/artifacts/"
                "cycle-1-route-b-v3-theorem-1-2-case-split.json"
            ),
        },
    }


def render(data: dict[str, Any]) -> str:
    return json.dumps(data, indent=2, sort_keys=True) + "\n"


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
