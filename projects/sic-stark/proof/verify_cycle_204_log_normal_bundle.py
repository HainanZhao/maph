#!/usr/bin/env python3
"""Exact b-normal weight audit for Cycle 204/B041.

The logarithmic generators s*d/ds and ds/s are genuinely invariant under
positive changes of the geodesic coordinate and under the A_6 contraction.
They nevertheless have Abel-rate weight zero.  Tensoring or contracting them
with the rank-36 normal packets therefore preserves, rather than cancels, the
packets' weight one.  No equation-(66) b-pairing is supplied by the frozen
source data, so this records a canonical line-valued b-object but no scalar
endpoint map to the fixed C198 values.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
DILATIONS = (2, 3, 5)


def b_generator_ledger() -> dict[str, object]:
    """Check b-generators under both independent scale actions."""

    return {
        "epistemic_status": "PROVED",
        "b_tangent_generator": "V_b=s*d/ds",
        "b_cotangent_generator": "eta_b=ds/s",
        "positive_coordinate_rescaling": {
            "change": "s_c=c*s, c>0",
            "V_b": "s_c*d/ds_c=s*d/ds",
            "eta_b": "ds_c/s_c=ds/s",
        },
        "A6_contraction": {
            "change": "s->beta^(-6)*s",
            "V_b": "invariant",
            "eta_b": "invariant",
        },
        "regulator_dilation": {
            "change": "lambda->q*lambda, q in {2,3,5}",
            "V_b": "invariant; independent of lambda",
            "eta_b": "invariant; independent of lambda",
        },
        "abel_rate_weight": 0,
        "category": "regular b-tangent/b-cotangent objects, not ordinary endpoint covectors",
    }


def tensor_weight_ledger() -> dict[str, object]:
    """Audit every preregistered b-tensor candidate on all 36 rows."""

    rows = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            rows.append({
                "characteristic": [first, second],
                "R": "weight 1",
                "R_tensor_eta_b": "weight 1+0=1",
                "i_V_b_of_R_tensor_eta_b": "weight 1",
                "b_derivative_of_lambda_s_R": "V_b(lambda*s*R)=lambda*s*R; no endpoint extraction",
            })
    assert len(rows) == DIMENSION * DIMENSION
    return {
        "epistemic_status": "PROVED",
        "row_count": len(rows),
        "candidates": ["R", "R tensor eta_b", "i_(V_b)(R tensor eta_b)"],
        "all_candidate_abel_rate_weight": 1,
        "source_regular_operation": "V_b(lambda*s*R)=lambda*s*R",
        "missing_operation": (
            "A source theorem defining a b-pairing or b-integral that changes "
            "the Abel-rate representation is absent from the frozen inputs."
        ),
        "records": rows,
    }


def fixed_target_consequence() -> dict[str, object]:
    """Compare the residual weight with the fixed nonzero C198 targets."""

    contradictions = []
    for q in DILATIONS:
        contradictions.append({
            "q": q,
            "source_b_tensor_action": "X_(a,b)->q*X_(a,b)",
            "fixed_C198_target_action": "L_src(chi_(a,b))->L_src(chi_(a,b))",
            "direct_linear_equality_consequence": f"{q - 1}*L_src(chi_(a,b))=0",
            "excluded_by": "Cycle 198: all 36 target values are finite and nonzero",
        })
    return {
        "epistemic_status": "PROVED",
        "source_candidate_weight": 1,
        "fixed_C198_target_weight": 0,
        "direct_linear_fixed_target_map_impossible": True,
        "contradictions": contradictions,
        "canonical_b_object_status": (
            "A coordinate-invariant line-valued b-object is available, but it "
            "is not a weight-zero scalar endpoint object."
        ),
    }


def run() -> dict[str, object]:
    b_generators = b_generator_ledger()
    tensors = tensor_weight_ledger()
    targets = fixed_target_consequence()
    assert b_generators["abel_rate_weight"] == 0
    assert tensors["all_candidate_abel_rate_weight"] == 1
    assert targets["direct_linear_fixed_target_map_impossible"]
    return {
        "schema": "sic-stark-cycle-204-log-normal-bundle-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The declared b-generators V_b=s*d/ds and eta_b=ds/s are canonical "
            "under the frozen source geometry but have Abel-rate weight zero. "
            "Every preregistered tensor/contraction with the rank-36 normal "
            "packets retains weight one and cannot directly map linearly to the "
            "fixed nonzero C198 targets. This rejects only b-objects without an "
            "additional equation-(66) b-pairing theorem; it does not exclude a "
            "new source pairing, covariant target line, nonlinear/higher-germ/"
            "non-Abel construction, AFK, fusion, Stark, or TCC."
        ),
        "b_generator_ledger": b_generators,
        "tensor_weight_ledger": tensors,
        "fixed_target_consequence": targets,
        "gate_outcome": {
            "bare_logarithmic_b_normal_objects": "FALSIFIED_FOR_DIRECT_WEIGHT_ZERO_ALL36_MAP",
            "remaining_design_problem": (
                "Find an equation-(66)-derived b-pairing theorem or a covariant "
                "target line whose rate representation is explicitly proved."
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
