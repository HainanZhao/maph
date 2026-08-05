#!/usr/bin/env python3
"""Exact fourth-order flat-stratum audit for the S3 Zhao deficit.

The three transposition coordinates form the standard S3 representation
V={x+y+z=0}; the oriented 3-cycle difference is the sign representation.
For a Hessian-flat central base, the restricted invariant quartic has form

 A |v|^4 + B |v|^2 s^2 + C s^4 + D s Delta(v),

where Delta=(x-y)(y-z)(z-x).  This program computes all coefficients from
the defining K_{5,5} minus C_10 sum with integer truncated polynomials.
It also proves strict positivity using Delta^2 <= |v|^6/2.
"""
from __future__ import annotations

import json
from fractions import Fraction
from itertools import permutations, product
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "discovery/out/cycle61-flat-stratum"
DEGREE = 4

# Lexicographic S3 order, matching C55's exact symbolic evaluator.
GROUP = list(permutations(range(3)))
INDEX = {g: i for i, g in enumerate(GROUP)}
MUL = [[INDEX[tuple(g[i] for i in h)] for h in GROUP] for g in GROUP]
INV = [next(j for j in range(6) if MUL[i][j] == MUL[j][i] == 0) for i in range(6)]


def order(i: int) -> int:
    value, n = i, 1
    while value:
        value = MUL[value][i]
        n += 1
    return n


CL = [0 if order(i) == 1 else 1 if order(i) == 2 else 2 for i in range(6)]
NEIGHBORS = ((2, 3, 4), (0, 3, 4), (0, 1, 4), (0, 1, 2), (1, 2, 3))


def add(a: list[int], b: list[int]) -> list[int]:
    return [x + y for x, y in zip(a, b)]


def mul(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (DEGREE + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b[: DEGREE + 1 - i]):
            out[i + j] += x * y
    return out


def deficit_taylor(base: tuple[int, int, int], direction: tuple[int, ...]) -> list[int]:
    """Unnormalised exact deficit polynomial at base+t*direction.

    Direction has class average zero, hence its positive-degree coefficients
    are exactly those of N(a)-N(P_cl a).
    """
    total = [0] * (DEGREE + 1)
    for x1, x2, x3, x4 in product(range(6), repeat=4):
        x = (0, x1, x2, x3, x4)
        graph_product = [1] + [0] * DEGREE
        for neighborhood in NEIGHBORS:
            summand = [0] * (DEGREE + 1)
            for y in range(6):
                term = [1] + [0] * DEGREE
                for i in neighborhood:
                    h = MUL[INV[x[i]]][y]
                    term = mul(term, [base[CL[h]], direction[h]])
                summand = add(summand, term)
            graph_product = mul(graph_product, summand)
        total = add(total, graph_product)
    return total


FLAT_BASES = ((1, 1, 1), (1, 2, 1), (2, 1, 2), (2, 2, 2))
# Coordinates on the transposition class and the oriented 3-cycle sign line.
STANDARD_AXIS = (0, -1, 0, 0, 0, 1)
STANDARD_GENERIC = (0, -1, -2, 0, 0, 3)
SIGN = (0, 0, 0, -1, 1, 0)


def plus(a: tuple[int, ...], b: tuple[int, ...], sign: int = 1) -> tuple[int, ...]:
    return tuple(x + sign * y for x, y in zip(a, b))


def norm2(v: tuple[int, ...]) -> int:
    return sum(v[i] * v[i] for i in (1, 2, 5))


def delta(v: tuple[int, ...]) -> int:
    x, y, z = (v[i] for i in (1, 2, 5))
    return (x - y) * (y - z) * (z - x)


def strict_lower_bound(
    A: Fraction, B: Fraction, C: Fraction, D: Fraction
) -> dict[str, bool]:
    """Certificate for A*r^4+B*r^2*s^2+C*s^4-|D|r^3|s|/sqrt(2)>0.

    The Cauchy/AM-GM bound r^4+s^4 >= 2 r^2 s^2 gives a simple entirely
    integral certificate when B >= 0 and D=0.  The generic calculation keeps
    this check deliberately narrow: a nonzero D demands a new exact
    univariate certificate rather than a claimed pass.
    """
    return {
        "A_positive": A > 0,
        "B_nonnegative": B >= 0,
        "C_positive": C > 0,
        "D_zero": D == 0,
        "strict_positive_certified": A > 0 and B >= 0 and C > 0 and D == 0,
    }


def fraction_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def main() -> None:
    results: dict[str, object] = {
        "status": "PASS",
        "claim_boundary": "Four frozen S3 central Hessian-flat bases only; not a universal Zhao proof.",
        "epistemic_status": "PROVED",
        "conventions": {
            "group_order": ["012", "021", "102", "120", "201", "210"],
            "standard_coordinates": [1, 2, 5],
            "sign_coordinates": [3, 4],
            "delta": "(x-y)(y-z)(z-x)",
        },
        "bases": {},
    }
    for base in FLAT_BASES:
        axis = deficit_taylor(base, STANDARD_AXIS)
        generic = deficit_taylor(base, STANDARD_GENERIC)
        sign = deficit_taylor(base, SIGN)
        mixed_plus = deficit_taylor(base, plus(STANDARD_GENERIC, SIGN))
        mixed_minus = deficit_taylor(base, plus(STANDARD_GENERIC, SIGN, -1))
        assert axis[2] == generic[2] == sign[2] == 0
        assert axis[3] == generic[3] == sign[3] == 0
        assert axis[4] > 0 and generic[4] > 0 and sign[4] > 0
        r2 = norm2(STANDARD_GENERIC)
        dlt = delta(STANDARD_GENERIC)
        assert dlt != 0
        A = Fraction(axis[4], norm2(STANDARD_AXIS) ** 2)
        assert generic[4] == A * r2 * r2
        C = sign[4]
        assert (mixed_plus[4] + mixed_minus[4]) % 2 == 0
        even = (mixed_plus[4] + mixed_minus[4]) // 2
        B = Fraction(even - A * r2 * r2 - C, r2)
        D = Fraction(mixed_plus[4] - mixed_minus[4], 2 * dlt)
        certificate = strict_lower_bound(A, B, C, D)
        assert certificate["strict_positive_certified"]
        results["bases"]["".join(map(str, base))] = {
            "axis_taylor": axis,
            "generic_taylor": generic,
            "sign_taylor": sign,
            "generic_plus_sign_taylor": mixed_plus,
            "generic_minus_sign_taylor": mixed_minus,
            "standard_generic_norm_squared": r2,
            "standard_generic_delta": dlt,
            "quartic_invariant_coefficients": {
                "A": fraction_text(A), "B": fraction_text(B),
                "C": fraction_text(C), "D": fraction_text(D),
            },
            "strict_positivity_certificate": certificate,
        }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "flat-stratum-summary.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    print(json.dumps(results, sort_keys=True))


if __name__ == "__main__":
    main()
