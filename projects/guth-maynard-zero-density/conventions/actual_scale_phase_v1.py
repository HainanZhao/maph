"""Cycle 107 actual scale lattice and geometric stationary phase."""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from math import gcd, lcm
from typing import Any

import sympy as sp


def nearest_integer_distance(value: Fraction) -> Fraction:
    floor_value = value.numerator // value.denominator
    return min(value - floor_value, floor_value + 1 - value)


@dataclass(frozen=True)
class ActualScaleLattice:
    A0: int
    S0: int
    B0: int
    C0: int
    p0: int
    q0: int

    def __post_init__(self) -> None:
        if min(self.A0, self.S0, self.B0, self.C0, self.p0, self.q0) <= 0:
            raise ValueError("positive scale and anchor data required")
        if gcd(self.A0, self.S0) != 1 or gcd(self.p0, self.q0) != 1:
            raise ValueError("K and c0 must be reduced")

    @property
    def lambda0(self) -> int:
        return lcm(
            self.S0 * self.p0 // gcd(self.p0, self.A0),
            self.p0 // gcd(self.p0, self.B0),
            self.q0 // gcd(self.q0, self.C0),
        )

    def actual(self, scale: int) -> bool:
        if scale <= 0:
            return False
        A = Fraction(scale * self.A0, self.S0)
        return (
            A.denominator == 1
            and A.numerator % self.p0 == 0
            and scale * self.B0 % self.p0 == 0
            and scale * self.C0 % self.q0 == 0
        )

    @property
    def base_indices(self) -> tuple[int, int, int]:
        scale = self.lambda0
        if not self.actual(scale):
            raise AssertionError("lambda0 is not admissible")
        n = scale * self.A0 // (self.S0 * self.p0)
        n_prime = scale * self.B0 // self.p0
        m = scale * self.C0 // self.q0
        return n, n_prime, m

    def verify_range(self, limit: int) -> None:
        if limit < 1:
            raise ValueError("positive verification limit required")
        expected = tuple(range(self.lambda0, limit + 1, self.lambda0))
        actual = tuple(scale for scale in range(1, limit + 1) if self.actual(scale))
        if actual != expected:
            raise AssertionError("actual scale lattice mismatch")


def symbolic_phase_homogeneity() -> dict[str, Any]:
    ell, H, Delta, m, n, n_prime, c0, c, mu, nu = sp.symbols(
        "ell H Delta m n n_prime c0 c mu nu", positive=True
    )

    def entropy(Hv: sp.Expr, Dv: sp.Expr, mv: sp.Expr, nv: sp.Expr, npv: sp.Expr) -> sp.Expr:
        return (
            Dv * sp.log(sp.cancel(c0 * Dv / mv))
            - Hv * sp.log(sp.cancel(Hv / nv))
            + (Hv - Dv) * sp.log(sp.cancel((Hv - Dv) / npv))
        )

    base = entropy(H, Delta, m, n, n_prime)
    scaled = entropy(ell * H, ell * Delta, ell * m, ell * n, ell * n_prime)
    if sp.simplify(scaled - ell * base) != 0:
        raise AssertionError("entropy phase is not homogeneous")
    full_base = c * base - mu * H - nu * Delta
    full_scaled = c * scaled - mu * ell * H - nu * ell * Delta
    if sp.simplify(full_scaled - ell * full_base) != 0:
        raise AssertionError("full phase is not homogeneous")

    stationary_h = sp.cancel((H - Delta) * n / (H * n_prime))
    stationary_delta = sp.cancel(c0 * Delta * n_prime / (m * (H - Delta)))
    scaled_h = sp.cancel(
        ((ell * H - ell * Delta) * ell * n) / (ell * H * ell * n_prime)
    )
    scaled_delta = sp.cancel(
        c0 * ell * Delta * ell * n_prime / (ell * m * (ell * H - ell * Delta))
    )
    if sp.simplify(stationary_h - scaled_h) != 0:
        raise AssertionError("H stationary ratio changed")
    if sp.simplify(stationary_delta - scaled_delta) != 0:
        raise AssertionError("Delta stationary ratio changed")
    return {
        "entropy": "F(ell*H,ell*Delta;ell*m,ell*n,ell*n')=ell*F(H,Delta;m,n,n')",
        "full_phase": "Phi_ell=ell*Phi0 for fixed c,mu,nu",
        "stationary_ratios": "both exponentiated stationary equations are scale invariant",
    }


def geometric_factor(phase: Fraction, length: int) -> Fraction:
    if length < 1:
        raise ValueError("positive sum length required")
    distance = nearest_integer_distance(phase)
    if distance == 0:
        return Fraction(length)
    return min(Fraction(length), Fraction(1, 2) / distance)


def bounded_variation_bound(
    *, phase: Fraction, length: int, terminal_abs: Fraction, variation: Fraction
) -> Fraction:
    if terminal_abs < 0 or variation < 0:
        raise ValueError("nonnegative BV data required")
    return geometric_factor(phase, length) * (terminal_abs + variation)


def exact_root_of_unity_sum(numerator: int, denominator: int, length: int) -> sp.Expr:
    if denominator <= 0 or length < 1:
        raise ValueError("positive denominator and length required")
    order = denominator // gcd(numerator, denominator)
    if order == 1:
        return sp.Integer(length)
    if length % order == 0:
        return sp.Integer(0)
    z = sp.exp(2 * sp.pi * sp.I * sp.Rational(numerator, denominator))
    return sp.simplify(sum(z**ell for ell in range(1, length + 1)))


def theorem_record() -> dict[str, object]:
    return {
        "lambda0": (
            "lcm(S0*p0/gcd(p0,A0), p0/gcd(p0,B0), q0/gcd(q0,C0))"
        ),
        "base_indices": (
            "n0=lambda0*A0/(S0*p0), n0'=lambda0*B0/p0, m0=lambda0*C0/q0"
        ),
        "stationary_scaling": (
            "(H0,Delta0;n0,n0',m0) scales to ell times every coordinate"
        ),
        "phase": "Phi_ell=ell*Phi0 exactly",
        "geometric_bound": (
            "|sum_{ell<=L}e(ell*Phi0)|<=min(L,1/(2*||Phi0||))"
        ),
        "weighted_bound": (
            "multiply the geometric factor by |a_L|+sum_{ell<L}|a_ell-a_(ell+1)|"
        ),
        "inverse": (
            "lack of cancellation forces near-integral Phi0 and retains c0,beta,modes,base indices,and stationary coordinates"
        ),
        "boundary": (
            "actual amplitude variation and conversion of phase resonance to a Cycle-67 seed remain open"
        ),
    }
