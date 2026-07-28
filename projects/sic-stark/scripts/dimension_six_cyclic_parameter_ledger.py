#!/usr/bin/env python3
"""Exact parameter ledger for the dimension-six cyclic boundary.

At a rational point m/n, the q-Pochhammer factor attached to the
level-six characteristic (a,b) has roots

    z_j = exp(2*pi*i * (b*m-a*n+6*j*m)/(6*n)).

This script records the resulting sparse embedding in the common
6n-th-root system, the six central sectors, and the exact relation
between the moving-characteristic Euler--Maclaurin constant and the
standard cyclic dilogarithm normalization.

The certificate deliberately separates a genuine parameter match from
a TCC proof.  It proves that the two root systems fit in one torus on an
odd coprime subsequence, but also proves that the 36 sampled nodes are
not a subgroup and that the singular central sector cannot be inserted
directly into the usual punctured-Fermat-curve pentagon theorem.
"""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
import json
import math


DIMENSION = 6
TRACE_BETA = 5
A_MATRIX = ((115, -24), (24, -5))


def trace_sequence(stop: int) -> list[int]:
    values = [2, TRACE_BETA]
    while len(values) <= stop:
        values.append(TRACE_BETA * values[-1] - values[-2])
    return values


TRACES = trace_sequence(15)


def mapped_rational(base_index: int) -> tuple[int, int, int, int]:
    """Return m,n,m',n' with A.(m/n)=m'/n'."""

    numerator = TRACES[base_index + 2]
    denominator = TRACES[base_index + 3]
    mapped_numerator = TRACES[base_index - 1]
    mapped_denominator = TRACES[base_index]
    assert (
        A_MATRIX[0][0] * numerator
        + A_MATRIX[0][1] * denominator
        == mapped_numerator
    )
    assert (
        A_MATRIX[1][0] * numerator
        + A_MATRIX[1][1] * denominator
        == mapped_denominator
    )
    return numerator, denominator, mapped_numerator, mapped_denominator


def common_root_node(
    numerator: int,
    denominator: int,
    first: int,
    second: int,
) -> int:
    """Return the exponent of the characteristic in mu_(6n)."""

    return (
        second * numerator - first * denominator
    ) % (DIMENSION * denominator)


def factor_node(
    numerator: int,
    denominator: int,
    first: int,
    second: int,
    index: int,
) -> int:
    """Return the exponent of the index-j Pochhammer factor."""

    return (
        common_root_node(
            numerator,
            denominator,
            first,
            second,
        )
        + DIMENSION * index * numerator
    ) % (DIMENSION * denominator)


def central_sector(
    numerator: int,
    denominator: int,
    first: int,
    second: int,
) -> int:
    """Return r such that z_0^n=zeta_6^r."""

    return (
        second * numerator - first * denominator
    ) % DIMENSION


def characteristic_nodes(
    numerator: int,
    denominator: int,
) -> set[int]:
    return {
        common_root_node(
            numerator,
            denominator,
            first,
            second,
        )
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    }


def closure_witness(nodes: set[int], modulus: int) -> tuple[int, int, int]:
    """Return x,y,x+y with x,y in nodes and x+y outside nodes."""

    for left in sorted(nodes):
        for right in sorted(nodes):
            total = (left + right) % modulus
            if total not in nodes:
                return left, right, total
    raise AssertionError("the sparse node set unexpectedly is a subgroup")


def singular_characteristics(
    numerator: int,
    denominator: int,
) -> set[tuple[int, int]]:
    """Return nonzero characteristics whose cyclic product has a zero."""

    result = set()
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            if (first, second) == (0, 0):
                continue
            if central_sector(
                numerator,
                denominator,
                first,
                second,
            ) == 0:
                result.add((first, second))
    return result


def cyclic_normalization_exponents(
    denominator: int,
    second: int,
) -> dict[str, Fraction]:
    """Split the boundary exponent into cyclic and central pieces.

    For a nonsingular characteristic, put c=z_0^n.  If D is the
    Yalkinoglu cyclic product and d* is the standard reciprocal cyclic
    dilogarithm, then

      C = log d*(z_0)
          + (3-b)/(6n) * sum_j log(1-z_j).

    The last sum is a branch-compatible logarithm of 1-c.  The identity
    below is coefficient-wise, so it does not assume a logarithm branch.
    """

    moving_central = Fraction(1, 2) - Fraction(
        second,
        DIMENSION * denominator,
    )
    standard_central = Fraction(
        denominator - 1,
        2 * denominator,
    )
    correction = Fraction(
        3 - second,
        DIMENSION * denominator,
    )
    assert standard_central + correction == moving_central
    return {
        "moving_characteristic_central_exponent": moving_central,
        "standard_cyclic_central_exponent": standard_central,
        "extra_central_exponent": correction,
    }


def odd_coprime_record(base_index: int) -> dict[str, object]:
    numerator, denominator, mapped_numerator, mapped_denominator = (
        mapped_rational(base_index)
    )
    assert denominator % 2 == 1
    assert math.gcd(denominator, 6) == 1
    assert math.gcd(numerator, denominator) == 1

    modulus = DIMENSION * denominator
    nodes = characteristic_nodes(numerator, denominator)
    assert len(nodes) == DIMENSION * DIMENSION
    sector_counts = Counter(
        central_sector(
            numerator,
            denominator,
            first,
            second,
        )
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    )
    assert sector_counts == Counter({sector: 6 for sector in range(6)})

    # The order-n cyclic commutator and the order-six Weyl commutator
    # combine into one primitive order-6n commutator.
    combined_commutator_exponent = (
        DIMENSION * numerator + denominator
    ) % modulus
    assert math.gcd(combined_commutator_exponent, modulus) == 1

    # A is congruent to the identity modulo six, so the numerator and
    # denominator cyclic factors have the same central character.
    assert all(
        central_sector(
            numerator,
            denominator,
            first,
            second,
        )
        == central_sector(
            mapped_numerator,
            mapped_denominator,
            first,
            second,
        )
        for first in range(DIMENSION)
        for second in range(DIMENSION)
    )

    singular = singular_characteristics(numerator, denominator)
    assert len(singular) == 5
    assert singular | {(0, 0)} == {
        (first, second)
        for first in range(DIMENSION)
        for second in range(DIMENSION)
        if central_sector(
            numerator,
            denominator,
            first,
            second,
        )
        == 0
    }

    # A size-36 subgroup of Z/(6n) can exist only if 36 divides 6n.
    # This is impossible on the coprime subsequence.  Record an explicit
    # failure of closure as well.
    assert modulus % 36 != 0
    witness = closure_witness(nodes, modulus)

    # The modular cocycle compares two genuinely different cyclic
    # orders.  A fixed-order pentagon theorem cannot be applied to this
    # quotient without an additional inter-level transfer identity.
    assert denominator != mapped_denominator

    # The two rational vectors span a fixed lattice correspondence.
    # Its determinant is c times the fixed norm -21:
    #
    #   det((m,n), A(m,n)) = 24*(m^2-5mn+n^2) = -504.
    #
    # Since the four entries have gcd one, the Smith invariants are
    # (1,504).  Reduction modulo six retains only the determinant
    # pairing b*m-a*n, hence only the six central sectors.  In
    # particular, the correspondence has only six elements of
    # six-torsion and cannot contain the 36-element characteristic
    # group (Z/6)^2.
    lattice_determinant = (
        numerator * mapped_denominator
        - mapped_numerator * denominator
    )
    assert (
        numerator * numerator
        - TRACE_BETA * numerator * denominator
        + denominator * denominator
        == -21
    )
    assert lattice_determinant == -504
    smith_first = math.gcd(
        numerator,
        denominator,
        mapped_numerator,
        mapped_denominator,
    )
    smith_second = abs(lattice_determinant) // smith_first
    assert (smith_first, smith_second) == (1, 504)
    assert math.gcd(smith_second, DIMENSION) == DIMENSION

    return {
        "base_index": base_index,
        "source": [numerator, denominator],
        "target": [mapped_numerator, mapped_denominator],
        "source_order_is_odd": True,
        "source_order_coprime_to_six": True,
        "common_root_order": modulus,
        "combined_commutator_exponent": combined_commutator_exponent,
        "combined_commutator_is_primitive": True,
        "characteristic_node_count": len(nodes),
        "central_sector_counts": dict(sorted(sector_counts.items())),
        "singular_central_sector": 0,
        "singular_nonzero_characteristics": [
            list(item) for item in sorted(singular)
        ],
        "central_sector_preserved_by_stabilizer": True,
        "node_set_is_subgroup": False,
        "closure_witness": list(witness),
        "fixed_cyclic_order_on_both_sides": False,
        "inter_level_lattice_determinant": lattice_determinant,
        "inter_level_smith_invariants": [smith_first, smith_second],
        "inter_level_six_torsion_order": math.gcd(
            smith_second,
            DIMENSION,
        ),
        "inter_level_correspondence_captures_full_characteristic_group": (
            False
        ),
    }


def main() -> None:
    assert all(
        A_MATRIX[row][column] % DIMENSION
        == (1 if row == column else 0)
        for row in range(2)
        for column in range(2)
    )

    # Base indices 1,2 modulo 3 form an infinite odd subsequence.
    records = [
        odd_coprime_record(base_index)
        for base_index in (1, 2, 4, 5, 7, 8)
    ]
    normalization = {
        str(second): {
            key: str(value)
            for key, value in cyclic_normalization_exponents(
                records[0]["source"][1],
                second,
            ).items()
        }
        for second in range(DIMENSION)
    }
    result = {
        "schema": "sic-stark-dimension-six-cyclic-parameter-ledger-v1",
        "characteristic_node_formula": "k_(a,b)=b*m-a*n mod 6n",
        "factor_node_formula": "k_(a,b,j)=b*m-a*n+6*j*m mod 6n",
        "central_character_formula": "z_(a,b)^n=zeta_6^(b*m-a*n)",
        "stabilizer_mod_six": "identity",
        "normalization_identity": (
            "C=log(d_n^*)+(3-b)/(6n)*"
            "sum_j(log(1-z_j))"
        ),
        "normalization_exponents_at_first_record": normalization,
        "records": records,
        "parameter_match": {
            "common_6n_torus": True,
            "six_central_sectors": True,
            "six_nodes_per_sector": True,
            "singular_sector_requires_qgamma_regularization": True,
            "fixed_index_504_inter_level_correspondence": True,
        },
        "direct_pentagon_gates": {
            "fixed_order": False,
            "punctured_fermat_parameter_at_every_sector": False,
            "characteristic_nodes_form_subgroup": False,
            "cyclic_quotient_alone_retains_both_coordinates": False,
        },
        "conclusion": (
            "The level-six Weyl phase and the odd cyclic approximants "
            "share a primitive 6n-torus, and the moving-characteristic "
            "constant differs from the standard cyclic normalization by "
            "one explicit central factor.  A direct published pentagon "
            "application still fails because the cocycle is inter-level, "
            "one central sector lies on the singular Fermat boundary, "
            "and the 36 sampled nodes are not a subgroup.  The fixed "
            "index-504 lattice correspondence explains the six central "
            "sectors but retains only six elements of six-torsion, so it "
            "does not recover the second characteristic coordinate by "
            "itself; the associated Heisenberg representation is "
            "treated separately."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
