"""Cycle 157 Hermitian selection-mask spectral conventions."""

from __future__ import annotations

from fractions import Fraction
from typing import Sequence


def spectral_ledger(
    *, eigenvalues: Sequence[Fraction], coefficient_projection_squares: Sequence[Fraction], external_weight: Fraction
) -> dict[str, Fraction]:
    """Exact diagonal spectral bookkeeping for q*c^*H*c."""
    if len(eigenvalues) != len(coefficient_projection_squares) or external_weight < 0:
        raise ValueError("matched spectral rows and nonnegative external weight required")
    if any(value < 0 for value in coefficient_projection_squares):
        raise ValueError("squared coefficient projections must be nonnegative")
    positive = sum(
        (external_weight * max(value, Fraction()) * overlap
         for value, overlap in zip(eigenvalues, coefficient_projection_squares)),
        Fraction(),
    )
    negative = sum(
        (external_weight * max(-value, Fraction()) * overlap
         for value, overlap in zip(eigenvalues, coefficient_projection_squares)),
        Fraction(),
    )
    return {
        "real_hermitian_correlation": positive - negative,
        "positive_spectral_energy": positive,
        "negative_spectral_energy": negative,
    }


def negative_energy_localization(rows: Sequence[dict[str, Fraction]], target: Fraction) -> dict[str, Fraction | int]:
    """Check that a negative aggregate is retained by negative spectral energy."""
    if target <= 0 or not rows:
        raise ValueError("positive target and nonempty labelled rows required")
    total_real = sum((row["real_hermitian_correlation"] for row in rows), Fraction())
    total_negative = sum((row["negative_spectral_energy"] for row in rows), Fraction())
    if -total_real < target:
        raise ValueError("aggregate negative correlation premise fails")
    if total_negative < target:
        raise ValueError("negative spectral energy premise fails")
    return {
        "block_count": len(rows),
        "aggregate_negative_correlation": -total_real,
        "negative_spectral_energy": total_negative,
    }


def theorem_record() -> dict[str, object]:
    return {
        "hermitianization": (
            "for a fixed nonzero d, K^(d)(a,a')=chi(a,d,ell)1_(a'=a+d) and H^(d)=(K^(d)+K^(d)* )/2, "
            "c^*H^(d)c equals Re(c^*K^(d)c); "
            "there is no extra factor of two in this convention"
        ),
        "zero_diagonal_obstruction": (
            "for fixed nonzero difference, a nonzero Hermitian raw selection mask has zero diagonal and is not PSD; "
            "if H_ab is nonzero then the two-by-two principal compression and interlacing give lambda_min(H)<=-|H_ab|"
        ),
        "negative_spectral_localization": (
            "if q_(ell,d)>=0 and -sum q c_ell^*H^(d)_ell c_ell>=kappa W_h, then "
            "sum q ||H_(ell,d),-^(1/2)c_ell||_2^2>=kappa W_h"
        ),
        "label_retention": (
            "every spectral row retains its anchor, tail, orientation, tensor-frequency, fixed-difference, and external-weight labels"
        ),
        "boundary": (
            "this does not establish coefficient alignment with a negative eigenspace, finite block concentration, a Gram approximation, "
            "a coefficient partition, a moment, density, or intervals"
        ),
    }
