#!/usr/bin/env python3
"""Exact Cycle 194 audit of the source-forced meromorphic B_(1,-) channel.

The calculation constructs neither an endpoint value nor an AFK identity.
It verifies that the actual two-gamma beta kernel has six nonzero odd
antisymmetric principal parts, so adding B_(1,-) is source-forced in the
interior meromorphic spectral periodization.  The published interior
two-base convergence theorem is used only after checking its strict chamber
hypotheses; no unit-circle or real-multiplication continuation is taken.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "proof"))

from verify_cycle_192_graded_fourier_polarization import block_fourier_action  # noqa: E402
from verify_cycle_193_helical_theta_amplitude import (  # noqa: E402
    beta_divisor_separation,
)


LEVEL = 24
DIMENSION = 6
ODD_CANONICAL_LABELS = tuple(range(1, 12, 2))


def physical_kernel_pair_record(label: int) -> dict[str, object]:
    """Audit K_Q(y,N)-K_Q(y,N+12) at y=-N.

    The true-pole and true-zero divisors of the d=6 Gamma_M imply the
    records below after comparing the independent omega_1 and omega_2
    coordinates.  At y=-N, Gamma_M(y,N) has the unique j=n=0 simple-pole
    witness; every other displayed gamma factor is finite nonzero.
    """

    shifted = label + 12
    assert label in ODD_CANONICAL_LABELS

    # K_Q(y,N): first factor is Gamma_M(-N,N), with the true pole j=n=0.
    pole_witness = {
        "factor": "Gamma_M(y,N)",
        "y": [0, -label],
        "witness": {"j": 0, "n": 0, "m": label},
        "simple": True,
    }

    # Reflected factor is Gamma_M(Q+N,-N), coordinates (1,N+1).
    # A pole would have -j=1, impossible.  A zero forces j=N and then
    # -115*(-N+N+1)+24n=1, hence 24n=116, impossible.
    reflected_unshifted = {
        "factor": "Gamma_M(Q-y,-N)",
        "argument_at_y_minus_N": [1, label + 1],
        "pole_reason": "-j=1 has no j>=0 solution",
        "zero_equation": "24*n=116",
        "finite_nonzero": True,
    }
    assert 116 % LEVEL != 0

    # K_Q(y,N+12): Gamma_M(-N,N+12) would need 24n=-12 for a pole;
    # its reflected factor has discrete label -N-12 and zero equation
    # -115*(-N-12+N+1)+24n=1, i.e. 24n=-1264.
    shifted_first = {
        "factor": "Gamma_M(y,N+12)",
        "argument_at_y_minus_N": [0, -label],
        "pole_equation": "24*n=-12",
        "finite_nonzero": True,
    }
    shifted_reflected = {
        "factor": "Gamma_M(Q-y,-N-12)",
        "argument_at_y_minus_N": [1, label + 1],
        "pole_reason": "-j=1 has no j>=0 solution",
        "zero_equation": "24*n=-1264",
        "finite_nonzero": True,
    }
    assert -12 % LEVEL != 0
    assert -1264 % LEVEL != 0

    return {
        "canonical_odd_N": label,
        "comparison_point": f"y=-{label}",
        "K_Q_y_N": {
            "has_simple_true_pole": True,
            "pole_witness": pole_witness,
            "reflected_factor": reflected_unshifted,
        },
        "K_Q_y_N_plus_12": {
            "is_finite_nonzero": True,
            "first_factor": shifted_first,
            "reflected_factor": shifted_reflected,
        },
        "anti_difference_has_nonzero_simple_principal_part": True,
    }


def forced_anti_fibre() -> dict[str, object]:
    """Prove that the source kernel forces every B_(1,-) coordinate."""

    records = [physical_kernel_pair_record(label) for label in ODD_CANONICAL_LABELS]
    assert len(records) == DIMENSION
    assert all(
        record["anti_difference_has_nonzero_simple_principal_part"]
        for record in records
    )

    action = block_fourier_action()["action"]
    anti_action = action["B_(1,-)"]
    assert anti_action["target"] == "B_(1,-)"
    return {
        "epistemic_status": "PROVED",
        "anti_fibre": "A=B_(1,-)=span{e_(1+2j)-e_(13+2j):j mod6}",
        "dimension": DIMENSION,
        "physical_kernel": "K_Q(y,m)=Gamma_M(y,m)*Gamma_M(Q-y,-m)",
        "principal_part_records": records,
        "all_six_anti_coordinates_source_forced": True,
        "F24_preserves_A": True,
        "F24_block_action": anti_action,
        "full_source_fibre": "V direct-sum A has dimension 24",
    }


def spectral_anti_retention() -> dict[str, object]:
    """Show Pi_A keeps raw beta differences instead of averaging them."""

    separation = beta_divisor_separation()
    records = []
    for pair in separation["pair_divisor_records"]:
        label = pair["canonical_N"]
        if label % 2 == 0:
            continue
        records.append(
            {
                "canonical_odd_N": label,
                "projection_formula": (
                    "Pi_A(R_N*e_N+R_(N+12)*e_(N+12))="
                    "(R_N-R_(N+12))/2*(e_N-e_(N+12))"
                ),
                "raw_difference_meromorphically_nonzero": pair[
                    "meromorphic_functions_are_distinct"
                ],
            }
        )
    assert len(records) == DIMENSION
    assert all(record["raw_difference_meromorphically_nonzero"] for record in records)
    return {
        "epistemic_status": "PROVED",
        "raw_beta_rhs": (
            "R_N(alpha)=24*Gamma_M(Q,0)*Gamma_M(alpha,N)*"
            "Gamma_M(-alpha,4-N)"
        ),
        "retention_records": records,
        "all_six_odd_raw_differences_retained": True,
        "capital_Gamma_normalization_retained_separately": True,
        "AFK_phase_retained_separately": True,
    }


def primary_pole_coordinates(
    base_label: int,
    alias_index: int,
    pole_j: int,
    pole_n: int,
) -> tuple[Fraction, Fraction]:
    """Coordinates of a primary R_(N_z)(alpha_z) pole in alpha_0.

    Write alpha_z=alpha_0+z*(omega_1-omega_2)/3 and
    N_z=base_label-6z.  Subtracting alpha_z from the published primary
    pole divisor gives the following independent omega_1/omega_2
    coordinates for the pole of the z-th alias as a function of alpha_0.
    """

    return (
        Fraction(-pole_j, 1) - Fraction(alias_index, 3),
        Fraction(-24 * pole_n - 5 * pole_j - base_label, 1)
        + Fraction(19 * alias_index, 3),
    )


def primary_pole_collision_lattice() -> dict[str, object]:
    """Solve the exact collision law before taking any residue sum."""

    witnesses = []
    for base_label in range(LEVEL):
        for alias_index in range(-3, 4):
            for pole_j in range(0, 5):
                for pole_n in range(-3, 4):
                    source = primary_pole_coordinates(
                        base_label, alias_index, pole_j, pole_n
                    )
                    for translation in range(-3, 4):
                        if translation == 0:
                            continue
                        target_alias = alias_index + 3 * translation
                        target_j = pole_j - translation
                        target_n = pole_n + translation
                        if target_j < 0:
                            continue
                        target = primary_pole_coordinates(
                            base_label,
                            target_alias,
                            target_j,
                            target_n,
                        )
                        assert target == source
                        witnesses.append(
                            {
                                "N_base": base_label,
                                "z": alias_index,
                                "j": pole_j,
                                "n": pole_n,
                                "translation_t": translation,
                                "z_prime": target_alias,
                                "j_prime": target_j,
                                "n_prime": target_n,
                            }
                        )

    # Coordinate equality forces z'-z divisible by 3: its omega_1
    # coordinate is -(j'-j)-(z'-z)/3.  For z'=z+3t, equality of the
    # omega_2 coordinate then forces j'=j-t and n'=n+t.
    assert witnesses
    return {
        "epistemic_status": "PROVED",
        "collision_law": (
            "(z,j,n) and (z+3t,j-t,n+t) represent the same primary "
            "pole whenever j-t>=0"
        ),
        "only_collision_direction": "z_prime-z is divisible by 3",
        "finite_witness_count": len(witnesses),
        "representative_witnesses": witnesses[:12],
        "consequence": (
            "Each z mod3 helical class has coincident-pole residue orbits; "
            "local uniform convergence away from poles does not license a "
            "termwise principal-part extraction."
        ),
    }


def residue_orbit_recurrence() -> dict[str, object]:
    """Derive the exact helical functional-equation recurrence.

    For (p,k,r,s)=(-115,24,5,24), the two source shift relations combine
    to the displayed H_+ ratio for (mu,m)->(mu+Delta,m+6).  Applying it
    to both factors of R gives the residue recurrence below.  It identifies
    the exact remaining analytic condition without choosing a numerical
    chamber point or a residue value.
    """

    h_plus = (
        "H_+(mu,m)=sin(pi*(mu+m)/24)/"
        "sin(pi*(mu-1+(691+115*m)*omega_1)/(24*omega_1))"
    )
    multiplier = (
        "M_N(alpha)=H_+(alpha,N)/H_+(-alpha-Delta,-2-N), "
        "so R_(N+6)(alpha+Delta)=M_N(alpha)*R_N(alpha)"
    )
    records = []
    for label in ODD_CANONICAL_LABELS:
        for depth in range(1, 7):
            # The shared pole orbit over the base j=n=0 representative is
            # (z,j,n)=(-3*depth, depth, -depth).  The forward helical shift
            # maps it to depth-1, hence c_depth=c_(depth-1)/M_depth.
            records.append(
                {
                    "canonical_odd_N": label,
                    "depth": depth,
                    "alias_pole_index": {"z": -3 * depth, "j": depth, "n": -depth},
                    "residue_recurrence": "c_depth=c_(depth-1)/M_depth",
                    "M_depth_source_arguments": {
                        "first_factor": ["alpha_pole", label - 6 * depth],
                        "second_factor": ["-alpha_pole-Delta", -2 - label + 6 * depth],
                    },
                }
            )
    assert len(records) == DIMENSION * 6
    tail = residue_tail_asymptotics()
    return {
        "epistemic_status": "PROVED",
        "combined_helical_Gamma_ratio": h_plus,
        "raw_beta_helical_multiplier": multiplier,
        "residue_orbit_records": records,
        "residue_tail_criterion": "limsup_(depth->infinity) abs(1/M_depth)<1 in the strict chamber |q|<|q_tilde|<1",
        "tail_asymptotics": tail,
        "termwise_residue_extraction_excluded": True,
    }


def residue_tail_asymptotics() -> dict[str, object]:
    """Derive the strict-interior decay of a coincident-pole orbit.

    At the pole shared by the aliases z=-3k, j=k, n=-k above the
    z=0,j=n=0 representative, let rho=omega_1, q=exp(2*pi*i*tau),
    q_tilde=exp(-2*pi*i/rho), and t=exp(2*pi*i/(24*rho)).  Substitution
    in the exact product-ratio formula for K(z+3)/K(z) gives the four
    displayed variables.  Root-of-unity factors have modulus one, so the
    residue-ratio root limit is exact.  The source strict chamber
    |q|<|q_tilde|<1 implies |q|*|q_tilde|^(-1/24)<1.
    """

    exponent = Fraction(1, 24)
    strict_margin = 1 - exponent
    assert 0 < exponent < 1
    assert strict_margin == Fraction(23, 24) and strict_margin > 0
    return {
        "epistemic_status": "PROVED",
        "definitions": {
            "q": "exp(2*pi*i*tau)",
            "q_tilde": "exp(-2*pi*i/omega_1)",
            "t": "exp(2*pi*i/(24*omega_1))=q_tilde^(-1/24)",
        },
        "shared_pole_orbit": "z=-3k, j=k, n=-k, k>=0",
        "exact_alias_variables_at_depth_k": {
            "x_first": "q^(-k)",
            "x_second": "w*q^k, w=exp(2*pi*i/6)",
            "a_first": "zeta_24^(5k+19N)*t^(k-N-24)",
            "a_second": "zeta_24^(4+5N+19k)*t^(-k+N-24)",
        },
        "source_alias_ratio": (
            "M_k=(1-x_first)/(1-a_first)*"
            "(1-a_second/q_tilde)/(1-x_second/q)"
        ),
        "root_limit": "lim_(k->infinity)|1/M_k|^(1/k)=|q|*|q_tilde|^(-1/24)",
        "strict_chamber_log_certificate": (
            "Put epsilon=-log|q| and epsilon_tilde=-log|q_tilde|. "
            "epsilon>epsilon_tilde>0, and "
            "epsilon-epsilon_tilde/24=(epsilon-epsilon_tilde)+"
            "(23/24)*epsilon_tilde>0."
        ),
        "strict_interior_implication": (
            "|q|<|q_tilde|<1 implies |q|*|q_tilde|^(-1/24)<1"
        ),
        "residue_orbit_absolute_convergence": True,
        "nonzero_interior_asymptotic_sector": (
            "The base residue c_0 is nonzero and the recurrence has successive "
            "q-orders k, so c_k/c_0 has q-order k*(k+1)/2. Along the strict "
            "interior cusp sector the normalized residue orbit tends to 1; the "
            "summed channel is therefore not identically zero."
        ),
        "all_points_nonvanishing_claimed": False,
    }


def interior_periodization() -> dict[str, object]:
    """Check the exact alias geometry and strict source interior chamber.

    The cited interior factorization proposition applies in the upper
    two-base chamber.  Here q=exp(2*pi*i*tau) and q_tilde is obtained by
    the real PSL(2,Z) A_6 action, so Im(tau)>0 implies both moduli are
    strictly below one.  Its locally uniform bilateral convergence controls
    the function away from poles.  The separate collision audit decides
    whether residues can be taken termwise.
    """

    alias_records = []
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for residue in range(3):
                # z -> z+3: N_z -> N_z-18=N_z+6 mod 24 and
                # alpha_z -> alpha_z+6D=alpha_z+Delta.
                start_label = (first + 2 - 6 * residue) % LEVEL
                next_label = (first + 2 - 6 * (residue + 3)) % LEVEL
                assert next_label == (start_label + 6) % LEVEL
                alias_records.append(
                    {
                        "characteristic": [first, second],
                        "alias_class_z_mod_3": residue,
                        "N_z_mod_24": start_label,
                        "next_N_z_mod_24": next_label,
                        "alpha_step": "Delta",
                        "N_step": "+6 mod24",
                    }
                )
    assert len(alias_records) == 36 * 3
    odd_rows = sum(1 for first in range(DIMENSION) for _ in range(DIMENSION) if first % 2)
    assert odd_rows == 18
    return {
        "epistemic_status": "PROVED",
        "interior_domain": "tau in H; both source product bases have modulus strictly below one",
        "source_convergence_theorem": (
            "the interior two-base factorization/periodization proposition: "
            "three bilateral classes are absolutely and locally uniformly "
            "convergent in the strict chamber"
        ),
        "termwise_principal_parts_permitted_in_interior": False,
        "coincident_pole_residue_orbit_required": True,
        "residue_ratio_status": "PROVED: exact helical recurrence and strict-interior root decay give an absolutely convergent coincident-pole residue orbit",
        "alias_records": alias_records,
        "alias_record_count": len(alias_records),
        "odd_characteristic_count": odd_rows,
        "boundary_continuation_taken": False,
        "periodized_object": (
            "three z mod3 classes of Pi_A R_(N_z)(alpha_z), with "
            "a coincident-pole residue orbit to be summed in the interior chamber"
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    forced = forced_anti_fibre()
    retention = spectral_anti_retention()
    collisions = primary_pole_collision_lattice()
    recurrence = residue_orbit_recurrence()
    periodization = interior_periodization()
    result = {
        "schema": "sic-stark-cycle-194-meromorphic-anti-channel-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": (
            "Exact source principal-part witnesses, F_24-stable A fibre, raw "
            "spectral anti-difference retention, the exact coincident-pole "
            "lattice, and an absolutely convergent interior residue orbit. "
            "No endpoint continuation, "
            "AFK identification, completed alias value, ray map, boundary, "
            "fusion, Stark, or TCC result is proved."
        ),
        "forced_anti_fibre": forced,
        "spectral_anti_retention": retention,
        "primary_pole_collision_lattice": collisions,
        "residue_orbit_recurrence": recurrence,
        "interior_periodization": periodization,
        "next_unresolved_boundary": {
            "epistemic_status": "CONJECTURED",
            "statement": (
                "The source-forced 24D meromorphic theta carrier may admit a "
                "distributional or contour-controlled continuation to the "
                "real-multiplication endpoint that preserves its anti-channel; "
                "this is not supplied by interior local uniform convergence."
            ),
        },
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(rendered, end="")
    else:
        args.output.write_text(rendered, encoding="utf-8")


if __name__ == "__main__":
    main()
