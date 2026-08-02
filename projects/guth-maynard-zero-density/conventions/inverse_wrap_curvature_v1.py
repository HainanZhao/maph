"""Exact Cycle 46 inverse-wrap curvature ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
FOURIER = Q(11, 25)
ALIAS_POWER = Q(7, 11)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def inverse_curve(nu: Q = FOURIER, alias_power: Q = ALIAS_POWER) -> dict[str, Q]:
    require(0 < nu <= DELTA, "Fourier exponent range")
    require(0 <= alias_power <= 1, "alias power range")
    j_length = nu
    curve_height = DELTA
    slope = DELTA - nu
    curvature = DELTA - 2 * nu
    tube_width = DELTA - nu - Q(1)
    target_count = alias_power * nu
    return {
        "fourier_exponent": nu,
        "j_length": j_length,
        "curve_height": curve_height,
        "slope": slope,
        "curvature": curvature,
        "tube_width": tube_width,
        "target_count": target_count,
        "reciprocal_curvature": -curvature,
    }


def registered_scales() -> dict[str, object]:
    row = inverse_curve()
    require(row["slope"] == Q(4, 25), "slope")
    require(row["curvature"] == Q(-7, 25), "curvature")
    require(row["tube_width"] == Q(-21, 25), "tube width")
    require(row["target_count"] == Q(7, 25), "target count")
    require(row["target_count"] == row["reciprocal_curvature"], "reciprocal-curvature transition")
    return {"critical_inverse_curve": row}


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
