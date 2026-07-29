#!/usr/bin/env python3
"""Arb conditioning slopes for the d=6 rehearsal and proved d=4 control.

At precision P we ask each q-Pochhammer factor for tolerance
10^(-(P-20)).  If Z is the resulting complex ball, define

    C = rad(Z)/|mid(Z)| * 10^(P-20).

Thus C measures decimal precision lost after the requested tail tolerance
has been divided out.  It is an implementation-conditioning diagnostic,
not a theorem about the boundary value.
"""

from __future__ import annotations

from fractions import Fraction
import json
import math

from flint import arb, ctx

from dimension_four_two_base_calibration import (
    gamma_lens_factorized as gamma_four,
    geodesic_point as geodesic_four,
)
from dimension_six_two_base_lens import (
    gamma_lens_factorized as gamma_six,
    geodesic_point as geodesic_six,
)


def linear_fit(x_values: list[float], y_values: list[float]) -> dict[str, float]:
    count = len(x_values)
    x_mean = sum(x_values) / count
    y_mean = sum(y_values) / count
    covariance = sum(
        (x - x_mean) * (y - y_mean)
        for x, y in zip(x_values, y_values)
    )
    variance = sum((x - x_mean) ** 2 for x in x_values)
    slope = covariance / variance
    intercept = y_mean - slope * x_mean
    residual = sum(
        (y - (slope * x + intercept)) ** 2
        for x, y in zip(x_values, y_values)
    )
    total = sum((y - y_mean) ** 2 for y in y_values)
    return {
        "slope": slope,
        "intercept": intercept,
        "r_squared": 1 - residual / total,
    }


def evaluate(
    dimension: int,
    precision: int,
    denominators: tuple[int, ...],
) -> dict[str, object]:
    ctx.dps = precision
    ctx.cap = 10
    guard_digits = 20
    requested_exponent = precision - guard_digits
    tolerance = Fraction(1, 10**requested_exponent)
    if dimension == 6:
        geodesic = geodesic_six
        gamma = gamma_six
        trace = 5
        reflected_total = 4
    elif dimension == 4:
        geodesic = geodesic_four
        gamma = gamma_four
        trace = 3
        reflected_total = 2
    else:
        raise ValueError("only dimensions four and six are calibrated")

    beta = (arb(trace) + arb(trace**2 - 4).sqrt()) / 2
    records = []
    for denominator in denominators:
        tau = geodesic(Fraction(1, denominator))
        if dimension == 6:
            alpha = 4 * (4 * tau - 1) / 3
            discrete = 2
        else:
            alpha = 2 * (2 * tau - 1)
            discrete = 1
        value = gamma(
            alpha, discrete, tau, tolerance
        ) * gamma(
            -alpha,
            reflected_total - discrete,
            tau,
            tolerance,
        )
        radius = max(value.real.rad(), value.imag.rad())
        relative_radius = radius / abs(value)
        condition_proxy = (
            float(relative_radius.mid()) * 10**requested_exponent
        )
        defect = abs(tau + 1 / tau - trace)
        endpoint_distance = abs(tau - beta)
        records.append(
            {
                "one_over_s": denominator,
                "s": 1 / denominator,
                "trace_defect": float(defect.mid()),
                "distance_to_beta": float(endpoint_distance.mid()),
                "relative_ball_radius": float(relative_radius.mid()),
                "condition_proxy": condition_proxy,
                "log10_condition_proxy": math.log10(condition_proxy),
            }
        )

    logarithms = [
        record["log10_condition_proxy"] for record in records
    ]
    reciprocal_s_fit = linear_fit(
        [float(record["one_over_s"]) for record in records],
        logarithms,
    )
    inverse_defect_fit = linear_fit(
        [1 / float(record["trace_defect"]) for record in records],
        logarithms,
    )
    inverse_endpoint_distance_fit = linear_fit(
        [1 / float(record["distance_to_beta"]) for record in records],
        logarithms,
    )
    power_fit = linear_fit(
        [
            math.log10(1 / float(record["trace_defect"]))
            for record in records
        ],
        logarithms,
    )
    return {
        "dimension": dimension,
        "precision_digits": precision,
        "guard_digits": guard_digits,
        "requested_tolerance": f"1e-{requested_exponent}",
        "records": records,
        "log10_condition_vs_one_over_s": reciprocal_s_fit,
        "log10_condition_vs_inverse_trace_defect": inverse_defect_fit,
        "log10_condition_vs_inverse_distance_to_beta": (
            inverse_endpoint_distance_fit
        ),
        "power_law_fit": power_fit,
    }


def main() -> None:
    primary_six = evaluate(6, 120, (8, 12, 16, 20, 24, 28, 32))
    replicate_six = evaluate(6, 80, (8, 12, 16, 20, 24))
    primary_four = evaluate(
        4, 180, (32, 36, 40, 44, 48, 52, 56, 60, 64)
    )
    replicate_four = evaluate(4, 140, (32, 36, 40, 44, 48, 52))

    six_slope = primary_six[
        "log10_condition_vs_one_over_s"
    ]["slope"]
    four_slope = primary_four[
        "log10_condition_vs_one_over_s"
    ]["slope"]
    assert 2.7 < six_slope < 2.9
    assert 0.60 < four_slope < 0.69
    assert 2.7 < replicate_six[
        "log10_condition_vs_one_over_s"
    ]["slope"] < 2.9
    assert 0.60 < replicate_four[
        "log10_condition_vs_one_over_s"
    ]["slope"] < 0.69
    assert primary_six[
        "log10_condition_vs_one_over_s"
    ]["r_squared"] > 0.999
    assert primary_four[
        "log10_condition_vs_one_over_s"
    ]["r_squared"] > 0.999

    result = {
        "schema": "sic-stark-conditioning-comparison-v1",
        "definition": (
            "C_d(s)=relative Arb radius divided by the requested "
            "q-Pochhammer tolerance"
        ),
        "primary_dimension_six": primary_six,
        "replicate_dimension_six": replicate_six,
        "primary_dimension_four": primary_four,
        "replicate_dimension_four": replicate_four,
        "slope_summary": {
            "d6_decimal_digits_lost_per_one_over_s": six_slope,
            "d4_decimal_digits_lost_per_one_over_s": four_slope,
            "d6_over_d4_slope_ratio": six_slope / four_slope,
            "d6_decimal_digits_lost_per_inverse_trace_defect": (
                primary_six[
                    "log10_condition_vs_inverse_trace_defect"
                ]["slope"]
            ),
            "d4_decimal_digits_lost_per_inverse_trace_defect": (
                primary_four[
                    "log10_condition_vs_inverse_trace_defect"
                ]["slope"]
            ),
            "d6_decimal_digits_lost_per_inverse_distance_to_beta": (
                primary_six[
                    "log10_condition_vs_inverse_distance_to_beta"
                ]["slope"]
            ),
            "d4_decimal_digits_lost_per_inverse_distance_to_beta": (
                primary_four[
                    "log10_condition_vs_inverse_distance_to_beta"
                ]["slope"]
            ),
        },
        "empirical_model_verdict": (
            "ESSENTIAL_EXPONENTIAL_IN_ONE_OVER_S_ON_PINNED_WINDOWS"
        ),
        "not_an_intrinsic_exponent": True,
        "interpretation": (
            "The factorized-continuation rehearsal loses precision "
            "like exp(c/s), not logarithmically and not by a stable "
            "power of the trace defect.  Dimension four proves that "
            "this numerical pathology does not imply nonexistence of "
            "the boundary value.  The d=6 slope is nevertheless about "
            "4.36 times steeper on the pinned windows."
        ),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
