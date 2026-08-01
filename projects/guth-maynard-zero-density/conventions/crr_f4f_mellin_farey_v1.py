"""Exact scale and constant bookkeeping for the CRR F4F Mellin--Farey gate.

The accompanying note proves the analytic identities.  This module freezes
only their integral-scale arithmetic and the safe eventual implications.
"""
from __future__ import annotations

from fractions import Fraction


MIN_V = 8


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def scales(v: int) -> dict[str, int]:
    require(isinstance(v, int) and v >= MIN_V, "v must be an integer at least 8")
    result = {"v": v, "H": v**12, "Q": v**4, "R": v**8}
    require(result["H"] == result["Q"] ** 3, "Mellin--Farey reduction needs H=Q^3")
    require(result["R"] == result["Q"] ** 2, "critical cardinality needs R=Q^2")
    return result


def exact_rows() -> dict[str, Fraction | str]:
    """Return constants used in the log-window and high-frequency no-go."""
    rows: dict[str, Fraction | str] = {
        "log_jitter_kernel_at_zero": Fraction(6),
        "log_jitter_uniform_upper_numerator": Fraction(7),
        "log_jitter_high_band_lower_numerator": Fraction(1, 2),
        "farey_count_lower": Fraction(1, 200),
        "log_frequency_separation": Fraction(1, 5),
        "high_band_left_endpoint_over_H": Fraction(1, 10),
        "high_band_right_endpoint_over_H": Fraction(9, 10),
        "high_band_length_over_H": Fraction(4, 5),
        "eventual_Q_threshold_for_hilbert_lower": Fraction(20000),
        "wiener_no_go_lower": Fraction(1, 1000),
        "conditional_wiener_to_f4f": "W_Q<=v^(-kappa) implies F4F_(kappa/2) eventually",
    }
    require(rows["log_jitter_kernel_at_zero"] == 6, "jitter kernel zero value mismatch")
    require(rows["farey_count_lower"] == Fraction(1, 200), "Farey count lower mismatch")
    require(rows["log_frequency_separation"] == Fraction(1, 5), "log separation mismatch")
    require(rows["high_band_length_over_H"] == Fraction(4, 5), "high-band length mismatch")
    return rows


def verify_all(v: int = MIN_V) -> dict[str, object]:
    data = scales(v)
    rows = exact_rows()
    require(data["Q"] >= 4096, "the inherited actual-Farey geometry threshold changed")
    require(rows["eventual_Q_threshold_for_hilbert_lower"] > data["Q"], "v=8 is intentionally below the asymptotic Hilbert threshold")
    return {"scales": data, "exact_rows": rows}
