"""Exact Cycle 49 row-Fourier exceptional-set ledger."""
from __future__ import annotations

from fractions import Fraction as Q


ROWS = Q(21, 25)
SPACING = Q(3, 5)
BAND = Q(3, 10)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def exceptional_exponent(tau: Q) -> Q:
    require(tau >= 0, "nonnegative threshold saving")
    return BAND + 2 * tau - ROWS


def absolute_lcam_gap(s: int, tau: Q) -> Q:
    require(isinstance(s, int) and s >= 1, "positive amplifier")
    absolute_off_diagonal = Q(2 * s + 2) + ROWS + BAND - tau
    target = Q(s) + Q(31, 10)
    return absolute_off_diagonal - target


def verify_all() -> dict[str, object]:
    off_diagonal_mean_square = ROWS - SPACING
    diagonal_mean_square = BAND + ROWS
    require(off_diagonal_mean_square == Q(6, 25), "mean-square off diagonal")
    require(diagonal_mean_square == Q(57, 50), "mean-square diagonal")
    thresholds = {
        "s4_margin": Q(7, 50),
        "full_missing": Q(4, 25),
        "s3_margin": Q(17, 50),
    }
    exceptional = {key: exceptional_exponent(value) for key, value in thresholds.items()}
    require(exceptional == {"s4_margin": Q(-13, 50), "full_missing": Q(-11, 50), "s3_margin": Q(7, 50)}, "exceptional exponents")
    require(absolute_lcam_gap(4, Q(7, 50)) == Q(39, 10), "s4 absolute gap")
    return {
        "mean_square": {
            "diagonal": diagonal_mean_square,
            "off_diagonal_absolute_bound": off_diagonal_mean_square,
            "off_diagonal_gap_below_diagonal": diagonal_mean_square - off_diagonal_mean_square,
        },
        "thresholds": thresholds,
        "exceptional_measure_exponents": exceptional,
        "absolute_lcam_gaps": {
            "s3_at_17_50": absolute_lcam_gap(3, Q(17, 50)),
            "s4_at_7_50": absolute_lcam_gap(4, Q(7, 50)),
        },
    }


if __name__ == "__main__":
    print(verify_all())
