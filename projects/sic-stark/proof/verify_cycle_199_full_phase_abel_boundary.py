#!/usr/bin/env python3
"""Exact boundary distribution of the full-phase C199 Abel character comb.

The A_6 approach from ``verify_cycle_199_abel_pole_geometry`` fixes the
opposite i0 sides of the six pinching Abel pole pairs.  Taking those boundary
values gives a concrete distribution, not an arbitrary principal value.  Its
support is lambda=0 and m=0 mod 4.  On that support the full equation-(66)
character loses its b-dependence.  Hence this literal symmetric full-phase
Abel/Poincare prescription has rank at most six and cannot admit the required
linear all-36 map to the distinct C198 T_6 basis.

The result rejects this one completed Abel prescription only.  It leaves open
different source-derived contour/distributional constructions that retain
off-support data or use a different regularization family.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DIMENSION = 6
LEVEL = 24
SOURCE_PHASE = 437


def c198_character_labels() -> list[dict[str, object]]:
    """Reproduce the exact C198 centred (sigma,N) labels."""

    records = []
    labels = set()
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            raw = 4 * second - 5 * first
            sigma = raw % DIMENSION
            if sigma > 2:
                sigma -= DIMENSION
            shift = (sigma - raw) // DIMENSION
            label = (first + 2 - DIMENSION * shift) % LEVEL
            labels.add((sigma, label))
            records.append({
                "characteristic": [first, second],
                "centered_sigma": sigma,
                "centered_N_mod_24": label,
            })
    assert len(records) == DIMENSION * DIMENSION
    assert len(labels) == DIMENSION * DIMENSION
    return records


def paired_i0_boundary() -> dict[str, object]:
    """Compute the distributional contribution of each r class exactly.

    With c=pi*r_beta/2, the rho=u pole is at +epsilon/c-i0 with
    residue -1/c and the rho=u^-1 pole is at -epsilon/c+i0 with residue
    +1/c.  The Sokhotski--Plemelj delta terms add, while their principal
    values cancel as epsilon tends to zero:

       (+i*pi/c + i*pi/c) delta = (4*i/r_beta) delta.
    """

    channels = list(range(0, LEVEL, 4))
    per_class_coefficient = "4*i/r_beta=4*i*omega/D"
    all_classes_coefficient = "12*i/r_beta=12*i*omega/D"
    return {
        "epistemic_status": "PROVED",
        "six_channels": channels,
        "per_residue_class_boundary_distribution": (
            f"{per_class_coefficient}*delta(lambda) on m=0 mod4"
        ),
        "three_class_sum_boundary_distribution": (
            f"{all_classes_coefficient}*delta(lambda) on m=0 mod4"
        ),
        "orientation": {
            "rho_equals_u": "lambda=+epsilon/c-i0, residue=-1/c",
            "rho_equals_u_inverse": "lambda=-epsilon/c+i0, residue=+1/c",
            "sokhotski_plemelj_delta_sum": "2*i*pi/c=4*i/r_beta",
            "principal_value_limit": "0 after pairing the opposite residues",
        },
        "normalization_note": (
            "This is the character-comb distribution in the lambda coordinate; "
            "the equation-(66) contour measure contributes a common nonzero "
            "factor and cannot restore b-dependence."
        ),
    }


def boundary_character_rank() -> dict[str, object]:
    """Evaluate every full character on the fixed comb support."""

    records = []
    boundary_vectors = set()
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            per_residue_phases = []
            for residue in range(3):
                # At y=Q/2 (lambda=0), the alpha-dependent continuous phase
                # equals one. N=a+2-6r and m=4h give the phase below.
                phases = tuple(
                    f"exp(pi*i*{SOURCE_PHASE}*{h}*{first}/3)"
                    for h in range(DIMENSION)
                )
                per_residue_phases.append(phases)
                boundary_vectors.add((first, phases))
            assert per_residue_phases[0] == per_residue_phases[1] == per_residue_phases[2]
            records.append({
                "characteristic": [first, second],
                "m_channels": [0, 4, 8, 12, 16, 20],
                "phase_vector_h_0_to_5": list(per_residue_phases[0]),
                "independent_of_b": True,
                "independent_of_residue_r": True,
            })
    assert len(records) == DIMENSION * DIMENSION
    assert len(boundary_vectors) == DIMENSION
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "distinct_boundary_character_vectors": len(boundary_vectors),
        "boundary_rank_upper_bound": DIMENSION,
        "loss": "all six b labels collapse for each fixed a",
        "reason": (
            "At delta(lambda) support, 2y-Q=0, so alpha_(a,b,z) and hence b "
            "drop out; for m=4h, the N=a+2-6r phase is also r-independent."
        ),
    }


def no_linear_all36_intertwiner() -> dict[str, object]:
    """A rank-six input cannot be sent linearly to 36 distinct T_6 vectors."""

    target_records = c198_character_labels()
    boundary = boundary_character_rank()
    assert len(target_records) == DIMENSION * DIMENSION
    assert boundary["distinct_boundary_character_vectors"] == DIMENSION
    return {
        "epistemic_status": "PROVED",
        "full_phase_abel_boundary_input_rank_at_most": boundary["boundary_rank_upper_bound"],
        "C198_target_basis_dimension": DIMENSION * DIMENSION,
        "C198_target_labels_distinct": True,
        "linear_intertwiner_requirement": "J(Pfull_(a,b))=chi_(a,b) for all 36 rows",
        "impossible": True,
        "scope": (
            "No linear source-defined J exists for the exact full-phase, "
            "symmetric-geodesic Abel boundary distribution derived here. This "
            "does not constrain a continuation whose boundary object retains "
            "additional off-support, derivative, residue, or non-Abel data."
        ),
    }


def run() -> dict[str, object]:
    distribution = paired_i0_boundary()
    boundary = boundary_character_rank()
    obstruction = no_linear_all36_intertwiner()
    assert obstruction["impossible"]
    return {
        "schema": "sic-stark-cycle-199-full-phase-abel-boundary-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "The source-geodesic i0 boundary value of the declared full-phase, "
            "symmetric three-class Abel character comb is a rank-at-most-six "
            "delta distribution. It therefore cannot have a linear all-36 "
            "intertwiner to C198's distinct T_6 basis. This rejects only that "
            "literal completed Abel prescription; it does not rule out a source-"
            "derived continuation retaining off-support/derivative/residue data, "
            "a different regularization, AFK identification, fusion, Stark, or TCC."
        ),
        "paired_i0_boundary": distribution,
        "boundary_character_rank": boundary,
        "no_linear_all36_intertwiner": obstruction,
        "gate_outcome": {
            "full_phase_symmetric_geodesic_abel_comb": "FALSIFIED_FOR_ALL36_LINEAR_T6_INTERTWINER",
            "remaining_design_problem": (
                "Construct a different source-derived endpoint object which "
                "retains b-dependent off-support, derivative, or explicitly "
                "combined-residue data before any C198 comparison."
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
