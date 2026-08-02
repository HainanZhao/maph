"""Cycle 151 lcm resonance and tail-transform ledger."""

from __future__ import annotations

from fractions import Fraction
from math import gcd


def resonance_modulus(witness_denominator: int, mode_denominator: int) -> dict[str, int]:
    if witness_denominator <= 0 or mode_denominator <= 0:
        raise ValueError("positive denominators required")
    common = gcd(witness_denominator, mode_denominator)
    return {
        "gcd": common,
        "lcm": witness_denominator * mode_denominator // common,
        "coefficient_congruence": mode_denominator // common,
    }


def relative_mode_capacity(witness_denominator: int, mode_denominator: int) -> Fraction:
    row = resonance_modulus(witness_denominator, mode_denominator)
    return Fraction(row["gcd"], mode_denominator)


def exponent_ledger(
    *, xi: Fraction, rho: Fraction, rho_b: Fraction, gamma: Fraction
) -> dict[str, Fraction]:
    if min(rho, rho_b, gamma) < 0 or gamma > min(rho, rho_b):
        raise ValueError("invalid gcd exponents")
    lcm = rho + rho_b - gamma
    return {
        "lcm": lcm,
        "resonance_exists_margin": xi - lcm,
        "per_mode_correlation": xi + Fraction(2, 3) - lcm,
        "relative_to_witness": gamma - rho_b,
    }


def theorem_record() -> dict[str, object]:
    return {
        "lcm_lattice": (
            "on k=h ell, the rational phase of a reduced r_b/h_b is integral "
            "exactly when lcm(h,h_b) divides k; the lcm is hh_b/gcd(h,h_b)"
        ),
        "nonresonant_removal": (
            "for h_b<=QX^(-delta), every nonmultiple of h_b is power-negligible "
            "by the Cycle-148 exact Poisson estimate"
        ),
        "tail_transform": (
            "if L_b=lcm(h,h_b)<=cK and tau_b=KQ epsilon_b is bounded, the "
            "sampled correlation equals KQ^2/L_b times the fixed transform "
            "B(tau_b)=int int U(x)V(y)e(tau_bxy)dxdy, up to relative "
            "O(L_b/K+1/Q) from smooth Riemann summation"
        ),
        "empty_lattice": (
            "if lcm(h,h_b) exceeds the upper frequency support, no common "
            "rational resonance exists and the strict-denominator contribution "
            "is power-negligible"
        ),
        "gcd_capacity": (
            "relative to the one-witness scale KQ^2/h, one halo mode has "
            "capacity gcd(h,h_b)/h_b; target negative mass therefore forces "
            "a weighted sum of these gcd ratios of order one"
        ),
        "negative_lobe": (
            "positive mode weights can contribute negative correlation only when "
            "Re B(tau_b) is negative beyond the explicit O(L_b/K+1/Q) error; "
            "the strict tau neighborhood is positive by Cycle 147"
        ),
        "boundary_denominator": (
            "when h_b lies within a fixed power of Q, nonmultiple Poisson decay "
            "is not power-saving and the formula is not asserted"
        ),
        "structural_implication": (
            "a smooth halo anti-aligner must simultaneously have lcm(h,h_b)<=K, "
            "large aggregate gcd capacity, and tail parameters in negative lobes"
        ),
        "boundary": (
            "the weighted gcd/negative-lobe population and boundary denominators "
            "are not bounded here; no full second moment, endpoint, density, or intervals is proved"
        ),
    }
