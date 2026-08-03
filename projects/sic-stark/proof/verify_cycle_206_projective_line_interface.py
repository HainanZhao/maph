#!/usr/bin/env python3
"""Exact projective normal-packet audit for Cycle 206/B043.

The rank-36 regular normal coefficient has one common Abel-rate line.  After
quotienting that line, the full packet has denominator-free homogeneous
coordinates.  This verifier proves their exact source relations and A6
projective covariance.  It deliberately does *not* turn the label-matched
C198 endpoint vector into an amplitude equality: equation (66) supplies a
linear endpoint transform, not the requisite multiplicative binomial law.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

try:  # Supports package tests and direct proof-script replay.
    from proof.verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger
except ModuleNotFoundError:
    from verify_cycle_198_analytic_frequency_endpoint import characteristic_ledger


DIMENSION = 6
DILATIONS = (2, 3, 5)
A6 = ((115, -24), (24, -5))


def packet_monomial(first: int, second: int, channel: int) -> dict[str, object]:
    """Encode one nonzero packet without choosing a value of t or h."""

    assert all(0 <= value < DIMENSION for value in (first, second, channel))
    return {
        "characteristic": [first, second],
        "h_channel": channel,
        "zeta_6_exponent_mod_6": (5 * channel * first) % DIMENSION,
        "t_exponent": 4 * second - 5 * first,
        "common_factor": "1+t^6+t^12",
        "packet": (
            f"zeta_6^({5 * channel * first})*t^({4 * second - 5 * first})*"
            "(1+t^6+t^12)"
        ),
    }


def source_projective_packet() -> dict[str, object]:
    """Retain all labelled source coordinates before any affine quotient."""

    records = [
        packet_monomial(first, second, channel)
        for channel in range(DIMENSION)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    ]
    assert len(records) == DIMENSION**3
    assert all(record["common_factor"] == "1+t^6+t^12" for record in records)
    return {
        "epistemic_status": "PROVED",
        "normal_vector": "R_(a,b;h)=lambda*P_(a,b;h)(t)",
        "lambda_action": "lambda->q*lambda for q in {2,3,5}",
        "coordinate_count_per_h": DIMENSION * DIMENSION,
        "h_channel_count": DIMENSION,
        "total_labelled_packet_count": len(records),
        "coordinates": records,
        "common_factor_base_locus": "1+t^6+t^12=0",
        "declared_real_source_locus": "t>0, hence 1+t^6+t^12>0 and lambda!=0",
        "projective_object": (
            "For each unselected h and unselected t on the non-base declared "
            "source locus, [P_(a,b;h)(t)]_(a,b) in P^35; no affine coordinate, "
            "component denominator, or t/h specialization is chosen."
        ),
    }


def elementary_binomial_ledger() -> dict[str, object]:
    """Prove all frozen denominator-free 2-by-2 source relations."""

    records = []
    for channel in range(DIMENSION):
        for first in range(DIMENSION - 1):
            for second in range(DIMENSION - 1):
                nw = packet_monomial(first, second, channel)
                se = packet_monomial(first + 1, second + 1, channel)
                ne = packet_monomial(first, second + 1, channel)
                sw = packet_monomial(first + 1, second, channel)
                lhs_phase = (nw["zeta_6_exponent_mod_6"] + se["zeta_6_exponent_mod_6"]) % DIMENSION
                rhs_phase = (ne["zeta_6_exponent_mod_6"] + sw["zeta_6_exponent_mod_6"]) % DIMENSION
                lhs_t = nw["t_exponent"] + se["t_exponent"]
                rhs_t = ne["t_exponent"] + sw["t_exponent"]
                assert lhs_phase == rhs_phase
                assert lhs_t == rhs_t
                records.append({
                    "h_channel": channel,
                    "square": [[first, second], [first + 1, second + 1]],
                    "homogeneous_relation": (
                        f"P_({first},{second};{channel})*P_({first + 1},{second + 1};{channel})"
                        f"-P_({first},{second + 1};{channel})*P_({first + 1},{second};{channel})=0"
                    ),
                    "phase_exponents_mod_6": [lhs_phase, rhs_phase],
                    "t_exponents": [lhs_t, rhs_t],
                    "common_factor_power_each_term": 2,
                    "identically_zero": True,
                })
    assert len(records) == DIMENSION * (DIMENSION - 1) ** 2
    assert all(record["identically_zero"] for record in records)
    return {
        "epistemic_status": "PROVED",
        "relation_count": len(records),
        "per_h_relation_count": (DIMENSION - 1) ** 2,
        "denominator_free": True,
        "all_relations_identically_zero": True,
        "records": records,
        "interpretation": (
            "Each fixed-h source coordinate array is rank one on its frozen "
            "5-by-5 elementary-square census. This is a projective source "
            "constraint on the non-base locus, not a target-amplitude identity."
        ),
    }


def common_line_covariance() -> dict[str, object]:
    """Audit regulator and A6 actions that act by a single scalar line."""

    dilation_records = []
    for q in DILATIONS:
        dilation_records.append({
            "q": q,
            "normal_vector_action": "R->q*R",
            "degree_one_projective_class": "[q*R]=[R]",
            "degree_two_binomial_action": "B->q^2*B=0",
            "projectively_invariant": True,
        })
    a6_records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            image = (
                (A6[0][0] * first + A6[0][1] * second) % DIMENSION,
                (A6[1][0] * first + A6[1][1] * second) % DIMENSION,
            )
            assert image == (first, second)
            a6_records.append({
                "characteristic": [first, second],
                "A6_characteristic_mod_6": list(image),
                "source_normal_line_action": "R->beta^(-6)*R",
                "projective_class_action": "[beta^(-6)*R]=[R]",
            })
    assert len(a6_records) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "dilation_records": dilation_records,
        "A6": [list(row) for row in A6],
        "A6_mod_6": [[1, 0], [0, 1]],
        "A6_axis_action": "s->beta^(-6)*s",
        "A6_multiplier_square": "psi^2(A6)=-1",
        "all_36_label_records": a6_records,
        "source_projective_covariance": "PROVED",
        "scope": (
            "The A6 statement is a common normal-line/projective source action. "
            "It is not an equation-(66) amplitude transformation law."
        ),
    }


def c198_projective_comparison() -> dict[str, object]:
    """State exactly what the frozen C198 theorem does and does not provide."""

    endpoint = characteristic_ledger()
    rows = endpoint["records"]
    assert len(rows) == DIMENSION * DIMENSION
    assert all(row["endpoint_value_finite_nonzero"] for row in rows)
    target_records = []
    for first in range(DIMENSION - 1):
        for second in range(DIMENSION - 1):
            by_label = {tuple(row["characteristic"]): row for row in rows}
            nw = by_label[(first, second)]["endpoint_value"]
            se = by_label[(first + 1, second + 1)]["endpoint_value"]
            ne = by_label[(first, second + 1)]["endpoint_value"]
            sw = by_label[(first + 1, second)]["endpoint_value"]
            target_records.append({
                "square": [[first, second], [first + 1, second + 1]],
                "homogeneous_target_expression": f"({nw})*({se})-({ne})*({sw})",
                "identity_status": "NOT_SUPPLIED_BY_FROZEN_C198_LINEAR_TRANSFORM",
            })
    assert len(target_records) == (DIMENSION - 1) ** 2
    return {
        "epistemic_status": "PROVED",
        "all_36_targets_finite_nonzero": True,
        "ordered_label_match_to_source": True,
        "target_projective_point_defined": "[L_(a,b)] in P^35",
        "target_elementary_binomial_count": len(target_records),
        "target_elementary_binomials": target_records,
        "frozen_c198_theorem_type": "unique source-derived linear endpoint transform on T_6",
        "provided_multiplicative_binomial_law": False,
        "comparison_status": "OPEN_REQUIRES_NEW_SOURCE_MULTIPLICATIVE_THEOREM",
        "reason": (
            "The frozen equation-(66) result gives labelled, finite, nonzero "
            "values and linearity on T_6. It does not assert that its values "
            "obey the 25 target binomials, or identify them with the source "
            "normal packet's homogeneous coordinates."
        ),
        "scope": (
            "This is an exact statement about the content of the frozen C198 "
            "interface, not a claim that no multiplicative identity exists."
        ),
    }


def run() -> dict[str, object]:
    source = source_projective_packet()
    binomials = elementary_binomial_ledger()
    covariance = common_line_covariance()
    comparison = c198_projective_comparison()
    assert source["coordinate_count_per_h"] == 36
    assert binomials["relation_count"] == 150
    assert covariance["source_projective_covariance"] == "PROVED"
    assert comparison["comparison_status"] == "OPEN_REQUIRES_NEW_SOURCE_MULTIPLICATIVE_THEOREM"
    return {
        "schema": "sic-stark-cycle-206-projective-line-interface-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The rank-36 regular source packet has a denominator-free labelled "
            "projective normal-line quotient with 150 exact elementary source "
            "binomials and common-line A6 covariance on 1+t^6+t^12!=0 (in "
            "particular on its declared real source locus). The frozen C198 endpoint "
            "ledger supplies an ordered nonzero projective target point, but no "
            "multiplicative equation identifying its homogeneous coordinates "
            "with the source packet. Thus this proves a source projective object "
            "while leaving the proposed projective interface equality open, rather than proving "
            "an AFK amplitude identity, fusion, Stark, or TCC."
        ),
        "source_projective_packet": source,
        "elementary_binomial_ledger": binomials,
        "common_line_covariance": covariance,
        "c198_projective_comparison": comparison,
        "gate_outcome": {
            "source_projective_normal_packet": "PROVED_ALL36_DENOMINATOR_FREE_A6_COVARIANT",
            "source_to_c198_projective_equality": "OPEN_REQUIRES_MULTIPLICATIVE_SOURCE_THEOREM",
            "next_design_problem": (
                "Derive a source-authorized multiplicative equation-(66), global "
                "pairing, or projective intertwiner that takes the 150 source "
                "homogeneous relations to exact C198 target relations without a "
                "chosen affine chart, scalar, alias, or ray datum."
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
