"""Cycle 136 common-multiplier large-sieve and jump ledger."""

from __future__ import annotations

from fractions import Fraction


def scalar_ledger(xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if tau <= 3 * rho:
        raise ValueError("outside strict exact-multiplier region")
    return {
        "tail_frequency": tau - rho,
        "kappa_exception_threshold": 3 * rho - tau,
        "rational_error_threshold": 2 * rho - 2 * tau,
        "legendre_margin": 2 * tau - 6 * rho,
        "next_denominator_floor": 2 * tau - 4 * rho,
        "next_partial_quotient_floor": 2 * tau - 6 * rho,
        "multiplier_height": 2 * rho,
    }


def common_multiplier(xa: Fraction, xb: Fraction, xc: Fraction, xd: Fraction) -> Fraction:
    """Return the common edge multiplier from xb*xc=xd*xa."""
    if xa == 0 or xc == 0 or xb * xc != xd * xa:
        raise ValueError("not an exact multiplicative rectangle")
    left = xb / xa
    right = xd / xc
    if left != right:
        raise RuntimeError("rectangle identity failed")
    return left


def theorem_record() -> dict[str, object]:
    return {
        "common_multiplier": (
            "in the exact Cycle-133 region, the rectangle "
            "(a+d)+c=(c+d)+a gives x_{a+d}/x_a=x_{c+d}/x_c; "
            "hence one reduced rational r_d serves every edge of difference d"
        ),
        "residual_factorization": (
            "the paired residual factors exactly as "
            "x_{a+d}-g^d x_a=(r_d-g^d)x_a"
        ),
        "large_sieve": (
            "with kappa_d=NS(r_d-g^d), L=S/N, and distinct rational labels "
            "separated by >>N^{-2}, the paired second moment is "
            "<<(L+N^2/|kappa_d|)|E_d| up to X^epsilon"
        ),
        "scalar_dichotomy": (
            "the diagonal target follows unless |kappa_d|<<N^3/S; "
            "an exceptional multiplier satisfies |r_d-g^d|<<N^2/S^2"
        ),
        "continued_fraction": (
            "r_d has reduced denominator <<N^2; when S>>N^3 the exceptional "
            "bound satisfies Legendre with margin S^2/N^6, so r_d is a "
            "convergent of g^d"
        ),
        "jump": (
            "the next convergent denominator is >>S^2/N^4 and the next "
            "partial quotient is >>S^2/N^6"
        ),
        "boundary": (
            "no averaged exclusion of exceptional r_d, full paired norm, "
            "endpoint, moment, density, or prime-interval theorem is proved"
        ),
    }
