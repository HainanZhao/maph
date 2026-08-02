"""Exact Cycle 48 Huxley--Sargos joint-sieve ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
MAX_NU = Q(11, 25)
TRIVIAL_JOINT = Q(8, 5)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def wrap_exponent(nu: Q) -> Q:
    require(0 <= nu <= MAX_NU, "Fourier range")
    return min(nu, Q(1, 10) + nu / 2)


def joint_ledger(nu: Q) -> dict[str, Q]:
    a = wrap_exponent(nu)
    energy_direct = a + 2
    energy_spacing = a + Q(8, 5) - nu
    energy = max(energy_direct, energy_spacing)
    joint = DELTA / 2 + energy / 2
    return {
        "nu": nu,
        "wrap": a,
        "energy_direct": energy_direct,
        "energy_spacing": energy_spacing,
        "energy": energy,
        "joint": joint,
        "saving": TRIVIAL_JOINT - joint,
    }


def verify_all() -> dict[str, object]:
    transition = joint_ledger(Q(1, 5))
    endpoint = joint_ledger(MAX_NU)
    require(transition["wrap"] == Q(1, 5), "wrap transition")
    require(endpoint["wrap"] == Q(8, 25), "endpoint wrap")
    require(endpoint["energy_direct"] == Q(58, 25), "direct energy")
    require(endpoint["energy_spacing"] == Q(37, 25), "spacing energy")
    require(endpoint["joint"] == Q(73, 50), "joint endpoint")
    require(endpoint["saving"] == Q(7, 50), "endpoint saving")
    return {
        "transition": transition,
        "endpoint": endpoint,
        "comparisons": {
            "cycle45_saving": Q(2, 25),
            "s4_margin": Q(7, 50),
            "full_missing": Q(4, 25),
            "s3_margin": Q(17, 50),
            "gain_over_cycle45": endpoint["saving"] - Q(2, 25),
            "gap_to_full_missing": Q(4, 25) - endpoint["saving"],
        },
    }


if __name__ == "__main__":
    print(verify_all())
