"""Exact Cycle 187 separated-support ledger against local packing alone."""
from __future__ import annotations

from math import comb


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def separated_critical_occupancy(k: int) -> dict[str, object]:
    """A complete-fibre critical ledger with separation much larger than T."""
    require(k >= 1, "positive scale parameter")
    T = 3 ** (2 * k)
    X, H, Delta = T**25, T**11, T**15
    S, U, M = T**2, T**9, 3 ** (13 * k)
    digits, separation = 24 * k, T**2
    require(2**digits >= M, "Cantor capacity for selected support")
    ambient_upper = 1 + separation * (3**digits - 1) // 2
    require(ambient_upper < Delta, "separated Cantor support leaves chart room")
    N, pair_count = S + 1, comb(S + 1, 2)
    mass = M * (M - 1) * pair_count * pair_count
    target = T**21  # X^(21/25)
    require(8 * mass >= target, "critical ordered cross mass")
    stable_cutoff_upper = 2 * H * Delta // X + 1
    require(U * U >= stable_cutoff_upper, "stable product shell")
    require(separation > T, "support exceeds C186 local scale")
    return {
        "parameters": {"k": k, "T": T, "X": X, "H": H, "Delta": Delta, "S": S, "U": U, "M": M},
        "support": {
            "construction": "1+T^2*cantor_encode(bits,24*k) for 0<=bits<M",
            "cantor_digits": digits, "ambient_upper": ambient_upper,
            "minimum_pairwise_separation": separation,
            "local_window_statement": "every integer interval of length T^2-1 contains at most one selected label",
        },
        "fibres": {"depth": N, "capacity": H // U + 1, "pair_count_per_label": pair_count, "complete": True},
        "mass": {"ordered_cross_mass": mass, "critical_target": target, "lower_factor": (mass, target)},
        "stable_shell": {"minimum_product": U * U, "cutoff_upper": stable_cutoff_upper},
        "boundary": "This is an abstract, separated occupancy ledger. It has no actual-positive-exponential phase assignment and is not an analytic counterexample.",
    }


def verify_all() -> dict[str, object]:
    ledger = separated_critical_occupancy(1)
    require(ledger["support"]["minimum_pairwise_separation"] > ledger["parameters"]["T"], "local separation replay")
    require(8 * ledger["mass"]["ordered_cross_mass"] >= ledger["mass"]["critical_target"], "mass replay")
    return {
        "local_packing_no_go": "Critical cross mass, full-fibre capacity, stable shells, and a local exclusion at the Cycle 186 scale do not by themselves force a critical-box saving: the explicit support has at most one label in much larger T^2 windows and retains X^(21/25) ordered mass.",
        "boundary": "This retains no actual exponential phase assignment. It proves only that a C186-type local packing conclusion needs a new actual-exponential distribution input before it can affect E13.",
        "samples": {"separated_occupancy_k1": ledger},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
