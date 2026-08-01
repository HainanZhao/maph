"""Exact phase-transition and rank-one semiprime conventions, Cycle 15."""
from __future__ import annotations

from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def steinhaus_fourth_count(m: int) -> dict[str, int]:
    require(m >= 1, "m must be positive")
    count = 0
    for i in range(m):
        for j in range(m):
            for k in range(m):
                for ell in range(m):
                    if sorted((i, j)) == sorted((k, ell)):
                        count += 1
    formula = 2 * m * m - m
    require(count == formula, "Steinhaus fourth-moment count mismatch")
    return {"m": m, "enumerated": count, "formula": formula}


def square_coefficient_norm(m: int) -> dict[str, int]:
    require(m >= 1, "m must be positive")
    diagonal = m
    off_diagonal = 4 * (m * (m - 1) // 2)
    total = diagonal + off_diagonal
    require(total == 2 * m * m - m, "square coefficient norm mismatch")
    return {"m": m, "diagonal": diagonal, "off_diagonal": off_diagonal, "total": total}


def phase_transition_rows() -> dict[str, object]:
    h = Q(12, 5)
    p_star = Q(24, 5)
    coherent = p_star
    random_bulk = h + p_star / 2
    require(coherent == random_bulk == Q(24, 5), "phase-transition equality mismatch")
    return {
        "time_exponent_in_X": h,
        "p_star": p_star,
        "coherent_exponent": coherent,
        "random_bulk_exponent": random_bulk,
        "crossing_equation": "p=12/5+p/2",
        "lower_envelope": "max(p,12/5+p/2)",
    }


def gm_rank_one_rows() -> dict[str, Fraction]:
    n = Q(2)
    time = Q(12, 5)
    threshold = Q(7, 5)
    term_1 = 2 * n - 2 * threshold
    term_2 = Q(18, 5) * n - 4 * threshold
    term_3 = time + Q(12, 5) * n - 4 * threshold
    generic = max(term_1, term_2, term_3)
    target = Q(36, 25)
    saving = generic - target
    require((term_1, term_2, term_3) == (Q(6, 5), Q(8, 5), Q(8, 5)), "GM term translation mismatch")
    require(generic == Q(8, 5), "generic exponent mismatch")
    require(saving == Q(4, 25), "required X-scale saving mismatch")
    require(5 * target == Q(36, 5), "v-scale target mismatch")
    require(5 * saving == Q(4, 5), "v-scale saving mismatch")
    return {
        "length_exponent_in_X": n,
        "time_exponent_in_X": time,
        "threshold_exponent_in_X": threshold,
        "gm_term_1": term_1,
        "gm_term_2": term_2,
        "gm_term_3": term_3,
        "generic_exponent": generic,
        "target_exponent": target,
        "required_saving": saving,
        "target_exponent_in_v": 5 * target,
        "saving_in_v": 5 * saving,
    }


def verify_all() -> dict[str, object]:
    fourth_counts = [steinhaus_fourth_count(m) for m in range(1, 13)]
    square_norms = [square_coefficient_norm(m) for m in range(1, 13)]
    require([row["formula"] for row in fourth_counts] == [row["total"] for row in square_norms], "fourth moment and square norm disagree")
    return {
        "finite_fourth_counts": fourth_counts,
        "finite_square_norms": square_norms,
        "phase_transition": phase_transition_rows(),
        "rank_one_gm_translation": gm_rank_one_rows(),
    }
