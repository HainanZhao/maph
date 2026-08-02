"""Cycle 129 continued-fraction jump exponent ledger."""

from __future__ import annotations

from fractions import Fraction


def jump_ledger(xi: Fraction, mu: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    if not 0 <= mu <= Fraction(1, 3):
        raise ValueError("mu outside multiplicity range")
    jump = xi + 2 * mu - Fraction(1, 3)
    return {
        "legendre_margin": jump,
        "next_denominator_floor": xi + mu,
        "next_partial_quotient_floor": jump,
        "occupied_mode_target": Fraction(1, 3) - mu,
    }


def theorem_record() -> dict[str, object]:
    return {
        "collision_input": (
            "for alpha=g^a, a reduced collision label p/q satisfies "
            "|alpha-p/q|<<1/(KQ) and q<<Q/M"
        ),
        "legendre": (
            "2q^2|alpha-p/q|<<Q/(KM^2)=X^(-(xi+2mu-1/3)); "
            "the minimum margin is 23/75, so Legendre's criterion makes p/q "
            "a continued-fraction convergent uniformly"
        ),
        "convergent_error": (
            "for consecutive convergent denominators q,q_next, "
            "|alpha-p/q|>1/[q(q+q_next)]"
        ),
        "next_denominator": (
            "q_next>1/(q|alpha-p/q|)-q>>KM; the subtraction is absorbed by "
            "the same positive Legendre margin"
        ),
        "partial_quotient": (
            "q_next=A_next q+q_previous forces A_next>>KM^2/Q, with "
            "X-exponent xi+2mu-1/3>=23/75"
        ),
        "averaged_target": (
            "for every dyadic M, it suffices to show that at most "
            "O((Q/M)X^epsilon) modes a have a convergent q<<Q/M whose next "
            "partial quotient is >>KM^2/Q"
        ),
        "boundary": (
            "no averaged large-partial-quotient theorem, collision or simple-root "
            "closure, complete moment, density, or prime intervals is proved"
        ),
    }
