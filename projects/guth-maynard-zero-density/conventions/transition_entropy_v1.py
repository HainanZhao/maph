"""Cycle 134 unimodular shear entropy ledger."""

from __future__ import annotations

from fractions import Fraction


def shear_lift(p: int, q: int, p0: int, r0: int, t: int) -> tuple[int, int]:
    if p0 * q - p * r0 not in (-1, 1):
        raise ValueError("base lift is not unimodular")
    return p0 + t * p, r0 + t * q


def normalized_tail(alpha: Fraction, p: int, q: int, r: int) -> Fraction:
    delta = abs(alpha - Fraction(p, q))
    if delta == 0:
        raise ValueError("zero collision error")
    theta = (Fraction(1, 1) / (q * delta) - r) / q
    if not 0 < theta < 1:
        raise ValueError("outside consecutive shell")
    return theta


def recovered_error(q: int, r: int, theta: Fraction) -> Fraction:
    if not 0 < theta < 1:
        raise ValueError("tail outside (0,1)")
    return Fraction(1, q) / (r + theta * q)


def entropy_ledger(xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if rho > Fraction(1, 3) - mu:
        raise ValueError("rho above denominator ceiling")
    if tau < xi + Fraction(1, 3) - rho:
        raise ValueError("tau below next-denominator floor")
    return {
        "shear_entropy": tau - rho,
        "minimum_shear_entropy": xi + Fraction(1, 3) - 2 * rho,
        "full_endpoint_minimum": xi + 2 * mu - Fraction(1, 3),
    }


def theorem_record() -> dict[str, object]:
    return {
        "torsor": (
            "for fixed primitive (p,q) and orientation s, all solutions of "
            "Pq-pR=s are (P0+tp,R0+tq), t in Z"
        ),
        "dyadic_entropy": (
            "when q~N and R~S with S>>N, a nonempty interior dyadic block "
            "contains asymptotically S/N shear choices up to absolute constants"
        ),
        "endpoint_floor": (
            "the shear exponent tau-rho is at least xi+1/3-2rho; at the full "
            "endpoint it is xi+2mu-1/3>=23/75"
        ),
        "tail_coordinate": (
            "for delta=|alpha-p/q| in the next-convergent shell, "
            "theta=(1/(q delta)-R)/q lies in (0,1) and "
            "delta=1/[q(R+theta q)] exactly"
        ),
        "scoped_no_go": (
            "rational labels, determinant signs, and dyadic sizes alone leave "
            "power-sized shear entropy; subpower transition concentration in "
            "that data class must retain theta or an equivalent phase anchor"
        ),
        "boundary": (
            "this is not a no-go theorem for the phase-coupled operator and "
            "proves no transition concentration, seed, endpoint, moment, density, "
            "or prime-interval theorem"
        ),
    }
