"""Exact mass ledgers for Cycle 162's dyadic high-cell extraction."""
from __future__ import annotations
from fractions import Fraction

B = 288

def low_codegree_mass_upper(*, threshold: Fraction, total_square_mass: Fraction) -> Fraction:
    if threshold < 0 or total_square_mass < 0:
        raise ValueError("nonnegative inputs required")
    return threshold * total_square_mass

def refined_high_l1_square_lower(parent_l1_square: Fraction) -> Fraction:
    if parent_l1_square < 0:
        raise ValueError("mass must be nonnegative")
    return parent_l1_square / (2 * B)

def oriented_star_square_lower(*, certificate_l1_square: Fraction, tau: Fraction) -> Fraction:
    if certificate_l1_square < 0 or tau < 0:
        raise ValueError("nonnegative inputs required")
    return tau * tau * certificate_l1_square / 4

def theorem_record() -> dict[str, object]:
    return {
        "mass_sensitive_extraction": "conditional Cycle-89 excess and Cycle-160 local Schur force sum_I L_I^2 >> A2^2 X^(1/75-o(1)); one high dyadic level retains that scale",
        "refinement_retention": "for B=288, sum_j L_(I,j)^2>=L_I^2/B; high refined classes retain at least L_I^2/(2B)",
        "aggregate_dichotomy": "four-atom mass is >>_B A2^2 X^(1/75-o(1)); star squared edge mass is >>_B A2^2 X^(1/150-o(1)) with degree X^(1/300-o(1))",
        "boundary": "this conditional extraction does not prove Cycle-89 excess, a coordinate pullback, rational web, moment bound, density, or intervals",
    }
