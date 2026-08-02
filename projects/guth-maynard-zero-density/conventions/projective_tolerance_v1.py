"""Cycle 116 projective gradient-to-Laurent tolerance ledger."""

from __future__ import annotations

from fractions import Fraction
from typing import Any


def tolerance_exponents(*, xi: Fraction, coefficient_height: Fraction = Fraction(0)) -> dict[str, Fraction]:
    D = Fraction(3, 5)
    Q = Fraction(1, 3)
    H = xi + Q - D
    gradient = -(D + H)  # 1/(c H0)=X^(-(D+H))=X^(-(xi+Q))
    laurent = Q + gradient
    energy_ceiling = 2 * D - xi
    mode_ceiling = D - xi / 2 - coefficient_height / 2
    return {
        "height": H,
        "gradient_tolerance": gradient,
        "laurent_tolerance": laurent,
        "energy_ceiling": energy_ceiling,
        "mode_ceiling": mode_ceiling,
    }


def theorem_record() -> dict[str, object]:
    return {
        "gradient_window": (
            "with H0~KQ/D and c=D/(2pi), a surviving smooth Poisson cell has |G1|+|G2|<<1/(cH0)<<1/(KQ)"
        ),
        "exact_elimination": (
            "A-B*g^u*exp(G1)-C*g^(u+v)*exp(G1+G2)=0"
        ),
        "laurent_tolerance": (
            "for small gradients and B,C<=Q, |A-Bg^u-Cg^(u+v)|<<1/K"
        ),
        "transition_energy": (
            "Cycle 115 then confines every weak transition to S2<<D^2/K"
        ),
        "mode_cap": (
            "if B,C are at least coefficient height Zc, max(|a|,|b|)<<D/sqrt(K*Zc)"
        ),
        "worst_exponent": (
            "for K>=X^(16/25) and Zc>=1, the weak-mode exponent is at most 3/5-8/25=7/25"
        ),
        "boundary": (
            "the reduced weak sector has not yet been summed with coefficient and simple-root weights; moment, density, and intervals remain open"
        ),
    }
