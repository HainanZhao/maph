"""Cycle 156 exact norm convention for a sampled divisor comb."""

from __future__ import annotations

from fractions import Fraction


def divisor_comb_norm_majorant(*, frequency_length: int, modulus: int, anchor_ratio: Fraction) -> dict[str, Fraction | int]:
    """Count multiples in the inclusive integer interval [K, 2K]."""
    if frequency_length <= 0 or modulus <= 0 or anchor_ratio <= 0:
        raise ValueError("positive integer scales and anchor ratio required")
    if Fraction(modulus, frequency_length) > anchor_ratio:
        raise ValueError("frozen modulus-to-frequency bound fails")
    count = (2 * frequency_length) // modulus - ((frequency_length + modulus - 1) // modulus) + 1
    scale = Fraction(frequency_length, modulus)
    constant = 1 + anchor_ratio
    if Fraction(count) > constant * scale:
        raise ValueError("exact count exceeds fixed majorant")
    return {
        "multiple_count": count,
        "scale_without_q_squared": scale,
        "anchor_ratio": anchor_ratio,
        "norm_squared_majorant_constant": constant,
    }


def theorem_record() -> dict[str, object]:
    return {
        "exact_count": (
            "for w_h(k)=Q 1_(h|k) on integer K<=k<=2K, ||w_h||_2^2/Q^2 equals "
            "floor(2K/h)-ceil(K/h)+1"
        ),
        "fixed_majorant": (
            "if h<=C_h K for a frozen fixed C_h>0, the exact count is at most K/h+1 "
            "and hence ||w_h||_2^2<=(1+C_h)KQ^2/h"
        ),
        "special_case": "if h<=K, take C_h=1 and the fixed majorant constant is A=2",
        "cycle154_interface": (
            "this supplies the comb-norm hypothesis in Cycle 154; an actual finite labelled escape partition is still required before that cycle localizes a class"
        ),
        "boundary": (
            "this exact counting lemma concerns only the selected divisor comb; it does not prove an actual escape partition, negative projection, positive transport, bounded fan, moment, density, or intervals"
        ),
    }
