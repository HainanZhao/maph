"""Cycle 117 weighted weak-sector exponent ledger."""

from __future__ import annotations

from fractions import Fraction


def exponent_ledger(xi: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    coefficient_diagonal = Fraction(1, 6)
    energy_term = Fraction(31, 30) - xi
    return {
        "coefficient_diagonal": coefficient_diagonal,
        "energy_term": energy_term,
        "weak_total": max(coefficient_diagonal, energy_term),
        "strong_benchmark": Fraction(13, 30),
        "margin": Fraction(13, 30) - max(coefficient_diagonal, energy_term),
    }


def theorem_record() -> dict[str, object]:
    return {
        "coefficient_support": "bounded p0,q0 and n',m~Q force B,C~Q",
        "mode_count": (
            "Ba^2+Cb^2<<D^2/K contains O(1+D^2/(K*sqrt(B*C)))=O(1+D^2/(KQ)) integer mode pairs"
        ),
        "A_uniqueness": (
            "for fixed B,C,a,b, the interval |A-Bg^a-Cg^b|<<1/K has length below one, so at most one integer A"
        ),
        "weighted_sum": (
            "Q^2 coefficient pairs times Q^(-3/2) kernel times (1+D^2/(KQ)) gives Q^(1/2)+D^2/(K Q^(1/2))"
        ),
        "exponent": (
            "max(1/6,31/30-xi)<=59/150 for xi>=16/25, a 1/25 margin below 13/30"
        ),
        "boundary": (
            "registered smooth weak turnover is closed; simple-root averages, nonsmooth payload variants, full moment assembly, density, and intervals remain open"
        ),
    }
