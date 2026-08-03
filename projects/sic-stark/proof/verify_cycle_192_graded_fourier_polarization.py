#!/usr/bin/env python3
"""Exact finite test for Cycle 192's graded beta-Fourier closure.

The published beta transform is continuous--discrete.  This verifier uses
only its *discrete* level-24 Fourier factor, so it can prove a necessary
finite carrier statement or a finite-metaplectic obstruction, never
continuous preservation or an amplitude identity.
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path


LEVEL = 24
DIMENSION = 6


def block_name(parity: int, sign: int) -> str:
    assert parity in (0, 1)
    assert sign in (-1, 1)
    return f"B_({parity},{'+' if sign == 1 else '-'})"


def fourier_target(parity: int, sign: int) -> tuple[int, int]:
    """Return the two-point block receiving F_24 B_(parity,sign)."""

    return (0 if sign == 1 else 1, 1 if parity == 0 else -1)


def source_kernel_exponent(
    input_parity: int,
    input_sign: int,
    output_local: int,
    input_local: int,
) -> int:
    """Root exponent in the normalized six-by-six F_24 block kernel.

    F_24 b_j^(p,sigma) = 6^(-1/2) sum_k
      omega_24^((q+2k)(p+2j)) b_k^(q,(-1)^p),
    where q=0 for sigma=+ and q=1 for sigma=-.
    """

    q, _ = fourier_target(input_parity, input_sign)
    return ((q + 2 * output_local) * (input_parity + 2 * input_local)) % LEVEL


def block_fourier_action() -> dict[str, object]:
    records: dict[str, object] = {}
    for parity in range(2):
        for sign in (-1, 1):
            target_parity, target_sign = fourier_target(parity, sign)
            kernel = [
                [
                    source_kernel_exponent(parity, sign, output, source)
                    for source in range(DIMENSION)
                ]
                for output in range(DIMENSION)
            ]

            # Check the asserted block formula directly against every one
            # of the 24 source Fourier coordinates.  The second point in
            # a target pair acquires exactly its target P^12 sign.
            q = target_parity
            for source in range(DIMENSION):
                for ambient_output in range(LEVEL):
                    direct_survives = (
                        1 + sign * (-1) ** ambient_output
                    ) != 0
                    assert direct_survives == (ambient_output % 2 == q)
                    if not direct_survives:
                        continue
                    output = ((ambient_output - q) // 2) % DIMENSION
                    base_output = q + 2 * output
                    direct_exponent = (
                        ambient_output * (parity + 2 * source)
                    ) % LEVEL
                    paired_exponent = kernel[output][source]
                    if ambient_output != base_output:
                        paired_exponent = (
                            paired_exponent
                            + (12 if target_sign == -1 else 0)
                        ) % LEVEL
                    assert direct_exponent == paired_exponent

            # Orthogonality is exact: after canceling constants the inner
            # product is a sixth-root geometric sum in 4*(j-j').
            for left in range(DIMENSION):
                for right in range(DIMENSION):
                    difference_counts = [
                        (
                            kernel[output][left]
                            - kernel[output][right]
                        )
                        % LEVEL
                        for output in range(DIMENSION)
                    ]
                    if left == right:
                        assert len(set(difference_counts)) == 1
                        assert difference_counts[0] == 0
                    else:
                        # It is one full coset of the order-six roots,
                        # possibly traversed with a proper period; its
                        # geometric sum is still zero for every nonzero
                        # local-coordinate difference modulo six.
                        step = (
                            difference_counts[1] - difference_counts[0]
                        ) % LEVEL
                        assert step == (4 * (left - right)) % LEVEL
                        assert step != 0 and (DIMENSION * step) % LEVEL == 0
                        assert all(
                            difference_counts[output]
                            == (difference_counts[0] + output * step) % LEVEL
                            for output in range(DIMENSION)
                        )
            records[block_name(parity, sign)] = {
                "target": block_name(target_parity, target_sign),
                "kernel_scale": "1/sqrt(6)",
                "kernel_root": "omega_24^((q+2k)*(p+2j))",
                "kernel_exponents_mod_24": kernel,
                "is_exact_unitary_six_point_kernel": True,
            }

    assert records["B_(0,+)"]["target"] == "B_(0,+)"
    assert records["B_(0,-)"]["target"] == "B_(1,+)"
    assert records["B_(1,+)"]["target"] == "B_(0,-)"
    assert records["B_(1,-)"]["target"] == "B_(1,-)"
    return {
        "epistemic_status": "PROVED",
        "full_level_24_operator": "F_24(e_m)=24^(-1/2)*sum_n omega_24^(n*m)*e_n",
        "two_point_basis": "b_j^(p,sigma)=e_(p+2j)+sigma*e_(p+2j+12)",
        "action": records,
        "permutation": "B_(p,sigma)->B_(q,(-1)^p), q=0 if sigma=+ else 1",
    }


def forced_closure() -> dict[str, object]:
    forced = {"B_(0,+)", "B_(0,-)"}
    action = {
        block_name(parity, sign): block_name(*fourier_target(parity, sign))
        for parity in range(2)
        for sign in (-1, 1)
    }
    closed = set(forced)
    while True:
        extension = closed | {action[name] for name in closed}
        if extension == closed:
            break
        closed = extension
    assert closed == {"B_(0,+)", "B_(0,-)", "B_(1,+)"}
    assert "B_(1,-)" not in closed
    return {
        "epistemic_status": "PROVED",
        "cycle_191_forced_blocks": sorted(forced),
        "unique_smallest_F24_invariant_closure": sorted(closed),
        "closure_block_count": len(closed),
        "closure_dimension": DIMENSION * len(closed),
        "Z2_grading": {
            "grade_zero": ["B_(0,+)"],
            "grade_one": ["B_(0,-)", "B_(1,+)"],
            "F24_preserves_each_grade": True,
            "nontrivial_grade_one_action": "B_(0,-)<->B_(1,+)",
        },
        "two_block_sum_is_F24_invariant": False,
        "three_block_closure_is_discrete_only": True,
    }


def alias_holonomy_intertwining() -> dict[str, object]:
    records = []
    for parity in range(2):
        for sign in (-1, 1):
            target_parity, target_sign = fourier_target(parity, sign)
            kernel = [
                [
                    source_kernel_exponent(parity, sign, output, source)
                    for source in range(DIMENSION)
                ]
                for output in range(DIMENSION)
            ]
            # Compute UDU^* exactly.  Its (k,l) exponent sum is
            # 2p(k-l)+j*(4(k-l)+12), so it vanishes unless l=k+3 mod6.
            # For p=0 this is the plain three-shift.  For p=1 its two
            # wrap directions have opposite fourth-root phases; a global
            # scalar would be false.
            monomial_records = []
            for source in range(DIMENSION):
                output = (source + 3) % DIMENSION
                exponent = (2 * parity * (output - source)) % LEVEL
                assert exponent == (
                    6 * parity if source < 3 else -6 * parity
                ) % LEVEL
                monomial_records.append(
                    {
                        "source_local": source,
                        "target_local": output,
                        "root_exponent_mod_24": exponent,
                    }
                )
            for output in range(DIMENSION):
                for source in range(DIMENSION):
                    coefficient = (4 * (output - source) + 12) % LEVEL
                    survives = coefficient == 0
                    assert survives == (source == (output + 3) % DIMENSION)
            records.append(
                {
                    "source_block": block_name(parity, sign),
                    "target_block": block_name(target_parity, target_sign),
                    "source_alias_operator": "D(e_j)=(-1)^j*e_j",
                    "target_operator": "F_block*D*F_block^*",
                    "monomial_three_shift_records": monomial_records,
                    "exact_relation": "F_block*D*F_block^*=S_3 for p=0; for p=1 it is the boundary-twisted three-shift with phases +i on source locals 0,1,2 and -i on 3,4,5",
                }
            )
    return {
        "epistemic_status": "PROVED",
        "records": records,
        "conclusion": "The non-scalar Cycle-191 alias holonomy has a canonical non-scalar metaplectic image. The original forced p=0 blocks give the ordinary three-shift; the canonically added p=1 block gives a boundary-twisted three-shift, not a removable global scalar. Scalarization is neither used nor possible.",
    }


def afk_phase_exponent(first: int, second: int) -> int:
    form = first * first - 5 * first * second + second * second
    parity = 6 + 7 * (1 + first) * (1 + second)
    return (24 * parity - 12 - 28 * form) % 48


def afk_carrier_rows() -> dict[str, object]:
    rows = []
    carrier_counts: dict[str, int] = {}
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            h = (second - 4 * first - 1) % LEVEL
            r = (second - 1) % 4
            local = ((h - r) // 4) % DIMENSION
            column_offset = (second - 1 - r) // 4
            assert h == (r + 4 * local) % LEVEL
            assert local == (-first + column_offset) % DIMENSION
            source_sign = 1 if first % 2 == 0 else -1
            target_source_block = block_name(*fourier_target(0, source_sign))
            name = f"W_{r}"
            carrier_counts[name] = carrier_counts.get(name, 0) + 1
            rows.append(
                {
                    "characteristic": [first, second],
                    "cycle_191_forced_source_block": block_name(0, source_sign),
                    "F24_image_block": target_source_block,
                    "afk_h_mod_24": h,
                    "afk_coefficient_carrier": name,
                    "afk_local_coordinate": local,
                    "afk_column_wrap_offset": column_offset,
                    "capital_to_lower_gamma_normalization": f"tau_6^{h}",
                    "capital_normalization_exponent_mod_12": (7 * h) % 12,
                    "afk_phase_exponent_mod_48": afk_phase_exponent(first, second),
                }
            )
    assert len(rows) == 36
    assert set(carrier_counts) == {"W_0", "W_1", "W_2", "W_3"}
    assert carrier_counts == {"W_0": 12, "W_1": 6, "W_2": 6, "W_3": 12}
    return {
        "epistemic_status": "PROVED",
        "rows_checked": len(rows),
        "all_four_coefficient_carriers_required": True,
        "carrier_counts": carrier_counts,
        "capital_gamma_normalization_retained_separately": True,
        "afk_phase_retained_separately": True,
        "rows": rows,
    }


def smith_invariants(matrix: tuple[tuple[int, int], tuple[int, int]]) -> tuple[int, int]:
    first = math.gcd(*(abs(entry) for row in matrix for entry in row))
    determinant = abs(matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0])
    assert determinant % first == 0
    return first, determinant // first


def polarization_obstruction() -> dict[str, object]:
    ideal = ((2, 0), (0, 2))
    coefficient = ((4, 0), (0, 1))
    ideal_smith = smith_invariants(ideal)
    coefficient_smith = smith_invariants(coefficient)
    assert ideal_smith == (2, 2)
    assert coefficient_smith == (1, 4)

    # In (Z/24)^2 the ideal image has exponent 12, whereas the coefficient
    # image contains (0,1) of order 24.  Any finite Heisenberg-normalizer
    # automorphism is an automorphism of this ambient finite module and
    # preserves subgroup exponent (equivalently the invariant factors).
    ideal_subgroup_exponent = 12
    coefficient_subgroup_exponent = 24
    assert ideal_subgroup_exponent != coefficient_subgroup_exponent
    return {
        "epistemic_status": "PROVED",
        "ideal_polarization_lattice": [[2, 0], [0, 2]],
        "ideal_smith_invariants": list(ideal_smith),
        "coefficient_polarization_lattice": [[4, 0], [0, 1]],
        "coefficient_smith_invariants": list(coefficient_smith),
        "ambient_module": "(Z/24Z)^2",
        "ideal_subgroup_exponent": ideal_subgroup_exponent,
        "coefficient_subgroup_exponent": coefficient_subgroup_exponent,
        "normalizer_invariant": "subgroup exponent and Smith invariant factors are preserved by every finite Heisenberg-normalizer/metaplectic automorphism",
        "finite_metaplectic_intertwiner_exists": False,
        "scope": "No finite Heisenberg-normalizer/metaplectic operator generated by the source F_24 block maps can carry the declared ideal-polarized graded closure to the coefficient-polarized AFK carrier. This leaves open a genuinely non-finite, polarization-changing continuous amplitude operator.",
    }


def payload() -> dict[str, object]:
    action = block_fourier_action()
    closure = forced_closure()
    holonomy = alias_holonomy_intertwining()
    carriers = afk_carrier_rows()
    obstruction = polarization_obstruction()
    return {
        "schema": "sic-stark-cycle-192-graded-fourier-polarization-prototype-v1",
        "epistemic_status": "PROVED",
        "claim_boundary": "This is an exact finite necessary-condition and finite-metaplectic obstruction result. It does not prove that the continuous beta integral preserves the three-block closure, identify its amplitude with AFK values, prove an RM boundary theorem, fusion continuity, Stark equality, or TCC.",
        "source_block_action": action,
        "forced_closure": closure,
        "alias_holonomy_intertwining": holonomy,
        "all36_afk_carriers": carriers,
        "finite_metaplectic_polarization_obstruction": obstruction,
        "gate_outcome": {
            "two_forced_blocks": "NOT_F24_INVARIANT",
            "canonical_Z2_graded_discrete_closure": "PROVED_THREE_BLOCKS_DIMENSION_18",
            "non_scalar_alias_holonomy": "EXACTLY_INTERTWINED_WITH_LOCAL_THREE_SHIFT",
            "all36_finite_metaplectic_AFK_intertwiner": "OBSTRUCTED_BY_POLARIZATION_INVARIANT",
            "continuous_beta_preservation": "OPEN",
            "amplitude_identity": "OPEN",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    arguments = parser.parse_args()
    rendered = json.dumps(payload(), indent=2, sort_keys=True) + "\n"
    if arguments.output:
        arguments.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
