"""Cycle 114 coupled anchor, scale-window, and label aggregation."""

from __future__ import annotations

from math import gcd
from typing import Any


def euler_phi(n: int) -> int:
    if n < 1:
        raise ValueError("positive integer required")
    return sum(gcd(k, n) == 1 for k in range(1, n + 1))


def gcd_convolution_sum(*, d: int, N: int, R: int) -> int:
    if d < 2 or min(N, R) <= 0 or gcd(N, R) != 1:
        raise ValueError("valid degree and reduced label required")
    return sum(gcd(u, R) * gcd(d - u, N) for u in range(1, d))


def gcd_convolution_expansion(*, d: int, N: int, R: int) -> int:
    total = 0
    for a in range(1, R + 1):
        if R % a:
            continue
        for b in range(1, N + 1):
            if N % b:
                continue
            count = sum(u % a == 0 and (d - u) % b == 0 for u in range(1, d))
            total += euler_phi(a) * euler_phi(b) * count
    return total


def anchor_height_bound(*, Q: int, support_n_prime: int, support_m: int, B: int, C: int, p0: int, q0: int) -> bool:
    if min(Q, support_n_prime, support_m, B, C, p0, q0) <= 0 or gcd(p0, q0) != 1:
        raise ValueError("positive support data required")
    if B != p0 * support_n_prime or C != q0 * support_m or max(B, C) > Q:
        return False
    return p0 <= Q // support_n_prime and q0 <= Q // support_m


def theorem_record() -> dict[str, object]:
    return {
        "anchor_bound": (
            "B=p0*n'<=Q and C=q0*m<=Q with n',m>=aQ imply p0,q0<=1/a"
        ),
        "coefficient_comparability": (
            "simultaneous support and a small near-hit make K,B0,C0 comparable to Zc=Q/lambda"
        ),
        "scale_window": (
            "a fixed core has O(Q/Zc) supported scales, each full coefficient kernel is O(Q^(-3/2)), so its scale sum is O(1/(sqrt(Q)*Zc))"
        ),
        "split_reduction": (
            "support comparability forces u,v comparable to d and Zc comparable to d*Z/(x*y), reducing the split sum to sum gcd(u,R)gcd(d-u,N)/(d*Z*sqrt(Q))"
        ),
        "gcd_identity": (
            "sum_u gcd(u,R)gcd(d-u,N) expands with phi(a)phi(b) over a|R,b|N and at most 1+d/(ab) solutions"
        ),
        "gcd_bound": (
            "splitting at Z=min(N,R)<=d or >=d bounds the gcd sum by d*Z*(d*N*R)^o(1)"
        ),
        "aggregate": (
            "all degrees at one strong mode cost Q^(-1/2)*X^o(1); summing |w|<=2M gives M*Q^(-1/2)*X^o(1)=X^(13/30+o(1)) after the common analytic chart factor"
        ),
        "boundary": (
            "weak localization, simple roots, nonsmooth payload variants, full moment assembly, density, and intervals remain open"
        ),
    }
