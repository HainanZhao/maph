#!/usr/bin/env python3
"""Exact level-24 block ledger for the dimension-six modular-gamma route.

The d=6 characteristic (a,b) is embedded in the discrete variable of the
general modular gamma function by

    h(a,b) = b - 4*a - 1  (mod 24).

For fixed b these six values form one eigenspace W_r of U^6, where
r=b-1 (mod 4).  This is a different polarization from the Zauner-stable
ideal block obtained from the lattice 2*Z^2.  The script records the
precise relation between the two decompositions and the even-level
Gaussian appearing in Ishibashi's inversion formula.

Everything below is finite integer arithmetic modulo 24 or 48.  It is a
structural certificate, not an identification of the analytic transfer
operator with the AFK ghost.
"""

from __future__ import annotations

from collections import Counter
import json
import math


DIMENSION = 6
LEVEL = 24
GAUSSIAN_LEVEL = 48
A_MATRIX = ((115, -24), (24, -5))
COEFFICIENT_LATTICE = ((4, 0), (0, 1))
IDEAL_LATTICE = ((2, 0), (0, 2))


def matrix_multiply(
    left: tuple[tuple[int, int], tuple[int, int]],
    right: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[tuple[int, int], tuple[int, int]]:
    return tuple(
        tuple(
            sum(left[row][middle] * right[middle][column] for middle in range(2))
            for column in range(2)
        )
        for row in range(2)
    )


def determinant(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> int:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def smith_invariants(
    matrix: tuple[tuple[int, int], tuple[int, int]],
) -> tuple[int, int]:
    first = math.gcd(*(abs(entry) for row in matrix for entry in row))
    return first, abs(determinant(matrix)) // first


def characteristic_h(first: int, second: int) -> int:
    return (second - 4 * first - 1) % LEVEL


def coefficient_block(second: int) -> int:
    return (second - 1) % 4


def local_coordinate(first: int, second: int) -> int:
    """Return ell with h=r+4*ell modulo 24."""

    h = characteristic_h(first, second)
    r = coefficient_block(second)
    assert (h - r) % 4 == 0
    return ((h - r) // 4) % DIMENSION


def gaussian_exponent_24(index: int) -> int:
    """Exponent modulo 48 of Ishibashi's even-level gamma(index)."""

    return (index * (index - LEVEL)) % GAUSSIAN_LEVEL


def gaussian_exponent_6(index: int) -> int:
    """Exponent modulo 48 of the embedded even level-six Gaussian."""

    # gamma_6(ell)=exp(pi*i*ell*(ell-6)/6)=zeta_48^(4 ell(ell-6)).
    return (4 * index * (index - DIMENSION)) % GAUSSIAN_LEVEL


def coefficient_gaussian_formula(block: int, local: int) -> int:
    """Predicted exponent for gamma_24(block+4*local)."""

    scalar = block * (block - LEVEL)
    linear = 8 * block * local
    fourth_power_level_six = 4 * gaussian_exponent_6(local)
    return (scalar + linear + fourth_power_level_six) % GAUSSIAN_LEVEL


def ideal_block_supports(parity: int, p12_sign: int) -> list[list[int]]:
    """Supports of the (U^12,P^12) ideal block.

    The coefficient on the second support is p12_sign.  Only supports
    are emitted in JSON; the sign is recorded separately.
    """

    assert parity in (0, 1)
    assert p12_sign in (-1, 1)
    return [
        [parity + 2 * local, parity + 2 * local + 12]
        for local in range(DIMENSION)
    ]


def main() -> None:
    assert determinant(COEFFICIENT_LATTICE) == 4
    assert determinant(IDEAL_LATTICE) == 4
    assert smith_invariants(COEFFICIENT_LATTICE) == (1, 4)
    assert smith_invariants(IDEAL_LATTICE) == (2, 2)

    # Their different Smith forms rule out an integral unimodular change
    # of polarization.  Their intersection and sum have indices 8 and 2.
    intersection_lattice = ((4, 0), (0, 2))
    sum_lattice = ((2, 0), (0, 1))
    assert determinant(intersection_lattice) == 8
    assert determinant(sum_lattice) == 2

    # A normalizes the coefficient lattice.  The induced matrix is
    # B^{-1}AB and is the identity modulo six.
    induced = ((115, -6), (96, -5))
    assert matrix_multiply(A_MATRIX, COEFFICIENT_LATTICE) == (
        matrix_multiply(COEFFICIENT_LATTICE, induced)
    )
    assert all(
        induced[row][column] % DIMENSION
        == (1 if row == column else 0)
        for row in range(2)
        for column in range(2)
    )

    characteristic_records = []
    counts = Counter()
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            h = characteristic_h(first, second)
            block = coefficient_block(second)
            local = local_coordinate(first, second)
            assert h == (block + 4 * local) % LEVEL
            counts[block] += 1
            characteristic_records.append(
                {
                    "characteristic": [first, second],
                    "mu_label": second,
                    "h": h,
                    "coefficient_block_r": block,
                    "local_coordinate": local,
                }
            )
    assert counts == Counter({0: 12, 3: 12, 1: 6, 2: 6})

    coefficient_blocks = {}
    for block in range(4):
        positions = [(block + 4 * local) % LEVEL for local in range(DIMENSION)]
        assert len(set(positions)) == DIMENSION

        # U^6 is scalar i^r on W_r; P^4 is the local shift and U,
        # after removal of zeta_24^r, is the local sixth-root clock.
        p12_pairs = [
            [positions[local], positions[(local + 3) % DIMENSION]]
            for local in range(3)
        ]
        assert all(
            (left + 12) % LEVEL == right
            for left, right in p12_pairs
        )

        # A sends the central label (0,6) to its inverse modulo 24,
        # so the metaplectic stabilizer pairs W_r with W_-r.
        inverse_block = (-block) % 4

        gaussian_exponents = [
            gaussian_exponent_24(position)
            for position in positions
        ]
        assert gaussian_exponents == [
            coefficient_gaussian_formula(block, local)
            for local in range(DIMENSION)
        ]

        # Translation by 12 either preserves or negates the inversion
        # Gaussian.  Thus it preserves P^12 eigenspaces for even r and
        # exchanges them for odd r.
        p12_ratios = [
            (
                gaussian_exponent_24((position + 12) % LEVEL)
                - gaussian_exponent_24(position)
            )
            % GAUSSIAN_LEVEL
            for position in positions[:3]
        ]
        expected_ratio = 0 if block % 2 == 0 else 24
        assert p12_ratios == [expected_ratio] * 3

        coefficient_blocks[str(block)] = {
            "positions": positions,
            "U_sixth_central_character": f"i^{block}",
            "P_fourth_is_local_shift": True,
            "U_is_local_clock_up_to_scalar": True,
            "P_twelfth_pairs": p12_pairs,
            "stabilizer_target_block": inverse_block,
            "ishibashi_gamma_exponents_mod_48": gaussian_exponents,
            "gamma_restriction_formula": (
                "gamma_24(r+4l)="
                "zeta_48^(r(r-24)+8rl)*gamma_6(l)^4"
            ),
            "gamma_P12_parity": (
                "preserves" if block % 2 == 0 else "exchanges"
            ),
        }

    # The ideal blocks split into three-dimensional P^12 eigenspaces
    # inside two coefficient blocks of the same parity:
    #
    # even positions: W_0 (+/-) direct-sum W_2 (+/-);
    # odd positions:  W_1 (+/-) direct-sum W_3 (+/-).
    ideal_blocks = {}
    for parity in (0, 1):
        coefficient_pair = [parity, parity + 2]
        for p12_sign in (-1, 1):
            key = f"U12_{1 if parity == 0 else -1}_P12_{p12_sign}"
            supports = ideal_block_supports(parity, p12_sign)
            assert {
                support[0] % 4
                for support in supports
            } == set(coefficient_pair)
            assert all(
                support[1] == support[0] + 12
                for support in supports
            )
            ideal_blocks[key] = {
                "position_parity": parity,
                "P12_eigenvalue": p12_sign,
                "coefficient_blocks": coefficient_pair,
                "three_dimensions_from_each_coefficient_block": True,
                "basis_supports": supports,
            }

    result = {
        "schema": "sic-stark-dimension-six-level24-blocks-v1",
        "characteristic_embedding": "h(a,b)=b-4a-1 mod 24",
        "characteristic_records": characteristic_records,
        "coefficient_block_counts": dict(sorted(counts.items())),
        "coefficient_blocks": coefficient_blocks,
        "stabilizer_induced_on_coefficient_lattice": [
            list(row) for row in induced
        ],
        "stabilizer_is_identity_on_local_level_six_labels": True,
        "ideal_blocks": ideal_blocks,
        "polarization_comparison": {
            "coefficient_lattice": [
                list(row) for row in COEFFICIENT_LATTICE
            ],
            "coefficient_smith_invariants": [1, 4],
            "ideal_lattice": [list(row) for row in IDEAL_LATTICE],
            "ideal_smith_invariants": [2, 2],
            "integral_unimodular_equivalence": False,
            "intersection_lattice": [
                list(row) for row in intersection_lattice
            ],
            "intersection_index": 8,
            "sum_lattice": [list(row) for row in sum_lattice],
            "sum_index": 2,
        },
        "inversion_phase_match": {
            "block_pairing_r_to_minus_r": True,
            "level24_gaussian_restricts_to_level6_gaussian": False,
            "restriction_is_fourth_power_with_linear_gauge": True,
            "P12_sign_exchange_occurs_exactly_on_odd_blocks": True,
        },
        "conclusion": (
            "The modular-gamma samples occupy four coefficient-polarized "
            "six-dimensional blocks.  The stabilizer pairs r with -r, "
            "exactly as required by reflection, and the ideal blocks are "
            "recovered by joining three-dimensional P^12 eigenspaces "
            "from r and r+2.  However the even-level inversion Gaussian "
            "restricts to gamma_6^4, not the nondegenerate level-six "
            "Gaussian.  An additional polarization-changing operator is "
            "therefore necessary before Ishibashi inversion can imply "
            "the AFK projector identity."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
