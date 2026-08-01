"""Pinned bookkeeping for the CRR capped spectral phase-lift reduction.

This module contains finite scale arithmetic only.  The accompanying note
proves the phase-lift/minimax identity in finite dimensions; this module does
not claim that an admissible CRR set exists, or that AFARI holds.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8
SCALE_EXPONENTS = {
    "local_height_H": 12,
    "polynomial_length_L": 10,
    "cardinality_R": 8,
    "large_value_V": 7,
}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    """Return the central CRR scales used by the spectral gate."""
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {
        "v": v,
        "H": v**SCALE_EXPONENTS["local_height_H"],
        "L": v**SCALE_EXPONENTS["polynomial_length_L"],
        "R": v**SCALE_EXPONENTS["cardinality_R"],
        "V": v**SCALE_EXPONENTS["large_value_V"],
    }
    require(result["R"] * result["V"] ** 2 == v**22, "central pointwise L2 scale mismatch")
    require(result["L"] * result["H"] == v**22, "central spectral L2 scale mismatch")
    return result


def support_rows(v: int) -> dict[str, int | str]:
    """Record the exact integer support count of the frozen smooth weight.

    At integer arguments, the frozen weight is positive exactly for
    ``L < n < 2L``.  The plateau is a smaller subset and is not used in the
    phase-lift theorem.
    """
    data = scales(v)
    L = data["L"]
    count = L - 1
    require(count > 0, "smooth support must be nonempty")
    return {
        "L": L,
        "nonzero_integer_support": "{n in Z: L<n<2L}",
        "support_count_N": count,
        "lower_bound": "N=L-1>=L/2",
    }


def exponent_rows() -> dict[str, tuple[Fraction, Fraction] | str]:
    """Return the affine-in-delta rows for the leading-phase sufficient gate.

    The parameters ell, r, s denote the losses in, respectively, the top
    eigenvalue, right-eigenvector delocalization, and row flatness.  The
    harmless factor ``(L-1)/L`` is kept outside exponent notation and is
    absorbed only after a strict delta-margin is supplied.
    """
    rows: dict[str, tuple[Fraction, Fraction] | str] = {
        "base_pointwise_square": (Fraction(14), Fraction(-2)),
        "leading_phase_square": "14-(ell+r+2s)*delta, up to (L-1)/L",
        "strict_closure_condition": "ell+r+2s<=2-gamma for fixed gamma>0",
        "central_top_eigenvalue": (Fraction(12), Fraction()),
        "central_support_over_cardinality": (Fraction(2), Fraction()),
    }
    require(rows["base_pointwise_square"] == (Fraction(14), Fraction(-2)), "Base square row mismatch")
    require(rows["central_top_eigenvalue"] == (Fraction(12), Fraction()), "spectral row mismatch")
    require(rows["central_support_over_cardinality"] == (Fraction(2), Fraction()), "support/cardinality row mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    """Run all exact finite checks required by the sealing builder."""
    data = scales(v)
    support = support_rows(v)
    rows = exponent_rows()
    require(support["support_count_N"] == data["L"] - 1, "support count mismatch")
    require(data["L"] * data["H"] == data["R"] * data["V"] ** 2, "critical spectral balance mismatch")
    return {"scales": data, "support": support, "exponents": rows}
