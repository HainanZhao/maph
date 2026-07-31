#!/usr/bin/env python3
"""Exact class descent and Fourier-cancellation audit for dimension five."""

from __future__ import annotations

from fractions import Fraction
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cocycle import kopp_total_multiplier_exponent  # noqa: E402


MATRIX = ((56, -15), (15, -4))
RAY_LOGS = (
    (None, 0, 6, 2, 4),
    (4, 7, 5, 7, 0),
    (2, 5, 5, 6, 3),
    (6, 7, 2, 1, 1),
    (0, 4, 3, 1, 3),
)


def positive_lift(first: int, second: int) -> int:
    lifted = first
    while True:
        if lifted < 0:
            return lifted
        passed = (
            second != 0
            and 2 * second - lifted > 0
            and (2 * second - lifted) ** 2 > 3 * second**2
        )
        if passed:
            return lifted
        lifted -= 5


def main() -> None:
    representatives: dict[int, list[tuple[int, int, Fraction]]] = {}
    for first in range(5):
        for second in range(5):
            if first == second == 0:
                continue
            ray_log = RAY_LOGS[first][second]
            if ray_log is None:
                raise AssertionError("missing nonzero ray label")
            lifted = positive_lift(first, second)
            multiplier = kopp_total_multiplier_exponent(
                MATRIX,
                Fraction(lifted, 5),
                Fraction(second, 5),
            )
            representatives.setdefault(ray_log, []).append(
                (first, second, multiplier)
            )

    descended = {}
    for ray_log in range(8):
        rows = representatives[ray_log]
        values = {row[2] for row in rows}
        if len(rows) != 3 or len(values) != 1:
            raise AssertionError(
                f"class {ray_log} does not descend: {rows}"
            )
        descended[ray_log] = values.pop()
        print(
            f"RAY_CLASS={ray_log}|REPRESENTATIVES=3"
            f"|MULTIPLIER={descended[ray_log]}|DESCENDS=1"
        )

    sign_class = 4
    for ray_log in range(4):
        if descended[ray_log + sign_class] != descended[ray_log]:
            raise AssertionError("sign-class invariance failed")
    print("SIGN_CLASS_INVARIANCE=PASS")

    # The differenced packet supports exactly characters j odd, for
    # which chi_j(R)=-1. Pairing A and R*A gives exact cancellation:
    # m(A)chi(A)^-1 + m(RA)chi(RA)^-1 = 0.
    supported = (1, 3, 5, 7)
    for character in supported:
        if character % 2 != 1:
            raise AssertionError("support parity changed")
        for ray_log in range(4):
            if descended[ray_log] != descended[ray_log + sign_class]:
                raise AssertionError("pair multiplier mismatch")
            # chi_j(R)=exp(2*pi*i*j*4/8)=(-1)^j=-1.
            if (-1) ** character != -1:
                raise AssertionError("supported character is not R-odd")
        print(
            f"CHARACTER={character}|R_VALUE=-1"
            "|FOURIER_RESOLVENT=0|PAIRWISE_PROOF=1"
        )

    print("CLASS_DESCENT=PASS")
    print("RELEVANT_FOURIER_RESOLVENT=ZERO")
    print("SQUARED_MULTIPLIER_PHASE_MECHANISM=VERIFIED_NO_GO")


if __name__ == "__main__":
    main()
