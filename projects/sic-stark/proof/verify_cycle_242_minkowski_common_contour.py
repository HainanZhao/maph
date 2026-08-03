#!/usr/bin/env python3
"""Exact common-cone contour audit for Cycle 242/B079."""
from __future__ import annotations

import json
from fractions import Fraction as F

try:
    from .verify_cycle_228_f3_square_residual_block import blocks
except ImportError:  # pragma: no cover - direct replay
    from verify_cycle_228_f3_square_residual_block import blocks


Affine = tuple[F, F]  # a*t+b


def affine_pair(item: dict[str, object], key: str) -> Affine:
    raw = item[key]
    assert isinstance(raw, list) and len(raw) == 2
    return (F(str(raw[0])), F(str(raw[1])))


def strict_interval(periods: list[Affine]) -> dict[str, str | None]:
    """Solve a*u+b>0 for every frozen period generator."""
    lower: F | None = None
    upper: F | None = None
    for a, b in periods:
        if a == 0:
            assert b > 0
        elif a > 0:
            bound = -b / a
            lower = bound if lower is None else max(lower, bound)
        else:
            bound = -b / a
            upper = bound if upper is None else min(upper, bound)
    return {
        "strict_lower": None if lower is None else str(lower),
        "strict_upper": None if upper is None else str(upper),
    }


def interval_is_nonempty(interval: dict[str, str | None]) -> bool:
    lower = interval["strict_lower"]
    upper = interval["strict_upper"]
    return lower is None or upper is None or F(lower) < F(upper)


def all_periods(start: str) -> list[Affine]:
    answer: list[Affine] = []
    for item in blocks()[start]:
        answer.extend((affine_pair(item, "alpha"), affine_pair(item, "beta")))
    assert len(answer) == 8
    return answer


def audit() -> dict[str, object]:
    block_periods = {start: all_periods(start) for start in ("A", "C")}
    intervals = {start: strict_interval(periods) for start, periods in block_periods.items()}
    assert intervals["A"] == {"strict_lower": "0", "strict_upper": "1/115"}
    assert intervals["C"] == {"strict_lower": "5", "strict_upper": None}

    combined = strict_interval(block_periods["A"] + block_periods["C"])
    assert combined == {"strict_lower": "5", "strict_upper": "1/115"}
    assert not interval_is_nonempty(combined)

    embeddings = []
    for label, value in (("sigma_+", "55+12*sqrt(21)"), ("sigma_-", "55-12*sqrt(21)")):
        # For t_sigma(epsilon)=x+i*epsilon and
        # L_h(z)=Re(z)+(h/epsilon)Im(z),
        # L_h(a*t_sigma(epsilon)+b)=a*(x+h)+b.  Since h ranges over R,
        # u=x+h has exactly the interval computed above for either embedding.
        embeddings.append(
            {
                "embedding": label,
                "t_value": value,
                "normal_form": "L_h(a*t_sigma(epsilon)+b)=a*u+b, u=t_sigma+h",
                "A_required_u_interval": "0<u<1/115",
                "C_required_u_interval": "u>5",
                "common_affine_linear_cone_separator": False,
            }
        )

    return {
        "epistemic_status": "PROVED",
        "regularization": {
            "tilt": "t_sigma(epsilon)=t_sigma+i*epsilon, epsilon>0",
            "contour_normal": "L_{sigma,h}(z)=Re(z)+(h/epsilon)Im(z)",
            "criterion": "one h per embedding must be strictly positive on all A/C period generators",
        },
        "period_intervals": intervals,
        "combined_interval": combined,
        "witness": {
            "A_periods": ["t", "(1-115*t)/24"],
            "C_period": "(t-5)/24",
            "contradiction": "0<u<1/115 and u>5",
        },
        "embeddings": embeddings,
        "common_affine_linear_cone_separator_exists": False,
        "status": "FALSIFIED_COMMON_AFFINE_LINEAR_MINKOWSKI_CONE_SEPARATOR",
        "conclusion": "Neither Minkowski embedding admits a fixed affine-linear cone normal separating all period rays of both C228 A and C words under the frozen upper tilt. Thus the paired words have no shared pole/zero cone contour in this specified class. This does not address a contour for one word alone, nonlinear/factor-dependent contours, other regularizations, a mixed-base identity, AFK, fusion, Stark, or TCC.",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, sort_keys=True))
