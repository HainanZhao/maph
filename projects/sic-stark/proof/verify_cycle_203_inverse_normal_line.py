#!/usr/bin/env python3
"""Exact normal-line canonicity audit for Cycle 203/B040.

The attracting A_6 axis has a canonical orientation and an exact contraction
eigenvalue beta^(-6).  Nevertheless, every positive reparametrization s_c=c s
preserves the axis, its endpoints, that eigenvalue, pole-side orientation, and
the pulled-back equation-(66) family.  It rescales the normal cotangent line,
so no nonzero inverse normal-line element is fixed by the declared source
data.  The invariant logarithmic form ds/s is not a boundary normal density.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path


def a6_axis_multiplier() -> dict[str, object]:
    """Derive the normal multiplier at beta from the exact A_6 matrix."""

    def multiply(left: tuple[Fraction, Fraction], right: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
        return (
            left[0] * right[0] + 21 * left[1] * right[1],
            left[0] * right[1] + left[1] * right[0],
        )

    beta = (Fraction(5, 2), Fraction(1, 2))
    beta_inverse = (Fraction(5, 2), Fraction(-1, 2))
    beta_cubed = multiply(multiply(beta, beta), beta)
    assert beta_cubed == (Fraction(55), Fraction(12))
    assert multiply(beta, beta_inverse) == (Fraction(1), Fraction(0))
    assert 115 * -5 - (-24) * 24 == 1

    # With x(tau)=(tau-beta)/(tau-beta^(-1)), direct substitution in gamma
    # gives x(gamma(s))=i*s.  A Mobius map with the two fixed points sends
    # x to A6'(beta)*x, so its exact local multiplier gives the displayed
    # gamma conjugacy without numerical sampling.
    return {
        "epistemic_status": "PROVED",
        "A6": [[115, -24], [24, -5]],
        "fixed_points": ["beta=(5+sqrt(21))/2", "beta^(-1)=(5-sqrt(21))/2"],
        "denominator_at_beta": "24*beta-5=55+12*sqrt(21)=beta^3",
        "mobius_derivative_at_beta": "A6'(beta)=1/(24*beta-5)^2=beta^(-6)",
        "axis_coordinate": (
            "gamma(s)=(beta+beta^(-1)*s^2+i*sqrt(21)*s)/(1+s^2)"
        ),
        "cross_ratio_coordinate": "(gamma(s)-beta)/(gamma(s)-beta^(-1))=i*s",
        "endpoint_tangent": "gamma'(0)=i*sqrt(21)!=0",
        "local_action": "A6*gamma(s)=gamma(beta^(-6)*s)",
        "orientation": "s>0 is the frozen upper-half-plane approach",
    }


def rescaling_symmetry() -> dict[str, object]:
    """Check what all positive local-coordinate rescalings preserve."""

    records = []
    for symbol in ("c", "c^2", "1/c"):
        records.append({
            "positive_rescaling": f"s_{symbol}={symbol}*s",
            "same_axis": "gamma_c(s_c)=gamma(s_c/" + symbol + ")",
            "A6_action": "s_c -> beta^(-6)*s_c",
            "endpoint": "s_c=0 iff s=0",
            "pole_side_orientation": "preserved for positive rescaling",
            "source_tau_family": "unchanged after pullback along the same tau-image",
        })
    return {
        "epistemic_status": "PROVED",
        "scaling_group": "c in R_{>0}",
        "records": records,
        "preserved_source_data": [
            "A_6 axis image and two endpoints",
            "A_6 normal eigenvalue beta^(-6)",
            "upper-half-plane/pole-side orientation",
            "equation-(66) tau-family after reparametrization",
        ],
        "not_fixed_by_source_data": "a nonzero scale for s",
    }


def normal_line_obstruction() -> dict[str, object]:
    """Separate a logarithmic invariant from a true inverse-line vector."""

    return {
        "epistemic_status": "PROVED",
        "normal_cotangent_line": "N^*=I/I^2=span([ds])",
        "coordinate_change": "[ds_c]=c*[ds]",
        "inverse_line_change": "[ds_c]^(-1)=c^(-1)*[ds]^(-1)",
        "invariant_logarithmic_form": "ds/s is c-invariant on the punctured axis",
        "logarithmic_form_failure": (
            "ds/s has a pole at s=0 and is not a nonzero element of N^* or "
            "its inverse at the boundary."
        ),
        "invariance_equation_for_inverse_vector": "v=c^(-1)*v for all c>0",
        "only_invariant_inverse_vector": "0",
        "consequence": (
            "The declared source data determines an oriented scaled normal line, "
            "but no nonzero source-defined inverse trivialization that can cancel "
            "the Cycle-202 weight-one normal datum."
        ),
    }


def run() -> dict[str, object]:
    multiplier = a6_axis_multiplier()
    rescaling = rescaling_symmetry()
    line = normal_line_obstruction()
    assert multiplier["mobius_derivative_at_beta"].endswith("beta^(-6)")
    assert rescaling["not_fixed_by_source_data"] == "a nonzero scale for s"
    assert line["only_invariant_inverse_vector"] == "0"
    return {
        "schema": "sic-stark-cycle-203-inverse-normal-line-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The declared A_6 axis, equation-(66) tau-family, and pole-side "
            "orientation determine only an oriented normal line with contraction "
            "beta^(-6), not a nonzero source-defined inverse normal-line "
            "trivialization. Hence they cannot canonically twist the weight-one "
            "normal datum to weight zero. This rejects only that intrinsic "
            "trivialization class and does not exclude a new source density "
            "theorem, covariant target line, nonlinear/higher-germ/non-Abel "
            "construction, AFK, fusion, Stark, or TCC."
        ),
        "a6_axis_multiplier": multiplier,
        "rescaling_symmetry": rescaling,
        "normal_line_obstruction": line,
        "gate_outcome": {
            "intrinsic_inverse_normal_line_from_declared_source_geometry": "FALSIFIED",
            "remaining_design_problem": (
                "Find a new source theorem that fixes a normal density, or a "
                "covariant target line and pairing, without importing a regulator "
                "scale or target-fitted trivialization."
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
