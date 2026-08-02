"""Exact variable-rank block-subspace ledger for Cycle 31."""
from fractions import Fraction


Q = Fraction
KAPPAS = tuple(Q(j, 25) for j in range(1, 6))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def row(kappa: Fraction) -> dict[str, Fraction]:
    critical_shift = Q(6, 25)
    block_size = 1 - kappa
    reconstruction = critical_shift - kappa
    difference_cycles = Q(3, 5) - kappa
    require(0 < kappa < critical_shift, "kappa outside variable-rank range")
    require(block_size > Q(17, 30), "block outside checked PNT range")
    require(difference_cycles > 0, "block phase has no angular cycles")
    require(reconstruction > 0, "reconstruction is not stretched exponential")
    return {
        "kappa": kappa,
        "block_count": kappa,
        "block_size": block_size,
        "reconstruction": reconstruction,
        "difference_cycles": difference_cycles,
    }


def tradeoff_table() -> list[dict[str, Fraction]]:
    rows = [row(kappa) for kappa in KAPPAS]
    require([item["reconstruction"] for item in rows] == [Q(j, 25) for j in range(5, 0, -1)], "tradeoff reconstruction sequence mismatch")
    return rows


def self_dual() -> dict[str, Fraction | str]:
    kappa = Q(4, 25)
    item = row(kappa)
    target_rows = Q(21, 25)
    missing_saving = Q(4, 25)
    require(item["block_count"] == missing_saving, "block count does not match missing saving")
    require(item["block_size"] == target_rows, "block size does not match target rows")
    require(item["reconstruction"] == Q(2, 25), "self-dual reconstruction mismatch")
    return {
        **item,
        "target_rows": target_rows,
        "missing_saving": missing_saving,
        "block_prime_count": "X^(21/25-o(1))",
        "target_skeleton_count": "X^(21/25+o(1))",
        "reconstruction_error": "exp(-X^(2/25-o(1)))",
    }


def verify_all() -> dict[str, object]:
    return {
        "tradeoff_table": tradeoff_table(),
        "self_dual": self_dual(),
        "admissible_range": "fixed 0<kappa<6/25",
        "regular_alternatives": "shift<=-k rho/4, approximate/exact block-modulated reconstruction, or exact scaled-row dependence",
    }
