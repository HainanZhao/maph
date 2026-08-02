"""Exact four-row common-intercept ledgers for Cycle 181."""
from __future__ import annotations

from fractions import Fraction as Q
from math import ceil, gcd
from typing import Iterable


Pair = tuple[tuple[int, int], tuple[int, int]]


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def pair_intercept(
    pair: Pair, *, alpha: Q, beta: Q, x: int, height: int, strip_constant: int
) -> dict[str, object]:
    """Retain an oriented physical pair and its integral rational-line intercept."""
    require(x > 0 and height > 0 and strip_constant > 0, "positive intercept scale")
    (h1, j1), (h2, j2) = sorted(pair)
    require(h1 < h2 and all(height <= h <= 2 * height for h in (h1, h2)), "oriented pair range")
    width = Q(strip_constant, x)
    eta1 = Q(j1) + beta - h1 * alpha
    eta2 = Q(j2) + beta - h2 * alpha
    require(abs(eta1) <= width and abs(eta2) <= width, "pair strip miss")
    d, a = h2 - h1, j2 - j1
    delta = Q(a) - d * alpha
    require(abs(delta) <= 2 * width, "pair slope error")
    q = d * j1 - a * h1
    intercept_error = Q(q) + d * beta
    exact_error_bound = width * (d + 2 * h1)
    uniform_error_bound = Q(5 * strip_constant * height, x)
    require(abs(intercept_error) <= exact_error_bound <= uniform_error_bound, "intercept error")
    return {
        "pair": {"h1": h1, "j1": j1, "h2": h2, "j2": j2},
        "gap": d,
        "numerator_gap": a,
        "slope_error": delta,
        "residuals": {"first": eta1, "second": eta2},
        "intercept_numerator": q,
        "intercept_error": intercept_error,
        "intercept_error_bound": exact_error_bound,
        "uniform_intercept_error_bound": uniform_error_bound,
    }


def common_intercept_rectangle(
    left: Pair,
    right: Pair,
    *,
    left_label: int,
    right_label: int,
    alpha_left: Q,
    alpha_right: Q,
    beta: Q,
    x: int,
    height: int,
    strip_constant: int,
    stable_product_cutoff: int,
) -> dict[str, object]:
    """Exactify the beta-cancelling intercept determinant for one rectangle."""
    require(left_label != right_label and stable_product_cutoff >= 1, "label/product state")
    first = pair_intercept(left, alpha=alpha_left, beta=beta, x=x, height=height, strip_constant=strip_constant)
    second = pair_intercept(right, alpha=alpha_right, beta=beta, x=x, height=height, strip_constant=strip_constant)
    d, e = int(first["gap"]), int(second["gap"])
    q, q_prime = int(first["intercept_numerator"]), int(second["intercept_numerator"])
    invariant = e * q - d * q_prime
    exact_bound = e * first["intercept_error_bound"] + d * second["intercept_error_bound"]
    uniform_bound = Q(10 * strip_constant * height * height, x)
    require(abs(invariant) <= exact_bound <= uniform_bound < 1, "intercept exactification cutoff")
    require(invariant == 0, "nonzero common-intercept invariant")
    rho_left, rho_right = Q(q, d), Q(q_prime, e)
    require(rho_left == rho_right, "common rational intercept")
    rho = rho_left
    denominator = rho.denominator
    numerator = rho.numerator
    require(d % denominator == 0 and e % denominator == 0, "reduced intercept divisibility")
    reduced_beta_error = abs(Q(numerator) + denominator * beta)
    require(reduced_beta_error <= Q(5 * strip_constant * height, x), "reduced intercept beta tube")
    label_gap = abs(left_label - right_label)
    product = label_gap * d * e
    require(product >= stable_product_cutoff, "not a stable-product rectangle")
    determinant = e * int(first["numerator_gap"]) - d * int(second["numerator_gap"])
    return {
        "labels": {"left": left_label, "right": right_label, "absolute_gap": label_gap},
        "phase_state": {
            "alpha_left": alpha_left,
            "alpha_right": alpha_right,
            "beta": beta,
            "x": x,
            "height": height,
            "strip_constant": strip_constant,
        },
        "left_pair": first,
        "right_pair": second,
        "slope_determinant": determinant,
        "product": product,
        "stable_product_cutoff": stable_product_cutoff,
        "intercept_determinant": invariant,
        "common_intercept": {"numerator": numerator, "denominator": denominator, "value": rho},
        "reduced_beta_error": reduced_beta_error,
    }


def eligible_intercept_count(
    intercepts: Iterable[Q], *, beta: Q, x: int, height: int, strip_constant: int
) -> int:
    """Certify that at most one beta-tube numerator occurs for each denominator <= H."""
    values = set(intercepts)
    require(x > 0 and height > 0 and strip_constant > 0, "positive packet scale")
    tube = Q(5 * strip_constant * height, x)
    require(tube < Q(1, 2), "unique numerator cutoff")
    by_denominator: dict[int, int] = {}
    for rho in values:
        denominator, numerator = rho.denominator, rho.numerator
        require(denominator <= height, "intercept denominator exceeds pair height")
        require(abs(Q(numerator) + denominator * beta) <= tube, "intercept outside beta tube")
        prior = by_denominator.setdefault(denominator, numerator)
        require(prior == numerator, "two tube numerators at one denominator")
    require(len(values) <= height, "too many eligible intercepts")
    return len(values)


def stable_packet_pigeonhole(*, stable_rectangles: int, height: int) -> int:
    """Return the guaranteed largest common-intercept packet size."""
    require(stable_rectangles >= 0 and height > 0, "packet population scale")
    return ceil(stable_rectangles / height)


def verify_all() -> dict[str, object]:
    rectangle = common_intercept_rectangle(
        ((21, 10), (23, 11)), ((22, 5), (26, 6)),
        left_label=1, right_label=2, alpha_left=Q(1, 2), alpha_right=Q(1, 4), beta=Q(1, 2),
        x=100000, height=20, strip_constant=1, stable_product_cutoff=8,
    )
    require(rectangle["intercept_determinant"] == 0, "sample intercept exactification")
    require(rectangle["common_intercept"]["value"] == Q(-1, 2), "sample common intercept")
    count = eligible_intercept_count([Q(-1, 2), Q(-3, 6)], beta=Q(1, 2), x=100000, height=20, strip_constant=1)
    require(count == 1, "reduced packet index")
    packet = stable_packet_pigeonhole(stable_rectangles=641, height=20)
    require(packet == 33, "packet pigeonhole")
    return {
        "intercept_exactification": "For every retained rectangle, I=e*q-d*q' is an integer of absolute value at most 10*C*H^2/X; below the frozen cutoff it vanishes, so q/d=q'/e.",
        "packet_partition": "Every stable rectangle is indexed by its reduced common intercept rho=p/v, with v dividing both pair gaps and |p+v*beta|<=5*C*H/X. There are at most H eligible rho.",
        "packet_consequence": "A stable rectangle population W partitions into at most H common-intercept packets, so one packet has at least ceil(W/H) rectangles while retaining both pairs, labels, residuals, product, and slope determinant.",
        "boundary": "This is an exact common-intercept packet reduction. It proves no upper bound inside a packet, recurrence, density gain, or interval result.",
        "samples": {"rectangle": rectangle, "eligible_intercepts": count, "packet_lower_bound": packet},
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
