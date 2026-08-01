#!/usr/bin/env python3
"""Exact Route A audit of the Guth--Maynard Theorem 1.2 case split.

This is a rational-exponent replay conditional on the cited zero-detection,
large-values, and mean-value inputs.  It does not reprove those analytic
results.  No floating-point arithmetic is used in the mathematical audit.
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


VERSION = 4
ROUTE = "A"
LEFT = Fraction(7, 10)
RIGHT = Fraction(4, 5)
FROZEN_SOURCE = {
    "arxiv_identifier": "2405.20552v2",
    "source_tarball_sha256": "9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc",
    "tex_sha256": "36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428",
    "source_locations": "source lines 2307--2399, proof of Theorem 1.2",
}


def q(value: Fraction) -> str:
    """Serialize exact rationals canonically, including denominator one."""
    return f"{value.numerator}/{value.denominator}"


def lower(s: Fraction) -> Fraction:
    return Fraction(10, 1) / (Fraction(6, 1) + Fraction(10, 1) * s)


def upper(s: Fraction) -> Fraction:
    return Fraction(15, 1) / (Fraction(6, 1) + Fraction(10, 1) * s)


def target(s: Fraction) -> Fraction:
    return Fraction(15, 1) * (Fraction(1, 1) - s) / (Fraction(3, 1) + Fraction(5, 1) * s)


def d(s: Fraction) -> Fraction:
    return Fraction(18, 5) - Fraction(4, 1) * s


def alpha(s: Fraction) -> Fraction:
    return target(s) / d(s)


def strict_mean_value_margin(s: Fraction) -> Fraction:
    """B(s)-[1+(1-2s)alpha(s)], in the source's exact form."""
    numerator = Fraction(250, 1) * (s - Fraction(3, 4)) ** 2 + Fraction(3, 8)
    denominator = (
        Fraction(2, 1)
        * (Fraction(3, 1) + Fraction(5, 1) * s)
        * (Fraction(9, 1) - Fraction(10, 1) * s)
    )
    return numerator / denominator


def direct_margin(s: Fraction) -> Fraction:
    return target(s) - (Fraction(1, 1) + (Fraction(1, 1) - Fraction(2, 1) * s) * alpha(s))


def canonical_sha256(value: dict[str, Any]) -> str:
    data = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def endpoint_and_monotonicity_audit() -> dict[str, Any]:
    """Audit all sign/endpoint facts used to choose k on the frozen range."""
    one = Fraction(1, 1)
    l_left, l_right = lower(LEFT), lower(RIGHT)
    u_left, u_right = upper(LEFT), upper(RIGHT)
    b_left, b_right = target(LEFT), target(RIGHT)
    d_left, d_right = d(LEFT), d(RIGHT)

    # The derivative numerators have positive squared denominators.
    assert l_left == Fraction(10, 13) and l_right == Fraction(5, 7)
    assert u_left == Fraction(15, 13) and u_right == Fraction(15, 14)
    assert b_left == Fraction(9, 13) and b_right == Fraction(3, 7)
    assert d_left == Fraction(4, 5) and d_right == Fraction(2, 5)
    assert u_right - one == Fraction(1, 14) > 0
    assert d_right > 0

    return {
        "interval": "7/10 <= s <= 4/5",
        "positive_denominators": [
            "6+10s >= 13 > 0",
            "3+5s >= 13/2 > 0",
            "9-10s >= 1 > 0",
            "d(s)=18/5-4s >= 2/5 > 0",
        ],
        "monotonicity": {
            "l": "l'(s)=-100/(6+10s)^2 < 0",
            "u": "u'(s)=-150/(6+10s)^2 < 0",
            "B": "B'(s)=-120/(3+5s)^2 < 0",
            "d": "d'(s)=-4 < 0",
        },
        "endpoint_values": {
            "l(7/10), l(4/5)": [q(l_left), q(l_right)],
            "u(7/10), u(4/5)": [q(u_left), q(u_right)],
            "B(7/10), B(4/5)": [q(b_left), q(b_right)],
            "d(7/10), d(4/5)": [q(d_left), q(d_right)],
            "uniform_gap_u_minus_1": q(u_right - one),
        },
    }


def theorem_1_2_case_split() -> dict[str, Any]:
    """Return the fully labelled rational branch audit required by G0."""
    one = Fraction(1, 1)
    zero = Fraction(0, 1)
    midpoint = Fraction(3, 4)
    audit = endpoint_and_monotonicity_audit()

    # Type II: B-2(1-s)=(1-s)(9-10s)/(3+5s), all factors nonnegative
    # through s=9/10.  This contains the frozen interval.
    type_ii_left = target(LEFT) - Fraction(2, 1) * (one - LEFT)
    type_ii_right = target(RIGHT) - Fraction(2, 1) * (one - RIGHT)
    assert type_ii_left == Fraction(6, 65)
    assert type_ii_right == Fraction(1, 35)
    assert type_ii_left > 0 and type_ii_right > 0

    # Small-n k choice: n<=l/2, k=ceil(l/n).  Then l<=q<l+n<=3l/2=u.
    # Since n>=1/100 on the power scale, k<=77 uniformly.
    small_boundary_left = lower(LEFT) / 2
    small_boundary_right = lower(RIGHT) / 2
    assert small_boundary_left == Fraction(5, 13)
    assert small_boundary_right == Fraction(5, 14)
    assert Fraction(1000, 13) < 77

    # Large-n k choice: q=2n>l.  The upper source input is
    # n<=1/2+o(1), hence q<=1+o(1); u(s)>=15/14=1+1/14 absorbs this
    # uniformly for sufficiently large T.  This is intentionally not an
    # unqualified finite-T assertion q<=u.
    assert upper(RIGHT) > one

    # Exact boundary substitutions in the GM branch q<=alpha.
    gm_first_at_upper_left = Fraction(2, 1) * upper(LEFT) * (one - LEFT)
    gm_first_at_upper_right = Fraction(2, 1) * upper(RIGHT) * (one - RIGHT)
    gm_second_at_alpha_left = d(LEFT) * alpha(LEFT)
    gm_second_at_alpha_right = d(RIGHT) * alpha(RIGHT)
    gm_third_at_lower_left = one + (Fraction(12, 5) - Fraction(4, 1) * LEFT) * lower(LEFT)
    gm_third_at_lower_right = one + (Fraction(12, 5) - Fraction(4, 1) * RIGHT) * lower(RIGHT)
    assert gm_first_at_upper_left == target(LEFT)
    assert gm_first_at_upper_right == target(RIGHT)
    assert gm_second_at_alpha_left == target(LEFT)
    assert gm_second_at_alpha_right == target(RIGHT)
    assert gm_third_at_lower_left == target(LEFT)
    assert gm_third_at_lower_right == target(RIGHT)
    assert Fraction(12, 5) - Fraction(4, 1) * RIGHT < 0
    assert Fraction(12, 5) - Fraction(4, 1) * LEFT < 0

    # Exact source margin on the MVT branch q>alpha.  The direct and stated
    # rational expressions agree at both endpoints and at the quadratic
    # vertex; the displayed factorization supplies positivity on all s.
    for value in (LEFT, midpoint, RIGHT):
        assert direct_margin(value) == strict_mean_value_margin(value)
        assert strict_mean_value_margin(value) > zero
    margin_left = strict_mean_value_margin(LEFT)
    margin_midpoint = strict_mean_value_margin(midpoint)
    margin_right = strict_mean_value_margin(RIGHT)
    assert margin_left == Fraction(1, 26)
    assert margin_midpoint == Fraction(1, 54)
    assert margin_right == Fraction(1, 14)

    return {
        "claim_boundary": (
            "Exact exponent audit conditional on the cited zero-detection "
            "lemma, Theorem 1.1, and mean-value theorem; it is not an "
            "independent proof of those analytic inputs."
        ),
        "definitions": {
            "l(s)": "10/(6+10s)",
            "u(s)": "15/(6+10s)",
            "B(s)": "15(1-s)/(3+5s)",
            "d(s)": "18/5-4s",
            "alpha(s)": "B(s)/d(s)",
        },
        "monotonicity_and_endpoints": audit,
        "type_ii": {
            "source_bound_exponent": "2(1-s)",
            "residual_identity": "B(s)-2(1-s)=(1-s)(9-10s)/(3+5s)",
            "valid_source_range": "s <= 9/10",
            "residual_at_frozen_endpoints": [q(type_ii_left), q(type_ii_right)],
            "conclusion": "2(1-s) <= B(s) on 7/10 <= s <= 4/5",
        },
        "integer_choice": {
            "power_scale_n_range": "1/100 < n <= 1/2+o(1)",
            "small_n": {
                "condition": "n <= l(s)/2 = 5/(6+10s)",
                "choice": "k=ceil(l(s)/n)",
                "boundedness": "k <= 77",
                "conclusion": "l(s) <= q=k*n < l(s)+n <= 3l(s)/2=u(s)",
            },
            "large_n": {
                "condition": "n > l(s)/2",
                "choice": "k=2",
                "exact_lower": "q=2n > l(s)",
                "source_upper": "q <= 1+o(1)",
                "uniform_slack": "u(s)-1 >= 1/14 > 0",
                "contained_conclusion": "q <= u(s)+o(1), and q<u(s) eventually; no finite-T exact q<=u claim is made",
            },
        },
        "guth_maynard_branch_q_le_alpha": {
            "condition": "q <= alpha(s)",
            "first_term": {
                "exponent": "2q(1-s)",
                "monotonicity_in_q": "increasing",
                "boundary_identity": "2u(s)(1-s)=B(s)",
                "conclusion": "2q(1-s) <= B(s)+o(1); exact in the small-n regime",
            },
            "second_term": {
                "exponent": "d(s)q",
                "monotonicity_in_q": "increasing because d(s)>0",
                "boundary_identity": "d(s)alpha(s)=B(s)",
                "conclusion": "d(s)q <= B(s)",
            },
            "third_term": {
                "exponent": "1+(12/5-4s)q",
                "monotonicity_in_q": "decreasing because 12/5-4s<0",
                "boundary_identity": "1+(12/5-4s)l(s)=B(s)",
                "conclusion": "1+(12/5-4s)q <= B(s)",
            },
            "exact_endpoint_substitutions": {
                "first": [q(gm_first_at_upper_left), q(gm_first_at_upper_right)],
                "second": [q(gm_second_at_alpha_left), q(gm_second_at_alpha_right)],
                "third": [q(gm_third_at_lower_left), q(gm_third_at_lower_right)],
            },
        },
        "mean_value_branch_q_gt_alpha": {
            "condition": "q > alpha(s)",
            "first_term": {
                "exponent": "2q(1-s)",
                "conclusion": "2q(1-s) <= B(s)+o(1); exact in the small-n regime",
            },
            "second_term": {
                "exponent": "1+(1-2s)q",
                "monotonicity_in_q": "strictly decreasing because 1-2s<0",
                "strict_conclusion": "1+(1-2s)q < B(s)",
                "margin_identity": (
                    "B(s)-[1+(1-2s)alpha(s)]="
                    "[250(s-3/4)^2+3/8]/[2(3+5s)(9-10s)]>0"
                ),
                "exact_margin_at_7_10_3_4_4_5": [q(margin_left), q(margin_midpoint), q(margin_right)],
            },
        },
        "coverage": {
            "q_branches": ["q <= alpha(s)", "q > alpha(s)"],
            "all_branch_labels_exercised": True,
            "o_one_containment_retained": True,
        },
        "construction_audit": {
            "contained_pre_artifact_failure": "a hand-entered midpoint margin 3/52 was rejected by an exact assertion",
            "corrected_value": "at s=3/4 the source margin formula evaluates to 1/54",
            "status": "corrected before the first v4 artifact was written",
        },
    }


def main() -> None:
    started_ns = time.perf_counter_ns()
    script = Path(__file__).resolve()
    project = script.parent.parent
    certificate = theorem_1_2_case_split()
    certificate.update(
        {
            "artifact_version": VERSION,
            "route": ROUTE,
            "arithmetic": "exact fractions.Fraction only",
            "frozen_source": FROZEN_SOURCE,
        }
    )
    certificate["mathematical_certificate_sha256"] = canonical_sha256(certificate)
    certificate["replay"] = {
        "script": str(script.relative_to(project)),
        "script_sha256": file_sha256(script),
        "python_implementation": platform.python_implementation(),
        "python_version": sys.version.split()[0],
        "wall_time_ns": time.perf_counter_ns() - started_ns,
    }
    artifact = project / "artifacts" / "theorem-1-2-case-split-route-a-v4.json"
    artifact.write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(artifact)


if __name__ == "__main__":
    main()
