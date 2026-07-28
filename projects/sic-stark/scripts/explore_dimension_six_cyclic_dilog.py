#!/usr/bin/env python3
"""Test the cyclic-quantum-dilogarithm route for the d=6 identity class.

Yalkinoglu's 2025 announcement writes the Shintani factor for a rational
principal modulus (u) as

    X_1((u)) = lim_n |D_{t_n}(1/u) / D_{t_{n+g}}(1/u)|,

where t_n=T_{n-1}(a)/T_n(a), T_(n+1)=a*T_n-T_(n-1), and g is the
order of the totally positive unit modulo (u).  Here a=5, u=6, g=3.

The logarithm of the cyclic dilogarithm is evaluated without choosing
fractional-power branches:

    log |D_(m/n)(x)| =
        sum_(k=1)^(n-1) (k/n) log |1-exp(2*pi*i*(k+x)*m/n)|.

The limiting factor is the reciprocal of the positive primitive overlap
x=2.212885... .  This is valid scalar, absolute-value evidence for the
identity ray class.  It neither retains the oriented order-six character
component nor supplies rational values for the full characteristic table.

The final audit deliberately makes the *formal* substitution of Kopp's
rational Jacobi formula into the modular-to-Jacobi characteristic
relation.  Kopp explicitly excludes the resulting zero cyclic factors
and defers characteristic evaluation.  Fractional formal boundary
exponents certify that this substitution cannot define meromorphic
orders and must not be used as a finite TCC table.
"""

from __future__ import annotations

from fractions import Fraction
import math

import numpy


TRACE_BETA = 5
MODULUS = 6
UNIT_ORDER_MODULUS = 3
A_MATRIX = ((115, -24), (24, -5))
A_INVERSE = ((-5, 24), (-24, 115))

# Absolute polynomial of the positive primitive overlap x.
PRIMITIVE_POLYNOMIAL = [
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


def trace_sequence(stop: int) -> list[int]:
    """Return T_0,...,T_stop with T_0=2, T_1=5."""

    values = [2, TRACE_BETA]
    while len(values) <= stop:
        values.append(TRACE_BETA * values[-1] - values[-2])
    return values


def log_cyclic_dilog(numerator: int, denominator: int) -> float:
    """Return log|D_(numerator/denominator)(1/6)|."""

    assert math.gcd(numerator, denominator) == 1
    full_denominator = MODULUS * denominator
    terms = []
    for index in range(1, denominator):
        residue = (
            MODULUS * index * numerator + numerator
        ) % full_denominator
        if residue == 0:
            raise ArithmeticError("unexpected zero cyclic factor")
        factor = 2 * abs(math.sin(math.pi * residue / full_denominator))
        terms.append((index / denominator) * math.log(factor))
    return math.fsum(terms)


def characteristic_cocycle_terms(
    first: int,
    second: int,
    parameter: Fraction,
) -> list[tuple[Fraction, Fraction]]:
    """Return the formal (angle, exponent) pairs.

    These pairs come from substituting a characteristic into the cyclic
    formula beyond its stated domain.  They are used solely to expose the
    resulting fractional-exponent contradiction.
    """

    root_numerator = parameter.numerator
    root_denominator = parameter.denominator
    a, b = first, second
    inverse_first = A_INVERSE[0][0] * a + A_INVERSE[0][1] * b
    inverse_second = A_INVERSE[1][0] * a + A_INVERSE[1][1] * b
    argument = Fraction(
        inverse_second * root_numerator
        - inverse_first * root_denominator,
        MODULUS * root_denominator,
    )

    matrix_a, matrix_b = A_MATRIX[0]
    matrix_c, matrix_d = A_MATRIX[1]
    transformed_numerator = (
        matrix_a * root_numerator + matrix_b * root_denominator
    )
    transformed_denominator = (
        matrix_c * root_numerator + matrix_d * root_denominator
    )
    transformed_argument = (
        root_denominator * argument / transformed_denominator
    )

    terms: list[tuple[Fraction, Fraction]] = []
    finite_length = 4 * a - 19 * b
    if finite_length >= 0:
        finite_indices = range(finite_length)
        finite_sign = 1
    else:
        finite_indices = range(finite_length, 0)
        finite_sign = -1
    for index in finite_indices:
        terms.append(
            (
                argument
                + Fraction(index * root_numerator, root_denominator),
                Fraction(finite_sign),
            )
        )
    for index in range(1, root_denominator):
        terms.append(
            (
                argument
                + Fraction(index * root_numerator, root_denominator),
                Fraction(index, root_denominator),
            )
        )
    for index in range(1, transformed_denominator):
        terms.append(
            (
                transformed_argument
                + Fraction(
                    index * transformed_numerator,
                    transformed_denominator,
                ),
                Fraction(-index, transformed_denominator),
            )
        )
    return terms


def formal_characteristic_boundary_exponent(
    first: int,
    second: int,
    parameter: Fraction,
) -> Fraction:
    """Return the exponent from the excluded formal substitution.

    A genuine order of a meromorphic function is integral.  Nonintegral
    outputs therefore diagnose missing branch-locus asymptotics; they are
    not valuations of the characteristic modular cocycle.
    """

    return sum(
        (
            coefficient
            for angle, coefficient in characteristic_cocycle_terms(
                first,
                second,
                parameter,
            )
            if angle.denominator == 1
        ),
        start=Fraction(0),
    )


def positive_overlap_root() -> float:
    roots = numpy.roots(PRIMITIVE_POLYNOMIAL)
    candidates = sorted(
        root.real
        for root in roots
        if abs(root.imag) < 1e-7 and 2.2 < root.real < 2.3
    )
    assert len(candidates) == 1
    return candidates[0]


def formal_tropical_convolution_audit(
    parameter: Fraction,
) -> tuple[dict[int, int], list[tuple[tuple[int, int], Fraction, tuple[int, int]]]]:
    """Audit the invalid formal exponents.

    This is retained only to reproduce why the earlier tropical proposal
    looked plausible.  It has no TCC meaning once any exponent is
    fractional.
    """

    orders = {
        (first, second): formal_characteristic_boundary_exponent(
            first,
            second,
            parameter,
        )
        for first in range(MODULUS)
        for second in range(MODULUS)
    }
    histogram: dict[int, int] = {}
    unique_nonzero_shifts = []
    for shift_first in range(MODULUS):
        for shift_second in range(MODULUS):
            valuations = [
                (
                    orders[(first, second)]
                    + orders[
                        (
                            (first - shift_first) % MODULUS,
                            (second - shift_second) % MODULUS,
                        )
                    ],
                    (first, second),
                )
                for first in range(MODULUS)
                for second in range(MODULUS)
            ]
            minimum = min(value for value, _ in valuations)
            minimizers = [
                characteristic
                for value, characteristic in valuations
                if value == minimum
            ]
            histogram[len(minimizers)] = (
                histogram.get(len(minimizers), 0) + 1
            )
            if (
                (shift_first, shift_second) != (0, 0)
                and len(minimizers) == 1
            ):
                unique_nonzero_shifts.append(
                    (
                        (shift_first, shift_second),
                        minimum,
                        minimizers[0],
                    )
                )
    return histogram, unique_nonzero_shifts


def main() -> None:
    maximum_index = 6
    traces = trace_sequence(maximum_index + UNIT_ORDER_MODULUS)
    overlap = positive_overlap_root()
    target = 1 / overlap

    print("schema=sic-stark-dimension-six-cyclic-dilog-v1")
    print(f"trace_parameter={TRACE_BETA}")
    print(f"modulus={MODULUS}")
    print(f"unit_order_modulus={UNIT_ORDER_MODULUS}")
    print(f"algebraic_overlap={overlap:.15f}")
    print(f"target_reciprocal={target:.15f}")
    print("n denominator_n denominator_n_plus_3 approximation error")

    errors = []
    for index in range(1, maximum_index + 1):
        numerator = traces[index - 1]
        denominator = traces[index]
        shifted_numerator = traces[
            index + UNIT_ORDER_MODULUS - 1
        ]
        shifted_denominator = traces[index + UNIT_ORDER_MODULUS]

        # For L=[[5,-1],[1,0]] and A=L^3, the rational modular
        # geodesic is transported exactly by A*t_(n+3)=t_n.
        shifted_parameter = Fraction(
            shifted_numerator, shifted_denominator
        )
        transported = shifted_parameter
        for _ in range(UNIT_ORDER_MODULUS):
            transported = (
                TRACE_BETA * transported - 1
            ) / transported
        assert transported == Fraction(numerator, denominator)

        approximation_log = (
            log_cyclic_dilog(numerator, denominator)
            - log_cyclic_dilog(shifted_numerator, shifted_denominator)
        )
        approximation = math.exp(approximation_log)
        error = abs(approximation - target)
        errors.append(error)
        print(
            f"{index} {denominator} {shifted_denominator} "
            f"{approximation:.15f} {error:.3e}"
        )

    assert errors[-1] < 1e-8
    print("excluded_characteristic_substitution_audit")
    nonintegral_exponent_seen = False
    for index in range(1, 5):
        parameter = Fraction(
            traces[index + UNIT_ORDER_MODULUS - 1],
            traces[index + UNIT_ORDER_MODULUS],
        )
        singular = []
        for first in range(MODULUS):
            for second in range(MODULUS):
                if first == second == 0:
                    continue
                order = formal_characteristic_boundary_exponent(
                    first,
                    second,
                    parameter,
                )
                if order:
                    if order.denominator != 1:
                        nonintegral_exponent_seen = True
                    singular.append(
                        f"({first},{second}):{order}"
                    )
        histogram, unique_shifts = formal_tropical_convolution_audit(
            parameter
        )
        print(
            f"{index} parameter={parameter} "
            f"singular_characteristics={len(singular)} "
            f"orders={','.join(singular)} "
            f"minimum_multiplicities={histogram} "
            f"unique_nonzero_shifts={unique_shifts}"
        )
    assert nonintegral_exponent_seen
    print(
        "conclusion=the scalar absolute-value approximants converge to "
        "the reciprocal identity-class d=6 overlap"
    )
    print(
        "proof_status=the scalar approximation is valid evidence, but "
        "the formal characteristic extension is invalid: fractional "
        "orders contradict meromorphicity, exactly in the case Kopp "
        "defers because cyclic factors vanish"
    )


if __name__ == "__main__":
    main()
