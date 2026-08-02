"""Exact Cycle 44 derivative-test exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
RESOLUTION = Q(11, 25)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def derivative_test(d: int, nu: Q) -> dict[str, Q | int]:
    require(isinstance(d, int) and d >= 3, "derivative order d>=3")
    require(nu >= 0, "nonnegative Fourier exponent")
    D = 2**d
    derivative_exponent = nu + Q(1) - d * DELTA
    term_a_saving = 2 * DELTA / D
    term_b_saving = -derivative_exponent / (D - 2)
    term_c_saving = 2 * (nu + Q(1)) / D
    guaranteed_saving = min(term_a_saving, term_b_saving, term_c_saving)
    return {
        "order": d,
        "D": D,
        "fourier_exponent": nu,
        "derivative_exponent": derivative_exponent,
        "term_a_saving": term_a_saving,
        "term_b_saving": term_b_saving,
        "term_c_saving": term_c_saving,
        "guaranteed_saving": guaranteed_saving,
    }


def registered_scales() -> dict[str, object]:
    low_d3 = derivative_test(3, Q(0))
    resolved_d3 = derivative_test(3, RESOLUTION)
    resolved_d4 = derivative_test(4, RESOLUTION)
    resolved_d5 = derivative_test(5, RESOLUTION)
    require(low_d3["guaranteed_saving"] == Q(2, 15), "low-mode cubic saving")
    require(resolved_d3["guaranteed_saving"] == Q(3, 50), "resolved cubic saving")
    require(resolved_d4["guaranteed_saving"] == Q(12, 175), "resolved quartic saving")
    require(resolved_d5["term_a_saving"] == Q(3, 80), "higher-order ceiling")
    require(resolved_d4["guaranteed_saving"] > resolved_d3["guaranteed_saving"], "d4 beats d3 at resolution")
    require(resolved_d4["guaranteed_saving"] < Q(7, 50), "below narrow closure margin")
    return {
        "resolution": RESOLUTION,
        "low_mode_d3": low_d3,
        "resolved_d3": resolved_d3,
        "resolved_d4": resolved_d4,
        "resolved_d5": resolved_d5,
        "best_registered_saving": resolved_d4["guaranteed_saving"],
        "cycle39_margin_r2": Q(17, 50),
        "cycle39_margin_r4": Q(7, 50),
    }


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
