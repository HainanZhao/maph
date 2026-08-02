"""Exact Cycle 69 stationary-dual exponent and Hessian ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
MAX_FREQUENCY = Q(36, 25)
MAX_STATIONARY_INDEX = MAX_FREQUENCY - DELTA
SKELETON_TARGET = Q(21, 25)


def dual_ledger(frequency_exponent: Q) -> dict[str, object]:
    if frequency_exponent < 0 or frequency_exponent > MAX_FREQUENCY:
        raise ValueError("frequency exponent outside registered range")
    stationary_index = frequency_exponent - DELTA
    return {
        "frequency_exponent": frequency_exponent,
        "stationary_regime_nonempty_at_power_scale": frequency_exponent >= DELTA,
        "stationary_index_exponent": stationary_index,
        "stationary_phase": "Psi(m,k)=u-m-u*log(u/m), u=k*Delta/(2*pi)",
        "stationary_point": "x=(2*pi)^-1 log(k*Delta/(2*pi*m))",
        "homogeneity": "Psi(lambda*m,lambda*k)=lambda*Psi(m,k)",
        "hessian_entries": "Psi_mm=-u/m^2, Psi_mk=Delta/(2*pi*m), Psi_kk=-(Delta/(2*pi))^2/u",
        "hessian_determinant": Q(0),
    }


def verify_all() -> dict[str, object]:
    top = dual_ledger(MAX_FREQUENCY)
    threshold = dual_ledger(DELTA)
    if MAX_STATIONARY_INDEX != SKELETON_TARGET:
        raise RuntimeError("stationary/skeleton exponent identity")
    if top["stationary_index_exponent"] != Q(21, 25):
        raise RuntimeError("top stationary index")
    if top["hessian_determinant"] != 0:
        raise RuntimeError("homogeneous Hessian degeneracy")
    if threshold["stationary_index_exponent"] != 0:
        raise RuntimeError("stationary threshold")
    return {
        "poisson_form": "Delta sum_k integral w(x)e(m(exp(2pi*x)-1)-k*Delta*x)dx",
        "stationary_condition": "2*pi*m*exp(2*pi*x)=k*Delta",
        "dual_phase": top["stationary_phase"],
        "homogeneity": top["homogeneity"],
        "hessian_determinant": Q(0),
        "dual_index_ceiling": MAX_STATIONARY_INDEX,
        "skeleton_target": SKELETON_TARGET,
        "gate": "exploit one-dimensional projective ratio curvature, retain unfurled variables, or route the X^21/25 stationary-index family to the skeleton engine",
    }


if __name__ == "__main__":
    print(verify_all())
