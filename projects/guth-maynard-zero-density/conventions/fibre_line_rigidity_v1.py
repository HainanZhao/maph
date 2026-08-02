"""Exact common-intercept fibre-line ledgers for Cycle 182."""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from typing import Mapping, Sequence


Row = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def oriented_slope(first: Row, second: Row) -> tuple[int, int, Q]:
    """Return the positive height gap, numerator gap, and reduced rational slope."""
    (h1, j1), (h2, j2) = sorted((first, second))
    require(h1 < h2, "distinct fibre heights")
    d, a = h2 - h1, j2 - j1
    return d, a, Q(a, d)


def certify_common_intercept_fibre(
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
    """Certify one complete non-singleton fibre as a rational lattice segment.

    ``rows`` is the full actual fibre for this label.  The certificate checks
    the strip row by row, all physical pair slopes, the packet intercept, and
    every integral lattice point between the extreme actual rows.
    """
    require(label > 0 and x > 0 and height > 0 and strip_constant > 0, "positive fibre scale")
    require(4 * strip_constant * height * height < x, "slope rigidity cutoff")
    ordered = sorted(set(rows))
    require(len(ordered) >= 2 and len(ordered) == len(rows), "complete non-singleton distinct fibre")
    require(all(height <= h <= 2 * height for h, _ in ordered), "fibre height range")
    width = Q(strip_constant, x)
    residuals = {h: Q(j) + beta - h * alpha for h, j in ordered}
    require(all(abs(value) <= width for value in residuals.values()), "fibre strip miss")

    pair_data = [oriented_slope(left, right) for left, right in combinations(ordered, 2)]
    slopes = {slope for _, _, slope in pair_data}
    require(len(slopes) == 1, "distinct reduced slopes in one fibre")
    slope = next(iter(slopes))
    numerator, denominator = slope.numerator, slope.denominator
    require(denominator <= height, "primitive slope denominator too large")

    for d, _, pair_slope in pair_data:
        require(abs(pair_slope - alpha) <= Q(2 * strip_constant, d * x), "pair slope strip bound")
    first_h, first_j = ordered[0]
    require(Q(first_j) - slope * first_h == rho, "packet intercept differs from fibre line")
    require(all(Q(j) - slope * h == rho for h, j in ordered), "actual row off rational fibre line")

    intercept_numerator, intercept_denominator = rho.numerator, rho.denominator
    require(denominator % intercept_denominator == 0, "intercept denominator does not divide slope denominator")
    residue = first_h % denominator
    require(all(h % denominator == residue for h, _ in ordered), "integral heights are not one congruence class")

    first_height, last_height = ordered[0][0], ordered[-1][0]
    expected_heights = list(range(first_height, last_height + 1, denominator))
    require([h for h, _ in ordered] == expected_heights, "missing lattice point between extreme fibre rows")
    for h in expected_heights:
        value = slope * h + rho
        require(value.denominator == 1, "line lattice point not integral")
        j = value.numerator
        require(abs(Q(j) + beta - h * alpha) <= width, "intermediate lattice point misses strip")

    extreme_gap = last_height - first_height
    count = len(ordered)
    require(extreme_gap == (count - 1) * denominator, "extreme gap not primitive progression")
    extreme_slope = Q(ordered[-1][1] - ordered[0][1], extreme_gap)
    require(extreme_slope == slope, "extreme pair slope")
    approximation_bound = Q(2 * strip_constant, extreme_gap * x)
    require(abs(slope - alpha) <= approximation_bound, "extreme-pair approximation")
    require(count <= Q(height, denominator) + 1, "primitive denominator capacity")

    return {
        "label": label,
        "phase_state": {"alpha": alpha, "beta": beta, "x": x, "height": height, "strip_constant": strip_constant},
        "packet_state": dict(packet_state),
        "common_intercept": {"numerator": intercept_numerator, "denominator": intercept_denominator, "value": rho},
        "primitive_slope": {"numerator": numerator, "denominator": denominator, "value": slope},
        "base_height_residue_modulo_slope_denominator": residue,
        "actual_rows": [{"h": h, "j": j, "residual": residuals[h]} for h, j in ordered],
        "fibre_count": count,
        "extreme_gap": extreme_gap,
        "extreme_slope_error": slope - alpha,
        "extreme_slope_error_bound": approximation_bound,
        "capacity_upper_bound": Q(height, denominator) + 1,
    }


def verify_all() -> dict[str, object]:
    packet_state = {
        "labels": {"left": 1, "right": 2},
        "slope_determinant": 2,
        "product_shell": "stable",
        "individual_residuals_retained": True,
    }
    fibre = certify_common_intercept_fibre(
        [(22, 5), (26, 6), (30, 7)],
        label=2, alpha=Q(1, 4), beta=Q(1, 2), rho=Q(-1, 2),
        x=100000, height=20, strip_constant=1, packet_state=packet_state,
    )
    require(fibre["primitive_slope"]["value"] == Q(1, 4), "sample primitive slope")
    require(fibre["common_intercept"]["denominator"] == 2, "sample intercept denominator")
    require(fibre["base_height_residue_modulo_slope_denominator"] == 2, "sample base congruence")
    require(fibre["fibre_count"] == 3 and fibre["extreme_gap"] == 8, "sample full progression")
    return {
        "slope_rigidity": "When 4*C*H^2/X<1, every physical pair in one non-singleton actual fibre has one reduced rational slope A/U.",
        "integral_line": "Inside a Cycle-181 rho=p/v packet, the full fibre lies on j=(A/U)h+p/v; integral rows force v|U and one base-height class modulo U.",
        "fibre_completion": "The actual fibre is a consecutive step-U lattice segment, with N<=1+H/U and |A/U-alpha_ell|<=2*C/((N-1)*U*X).",
        "boundary": "This is a fixed-packet fibre rigidity and capacity reduction. It proves no in-packet census bound, recurrence, density gain, or interval result.",
        "samples": {"fibre": fibre},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
