"""Exact evaluation-floor correction for Cycle 33 v2."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def one_anchor_check() -> dict[str, Fraction]:
    evaluation_floor = Q(3, 5)
    approximation_error = Q(1, 20)
    coefficient = Q(1)
    kernel_lower = evaluation_floor - approximation_error
    require(kernel_lower == Q(11, 20), "one-anchor recurrence constant mismatch")
    return {
        "evaluation_floor": evaluation_floor,
        "approximation_error": approximation_error,
        "coefficient": coefficient,
        "kernel_lower": kernel_lower,
    }


def unstable_multi_anchor_check() -> dict[str, object]:
    # Nearly cancelling anchors: gamma=(G,-G), so distance information can
    # coexist with arbitrarily large coefficient norm.
    G = Q(100)
    coefficients = (G, -G)
    l1_norm = abs(coefficients[0]) + abs(coefficients[1])
    require(l1_norm == 200, "multi-anchor stability witness mismatch")
    return {
        "coefficients": coefficients,
        "l1_norm": l1_norm,
        "lesson": "anchor distance alone supplies no coefficient cap",
    }


def verify_all() -> dict[str, object]:
    return {
        "one_anchor": one_anchor_check(),
        "multi_anchor": unstable_multi_anchor_check(),
        "valid_direction": "original b with nu_C(b)>=sqrt(rho)",
        "adaptive_direction_gate": "prove an evaluation floor before recurrence translation",
    }
