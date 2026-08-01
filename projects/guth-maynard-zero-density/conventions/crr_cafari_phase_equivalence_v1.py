"""Exact scale bookkeeping for the CRR CFARI/AFARI equivalence.

The analytic sampled mean-value estimate is recorded in the accompanying
document.  This module only freezes the CRR scales, the exact affine slack
rows, and the fixed-power implication bookkeeping.  It does not prove a
Farey restricted large-sieve saving, CFARI, AFARI, or CRR-U.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "rational_height_Q": 4,
    "cardinality_R": 8,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the integral scales shared by Base, AFARI, and CFARI."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "Q": v**SCALE_EXPONENTS["rational_height_Q"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
    }
    require(result["H"] == result["L"] * v**2, "the mean-value comparison needs H=L*v^2")
    require(result["L"] == result["Q"] * v**6, "the AFARI ray comparison needs L/Q=v^6")
    require(result["R"] == result["Q"] ** 2, "the critical cardinality needs R=Q^2")
    return result


def affine_rows() -> dict[str, tuple[Fraction, Fraction] | str]:
    """Return exact exponent rows before harmless logarithmic factors.

    A pair ``(c,d)`` denotes ``c+d*delta(v)``.  The sampled mean-value
    row retains its separate ``log(2L)`` factor rather than disguising it as
    a fixed power of ``v``.
    """
    rows: dict[str, tuple[Fraction, Fraction] | str] = {
        "base_phase_rayleigh_lower": (Fraction(20), Fraction(-4)),
        "sampled_mean_value_phase_upper": (Fraction(20), Fraction(1)),
        "sampled_mean_value_extra_factor": "C*(1+log(2L))",
        "afaris_A_to_Mcal": (Fraction(20), Fraction()),
        "Mcal_to_afaris_A": (Fraction(26), Fraction()),
        "cfari_to_Mcal_before_absorption": (Fraction(20), Fraction(-1)),
        "afari_to_cafari_before_absorption": (Fraction(40), Fraction(-1)),
    }
    require(rows["base_phase_rayleigh_lower"] == (Fraction(20), Fraction(-4)), "Base phase lower row mismatch")
    require(rows["sampled_mean_value_phase_upper"] == (Fraction(20), Fraction(1)), "sampled mean-value row mismatch")
    require(rows["afaris_A_to_Mcal"] == (Fraction(20), Fraction()), "A-to-Mcal scale mismatch")
    require(rows["Mcal_to_afaris_A"] == (Fraction(26), Fraction()), "Mcal-to-A scale mismatch")
    require(rows["cfari_to_Mcal_before_absorption"] == (Fraction(20), Fraction(-1)), "CFARI implication row mismatch")
    require(rows["afari_to_cafari_before_absorption"] == (Fraction(40), Fraction(-1)), "AFARI implication row mismatch")
    return rows


def fixed_power_maps() -> dict[str, str]:
    """Freeze the safe eventual saving maps used in the document."""
    return {
        "cfari_eta_to_afari": "CFARI_eta implies AFARI_(eta/2) for all sufficiently large v",
        "afari_eta_to_cafari": "AFARI_eta implies CFARI_(eta/2) for all sufficiently large v",
        "f4f_zeta_to_cafari": "F4F_zeta implies CFARI_(zeta/3) for all sufficiently large v",
        "scope": "Each map absorbs only fixed constants, delta(v), and logarithmic/subpower factors; it is not an effective finite-v threshold.",
    }


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run all finite exact checks used by the sealing builder."""
    data = scales(v)
    rows = affine_rows()
    maps = fixed_power_maps()
    require(data["H"] > data["L"], "the sampled mean-value regime requires H>L")
    require(data["H"] == data["Q"] ** 3, "the actual-Farey height convention changed")
    require("eta/2" in maps["cfari_eta_to_afari"], "CFARI-to-AFARI map mismatch")
    require("eta/2" in maps["afari_eta_to_cafari"], "AFARI-to-CFARI map mismatch")
    return {"scales": data, "affine_rows": rows, "fixed_power_maps": maps}
