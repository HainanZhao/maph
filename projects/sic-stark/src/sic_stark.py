"""Exact elementary arithmetic for the canonical SIC--Stark family."""

from __future__ import annotations


Matrix2 = tuple[tuple[int, int], tuple[int, int]]
BinaryQuadraticForm = tuple[int, int, int]
ResidueVector = tuple[int, int]

IDENTITY_2: Matrix2 = ((1, 0), (0, 1))


def matrix_multiply(left: Matrix2, right: Matrix2) -> Matrix2:
    """Multiply two 2-by-2 integer matrices."""

    return (
        (
            left[0][0] * right[0][0] + left[0][1] * right[1][0],
            left[0][0] * right[0][1] + left[0][1] * right[1][1],
        ),
        (
            left[1][0] * right[0][0] + left[1][1] * right[1][0],
            left[1][0] * right[0][1] + left[1][1] * right[1][1],
        ),
    )


def matrix_power(matrix: Matrix2, exponent: int) -> Matrix2:
    """Raise a 2-by-2 integer matrix to a nonnegative power."""

    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    result = IDENTITY_2
    factor = matrix
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = matrix_multiply(result, factor)
        factor = matrix_multiply(factor, factor)
        remaining //= 2
    return result


def determinant(matrix: Matrix2) -> int:
    """Return the determinant of a 2-by-2 matrix."""

    return (
        matrix[0][0] * matrix[1][1]
        - matrix[0][1] * matrix[1][0]
    )


def canonical_form(dimension: int) -> BinaryQuadraticForm:
    r"""Return ``<1, 1-d, 1>`` for the canonical rank-one family."""

    if dimension < 4:
        raise ValueError("the non-sporadic canonical family starts at d=4")
    return (1, 1 - dimension, 1)


def form_discriminant(form: BinaryQuadraticForm) -> int:
    """Return ``b^2 - 4ac`` for ``<a,b,c>``."""

    a, b, c = form
    return b * b - 4 * a * c


def canonical_stabilizer(dimension: int) -> Matrix2:
    r"""Return the elementary stabilizer ``[[d-1,-1],[1,0]]``."""

    if dimension < 4:
        raise ValueError("the non-sporadic canonical family starts at d=4")
    return ((dimension - 1, -1), (1, 0))


def extended_displacement_modulus(dimension: int) -> int:
    r"""Return ``d`` for odd ``d`` and ``2d`` for even ``d``."""

    if dimension <= 0:
        raise ValueError("dimension must be positive")
    return dimension if dimension % 2 else 2 * dimension


def canonical_twist_multiplier(dimension: int, shift: int) -> int:
    r"""Return ``2*shift + 2*d - 1`` modulo the extended modulus.

    For rank one, the admissible tuple has ``r=1`` and ``d_j=d``.  Thus
    the source paper's twist function is
    ``f_t(shift)=2*shift+d+d_j-1``.  In particular shift 1 gives multiplier
    1 in every dimension, so it is compatible with the identity twist.
    """

    modulus = extended_displacement_modulus(dimension)
    return (2 * shift + 2 * dimension - 1) % modulus


def canonical_zauner_action(
    dimension: int, vector: ResidueVector
) -> ResidueVector:
    """Apply ``L_d`` to a column vector modulo ``d``."""

    stabilizer = canonical_stabilizer(dimension)
    return (
        (
            stabilizer[0][0] * vector[0]
            + stabilizer[0][1] * vector[1]
        )
        % dimension,
        (
            stabilizer[1][0] * vector[0]
            + stabilizer[1][1] * vector[1]
        )
        % dimension,
    )


def canonical_zauner_orbits(
    dimension: int,
) -> tuple[tuple[ResidueVector, ...], ...]:
    """Return all orbits of ``L_d`` on ``(Z/dZ)^2``."""

    if dimension < 4:
        raise ValueError("the non-sporadic canonical family starts at d=4")
    visited: set[ResidueVector] = set()
    orbits: list[tuple[ResidueVector, ...]] = []
    for p in range(dimension):
        for q in range(dimension):
            start = (p, q)
            if start in visited:
                continue
            orbit: list[ResidueVector] = []
            current = start
            while current not in orbit:
                orbit.append(current)
                current = canonical_zauner_action(dimension, current)
            canonical_orbit = tuple(orbit)
            visited.update(canonical_orbit)
            orbits.append(canonical_orbit)
    return tuple(orbits)


def canonical_quadratic_identity(dimension: int) -> Matrix2:
    r"""Return ``L_d^2 + L_d + I - d L_d`` entrywise.

    The returned zero matrix proves both the characteristic equation of
    ``L_d`` and ``L_d^2 + L_d + I == 0 (mod d)``.
    """

    stabilizer = canonical_stabilizer(dimension)
    square = matrix_multiply(stabilizer, stabilizer)
    return tuple(
        tuple(
            square[row][column]
            + stabilizer[row][column]
            + IDENTITY_2[row][column]
            - dimension * stabilizer[row][column]
            for column in range(2)
        )
        for row in range(2)
    )  # type: ignore[return-value]


def matrix_mod(matrix: Matrix2, modulus: int) -> Matrix2:
    """Reduce a 2-by-2 integer matrix entrywise modulo ``modulus``."""

    if modulus <= 0:
        raise ValueError("modulus must be positive")
    return tuple(
        tuple(entry % modulus for entry in row) for row in matrix
    )  # type: ignore[return-value]


def canonical_family_record(dimension: int) -> dict[str, object]:
    """Return exact invariants of the canonical dimension-``d`` datum."""

    form = canonical_form(dimension)
    stabilizer = canonical_stabilizer(dimension)
    return {
        "dimension": dimension,
        "form": form,
        "discriminant": form_discriminant(form),
        "expected_discriminant": (dimension + 1) * (dimension - 3),
        "stabilizer": stabilizer,
        "determinant": determinant(stabilizer),
        "extended_modulus": extended_displacement_modulus(dimension),
        "shift_zero_multiplier": canonical_twist_multiplier(dimension, 0),
        "shift_one_multiplier": canonical_twist_multiplier(dimension, 1),
        "zauner_orbit_count": len(canonical_zauner_orbits(dimension)),
        "quadratic_identity_residual": canonical_quadratic_identity(
            dimension
        ),
        "cube_mod_dimension": matrix_mod(
            matrix_power(stabilizer, 3), dimension
        ),
    }
