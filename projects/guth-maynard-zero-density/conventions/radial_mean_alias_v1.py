"""Cycle 122 radial zero-mode cancellation and Poisson-alias ledger."""

from __future__ import annotations

from fractions import Fraction


def alias_exponent_ledger(xi: Fraction) -> dict[str, Fraction]:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    return {
        "alias_order": xi,
        "n_stationary_amplitude": Fraction(1, 6) - xi / 2,
        "Hc_scale": xi + Fraction(1, 3),
    }


def theorem_record() -> dict[str, object]:
    return {
        "kernel": (
            "K_H0(y)=H0 hat(U)(-H0 y), with U smooth and compactly "
            "supported in (0,infinity)"
        ),
        "vanishing_moments": (
            "int y^j K_H0(y)dy=0 for every j>=0 because U^(j)(0)=0"
        ),
        "zero_mode": (
            "after y=c log(p0 n/S), the zero n-Poisson mode is "
            "O_N((Q/c)(cH0)^(-N)) for every N, uniformly for bounded p0 "
            "and fixed smooth compact supports"
        ),
        "nonzero_phase": "Phi_ell(n)=Hc log(p0 n/S)-ell n",
        "nonzero_saddle": (
            "a stationary point exists only for ell>0 and is "
            "n*=Hc/ell, equivalently A*=p0Hc/ell"
        ),
        "nonzero_geometry": (
            "Phi_ell(n*)=Hc[log(p0Hc/(ell S))-1], "
            "|Phi_ell''(n*)|=ell^2/(Hc), and stationary amplitude "
            "sqrt(Hc)/ell=n*/sqrt(Hc)~sqrt(Q/K)"
        ),
        "alias_support": "n~Q and H~H0~KQ/D with c~D force ell~K",
        "boundary": (
            "the continuous volume term is removed, but no bound for the "
            "nonzero ell~K aliases, simple-root sum, complete moment, density, "
            "or prime intervals is proved"
        ),
    }
