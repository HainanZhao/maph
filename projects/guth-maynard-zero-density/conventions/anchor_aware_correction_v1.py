"""Exact anchor-aware correction conventions for Cycle 33."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def flat_phase_row_witness() -> dict[str, object]:
    primes = (2, 3, 5)
    t0 = 0
    row = (Q(1), Q(1), Q(1))
    norm_squared = sum(value * value for value in row)
    normalized_coordinate_squared = Q(1, norm_squared)
    augmented_gram = ((norm_squared, norm_squared), (norm_squared, norm_squared))
    determinant = augmented_gram[0][0] * augmented_gram[1][1] - augmented_gram[0][1] * augmented_gram[1][0]
    require(norm_squared == 3, "phase-row norm mismatch")
    require(normalized_coordinate_squared == Q(1, 3), "flat coordinate mismatch")
    require(determinant == 0, "duplicate-row determinant did not vanish")
    return {
        "primes": primes,
        "t0": t0,
        "unnormalized_row": row,
        "norm_squared": norm_squared,
        "normalized_coordinate_squared": normalized_coordinate_squared,
        "augmented_gram": augmented_gram,
        "augmented_determinant": determinant,
        "distance_to_row_span_squared": Q(0),
    }


def full_column_rank_witness() -> dict[str, object]:
    # Rows (1,0), (0,1), (1,1) span Q^2.
    rows = ((Q(1), Q(0)), (Q(0), Q(1)), (Q(1), Q(1)))
    detector = (Q(2), Q(3))
    coefficients = (Q(2), Q(3), Q(0))
    reconstruction = tuple(sum(coefficients[i] * rows[i][j] for i in range(3)) for j in range(2))
    require(reconstruction == detector, "full-column-rank reconstruction mismatch")
    return {
        "k": 3,
        "N": 2,
        "rows": rows,
        "detector": detector,
        "coefficients": coefficients,
        "reconstruction": reconstruction,
        "row_span_is_full_coordinate_space": True,
    }


def anchor_reformulation() -> dict[str, str]:
    return {
        "anchor_statistic": "alpha_r(d)=min_{|A|<=r} dist(d,span{x_t:t in A})",
        "anchor_branch": "small alpha_r gives a weighted sum of restricted prime kernels K_S(t-t_a)",
        "transverse_branch": "positive alpha_r plus full-span reconstruction requires a many-row arithmetic theorem",
        "anchor_cap": "r=X^o(1)",
        "one_anchor_identity": "if d_p=c p^(-it0) on S, then <x_t,d> is conjugate(c) K_S(t-t0) up to the pinned inner-product convention",
    }


def verify_all() -> dict[str, object]:
    return {
        "flat_phase_row": flat_phase_row_witness(),
        "full_column_rank": full_column_rank_witness(),
        "anchor_reformulation": anchor_reformulation(),
        "correction": "universal flat-vector distance lower bound is false on actual prime rows",
    }
