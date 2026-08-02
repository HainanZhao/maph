"""Cycle 119 simple-root zeroth-mode and saving ledger."""

from __future__ import annotations

from fractions import Fraction


LOWER_BAND_LEFT = Fraction(16, 25)
LOWER_BAND_RIGHT = Fraction(58, 75)
STRONG_BENCHMARK = Fraction(13, 30)
KERNEL_EXPONENT = Fraction(-1, 2)  # Q^(-3/2), with Q=X^(1/3)


def exponent_ledger(xi: Fraction) -> dict[str, Fraction]:
    """Return exact X-exponents for the simple-root zeroth Fourier mode."""
    if not LOWER_BAND_LEFT <= xi < LOWER_BAND_RIGHT:
        raise ValueError("xi outside lower band")
    raw_volume = Fraction(28, 15) - xi
    weighted_volume = raw_volume + KERNEL_EXPONENT
    return {
        "raw_volume": raw_volume,
        "kernel": KERNEL_EXPONENT,
        "weighted_volume": weighted_volume,
        "strong_benchmark": STRONG_BENCHMARK,
        "required_saving": weighted_volume - STRONG_BENCHMARK,
    }


def theorem_record() -> dict[str, object]:
    return {
        "scales": "Q=X^(1/3), D=X^(3/5), K=X^xi, 16/25<=xi<58/75",
        "zeroth_mode": (
            "a periodic Selberg majorant of radius c/K and degree H~K has "
            "constant coefficient asymp 1/K; on Q^2 D^2 tuples this is "
            "Q^2 D^2/K=X^(28/15-xi)"
        ),
        "fourier_factorization": (
            "for sign sectors sigma,tau, the nonzero mode is exactly "
            "hat(S)(h) T_sigma(h) T_tau(h), where "
            "T_sigma(h)=sum_{B~Q,a in I_sigma} e(h B exp(2 pi a/D)); "
            "it is not replaced by an absolute square"
        ),
        "weighted_exponent": (
            "after the corrected Q^(-3/2)=X^(-1/2) kernel, the zeroth mode "
            "has exponent 41/30-xi"
        ),
        "required_saving": (
            "to reach 13/30 one must save X^(14/15-xi): from X^(22/75) "
            "at xi=16/25 down to X^(4/25) as xi approaches 58/75"
        ),
        "limitation": (
            "any Selberg-majorant proof that bounds the nonzero Fourier "
            "contribution termwise in absolute value retains the positive "
            "zeroth mode and therefore cannot reach the 13/30 benchmark"
        ),
        "boundary": (
            "this does not exclude an unsigned discrepancy theorem with "
            "cancellation against the mean; it proves no estimate for the "
            "original signed moment, density, or prime intervals"
        ),
    }
