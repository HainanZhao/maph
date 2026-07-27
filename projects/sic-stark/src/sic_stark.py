"""Exact elementary arithmetic for the canonical SIC--Stark family."""

from __future__ import annotations

from collections.abc import Mapping
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt


Matrix2 = tuple[tuple[int, int], tuple[int, int]]
BinaryQuadraticForm = tuple[int, int, int]
ResidueVector = tuple[int, int]
QuadraticCoordinate = tuple[Fraction, Fraction]
LaurentExponent = tuple[int, int]
LaurentPolynomial = dict[LaurentExponent, Fraction]
BiquadraticCoordinate = tuple[Fraction, Fraction, Fraction, Fraction]
TowerCoordinate = tuple[
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
    Fraction,
]
TowerComplex = tuple[TowerCoordinate, TowerCoordinate]

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


def canonical_beta_is_rational(dimension: int) -> bool:
    r"""Return whether the positive root ``beta_d`` is rational.

    Here ``beta_d`` is the larger root of
    ``x^2-(d-1)x+1``.  Its discriminant is
    ``(d-1)^2-4``.  This is never a square in the canonical range
    ``d >= 4``, but the exact predicate makes the cyclic-pentagon
    compatibility check executable.
    """

    discriminant = form_discriminant(canonical_form(dimension))
    root = isqrt(discriminant)
    return root * root == discriminant


def canonical_general_modular_modulus(dimension: int) -> int:
    r"""Return the discrete modulus of the modular gamma for ``A_d``.

    The general modular quantum dilogarithm attached to
    ``A_d=L_d^3`` uses the absolute value of the lower-left entry of
    ``A_d`` as its discrete modulus.  In the canonical family this is
    ``d(d-2)``, rather than the characteristic modulus ``d``.
    """

    modulus = abs(canonical_level_stabilizer(dimension)[1][0])
    assert modulus == dimension * (dimension - 2)
    return modulus


def canonical_general_modular_parameters(
    dimension: int,
) -> tuple[int, int, int, int]:
    r"""Return ``(k,p,r,s)`` for the general modular gamma of ``A_d``.

    Sarkissian--Spiridonov write

    ``M=[[-p,-s],[k,-r]]`` with ``p*r+k*s=1`` and ``k>0``.

    This function translates the canonical matrix ``A_d=L_d^3`` into
    that convention.
    """

    matrix = canonical_level_stabilizer(dimension)
    parameters = (
        matrix[1][0],
        -matrix[0][0],
        -matrix[1][1],
        -matrix[0][1],
    )
    k, p, r, s = parameters
    assert k > 0
    assert p * r + k * s == 1
    return parameters


def canonical_quadratic_residue_multiply(
    dimension: int,
    left: ResidueVector,
    right: ResidueVector,
) -> ResidueVector:
    r"""Multiply two elements of ``Z[beta_d]/d`` in the basis ``(1,beta)``."""

    canonical_form(dimension)
    a, b = left
    c, e = right
    return (
        (a * c - b * e) % dimension,
        (
            a * e
            + b * c
            + (dimension - 1) * b * e
        )
        % dimension,
    )


def canonical_quadratic_residue_norm(
    dimension: int, element: ResidueVector
) -> int:
    r"""Return the norm of ``a+b*beta_d`` modulo ``d``."""

    canonical_form(dimension)
    a, b = element
    return (
        a * a + (dimension - 1) * a * b + b * b
    ) % dimension


def canonical_residue_multiplication_matrix(
    dimension: int, element: ResidueVector
) -> Matrix2:
    r"""Return multiplication by ``a+b*beta_d`` on TCC coordinates.

    TCC uses ``q_2*beta_d-q_1`` rather than the basis coordinates
    ``(1,beta_d)``.  In the ``(q_1,q_2)`` convention the matrix is

    ``[[a,b],[-b,a+(d-1)b]]`` modulo ``d``.
    """

    canonical_form(dimension)
    a, b = element
    return matrix_mod(
        ((a, b), (-b, a + (dimension - 1) * b)),
        dimension,
    )


def canonical_quadratic_residue_units(
    dimension: int,
) -> tuple[ResidueVector, ...]:
    r"""Return ``(Z[beta_d]/d)^x`` as coefficient pairs."""

    canonical_form(dimension)
    return tuple(
        (a, b)
        for a in range(dimension)
        for b in range(dimension)
        if gcd(
            canonical_quadratic_residue_norm(
                dimension, (a, b)
            ),
            dimension,
        )
        == 1
    )


def canonical_global_unit_residues(
    dimension: int,
) -> tuple[ResidueVector, ResidueVector, ResidueVector]:
    r"""Return the order-three subgroup generated by ``beta_d`` modulo ``d``."""

    canonical_form(dimension)
    return (
        (1, 0),
        (0, 1),
        (dimension - 1, dimension - 1),
    )


def canonical_local_unit_cosets(
    dimension: int,
) -> tuple[tuple[ResidueVector, ...], ...]:
    r"""Return local residue-unit cosets modulo the global beta subgroup."""

    subgroup = canonical_global_unit_residues(dimension)
    unseen = set(canonical_quadratic_residue_units(dimension))
    cosets: list[tuple[ResidueVector, ...]] = []
    while unseen:
        representative = min(unseen)
        coset = tuple(
            sorted(
                {
                    canonical_quadratic_residue_multiply(
                        dimension, representative, unit
                    )
                    for unit in subgroup
                }
            )
        )
        cosets.append(coset)
        unseen.difference_update(coset)
    return tuple(sorted(cosets))


def canonical_primitive_direction_unit_stabilizers(
    dimension: int,
) -> dict[str, tuple[ResidueVector, ...]]:
    r"""Return residue units fixing ``e_1`` exactly or up to Zauner action."""

    direction = (1, 0)
    direction_orbit = {
        matrix_vector_multiply(
            canonical_residue_multiplication_matrix(
                dimension, unit
            ),
            direction,
        )
        for unit in canonical_global_unit_residues(dimension)
    }
    exact: list[ResidueVector] = []
    zauner: list[ResidueVector] = []
    for unit in canonical_quadratic_residue_units(dimension):
        image = tuple(
            coordinate % dimension
            for coordinate in matrix_vector_multiply(
                canonical_residue_multiplication_matrix(
                    dimension, unit
                ),
                direction,
            )
        )
        if image == direction:
            exact.append(unit)
        if image in direction_orbit:
            zauner.append(unit)
    return {
        "exact": tuple(sorted(exact)),
        "up_to_zauner": tuple(sorted(zauner)),
    }


def canonical_dimension_four_trace_obstruction_record(
) -> dict[str, object]:
    r"""Return exact failures of a fixed-direction ray-class trace in d=4.

    The global unit ``beta`` represents the identity in the local-unit
    quotient.  Acting by it on ``q=e_1`` changes the primitive phase when
    ``p=e_1`` is held fixed, so that phase cannot descend to a ray-class
    character.  Acting on ``p`` and ``q`` simultaneously preserves the
    phase, but then moves the output direction.
    """

    dimension = 4
    direction = (1, 0)
    characteristic = (1, 0)
    global_beta = (0, 1)
    global_units = canonical_global_unit_residues(dimension)
    quotient_cosets = canonical_local_unit_cosets(dimension)
    quotient_exponent_two = all(
        canonical_quadratic_residue_multiply(
            dimension, coset[0], coset[0]
        )
        in global_units
        for coset in quotient_cosets
    )
    action = canonical_residue_multiplication_matrix(
        dimension, global_beta
    )
    acted_direction = tuple(
        coordinate % dimension
        for coordinate in matrix_vector_multiply(action, direction)
    )
    acted_characteristic = tuple(
        coordinate % dimension
        for coordinate in matrix_vector_multiply(
            action, characteristic
        )
    )
    phase = canonical_twist_exponent(
        dimension, direction, characteristic
    )
    fixed_direction_phase = canonical_twist_exponent(
        dimension, direction, acted_characteristic
    )
    simultaneous_phase = canonical_twist_exponent(
        dimension, acted_direction, acted_characteristic
    )
    return {
        "local_unit_count": len(
            canonical_quadratic_residue_units(dimension)
        ),
        "global_unit_subgroup": global_units,
        "local_unit_quotient_cosets": quotient_cosets,
        "local_unit_quotient_order": len(quotient_cosets),
        "local_unit_quotient_exponent_two": quotient_exponent_two,
        "local_unit_quotient_structure": "C2 x C2",
        "direction_stabilizers": (
            canonical_primitive_direction_unit_stabilizers(dimension)
        ),
        "phase_descent_witness": {
            "direction": direction,
            "characteristic": characteristic,
            "global_unit": global_beta,
            "acted_direction": acted_direction,
            "acted_characteristic": acted_characteristic,
            "original_phase": phase,
            "fixed_direction_phase": fixed_direction_phase,
            "simultaneous_phase": simultaneous_phase,
        },
        "artin_controls": "squared Stark values",
        "tcc_uses": "coherently signed square-root ratios",
    }


def canonical_general_modular_characteristic(
    dimension: int, characteristic: ResidueVector
) -> tuple[QuadraticCoordinate, int]:
    r"""Map a TCC characteristic to an unnormalized modular gamma sample.

    Let ``D_d=(d-2)beta_d-1`` and represent a quadratic number by its
    coordinates in the basis ``(1,beta_d)``.  On the canonical residue
    grid, the exact q-product dictionary is

    ``u(q)=gamma_A(1+q_2*D_d, q_2-(d-2)q_1-1)``.

    The discrete coordinate is reduced modulo ``k=d(d-2)``.  In
    particular, the continuous coordinate is independent of ``q_1``.
    """

    modulus = canonical_general_modular_modulus(dimension)
    first = characteristic[0] % dimension
    second = characteristic[1] % dimension
    continuous = (
        Fraction(1 - second),
        Fraction((dimension - 2) * second),
    )
    discrete = (
        second - (dimension - 2) * first - 1
    ) % modulus
    return (continuous, discrete)


def canonical_general_modular_node_strip_margins(
    dimension: int, characteristic: ResidueVector
) -> tuple[tuple[int, int], tuple[int, int]]:
    r"""Certify the node's distances from the two modular-gamma pole cones.

    A pair ``(a,n)`` denotes the positive quantity ``a+n*D_d``, where
    ``D_d=(d-2)beta_d-1>0``.  For a node with reduced second coordinate
    ``q_2``, the distances from ``0`` and
    ``Q=omega_1+omega_2=d*D_d+2`` are respectively

    ``mu=1+q_2*D_d`` and ``Q-mu=1+(d-q_2)*D_d``.

    Both are strictly positive, so every TCC node lies in the open strip
    between the left and right pole cones.
    """

    canonical_form(dimension)
    second = characteristic[1] % dimension
    return ((1, second), (1, dimension - second))


def canonical_dimension_four_localization_record() -> dict[str, object]:
    r"""Return the exact d=4 beta-integral/TCC phase comparison.

    Exponents are modulo eight and denote powers of
    ``zeta_8=exp(pi*i/4)``.  With ``N=3``, ``g=Q``, and
    ``alpha=-3D``, the published two-gamma beta-integral phase agrees
    with the normalized primitive TCC phase up to the global factor
    ``zeta_8^3``.  The nodes nevertheless lie in the pole-free strip,
    so they cannot arise as residues of that integrand.
    """

    dimension = 4
    nodes: list[dict[str, object]] = []
    for first in range(dimension):
        for second in range(dimension):
            continuous, discrete = (
                canonical_general_modular_characteristic(
                    dimension, (first, second)
                )
            )
            tcc_phase = (discrete + 1 - 3 * second) % 8
            normalization_ratio = (5 * discrete) % 8
            normalized_tcc_phase = (
                tcc_phase + normalization_ratio
            ) % 8
            beta_discrete_phase = (6 * discrete) % 8
            beta_continuous_phase = (6 - 3 * second) % 8
            beta_integral_phase = (
                beta_discrete_phase + beta_continuous_phase
            ) % 8
            lower, upper = (
                canonical_general_modular_node_strip_margins(
                    dimension, (first, second)
                )
            )
            nodes.append(
                {
                    "characteristic": (first, second),
                    "continuous_coordinates": continuous,
                    "discrete": discrete,
                    "selection_parity": (second - 1) % 2,
                    "tcc_phase": tcc_phase,
                    "normalization_ratio": normalization_ratio,
                    "normalized_tcc_phase": normalized_tcc_phase,
                    "beta_integral_phase": beta_integral_phase,
                    "global_phase_difference": (
                        normalized_tcc_phase - beta_integral_phase
                    )
                    % 8,
                    "lower_strip_margin": lower,
                    "upper_strip_margin": upper,
                }
            )
    return {
        "parameters": canonical_general_modular_parameters(dimension),
        "period_coordinates": {
            "D": (Fraction(-1), Fraction(2)),
            "omega_1": (Fraction(-3), Fraction(8)),
            "omega_2": (Fraction(1), Fraction(0)),
            "Q": (Fraction(-2), Fraction(8)),
        },
        "beta_integral_parameters": {
            "N": 3,
            "g": "Q",
            "alpha": "-3D",
        },
        "nodes": tuple(nodes),
    }


def canonical_primitive_sigma_shift_coordinates(
    dimension: int,
) -> tuple[QuadraticCoordinate, QuadraticCoordinate, QuadraticCoordinate]:
    r"""Return coordinates of ``1/(d beta_d^k)``, for ``k=0,1,2``.

    Each pair ``(a,b)`` represents ``a+b*beta_d``.  The coordinates
    follow from ``beta_d^2-(d-1)beta_d+1=0`` and are useful because the
    real quasiperiod lattice of ``sigma_S`` is
    ``Z + Z*beta_d``.
    """

    canonical_form(dimension)
    return (
        (Fraction(1, dimension), Fraction(0)),
        (
            Fraction(dimension - 1, dimension),
            Fraction(-1, dimension),
        ),
        (
            Fraction(dimension - 2),
            Fraction(-(dimension - 1), dimension),
        ),
    )


def canonical_primitive_sigma_shifts_are_quasiperiods(
    dimension: int,
) -> tuple[bool, bool, bool]:
    r"""Test whether the primitive quotient shifts lie in ``Z+Z beta``."""

    return tuple(
        constant.denominator == 1 and beta.denominator == 1
        for constant, beta in canonical_primitive_sigma_shift_coordinates(
            dimension
        )
    )  # type: ignore[return-value]


def canonical_pentagon_compatibility_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return exact warnings for applying known pentagon identities.

    A cyclic finite quantum-dilogarithm identity requires a root-of-unity
    deformation parameter, which would require rational ``beta_d``.  The
    general modular identity does apply to ``A_d``, but its native
    discrete modulus is ``d(d-2)`` and it retains a continuous integral.
    The larger modulus admits the sparse characteristic embedding
    implemented by ``canonical_general_modular_characteristic``; it is
    not by itself an obstruction.  The primitive sigma shifts also miss
    the quasiperiod lattice.
    """

    beta_rational = canonical_beta_is_rational(dimension)
    modular_modulus = canonical_general_modular_modulus(dimension)
    return {
        "beta_rational": beta_rational,
        "cyclic_parameter_is_root_of_unity": beta_rational,
        "characteristic_modulus": dimension,
        "general_modular_modulus": modular_modulus,
        "moduli_match": modular_modulus == dimension,
        "general_modular_parameters": (
            canonical_general_modular_parameters(dimension)
        ),
        "primitive_shift_coordinates": (
            canonical_primitive_sigma_shift_coordinates(dimension)
        ),
        "primitive_shifts_are_quasiperiods": (
            canonical_primitive_sigma_shifts_are_quasiperiods(dimension)
        ),
        "faddeev_fourier_sigma_line": "1+i*sqrt(beta)*R",
        "tcc_sigma_line": "R",
        "general_modular_measure": "finite sum times continuous integral",
    }


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


def _laurent_add(
    *terms: tuple[Fraction | int, Mapping[LaurentExponent, Fraction]]
) -> LaurentPolynomial:
    """Return an exact linear combination of Laurent polynomials."""

    result: LaurentPolynomial = {}
    for scalar, polynomial in terms:
        coefficient = Fraction(scalar)
        for exponent, value in polynomial.items():
            result[exponent] = (
                result.get(exponent, Fraction(0))
                + coefficient * value
            )
    return {
        exponent: value
        for exponent, value in result.items()
        if value
    }


def _laurent_multiply(
    left: Mapping[LaurentExponent, Fraction],
    right: Mapping[LaurentExponent, Fraction],
) -> LaurentPolynomial:
    """Multiply two exact bivariate Laurent polynomials."""

    result: LaurentPolynomial = {}
    for left_exponent, left_value in left.items():
        for right_exponent, right_value in right.items():
            exponent = (
                left_exponent[0] + right_exponent[0],
                left_exponent[1] + right_exponent[1],
            )
            result[exponent] = (
                result.get(exponent, Fraction(0))
                + left_value * right_value
            )
    return {
        exponent: value
        for exponent, value in result.items()
        if value
    }


def _laurent_power(
    polynomial: Mapping[LaurentExponent, Fraction],
    exponent: int,
) -> LaurentPolynomial:
    """Raise a Laurent polynomial to a nonnegative integer power."""

    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    result: LaurentPolynomial = {(0, 0): Fraction(1)}
    factor = dict(polynomial)
    remaining = exponent
    while remaining:
        if remaining & 1:
            result = _laurent_multiply(result, factor)
        factor = _laurent_multiply(factor, factor)
        remaining //= 2
    return result


def canonical_dimension_four_packet_directions(
) -> tuple[ResidueVector, ResidueVector, ResidueVector, ResidueVector]:
    r"""Return the regular ray-unit orbit of the primitive direction in d=4."""

    return ((0, 3), (0, 1), (1, 1), (2, 3))


def canonical_dimension_four_packet_permutations(
) -> tuple[tuple[int, int, int, int], ...]:
    r"""Return the ``C2 x C2`` regular action on packet coordinates."""

    return (
        (0, 1, 2, 3),
        (1, 0, 3, 2),
        (2, 3, 0, 1),
        (3, 2, 1, 0),
    )


def canonical_dimension_four_packet_variable_actions(
) -> tuple[Matrix2, Matrix2, Matrix2, Matrix2]:
    r"""Return the ray-unit action on Laurent exponents of ``x`` and ``y``.

    On the four primitive value orbits, use the coordinates

    ``(x^-1, x, y, y^-1)``.

    The quotient ``C2 x C2`` then acts on ``(x,y)`` by

    ``(x,y)``, ``(x^-1,y^-1)``, ``(y^-1,x^-1)``, and ``(y,x)``.
    """

    return (
        ((1, 0), (0, 1)),
        ((-1, 0), (0, -1)),
        ((0, -1), (-1, 0)),
        ((0, 1), (1, 0)),
    )


def canonical_dimension_four_laurent_action(
    polynomial: Mapping[LaurentExponent, Fraction],
    group_index: int,
) -> LaurentPolynomial:
    """Apply a dimension-four ray-unit quotient element to a Laurent polynomial."""

    actions = canonical_dimension_four_packet_variable_actions()
    if not 0 <= group_index < len(actions):
        raise ValueError("group index must lie between 0 and 3")
    action = actions[group_index]
    return {
        matrix_vector_multiply(action, exponent): value
        for exponent, value in polynomial.items()
    }


def _canonical_dimension_four_orbit_monomials(
) -> dict[ResidueVector, LaurentExponent]:
    """Return the cycle-8 formal unit assigned to each Zauner orbit."""

    return {
        (0, 0): (0, 0),
        (0, 1): (1, 0),
        (0, 2): (0, 0),
        (0, 3): (-1, 0),
        (1, 1): (0, 1),
        (2, 3): (0, -1),
    }


def _canonical_dimension_four_monomial(
    characteristic: ResidueVector,
) -> LaurentExponent:
    """Return the formal-unit exponent at a dimension-four node."""

    return _canonical_dimension_four_orbit_monomials()[
        canonical_zauner_orbit_representative(4, characteristic)
    ]


def canonical_dimension_four_residual_laurent_packet(
) -> tuple[
    LaurentPolynomial,
    LaurentPolynomial,
    LaurentPolynomial,
    LaurentPolynomial,
]:
    r"""Return the exact reciprocal two-parameter TCC residual packet.

    Normalize the four actual residuals by Gaussian units as

    ``(R_(0,3), R_(0,1), R_(1,1), R_(2,3))
      = ((1-i)A, (1-i)B, (1+i)C, (1+i)D)``.

    Zauner covariance and inversion reduce the six value orbits to

    ``(1, x, 1, x^-1, y, y^-1)``.

    The result is the tuple ``(A,B,C,D)`` of Laurent polynomials in
    ``x,y``.  It is a formal unit model: ``x`` and ``y`` are invertible
    indeterminates and form one regular ray-unit orbit with their
    inverses.
    """

    dimension = 4
    gaussian_units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    normalizers = ((1, -1), (1, -1), (1, 1), (1, 1))
    packet: list[LaurentPolynomial] = []
    for output, normalizer in zip(
        canonical_dimension_four_packet_directions(),
        normalizers,
    ):
        gaussian_polynomial: dict[LaurentExponent, tuple[int, int]] = {}
        for first in range(dimension):
            for second in range(dimension):
                characteristic = (first, second)
                difference = (
                    (first - output[0]) % dimension,
                    (second - output[1]) % dimension,
                )
                numerator_exponent = (
                    _canonical_dimension_four_monomial(characteristic)
                )
                denominator_exponent = (
                    _canonical_dimension_four_monomial(difference)
                )
                exponent = (
                    numerator_exponent[0]
                    - denominator_exponent[0],
                    numerator_exponent[1]
                    - denominator_exponent[1],
                )
                phase = gaussian_units[
                    canonical_twist_exponent(
                        dimension, output, characteristic
                    )
                ]
                previous = gaussian_polynomial.get(exponent, (0, 0))
                gaussian_polynomial[exponent] = (
                    previous[0] + phase[0],
                    previous[1] + phase[1],
                )
        polynomial: LaurentPolynomial = {}
        for exponent, phase in gaussian_polynomial.items():
            assert (
                phase[1] * normalizer[0]
                - phase[0] * normalizer[1]
                == 0
            )
            polynomial[exponent] = Fraction(
                phase[0] * normalizer[0]
                + phase[1] * normalizer[1],
                2,
            )
        packet.append(
            {
                exponent: value
                for exponent, value in polynomial.items()
                if value
            }
        )
    assert len(packet) == 4
    return (packet[0], packet[1], packet[2], packet[3])


def canonical_dimension_four_character_resolvents(
) -> dict[str, LaurentPolynomial]:
    r"""Return the four Walsh character projections ``T,U,V,W``."""

    first, second, third, fourth = (
        canonical_dimension_four_residual_laurent_packet()
    )
    return {
        "T": _laurent_add(
            (1, first), (1, second), (1, third), (1, fourth)
        ),
        "U": _laurent_add(
            (1, first), (-1, second), (1, third), (-1, fourth)
        ),
        "V": _laurent_add(
            (1, first), (1, second), (-1, third), (-1, fourth)
        ),
        "W": _laurent_add(
            (1, first), (-1, second), (-1, third), (1, fourth)
        ),
    }


def canonical_dimension_four_packet_relation_residuals(
) -> dict[str, LaurentPolynomial]:
    r"""Return exact residuals of the first two packet relations.

    There is no polynomial relation of total degree at most four.  In
    character coordinates ``T,U,V,W``, the first relation has degree
    five.  A particularly short independent degree-six relation is

    ``(V^3-T*U*W)^2 = 16*T^3*U^2``.
    """

    resolvents = canonical_dimension_four_character_resolvents()
    t_value = resolvents["T"]
    u_value = resolvents["U"]
    v_value = resolvents["V"]
    w_value = resolvents["W"]
    degree_five = _laurent_add(
        (
            -16,
            _laurent_multiply(
                _laurent_multiply(t_value, u_value),
                _laurent_power(v_value, 2),
            ),
        ),
        (
            16,
            _laurent_multiply(
                _laurent_power(t_value, 3), u_value
            ),
        ),
        (
            -1,
            _laurent_multiply(
                u_value, _laurent_power(v_value, 4)
            ),
        ),
        (
            2,
            _laurent_multiply(
                _laurent_multiply(
                    t_value, _laurent_power(v_value, 3)
                ),
                w_value,
            ),
        ),
        (
            -1,
            _laurent_multiply(
                _laurent_multiply(
                    _laurent_power(t_value, 2), u_value
                ),
                _laurent_power(w_value, 2),
            ),
        ),
        (
            -1,
            _laurent_multiply(
                _laurent_multiply(
                    _laurent_power(t_value, 2), u_value
                ),
                _laurent_power(v_value, 2),
            ),
        ),
        (
            1,
            _laurent_multiply(
                _laurent_power(t_value, 2),
                _laurent_power(u_value, 3),
            ),
        ),
    )
    degree_six = _laurent_add(
        (
            1,
            _laurent_power(
                _laurent_add(
                    (1, _laurent_power(v_value, 3)),
                    (
                        -1,
                        _laurent_multiply(
                            _laurent_multiply(t_value, u_value),
                            w_value,
                        ),
                    ),
                ),
                2,
            ),
        ),
        (
            -16,
            _laurent_multiply(
                _laurent_power(t_value, 3),
                _laurent_power(u_value, 2),
            ),
        ),
    )
    return {
        "degree_five": degree_five,
        "degree_six": degree_six,
    }


def _weak_compositions(
    total: int, length: int
) -> tuple[tuple[int, ...], ...]:
    """Return weak compositions of ``total`` into ``length`` parts."""

    if length == 1:
        return ((total,),)
    return tuple(
        (first,) + tail
        for first in range(total + 1)
        for tail in _weak_compositions(total - first, length - 1)
    )


def _sparse_laurent_rank(
    polynomials: tuple[LaurentPolynomial, ...],
) -> int:
    """Return exact column rank using sparse Laurent elimination."""

    basis: dict[LaurentExponent, LaurentPolynomial] = {}
    for polynomial in polynomials:
        vector = dict(polynomial)
        while vector:
            pivot = min(vector)
            if pivot not in basis:
                pivot_value = vector[pivot]
                basis[pivot] = {
                    exponent: value / pivot_value
                    for exponent, value in vector.items()
                }
                break
            scalar = vector[pivot]
            vector = _laurent_add(
                (1, vector), (-scalar, basis[pivot])
            )
    return len(basis)


def canonical_dimension_four_relation_nullities(
    maximum_degree: int,
) -> tuple[int, ...]:
    r"""Return counts of packet relations through each positive degree."""

    if maximum_degree < 1:
        raise ValueError("maximum degree must be positive")
    packet = canonical_dimension_four_residual_laurent_packet()
    powers: list[list[LaurentPolynomial]] = []
    for polynomial in packet:
        component_powers = [{(0, 0): Fraction(1)}]
        for _ in range(maximum_degree):
            component_powers.append(
                _laurent_multiply(
                    component_powers[-1], polynomial
                )
            )
        powers.append(component_powers)

    nullities: list[int] = []
    monomials: list[tuple[int, ...]] = []
    for degree in range(1, maximum_degree + 1):
        monomials.extend(_weak_compositions(degree, len(packet)))
        composed: list[LaurentPolynomial] = []
        for monomial in ((0, 0, 0, 0), *monomials):
            value: LaurentPolynomial = {(0, 0): Fraction(1)}
            for index, exponent in enumerate(monomial):
                value = _laurent_multiply(
                    value, powers[index][exponent]
                )
            composed.append(value)
        nullities.append(
            len(composed) - _sparse_laurent_rank(tuple(composed))
        )
    return tuple(nullities)


def canonical_dimension_four_packet_evaluation(
    x_value: int | Fraction,
    y_value: int | Fraction,
) -> tuple[Fraction, Fraction, Fraction, Fraction]:
    """Evaluate the normalized formal packet at nonzero rational ``x,y``."""

    x_fraction = Fraction(x_value)
    y_fraction = Fraction(y_value)
    if x_fraction == 0 or y_fraction == 0:
        raise ValueError("Laurent variables must be nonzero")
    values: list[Fraction] = []
    for polynomial in canonical_dimension_four_residual_laurent_packet():
        values.append(
            sum(
                coefficient
                * x_fraction ** exponent[0]
                * y_fraction ** exponent[1]
                for exponent, coefficient in polynomial.items()
            )
        )
    assert len(values) == 4
    return (values[0], values[1], values[2], values[3])


def biquadratic_2_3_multiply(
    left: BiquadraticCoordinate,
    right: BiquadraticCoordinate,
) -> BiquadraticCoordinate:
    r"""Multiply coordinates in the basis ``(1,sqrt(2),sqrt(3),sqrt(6))``."""

    a, b, c, d = left
    e, f, g, h = right
    return (
        a * e + 2 * b * f + 3 * c * g + 6 * d * h,
        a * f + b * e + 3 * c * h + 3 * d * g,
        a * g + c * e + 2 * b * h + 2 * d * f,
        a * h + d * e + b * g + c * f,
    )


def biquadratic_2_3_galois_action(
    value: BiquadraticCoordinate,
    group_index: int,
) -> BiquadraticCoordinate:
    r"""Apply the ordered ``C2 x C2`` action used by the d=4 packet."""

    if not 0 <= group_index < 4:
        raise ValueError("group index must lie between 0 and 3")
    first_signs = (1, -1, -1, 1)
    second_signs = (1, 1, -1, -1)
    first_sign = first_signs[group_index]
    second_sign = second_signs[group_index]
    a, b, c, d = value
    return (
        a,
        first_sign * b,
        second_sign * c,
        first_sign * second_sign * d,
    )


def _biquadratic_power(
    value: BiquadraticCoordinate,
    inverse: BiquadraticCoordinate,
    exponent: int,
) -> BiquadraticCoordinate:
    """Raise a known unit to an arbitrary integer power."""

    result: BiquadraticCoordinate = (
        Fraction(1),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )
    factor = value if exponent >= 0 else inverse
    for _ in range(abs(exponent)):
        result = biquadratic_2_3_multiply(result, factor)
    return result


def _evaluate_laurent_biquadratic(
    polynomial: Mapping[LaurentExponent, Fraction],
    x_value: BiquadraticCoordinate,
    x_inverse: BiquadraticCoordinate,
    y_value: BiquadraticCoordinate,
    y_inverse: BiquadraticCoordinate,
) -> BiquadraticCoordinate:
    """Evaluate a Laurent polynomial at two known biquadratic units."""

    result: BiquadraticCoordinate = (
        Fraction(0),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )
    for exponent, coefficient in polynomial.items():
        term = biquadratic_2_3_multiply(
            _biquadratic_power(
                x_value, x_inverse, exponent[0]
            ),
            _biquadratic_power(
                y_value, y_inverse, exponent[1]
            ),
        )
        result = tuple(
            result[index] + coefficient * term[index]
            for index in range(4)
        )
    return result


def canonical_dimension_four_algebraic_unit_packet_record(
) -> dict[str, object]:
    r"""Return a faithful algebraic-unit Galois countermodel for the packet.

    Work in ``L=Q(sqrt(2),sqrt(3))`` and take

    ``x=(3+2*sqrt(2))*(5+2*sqrt(6))``,
    ``y=(3+2*sqrt(2))*(5-2*sqrt(6))``.

    These are algebraic units.  Their four conjugates are
    ``(x^-1,x,y,y^-1)`` and realize the regular ``C2 x C2`` ray-unit
    permutation.  Nevertheless, the resulting residual packet and all
    four character projections are nonzero.
    """

    one: BiquadraticCoordinate = (
        Fraction(1),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )
    x_value = tuple(
        Fraction(value) for value in (15, 10, 8, 6)
    )
    x_inverse = tuple(
        Fraction(value) for value in (15, -10, 8, -6)
    )
    y_value = tuple(
        Fraction(value) for value in (15, 10, -8, -6)
    )
    y_inverse = tuple(
        Fraction(value) for value in (15, -10, -8, 6)
    )
    assert biquadratic_2_3_multiply(x_value, x_inverse) == one
    assert biquadratic_2_3_multiply(y_value, y_inverse) == one

    packet = tuple(
        _evaluate_laurent_biquadratic(
            polynomial,
            x_value,
            x_inverse,
            y_value,
            y_inverse,
        )
        for polynomial in (
            canonical_dimension_four_residual_laurent_packet()
        )
    )
    character_signs = (
        (1, 1, 1, 1),
        (1, -1, 1, -1),
        (1, 1, -1, -1),
        (1, -1, -1, 1),
    )
    character_values = tuple(
        tuple(
            sum(
                sign * packet[index][coordinate]
                for index, sign in enumerate(signs)
            )
            for coordinate in range(4)
        )
        for signs in character_signs
    )
    return {
        "field": "Q(sqrt(2),sqrt(3))",
        "units": (x_inverse, x_value, y_value, y_inverse),
        "unit_products": (
            biquadratic_2_3_multiply(x_value, x_inverse),
            biquadratic_2_3_multiply(y_value, y_inverse),
        ),
        "packet": packet,
        "character_values": character_values,
        "all_packet_components_nonzero": all(
            any(value) for value in packet
        ),
        "all_character_values_nonzero": all(
            any(value) for value in character_values
        ),
    }


def canonical_scalar_distribution_fibers(
    dimension: int,
    divisor: int,
) -> dict[ResidueVector, tuple[ResidueVector, ...]]:
    r"""Return fibers of multiplication by ``divisor`` on the d-grid.

    When ``divisor`` divides ``dimension``, Kopp's
    conductor-lowering/level-raising theorem with ``B=divisor*I``
    specializes to the internal product relation

    ``u(divisor*q) = product_{divisor*t=divisor*q} u(t)``.
    """

    canonical_form(dimension)
    if divisor <= 0 or dimension % divisor:
        raise ValueError("divisor must be a positive divisor of dimension")
    fibers: dict[ResidueVector, list[ResidueVector]] = {}
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            image = (
                divisor * first % dimension,
                divisor * second % dimension,
            )
            fibers.setdefault(image, []).append(characteristic)
    return {
        image: tuple(characteristics)
        for image, characteristics in sorted(fibers.items())
    }


def canonical_proper_scalar_distribution_divisors(
    dimension: int,
) -> tuple[int, ...]:
    """Return nontrivial scalar distribution maps internal to the d-grid."""

    canonical_form(dimension)
    return tuple(
        divisor
        for divisor in range(2, dimension)
        if dimension % divisor == 0
    )


def canonical_dimension_four_internal_distribution_maps(
) -> tuple[Matrix2, Matrix2, Matrix2, Matrix2]:
    r"""Return all d=4 internal distribution maps modulo global units.

    An integral multiplication endomorphism whose complete torus kernel
    lies in the four-torsion has Smith factors dividing four.  For the
    canonical norm form this leaves ``2`` times the three powers of
    ``beta`` and the zero map induced by ``4``.
    """

    dimension = 4
    maps: list[Matrix2] = []
    for global_unit in canonical_global_unit_residues(dimension):
        unit_matrix = canonical_residue_multiplication_matrix(
            dimension, global_unit
        )
        maps.append(
            matrix_mod(
                tuple(
                    tuple(2 * entry for entry in row)
                    for row in unit_matrix
                ),
                dimension,
            )
        )
    maps.append(((0, 0), (0, 0)))
    return (maps[0], maps[1], maps[2], maps[3])


def canonical_dimension_four_distribution_relation_record(
) -> dict[str, object]:
    r"""Audit all internal d=4 distribution relations on the countermodel."""

    def monomial(characteristic: ResidueVector) -> LaurentExponent:
        return _canonical_dimension_four_monomial(characteristic)

    formal_defects: dict[
        tuple[int, ResidueVector], LaurentExponent
    ] = {}
    for divisor in (2, 4):
        for image, fiber in canonical_scalar_distribution_fibers(
            4, divisor
        ).items():
            right_exponent = (
                sum(monomial(value)[0] for value in fiber),
                sum(monomial(value)[1] for value in fiber),
            )
            left_exponent = monomial(image)
            formal_defects[(divisor, image)] = (
                right_exponent[0] - left_exponent[0],
                right_exponent[1] - left_exponent[1],
            )

    algebraic_record = (
        canonical_dimension_four_algebraic_unit_packet_record()
    )
    inverse_x, x_value, y_value, inverse_y = algebraic_record[
        "units"
    ]
    one: BiquadraticCoordinate = (
        Fraction(1),
        Fraction(0),
        Fraction(0),
        Fraction(0),
    )
    orbit_values = {
        (0, 0): one,
        (0, 1): x_value,
        (0, 2): one,
        (0, 3): inverse_x,
        (1, 1): y_value,
        (2, 3): inverse_y,
    }

    def algebraic_value(
        characteristic: ResidueVector,
    ) -> BiquadraticCoordinate:
        return orbit_values[
            canonical_zauner_orbit_representative(
                4, characteristic
            )
        ]

    algebraic_equalities: dict[
        tuple[int, ResidueVector], bool
    ] = {}
    for divisor in (2, 4):
        for image, fiber in canonical_scalar_distribution_fibers(
            4, divisor
        ).items():
            product = one
            for characteristic in fiber:
                product = biquadratic_2_3_multiply(
                    product, algebraic_value(characteristic)
                )
            algebraic_equalities[(divisor, image)] = (
                product == algebraic_value(image)
            )

    return {
        "internal_maps_mod_4": (
            canonical_dimension_four_internal_distribution_maps()
        ),
        "fiber_sizes": {
            divisor: tuple(
                len(fiber)
                for fiber in canonical_scalar_distribution_fibers(
                    4, divisor
                ).values()
            )
            for divisor in (2, 4)
        },
        "formal_exponent_defects": formal_defects,
        "all_formal_relations_hold": all(
            defect == (0, 0)
            for defect in formal_defects.values()
        ),
        "algebraic_equalities": algebraic_equalities,
        "all_algebraic_relations_hold": all(
            algebraic_equalities.values()
        ),
    }


def canonical_dimension_four_perturbation_witness(
) -> dict[str, object]:
    r"""Return a coefficient proving multiplicative identities cannot imply TCC.

    Multiply any nonzero Zauner-invariant baseline array by the formal
    unit perturbation from cycle 8.  That perturbation preserves inverse
    pairing, the fixed half-characteristic values, and every internal
    d=4 distribution relation.  In the primitive residual at ``p=e_1``,
    the coefficient of ``x^2`` comes only from two terms.  Both have the
    same baseline ratio and their phases sum to ``1-i``, so the
    perturbed residual is never the zero Laurent polynomial.
    """

    dimension = 4
    output = (1, 0)
    target_exponent = (2, 0)
    terms: list[
        tuple[
            ResidueVector,
            int,
            ResidueVector,
            ResidueVector,
        ]
    ] = []
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            difference = ((first - 1) % dimension, second)
            numerator_orbit = (
                canonical_zauner_orbit_representative(
                    dimension, characteristic
                )
            )
            denominator_orbit = (
                canonical_zauner_orbit_representative(
                    dimension, difference
                )
            )
            numerator_exponent = (
                _canonical_dimension_four_monomial(characteristic)
            )
            denominator_exponent = (
                _canonical_dimension_four_monomial(difference)
            )
            exponent = (
                numerator_exponent[0]
                - denominator_exponent[0],
                numerator_exponent[1]
                - denominator_exponent[1],
            )
            if exponent == target_exponent:
                terms.append(
                    (
                        characteristic,
                        canonical_twist_exponent(
                            dimension, output, characteristic
                        ),
                        numerator_orbit,
                        denominator_orbit,
                    )
                )
    phase_units = ((1, 0), (0, 1), (-1, 0), (0, -1))
    phase_sum = (
        sum(phase_units[term[1]][0] for term in terms),
        sum(phase_units[term[1]][1] for term in terms),
    )
    baseline_ratios = tuple(
        (term[2], term[3]) for term in terms
    )
    return {
        "output": output,
        "laurent_exponent": target_exponent,
        "terms": tuple(terms),
        "phase_sum": phase_sum,
        "baseline_orbit_ratios": baseline_ratios,
        "ratios_are_identical": len(set(baseline_ratios)) == 1,
        "coefficient_is_forced_nonzero": (
            phase_sum != (0, 0)
            and len(set(baseline_ratios)) == 1
        ),
    }


def q_pochhammer_fractional_cell_determinant_coefficient(
) -> LaurentPolynomial:
    r"""Return the first obstruction to a scalar Hirota cell identity.

    Put ``F(w)=(w;q)_infinity`` and let ``s`` and ``t`` encode the
    horizontal and vertical fractional characteristic shifts.  For

    ``D(w)=F(w)F(s*t*w)-F(s*w)F(t*w)``,

    Euler's expansion gives

    ``[w]D=(-1+s+t-s*t)/(1-q)``.

    The returned polynomial is the numerator, indexed by powers of
    ``(s,t)``.  It is ``-(1-s)(1-t)``, hence is nonzero for a genuine
    fractional cell.
    """

    return {
        (0, 0): Fraction(-1),
        (1, 0): Fraction(1),
        (0, 1): Fraction(1),
        (1, 1): Fraction(-1),
    }


def canonical_dimension_four_fractional_cell_record(
) -> dict[str, object]:
    r"""Audit closed-cell elimination and the first Hirota candidate.

    Edge quotients of any nonzero vertex array form a pure-gauge
    connection, so their elementary-cell holonomy is identically one.
    The cycle-8 formal deformation therefore passes every such
    elimination.  The bilinear vertex determinant does detect the
    deformation, but the first coefficient of the actual
    q-Pochhammer product proves that determinant is not an analytic
    identity.
    """

    dimension = 4
    holonomy_defects: dict[ResidueVector, LaurentExponent] = {}
    bilinear_defects: dict[ResidueVector, LaurentExponent] = {}
    for first in range(dimension):
        for second in range(dimension):
            lower_left = (first, second)
            lower_right = ((first + 1) % dimension, second)
            upper_left = (first, (second + 1) % dimension)
            upper_right = (
                (first + 1) % dimension,
                (second + 1) % dimension,
            )
            exponents = tuple(
                _canonical_dimension_four_monomial(characteristic)
                for characteristic in (
                    lower_left,
                    lower_right,
                    upper_left,
                    upper_right,
                )
            )
            lower_horizontal = (
                exponents[1][0] - exponents[0][0],
                exponents[1][1] - exponents[0][1],
            )
            right_vertical = (
                exponents[3][0] - exponents[1][0],
                exponents[3][1] - exponents[1][1],
            )
            left_vertical = (
                exponents[2][0] - exponents[0][0],
                exponents[2][1] - exponents[0][1],
            )
            upper_horizontal = (
                exponents[3][0] - exponents[2][0],
                exponents[3][1] - exponents[2][1],
            )
            holonomy_defects[lower_left] = (
                lower_horizontal[0]
                + right_vertical[0]
                - left_vertical[0]
                - upper_horizontal[0],
                lower_horizontal[1]
                + right_vertical[1]
                - left_vertical[1]
                - upper_horizontal[1],
            )
            bilinear_defects[lower_left] = (
                exponents[0][0]
                + exponents[3][0]
                - exponents[1][0]
                - exponents[2][0],
                exponents[0][1]
                + exponents[3][1]
                - exponents[1][1]
                - exponents[2][1],
            )

    coefficient = (
        q_pochhammer_fractional_cell_determinant_coefficient()
    )
    return {
        "cell_count": len(holonomy_defects),
        "holonomy_defects": holonomy_defects,
        "all_holonomies_are_trivial": all(
            defect == (0, 0)
            for defect in holonomy_defects.values()
        ),
        "flatness_rejects_deformation": any(
            defect != (0, 0)
            for defect in holonomy_defects.values()
        ),
        "bilinear_deformation_defects": bilinear_defects,
        "bilinear_rejects_deformation_on_every_cell": all(
            defect != (0, 0)
            for defect in bilinear_defects.values()
        ),
        "q_pochhammer_determinant_linear_coefficient": coefficient,
        "q_pochhammer_bilinear_identity_holds": not any(
            coefficient.values()
        ),
        "gate_table": {
            "closed_cell_flatness": {
                "analytic_identity": True,
                "rejects_deformation": False,
                "viable": False,
            },
            "rank_one_bilinear": {
                "analytic_identity": False,
                "rejects_deformation": True,
                "viable": False,
            },
        },
        "any_candidate_passes_both_gates": False,
    }


def canonical_floquet_transfer_support(
    dimension: int,
) -> tuple[tuple[ResidueVector, ResidueVector], ...]:
    r"""Return the support of one ``L_d`` characteristic transfer.

    The Jacobi transformation law has the form

    ``P_{L_d*q}(L_d*tau) = kappa_q(tau) P_q(tau)``.

    Thus its vector transfer matrix is a weighted permutation: every
    source and every target occurs exactly once.
    """

    canonical_form(dimension)
    return tuple(
        (
            (first, second),
            canonical_zauner_action(dimension, (first, second)),
        )
        for first in range(dimension)
        for second in range(dimension)
    )


def canonical_floquet_block_degrees(
    dimension: int,
) -> tuple[int, ...]:
    r"""Return degrees of the weighted-cycle characteristic factors.

    A weighted permutation decomposes over Zauner orbits.  An orbit of
    length ``ell`` contributes a factor ``lambda^ell-c``, where ``c``
    is the product of its edge weights.
    """

    return tuple(
        len(orbit) for orbit in canonical_zauner_orbits(dimension)
    )


def canonical_floquet_commutator_trace_signature(
    dimension: int,
    output: ResidueVector,
) -> dict[tuple[int, ResidueVector, ResidueVector], int]:
    r"""Return the formal trace of the Floquet/translation commutator.

    Let ``D=diag(u(q))``, let ``T_p e_q=e_{q+p}``, and let
    ``W_p e_q=omega^<p,(I+L)q> e_q``.  Then

    ``Tr(W_p D T_p D^-1 T_p^-1)``

    is exactly the canonical TCC residual.  This returns its
    orbit-reduced formal signature.
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
            basis_index = (first, second)
            translated_back = (
                (first - reduced_output[0]) % dimension,
                (second - reduced_output[1]) % dimension,
            )
            key = (
                canonical_twist_exponent(
                    dimension, reduced_output, basis_index
                ),
                canonical_zauner_orbit_representative(
                    dimension, basis_index
                ),
                canonical_zauner_orbit_representative(
                    dimension, translated_back
                ),
            )
            signature[key] = signature.get(key, 0) + 1
    return signature


def canonical_dimension_four_floquet_gate_record(
) -> dict[str, object]:
    r"""Audit the RM Floquet transfer against the formal deformation.

    The one-step transfer is a weighted Zauner permutation.  Assigning
    one formal deformation weight to one edge of each three-cycle lifts
    the cycle-9 vertex deformation to that transfer.  Its three-step
    monodromy is exactly the deformed diagonal array, so weighted-cycle
    structure and its spectral factorization do not reject the
    deformation.
    """

    dimension = 4
    orbits = canonical_zauner_orbits(dimension)
    edge_exponents: dict[ResidueVector, LaurentExponent] = {}
    for orbit in orbits:
        target = _canonical_dimension_four_monomial(orbit[0])
        for index, characteristic in enumerate(orbit):
            edge_exponents[characteristic] = (
                target if len(orbit) == 3 and index == 0 else (0, 0)
            )

    monodromy_defects: dict[
        ResidueVector, LaurentExponent
    ] = {}
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            current = characteristic
            total = (0, 0)
            for _ in range(3):
                edge = edge_exponents[current]
                total = (
                    total[0] + edge[0],
                    total[1] + edge[1],
                )
                current = canonical_zauner_action(
                    dimension, current
                )
            target = _canonical_dimension_four_monomial(
                characteristic
            )
            monodromy_defects[characteristic] = (
                total[0] - target[0],
                total[1] - target[1],
            )

    support = canonical_floquet_transfer_support(dimension)
    sources = tuple(source for source, _ in support)
    targets = tuple(target for _, target in support)
    algebraic_packet = (
        canonical_dimension_four_algebraic_unit_packet_record()
    )
    primitive_witness = (
        canonical_dimension_four_perturbation_witness()
    )
    return {
        "dimension": dimension,
        "block_degrees": canonical_floquet_block_degrees(dimension),
        "gauge_invariant_cycle_count": len(orbits),
        "transfer_nonzero_count": len(support),
        "one_nonzero_per_source": len(set(sources)) == dimension**2,
        "one_nonzero_per_target": len(set(targets)) == dimension**2,
        "edge_exponents": edge_exponents,
        "monodromy_defects": monodromy_defects,
        "deformation_lifts_to_weighted_transfer": all(
            defect == (0, 0)
            for defect in monodromy_defects.values()
        ),
        "weighted_transfer_rejects_deformation": any(
            defect != (0, 0)
            for defect in monodromy_defects.values()
        ),
        "primitive_commutator_trace_signature": (
            canonical_floquet_commutator_trace_signature(
                dimension, (1, 0)
            )
        ),
        "primitive_trace_coefficient_is_forced_nonzero": (
            primitive_witness["coefficient_is_forced_nonzero"]
        ),
        "algebraic_commutator_trace_packet_is_nonzero": (
            algebraic_packet["all_packet_components_nonzero"]
        ),
        "floquet_spectrum_alone_can_force_tcc": False,
        "missing_structure": (
            "a non-pure-gauge characteristic translation compatible "
            "with RM monodromy"
        ),
    }


def canonical_zak_cocycle_exponent(
    dimension: int,
    left: ResidueVector,
    right: ResidueVector,
) -> int:
    r"""Return the exponent of the canonical Zak cocycle.

    With ``Z=I+L_d``, the cocycle is

    ``sigma(q,r)=omega_d^<r,Z*q>``.
    """

    return canonical_twist_exponent(dimension, right, left)


def canonical_zak_quadratic_exponent(
    dimension: int,
    vector: ResidueVector,
) -> int:
    r"""Return the chirp exponent ``<q,Z*q>`` modulo ``d``."""

    return canonical_twist_exponent(dimension, vector, vector)


def canonical_zak_alternating_exponent(
    dimension: int,
    left: ResidueVector,
    right: ResidueVector,
) -> int:
    r"""Return the alternating bicharacter exponent of ``sigma``.

    It equals ``-<left,right>`` modulo ``d`` and is therefore
    nondegenerate on ``(Z/dZ)^2``.
    """

    return (
        canonical_zak_cocycle_exponent(
            dimension, left, right
        )
        - canonical_zak_cocycle_exponent(
            dimension, right, left
        )
    ) % dimension


def canonical_zak_representation_action(
    dimension: int,
    characteristic: ResidueVector,
    basis_index: int,
) -> tuple[int, int]:
    r"""Apply the explicit Weyl representative to a standard basis node.

    Let ``tau_d=-exp(pi*i/d)``, so ``tau_d^2=omega_d``, and let
    ``X e_j=e_(j+1)``, ``Z e_j=omega_d^j e_j``.  The projective
    representation

    ``rho(a,b)=tau_d^(a^2+b^2) X^a Z^(-b)``

    realizes the canonical Zak cocycle.  The return value is the target
    basis index and the exponent of ``tau_d`` modulo its order.
    """

    canonical_form(dimension)
    first = characteristic[0] % dimension
    second = characteristic[1] % dimension
    source = basis_index % dimension
    phase_modulus = extended_displacement_modulus(dimension)
    return (
        (source + first) % dimension,
        (
            first * first
            + second * second
            - 2 * second * source
        )
        % phase_modulus,
    )


def canonical_zak_representation_product_defect(
    dimension: int,
    left: ResidueVector,
    right: ResidueVector,
    basis_index: int,
) -> tuple[int, int]:
    r"""Return target and phase defects in ``rho(q)rho(r)=sigma(q,r)rho(q+r)``."""

    intermediate, right_phase = (
        canonical_zak_representation_action(
            dimension, right, basis_index
        )
    )
    actual_target, left_phase = (
        canonical_zak_representation_action(
            dimension, left, intermediate
        )
    )
    total = (
        (left[0] + right[0]) % dimension,
        (left[1] + right[1]) % dimension,
    )
    expected_target, expected_phase = (
        canonical_zak_representation_action(
            dimension, total, basis_index
        )
    )
    cocycle_phase = 2 * canonical_zak_cocycle_exponent(
        dimension, left, right
    )
    phase_modulus = extended_displacement_modulus(dimension)
    return (
        (actual_target - expected_target) % dimension,
        (
            left_phase
            + right_phase
            - cocycle_phase
            - expected_phase
        )
        % phase_modulus,
    )


def canonical_zak_matrix_entry_terms(
    dimension: int,
    row: int,
    column: int,
) -> tuple[tuple[ResidueVector, int], ...]:
    r"""Return terms contributing to one entry of the finite Zak matrix.

    If ``Zak(f)=sum_(a,b) f(a,b) rho(a,b)``, then the ``(k,j)`` entry is

    ``sum_b f(k-j,b) tau_d^((k-j)^2+b^2-2*b*j)``.
    """

    canonical_form(dimension)
    reduced_row = row % dimension
    reduced_column = column % dimension
    first = (reduced_row - reduced_column) % dimension
    return tuple(
        (
            (first, second),
            canonical_zak_representation_action(
                dimension,
                (first, second),
                reduced_column,
            )[1],
        )
        for second in range(dimension)
    )


def canonical_dimension_four_zak_gate_record(
) -> dict[str, object]:
    r"""Return the exact finite Zak reformulation and deformation gate."""

    dimension = 4
    phase_defects: dict[
        tuple[ResidueVector, ResidueVector], int
    ] = {}
    for output_first in range(dimension):
        for output_second in range(dimension):
            output = (output_first, output_second)
            for first in range(dimension):
                for second in range(dimension):
                    characteristic = (first, second)
                    remainder = (
                        (output_first - first) % dimension,
                        (output_second - second) % dimension,
                    )
                    twisted_exponent = (
                        canonical_zak_cocycle_exponent(
                            dimension,
                            characteristic,
                            remainder,
                        )
                        + canonical_zak_quadratic_exponent(
                            dimension, characteristic
                        )
                    ) % dimension
                    phase_defects[(output, characteristic)] = (
                        twisted_exponent
                        - canonical_twist_exponent(
                            dimension, output, characteristic
                        )
                    ) % dimension

    representation_defects: dict[
        tuple[ResidueVector, ResidueVector, int],
        tuple[int, int],
    ] = {}
    for left_first in range(dimension):
        for left_second in range(dimension):
            left = (left_first, left_second)
            for right_first in range(dimension):
                for right_second in range(dimension):
                    right = (right_first, right_second)
                    for basis_index in range(dimension):
                        representation_defects[
                            (left, right, basis_index)
                        ] = (
                            canonical_zak_representation_product_defect(
                                dimension,
                                left,
                                right,
                                basis_index,
                            )
                        )

    nondegenerate = True
    for first in range(dimension):
        for second in range(dimension):
            characteristic = (first, second)
            if characteristic == (0, 0):
                continue
            if not any(
                canonical_zak_alternating_exponent(
                    dimension,
                    characteristic,
                    (test_first, test_second),
                )
                for test_first in range(dimension)
                for test_second in range(dimension)
            ):
                nondegenerate = False

    witness = canonical_dimension_four_perturbation_witness()
    return {
        "group_order": dimension**2,
        "matrix_dimension": dimension,
        "twisted_algebra_dimension": dimension**2,
        "terms_per_matrix_entry": tuple(
            len(
                canonical_zak_matrix_entry_terms(
                    dimension, row, column
                )
            )
            for row in range(dimension)
            for column in range(dimension)
        ),
        "phase_defects": phase_defects,
        "all_residual_phases_match": not any(
            phase_defects.values()
        ),
        "representation_defects": representation_defects,
        "representation_is_exact": all(
            defect == (0, 0)
            for defect in representation_defects.values()
        ),
        "alternating_bicharacter_is_nondegenerate": nondegenerate,
        "zak_transform_closes_on_finite_matrices": True,
        "matrix_target": "Zak(F) Zak(V) = d^2 I_d",
        "deformation_rejects_matrix_target": (
            witness["coefficient_is_forced_nonzero"]
        ),
        "matrix_target_proved_for_rm_values": False,
    }


def canonical_beta_power_trace(
    dimension: int,
    exponent: int,
) -> int:
    r"""Return ``beta_d^n + beta_d^(-n)`` exactly.

    The canonical quadratic equation gives

    ``beta_d + beta_d^(-1) = d - 1``.

    The returned integer is generated by the corresponding Chebyshev
    recurrence.  It avoids introducing floating-point quadratic
    radicals into the reflection reduction.
    """

    canonical_form(dimension)
    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    if exponent == 0:
        return 2
    previous = 2
    current = dimension - 1
    for _ in range(2, exponent + 1):
        previous, current = (
            current,
            (dimension - 1) * current - previous,
        )
    return current


def canonical_cyclic_approximant_pair(
    dimension: int,
    index: int,
) -> tuple[int, int]:
    r"""Return the reduced Chebyshev approximant to ``beta_d``.

    Write ``S_n=beta_d^n+beta_d^(-n)``.  The modular-geodesic
    approximants used in the cyclic-quantum-dilogarithm formula are

    ``t_n=S_(n-1)/S_n``.

    Consecutive ``S`` values have constant gcd
    ``gcd(2,d-1)``, so the returned numerator and denominator are
    coprime.  Their ratio tends to the small fixed point ``beta_d``.
    """

    canonical_form(dimension)
    if index < 1:
        raise ValueError("approximant index must be positive")
    divisor = gcd(2, dimension - 1)
    numerator = canonical_beta_power_trace(dimension, index - 1)
    denominator = canonical_beta_power_trace(dimension, index)
    assert numerator % divisor == 0
    assert denominator % divisor == 0
    reduced = (numerator // divisor, denominator // divisor)
    assert gcd(*reduced) == 1
    return reduced


def canonical_cyclic_approximant_record(
    dimension: int,
    index: int,
    total_series_index: int,
) -> dict[str, object]:
    r"""Audit the cyclic-dilogarithm approximation route to TCC.

    For ``a=d-1``, the Chebyshev recurrence has period three modulo
    ``d``.  This is the arithmetic shadow of ``L_d^3 in Gamma(d)``:
    the reduced root-of-unity approximants at indices ``n`` and
    ``n+3`` have identical numerator and denominator residues modulo
    ``d``.

    The rational boundary monomial at ``t_n=M_n/N_n`` is
    ``exp(2*pi*i*M_n*J/N_n)``.  Since ``M_n,N_n`` are coprime, its
    difference from one is retained exactly when ``N_n`` does not
    divide ``J``.  Thus fixed positive series degrees survive for all
    sufficiently large approximants instead of suffering the
    premature equal-base cancellation from cycle 13.
    """

    canonical_form(dimension)
    if total_series_index < 0:
        raise ValueError("total series index must be nonnegative")
    numerator, denominator = canonical_cyclic_approximant_pair(
        dimension, index
    )
    shifted_numerator, shifted_denominator = (
        canonical_cyclic_approximant_pair(dimension, index + 3)
    )
    denominator_coprime = gcd(denominator, dimension) == 1
    monomial_is_one = total_series_index % denominator == 0
    stabilizer = canonical_stabilizer(dimension)
    return {
        "index": index,
        "conductor_step": 3,
        "approximant": (numerator, denominator),
        "shifted_approximant": (
            shifted_numerator,
            shifted_denominator,
        ),
        "approximants_are_reduced": (
            gcd(numerator, denominator) == 1
            and gcd(shifted_numerator, shifted_denominator) == 1
        ),
        "same_residues_after_conductor_step": (
            numerator % dimension == shifted_numerator % dimension
            and denominator % dimension
            == shifted_denominator % dimension
        ),
        "level_step_is_identity": (
            matrix_mod(matrix_power(stabilizer, 3), dimension)
            == IDENTITY_2
        ),
        "denominator_coprime_to_dimension": denominator_coprime,
        "safe_universal_subsequence": index % 3 in (1, 2),
        "total_series_index": total_series_index,
        "rational_boundary_monomial_is_one": monomial_is_one,
        "off_grid_factor_is_retained": not monomial_is_one,
        "cyclic_limit_available_for_identity_shintani_invariant": True,
        "cyclic_limit_covers_full_characteristic_packet": False,
        "cyclic_limit_retains_signed_sf_phases": False,
        "finite_five_term_tcc_identity_proved": False,
    }


def canonical_zak_reflection_quadratic_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return the exact one-matrix reduction of canonical TCC.

    Write ``A=Zak(F)`` and ``B=Zak(V)`` as in cycle 12.  The fixed-point
    reflection theorem and the Shintani--Faddeev phase imply

    ``B = c0*A + delta*I``.

    The exceptional zero characteristic is responsible for ``delta``;
    omitting it gives a false coefficient-conjugation or adjoint
    identity.  After scaling ``C=s*A`` with ``s^2=c0``, TCC is

    ``C^2 - d*sqrt(d-3)*C - d^2*I = 0``.

    Equivalently,

    ``H=(2*C-d*sqrt(d-3)*I)/(d*sqrt(d+1))``

    must be an involution.  Its trace is unconditionally ``2-d``.
    """

    canonical_form(dimension)
    beta_cube_trace = canonical_beta_power_trace(dimension, 3)
    sum_square = beta_cube_trace + 2
    difference_square = beta_cube_trace - 2
    expected_sum_square = (
        (dimension - 2) ** 2 * (dimension + 1)
    )
    expected_difference_square = (
        dimension * dimension * (dimension - 3)
    )
    return {
        "beta_cube_plus_inverse": beta_cube_trace,
        "sqrt_lambda_sum_square": sum_square,
        "expected_sqrt_lambda_sum_square": expected_sum_square,
        "sqrt_lambda_sum_square_residual": (
            sum_square - expected_sum_square
        ),
        "sqrt_lambda_difference_square": difference_square,
        "expected_sqrt_lambda_difference_square": (
            expected_difference_square
        ),
        "sqrt_lambda_difference_square_residual": (
            difference_square - expected_difference_square
        ),
        "affine_reflection_reduction": "B = c0 A + delta I",
        "zero_characteristic_correction_is_required": True,
        "scaled_quadratic_target": (
            "C^2 - d sqrt(d-3) C - d^2 I = 0"
        ),
        "normalized_target": "H^2 = I_d",
        "normalization_square": (
            dimension * dimension * (dimension + 1)
        ),
        "trace_h": 2 - dimension,
        "conditional_eigenvalue_multiplicities": (
            1,
            dimension - 1,
        ),
        "reflection_alone_proves_involution": False,
        "rm_involution_proved": False,
    }


def canonical_reciprocal_trace_moment_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return the quadratic moments forced before TCC.

    For canonical rank one, write the ghost Weyl coefficients as
    ``a_0=1`` and ``a_p=c*u_p`` off zero, where
    ``c^2=1/(d+1)`` and ``u_p*u_(-p)=1``.  Weyl orthogonality then
    forces ``Tr(Pi)=Tr(Pi^2)=1``.  Thus ``H=2*Pi-I`` has the correct
    first two trace moments even when its traceless square is nonzero.
    """

    canonical_form(dimension)
    scale_square = Fraction(1, dimension + 1)
    trace_pi_square = Fraction(
        1 + (dimension * dimension - 1) * scale_square,
        dimension,
    )
    trace_h_square = (
        4 * trace_pi_square - 4 + dimension
    )
    second_elementary_symmetric_h = (
        (2 - dimension) ** 2 - trace_h_square
    ) // 2
    return {
        "off_zero_scale_square": scale_square,
        "trace_pi": 1,
        "trace_pi_square": trace_pi_square,
        "trace_h": 2 - dimension,
        "trace_h_square": trace_h_square,
        "second_elementary_symmetric_h": (
            second_elementary_symmetric_h
        ),
        "first_unforced_spectral_moment_degree": 3,
        "identity_coefficient_of_h_square_is_forced": True,
        "traceless_coefficients_of_h_square_are_forced": False,
        "idempotency_equivalent_to_rank_one": True,
        "rank_one_equivalent_to_vanishing_two_by_two_minors": True,
    }


def canonical_odd_constant_overlap_countermodel_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return an exact Hermitian nonprojector with all coarse moments.

    For odd ``d``, put every nonzero normalized overlap equal to one.
    With ``c^2=1/(d+1)``, the resulting operator is

    ``Pi_* = ((1-c)/d) I + c P``,

    where ``P`` is parity.  It is ordinarily Hermitian, reciprocal,
    Zauner invariant, and has ``Tr(Pi_*)=Tr(Pi_*^2)=1``, but its
    negative-parity eigenvalue is negative.  Every nonzero twisted
    convolution residual equals ``(2-d)c-2c^2``, which is strictly
    negative.
    """

    canonical_form(dimension)
    if dimension % 2 == 0:
        raise ValueError("the constant-overlap record requires odd d")
    scale_square = Fraction(1, dimension + 1)
    zero_residual = (
        1
        + (dimension * dimension - 1) * scale_square
        - dimension
    )
    moments = canonical_reciprocal_trace_moment_record(dimension)
    return {
        "dimension": dimension,
        "off_zero_normalized_overlap": 1,
        "off_zero_scale_square": scale_square,
        "operator_formula": "Pi_* = ((1-c)/d) I + c P",
        "parity_multiplicities": (
            (dimension + 1) // 2,
            (dimension - 1) // 2,
        ),
        "positive_parity_eigenvalue": (
            "lambda_+ = (1+(d-1)c)/d"
        ),
        "negative_parity_eigenvalue": (
            "lambda_- = (1-sqrt(d+1))/d"
        ),
        "negative_parity_eigenvalue_is_negative": True,
        "real": True,
        "reciprocal": True,
        "periodic": True,
        "zauner_invariant": True,
        "ordinarily_hermitian": True,
        "trace_pi": moments["trace_pi"],
        "trace_pi_square": moments["trace_pi_square"],
        "trace_h": moments["trace_h"],
        "trace_h_square": moments["trace_h_square"],
        "zero_twisted_residual": zero_residual,
        "nonzero_twisted_residual": "(2-d)c-2c^2",
        "nonzero_twisted_residual_is_negative": True,
        "is_idempotent": False,
        "h_is_involution": False,
    }


def canonical_ghost_weyl_entry_terms(
    dimension: int,
    row: int,
    column: int,
) -> tuple[tuple[ResidueVector, int], ...]:
    r"""Return the Weyl coefficients contributing to one ghost entry.

    With ``D_(a,b)=tau^(a*b) X^a Z^b`` and Weyl coefficient ``mu``,

    ``d*Pi[j,k] = sum_b mu_(j-k,b) tau^(b*(j+k))``.

    The returned phase exponent is reduced modulo the extended
    displacement modulus.  This partial Fourier form turns each
    rank-one minor into an explicit bilinear exchange identity.
    """

    canonical_form(dimension)
    reduced_row = row % dimension
    reduced_column = column % dimension
    displacement = (reduced_row - reduced_column) % dimension
    modulus = extended_displacement_modulus(dimension)
    return tuple(
        (
            (displacement, second),
            (second * (reduced_row + reduced_column)) % modulus,
        )
        for second in range(dimension)
    )


def canonical_ghost_minor_record(
    dimension: int,
    rows: tuple[int, int],
    columns: tuple[int, int],
) -> dict[str, object]:
    r"""Return one explicit two-by-two determinantal TCC target."""

    canonical_form(dimension)
    reduced_rows = tuple(row % dimension for row in rows)
    reduced_columns = tuple(
        column % dimension for column in columns
    )
    if reduced_rows[0] == reduced_rows[1]:
        raise ValueError("minor rows must be distinct modulo d")
    if reduced_columns[0] == reduced_columns[1]:
        raise ValueError("minor columns must be distinct modulo d")
    pair_count = dimension * (dimension - 1) // 2
    return {
        "rows": reduced_rows,
        "columns": reduced_columns,
        "positive_entries": (
            canonical_ghost_weyl_entry_terms(
                dimension, reduced_rows[0], reduced_columns[0]
            ),
            canonical_ghost_weyl_entry_terms(
                dimension, reduced_rows[1], reduced_columns[1]
            ),
        ),
        "negative_entries": (
            canonical_ghost_weyl_entry_terms(
                dimension, reduced_rows[0], reduced_columns[1]
            ),
            canonical_ghost_weyl_entry_terms(
                dimension, reduced_rows[1], reduced_columns[0]
            ),
        ),
        "terms_per_product": dimension * dimension,
        "expanded_signed_term_count": 2 * dimension * dimension,
        "all_two_by_two_minor_count": pair_count * pair_count,
        "fixed_nonzero_pivot_equation_count": (
            (dimension - 1) * (dimension - 1)
        ),
        "minor_vanishing_equivalent_to_rank_one_collectively": True,
    }


def matrix_exterior_square_energy(
    matrix: tuple[tuple[complex, ...], ...],
) -> float:
    r"""Return the sum of the squared absolute values of all 2-minors.

    This is ``||wedge^2(matrix)||_F^2``.  It vanishes exactly when the
    matrix has rank at most one, and is the positive scalar certificate
    used in cycle 16.
    """

    if not matrix or not matrix[0]:
        return 0.0
    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("matrix rows must have equal length")
    energy = 0.0
    for first_row, second_row in combinations(range(len(matrix)), 2):
        for first_column, second_column in combinations(
            range(column_count), 2
        ):
            minor = (
                matrix[first_row][first_column]
                * matrix[second_row][second_column]
                - matrix[first_row][second_column]
                * matrix[second_row][first_column]
            )
            energy += abs(minor) ** 2
    return energy


def matrix_gram_second_elementary(
    matrix: tuple[tuple[complex, ...], ...],
) -> float:
    r"""Return ``((Tr K* K)^2-Tr((K* K)^2))/2``.

    Cauchy--Binet identifies this number with
    :func:`matrix_exterior_square_energy`.
    """

    if not matrix or not matrix[0]:
        return 0.0
    column_count = len(matrix[0])
    if any(len(row) != column_count for row in matrix):
        raise ValueError("matrix rows must have equal length")
    gram = tuple(
        tuple(
            sum(
                matrix[row][first].conjugate() * matrix[row][second]
                for row in range(len(matrix))
            )
            for second in range(column_count)
        )
        for first in range(column_count)
    )
    trace = sum(gram[index][index] for index in range(column_count))
    trace_square = sum(
        gram[first][second] * gram[second][first]
        for first in range(column_count)
        for second in range(column_count)
    )
    return float(((trace * trace - trace_square) / 2).real)


def canonical_ghost_exterior_square_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return the single positive rank-one certificate for canonical TCC.

    If ``K=d*sqrt(d+1)*Pi`` and ``d*Pi[j,k]=W(j-k,k)``, then

    ``||wedge^2 K||_F^2 = (d+1)^2 sum |E(j,l;k,m)|^2``,

    where ``E`` is the sheared partial-Fourier exchange residual from
    cycle 15.  Thus all minors vanish iff one nonnegative scalar does.
    """

    canonical_form(dimension)
    pair_count = dimension * (dimension - 1) // 2
    minor_count = pair_count * pair_count
    block_multiplicities = canonical_zauner_block_multiplicities(
        dimension
    )
    return {
        "dimension": dimension,
        "row_pair_count": pair_count,
        "column_pair_count": pair_count,
        "exchange_residual_count": minor_count,
        "shifted_zak_to_partial_fourier_minor_scale": dimension + 1,
        "energy_scale": (dimension + 1) ** 2,
        "positive_certificate": (
            "Delta_2(K)=((Tr K^*K)^2-Tr((K^*K)^2))/2"
        ),
        "cauchy_binet_form": (
            "Delta_2(K)=sum_{|I|=|J|=2}|det K[I,J]|^2"
        ),
        "partial_fourier_form": (
            "Delta_2(K)=(d+1)^2 sum |E(j,l;k,m)|^2"
        ),
        "zauner_block_multiplicities": block_multiplicities,
        "zauner_positive_sector_count": (
            sum(
                multiplicity * (multiplicity - 1) // 2
                for multiplicity in block_multiplicities
            )
            + sum(
                block_multiplicities[first]
                * block_multiplicities[second]
                for first in range(3)
                for second in range(first + 1, 3)
            )
        ),
        "trace_k_is_nonzero": True,
        "certificate_zero_equivalent_to_rank_one": True,
        "certificate_zero_equivalent_to_tcc": True,
        "certificate_is_nonnegative_in_complex_embedding": True,
        "certificate_is_holomorphic": False,
    }


def matrix_parity_schatten_certificate(
    matrix: tuple[tuple[complex, ...], ...],
) -> dict[str, float]:
    r"""Evaluate the parity-polynomial form of the rank-one certificate.

    Parity acts by ``P e_j=e_(-j)``.  When ``matrix^*=P matrix P``,
    ``J=P matrix`` is Hermitian and

    ``K^*K=J^2``.

    The returned exterior-square and parity-moment energies must then
    agree.
    """

    dimension = len(matrix)
    if dimension == 0 or any(len(row) != dimension for row in matrix):
        raise ValueError("matrix must be nonempty and square")

    parity_product = tuple(
        tuple(matrix[(-row) % dimension][column] for column in range(dimension))
        for row in range(dimension)
    )

    def multiply(
        left: tuple[tuple[complex, ...], ...],
        right: tuple[tuple[complex, ...], ...],
    ) -> tuple[tuple[complex, ...], ...]:
        return tuple(
            tuple(
                sum(
                    left[row][index] * right[index][column]
                    for index in range(dimension)
                )
                for column in range(dimension)
            )
            for row in range(dimension)
        )

    square = multiply(parity_product, parity_product)
    fourth = multiply(square, square)
    trace_square = sum(square[index][index] for index in range(dimension))
    trace_fourth = sum(fourth[index][index] for index in range(dimension))
    parity_moment_energy = (
        (trace_square * trace_square - trace_fourth) / 2
    )

    parity_hermiticity_defect = 0.0
    for row in range(dimension):
        for column in range(dimension):
            defect = (
                matrix[column][row].conjugate()
                - matrix[(-row) % dimension][(-column) % dimension]
            )
            parity_hermiticity_defect = max(
                parity_hermiticity_defect, abs(defect)
            )

    return {
        "parity_hermiticity_max_defect": parity_hermiticity_defect,
        "trace_parity_square": float(trace_square.real),
        "trace_parity_fourth": float(trace_fourth.real),
        "parity_moment_energy": float(parity_moment_energy.real),
        "exterior_square_energy": matrix_exterior_square_energy(matrix),
    }


def canonical_parity_schatten_record(
    dimension: int,
) -> dict[str, object]:
    r"""Return the parity-Hermitian fourth-moment form of canonical TCC.

    For the normalized ghost ``G``, source parity-Hermiticity gives
    ``G^*=PGP``.  Hence ``J=PG`` is Hermitian, ``G^*G=J^2``, and the
    cycle-16 certificate is the polynomial

    ``((Tr J^2)^2-Tr J^4)/2``.

    Reciprocal pairing only bounds ``Tr J^2=||G||_F^2`` below by one;
    it does not force the fourth-moment equality.
    """

    canonical_form(dimension)
    self_inverse_characteristics = gcd(2, dimension) ** 2
    nontrivial_reciprocal_pairs = (
        dimension * dimension - self_inverse_characteristics
    ) // 2
    return {
        "dimension": dimension,
        "parity_formula": "P e_j = e_(-j)",
        "source_parity_hermiticity": "G^* = P G P",
        "hermitian_transform": "J = P G = J^*",
        "gram_reduction": "G^* G = J^2",
        "positive_certificate": (
            "Delta_2(G)=((Tr J^2)^2-Tr J^4)/2"
        ),
        "self_inverse_characteristic_count": (
            self_inverse_characteristics
        ),
        "nontrivial_reciprocal_pair_count": (
            nontrivial_reciprocal_pairs
        ),
        "reciprocity_frobenius_lower_bound": "Tr J^2 >= 1",
        "equality_condition_for_lower_bound": (
            "u(p)^2=1 for every characteristic p"
        ),
        "quadratic_lower_bound_forces_tcc": False,
        "constant_overlap_countermodel_attains_lower_bound": True,
        "constant_overlap_countermodel_saturates_fourth_moment": False,
        "adjoint_eliminated_on_parity_hermitian_locus": True,
        "fourth_moment_equivalent_to_tcc": True,
        "tcc_fourth_moment_target": "Tr J^4 = (Tr J^2)^2",
    }


def canonical_dimension_four_holomorphic_quartic_countermodel_record(
) -> dict[str, object]:
    r"""Return a parity-Hermitian countermodel to a lone holomorphic quartic.

    In a parity eigenbasis with signature ``(+,+,+,-)``, take

    ``G = diag(1, 1, B)``,
    ``B=[[-1/2,sqrt(3)/2],[-sqrt(3)/2,-1/2]]``.

    It is parity-Hermitian and has eigenvalues ``1,1,zeta_3,zeta_3^2``.
    Hence its first, second, and fourth power traces are all one, while
    it is invertible.  This shows why the Bos--Waldron holomorphic
    quartic cannot be moved from its unit-torus/Hermitian locus to the
    RM ghost using parity-Hermiticity and trace identities alone.
    """

    return {
        "dimension": 4,
        "parity_signature": (3, 1),
        "parity_eigenbasis_matrix": (
            ("1", "0", "0", "0"),
            ("0", "1", "0", "0"),
            ("0", "0", "-1/2", "sqrt(3)/2"),
            ("0", "0", "-sqrt(3)/2", "-1/2"),
        ),
        "characteristic_polynomial": "(x-1)(x^3-1)",
        "eigenvalues": ("1", "1", "zeta_3", "zeta_3^2"),
        "trace_power_1": 1,
        "trace_power_2": 1,
        "trace_power_3": 4,
        "trace_power_4": 1,
        "determinant": 1,
        "rank": 4,
        "parity_hermitian": True,
        "ordinary_hermitian": False,
        "bos_waldron_quartic_holds": True,
        "rank_one": False,
        "tcc_holds": False,
        "unit_torus_hypothesis_is_essential": True,
        "correct_rm_positive_quartic_holds": False,
    }


def _tower_basis(index: int, coefficient: Fraction | int = 1) -> TowerCoordinate:
    """Return one basis vector of Q(sqrt(2),sqrt(5),sqrt(3+sqrt(5)))."""

    return tuple(
        Fraction(coefficient if position == index else 0)
        for position in range(8)
    )  # type: ignore[return-value]


def _tower_add(*values: TowerCoordinate) -> TowerCoordinate:
    return tuple(
        sum((value[index] for value in values), Fraction(0))
        for index in range(8)
    )  # type: ignore[return-value]


def _tower_scale(
    scalar: Fraction | int, value: TowerCoordinate
) -> TowerCoordinate:
    factor = Fraction(scalar)
    return tuple(factor * entry for entry in value)  # type: ignore[return-value]


def _tower_multiply(
    left: TowerCoordinate, right: TowerCoordinate
) -> TowerCoordinate:
    r"""Multiply in the basis ``sqrt(2)^a sqrt(5)^b t^c``.

    Basis indices are ``a+2*b+4*c`` and ``t^2=3+sqrt(5)``.
    """

    result = [Fraction(0) for _ in range(8)]
    for left_index, left_value in enumerate(left):
        if not left_value:
            continue
        for right_index, right_value in enumerate(right):
            if not right_value:
                continue
            coefficient = left_value * right_value
            first_power = (left_index & 1) + (right_index & 1)
            fifth_power = (
                ((left_index >> 1) & 1)
                + ((right_index >> 1) & 1)
            )
            tower_power = (
                ((left_index >> 2) & 1)
                + ((right_index >> 2) & 1)
            )
            if first_power == 2:
                coefficient *= 2
                first_power = 0
            if fifth_power == 2:
                coefficient *= 5
                fifth_power = 0
            branches = [(coefficient, fifth_power)]
            if tower_power == 2:
                tower_power = 0
                branches = [
                    (3 * coefficient, fifth_power),
                    (coefficient, fifth_power + 1),
                ]
            for branch_coefficient, branch_fifth_power in branches:
                if branch_fifth_power == 2:
                    branch_coefficient *= 5
                    branch_fifth_power = 0
                index = (
                    first_power
                    + 2 * branch_fifth_power
                    + 4 * tower_power
                )
                result[index] += branch_coefficient
    return tuple(result)  # type: ignore[return-value]


def _tower_complex_add(*values: TowerComplex) -> TowerComplex:
    return (
        _tower_add(*(value[0] for value in values)),
        _tower_add(*(value[1] for value in values)),
    )


def _tower_complex_scale(
    scalar: TowerComplex, value: TowerComplex
) -> TowerComplex:
    return (
        _tower_add(
            _tower_multiply(scalar[0], value[0]),
            _tower_scale(-1, _tower_multiply(scalar[1], value[1])),
        ),
        _tower_add(
            _tower_multiply(scalar[0], value[1]),
            _tower_multiply(scalar[1], value[0]),
        ),
    )


def canonical_dimension_four_double_sine_factor_record(
) -> dict[str, object]:
    r"""Factor every dimension-four ghost minor through one RM unit law.

    The principal-ghost double-sine algorithm gives, up to its exceptional
    zero value, a signed table in ``{1,x,x^-1}``.  Put

    ``t=sqrt(3+sqrt(5))``.

    This routine computes all 36 two-by-two minors exactly in
    ``Q(sqrt(2),sqrt(5),t)[x,x^-1]`` and reduces them by

    ``x^2-t*x+1=0``.

    Every remainder is zero.  Thus the complete dimension-four TCC follows
    from the single still-analytic special-value identity ``x+x^-1=t``.
    """

    zero = _tower_basis(0, 0)
    one = _tower_basis(0)
    sqrt_two = _tower_basis(1)
    sqrt_five = _tower_basis(2)
    # The positive radical is already in Q(sqrt(2),sqrt(5)):
    # sqrt(3+sqrt(5))=(sqrt(2)+sqrt(10))/2.
    tower_t = _tower_add(
        _tower_scale(Fraction(1, 2), sqrt_two),
        _tower_scale(
            Fraction(1, 2),
            _tower_multiply(sqrt_two, sqrt_five),
        ),
    )
    complex_one: TowerComplex = (one, zero)
    complex_i: TowerComplex = (zero, one)
    tau: TowerComplex = (
        _tower_scale(Fraction(-1, 2), sqrt_two),
        _tower_scale(Fraction(-1, 2), sqrt_two),
    )

    def complex_power(value: TowerComplex, exponent: int) -> TowerComplex:
        result = complex_one
        for _ in range(exponent):
            result = _tower_complex_scale(result, value)
        return result

    def polynomial_add(
        *polynomials: Mapping[int, TowerComplex],
    ) -> dict[int, TowerComplex]:
        result: dict[int, TowerComplex] = {}
        for polynomial in polynomials:
            for exponent, coefficient in polynomial.items():
                result[exponent] = _tower_complex_add(
                    result.get(exponent, (zero, zero)), coefficient
                )
        return {
            exponent: coefficient
            for exponent, coefficient in result.items()
            if coefficient != (zero, zero)
        }

    def polynomial_scale(
        scalar: TowerComplex, polynomial: Mapping[int, TowerComplex]
    ) -> dict[int, TowerComplex]:
        return {
            exponent: _tower_complex_scale(scalar, coefficient)
            for exponent, coefficient in polynomial.items()
        }

    def polynomial_multiply(
        left: Mapping[int, TowerComplex],
        right: Mapping[int, TowerComplex],
    ) -> dict[int, TowerComplex]:
        result: dict[int, TowerComplex] = {}
        for left_exponent, left_value in left.items():
            for right_exponent, right_value in right.items():
                exponent = left_exponent + right_exponent
                product = _tower_complex_scale(left_value, right_value)
                result[exponent] = _tower_complex_add(
                    result.get(exponent, (zero, zero)), product
                )
        return {
            exponent: coefficient
            for exponent, coefficient in result.items()
            if coefficient != (zero, zero)
        }

    # Entries are (sign coefficient, exponent of x).  This is the full
    # signed table produced by the symmetrized principal double sine.
    unit_table = (
        ((sqrt_five, 0), (_tower_scale(-1, one), 1), (one, 0), (_tower_scale(-1, one), -1)),
        ((_tower_scale(-1, one), -1), (_tower_scale(-1, one), -1), (_tower_scale(-1, one), -1), (_tower_scale(-1, one), 1)),
        ((one, 0), (_tower_scale(-1, one), -1), (one, 0), (one, 1)),
        ((_tower_scale(-1, one), 1), (_tower_scale(-1, one), -1), (one, 1), (_tower_scale(-1, one), 1)),
    )

    inverse_sqrt_five = _tower_scale(Fraction(1, 5), sqrt_five)
    matrix: list[list[dict[int, TowerComplex]]] = [
        [{} for _ in range(4)] for _ in range(4)
    ]
    for first in range(4):
        for second in range(4):
            unit_coefficient, exponent = unit_table[first][second]
            scalar = _tower_complex_scale(
                complex_power(tau, first * second),
                (inverse_sqrt_five, zero),
            )
            coefficient = _tower_complex_scale(
                scalar, (unit_coefficient, zero)
            )
            for column in range(4):
                row = (column + first) % 4
                phase = _tower_complex_scale(
                    complex_power(complex_i, second * column),
                    (_tower_scale(Fraction(1, 4), one), zero),
                )
                term = {exponent: _tower_complex_scale(phase, coefficient)}
                matrix[row][column] = polynomial_add(
                    matrix[row][column], term
                )

    # Reduce x^e to A_e+B_e*x under x^2=t*x-1.
    reductions: dict[int, tuple[TowerCoordinate, TowerCoordinate]] = {
        -2: (
            _tower_add(_tower_multiply(tower_t, tower_t), _tower_scale(-1, one)),
            _tower_scale(-1, tower_t),
        ),
        -1: (tower_t, _tower_scale(-1, one)),
        0: (one, zero),
        1: (zero, one),
        2: (_tower_scale(-1, one), tower_t),
    }

    nonzero_minor_count = 0
    nonzero_remainder_count = 0
    minor_certificates: list[dict[str, object]] = []

    def fraction_text(value: Fraction) -> str:
        if value.denominator == 1:
            return str(value.numerator)
        return f"{value.numerator}/{value.denominator}"

    def tower_text(value: TowerCoordinate) -> list[str]:
        # In this calculation t=sqrt(3+sqrt(5)) is explicitly replaced by
        # (sqrt(2)+sqrt(10))/2.  Hence every coefficient lies in the
        # biquadratic field Q(sqrt(2),sqrt(5)); the upper four coordinates
        # of the legacy tower representation must vanish.
        assert all(coefficient == 0 for coefficient in value[4:])
        return [fraction_text(coefficient) for coefficient in value[:4]]

    def complex_text(value: TowerComplex) -> dict[str, list[str]]:
        return {
            "real": tower_text(value[0]),
            "imaginary": tower_text(value[1]),
        }

    def polynomial_text(
        polynomial: Mapping[int, TowerComplex],
    ) -> dict[str, dict[str, list[str]]]:
        return {
            str(exponent): complex_text(coefficient)
            for exponent, coefficient in sorted(polynomial.items())
        }

    # Divide a Laurent polynomial by x^2-t*x+1 after multiplying by x^2.
    # All minors have exponents in [-2,2], so the quotient is an ordinary
    # polynomial of degree at most two.  The returned zero remainder is an
    # independently checkable exact divisibility certificate.
    def divide_shifted_minor(
        minor: Mapping[int, TowerComplex],
    ) -> tuple[dict[int, TowerComplex], dict[int, TowerComplex]]:
        dividend = {
            exponent + 2: coefficient
            for exponent, coefficient in minor.items()
        }
        quotient: dict[int, TowerComplex] = {}
        relation = {
            2: (one, zero),
            1: (_tower_scale(-1, tower_t), zero),
            0: (one, zero),
        }
        while dividend and max(dividend) >= 2:
            degree = max(dividend)
            coefficient = dividend[degree]
            quotient[degree - 2] = coefficient
            for relation_degree, relation_coefficient in relation.items():
                target = degree - 2 + relation_degree
                dividend[target] = _tower_complex_add(
                    dividend.get(target, (zero, zero)),
                    _tower_complex_scale(
                        (_tower_scale(-1, one), zero),
                        _tower_complex_scale(
                            coefficient, relation_coefficient
                        ),
                    ),
                )
                if dividend[target] == (zero, zero):
                    del dividend[target]
        return quotient, dividend

    for first_row, second_row in combinations(range(4), 2):
        for first_column, second_column in combinations(range(4), 2):
            positive = polynomial_multiply(
                matrix[first_row][first_column],
                matrix[second_row][second_column],
            )
            negative = polynomial_scale(
                (_tower_scale(-1, one), zero),
                polynomial_multiply(
                    matrix[first_row][second_column],
                    matrix[second_row][first_column],
                ),
            )
            minor = polynomial_add(positive, negative)
            if minor:
                nonzero_minor_count += 1
            remainder_constant: TowerComplex = (zero, zero)
            remainder_linear: TowerComplex = (zero, zero)
            for exponent, coefficient in minor.items():
                constant, linear = reductions[exponent]
                remainder_constant = _tower_complex_add(
                    remainder_constant,
                    _tower_complex_scale((constant, zero), coefficient),
                )
                remainder_linear = _tower_complex_add(
                    remainder_linear,
                    _tower_complex_scale((linear, zero), coefficient),
                )
            if remainder_constant != (zero, zero) or remainder_linear != (
                zero,
                zero,
            ):
                nonzero_remainder_count += 1
            quotient, division_remainder = divide_shifted_minor(minor)
            minor_certificates.append(
                {
                    "rows": [first_row, second_row],
                    "columns": [first_column, second_column],
                    "laurent_minor": polynomial_text(minor),
                    "quotient_after_multiplication_by_x_squared": (
                        polynomial_text(quotient)
                    ),
                    "division_remainder": polynomial_text(
                        division_remainder
                    ),
                }
            )

    return {
        "dimension": 4,
        "coefficient_basis": [
            "1",
            "sqrt(2)",
            "sqrt(5)",
            "sqrt(10)",
        ],
        "coefficient_encoding": (
            "Each coefficient is an exact vector in the displayed basis; "
            "complex coefficients have separate real and imaginary vectors."
        ),
        "matrix_definition": (
            "K[r,c]=(1/(4*sqrt(5))) sum_{a,b: r=c+a mod 4} "
            "T[a,b]*tau^(a*b)*i^(b*c), tau=-(1+i)/sqrt(2)"
        ),
        "normalization": (
            "The exceptional T[0,0]=sqrt(5) is divided by sqrt(5), "
            "so the zero Weyl overlap is a_0=1."
        ),
        "signed_double_sine_table": [
            ["sqrt(5)", "-x", "1", "-x^-1"],
            ["-x^-1", "-x^-1", "-x^-1", "-x"],
            ["1", "-x^-1", "1", "x"],
            ["-x", "-x^-1", "x", "-x"],
        ],
        "matrix_entries": [
            [polynomial_text(entry) for entry in row]
            for row in matrix
        ],
        "double_sine_unit_table_values": "{sqrt(5),1,x,x^-1} with signs",
        "unit_relation": "x^2-sqrt(3+sqrt(5))*x+1=0",
        "equivalent_reciprocal_relation": (
            "x+x^-1=sqrt(3+sqrt(5))"
        ),
        "all_minor_count": 36,
        "formally_nonzero_minor_count_before_relation": (
            nonzero_minor_count
        ),
        "nonzero_remainder_count_after_relation": (
            nonzero_remainder_count
        ),
        "every_minor_is_in_principal_ideal": (
            nonzero_remainder_count == 0
        ),
        "minor_certificates": minor_certificates,
        "certificate_identity": (
            "x^2*minor=(x^2-t*x+1)*quotient+division_remainder"
        ),
        "matrix_trace": "1",
        "nonzero_entry": (
            "K[0,0]=(sqrt(5)+1-x-x^-1)/(4*sqrt(5))"
        ),
        "nonzero_entry_positive_under_relation": True,
        "single_special_value_identity_implies_dimension_four_ghost_rank_one": True,
        "both_shifts_checked_by_minor_file_alone": False,
        "special_value_identity_proved_analytically": False,
    }


def canonical_zauner_block_multiplicities(
    dimension: int,
) -> tuple[int, int, int]:
    r"""Return the three canonical Zauner eigenspace dimensions.

    Only the multiset is canonical here, so the tuple is returned in
    nonincreasing order.
    """

    canonical_form(dimension)
    quotient, remainder = divmod(dimension, 3)
    if remainder == 0:
        return (quotient + 1, quotient, quotient - 1)
    if remainder == 1:
        return (quotient + 1, quotient, quotient)
    return (quotient + 1, quotient + 1, quotient)


def canonical_zak_zauner_block_record(
    dimension: int,
) -> dict[str, object]:
    r"""Audit whether Zauner block diagonalization reduces TCC.

    The sum of the squared block dimensions equals the number of
    Zauner characteristic orbits.  Thus the commutant has exactly as
    many scalar degrees of freedom as the already-known orbit
    reduction and supplies no additional equations.
    """

    multiplicities = canonical_zauner_block_multiplicities(dimension)
    commutant_dimension = sum(
        multiplicity * multiplicity
        for multiplicity in multiplicities
    )
    orbit_count = canonical_tcc_orbit_bound(dimension)
    return {
        "multiplicities": multiplicities,
        "commutant_dimension": commutant_dimension,
        "zauner_orbit_count": orbit_count,
        "dimension_defect": commutant_dimension - orbit_count,
        "block_diagonalization_reduces_equation_count": (
            commutant_dimension < orbit_count
        ),
    }


def _q_polynomial_add(
    left: tuple[int, ...],
    right: tuple[int, ...],
) -> tuple[int, ...]:
    """Add two integer polynomials represented by coefficient tuples."""

    length = max(len(left), len(right))
    coefficients = tuple(
        (left[index] if index < len(left) else 0)
        + (right[index] if index < len(right) else 0)
        for index in range(length)
    )
    while len(coefficients) > 1 and coefficients[-1] == 0:
        coefficients = coefficients[:-1]
    return coefficients


def _q_polynomial_shift(
    polynomial: tuple[int, ...],
    exponent: int,
    scalar: int = 1,
) -> tuple[int, ...]:
    """Multiply an integer polynomial by ``scalar*q^exponent``."""

    if exponent < 0:
        raise ValueError("exponent must be nonnegative")
    return (0,) * exponent + tuple(
        scalar * coefficient for coefficient in polynomial
    )


def _q_binomial_polynomial(
    degree: int,
    index: int,
) -> tuple[int, ...]:
    r"""Return the Gaussian polynomial ``[degree choose index]_q``."""

    if not 0 <= index <= degree:
        return (0,)
    rows: list[list[tuple[int, ...]]] = [[(1,)]]
    for current_degree in range(1, degree + 1):
        row: list[tuple[int, ...]] = []
        for current_index in range(current_degree + 1):
            if current_index == 0 or current_index == current_degree:
                row.append((1,))
                continue
            row.append(
                _q_polynomial_add(
                    rows[-1][current_index],
                    _q_polynomial_shift(
                        rows[-1][current_index - 1],
                        current_degree - current_index,
                    ),
                )
            )
        rows.append(row)
    return rows[degree][index]


def canonical_equal_base_q_binomial_cancellation(
    degree: int,
) -> tuple[int, ...]:
    r"""Return the equal-base root-filter cancellation polynomial.

    Multiplying the premature equal-base coefficient by ``(q;q)_N``
    gives

    ``sum_n (-1)^n q^(n(n-1)/2) [N choose n]_q``.

    The finite q-binomial theorem makes this ``(1;q)_N``, which is zero
    for ``N>0``.  This proves that setting the two radial bases equal
    before the RM boundary limit erases every nonconstant coefficient.
    """

    if degree < 0:
        raise ValueError("degree must be nonnegative")
    result = (0,)
    for index in range(degree + 1):
        result = _q_polynomial_add(
            result,
            _q_polynomial_shift(
                _q_binomial_polynomial(degree, index),
                index * (index - 1) // 2,
                -1 if index % 2 else 1,
            ),
        )
    return result


def canonical_root_filtered_stokes_record(
    dimension: int,
    numerator_index: int,
    denominator_index: int,
) -> dict[str, object]:
    r"""Return the exact acceptance gate for the filtered RM limit.

    If ``N=n+m``, root filtering retains

    ``1-q_tilde^n*q^m``.

    At the RM boundary its monomial is ``exp(2*pi*i*beta_d*N)``.
    Irrationality of ``beta_d`` means this is a root of unity only when
    ``N=0``.  Meanwhile, identifying the two radial bases before taking
    the limit gives the q-binomial cancellation recorded here.
    """

    canonical_form(dimension)
    if numerator_index < 0 or denominator_index < 0:
        raise ValueError("series indices must be nonnegative")
    total_index = numerator_index + denominator_index
    cancellation = canonical_equal_base_q_binomial_cancellation(
        total_index
    )
    return {
        "total_index": total_index,
        "filtered_difference_factor": "1 - q_tilde^n q^m",
        "beta_is_irrational": not canonical_beta_is_rational(dimension),
        "boundary_monomial_is_root_of_unity": total_index == 0,
        "equal_base_cancellation_polynomial": cancellation,
        "equal_base_coefficient_vanishes": (
            total_index > 0 and cancellation == (0,)
        ),
        "radial_speed_ratio": "beta^(-6)",
        "uniform_root_filtered_stokes_limit_proved": False,
    }


def canonical_dimension_four_ray_class_record() -> dict[str, object]:
    r"""Return the elementary 2-power ray-group audit for ``Q(sqrt(5))``.

    Write ``O_K = Z[phi]`` with ``phi^2=phi+1``.  Since 2 is inert,
    a residue ``a+b*phi`` modulo ``2^k`` is a unit exactly when its norm
    is odd.  Class number one gives the one-real-place ray-group order

    ``2 * |(O_K/m)^x| / |image(O_K^x)|``.

    Enumerating the finite groups shows that modulus 4 has order two.
    This matches the degree of the Stark candidate ``x^2`` over the
    base field.  The cocycle value ``x`` is a square root of that Stark
    invariant and has degree four.  Modulus 8 has a Vierergruppe, but
    its appearance as the general modular phase modulus does not make
    it the ray conductor.
    """

    def multiply(
        left: tuple[int, int],
        right: tuple[int, int],
        modulus: int,
    ) -> tuple[int, int]:
        a, b = left
        c, d = right
        return (
            (a * c + b * d) % modulus,
            (a * d + b * c + b * d) % modulus,
        )

    def norm(value: tuple[int, int]) -> int:
        a, b = value
        return a * a + a * b - b * b

    audits: dict[int, dict[str, object]] = {}
    for modulus in (4, 8):
        residues = [
            (a, b)
            for a in range(modulus)
            for b in range(modulus)
            if norm((a, b)) % 2
        ]
        phi_powers: list[tuple[int, int]] = []
        power = (1, 0)
        while True:
            power = multiply(power, (0, 1), modulus)
            phi_powers.append(power)
            if power == (1, 0):
                break
        unit_image = set(phi_powers)
        unit_image.update(
            ((-a) % modulus, (-b) % modulus)
            for a, b in phi_powers
        )

        signed_group = [
            (residue, sign)
            for residue in residues
            for sign in (-1, 1)
        ]
        signed_unit_image = set()
        power = (1, 0)
        for exponent in range(2 * len(phi_powers)):
            for minus in (False, True):
                residue = (
                    ((-power[0]) % modulus, (-power[1]) % modulus)
                    if minus
                    else power
                )
                signed_unit_image.add((residue, -1 if minus else 1))
            power = multiply(power, (0, 1), modulus)

        def signed_multiply(
            left: tuple[tuple[int, int], int],
            right: tuple[tuple[int, int], int],
        ) -> tuple[tuple[int, int], int]:
            return (
                multiply(left[0], right[0], modulus),
                left[1] * right[1],
            )

        remaining = set(signed_group)
        quotient_orders: list[int] = []
        while remaining:
            representative = min(remaining)
            coset = {
                signed_multiply(representative, unit)
                for unit in signed_unit_image
            }
            remaining.difference_update(coset)
            value = ((1, 0), 1)
            for order in range(1, 9):
                value = signed_multiply(value, representative)
                if value in signed_unit_image:
                    quotient_orders.append(order)
                    break

        audits[modulus] = {
            "residue_unit_count": len(residues),
            "phi_residue_order": len(phi_powers),
            "ordinary_unit_image_count": len(unit_image),
            "signed_unit_image_count": len(signed_unit_image),
            "one_real_place_ray_group_order": (
                len(signed_group) // len(signed_unit_image)
            ),
            "quotient_element_orders": tuple(sorted(quotient_orders)),
        }

    stabilizer = canonical_level_stabilizer(4)
    characteristic = (Fraction(0), Fraction(1, 4))
    acted_characteristic = (
        stabilizer[0][0] * characteristic[0]
        + stabilizer[0][1] * characteristic[1],
        stabilizer[1][0] * characteristic[0]
        + stabilizer[1][1] * characteristic[1],
    )
    characteristic_difference = tuple(
        int(acted_characteristic[index] - characteristic[index])
        for index in range(2)
    )

    def sawtooth(value: Fraction) -> Fraction:
        if value.denominator == 1:
            return Fraction(0)
        return value - (value.numerator // value.denominator) - Fraction(
            1, 2
        )

    rademacher_dedekind_sum = sum(
        (
            sawtooth(Fraction(index, 8))
            * sawtooth(Fraction(21 * index, 8))
            for index in range(1, 8)
        ),
        Fraction(0),
    )
    rademacher_invariant = (
        Fraction(stabilizer[0][0] + stabilizer[1][1], stabilizer[1][0])
        - 3
        - 12 * rademacher_dedekind_sum
    )
    assert stabilizer == ((21, -8), (8, -3))
    assert characteristic_difference == (-2, -1)
    assert rademacher_dedekind_sum == Fraction(-1, 16)
    assert rademacher_invariant == 0

    return {
        "base_field": "Q(sqrt(5))",
        "class_number": 1,
        "quarter_argument_denominator": 4,
        "general_modular_modulus": 8,
        "modulus_audits": audits,
        "modulus_four_matches_stark_square_degree": (
            audits[4]["one_real_place_ray_group_order"] == 2
        ),
        "modulus_eight_phase_cover_group": "C2 x C2",
        "candidate_cocycle_polynomial_over_base": (
            "X^4 - (1 + sqrt(5)) X^2 + 1"
        ),
        "candidate_stark_square_polynomial_over_base": (
            "U^2 - (1 + sqrt(5)) U + 1"
        ),
        "golden_ratio_form": "x^2 = phi + sqrt(phi)",
        "candidate_ray_field": "Q(sqrt(5), sqrt(phi))",
        "candidate_relative_discriminant": "(4)",
        "candidate_absolute_discriminant": 400,
        "minkowski_bound": "15 / (2 pi)",
        "minkowski_bound_below_three": True,
        "smallest_dyadic_prime_norm": 4,
        "candidate_class_number": 1,
        "candidate_infinite_ramification": "second real place",
        "ray_field_degree_matches_ray_group": True,
        "visible_units": ("sqrt(phi)", "phi + sqrt(phi)"),
        "visible_regulator": "log(phi) log(phi + sqrt(phi))",
        "relative_l_derivative": (
            "log(phi + sqrt(phi))"
        ),
        "fundamental_units_verified_by_pari_bnf": True,
        "pari_bnfcertify_required": True,
        "two_infinite_place_ray_group_order": 4,
        "one_infinite_place_fiber_order": 2,
        "kopp_exponent_n": 1,
        "kopp_modulus": "(4) infinity_2",
        "kopp_labeled_embeddings": (
            "infinity_1(sqrt(5))=+sqrt(5)",
            "infinity_2(sqrt(5))=-sqrt(5)",
        ),
        "kopp_ray_class": "identity",
        "kopp_auxiliary_ideal": "O_K",
        "kopp_alpha": 4,
        "kopp_characteristic": ("0", "1/4"),
        "kopp_positive_stabilizer": stabilizer,
        "kopp_stabilizer_eigenvalue": "beta^3",
        "kopp_characteristic_difference": characteristic_difference,
        "rademacher_dedekind_sum": "-1/16",
        "rademacher_invariant": 0,
        "kopp_multiplier": "-i",
        "kopp_eta_character_square": "1",
        "kopp_theta_character": "i",
        "kopp_theta_character_defining_exponent": "5/4",
        "kopp_phase": "exp(3*pi*i/4)",
        "partial_zeta_normalization": (
            "Z(s,id)=zeta(s,id)-zeta(s,R)=L(s,chi)"
        ),
        "partial_zeta_normalization_matched": True,
        "kopp_specialization_proved": True,
        "shift_one_twist": "I",
        "shift_zero_twist": "diag(1,-1)",
        "shift_pairing": "lambda_bar=1-lambda mod 4",
        "both_formal_tcc_shifts_proved": True,
        "candidate_polynomial_over_rationals": (
            "X^8 - 2 X^6 - 2 X^4 - 2 X^2 + 1"
        ),
        "ray_class_identification_proved": True,
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
        "pentagon_compatibility": (
            canonical_pentagon_compatibility_record(dimension)
        ),
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
        "zak_reflection_quadratic": (
            canonical_zak_reflection_quadratic_record(dimension)
        ),
        "reciprocal_trace_moments": (
            canonical_reciprocal_trace_moment_record(dimension)
        ),
        "ghost_rank_one_minor": canonical_ghost_minor_record(
            dimension, (0, 1), (0, 1)
        ),
        "ghost_exterior_square": (
            canonical_ghost_exterior_square_record(dimension)
        ),
        "parity_schatten": canonical_parity_schatten_record(dimension),
        "holomorphic_quartic_gate_dimension_four": (
            canonical_dimension_four_holomorphic_quartic_countermodel_record()
        ),
        "dimension_four_double_sine_factor": (
            canonical_dimension_four_double_sine_factor_record()
        ),
        "dimension_four_ray_class": (
            canonical_dimension_four_ray_class_record()
        ),
        "zak_zauner_blocks": canonical_zak_zauner_block_record(
            dimension
        ),
        "cyclic_approximant": canonical_cyclic_approximant_record(
            dimension, 1, 1
        ),
        "jacobi_word": canonical_jacobi_word(dimension),
        "jacobi_scale_exponents": canonical_jacobi_scale_exponents(),
        "quadratic_identity_residual": canonical_quadratic_identity(
            dimension
        ),
        "cube_mod_dimension": matrix_mod(
            matrix_power(stabilizer, 3), dimension
        ),
    }
