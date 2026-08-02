"""Cycle 135 exact tail tiling and paired-edge identities."""

from __future__ import annotations

from fractions import Fraction


def shell_interval(r: int, q: int, t: int) -> tuple[Fraction, Fraction]:
    if q <= 0:
        raise ValueError("q must be positive")
    left = Fraction(r + t * q, 1)
    return left, left + q


def tiled_interval(r: int, q: int, t0: int, t1: int) -> tuple[Fraction, Fraction]:
    if t1 <= t0:
        raise ValueError("empty shear block")
    return Fraction(r + t0 * q, 1), Fraction(r + t1 * q, 1)


def shell_memberships(y: Fraction, r: int, q: int, t0: int, t1: int) -> tuple[int, ...]:
    return tuple(t for t in range(t0, t1) if shell_interval(r, q, t)[0] < y < shell_interval(r, q, t)[1])


def tail_term(q: int, r: int, theta: Fraction, sign: int) -> Fraction:
    if q <= 0 or r <= 0 or sign not in (-1, 1) or not 0 < theta < 1:
        raise ValueError("invalid tail data")
    return Fraction(sign, q) / (r + theta * q)


def rational_center(p: int, q: int) -> Fraction:
    if q <= 0:
        raise ValueError("q must be positive")
    return Fraction(p, q)


def paired_edge_residual(
    g_to_d: Fraction,
    left: tuple[int, int, int, int, Fraction],
    right: tuple[int, int, int, int, Fraction],
) -> Fraction:
    """Return x_right-g^d*x_left from the two exact signed tails.

    Tuples are ``(p,q,R,sign,theta)``.
    """
    p, q, r, sign, theta = left
    pp, qq, rr, signp, thetap = right
    lhs = rational_center(pp, qq) - g_to_d * rational_center(p, q)
    rhs = g_to_d * tail_term(q, r, theta, sign) - tail_term(qq, rr, thetap, signp)
    if lhs != rhs:
        raise ValueError("edge data do not satisfy the exact phase identity")
    return rhs


def frequency_ledger(xi: Fraction, mu: Fraction, rho: Fraction, tau: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= (1 - xi) / 4:
        raise ValueError("mu outside low-multiplicity range")
    if tau < xi + Fraction(1, 3) - rho:
        raise ValueError("tau below next-denominator floor")
    return {
        "normalized_residual_scale": rho + tau,
        "tail_variation": rho - tau,
        "tail_frequency": tau - rho,
        "raw_residual_frequency": 2 * tau,
        "minimum_full_endpoint_tail_frequency": xi + 2 * mu - Fraction(1, 3),
    }


def theorem_record() -> dict[str, object]:
    return {
        "tail_tiling": (
            "with Y=1/(q|alpha-p/q|) and R=r+tq, the conditions "
            "R<Y<R+q tile exactly over consecutive t; a complete shear block "
            "is one interval with only its two outer boundaries"
        ),
        "marginal_no_gain": (
            "Fourier projection in theta alone therefore cancels only internal "
            "shear boundaries and reproduces the Cycle-132 logarithmic-center "
            "discrepancy; it yields no independent transition-entropy saving"
        ),
        "edge_identity": (
            "for b=a+d, x_b-g^d x_a equals g^d*s_a/[q_a(R_a+theta_a q_a)] "
            "minus s_b/[q_b(R_b+theta_b q_b)] exactly"
        ),
        "frequency_scale": (
            "after normalizing the edge residual by NS, theta changes it on "
            "scale N/S; resolving the tail requires frequency L=S/N, "
            "equivalently raw residual frequency S^2"
        ),
        "paired_norm": (
            "the next proof target is the fixed-difference diagonal estimate "
            "sum_{|ell|<=L}|sum_{a in E_d} w_a e(ell Omega_d(a))|^2 "
            "<< L|E_d|X^epsilon, where Omega_d=NS(x_{a+d}-g^d x_a) and L=S/N"
        ),
        "boundary": (
            "the paired-tail norm is not proved; no transition concentration, "
            "seed, endpoint, moment, density, or prime-interval theorem follows"
        ),
    }
