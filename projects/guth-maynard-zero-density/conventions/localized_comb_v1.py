"""Exact Cycle 42 localized-comb exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


HEIGHT = Q(12, 5)
SPACING = Q(3, 5)
HARMONIC_RANGE = Q(3, 10)
MAX_ROWS = HEIGHT - SPACING


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def comb_ledger(s: int) -> dict[str, Q | int]:
    require(isinstance(s, int) and s >= 1, "fixed positive amplifier")
    full_annulus_mass = HEIGHT + HARMONIC_RANGE
    localized_mass = MAX_ROWS
    relaxation_loss = full_annulus_mass - localized_mass
    diagonal_vector = Q(s + 1) + MAX_ROWS + HARMONIC_RANGE
    target = Q(s) + Q(31, 10)
    require(relaxation_loss == Q(9, 10), "comb relaxation loss")
    require(diagonal_vector == target, "localized diagonal must match target")
    return {
        "amplifier": s,
        "full_annulus_comb_mass": full_annulus_mass,
        "localized_comb_mass": localized_mass,
        "full_annulus_relaxation_loss": relaxation_loss,
        "localized_diagonal_vector": diagonal_vector,
        "lcam_target": target,
    }


def registered_scales() -> dict[str, object]:
    s3 = comb_ledger(3)
    s4 = comb_ledger(4)
    require(s3["lcam_target"] == Q(61, 10), "s3 target")
    require(s4["lcam_target"] == Q(71, 10), "s4 target")
    require(s3["full_annulus_relaxation_loss"] > Q(17, 50), "loss exceeds r2 margin")
    require(s4["full_annulus_relaxation_loss"] > Q(7, 50), "loss exceeds r4 margin")
    return {"s3": s3, "s4": s4}


def verify_all() -> dict[str, object]:
    return registered_scales()


if __name__ == "__main__":
    print(verify_all())
