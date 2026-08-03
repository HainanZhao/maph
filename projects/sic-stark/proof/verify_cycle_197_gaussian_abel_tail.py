#!/usr/bin/env python3
"""Exact all-36 failure audit for the fixed Gaussian Abel tail rule.

At the RM endpoint the source two-gamma kernel has nonzero constant tails
after its quadratic phases cancel.  A real nonzero Fourier frequency turns
one tail into a growing exponential.  The prescribed even Gaussian cutoff
therefore has a positive Laplace exponent proportional to 1/epsilon.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6


def centered_mod_six(value: int) -> int:
    residue = value % DIMENSION
    return residue if residue <= 2 else residue - DIMENSION


def endpoint_constants() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED",
        "beta": "(5+sqrt(21))/2",
        "omega": "55+12*sqrt(21)",
        "Q": "56+12*sqrt(21)",
        "B": "2*pi/(24*omega)>0",
        "alpha_centered": "alpha_s=(omega-1)*s/18",
        "gaussian": "exp(epsilon*(y-Re(Q)/2)^2)=exp(-epsilon*lambda^2)",
        "source_tail": "K_Q(Re(Q)/2+i*lambda,m) has a nonzero constant tail coefficient after the quadratic Gamma_M phases cancel",
    }


def component_record(first: int, second: int) -> dict[str, object]:
    centered = centered_mod_six(4 * second - 5 * first)
    if centered == 0:
        return {
            "characteristic": [first, second],
            "centered_frequency_s": centered,
            "alpha": 0,
            "classification": "ZERO_FREQUENCY_SEPARATE",
            "gaussian_failure_exponent": 0,
            "uniform_endpoint_limit_contributed": False,
        }
    squared = centered * centered
    return {
        "characteristic": [first, second],
        "centered_frequency_s": centered,
        "alpha": f"(omega-1)*{centered}/18",
        "growing_tail_direction": "lambda->-infinity" if centered > 0 else "lambda->+infinity",
        "source_tail_coefficient": "nonzero Z(m)/Z(-m) phase coefficient",
        "gaussian_laplace_exponent": f"pi^2*(omega-1)^2*{squared}/(186624*omega^2*epsilon)",
        "gaussian_failure_exponent_numerator_s_squared": squared,
        "classification": "POSITIVE_1_OVER_EPSILON_DIVERGENCE",
        "uniform_endpoint_limit_contributed": False,
    }


def all_component_ledger() -> dict[str, object]:
    records = [component_record(first, second) for first in range(DIMENSION) for second in range(DIMENSION)]
    nonzero = [row for row in records if row["centered_frequency_s"] != 0]
    zero = [row for row in records if row["centered_frequency_s"] == 0]
    assert len(records) == 36 and len(nonzero) == 30 and len(zero) == 6
    assert {row["centered_frequency_s"] for row in records} == {-3, -2, -1, 0, 1, 2}
    assert all(row["gaussian_failure_exponent_numerator_s_squared"] > 0 for row in nonzero)
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "component_count": len(records),
        "nonzero_frequency_count": len(nonzero),
        "zero_frequency_count": len(zero),
        "all_30_nonzero_components_have_positive_gaussian_laplace_exponent": True,
        "zero_modes_do_not_supply_a_uniform_36_component_rule": True,
    }


def gaussian_asymptotic() -> dict[str, object]:
    return {
        "epistemic_status": "PROVED",
        "model_half_tail": "integral_0^infinity exp(-epsilon*t^2+B*abs(alpha)*t) dt",
        "completion_of_square": "-epsilon*(t-B*abs(alpha)/(2*epsilon))^2+B^2*alpha^2/(4*epsilon)",
        "asymptotic": "~sqrt(pi/epsilon)*exp(B^2*alpha^2/(4*epsilon)) as epsilon->0+ for alpha!=0",
        "source_coefficient_status": "The multiplied constant tail coefficient is nonzero, so it cannot remove the positive exponential scale without a forbidden subtraction.",
        "fixed_gaussian_abel_limit_for_nonzero_alpha": "DOES_NOT_EXIST_AS_A_FINITE_RAW_LIMIT",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    ledger = all_component_ledger()
    result = {
        "schema": "sic-stark-cycle-197-gaussian-abel-tail-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "For the one frozen even scalar Gaussian Abel cutoff on the fixed central contour, every one of the 30 nonzero real endpoint Fourier components has a positive exact 1/epsilon Laplace exponent from a nonzero source tail. Thus this Gaussian family supplies no finite uniform raw 36-component endpoint limit. The six zero modes are separate and do not repair that failure. This excludes neither another regulator nor any distributional, analytic-frequency, AFK, boundary, fusion, Stark, or TCC construction.",
        "endpoint_constants": endpoint_constants(),
        "component_ledger": ledger,
        "gaussian_asymptotic": gaussian_asymptotic(),
        "gate_outcome": {
            "fixed_even_gaussian_abel": "FALSIFIED_FOR_UNIFORM_RAW_36_COMPONENT_ENDPOINT_LIMIT",
            "scope": "one fixed scalar Gaussian family on raw real endpoint frequencies and the sealed central contour",
        },
        "next_unresolved_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": "A source-derived frequency-continued, Fresnel/tilted, or genuinely distributional endpoint rule may still control the regular part; it must not be selected after inspecting the Gaussian failure.",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
