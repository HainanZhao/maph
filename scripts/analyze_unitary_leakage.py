#!/usr/bin/env python3
"""Exact leakage fingerprints for selected dark F_4 transitions.

The perturbations are unitary two-mode rotations appended after F_4:

    U_X(epsilon) = exp(i epsilon X_pq) F_4,
    U_Y(epsilon) = exp(i epsilon Y_pq) F_4,

where X_pq = |p><q| + |q><p| and
Y_pq = -i|p><q| + i|q><p|.

All permanent calculations are exact Gaussian-integer calculations.  The
script uses only the Python standard library and the project's exact
phase-histogram routine.
"""

from __future__ import annotations

import sys
from collections import defaultdict
from fractions import Fraction
from math import factorial
from pathlib import Path
from typing import Literal

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.fourier_suppression import phase_histogram  # noqa: E402


Occupation = tuple[int, int, int, int]
GaussianInteger = tuple[int, int]
Generator = Literal["X", "Y"]
PAIRS = tuple(
    (left, right)
    for left in range(4)
    for right in range(left + 1, 4)
)


def gaussian_add(
    left: GaussianInteger,
    right: GaussianInteger,
) -> GaussianInteger:
    return left[0] + right[0], left[1] + right[1]


def gaussian_multiply(
    left: GaussianInteger,
    right: GaussianInteger,
) -> GaussianInteger:
    return (
        left[0] * right[0] - left[1] * right[1],
        left[0] * right[1] + left[1] * right[0],
    )


def gaussian_norm_squared(value: GaussianInteger) -> int:
    return value[0] ** 2 + value[1] ** 2


def root_permanent(
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> GaussianInteger:
    """Return the permanent for the unnormalised root matrix 2 F_4."""
    histogram = phase_histogram(input_occupation, output_occupation)
    return histogram[0] - histogram[2], histogram[1] - histogram[3]


def physical_denominator_squared(
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> int:
    """Return D^2 when A=Z/D is the normalized Fock amplitude."""
    result = 4 ** sum(input_occupation)
    for multiplicity in input_occupation + output_occupation:
        result *= factorial(multiplicity)
    return result


def generator_moments(
    input_occupation: Occupation,
    output_occupation: Occupation,
    pair: tuple[int, int],
    generator: Generator,
    maximum_order: int,
) -> list[GaussianInteger]:
    """Return common-denominator numerators of <s|G^k F_4|r>.

    Square-root occupation factors cancel against the changing Fock-state
    normalization.  A transfer out of a mode with multiplicity n therefore
    contributes the integer n.  For Y, the two transfer orientations carry
    phases +i and -i.
    """
    p, q = pair
    weights: dict[Occupation, GaussianInteger] = {
        output_occupation: (1, 0)
    }
    moments: list[GaussianInteger] = []

    for _ in range(maximum_order + 1):
        moment = (0, 0)
        for occupation, weight in weights.items():
            contribution = gaussian_multiply(
                weight,
                root_permanent(input_occupation, occupation),
            )
            moment = gaussian_add(moment, contribution)
        moments.append(moment)

        next_weights: dict[Occupation, GaussianInteger] = defaultdict(
            lambda: (0, 0)
        )
        for occupation, weight in weights.items():
            values = list(occupation)
            if values[q]:
                moved = values.copy()
                moved[p] += 1
                moved[q] -= 1
                factor = (
                    (values[q], 0)
                    if generator == "X"
                    else (0, values[q])
                )
                key = tuple(moved)
                next_weights[key] = gaussian_add(
                    next_weights[key],
                    gaussian_multiply(weight, factor),
                )
            if values[p]:
                moved = values.copy()
                moved[p] -= 1
                moved[q] += 1
                factor = (
                    (values[p], 0)
                    if generator == "X"
                    else (0, -values[p])
                )
                key = tuple(moved)
                next_weights[key] = gaussian_add(
                    next_weights[key],
                    gaussian_multiply(weight, factor),
                )
        weights = dict(next_weights)

    return moments


def probability_leading_coefficient(
    input_occupation: Occupation,
    output_occupation: Occupation,
    pair: tuple[int, int],
    generator: Generator,
    order: int,
) -> Fraction:
    """Return c in P(epsilon)=c epsilon^(2 order)+higher powers."""
    moment = generator_moments(
        input_occupation,
        output_occupation,
        pair,
        generator,
        order,
    )[order]
    denominator_squared = physical_denominator_squared(
        input_occupation,
        output_occupation,
    )
    return Fraction(
        gaussian_norm_squared(moment),
        factorial(order) ** 2 * denominator_squared,
    )


def first_nonzero_order(
    input_occupation: Occupation,
    output_occupation: Occupation,
    pair: tuple[int, int],
    generator: Generator,
) -> tuple[int, Fraction] | None:
    """Find the first nonzero moment in the finite two-mode sector.

    If all moments through the sector dimension vanish, Cayley-Hamilton
    implies that the amplitude is identically zero along this rotation.
    """
    particles_in_pair = (
        output_occupation[pair[0]] + output_occupation[pair[1]]
    )
    moments = generator_moments(
        input_occupation,
        output_occupation,
        pair,
        generator,
        particles_in_pair,
    )
    for order, moment in enumerate(moments):
        if moment != (0, 0):
            coefficient = probability_leading_coefficient(
                input_occupation,
                output_occupation,
                pair,
                generator,
                order,
            )
            return order, coefficient
    return None


def format_leakage(result: tuple[int, Fraction] | None) -> str:
    if result is None:
        return "exact"
    order, coefficient = result
    return f"{coefficient} eps^{2 * order}"


def print_case(
    name: str,
    input_occupation: Occupation,
    output_occupation: Occupation,
) -> None:
    print(name)
    print("pair       X                         Y")
    for pair in PAIRS:
        x_result = first_nonzero_order(
            input_occupation, output_occupation, pair, "X"
        )
        y_result = first_nonzero_order(
            input_occupation, output_occupation, pair, "Y"
        )
        print(
            f"{pair[0]}{pair[1]:<7}"
            f"{format_leakage(x_result):<26}"
            f"{format_leakage(y_result)}"
        )
    print()


def certify_claims() -> None:
    cyclic = ((1, 1, 1, 1), (3, 1, 0, 0))
    parity = ((0, 1, 2, 1), (0, 1, 2, 1))
    isolated = ((0, 1, 3, 7), (1, 3, 3, 4))

    for generator in ("X", "Y"):
        assert probability_leading_coefficient(
            *cyclic, (0, 1), generator, 1
        ) == Fraction(3, 8)
        assert probability_leading_coefficient(
            *cyclic, (0, 3), generator, 1
        ) == Fraction(3, 8)
        for pair in ((0, 2), (1, 2), (1, 3), (2, 3)):
            assert first_nonzero_order(*cyclic, pair, generator) is None

    expected_parity_x = {
        (0, 1): Fraction(1, 64),
        (0, 2): Fraction(1, 4),
        (0, 3): Fraction(1, 64),
        (1, 2): Fraction(1, 64),
        (1, 3): Fraction(1, 4),
        (2, 3): Fraction(1, 64),
    }
    expected_parity_y = {
        (0, 1): Fraction(1, 64),
        (0, 2): Fraction(1, 4),
        (0, 3): Fraction(1, 64),
        (1, 2): Fraction(25, 64),
        (2, 3): Fraction(25, 64),
    }
    for pair, coefficient in expected_parity_x.items():
        assert probability_leading_coefficient(
            *parity, pair, "X", 1
        ) == coefficient
    for pair, coefficient in expected_parity_y.items():
        assert probability_leading_coefficient(
            *parity, pair, "Y", 1
        ) == coefficient
    assert first_nonzero_order(*parity, (1, 3), "Y") is None

    expected_isolated_x = {
        (0, 1): Fraction(595, 8192),
        (0, 2): Fraction(315, 16384),
        (0, 3): Fraction(875, 16384),
        (1, 2): Fraction(315, 16384),
        (1, 3): Fraction(315, 16384),
        (2, 3): Fraction(35, 4096),
    }
    expected_isolated_y = {
        (0, 1): Fraction(455, 16384),
        (0, 2): Fraction(315, 8192),
        (0, 3): Fraction(315, 16384),
        (1, 3): Fraction(315, 16384),
        (2, 3): Fraction(35, 4096),
    }
    for pair, coefficient in expected_isolated_x.items():
        assert probability_leading_coefficient(
            *isolated, pair, "X", 1
        ) == coefficient
    for pair, coefficient in expected_isolated_y.items():
        assert probability_leading_coefficient(
            *isolated, pair, "Y", 1
        ) == coefficient
    assert first_nonzero_order(*isolated, (1, 2), "Y") == (
        2,
        Fraction(315, 8192),
    )

    # Finite checks of the all-odd-a exact theorem proved in the note.
    for a in (1, 3, 5, 7):
        occupation = (0, a, 2 * a, a)
        assert first_nonzero_order(
            occupation, occupation, (1, 3), "Y"
        ) is None


def main() -> None:
    certify_claims()
    print_case(
        "cyclic: (1,1,1,1) -> (3,1,0,0)",
        (1, 1, 1, 1),
        (3, 1, 0, 0),
    )
    print_case(
        "parity a=1: (0,1,2,1) -> itself",
        (0, 1, 2, 1),
        (0, 1, 2, 1),
    )
    print_case(
        "isolated N=11 B: (0,1,3,7) -> (1,3,3,4)",
        (0, 1, 3, 7),
        (1, 3, 3, 4),
    )
    print("All exact leakage certificates passed.")


if __name__ == "__main__":
    main()
