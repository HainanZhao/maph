#!/usr/bin/env python3
"""Uniform rational-boundary audit for the d=6 characteristic cocycle.

Kopp's generic cyclic-dilogarithm formula excludes characteristics for
which a cyclic factor vanishes.  Factoring a q-Pochhammer product into
residue classes replaces the singular residue by the q-gamma asymptotic

    (Q^alpha; Q)_inf
      ~ sqrt(2*pi) / Gamma(alpha)
        * (1-Q)^(1/2-alpha)
        * exp(pi^2 / (6*log(Q))).

For the canonical d=6 stabilizer, the numerator and denominator have the
same alpha for every singular nonzero characteristic.  Their boundary
orders and Gamma factors therefore cancel.

The script also includes the constant phase caused by the quadratic term
in the Mobius transformation of the radial parameter.  It builds the
regularized rational-boundary table, applies the AFK phase, reconstructs
the Weyl matrix, and records convergence toward twisted convolution.

This is an asymptotic/numerical audit, not a finite-level TCC proof.
"""

from __future__ import annotations

import cmath
from fractions import Fraction
import math

import mpmath
import numpy


DIMENSION = 6
TRACE_BETA = 5
L_MATRIX = ((5, -1), (1, 0))
L_INVERSE_MOD_SIX = ((0, 1), (-1, 5))
A_MATRIX = ((115, -24), (24, -5))


def trace_sequence(stop: int) -> list[int]:
    values = [2, TRACE_BETA]
    while len(values) <= stop:
        values.append(TRACE_BETA * values[-1] - values[-2])
    return values


TRACES = trace_sequence(12)


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
    return (
        numerator,
        denominator,
        mapped_numerator,
        mapped_denominator,
    )


def singular_data(
    numerator: int,
    denominator: int,
    first: int,
    second: int,
) -> tuple[int, Fraction] | None:
    """Return the singular residue and q-gamma parameter alpha."""

    residue_numerator = first * denominator - second * numerator
    if residue_numerator % DIMENSION:
        return None
    singular_residue = (
        (residue_numerator // DIMENSION)
        * pow(numerator, -1, denominator)
    ) % denominator
    alpha = Fraction(
        second + DIMENSION * singular_residue,
        DIMENSION * denominator,
    )
    return singular_residue, alpha


def transformed_characteristic(
    characteristic: tuple[int, int],
) -> tuple[int, int]:
    first, second = characteristic
    return (
        (
            L_INVERSE_MOD_SIX[0][0] * first
            + L_INVERSE_MOD_SIX[0][1] * second
        )
        % DIMENSION,
        (
            L_INVERSE_MOD_SIX[1][0] * first
            + L_INVERSE_MOD_SIX[1][1] * second
        )
        % DIMENSION,
    )


def exact_boundary_audit() -> list[dict[tuple[int, int], Fraction]]:
    patterns: list[dict[tuple[int, int], Fraction]] = []
    for base_index in range(1, 10):
        numerator, denominator, mapped_numerator, mapped_denominator = (
            mapped_rational(base_index)
        )
        pattern: dict[tuple[int, int], Fraction] = {}
        for first in range(DIMENSION):
            for second in range(DIMENSION):
                source = singular_data(
                    numerator, denominator, first, second
                )
                target = singular_data(
                    mapped_numerator,
                    mapped_denominator,
                    first,
                    second,
                )
                assert (source is None) == (target is None)
                if source is None:
                    continue
                assert target is not None
                assert source[1] == target[1]
                if (first, second) != (0, 0):
                    pattern[(first, second)] = source[1]
        assert len(pattern) == 5
        assert set(pattern.values()) == {
            Fraction(1, 6),
            Fraction(1, 3),
            Fraction(1, 2),
            Fraction(2, 3),
            Fraction(5, 6),
        }
        patterns.append(pattern)

    for index in range(3, len(patterns)):
        assert patterns[index] == patterns[index - 3]
    for index in range(len(patterns) - 1):
        transported = {
            transformed_characteristic(characteristic): alpha
            for characteristic, alpha in patterns[index].items()
        }
        assert transported == patterns[index + 1]
    return patterns


def regularized_log_constant(
    numerator: int,
    denominator: int,
    first: int,
    second: int,
) -> complex:
    """Return the t-independent radial asymptotic of one Pochhammer.

    The common essential exponential is omitted.  It cancels in the
    modular cocycle ratio.
    """

    singular = singular_data(
        numerator, denominator, first, second
    )
    root_w = cmath.exp(
        2j
        * math.pi
        * (second * numerator / denominator - first)
        / DIMENSION
    )
    root_q = cmath.exp(2j * math.pi * numerator / denominator)

    if singular is None:
        log_cyclic_dilogarithm = 0j
        root = root_q * root_w
        for index in range(1, denominator):
            log_cyclic_dilogarithm += index * cmath.log(1 - root)
            root *= root_q
        return -log_cyclic_dilogarithm / denominator

    singular_residue, alpha = singular
    if alpha == 0:
        raise ValueError("zero characteristic is treated exceptionally")
    boundary_power = Fraction(1, 2) - alpha
    result = (
        0.5 * math.log(2 * math.pi)
        - math.lgamma(float(alpha))
        - float(boundary_power) * math.log(denominator)
    )
    root = root_w
    for index in range(denominator):
        if index != singular_residue:
            residue_alpha = (
                Fraction(second, DIMENSION) + index
            ) / denominator
            result += float(
                Fraction(1, 2) - residue_alpha
            ) * cmath.log(1 - root)
        root *= root_q
    return complex(result)


def boundary_shin(
    base_index: int,
    first: int,
    second: int,
) -> complex:
    """Return the regularized rational-boundary modular cocycle."""

    numerator, denominator, mapped_numerator, mapped_denominator = (
        mapped_rational(base_index)
    )
    source = regularized_log_constant(
        numerator, denominator, first, second
    )
    target = regularized_log_constant(
        mapped_numerator,
        mapped_denominator,
        first,
        second,
    )

    # If tau=m/n+i*t/(2*pi*n^2), then
    #
    #   A.tau = m'/n' + i*(t+kappa*t^2+O(t^3))/(2*pi*n'^2),
    #   kappa = -i*c/(2*pi*n*n').
    #
    # The common essential exponential therefore leaves this constant.
    root_power = (second * numerator - first * denominator) % DIMENSION
    common_root = cmath.exp(
        2j * math.pi * root_power / DIMENSION
    )
    curvature = (
        -1j
        * A_MATRIX[1][0]
        / (2 * math.pi * denominator * mapped_denominator)
    )
    curvature_correction = curvature * complex(
        mpmath.polylog(2, common_root)
    )
    return cmath.exp(target - source + curvature_correction)


def small_denominator_boundary_shin(
    first: int,
    second: int,
) -> complex:
    """Return the corrected boundary value at 1/4 -> 19/4."""

    numerator, denominator = 1, 4
    mapped_numerator, mapped_denominator = 19, 4
    source = regularized_log_constant(
        numerator, denominator, first, second
    )
    target = regularized_log_constant(
        mapped_numerator,
        mapped_denominator,
        first,
        second,
    )
    common_root = cmath.exp(
        2j
        * math.pi
        * ((second * numerator - first * denominator) % DIMENSION)
        / DIMENSION
    )
    correction = (
        -1j
        * A_MATRIX[1][0]
        / (
            2
            * math.pi
            * denominator
            * mapped_denominator
        )
        * complex(mpmath.polylog(2, common_root))
    )
    return cmath.exp(target - source + correction)


def direct_small_denominator_shin(
    radial_parameter: float,
    first: int,
    second: int,
) -> complex:
    """Evaluate the defining Pochhammer ratio near 1/4."""

    old_precision = mpmath.mp.dps
    mpmath.mp.dps = 35
    try:
        tau = (
            mpmath.mpf(1) / 4
            + 1j
            * mpmath.mpf(radial_parameter)
            / (2 * mpmath.pi * 16)
        )
        transformed_tau = (
            A_MATRIX[0][0] * tau + A_MATRIX[0][1]
        ) / (
            A_MATRIX[1][0] * tau + A_MATRIX[1][1]
        )
        characteristic_first = mpmath.mpf(first) / DIMENSION
        characteristic_second = mpmath.mpf(second) / DIMENSION
        source_argument = mpmath.exp(
            2j
            * mpmath.pi
            * (
                characteristic_second * tau
                - characteristic_first
            )
        )
        target_argument = mpmath.exp(
            2j
            * mpmath.pi
            * (
                characteristic_second * transformed_tau
                - characteristic_first
            )
        )
        source_q = mpmath.exp(2j * mpmath.pi * tau)
        target_q = mpmath.exp(
            2j * mpmath.pi * transformed_tau
        )
        return complex(
            mpmath.qp(
                target_argument,
                target_q,
                maxterms=1_000_000,
            )
            / mpmath.qp(
                source_argument,
                source_q,
                maxterms=1_000_000,
            )
        )
    finally:
        mpmath.mp.dps = old_precision


def direct_boundary_validation() -> dict[tuple[int, int], list[float]]:
    """Check a singular and nonsingular value against the product."""

    results: dict[tuple[int, int], list[float]] = {}
    for characteristic in ((2, 2), (0, 1)):
        boundary = small_denominator_boundary_shin(*characteristic)
        errors = [
            abs(
                direct_small_denominator_shin(
                    radial_parameter, *characteristic
                )
                / boundary
                - 1
            )
            for radial_parameter in (0.4, 0.2, 0.1)
        ]
        assert all(
            later < earlier
            for earlier, later in zip(errors, errors[1:])
        )
        assert errors[-1] < 0.008
        results[characteristic] = errors
    return results


def sawtooth(value: Fraction) -> Fraction:
    if value.denominator == 1:
        return Fraction(0)
    return (
        value
        - value.numerator // value.denominator
        - Fraction(1, 2)
    )


def dedekind_sum(first: int, second: int) -> Fraction:
    return sum(
        (
            sawtooth(Fraction(index, second))
            * sawtooth(Fraction(index * first, second))
            for index in range(1, abs(second))
        ),
        start=Fraction(0),
    )


def rademacher_invariant() -> int:
    first, _, lower_left, lower_right = (
        A_MATRIX[0][0],
        A_MATRIX[0][1],
        A_MATRIX[1][0],
        A_MATRIX[1][1],
    )
    value = (
        Fraction(first + lower_right, lower_left)
        - 3
        - 12 * dedekind_sum(first, lower_left)
    )
    assert value.denominator == 1
    return value.numerator


RADEMACHER = rademacher_invariant()
assert RADEMACHER == 6


def afk_phase(first: int, second: int) -> complex:
    parity_exponent = (
        DIMENSION
        + (1 + DIMENSION) * (1 + first) * (1 + second)
    )
    form_value = (
        first * first - 5 * first * second + second * second
    )
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    return (
        (-1) ** parity_exponent
        * cmath.exp(-math.pi * 1j * RADEMACHER / 12)
        * tau ** (-form_value)
    )


def boundary_table(base_index: int) -> list[list[complex]]:
    return [
        [
            (
                math.sqrt(DIMENSION + 1)
                if first == second == 0
                else afk_phase(first, second)
                * boundary_shin(base_index, first, second)
            )
            for second in range(DIMENSION)
        ]
        for first in range(DIMENSION)
    ]


def reconstruct(table: list[list[complex]]) -> numpy.ndarray:
    tau = -cmath.exp(math.pi * 1j / DIMENSION)
    omega = cmath.exp(2 * math.pi * 1j / DIMENSION)
    matrix = numpy.zeros((DIMENSION, DIMENSION), dtype=complex)
    for first in range(DIMENSION):
        for second in range(DIMENSION):
            for column in range(DIMENSION):
                row = (column + first) % DIMENSION
                matrix[row, column] += (
                    table[first][second]
                    * tau ** (first * second)
                    * omega ** (second * column)
                    / (DIMENSION * math.sqrt(DIMENSION + 1))
                )
    return matrix


def maximum_minor(matrix: numpy.ndarray) -> float:
    result = 0.0
    for first_row in range(DIMENSION):
        for second_row in range(first_row + 1, DIMENSION):
            for first_column in range(DIMENSION):
                for second_column in range(first_column + 1, DIMENSION):
                    minor = (
                        matrix[first_row, first_column]
                        * matrix[second_row, second_column]
                        - matrix[first_row, second_column]
                        * matrix[second_row, first_column]
                    )
                    result = max(result, abs(minor))
    return result


def primitive_polynomial(value: float) -> float:
    coefficients = [
        1,
        3,
        -6,
        -16,
        3,
        0,
        27,
        0,
        3,
        -16,
        -6,
        3,
        1,
    ]
    result = 0.0
    for coefficient in coefficients:
        result = result * value + coefficient
    return result


def positive_primitive_root() -> float:
    left, right = 2.212, 2.213
    left_value = primitive_polynomial(left)
    for _ in range(80):
        middle = (left + right) / 2
        middle_value = primitive_polynomial(middle)
        if left_value * middle_value <= 0:
            right = middle
        else:
            left, left_value = middle, middle_value
    return (left + right) / 2


def main() -> None:
    patterns = exact_boundary_audit()
    direct_errors = direct_boundary_validation()
    print("RADEMACHER_INVARIANT=", RADEMACHER, sep="")
    print("NONZERO_SINGULAR_COUNT_PER_STEP=5")
    print(
        "QGAMMA_PARAMETER_SET="
        "[1/6,1/3,1/2,2/3,5/6]"
    )
    print("ALL_SINGULAR_QGAMMA_PARAMETERS_MATCH=1")
    print("ALL_NONZERO_BOUNDARY_ORDERS_ZERO=1")
    print("SINGULAR_PATTERN_PERIOD=3")
    print("QGAMMA_PATTERN_ZAUNER_COVARIANT=1")
    for index, pattern in enumerate(patterns[:3], start=1):
        entries = ",".join(
            f"({first},{second}):{alpha}"
            for (first, second), alpha in sorted(pattern.items())
        )
        print(f"SINGULAR_PATTERN_{index}={entries}")
    for characteristic, errors in direct_errors.items():
        label = (
            "SINGULAR" if characteristic == (2, 2)
            else "NONSINGULAR"
        )
        print(
            f"DIRECT_{label}_PRODUCT_ERRORS="
            + ",".join(f"{error:.15e}" for error in errors)
        )
    print("DIRECT_PRODUCT_ERRORS_DECREASE=1")

    primitive_root = positive_primitive_root()
    idempotency_residuals = []
    minor_residuals = []
    imaginary_residuals = []
    final_principal = 0j
    for base_index in range(1, 5):
        table = boundary_table(base_index)
        matrix = reconstruct(table)
        idempotency = float(
            numpy.max(numpy.abs(matrix @ matrix - matrix))
        )
        minor = maximum_minor(matrix)
        maximum_imaginary = max(
            abs(value.imag)
            for row in table
            for value in row
        )
        idempotency_residuals.append(idempotency)
        minor_residuals.append(minor)
        imaginary_residuals.append(maximum_imaginary)
        principal = table[0][1]
        final_principal = principal
        _, denominator, _, _ = mapped_rational(base_index)
        print(
            f"BOUNDARY_STEP_{base_index}="
            f"denominator:{denominator},"
            f"principal_real:{principal.real:.15e},"
            f"principal_imag:{principal.imag:.15e},"
            f"idempotency:{idempotency:.15e},"
            f"maximum_minor:{minor:.15e},"
            f"maximum_table_imaginary:{maximum_imaginary:.15e}"
        )

    assert all(
        later < earlier
        for earlier, later in zip(
            idempotency_residuals, idempotency_residuals[1:]
        )
    )
    assert all(
        later < earlier
        for earlier, later in zip(
            minor_residuals, minor_residuals[1:]
        )
    )
    assert all(
        later < earlier
        for earlier, later in zip(
            imaginary_residuals, imaginary_residuals[1:]
        )
    )
    assert abs(final_principal.real + primitive_root) < 5e-4
    assert abs(final_principal.imag) < 5e-4
    assert idempotency_residuals[-1] < 5e-4
    assert minor_residuals[-1] < 5e-4
    print(f"ALGEBRAIC_PRIMITIVE_ROOT={primitive_root:.15e}")
    print("BOUNDARY_TABLE_IMAGINARY_PARTS_DECREASE=1")
    print("BOUNDARY_IDEMPOTENCY_RESIDUALS_DECREASE=1")
    print("BOUNDARY_MINOR_RESIDUALS_DECREASE=1")
    print("REGULARIZED_BOUNDARY_APPROACHES_ALGEBRAIC_PACKET=1")
    print("FINITE_LEVEL_TCC_IDENTITY_PROVED=0")


if __name__ == "__main__":
    main()
