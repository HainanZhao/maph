"""Cycle 113 weighted aggregation for general reduced critical labels."""

from __future__ import annotations

from fractions import Fraction
from math import gcd, sqrt
from typing import Any


def split_record(*, d: int, u: int, N: int, R: int) -> dict[str, Any]:
    if d < 2 or not 1 <= u < d or min(N, R) <= 0:
        raise ValueError("invalid split data")
    v = d - u
    if gcd(u, v) != 1 or gcd(N, R) != 1:
        raise ValueError("primitive split and reduced label required")
    x, y = gcd(u, R), gcd(v, N)
    B0 = v * R // (x * y)
    C0 = u * N // (x * y)
    # Store K^d and (K B0 C0)^d exactly; K itself need not be rational.
    K_power = Fraction(d**d * R ** (d - u) * N**u, (x * y) ** d)
    product_power = K_power * (B0 * C0) ** d
    expected = Fraction(
        (d * u * v) ** d * N ** (d + u) * R ** (2 * d - u),
        (x * y) ** (3 * d),
    )
    if product_power != expected:
        raise AssertionError("general coefficient product identity failed")
    return {
        "d": d, "u": u, "v": v, "N": N, "R": R, "x": x, "y": y,
        "B0": B0, "C0": C0, "K_power": K_power,
        "product_power": product_power,
    }


def floating_split_sum(*, d: int, N: int, R: int) -> float:
    if gcd(N, R) != 1:
        raise ValueError("reduced label required")
    total = 0.0
    ratio = N / R
    for u in range(1, d):
        v = d - u
        if gcd(u, v) != 1:
            continue
        x, y = gcd(u, R), gcd(v, N)
        K = d * R / (x * y) * ratio ** (u / d)
        B0, C0 = v * R / (x * y), u * N / (x * y)
        total += 1 / sqrt(K * B0 * C0)
    return total


def theorem_record() -> dict[str, object]:
    return {
        "product": (
            "(K B0 C0)^d=(d*u*v)^d*N^(d+u)*R^(2d-u)/(x*y)^(3d)"
        ),
        "compact_weight": (
            "when N/R is in a fixed compact positive interval and Z=min(N,R), "
            "J is comparable to (xy)^(3/2)/(Z^(3/2)*sqrt(d*u*v))"
        ),
        "small_height": (
            "if Z<=d^(1/3), x,y<=Z and the full split sum is O_L(Z^(3/2)/sqrt(d))=O_L(1)"
        ),
        "large_height": (
            "if Z>=d^(1/3), dyadically freeze u,v and exact divisors x|R,y|N; "
            "the congruence pair has at most 1+d/(xy) solutions and each divisor-pair cell is O_L(1)"
        ),
        "split_sum": (
            "sum over primitive u+v=d of (K B0 C0)^(-1/2) is (d*N*R)^o(1) uniformly on the compact ratio chart"
        ),
        "scale_sum": (
            "writing lambda=lambda_BC*ell and E for the first supported ell, absolute summation costs at most "
            "3*p0*sqrt(q0)/(lambda_BC^(3/2)*sqrt(E)) times 1/sqrt(K B0 C0)"
        ),
        "correction": (
            "Cycle 112's pointwise anchor absorption does not control this summed tail; its X^(3/5+o(1)) aggregate promotion is withheld"
        ),
        "aggregate": (
            "the split entropy is subpower, but the coupled anchor-scale-label factor remains open"
        ),
        "boundary": (
            "anchor-scale aggregation, weak localization, simple roots, nonsmooth payload variants, the complete moment, density, and intervals remain open"
        ),
    }
