"""Exact Cycle 47 near-curve and geometric exponent ledger."""
from __future__ import annotations

from fractions import Fraction as Q


DELTA = Q(3, 5)
H = Q(11, 25)
TUBE_VERTICAL = Q(-21, 25)
TARGET = Q(7, 25)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def derivative_exponent(order: int) -> Q:
    require(order >= 1, "positive derivative order")
    return DELTA - order * H


def huxley_sargos_terms(order: int) -> dict[str, Q]:
    require(order >= 3, "Huxley--Sargos order")
    lam = derivative_exponent(order)
    return {
        "order": Q(order),
        "lambda": lam,
        "derivative_term": H + Q(2, order * (order + 1)) * lam,
        "tube_term": H + Q(2, order * (order - 1)) * TUBE_VERTICAL,
        "ratio_term": (TUBE_VERTICAL - lam) / order,
        "constant_term": Q(0),
    }


def huxley_sargos_bound(order: int) -> Q:
    row = huxley_sargos_terms(order)
    return max(row[key] for key in ("derivative_term", "tube_term", "ratio_term", "constant_term"))


def geometric_scales() -> dict[str, Q]:
    slope = derivative_exponent(1)
    second = derivative_exponent(2)
    arclength = H + slope
    euclidean_curvature = second - 3 * slope
    radius = -euclidean_curvature
    normal_tube = TUBE_VERTICAL - slope
    affine_arclength = H + second / 3
    howard_trifonov_count = arclength - radius / 3
    return {
        "slope": slope,
        "graph_second_derivative": second,
        "euclidean_arclength": arclength,
        "euclidean_curvature": euclidean_curvature,
        "radius": radius,
        "normal_tube": normal_tube,
        "affine_arclength": affine_arclength,
        "howard_trifonov_count": howard_trifonov_count,
    }


def verify_all() -> dict[str, object]:
    rows = [{**huxley_sargos_terms(k), "bound": huxley_sargos_bound(k)} for k in range(3, 21)]
    best = min(rows, key=lambda row: (row["bound"], row["order"]))
    geometry = geometric_scales()
    require(best["order"] == Q(3), "best order")
    require(best["bound"] == Q(8, 25), "best Huxley--Sargos exponent")
    require(best["bound"] - TARGET == Q(1, 25), "Huxley--Sargos gap")
    require(best["derivative_term"] == best["bound"], "leading term")
    require(geometry["graph_second_derivative"] == Q(-7, 25), "graph second derivative")
    require(geometry["euclidean_curvature"] == Q(-19, 25), "Euclidean curvature")
    require(geometry["normal_tube"] == Q(-1), "normal tube")
    require(geometry["affine_arclength"] == Q(26, 75), "affine arclength")
    require(geometry["howard_trifonov_count"] == Q(26, 75), "Howard--Trifonov exponent")
    return {
        "target": TARGET,
        "huxley_sargos_rows": rows,
        "best_huxley_sargos": best,
        "huxley_sargos_gap": best["bound"] - TARGET,
        "geometry": geometry,
    }


if __name__ == "__main__":
    print(verify_all())
