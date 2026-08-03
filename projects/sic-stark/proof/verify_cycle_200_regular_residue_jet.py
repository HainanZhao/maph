#!/usr/bin/env python3
"""Exact source regular/residue ledger for Cycle 200/B037.

The full-phase symmetric Abel comb has two distinct pieces near the endpoint.
Its paired-pole boundary has only even delta jets, which cannot retain six
``b`` labels by order five.  Away from the collision point, however, the
first source Taylor coefficient is an exact common meromorphic factor times
36 independent full-character exponential packets.  This verifies a
rank-capable *off-support response*, not an endpoint distribution or the
missing Zak intertwiner.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
LEVEL = 24
SOURCE_PHASE = 437
MAX_JET_ORDER = 5


def paired_pole_jet_parity() -> dict[str, object]:
    """Derive the parity and information bound of the literal pole sector.

    The two source-geodesically oriented delta terms are proportional to
    ``delta(Lambda-a_s)+delta(Lambda+a_s)``.  Their Taylor series contains
    only even distributional derivatives.  Multiplying by the full character
    can introduce phase powers only up to the derivative order, so orders
    through five provide at most degree four in the six b labels.
    """

    retained_orders = list(range(0, MAX_JET_ORDER + 1, 2))
    assert retained_orders == [0, 2, 4]
    records = []
    for order in retained_orders:
        records.append({
            "delta_derivative_order": order,
            "source_coefficient_status": "possible paired-pole Taylor coefficient",
            "maximum_full_phase_polynomial_degree": order,
            "b_rank_upper_bound": order + 1,
        })
    return {
        "epistemic_status": "PROVED",
        "paired_pole_distribution": "delta(Lambda-a_s)+delta(Lambda+a_s)",
        "retained_orders_through_five": retained_orders,
        "odd_delta_jets_source_forbidden_by_pair_symmetry": True,
        "maximum_b_polynomial_degree_through_order_five": 4,
        "maximum_b_rank_through_order_five": 5,
        "all_a_b_rank_upper_bound_through_order_five": 30,
        "fixed_a_collision_witness": (
            "sum_(b=0)^5 (-1)^(5-b)*binom(5,b)*row_(a,b)=0 for every a; "
            "each retained full-phase coefficient is a polynomial in b of "
            "degree at most four"
        ),
        "records": records,
        "scope": (
            "This bounds the paired pole sector only. It does not discard the "
            "regular off-support Taylor coefficient."
        ),
    }


def first_off_support_coefficient() -> dict[str, object]:
    """Differentiate the exact Abel kernel away from Lambda=0.

    For epsilon=lambda*s and c_s=pi*r_gamma(s)/2,
    A=sinh(epsilon)/(cosh(epsilon)-cosh(c_s*Lambda)).  At nonzero real
    Lambda its first s coefficient is lambda/(1-cosh(c_beta*Lambda)).
    This is a direct source formula; no numerical finite part is used.
    """

    return {
        "epistemic_status": "PROVED",
        "exact_kernel": (
            "A_(exp(-lambda*s))(exp(-c_s*Lambda))="
            "sinh(lambda*s)/(cosh(lambda*s)-cosh(c_s*Lambda))"
        ),
        "domain": "real Lambda != 0, c_beta=pi*D/(2*omega)>0",
        "first_s_coefficient": "lambda/(1-cosh(c_beta*Lambda))",
        "abel_coordinate_coefficient": "1/(1-cosh(c_beta*Lambda))",
        "proof": (
            "sinh(lambda*s)=lambda*s+O(s^3), while the denominator is "
            "1-cosh(c_beta*Lambda)+O(s) on the stated off-support domain."
        ),
        "rate_dependence": (
            "The raw first s coefficient is proportional to lambda. Therefore "
            "it is not a lambda-independent endpoint limit; dividing by "
            "lambda*s defines only the displayed Abel-coordinate Taylor "
            "coefficient, not an endpoint value."
        ),
    }


def full_packet_independence() -> dict[str, object]:
    """Prove rank 36 of the full-character off-support coefficient.

    Put t=exp(-pi*D*Lambda/(36*omega)).  On m=4h, the sum of the three
    residue classes has packet

      zeta_6^(5*h*a) * t^(4*b-5*a) * (1+t^6+t^12).

    The h coordinates are a six-point Fourier basis in a.  After isolating
    a, the six b packets are distinct monomials t^(4b) times one common
    nonzero factor; hence all 36 packets are independent as analytic
    functions on every real interval avoiding Lambda=0.
    """

    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            exponents = [4 * second - 5 * first + 6 * residue for residue in range(3)]
            rows.append({
                "characteristic": [first, second],
                "h_phase": f"zeta_6^(5*h*{first})",
                "t_exponents_for_r_0_1_2": exponents,
                "packet": (
                    f"zeta_6^(5*h*{first})*t^({4 * second - 5 * first})"
                    "*(1+t^6+t^12)"
                ),
            })
    assert len(rows) == DIMENSION * DIMENSION
    for first in range(DIMENSION):
        b_exponents = [row["t_exponents_for_r_0_1_2"][0] for row in rows if row["characteristic"][0] == first]
        assert b_exponents == [-5 * first + 4 * second for second in range(DIMENSION)]
        assert len(set(b_exponents)) == DIMENSION
    return {
        "epistemic_status": "PROVED",
        "variable": "t=exp(-pi*D*Lambda/(36*omega))",
        "m_channels": [0, 4, 8, 12, 16, 20],
        "full_three_residue_packet": (
            "zeta_6^(5*h*a)*t^(4*b-5*a)*(1+t^6+t^12)"
        ),
        "row_count": len(rows),
        "h_phase_matrix": "[zeta_6^(5*h*a)]_(h,a in Z/6Z), a permuted six-point DFT",
        "fixed_a_b_packets": "six distinct monomials t^(4*b) times a common nonzero analytic factor",
        "analytic_function_rank": DIMENSION * DIMENSION,
        "records": rows,
        "scope": (
            "Rank is on the six m=4h channel functions over any real Lambda "
            "interval avoiding the collision. It is not rank of the C199 "
            "delta boundary and does not construct J."
        ),
    }


def run() -> dict[str, object]:
    poles = paired_pole_jet_parity()
    regular = first_off_support_coefficient()
    packets = full_packet_independence()
    assert poles["all_a_b_rank_upper_bound_through_order_five"] == 30
    assert "binom(5,b)" in poles["fixed_a_collision_witness"]
    assert packets["analytic_function_rank"] == 36
    return {
        "schema": "sic-stark-cycle-200-regular-residue-jet-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "For the frozen full-phase symmetric Abel family, the paired pole "
            "sector supplies only even delta jets through order five and has "
            "all-row rank at most 30. Separately, the exact first off-support "
            "source Taylor coefficient contains 36 independent full-character "
            "analytic packets, but its raw coefficient is Abel-rate dependent "
            "and is not an endpoint distribution. This proves neither a "
            "regular-plus-residue endpoint object, a Zak map, C198 amplitude "
            "equality, AFK data, fusion, Stark, nor TCC."
        ),
        "paired_pole_jet_parity": poles,
        "first_off_support_coefficient": regular,
        "full_packet_independence": packets,
        "gate_outcome": {
            "paired_pole_jet_through_order_five": "FALSIFIED_FOR_ALL36_RANK",
            "off_support_full_character_response": "PROVED_RANK_36_BUT_NOT_ENDPOINT_OBJECT",
            "remaining_design_problem": (
                "Derive a source-authorized operation that joins the rank-36 "
                "off-support response to a finite lambda-independent endpoint "
                "object without a fitted finite part or renormalization."
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
