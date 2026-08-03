#!/usr/bin/env python3
"""Exact correction audit for Cycle 194's true-pole collision orbit.

The v1 verifier solved equality of affine divisor coordinates but did not
enforce the additional source condition for a *true* Gamma_M pole.  This
replay enforces it before every collision/residue statement.  It deliberately
does not decide cancellation of the resulting finite combined residues or an
RM-endpoint value.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from verify_cycle_194_meromorphic_anti_channel import (
    ODD_CANONICAL_LABELS,
    forced_anti_fibre,
    spectral_anti_retention,
)


LEVEL = 24


def true_primary_pole(*, j: int, n: int, m: int) -> bool:
    """S--S (9): true primary Gamma_M pole, for k=24 and r=5."""

    return j >= 0 and LEVEL * n + 5 * j + m >= 0


def reflected_factor_is_finite_nonzero(label: int, depth: int) -> dict[str, object]:
    """Check the other beta factor at the shared first-factor pole.

    At the depth-k point the first gamma has
      alpha = -k*omega_1 -(N-k),  m=N+18k.
    The reflected gamma is evaluated at
      mu = k*omega_1 +(N-k),  m_ref=4-N-18k.
    A reflected pole is impossible from its omega_1 coefficient.  A zero
    would force j=N-k-1 and then 24*n=460-2184*k, which is never integral
    because the right-hand side is 4 mod 24.
    """

    assert 0 <= depth <= label
    zero_j = label - depth - 1
    zero_numerator = 460 - 2184 * depth
    assert zero_numerator % LEVEL == 4
    return {
        "reflected_mu": f"{depth}*omega_1+({label}-{depth})",
        "reflected_discrete_label": 4 - label - 18 * depth,
        "pole_reason": "-j=depth has no j>=0 solution unless depth=0; at depth=0 its constant equation is 24*n=-4",
        "zero_candidate_j": zero_j,
        "zero_equation": f"24*n={zero_numerator}",
        "zero_equation_mod_24": zero_numerator % LEVEL,
        "finite_nonzero": True,
    }


def finite_true_pole_orbit(label: int) -> dict[str, object]:
    """Classify the collision orbit over the base `(z,j,n)=(0,0,0)`.

    Affine equality gives `(z,j,n)=(-3k,k,-k)`.  With
    `m=N-6z=N+18k`, the true-pole inequality is precisely `N-k>=0`.
    """

    assert label in ODD_CANONICAL_LABELS
    members = []
    for depth in range(label + 1):
        z, j, n = -3 * depth, depth, -depth
        m = label - 6 * z
        inequality = LEVEL * n + 5 * j + m
        assert inequality == label - depth
        assert true_primary_pole(j=j, n=n, m=m)
        members.append(
            {
                "depth_k": depth,
                "alias_index_z": z,
                "first_gamma_indices": {"j": j, "n": n, "m": m},
                "true_pole_inequality": f"24*n+5*j+m={inequality}",
                "reflected_factor": reflected_factor_is_finite_nonzero(label, depth),
                "individual_simple_residue_nonzero": True,
            }
        )
    rejected_depth = label + 1
    rejected_m = label + 18 * rejected_depth
    rejected_inequality = -1
    assert LEVEL * (-rejected_depth) + 5 * rejected_depth + rejected_m == rejected_inequality
    assert not true_primary_pole(j=rejected_depth, n=-rejected_depth, m=rejected_m)
    return {
        "canonical_odd_N": label,
        "affine_collision_law": "(z,j,n)=(-3k,k,-k) over the base pole",
        "true_pole_rule": "24*n+5*j+m>=0",
        "substitution": "m=N-6z=N+18k, hence 24*n+5*j+m=N-k",
        "admissible_depths": list(range(label + 1)),
        "true_pole_orbit_cardinality": label + 1,
        "members": members,
        "first_rejected_depth": rejected_depth,
        "first_rejected_indices": {"z": -3 * rejected_depth, "j": rejected_depth, "n": -rejected_depth, "m": rejected_m},
        "first_rejected_inequality": rejected_inequality,
        "infinite_true_pole_tail_exists": False,
    }


def corrected_collision_census() -> dict[str, object]:
    records = [finite_true_pole_orbit(label) for label in ODD_CANONICAL_LABELS]
    cardinalities = [record["true_pole_orbit_cardinality"] for record in records]
    assert cardinalities == [2, 4, 6, 8, 10, 12]
    assert sum(cardinalities) == 42
    return {
        "epistemic_status": "PROVED",
        "source_condition": "Sarkissian--Spiridonov arXiv:1910.11747v4 equations (9)--(10): 24*n+5*j+m>=0",
        "records": records,
        "orbit_cardinalities": cardinalities,
        "total_true_pole_summands": sum(cardinalities),
        "combined_residue_status": "OPEN: each finite summand is nonzero, but no cancellation theorem for their finite sums is claimed",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {
        "schema": "sic-stark-cycle-194-meromorphic-anti-channel-correction-v2-prototype",
        "epistemic_status": "PROVED",
        "claim_boundary": "This correction enforces the source true-pole inequality on the C194 affine collision relation. It retains local source-forced anti-principal parts and spectral retention, proves finite collision orbits and nonzero individual residues, and withdraws the v1 infinite-tail/convergence/sector claims. It proves no finite combined-residue noncancellation, endpoint continuation, AFK identification, boundary value, fusion, Stark, or TCC result.",
        "retained_v1_results": {
            "forced_anti_fibre": forced_anti_fibre(),
            "spectral_anti_retention": spectral_anti_retention(),
        },
        "corrected_true_pole_census": corrected_collision_census(),
        "withdrawn_v1_claims": [
            "infinite coincident-pole residue orbit",
            "strict-interior residue-tail convergence from that orbit",
            "non-identically-zero sector conclusion derived from that tail",
        ],
        "next_unresolved_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": "A source-derived finite combined-residue rule and distributional or contour continuation of the 24D channel to the RM endpoint may preserve the anti-channel; no such result is supplied by the finite true-pole census.",
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
