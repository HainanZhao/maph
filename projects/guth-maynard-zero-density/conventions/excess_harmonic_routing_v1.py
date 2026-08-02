"""Exact Cycle 37 Fourier-routing exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def routing(excess_decay: Q) -> dict[str, Q]:
    arc_count = Q(3, 10)
    mass = Q(1)
    normalized_harmonic = -(excess_decay + arc_count) / 2
    kernel_harmonic = mass + normalized_harmonic
    color_loss = arc_count
    return {
        "excess_decay": excess_decay,
        "arc_count": arc_count,
        "normalized_harmonic": normalized_harmonic,
        "kernel_harmonic": kernel_harmonic,
        "harmonic_color_loss": color_loss,
    }


def registered_scales() -> dict[str, dict[str, Q]]:
    quadratic_tiny = routing(Q(6, 5))
    first_harmonic = routing(Q(3, 5))
    require(quadratic_tiny["kernel_harmonic"] == Q(1, 4), "r^4 excess routing")
    require(first_harmonic["kernel_harmonic"] == Q(11, 20), "r^2 excess routing")
    require(first_harmonic["harmonic_color_loss"] == Q(3, 10), "harmonic color loss")
    return {"r4_excess": quadratic_tiny, "r2_excess": first_harmonic}


def finite_fourier_perturbation() -> dict[str, str]:
    return {
        "perturbation": "q_j=qstar_j+(2a/L)cos(2pi*m*j/L)",
        "mass": "preserved for 2<=m<=L-2",
        "first_harmonic": "preserved exactly by cyclic orthogonality",
        "new_harmonics": "hat(q-qstar)(m)=hat(q-qstar)(L-m)=a",
        "entropy": "E(q) is comparable to a^2 when qstar/u is bounded and |a| is small",
    }


def verify_all() -> dict[str, object]:
    rows = {"registered_scales": registered_scales(), "finite_model": finite_fourier_perturbation()}
    require(rows["registered_scales"]["r4_excess"]["kernel_harmonic"] < Q(2, 5), "r4 route should be below popular scale")
    require(rows["registered_scales"]["r2_excess"]["kernel_harmonic"] < Q(7, 10), "r2 route should be below original threshold")
    return rows


if __name__ == "__main__":
    print(verify_all())
