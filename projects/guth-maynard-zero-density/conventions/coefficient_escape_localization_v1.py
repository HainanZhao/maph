"""Cycle 154 finite labelled escape localization at one divisor comb."""

from __future__ import annotations

from fractions import Fraction


def localized_escape(
    *,
    total_negative_projection: Fraction,
    class_real_projections: tuple[Fraction, ...],
    witness_norm_squared_over_scale: Fraction,
) -> dict[str, object]:
    """Extract one negative class from a finite additive escape partition.

    Projections are normalized by the one-witness scale, and a negative real
    projection is recorded as a positive negative mass.
    """
    if (
        total_negative_projection <= 0
        or not class_real_projections
        or witness_norm_squared_over_scale <= 0
    ):
        raise ValueError("positive target, finite partition, and witness norm bound required")
    negative_parts = tuple(max(-projection, Fraction()) for projection in class_real_projections)
    total_available = sum(negative_parts, Fraction())
    if total_available < total_negative_projection:
        raise ValueError("class partition cannot support the stated total negative projection")
    class_count = len(class_real_projections)
    threshold = total_negative_projection / class_count
    chosen = min(index for index, mass in enumerate(negative_parts) if mass >= threshold)
    return {
        "class_count": class_count,
        "total_negative_projection": total_negative_projection,
        "sum_class_negative_parts": total_available,
        "per_class_lower_bound": threshold,
        "chosen_class_index": chosen,
        "chosen_class_negative_projection": negative_parts[chosen],
        "witness_norm_squared_over_scale": witness_norm_squared_over_scale,
        "one_ray_l2_squared_over_scale_lower_bound": threshold * threshold
        / witness_norm_squared_over_scale,
    }


def theorem_record() -> dict[str, object]:
    return {
        "finite_class_pigeonhole": (
            "if -Re<F,w_h>/W_h>=kappa and F is an additive partition into J labelled classes, "
            "one class has negative normalized projection at least kappa/J"
        ),
        "one_ray_l2": (
            "if the frozen comb norm satisfies ||w_h||_2^2<=A W_h with fixed A, Cauchy turns a class projection "
            "at least (kappa/J)W_h into L2 norm squared at least (kappa/J)^2 W_h/A"
        ),
        "label_retention": (
            "the chosen class retains its frozen escape reason and all coefficient, rational-tail, and payload labels"
        ),
        "boundary": (
            "this localizes an assumed finite labelled escape projection and a frozen comb-norm bound; it does not prove the partition, bound the class, "
            "or prove a full moment, density, or intervals"
        ),
    }
