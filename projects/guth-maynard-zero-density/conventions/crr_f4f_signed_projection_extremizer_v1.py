"""Exact scale bookkeeping for the signed F4F projection/extremizer note.

The analytic projection and probabilistic-existence arguments are written in
the accompanying note.  This module freezes only the integer identities and
the conservative constants used by those arguments.
"""
from __future__ import annotations

from fractions import Fraction
from math import gcd


MIN_Q = 2**20


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    require(isinstance(v, int) and v >= 8 and v % 2 == 0, "v must be an even integer at least 8")
    q = v**4
    h = v**12
    r = v**8
    require(h == q**3, "signed extremizer requires H=Q^3")
    require(r == q**2, "signed extremizer requires R=Q^2")
    require(q % 4 == 0, "even v must make Q divisible by four")
    return {"v": v, "Q": q, "H": h, "R": r}


def actual_anchor(q: int) -> dict[str, int]:
    require(isinstance(q, int) and q >= 4 and q % 4 == 0, "anchor requires Q divisible by four and at least four")
    r = q + 1
    s = 5 * q // 4 + 1
    require(q <= r < 2 * q and q <= s < 2 * q, "anchor lies outside the actual Farey shell")
    require(gcd(r, s) == 1, "anchor label must be reduced")
    require(4 * r > 3 * s and 4 * r <= 5 * s, "anchor ratio leaves the frozen Farey ratio shell")
    require(5 * r > 4 * s and 6 * r <= 5 * s, "anchor must lie between 4/5 and 5/6")
    return {"r": r, "s": s}


def exact_rows() -> dict[str, Fraction | int | str]:
    rows: dict[str, Fraction | int | str] = {
        "period_strict_lower": 24,
        "period_strict_upper": 38,
        "random_subset_multiplier": 2,
        "energy_expectation_upper_constant": 2**14,
        "energy_existence_upper_constant": 2**16,
        "close_pair_expectation_constant": 304,
        "close_pair_existence_constant": 1216,
        "close_pair_q_exponent": Fraction(103, 100),
        "safe_minimum_Q": MIN_Q,
        "local_fourth_moment_lower_constant": Fraction(1, 20),
        "projection_normalization": "P_E=(2*pi)^(-1)K_E=F^(-1)M_(1_E)F",
        "finite_diagnostic_scope": "finite homogeneous continuous linear functionals on unrestricted L^2(R)",
    }
    require(rows["energy_existence_upper_constant"] == 4 * rows["energy_expectation_upper_constant"], "Markov energy factor mismatch")
    require(rows["close_pair_existence_constant"] == 4 * rows["close_pair_expectation_constant"], "Markov close-pair factor mismatch")
    require(rows["energy_expectation_upper_constant"] > 9826, "random-energy constant is not conservative")
    require((2**20) ** 97 > 1216**100, "minimum Q no longer makes close-pair deletions subcritical")
    return rows


def verify_all(v: int = 8) -> dict[str, object]:
    data = scales(v)
    anchor = actual_anchor(data["Q"])
    rows = exact_rows()
    require(data["H"] ** 1 == data["Q"] ** 3, "H/Q exponent identity changed")
    require(data["R"] ** 4 // data["H"] == data["Q"] ** 5, "central local-fourth-moment scale changed")
    require(Fraction(4) - Fraction(3) + Fraction(3, 100) == rows["close_pair_q_exponent"], "close-pair exponent changed")
    return {"scales": data, "actual_anchor": anchor, "exact_rows": rows}
