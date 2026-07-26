"""Exact elementary arithmetic for the canonical SIC--Stark family."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction


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


def matrix_vector_multiply(
    matrix: Matrix2, vector: ResidueVector
) -> ResidueVector:
    """Multiply a 2-by-2 integer matrix by a column vector."""

    return (
        matrix[0][0] * vector[0] + matrix[0][1] * vector[1],
        matrix[1][0] * vector[0] + matrix[1][1] * vector[1],
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


def transform_form(
    form: BinaryQuadraticForm, matrix: Matrix2
) -> BinaryQuadraticForm:
    r"""Return the coefficients of ``form(matrix*(x,y))``.

    This is the determinant-one specialization of the source paper's
    ``GL_2(Z)`` action on binary quadratic forms.
    """

    a, b, c = form
    alpha, beta = matrix[0]
    gamma, delta = matrix[1]
    return (
        a * alpha * alpha + b * alpha * gamma + c * gamma * gamma,
        2 * a * alpha * beta
        + b * (alpha * delta + beta * gamma)
        + 2 * c * gamma * delta,
        a * beta * beta + b * beta * delta + c * delta * delta,
    )


def canonical_stabilizer(dimension: int) -> Matrix2:
    r"""Return the elementary stabilizer ``[[d-1,-1],[1,0]]``."""

    if dimension < 4:
        raise ValueError("the non-sporadic canonical family starts at d=4")
    return ((dimension - 1, -1), (1, 0))


def canonical_form_stabilizer_residual(
    dimension: int,
) -> BinaryQuadraticForm:
    r"""Return ``Q_d(L_d*(x,y))-Q_d(x,y)`` coefficientwise."""

    form = canonical_form(dimension)
    transformed = transform_form(
        form, canonical_stabilizer(dimension)
    )
    return (
        transformed[0] - form[0],
        transformed[1] - form[1],
        transformed[2] - form[2],
    )


def canonical_level_stabilizer(dimension: int) -> Matrix2:
    r"""Return ``A_d=L_d^3``, which is identity modulo ``d``."""

    return matrix_power(canonical_stabilizer(dimension), 3)


def canonical_level_quotient(dimension: int) -> Matrix2:
    r"""Return the integral matrix ``(L_d^3-I)/d``.

    Explicitly, this is
    ``[[d^2-3d+1, 2-d], [d-2, -1]]``.  It records the exact lift of the
    congruence ``L_d^3 == I (mod d)`` and makes characteristic correction
    factors computable without forming a large matrix power.
    """

    canonical_form(dimension)
    return (
        (dimension * dimension - 3 * dimension + 1, 2 - dimension),
        (dimension - 2, -1),
    )


def canonical_twist_kernel(dimension: int) -> Matrix2:
    r"""Return ``I+L_d`` reduced modulo ``d``.

    Although represented with residues in ``0,...,d-1``, this matrix is
    uniformly congruent to ``[[0,-1],[1,1]]``.
    """

    stabilizer = canonical_stabilizer(dimension)
    return matrix_mod(
        (
            (1 + stabilizer[0][0], stabilizer[0][1]),
            (stabilizer[1][0], 1 + stabilizer[1][1]),
        ),
        dimension,
    )


def canonical_kernel_identity(dimension: int) -> Matrix2:
    r"""Return ``I+L_d+L_d^2`` modulo ``d``.

    The zero result proves that the canonical twist kernel ``I+L_d`` is
    also ``-L_d^2`` modulo ``d``.
    """

    stabilizer = canonical_stabilizer(dimension)
    square = matrix_multiply(stabilizer, stabilizer)
    identity_sum: Matrix2 = (
        (
            1 + stabilizer[0][0] + square[0][0],
            stabilizer[0][1] + square[0][1],
        ),
        (
            stabilizer[1][0] + square[1][0],
            1 + stabilizer[1][1] + square[1][1],
        ),
    )
    return matrix_mod(
        identity_sum,
        dimension,
    )


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


def canonical_shift_partner(dimension: int, shift: int) -> int:
    r"""Return the complex-conjugate shift ``1-shift`` modulo ``d``.

    Appleby--Flammia--Kopp prove that shifts are paired by
    ``bar(lambda)=-(lambda+d_j-1)``.  In the canonical rank-one family
    ``d_j=d``, so this becomes ``1-lambda`` modulo ``d``.  In particular,
    shifts zero and one occur together.
    """

    canonical_form(dimension)
    return (1 - shift) % dimension


def symplectic_pair(
    left: ResidueVector, right: ResidueVector
) -> int:
    r"""Return ``left_2*right_1-left_1*right_2``."""

    return left[1] * right[0] - left[0] * right[1]


def canonical_twist_exponent(
    dimension: int,
    left: ResidueVector,
    right: ResidueVector,
) -> int:
    r"""Return ``<left,(I+L_d)right>`` modulo ``d``."""

    transformed = matrix_vector_multiply(
        canonical_twist_kernel(dimension), right
    )
    return symplectic_pair(left, transformed) % dimension


def canonical_tcc_fourier_frequency(
    dimension: int, output: ResidueVector
) -> ResidueVector:
    r"""Return the Fourier frequency ``(I+L_d)^(-1)*output`` modulo ``d``.

    The canonical twist kernel is congruent to
    ``Z=[[0,-1],[1,1]]``, whose inverse is
    ``[[1,1],[-1,0]]``.  Since ``Z`` is symplectic,

    ``<output,Z*q> = <Z^(-1)*output,q> (mod d)``.

    Thus TCC asks for the symplectic Fourier coefficient of the
    multiplicative difference ``u(q)/u(q-output)`` at this frequency.
    """

    canonical_form(dimension)
    first, second = output
    return (
        (first + second) % dimension,
        (-first) % dimension,
    )


def canonical_zauner_action(
    dimension: int, vector: ResidueVector
) -> ResidueVector:
    """Apply ``L_d`` to a column vector modulo ``d``."""

    first, second = matrix_vector_multiply(
        canonical_stabilizer(dimension), vector
    )
    return (first % dimension, second % dimension)


def canonical_zauner_orbit_sum(
    dimension: int, vector: ResidueVector
) -> ResidueVector:
    r"""Return ``vector+L_d*vector+L_d^2*vector`` modulo ``d``."""

    first = canonical_zauner_action(dimension, vector)
    second = canonical_zauner_action(dimension, first)
    return (
        (vector[0] + first[0] + second[0]) % dimension,
        (vector[1] + first[1] + second[1]) % dimension,
    )


def canonical_zauner_orbit_representative(
    dimension: int, vector: ResidueVector
) -> ResidueVector:
    """Return the lexicographically least vector in a Zauner orbit."""

    reduced = (vector[0] % dimension, vector[1] % dimension)
    first = canonical_zauner_action(dimension, reduced)
    second = canonical_zauner_action(dimension, first)
    return min(reduced, first, second)


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


def canonical_tcc_equation_count(dimension: int) -> int:
    r"""Return the exact number of unresolved Zauner-orbit TCC equations.

    The source's ``GL_2(Z)`` transformation theorem, specialized to the
    canonical form stabilizer, proves that the Shintani--Faddeev array is
    invariant under ``L_d``.  The TCC residual is therefore constant on
    these orbits.  The zero-output equation is already an identity by the
    cocycle inverse law, so it is excluded here.
    """

    canonical_form(dimension)
    fixed_points = 3 if dimension % 3 == 0 else 1
    orbit_count = fixed_points + (
        dimension * dimension - fixed_points
    ) // 3
    return orbit_count - 1


def canonical_tcc_orbit_bound(dimension: int) -> int:
    """Return the total number of Zauner orbits, including zero."""

    canonical_form(dimension)
    fixed_points = 3 if dimension % 3 == 0 else 1
    return fixed_points + (
        dimension * dimension - fixed_points
    ) // 3


def canonical_tcc_equation_representatives(
    dimension: int,
) -> tuple[ResidueVector, ...]:
    """Return one lexicographically canonical output index per TCC orbit."""

    return tuple(
        representative
        for representative in (
            min(orbit) for orbit in canonical_zauner_orbits(dimension)
        )
        if representative != (0, 0)
    )


def canonical_tcc_formal_signature(
    dimension: int, output: ResidueVector
) -> dict[tuple[int, ResidueVector, ResidueVector], int]:
    r"""Return the formal orbit-reduced signature of a TCC sum.

    Each term is keyed by its root-of-unity exponent, the Zauner orbit of
    the numerator ``u(q)``, and the orbit of the denominator
    ``u(q-output)``.  The inverse cocycle law rewrites the two TCC factors
    as this quotient. Equality of these dictionaries is a symbolic
    certificate of covariance that assumes only ``u(L_d*q)=u(q)``.
    """

    canonical_form(dimension)
    reduced_output = (
        output[0] % dimension,
        output[1] % dimension,
    )
    signature: dict[
        tuple[int, ResidueVector, ResidueVector], int
    ] = {}
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            difference = (
                (first - reduced_output[0]) % dimension,
                (second - reduced_output[1]) % dimension,
            )
            key = (
                canonical_twist_exponent(
                    dimension, reduced_output, characteristic
                ),
                canonical_zauner_orbit_representative(
                    dimension, characteristic
                ),
                canonical_zauner_orbit_representative(
                    dimension, difference
                ),
            )
            signature[key] = signature.get(key, 0) + 1
    return signature


def canonical_primitive_correction_indices(
    dimension: int, characteristic: ResidueVector
) -> tuple[int, int]:
    r"""Return the finite-product indices for ``q`` and ``q-(1,0)``.

    If ``n(q)=q_2-(d-2)q_1`` is the q-Pochhammer correction index, the
    primitive adjacent quotient has indices
    ``(n(q), n(q)+d-2)``.
    """

    first = canonical_characteristic_correction_index(
        dimension, characteristic
    )
    shifted = canonical_characteristic_correction_index(
        dimension, (characteristic[0] - 1, characteristic[1])
    )
    return (first, shifted)


def canonical_tcc_orbit_model_phase_totals(
    dimension: int,
    output: ResidueVector,
    orbit_values: Mapping[ResidueVector, int | Fraction],
) -> dict[int, Fraction]:
    r"""Evaluate an exact Zauner-invariant model, grouped by phase.

    ``orbit_values`` assigns a nonzero rational value to the canonical
    representative of every Zauner orbit.  The return value groups

    ``u(q)/u(q-output)``

    by the exponent of the ``d``-th root of unity in TCC.  It is useful
    for exact countermodels: covariance constraints are built in, while
    no claim is made that the supplied values are genuine modular-cocycle
    special values.
    """

    canonical_form(dimension)
    representatives = {
        min(orbit) for orbit in canonical_zauner_orbits(dimension)
    }
    supplied = set(orbit_values)
    if supplied != representatives:
        missing = sorted(representatives - supplied)
        extra = sorted(supplied - representatives)
        raise ValueError(
            f"orbit values have missing representatives {missing} "
            f"and extra representatives {extra}"
        )
    values = {
        representative: Fraction(value)
        for representative, value in orbit_values.items()
    }
    if any(value == 0 for value in values.values()):
        raise ValueError("orbit values must be nonzero")

    reduced_output = (
        output[0] % dimension,
        output[1] % dimension,
    )
    totals = {
        exponent: Fraction(0) for exponent in range(dimension)
    }
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            difference = (
                (first - reduced_output[0]) % dimension,
                (second - reduced_output[1]) % dimension,
            )
            numerator = values[
                canonical_zauner_orbit_representative(
                    dimension, characteristic
                )
            ]
            denominator = values[
                canonical_zauner_orbit_representative(
                    dimension, difference
                )
            ]
            exponent = canonical_twist_exponent(
                dimension, reduced_output, characteristic
            )
            totals[exponent] += numerator / denominator
    return totals


def canonical_dimension_four_countermodel(
) -> dict[ResidueVector, Fraction]:
    r"""Return an exact reciprocal, Zauner-invariant non-TCC witness.

    The values are indexed by the six Zauner-orbit representatives in
    dimension four.  They obey ``u(-q)=u(q)^(-1)``.  Nevertheless, their
    primitive TCC residual is ``3/2 - (3/2)i``, proving that covariance,
    reciprocal pairing, and cyclic telescoping do not force TCC.
    """

    return {
        (0, 0): Fraction(1),
        (0, 1): Fraction(2),
        (0, 2): Fraction(1),
        (0, 3): Fraction(1, 2),
        (1, 1): Fraction(1),
        (2, 3): Fraction(1),
    }


def canonical_jacobi_word(dimension: int) -> tuple[int, int, int]:
    r"""Return the HJ exponents in ``L_d^3=(T^(d-1)S)^3``."""

    canonical_form(dimension)
    return (dimension - 1,) * 3


def canonical_jacobi_scale_exponents() -> tuple[int, int, int]:
    r"""Return the powers of ``beta_d`` in the three ``S``-kernel inputs.

    At the fixed point ``beta_d``, the Jacobi cocycle law gives
    ``sigma_(L^3)(z,beta)`` as the product of ``sigma_S`` evaluated at
    ``z/beta^2``, ``z/beta``, and ``z``.
    """

    return (-2, -1, 0)


def canonical_characteristic_correction_index(
    dimension: int, characteristic: ResidueVector
) -> int:
    r"""Return the finite-product index for ``r=characteristic/d``.

    In the modular-to-Jacobi conversion this index is the second component
    of ``(I-L_d^3)r``.  Since
    ``L_d^3=I+d*canonical_level_quotient(d)``, it simplifies to
    ``characteristic[1]-(d-2)*characteristic[0]``.
    """

    canonical_form(dimension)
    return (
        characteristic[1]
        - (dimension - 2) * characteristic[0]
    )


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
        "form_stabilizer_residual": (
            canonical_form_stabilizer_residual(dimension)
        ),
        "level_stabilizer": canonical_level_stabilizer(dimension),
        "level_quotient": canonical_level_quotient(dimension),
        "twist_kernel": canonical_twist_kernel(dimension),
        "kernel_identity_residual": canonical_kernel_identity(dimension),
        "determinant": determinant(stabilizer),
        "extended_modulus": extended_displacement_modulus(dimension),
        "shift_zero_multiplier": canonical_twist_multiplier(dimension, 0),
        "shift_one_multiplier": canonical_twist_multiplier(dimension, 1),
        "shift_zero_partner": canonical_shift_partner(dimension, 0),
        "zauner_orbit_count": len(canonical_zauner_orbits(dimension)),
        "tcc_equation_count": canonical_tcc_equation_count(dimension),
        "tcc_orbit_bound": canonical_tcc_orbit_bound(dimension),
        "jacobi_word": canonical_jacobi_word(dimension),
        "jacobi_scale_exponents": canonical_jacobi_scale_exponents(),
        "quadratic_identity_residual": canonical_quadratic_identity(
            dimension
        ),
        "cube_mod_dimension": matrix_mod(
            matrix_power(stabilizer, 3), dimension
        ),
    }
