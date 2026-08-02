"""Exact ledgers for Cycle 179 cross-label tower and area resonance.

The geometric tower is an actual positive-exponential rational-base family.
The oriented area identity is algebraic and retains the fixed-beta residuals.
"""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd
from typing import Iterable


Row = tuple[int, int]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def exact_row_count(height: int, denominator: int) -> int:
    """Count positive multiples of denominator in the integer interval [H,2H]."""
    require(height >= 1 and denominator >= 1, "positive row data")
    lower = (height + denominator - 1) // denominator
    upper = (2 * height) // denominator
    return max(0, upper - lower + 1)


def active_depth(height: int, base_denominator: int) -> int:
    """Largest m>=0 with r**m<=2H, computed without floating logarithms."""
    require(height >= 1 and base_denominator >= 2, "tower scale")
    depth, power = 0, 1
    while power * base_denominator <= 2 * height:
        power *= base_denominator
        depth += 1
    return depth


def geometric_tower(height: int, base_denominator: int, chart_multiples: int) -> dict[str, object]:
    """Exact beta-zero rows at labels mL in the rational-base tower."""
    require(chart_multiples >= 0, "nonnegative chart range")
    rows = []
    for multiple in range(1, chart_multiples + 1):
        denominator = base_denominator**multiple
        numerator = (base_denominator + 1) ** multiple - denominator
        require(gcd(numerator, denominator) == 1, "tower denominator not primitive")
        count = exact_row_count(height, denominator)
        rows.append({"m": multiple, "numerator": numerator, "denominator": denominator, "count": count})
    counts = [row["count"] for row in rows]
    total = sum(counts)
    ordered_cross = total * total - sum(count * count for count in counts)
    depth = active_depth(height, base_denominator)
    geometric_bound = Q(height, base_denominator - 1) + depth
    require(total <= geometric_bound, "geometric row sum bound")
    require(depth <= 2 * height, "elementary logarithmic boundary")
    require(total <= 3 * height, "uniform tower row bound")
    require(ordered_cross <= 9 * height * height, "uniform tower cross bound")
    return {
        "height": height,
        "base_denominator": base_denominator,
        "chart_multiples": chart_multiples,
        "active_depth": depth,
        "rows": rows,
        "total_rows": total,
        "ordered_cross_label_mass": ordered_cross,
        "geometric_row_bound": geometric_bound,
        "uniform_row_bound": 3 * height,
        "uniform_cross_bound": 9 * height * height,
    }


def _extended_gcd(left: int, right: int) -> tuple[int, int, int]:
    """Return g,s,t with s*left+t*right=g=gcd(left,right)."""
    if right == 0:
        return abs(left), 1 if left >= 0 else -1, 0
    divisor, s1, t1 = _extended_gcd(right, left % right)
    return divisor, t1, s1 - (left // right) * t1


def bezout_base_recovery(exponents: Iterable[int], rational_powers: Iterable[Q]) -> dict[str, object]:
    """Recover y from rational values y**m_i when gcd(m_i)=1."""
    powers = list(rational_powers)
    indices = list(exponents)
    require(len(indices) == len(powers) and indices, "nonempty matched powers")
    require(all(index > 0 and value > 0 for index, value in zip(indices, powers)), "positive power data")
    common = indices[0]
    coefficients = [1]
    for index in indices[1:]:
        divisor, left_coefficient, right_coefficient = _extended_gcd(common, index)
        coefficients = [left_coefficient * coefficient for coefficient in coefficients] + [right_coefficient]
        common = divisor
    require(common == 1 and sum(coefficient * index for coefficient, index in zip(coefficients, indices)) == 1, "Bezout normalization")
    recovered = Q(1)
    for value, coefficient in zip(powers, coefficients):
        recovered *= value**coefficient
    return {"normalized_exponents": indices, "bezout_coefficients": coefficients, "recovered_base": recovered}


def rational_base_exact_tower(
    height: int, *, numerator_base: int, denominator_base: int, chart_multiples: int
) -> dict[str, object]:
    """Exact beta-zero rational-root rows for a reduced base u/v>1.

    For v>=2, geometric denominators give a uniform O(H) row bound.  For an
    integral base v=1, chart admissibility supplies the frozen M<=9 bound.
    """
    require(height >= 1 and numerator_base > denominator_base >= 1, "reduced positive rational base")
    require(gcd(numerator_base, denominator_base) == 1, "base must be reduced")
    require(chart_multiples >= 0, "nonnegative chart range")
    if denominator_base == 1:
        require(chart_multiples <= 9, "integral base chart bound")
    rows = []
    for multiple in range(1, chart_multiples + 1):
        denominator = denominator_base**multiple
        numerator = numerator_base**multiple - denominator
        require(gcd(numerator, denominator) == 1, "exact rational root denominator")
        count = exact_row_count(height, denominator)
        rows.append({"m": multiple, "numerator": numerator, "denominator": denominator, "count": count})
    counts = [row["count"] for row in rows]
    total = sum(counts)
    cross = total * total - sum(count * count for count in counts)
    if denominator_base >= 2:
        depth = active_depth(height, denominator_base)
        require(total <= Q(height, denominator_base - 1) + depth <= 3 * height, "nonintegral tower row bound")
        uniform_cross_bound = 9 * height * height
    else:
        require(total <= 9 * (height + 1) <= 18 * height, "integral tower row bound")
        uniform_cross_bound = 324 * height * height
    require(cross <= uniform_cross_bound, "exact-rational tower cross bound")
    return {
        "height": height,
        "base": {"u": numerator_base, "v": denominator_base},
        "chart_multiples": chart_multiples,
        "rows": rows,
        "total_exact_beta_zero_rows": total,
        "ordered_cross_label_mass": cross,
        "uniform_cross_bound": uniform_cross_bound,
    }


def same_label_area_resonance(
    first: Row,
    second: Row,
    third: Row,
    *,
    alpha_same: Q,
    alpha_other: Q,
    beta: Q,
    x: int,
    height: int,
    strip_constant: int,
) -> dict[str, object]:
    """Beta-eliminated integer area from two same-label and one other-label rows."""
    require(x > 0 and height > 0 and strip_constant > 0, "positive area scale")
    h1, j1 = first
    h2, j2 = second
    h3, j3 = third
    require(len({h1, h2}) == 2, "two distinct same-label rows")
    require(all(height <= h <= 2 * height for h in (h1, h2, h3)), "area row range")
    residuals = [
        Q(j1) + beta - h1 * alpha_same,
        Q(j2) + beta - h2 * alpha_same,
        Q(j3) + beta - h3 * alpha_other,
    ]
    width = Q(strip_constant, x)
    require(all(abs(residual) <= width for residual in residuals), "area strip miss")
    weights = (h2 - h3, h3 - h1, h1 - h2)
    require(sum(weights) == 0, "beta cancellation weights")
    area = weights[0] * j1 + weights[1] * j2 + weights[2] * j3
    phase = h3 * (h2 - h1) * (alpha_same - alpha_other)
    error = Q(area) - phase
    error_bound = width * sum(abs(weight) for weight in weights)
    require(sum(abs(weight) for weight in weights) <= 2 * height, "cyclic height variation")
    require(abs(error) <= error_bound <= 2 * height * width, "area error bound")
    return {
        "area_integer": area,
        "phase": phase,
        "area_error": error,
        "area_error_bound": error_bound,
        "residuals": residuals,
        "weights": weights,
        "beta": beta,
        "same_label_difference": h2 - h1,
        "third_height": h3,
    }


def light_triangle_population(counts: Iterable[int], *, threshold: int, label_capacity: int) -> dict[str, int]:
    """Count oriented two-at-one-label/one-at-another-label actual triangles."""
    values = list(counts)
    require(threshold >= 1 and label_capacity >= len(values), "population parameters")
    require(all(value >= 0 for value in values), "nonnegative fibre counts")
    require(all(value <= 2 * threshold for value in values), "not in light branch")
    total = sum(values)
    same_label_ordered_pairs = sum(value * (value - 1) for value in values)
    triangles = sum(value * (value - 1) * (total - value) for value in values)
    lower_bound = (total - 2 * threshold) * (total - label_capacity)
    require(same_label_ordered_pairs >= total - label_capacity, "pigeonhole pair lower bound")
    require(triangles >= lower_bound, "light triangle lower bound")
    return {
        "total": total,
        "same_label_ordered_pairs": same_label_ordered_pairs,
        "oriented_cross_label_triangles": triangles,
        "light_triangle_lower_bound": lower_bound,
        "threshold": threshold,
        "label_capacity": label_capacity,
    }


def verify_all() -> dict[str, object]:
    tower = geometric_tower(height=120, base_denominator=2, chart_multiples=7)
    require(tower["rows"][0] == {"m": 1, "numerator": 1, "denominator": 2, "count": 61}, "first tower row")
    require(tower["rows"][6]["count"] == 1, "boundary tower row")
    require(tower["total_rows"] <= 3 * 120 and tower["ordered_cross_label_mass"] <= 9 * 120 * 120, "tower envelope")

    recovery = bezout_base_recovery([2, 3], [Q(9, 4), Q(27, 8)])
    require(recovery["recovered_base"] == Q(3, 2), "Bezout rational-base recovery")
    nonintegral = rational_base_exact_tower(120, numerator_base=5, denominator_base=3, chart_multiples=7)
    integral = rational_base_exact_tower(120, numerator_base=2, denominator_base=1, chart_multiples=9)
    require(nonintegral["uniform_cross_bound"] == 9 * 120 * 120, "nonintegral exact tower")
    require(integral["uniform_cross_bound"] == 324 * 120 * 120, "integral exact tower")

    area = same_label_area_resonance(
        (21, 10), (23, 11), (22, 5),
        alpha_same=Q(1, 2), alpha_other=Q(1, 4), beta=Q(1, 2),
        x=1000, height=20, strip_constant=1,
    )
    require(area["area_integer"] == 11 and area["phase"] == 11 and area["area_error"] == 0, "beta cancellation example")

    population = light_triangle_population([3, 3, 3], threshold=2, label_capacity=3)
    require(population["oriented_cross_label_triangles"] == 108, "triangle count")
    require(4 * population["oriented_cross_label_triangles"] >= population["total"] ** 2, "critical-shape triangle mass")
    return {
        "geometric_tower": "For every r>=2, all exact beta-zero rows in the mL rational-base tower have total at most 3H and ordered distinct-label mass at most 9H^2, uniformly even when r varies.",
        "rational_gcd_compression": "Any finite exact-rational label set gcd-compresses by Bezout to one reduced rational base u/v. At beta zero with exact rows, its complete tower has ordered cross mass O(H^2), with an explicit integral-base chart constant.",
        "area_identity": "Two actual rows at one label and one at another give an integer A with |A-h3(h2-h1)(alpha_ell-alpha_m)|<=2CH/X; beta cancels exactly.",
        "triangle_population": "In the light branch, Q_tri=sum N_ell(N_ell-1)(T-N_ell)>=(T-2R)(T-L), where L is the chart label capacity.",
        "boundary": "These are a structured prototype no-go and a lower-bound reduction. They prove no upper bound for the area-resonance census, density gain, or interval result.",
        "samples": {"tower": tower, "Bezout_recovery": recovery, "nonintegral_tower": nonintegral, "integral_tower": integral, "area": area, "population": population},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
