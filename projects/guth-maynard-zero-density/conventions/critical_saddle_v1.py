"""Exact Cycle 77 critical anchored-saddle exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


THETA = Q(1, 3)
ALPHA = Q(1, 3)
KAPPA = Q(8, 75)
DELTA = Q(3, 5)
PACKET_ERROR = -1 - KAPPA
PACKET_TARGET = Q(6, 25) - KAPPA


def saddle_hessian(beta: Q, c0: Q, y: Q, exponential_value: Q) -> tuple[tuple[Q, Q], tuple[Q, Q]]:
    """Hessian of c0*y*exp(beta*x), treating exp(beta*x) as an exact value."""
    if min(beta, c0, y, exponential_value) <= 0:
        raise ValueError("positive saddle parameters required")
    xx = beta**2 * c0 * y * exponential_value
    xy = beta * c0 * exponential_value
    return ((xx, xy), (xy, Q(0)))


def det2(matrix: tuple[tuple[Q, Q], tuple[Q, Q]]) -> Q:
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def critical_ledger() -> dict[str, object]:
    normalized_tube = PACKET_ERROR - THETA
    anchored_volume = DELTA + THETA + PACKET_ERROR
    pair_error = THETA + PACKET_ERROR
    product_range = 2 * THETA
    ratio_volume = DELTA + product_range + pair_error
    pair_target = 2 * PACKET_TARGET
    ratio_anchor_loss = ratio_volume - pair_target
    common_height = DELTA + THETA
    common_tolerance = DELTA + PACKET_ERROR
    common_main = common_tolerance + 2 * common_height
    common_error = common_height
    common_best = min(DELTA + THETA, max(common_main, common_error))
    return {
        "theta": THETA,
        "alpha": ALPHA,
        "kappa": KAPPA,
        "delta_length_exponent": DELTA,
        "q_length_exponent": THETA,
        "absolute_packet_error_exponent": PACKET_ERROR,
        "packet_count_target_exponent_open": PACKET_TARGET,
        "normalized_mesh": "(Delta^-1,Q^-1,Q^-1)",
        "normalized_tube_exponent": normalized_tube,
        "anchored_volume_exponent": anchored_volume,
        "pair_product_error_exponent": pair_error,
        "pair_product_range_exponent": product_range,
        "ratio_census_volume_exponent": ratio_volume,
        "ratio_pair_target_exponent_open": pair_target,
        "ratio_anchor_loss_exponent": ratio_anchor_loss,
        "common_denominator_height_exponent": common_height,
        "common_denominator_tolerance_exponent": common_tolerance,
        "common_denominator_main_term_exponent": common_main,
        "common_denominator_error_exponent": common_error,
        "common_embedding_best_exponent": common_best,
        "common_embedding_gap_to_target": common_best - PACKET_TARGET,
    }


def verify_all() -> dict[str, object]:
    matrix = saddle_hessian(Q(7, 5), Q(3, 2), Q(4, 3), Q(9, 7))
    if det2(matrix) != -(Q(7, 5) * Q(3, 2) * Q(9, 7)) ** 2:
        raise RuntimeError("saddle determinant")
    row = critical_ledger()
    expected = {
        "normalized_tube_exponent": -Q(36, 25),
        "anchored_volume_exponent": -Q(13, 75),
        "pair_product_error_exponent": -Q(58, 75),
        "ratio_census_volume_exponent": Q(37, 75),
        "ratio_pair_target_exponent_open": Q(4, 15),
        "ratio_anchor_loss_exponent": Q(17, 75),
        "common_denominator_height_exponent": Q(14, 15),
        "common_denominator_tolerance_exponent": -Q(38, 75),
        "common_embedding_best_exponent": Q(14, 15),
        "common_embedding_gap_to_target": Q(4, 5),
    }
    for key, value in expected.items():
        if row[key] != value:
            raise RuntimeError(f"critical ledger mismatch: {key}")
    return {
        "anchored_incidence": "|n-c0*q*exp(2*pi*d/Delta)|<<X^(-83/75)",
        "normalized_surface": "z=c0*y*exp(2*pi*x) on mesh (Delta^-1,Q^-1,Q^-1)",
        "normalized_hessian": "det=-(2*pi*c0*exp(2*pi*x))^2",
        "anchored_target": "uniform count <X^(2/15+o(1))",
        "ratio_census": "|U-exp(2*pi*d/Delta)*V|<<X^(-58/75), U,V product-supported at X^(2/3)",
        "ratio_loss": "formal volume 37/75 versus pair target 4/15; anchor loss 17/75",
        "common_denominator_boundary": "even granting integer Delta, height 14/15 leaves best exponent 14/15, gap 4/5",
        "gate": "prove an anisotropic anchored-saddle incidence theorem or a seed-aware shifted-strip operator bound",
    }


if __name__ == "__main__":
    print(verify_all())
