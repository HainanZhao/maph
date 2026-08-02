"""Cycle 110 weighted perfect-power primitive-split aggregation."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, sqrt
from typing import Any


def divisor_count(n: int) -> int:
    if n < 1:
        raise ValueError("positive integer required")
    return sum(n % divisor == 0 for divisor in range(1, n + 1))


def split_record(*, u: int, v: int, n0: int, r0: int) -> dict[str, Any]:
    if min(u, v, n0, r0) <= 0 or gcd(u, v) != 1 or gcd(n0, r0) != 1:
        raise ValueError("positive coprime split and reduced base required")
    d = u + v
    x = gcd(u, r0**d)
    y = gcd(v, n0**d)
    K = Fraction(d * n0**u * r0**v, x * y)
    B0 = v * r0**d // (x * y)
    C0 = u * n0**d // (x * y)
    if min(B0, C0) <= 0:
        raise AssertionError("nonpositive coefficient base")
    product = K * B0 * C0
    expected = Fraction(
        d * u * v * n0 ** (u + d) * r0 ** (v + d),
        (x * y) ** 3,
    )
    if product != expected:
        raise AssertionError("coefficient product identity failed")
    return {
        "d": d,
        "u": u,
        "v": v,
        "x": x,
        "y": y,
        "K": K,
        "B0": B0,
        "C0": C0,
        "product": product,
        "weight_squared": 1 / product,
    }


def split_sum(*, d: int, n0: int, r0: int) -> float:
    """Discovery-only floating evaluation of the exact algebraic split sum."""
    if d < 2 or min(n0, r0) <= 0 or gcd(n0, r0) != 1:
        raise ValueError("valid degree and reduced positive base required")
    return sum(
        sqrt(float(split_record(u=u, v=d - u, n0=n0, r0=r0)["weight_squared"]))
        for u in range(1, d)
        if gcd(u, d - u) == 1
    )


def finite_falsifier(*, max_degree: int, max_base: int) -> dict[str, Any]:
    if max_degree < 2 or max_base < 1:
        raise ValueError("invalid search box")
    maximum = -1.0
    witness = None
    rows = 0
    for d in range(2, max_degree + 1):
        for n0 in range(1, max_base + 1):
            for r0 in range(1, max_base + 1):
                if gcd(n0, r0) != 1:
                    continue
                value = split_sum(d=d, n0=n0, r0=r0)
                rows += 1
                if value > maximum:
                    maximum = value
                    witness = (d, n0, r0)
    return {"rows": rows, "maximum": maximum, "witness": witness, "threshold": 4.0}


def mode_bound(W: int) -> int:
    """Proved arithmetic split envelope across every degree d dividing W."""
    if W < 2:
        raise ValueError("mode magnitude at least two required")
    return 4 * divisor_count(W)


def theorem_record() -> dict[str, object]:
    return {
        "coefficient_product": (
            "K*B0*C0=d*u*v*n0^(u+d)*r0^(v+d)/(x*y)^3, "
            "x=gcd(u,r0^d), y=gcd(v,n0^d)"
        ),
        "split_weight": "J(u,v)=1/sqrt(K*B0*C0)",
        "uniform_split_sum": (
            "sum over primitive u+v=d of J(u,v) is less than 4, uniformly in d,n0,r0"
        ),
        "degree_aggregation": (
            "for a fixed mode W and its injective strong label, d divides W, so all "
            "perfect-power primitive splits have total normalized weight at most 4*tau(W)"
        ),
        "actual_scale": (
            "the actual-scale lattice contributes lambda0^(-3/2)<=1 before the summable ell ray"
        ),
        "boundary": (
            "the compact-chart/anchor prefactor and nonsmooth payload are not bounded here; "
            "large-degree irrational, weak, simple-root, moment, density, and interval claims remain open"
        ),
    }
