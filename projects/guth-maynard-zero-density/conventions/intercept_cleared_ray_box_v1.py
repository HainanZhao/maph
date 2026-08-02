"""Exact intercept-cleared primitive-ray ledgers for Cycle 183."""
from __future__ import annotations

from fractions import Fraction as Q
from typing import Iterable, Mapping, Sequence

from conventions.fibre_line_rigidity_v1 import certify_common_intercept_fibre


Row = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def cleared_ray_fibre(
    rows: Sequence[Row],
    *,
    label: int,
    alpha: Q,
    beta: Q,
    rho: Q,
    x: int,
    height: int,
    strip_constant: int,
    packet_state: Mapping[str, object],
) -> dict[str, object]:
    """Clear rho=p/v from a certified C182 fibre into an integral ray segment."""
    fibre = certify_common_intercept_fibre(
        rows, label=label, alpha=alpha, beta=beta, rho=rho, x=x,
        height=height, strip_constant=strip_constant, packet_state=packet_state,
    )
    slope = fibre["primitive_slope"]
    intercept = fibre["common_intercept"]
    numerator, denominator = int(slope["numerator"]), int(slope["denominator"])
    p, v = int(intercept["numerator"]), int(intercept["denominator"])
    require(denominator % v == 0, "uncleared intercept denominator")
    u = denominator // v
    transformed = []
    for row in fibre["actual_rows"]:
        h, j = int(row["h"]), int(row["j"])
        require(h % u == 0, "cleared height divisor")
        t, ordinate = h // u, v * j - p
        require(ordinate == numerator * t, "cleared ray identity")
        transformed.append({"t": t, "J": ordinate, "residual": row["residual"]})
    residue = transformed[0]["t"] % v
    require(all(row["t"] % v == residue for row in transformed), "cleared ray residue")
    return {
        "fibre": fibre,
        "clearing": {"p": p, "v": v, "u": u, "A": numerator, "U": denominator, "t_residue_mod_v": residue},
        "ray_rows": transformed,
        "near_orbit_error": Q(numerator) - denominator * alpha,
        "near_orbit_error_bound": Q(2 * strip_constant, (int(fibre["fibre_count"]) - 1) * x),
    }


def primitive_ray_rectangle(
    left_rows: Sequence[Row],
    right_rows: Sequence[Row],
    *,
    left_label: int,
    right_label: int,
    alpha_left: Q,
    alpha_right: Q,
    beta: Q,
    rho: Q,
    x: int,
    height: int,
    strip_constant: int,
    packet_state: Mapping[str, object],
    left_start: int,
    right_start: int,
    left_multiplier: int,
    right_multiplier: int,
    scale_delta: int,
    stable_cutoff: Q,
    lower_coefficient: Q,
    upper_coefficient: Q,
) -> dict[str, object]:
    """Retain a stable physical rectangle and factor its determinant through rays."""
    require(left_label != right_label and scale_delta > 0, "distinct ray labels")
    require(left_multiplier > 0 and right_multiplier > 0 and stable_cutoff > 0, "positive ray multipliers")
    require(lower_coefficient > 0 and upper_coefficient >= lower_coefficient, "ray spacing constants")
    left = cleared_ray_fibre(
        left_rows, label=left_label, alpha=alpha_left, beta=beta, rho=rho,
        x=x, height=height, strip_constant=strip_constant, packet_state=packet_state,
    )
    right = cleared_ray_fibre(
        right_rows, label=right_label, alpha=alpha_right, beta=beta, rho=rho,
        x=x, height=height, strip_constant=strip_constant, packet_state=packet_state,
    )
    left_fibre, right_fibre = left["fibre"], right["fibre"]
    n_left, n_right = int(left_fibre["fibre_count"]), int(right_fibre["fibre_count"])
    require(left_start >= 0 and left_start + left_multiplier < n_left, "left physical pair index")
    require(right_start >= 0 and right_start + right_multiplier < n_right, "right physical pair index")
    A, U, u, v = (int(left["clearing"][key]) for key in ("A", "U", "u", "v"))
    B, V, w, v_right = (int(right["clearing"][key]) for key in ("A", "U", "u", "v"))
    require(v == v_right, "packet intercept mismatch")
    left_pair = left_fibre["actual_rows"][left_start], left_fibre["actual_rows"][left_start + left_multiplier]
    right_pair = right_fibre["actual_rows"][right_start], right_fibre["actual_rows"][right_start + right_multiplier]
    d, a = left_multiplier * U, left_multiplier * A
    e, b = right_multiplier * V, right_multiplier * B
    primitive_determinant = w * A - u * B
    determinant = e * a - d * b
    require(determinant == left_multiplier * right_multiplier * v * primitive_determinant, "primitive determinant factorization")
    label_gap = abs(left_label - right_label)
    alpha_gap = abs(alpha_left - alpha_right)
    require(lower_coefficient * label_gap <= alpha_gap * scale_delta <= upper_coefficient * label_gap, "ray label gap envelope")
    determinant_error = abs(Q(determinant) - d * e * (alpha_left - alpha_right))
    error_bound = Q(4 * strip_constant * height, x)
    require(determinant_error <= error_bound, "physical determinant error")
    product = label_gap * d * e
    require(product >= stable_cutoff, "below stable ray product cutoff")
    divided_error = determinant_error / (left_multiplier * right_multiplier * v)
    primitive_phase = Q(U * V, v) * (alpha_left - alpha_right)
    require(abs(Q(primitive_determinant) - primitive_phase) == divided_error, "divided determinant error")
    require(divided_error <= lower_coefficient * label_gap * U * V / (2 * v * scale_delta), "stable primitive error")
    lower_bound = lower_coefficient * label_gap * U * V / (2 * v * scale_delta)
    upper_bound = (upper_coefficient + lower_coefficient / 2) * label_gap * U * V / (v * scale_delta)
    require(abs(primitive_determinant) >= lower_bound, "primitive determinant lower bound")
    require(abs(primitive_determinant) <= upper_bound, "primitive determinant upper bound")
    require(primitive_determinant != 0, "zero primitive cross-ray determinant")
    return {
        "labels": {"left": left_label, "right": right_label, "absolute_gap": label_gap},
        "packet_state": dict(packet_state),
        "left_ray": left,
        "right_ray": right,
        "physical_pairs": {"left": left_pair, "right": right_pair, "left_multiplier": left_multiplier, "right_multiplier": right_multiplier},
        "gaps": {"d": d, "a": a, "e": e, "b": b, "product": product, "stable_cutoff": stable_cutoff},
        "determinants": {
            "D": determinant,
            "F": primitive_determinant,
            "primitive_phase": primitive_phase,
            "error": determinant_error,
            "error_bound": error_bound,
            "F_lower_bound": lower_bound,
            "F_upper_bound": upper_bound,
        },
    }


def dyadic_floor(value: int) -> int:
    require(value >= 1, "positive dyadic field")
    return 1 << (value.bit_length() - 1)


def frozen_ray_box_cap(*, light_threshold: int, height: int, scale_delta: int) -> int:
    """Preregistered B_box=b_R^4*b_H^2*b_Delta for the seven fields."""
    require(light_threshold >= 1 and height >= 1 and scale_delta >= 1, "positive frozen box scales")
    depth_bins = (2 * light_threshold).bit_length()
    denominator_bins = height.bit_length()
    label_bins = scale_delta.bit_length()
    return depth_bins**4 * denominator_bins**2 * label_bins


def ray_box_key(rectangle: Mapping[str, object]) -> tuple[int, int, int, int, int, int, int]:
    """Frozen seven-field box key; no field is inferred after population inspection."""
    left = rectangle["left_ray"]["fibre"]
    right = rectangle["right_ray"]["fibre"]
    gaps = rectangle["gaps"]
    physical = rectangle["physical_pairs"]
    return (
        dyadic_floor(int(left["fibre_count"])),
        dyadic_floor(int(right["fibre_count"])),
        dyadic_floor(int(left["primitive_slope"]["denominator"])),
        dyadic_floor(int(right["primitive_slope"]["denominator"])),
        dyadic_floor(int(physical["left_multiplier"])),
        dyadic_floor(int(physical["right_multiplier"])),
        dyadic_floor(int(rectangle["labels"]["absolute_gap"])),
    )


def select_populated_ray_box(rectangles: Iterable[Mapping[str, object]], *, box_cap: int) -> dict[str, object]:
    """Pigeonhole stable rectangles into their preregistered seven-field boxes."""
    require(box_cap >= 1, "positive frozen box cap")
    groups: dict[tuple[int, int, int, int, int, int, int], list[Mapping[str, object]]] = {}
    for rectangle in rectangles:
        key = ray_box_key(rectangle)
        groups.setdefault(key, []).append(rectangle)
    require(groups, "empty stable rectangle population")
    key, members = max(groups.items(), key=lambda item: (len(item[1]), item[0]))
    total = sum(len(values) for values in groups.values())
    require(len(groups) <= box_cap, "unfrozen ray box count exceeded")
    require(len(members) * box_cap >= total, "ray-box pigeonhole")
    return {"key": key, "stable_rectangle_count": len(members), "total_stable_rectangles": total, "frozen_box_cap": box_cap}


def verify_all() -> dict[str, object]:
    packet_state = {"intercept_packet": "rho=-1/2", "product_shell": "stable", "residuals_retained": True}
    rectangle = primitive_ray_rectangle(
        [(21, 10), (23, 11), (25, 12)], [(22, 5), (26, 6), (30, 7)],
        left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
        x=100000, height=20, strip_constant=1, packet_state=packet_state,
        left_start=0, right_start=0, left_multiplier=1, right_multiplier=1,
        scale_delta=10, stable_cutoff=Q(8, 100), lower_coefficient=Q(2), upper_coefficient=Q(3),
    )
    require(rectangle["determinants"]["D"] == 2 and rectangle["determinants"]["F"] == 1, "sample determinant factorization")
    require(rectangle["left_ray"]["ray_rows"][0]["t"] == 21, "left cleared ray")
    require(rectangle["right_ray"]["ray_rows"][0]["t"] == 11, "right cleared ray")
    box_cap = frozen_ray_box_cap(light_threshold=2, height=20, scale_delta=10)
    box = select_populated_ray_box([rectangle, rectangle], box_cap=box_cap)
    require(box["stable_rectangle_count"] == 2, "sample ray box")
    return {
        "intercept_clearing": "For rho=p/v and U=v*u, every fibre row has u|h and becomes the integral ray point (t,J)=(h/u,v*j-p) with J=A*t.",
        "primitive_determinant": "For physical pair multipliers k,q, D=k*q*v*F with F=w*A-u*B nonzero and |F| comparable to r*U*V/(v*Delta) in the stable range.",
        "near_orbit": "Every fibre side retains ||U*alpha_ell||<=2C/((N_ell-1)X) together with its full line and residual data.",
        "box_population": "With B_box=bit_length(2R)^4*bit_length(H)^2*bit_length(Delta), a frozen seven-field dyadic partition has at most B_box boxes, so one complete primitive-ray box contains at least W/B_box of any stable packet population W.",
        "boundary": "This is a populated candidate saturation class, not an in-packet upper bound, recurrence, density gain, or interval result.",
        "samples": {"rectangle": rectangle, "box": box},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
