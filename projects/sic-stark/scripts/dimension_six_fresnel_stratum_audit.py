#!/usr/bin/env python3
"""Compare d=6 Fresnel frequencies with analytic and arithmetic strata."""

from __future__ import annotations

from fractions import Fraction
import json
import math


DIMENSION = 6
TRACE_SEQUENCE = [2, 5]
while len(TRACE_SEQUENCE) <= 12:
    TRACE_SEQUENCE.append(
        5 * TRACE_SEQUENCE[-1] - TRACE_SEQUENCE[-2]
    )


def centered_lift(value: int) -> int:
    return (value + 3) % 6 - 3


def shift_output_from_frequency(
    shift: int, frequency: tuple[int, int]
) -> tuple[int, int]:
    first, second = frequency
    if shift == 1:
        # Inverse of (u,v)->(-u,-u-v).
        return (-first % 6, (first - second) % 6)
    if shift == 0:
        # Inverse of (u,v)->(-u-v,-v).
        return ((second - first) % 6, -second % 6)
    raise ValueError("formal shift must be zero or one")


def characteristic_denominator(point: tuple[int, int]) -> int:
    first, second = point
    return DIMENSION // math.gcd(DIMENSION, first, second)


def zauner_step(point: tuple[int, int]) -> tuple[int, int]:
    first, second = point
    return ((5 * first + second) % 6, (-first) % 6)


def orbit(point: tuple[int, int]) -> tuple[tuple[int, int], ...]:
    result = []
    current = point
    while current not in result:
        result.append(current)
        current = zauner_step(current)
    assert current == point
    return tuple(result)


def mapped_rational(base_index: int) -> tuple[int, int]:
    return (
        TRACE_SEQUENCE[base_index + 2],
        TRACE_SEQUENCE[base_index + 3],
    )


def singular_data(
    numerator: int,
    denominator: int,
    point: tuple[int, int],
) -> tuple[int, Fraction] | None:
    first, second = point
    residue_numerator = first * denominator - second * numerator
    if residue_numerator % 6:
        return None
    residue = (
        (residue_numerator // 6)
        * pow(numerator, -1, denominator)
    ) % denominator
    alpha = Fraction(
        second + 6 * residue,
        6 * denominator,
    )
    return residue, alpha


def qgamma_tame_set(base_index: int) -> set[tuple[int, int]]:
    numerator, denominator = mapped_rational(base_index)
    result = {(0, 0)}
    for first in range(6):
        for second in range(6):
            point = (first, second)
            if point != (0, 0) and singular_data(
                numerator, denominator, point
            ) is not None:
                result.add(point)
    assert len(result) == 6
    return result


def main() -> None:
    fresnel_frequencies = {
        (first, second)
        for first in range(6)
        for second in range(6)
        if centered_lift(4 * second - 5 * first) == 0
    }
    assert len(fresnel_frequencies) == 6
    lower_orbit = set(orbit((0, 2)))
    assert lower_orbit == {(0, 2), (2, 0), (4, 4)}

    shift_records = {}
    for shift, qgamma_index in ((1, 1), (0, 2)):
        fresnel_outputs = {
            shift_output_from_frequency(shift, frequency)
            for frequency in fresnel_frequencies
        }
        assert len(fresnel_outputs) == 6
        analytic_tame = qgamma_tame_set(qgamma_index)
        assert fresnel_outputs == analytic_tame

        growing_outputs = {
            (first, second)
            for first in range(6)
            for second in range(6)
        } - fresnel_outputs
        fresnel_denominators = {
            denominator: sum(
                characteristic_denominator(point) == denominator
                for point in fresnel_outputs
            )
            for denominator in (1, 2, 3, 6)
        }
        growing_denominators = {
            denominator: sum(
                characteristic_denominator(point) == denominator
                for point in growing_outputs
            )
            for denominator in (1, 2, 3, 6)
        }
        assert fresnel_denominators == {1: 1, 2: 1, 3: 2, 6: 2}
        assert growing_denominators == {1: 0, 2: 2, 3: 6, 6: 22}
        assert len(fresnel_outputs & lower_orbit) == 1
        assert len(growing_outputs & lower_orbit) == 2

        shift_records[str(shift)] = {
            "qgamma_axis_step": qgamma_index,
            "fresnel_outputs": sorted(
                [list(point) for point in fresnel_outputs]
            ),
            "qgamma_tame_outputs": sorted(
                [list(point) for point in analytic_tame]
            ),
            "fresnel_equals_qgamma_tame": True,
            "fresnel_denominator_counts": fresnel_denominators,
            "growing_denominator_counts": growing_denominators,
            "proved_modulus_three_orbit": sorted(
                [list(point) for point in lower_orbit]
            ),
            "fresnel_intersection_with_modulus_three": sorted(
                [list(point) for point in fresnel_outputs & lower_orbit]
            ),
            "growing_intersection_with_modulus_three": sorted(
                [list(point) for point in growing_outputs & lower_orbit]
            ),
        }

    result = {
        "schema": "sic-stark-dimension-six-fresnel-stratum-v1",
        "fresnel_frequency_condition": "4*b-5*a == 0 mod 6",
        "fresnel_frequencies": sorted(
            [list(point) for point in fresnel_frequencies]
        ),
        "shift_records": shift_records,
        "analytic_classification_matches_qgamma_cancellation": True,
        "analytic_classification_matches_arithmetic_lower_stratum": False,
        "mismatch": (
            "Each Fresnel set contains two denominator-six "
            "characteristics, while each growing set contains eight "
            "proper-denominator characteristics.  Only one of the "
            "three proved modulus-three orbit points is Fresnel for "
            "either formal shift."
        ),
        "conclusion": (
            "The 6/30 split is an analytic Fourier-direction split, "
            "not the conductor stratification.  Its exact match is "
            "with the six q-gamma tame/singular-cancellation modes."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
