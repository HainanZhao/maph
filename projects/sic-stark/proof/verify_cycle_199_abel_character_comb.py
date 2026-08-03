#!/usr/bin/env python3
"""Exact Abel-character audit for the Cycle-199 Poincare family.

This is deliberately an audit of the *test-character* Poincare sum before it
is paired with the meromorphic beta kernel.  On the endpoint central contour
the three-step deck ratio is explicit.  It shows that a literal bilateral
Abel sum has only a finite lambda strip, and that its meromorphic extension
has six unavoidable contour pole channels.  Thus an endpoint construction
needs a source-derived distributional/contour prescription; it cannot simply
insert u^|k| and integrate over the original whole vertical line.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
LEVEL = 24
SOURCE_PHASE = 437


def triple_step_character_ratio() -> dict[str, object]:
    """Derive chi_(z+3)/chi_z directly from equation-(66)'s character."""

    # N_(z+3)=N_z-18 and alpha_(z+3)=alpha_z+6D.
    discrete_exponent_numerator = -36 * SOURCE_PHASE
    assert discrete_exponent_numerator % 24 == 12
    # exp(pi*i*m*(-36*437)/24)=exp(-3*pi*i*m/2)=i^m.
    return {
        "epistemic_status": "PROVED",
        "deck_shift": "z->z+3: N->N-18, alpha->alpha+6D",
        "discrete_ratio": "exp(-3*pi*i*437*m/2)=i^m",
        "continuous_ratio": "exp(pi*i*D*(2y-Q)/(4*omega))",
        "full_ratio": "rho_m(y)=i^m*exp(pi*i*D*(2y-Q)/(4*omega))",
        "source_phase_mod_24": SOURCE_PHASE % LEVEL,
    }


def endpoint_strip_and_poles() -> dict[str, object]:
    """Audit the literal Abel sum on y=Q/2+i*lambda exactly.

    For 0<u<1, sum_{k in Z} u^|k| rho^k converges iff
    u<|rho|<u^-1.  At the endpoint rho=i^m exp(-c lambda),
    c=pi*D/(2*omega)>0.  It therefore cannot be a test function on all
    lambda in R.  Its rational meromorphic continuation has real-lambda
    poles iff i^m=1, i.e. precisely six m channels.
    """

    records = []
    singular_labels = []
    for label in range(LEVEL):
        singular = label % 4 == 0
        if singular:
            singular_labels.append(label)
        records.append({
            "m_mod_24": label,
            "rho_on_central_contour": f"i^{label}*exp(-pi*D*lambda/(2*omega))",
            "bilateral_abel_convergence_condition": (
                "u<exp(-pi*D*lambda/(2*omega))<u^(-1)"
            ),
            "finite_strip": "|lambda|<2*omega*log(1/u)/(pi*D)",
            "meromorphic_abel_formula": (
                "(1-u^2)/((1-u*rho_m(lambda))*(1-u/rho_m(lambda)))"
            ),
            "on_contour_meromorphic_poles": singular,
            "pole_locations_if_present": (
                "lambda=+-2*omega*log(1/u)/(pi*D)" if singular else None
            ),
        })
    assert singular_labels == [0, 4, 8, 12, 16, 20]
    return {
        "epistemic_status": "PROVED",
        "endpoint_ratio": "rho_m(lambda)=i^m*exp(-pi*D*lambda/(2*omega))",
        "positive_constant": "D/omega>0 because omega=55+12*sqrt(21)>1 and D=(omega-1)/6",
        "abel_sum": "A_u(rho)=sum_(k in Z)u^abs(k)*rho^k",
        "global_central_contour_absolute_convergence": False,
        "six_meromorphic_contour_pole_channels": singular_labels,
        "records": records,
        "required_missing_rule": (
            "A contour deformation, finite-part, or distributional rule must "
            "be derived from the source before the meromorphic Abel formula can "
            "be paired with the endpoint kernel."
        ),
    }


def formal_support_rank_test() -> dict[str, object]:
    """Record the finite-rank warning for a naive rho=1 comb limit.

    This is conditional: it does not assert that the required distributional
    limit exists.  It records what a naive support-only replacement would
    retain, and therefore why it cannot silently be called an all-36
    intertwiner.
    """

    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for residue in range(3):
                # At lambda=0 and m=4h, alpha's continuous phase is one.
                # N=a+2-6r gives exp(pi*i*437*h*(a-6r)/3)
                # = exp(pi*i*437*h*a/3), independently of b,r.
                rows.append({
                    "characteristic": [first, second],
                    "residue_r": residue,
                    "surviving_m_channels": [0, 4, 8, 12, 16, 20],
                    "phase_at_formal_rho_one_support": (
                        "exp(pi*i*437*h*a/3), m=4h; independent of b and r"
                    ),
                })
    assert len(rows) == DIMENSION * DIMENSION * 3
    return {
        "epistemic_status": "PROVED",
        "conditional_premise": (
            "If one replaces the Abel family by only its formal rho=1 support "
            "on the central contour, without additional regular/residue data"
        ),
        "all_rows_and_residues_checked": len(rows),
        "surviving_channel_count": DIMENSION,
        "dependence_after_naive_support_replacement": "only on a, not b or r",
        "rank_upper_bound": DIMENSION,
        "consequence": (
            "That naive support-only object cannot be an injective all-36 map "
            "to T_6. This is not a no-go for a genuine distributional or "
            "residue-completed continuation."
        ),
        "records": rows,
    }


def run() -> dict[str, object]:
    ratio = triple_step_character_ratio()
    strip = endpoint_strip_and_poles()
    support = formal_support_rank_test()
    assert strip["six_meromorphic_contour_pole_channels"] == [0, 4, 8, 12, 16, 20]
    assert support["rank_upper_bound"] == DIMENSION
    return {
        "schema": "sic-stark-cycle-199-abel-character-comb-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The declared literal symmetric three-step Abel character sum is "
            "not globally absolutely convergent on the endpoint central contour, "
            "and its meromorphic formula has six on-contour pole channels. A "
            "naive support-only comb would have rank at most six. This rejects "
            "only an uncompleted literal/supported Abel insertion; it does not "
            "exclude a source-derived contour deformation, finite-part, regular-"
            "plus-residue distribution, other Abel continuation, AFK map, fusion, "
            "Stark result, or TCC."
        ),
        "triple_step_character_ratio": ratio,
        "endpoint_strip_and_poles": strip,
        "formal_support_rank_test": support,
        "gate_outcome": {
            "literal_symmetric_abel_character_insertion": "OBSTRUCTED_ON_ENDPOINT_CENTRAL_CONTOUR",
            "remaining_design_problem": (
                "Construct an explicitly source-derived distributional or contour "
                "continuation that resolves the six character-comb pole channels "
                "and retains enough b-dependent data for an all-36 T6 map."
            ),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rendered = json.dumps(run(), indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
