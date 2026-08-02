"""Exact square-root volume-noise conventions, Cycle 22."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def critical_exponents() -> dict[str, Fraction]:
    m = Q(1)
    k = Q(21, 25)
    entry = -m / 2
    operator_noise = (k - m) / 2
    requested_operator = Q(-3, 5)
    operator_gap = operator_noise - requested_operator
    bulk_log_volume = 2 * k - m
    signal_log_volume = Q(6, 25)
    volume_gap = bulk_log_volume - signal_log_volume
    require(entry == Q(-1, 2), "entry-noise exponent mismatch")
    require(operator_noise == Q(-2, 25), "operator-noise exponent mismatch")
    require(operator_gap == Q(13, 25), "operator gap mismatch")
    require(bulk_log_volume == Q(17, 25), "bulk volume exponent mismatch")
    require(volume_gap == Q(11, 25), "volume gap mismatch")
    return {
        "m": m,
        "k": k,
        "entry_noise": entry,
        "operator_noise": operator_noise,
        "cycle21_requested_operator": requested_operator,
        "operator_power_gap": operator_gap,
        "bulk_log_volume": bulk_log_volume,
        "common_vector_log_volume": signal_log_volume,
        "bulk_minus_signal": volume_gap,
    }


def finite_block_unitary() -> dict[str, Fraction | int]:
    n = 4
    k = 2 * n
    m = 16
    delta_squared = Q(n, m)
    off_diagonal_squared = Q(1, m)
    determinant = (1 - delta_squared) ** n
    require(delta_squared == Q(k, 2 * m), "operator discrepancy formula mismatch")
    require(off_diagonal_squared == Q(1, m), "square-root entry scale mismatch")
    require(determinant == Q(3, 4) ** 4, "block-unitary determinant mismatch")
    return {
        "n": n,
        "k": k,
        "m": m,
        "delta_squared": delta_squared,
        "off_diagonal_squared": off_diagonal_squared,
        "positive_eigenvalue": "1+sqrt(n/m)",
        "negative_eigenvalue": "1-sqrt(n/m)",
        "each_eigenvalue_multiplicity": n,
        "determinant": determinant,
        "diagonal": Q(1),
    }


def verify_all() -> dict[str, object]:
    return {
        "critical_exponents": critical_exponents(),
        "finite_block_unitary": finite_block_unitary(),
        "exact_model": "H=I+sqrt(n/m)[[0,U],[U*,0]] with flat unitary U",
        "route_boundary": "square-root entry cancellation alone cannot supply the Cycle-21 full operator gate or Cycle-20 absolute volume lower bound",
        "replacement_gate": "control a bulk-renormalized log-volume or spectral shift at the smaller common-vector scale X^(6/25)",
    }
