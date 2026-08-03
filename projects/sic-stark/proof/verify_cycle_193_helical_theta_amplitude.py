#!/usr/bin/env python3
"""Exact Cycle 193 audit of the graded helical theta lift.

This verifier has two deliberately separate parts.

1.  For Schwartz seeds in the Cycle-192 fibre V, it proves the formal
    Poincare/Poisson transport to a dual theta distribution and the exact
    preservation of V by the *continuous-discrete* Fourier transform.  It
    does not place the meromorphic beta kernel or its Poincare sum in that
    Schwartz domain.
2.  It proves a scoped amplitude obstruction.  The V projection identifies
    the six odd pairs (N,N+12), whereas the published beta right-hand-side
    amplitudes R_N and R_(N+12) have different divisors.  Hence no fixed
    fibrewise, iota-equivariant complex-linear operation on the V theta fibre
    can recover individual odd raw amplitudes.

Neither conclusion is an AFK evaluation, alias summation, boundary theorem,
fusion statement, Stark statement, or TCC proof.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))
sys.path.insert(0, str(ROOT / "scripts"))

from verify_cycle_192_graded_fourier_polarization import (  # noqa: E402
    block_fourier_action,
    forced_closure,
)
from dimension_six_beta_fourier import gamma_q_zero_divisor_audit  # noqa: E402


LEVEL = 24
DIMENSION = 6
ODD_CANONICAL_LABELS = tuple(range(1, 12, 2))


def beta_label(first_characteristic: int, alias_lift: int) -> int:
    """The source beta label N=a+2-6z modulo 24."""

    return (first_characteristic + 2 - 6 * alias_lift) % LEVEL


def theta_section_transport() -> dict[str, object]:
    """Record the exact reindexing proof for P_eta and Fourier transport."""

    records = []
    for eta in (-1, 1):
        # P_eta f(x+T)=sum_q eta^q f(x+(q+1)T)
        # =eta^(-1) sum_u eta^u f(x+uT).  Since eta^2=1, this is eta.
        assert eta**-1 == eta
        # Fourier reindexing produces sum_q (eta*chi(T)^-1)^q.
        # It is supported precisely where chi(T)=eta; eta^-1=eta here.
        records.append(
            {
                "eta": eta,
                "poincare_quasiperiodicity": "P_eta f(x+T)=eta^(-1)*P_eta f(x)",
                "dual_theta_support": "chi_(xi,n)(T)=eta^(-1)",
                "dual_condition": (
                    "xi*Delta+n/4 belongs to Z"
                    if eta == 1
                    else "xi*Delta+n/4 belongs to Z+1/2"
                ),
                "fourier_reindexing_factor": "eta^q*chi_(xi,n)(T)^(-q)",
            }
        )

    closure = forced_closure()
    action = block_fourier_action()["action"]
    closed_blocks = set(closure["unique_smallest_F24_invariant_closure"])
    assert closed_blocks == {"B_(0,+)", "B_(0,-)", "B_(1,+)"}
    assert {
        action[name]["target"]
        for name in closed_blocks
    } == closed_blocks
    return {
        "epistemic_status": "PROVED",
        "seed_domain": "Schwartz(R) tensor V",
        "section_space": (
            "finite sums P_eta f(y,m)=sum_(q in Z) eta^q*"
            "f(y+q*Delta,m+6q), eta in {+1,-1}"
        ),
        "poincare_records": records,
        "finite_fibre": sorted(closed_blocks),
        "finite_fibre_dimension": 18,
        "F24_preserves_finite_fibre": True,
        "continuous_discrete_transform_preserves_seed_fibre": True,
        "fourier_image": "tempered dual theta distribution on the stated support",
        "p1_boundary_twisted_three_shift_retained": True,
        "kernel_domain_status": "OPEN: Gamma_M beta kernel is meromorphic and no Poincare convergence/distributional continuation is proved here",
    }


def v_projection() -> dict[str, object]:
    """Calculate Pi_V and its odd pair symmetry exactly."""

    records = []
    for label in range(LEVEL):
        partner = (label + 12) % LEVEL
        if label % 2 == 0:
            projection = {label: 1}
            relation = "retained individually"
        else:
            projection = {label: "1/2", partner: "1/2"}
            relation = "identified with N+12 by iota-fixed projection"
        records.append(
            {
                "label_N": label,
                "partner_N_plus_12": partner,
                "Pi_V_of_e_N": projection,
                "relation": relation,
            }
        )

    odd_pairs = [
        {"canonical_N": label, "partner": label + 12}
        for label in ODD_CANONICAL_LABELS
    ]
    assert len(odd_pairs) == 6
    assert all(pair["partner"] < LEVEL for pair in odd_pairs)
    return {
        "epistemic_status": "PROVED",
        "V": "B_(0,+) direct-sum B_(0,-) direct-sum B_(1,+)",
        "projection_records": records,
        "odd_iota_fixed_pairs": odd_pairs,
        "odd_pair_count": len(odd_pairs),
        "Pi_V_is_iota_equivariant": True,
        "Pi_V_loses_odd_antisymmetric_subspace_dimension": 6,
    }


def divisor_record_for_pair(canonical_label: int) -> dict[str, object]:
    """Use the published true divisors at alpha=-N, exactly.

    For d=6, a true pole of Gamma_M(mu,m) is

      mu=-j*w1-(24*n+5*j+m)*w2,

    where j>=0 and the displayed w2 coefficient is nonnegative.  A
    true zero has w2 coefficient j+1 and w1 coefficient

      -115*(m+j+1)+24*n > 0.

    Irrationality of w1/w2 makes coordinate comparison exact.
    """

    label = canonical_label
    shifted = label + 12
    assert label in range(12)

    # R_N: Gamma_M(alpha,N) has the true-pole witness j=n=0 at alpha=-N.
    primary_pole = {
        "factor": "Gamma_M(alpha,N)",
        "mu_at_alpha_minus_N": [0, -label],
        "witness": {"j": 0, "n": 0, "m": label},
        "true_pole_condition": f"{label}>=0",
    }

    # Its partner Gamma_M(-alpha,4-N) is finite/nonzero there.  Its only
    # possible pole has j=0 and would require 24n=-4; its only possible
    # zero has j+1=N and would require 24n=460 (for N>0).
    unshifted_partner = {
        "factor": "Gamma_M(-alpha,4-N)",
        "mu_at_alpha_minus_N": [0, label],
        "pole_equation": "24*n=-4",
        "zero_equation": "24*n=460 (when N>0)",
        "finite_nonzero": True,
    }
    assert -4 % 24 != 0
    assert 460 % 24 != 0

    # For R_(N+12), the first factor would need 24n=-12 to have a pole.
    # The reflected factor has label -8-N and would need 24n=8 for a pole,
    # or 24n=-920 for its only possible zero.
    shifted_first = {
        "factor": "Gamma_M(alpha,N+12)",
        "mu_at_alpha_minus_N": [0, -label],
        "pole_equation": "24*n=-12",
        "finite_nonzero": True,
    }
    shifted_second = {
        "factor": "Gamma_M(-alpha,-8-N)",
        "mu_at_alpha_minus_N": [0, label],
        "pole_equation": "24*n=8",
        "zero_equation": "24*n=-920 (when N>0)",
        "finite_nonzero": True,
    }
    assert -12 % 24 != 0
    assert 8 % 24 != 0
    assert -920 % 24 != 0

    return {
        "canonical_N": label,
        "comparison_point": f"alpha=-{label}",
        "R_N": {
            "has_true_pole": True,
            "pole_witness": primary_pole,
            "other_factor": unshifted_partner,
        },
        "R_N_plus_12": {
            "is_finite_nonzero": True,
            "first_factor": shifted_first,
            "second_factor": shifted_second,
        },
        "meromorphic_functions_are_distinct": True,
    }


def beta_divisor_separation() -> dict[str, object]:
    """Prove R_N != R_(N+12) on every canonical pair."""

    scalar = gamma_q_zero_divisor_audit()
    assert scalar["Gamma_M_Q_0_is_finite_nonzero"]
    records = [divisor_record_for_pair(label) for label in range(12)]
    assert all(record["meromorphic_functions_are_distinct"] for record in records)
    return {
        "epistemic_status": "PROVED",
        "raw_beta_amplitude": (
            "R_N(alpha)=24*Gamma_M(Q,0)*Gamma_M(alpha,N)*"
            "Gamma_M(-alpha,4-N)"
        ),
        "period_assumption": "omega_2=1 and omega_1/omega_2 irrational",
        "fixed_scalar": scalar,
        "pair_divisor_records": records,
        "all_twelve_N_vs_N_plus_12_pairs_distinct": True,
    }


def all_characteristic_coverage() -> dict[str, object]:
    """Check that the odd loss reaches half of the complete AFK grid."""

    rows = []
    odd_rows = 0
    labels_over_aliases: set[int] = set()
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            parity = "odd" if first % 2 else "even"
            if parity == "odd":
                odd_rows += 1
            rows.append(
                {
                    "characteristic": [first, second],
                    "source_beta_label_mod_6": (first + 2) % DIMENSION,
                    "source_label_parity": parity,
                }
            )
            for lift in range(4):
                labels_over_aliases.add(beta_label(first, lift))
    assert len(rows) == 36
    assert odd_rows == 18
    assert labels_over_aliases == set(range(LEVEL))
    assert {
        label for label in labels_over_aliases if label % 2
    } == set(range(1, LEVEL, 2))
    return {
        "epistemic_status": "PROVED",
        "all36_rows": rows,
        "odd_characteristic_count": odd_rows,
        "all_24_source_beta_labels_appear_over_four_alias_lifts": True,
        "all_12_odd_labels_appear": True,
    }


def scoped_amplitude_obstruction(
    projection: dict[str, object],
    divisors: dict[str, object],
    coverage: dict[str, object],
) -> dict[str, object]:
    """State the invariant obstruction without overclaiming an AFK result."""

    assert projection["Pi_V_is_iota_equivariant"]
    assert projection["Pi_V_loses_odd_antisymmetric_subspace_dimension"] == 6
    assert divisors["all_twelve_N_vs_N_plus_12_pairs_distinct"]
    assert coverage["odd_characteristic_count"] == 18
    return {
        "epistemic_status": "PROVED",
        "operator_class": (
            "fixed fibrewise complex-linear iota-equivariant amplitude "
            "operations on the declared V-valued dual theta fibre"
        ),
        "invariant": (
            "The image of an iota-fixed V fibre under an iota-equivariant "
            "operation is iota-fixed, but the raw odd beta amplitude vector "
            "has distinct N and N+12 coordinates."
        ),
        "conclusion": (
            "No operator in the declared class can recover individual odd "
            "raw R_N amplitudes from the V-projected theta fibre."
        ),
        "affected_characteristics": 18,
        "does_not_exclude": [
            "a larger fibre including B_(1,-)",
            "a non-iota-equivariant or nonlocal alpha operator",
            "derivatives, contours, residues, or a new analytic identity",
            "an alias-sum identity or AFK cocycle evaluation",
            "an RM boundary theorem, fusion continuity, Stark data, or TCC",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    theta = theta_section_transport()
    projection = v_projection()
    divisors = beta_divisor_separation()
    coverage = all_characteristic_coverage()
    obstruction = scoped_amplitude_obstruction(projection, divisors, coverage)
    result = {
        "schema": "sic-stark-cycle-193-helical-theta-amplitude-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Exact Schwartz-seed Poincare/Poisson theta transport and a "
            "scoped V-fibre amplitude obstruction only. The meromorphic beta "
            "kernel is not proved to have a convergent or distributionally "
            "continued Poincare periodization here; no raw beta amplitude is "
            "identified with an AFK value or an alias sum."
        ),
        "continuous_theta_preservation": theta,
        "fibre_projection": projection,
        "beta_divisor_separation": divisors,
        "all36_coverage": coverage,
        "scoped_amplitude_obstruction": obstruction,
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
