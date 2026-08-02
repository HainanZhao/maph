"""Cycle 138 multiplier-fiber height descent ledger."""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def cancellation_divisor(a: int, b: int, p: int, q: int) -> int:
    if min(a, b, p, q) <= 0 or gcd(a, b) != 1 or gcd(p, q) != 1:
        raise ValueError("inputs must be positive primitive pairs")
    return gcd(a * p, b * q)


def split_cancellation_divisor(a: int, b: int, p: int, q: int) -> int:
    return gcd(a, q) * gcd(b, p)


def closure_ledger(xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if tau <= 3 * rho:
        raise ValueError("outside strict exact region")
    target = Fraction(2, 3) - 2 * mu
    discretization = 4 * rho
    volume = Fraction(3, 5) + 6 * rho - 2 * tau
    hs = Fraction(7, 45) - 2 * mu / 3
    ceiling = Fraction(1, 6) - mu / 2
    return {
        "weighted_discretization": discretization,
        "weighted_volume": volume,
        "edge_weight_target": target,
        "discretization_margin": target - discretization,
        "volume_margin": target - volume,
        "rho_ceiling": ceiling,
        "extension_beyond_hs": ceiling - hs,
        "volume_gap_condition": tau - 3 * rho - mu + Fraction(1, 30),
    }


def theorem_record() -> dict[str, object]:
    return {
        "cancellation_identity": (
            "for coprime A,B and coprime p,q, "
            "gcd(Ap,Bq)=gcd(A,q)gcd(B,p)"
        ),
        "fiber_bound": (
            "if A/B has compact height H and both p/q and (A/B)(p/q) have "
            "compact height N, divisor-class summation gives at most "
            "N^2 H^{-1}X^epsilon possible primitive p/q"
        ),
        "height_descent": (
            "an edge class |E_d|~J therefore forces height(r_d) "
            "<<N^2 J^{-1}X^epsilon"
        ),
        "weighted_count": (
            "the exceptional count becomes "
            "B_exc<<X^epsilon(N^4/J^2+D N^6/(J^2 S^2)); after multiplying "
            "by J^2 the edge multiplicity cancels exactly"
        ),
        "closure_region": (
            "all edge multiplicities meet the exceptional-average diagonal "
            "budget when rho<1/6-mu/2 and tau-3rho>mu-1/30"
        ),
        "regional_width": (
            "the rho ceiling exceeds 7/45-2mu/3 by 1/90+mu/6>=1/90"
        ),
        "boundary": (
            "this closes only the exceptional-multiplier weighted average in "
            "the stated region; no full paired norm, endpoint, moment, density, "
            "or prime-interval theorem is proved"
        ),
    }
