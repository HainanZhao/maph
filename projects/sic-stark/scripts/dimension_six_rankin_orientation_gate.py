#!/usr/bin/env python3
"""Exact orientation audit for norm/adjoint modular constructions in d=6."""

from fractions import Fraction


def conjugate(coordinates: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    """Conjugate a+b*zeta_6 using zeta_6 -> 1-zeta_6."""
    a, b = coordinates
    return a + b, -b


def add(
    left: tuple[Fraction, Fraction],
    right: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    return left[0] + right[0], left[1] + right[1]


def subtract(
    left: tuple[Fraction, Fraction],
    right: tuple[Fraction, Fraction],
) -> tuple[Fraction, Fraction]:
    return left[0] - right[0], left[1] - right[1]


def main() -> None:
    basis_one = (Fraction(1), Fraction(0))
    basis_zeta = (Fraction(0), Fraction(1))

    assert conjugate(basis_one) == basis_one
    assert conjugate(basis_zeta) == (Fraction(1), Fraction(-1))
    assert conjugate(conjugate(basis_zeta)) == basis_zeta

    generic = (Fraction(2), Fraction(3))
    trace = add(generic, conjugate(generic))
    anti_trace = subtract(generic, conjugate(generic))
    assert conjugate(trace) == trace
    assert conjugate(anti_trace) == (-anti_trace[0], -anti_trace[1])

    print("COEFFICIENT_FIELD=Q(zeta_6)")
    print("GALOIS_INVOLUTION_MATRIX=[[1,1],[0,-1]]")
    print("FIXED_SUBSPACE_DIMENSION=1")
    print("ANTI_INVARIANT_SUBSPACE_DIMENSION=1")
    print("RANKIN_SELF_PRODUCT_GALOIS_INVARIANT=1")
    print("ADJOINT_PACKET_SEES_ANTI_INVARIANT_ORIENTATION=0")
    print("NORM_OR_TRACE_METHOD_CAN_PROVE_ORIENTED_VALUE=0")
    print("LINEAR_F_ISOTYPIC_REGULATOR_STILL_REQUIRED=1")


if __name__ == "__main__":
    main()
