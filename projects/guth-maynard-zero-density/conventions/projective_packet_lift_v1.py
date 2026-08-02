"""Exact signed projective packet-lift ledger for Cycle 170."""
from __future__ import annotations

from fractions import Fraction as Q
from math import gcd


def _floor(value: Q) -> int:
    return value.numerator // value.denominator


def projective_data(*, d: int, b: int, q: int, a: int) -> dict[str, int]:
    """Canonical positive-denominator reduction of the lifted relation."""
    if d == 0 or q <= 0 or a <= 0 or gcd(a, q) != 1:
        raise ValueError("invalid source packet/cross edge")
    d_raw = q * d
    n_raw = a * (d + b) - q * d
    content = gcd(abs(d_raw), abs(n_raw))
    if content == 0:
        raise RuntimeError("zero projective pair")
    sign = 1 if d_raw > 0 else -1
    return {"D": d_raw, "N": n_raw, "g": content, "Q": abs(d_raw) // content, "A": sign * n_raw // content}


def lift_identity(*, alpha_source: Q, alpha_target: Q, edge_ratio: Q, d: int, b: int, q: int, a: int) -> Q:
    """Return both sides' common exact residual, raising on a wrong target map."""
    if 1 + alpha_target != edge_ratio * (1 + alpha_source):
        raise ValueError("target is not the exponential lift")
    delta = d * alpha_source - b
    edge_error = q * edge_ratio - a
    data = projective_data(d=d, b=b, q=q, a=a)
    raw = data["D"] * alpha_target - data["N"]
    expected = a * delta + edge_error * (d + b + delta)
    if raw != expected:
        raise RuntimeError("projective lift identity")
    return raw


def transported_seed_residual(*, h: int, j: int, beta: Q, alpha_source: Q, alpha_target: Q, edge_ratio: Q, q: int, a: int) -> dict[str, Q | int]:
    """Carry one eligible beta seed through the same reduced-rational edge."""
    if (q * h) % a:
        raise ValueError("nonintegral transported seed")
    if 1 + alpha_target != edge_ratio * (1 + alpha_source):
        raise ValueError("target is not the exponential lift")
    hp = q * h // a
    jp = j + h - hp
    source = j + beta - h * alpha_source
    target = jp + beta - hp * alpha_target
    edge_error = q * edge_ratio - a
    expected = source - Q(h, a) * (1 + alpha_source) * edge_error
    if target != expected:
        raise RuntimeError("seed transport identity")
    return {"h_plus": hp, "j_plus": jp, "source_residual": source, "target_residual": target}


def error_load(*, a: int, d: int, b: int, source_constant: Q, source_depth: int, edge_constant: Q, edge_depth: int) -> Q:
    """Conservative numerator error coefficient Lambda under |delta|<=1."""
    if min(a, source_depth, edge_depth) <= 0 or min(source_constant, edge_constant) < 0:
        raise ValueError("invalid error ledger")
    return a * source_constant / source_depth + (abs(d + b) + 1) * edge_constant / edge_depth


def depth_ledger(*, content: int, load: Q, h_cap: int, denominator: int) -> dict[str, int | None]:
    """Separate error-supported and denominator-admissible target depths."""
    if content <= 0 or load < 0 or h_cap <= 0 or denominator <= 0:
        raise ValueError("invalid depth ledger")
    error_depth = None if load == 0 else _floor(Q(content, 1) / load)
    capacity_depth = h_cap // denominator
    target_depth = capacity_depth if error_depth is None else min(error_depth, capacity_depth)
    return {"error_depth": error_depth, "capacity_depth": capacity_depth, "target_depth": target_depth}


def certifies_reduced_packet(*, load: Q, content: int, depth: int, denominator: int, h_cap: int) -> bool:
    """Check both Lambda/g <= 1/K and QK<=H, including exact zero load."""
    if load < 0 or content <= 0 or depth <= 0 or denominator <= 0 or h_cap <= 0:
        raise ValueError("invalid packet certification")
    return (load == 0 or load / content <= Q(1, depth)) and denominator * depth <= h_cap


def obstruction_reason(*, seed_integral_and_in_range: bool, content: int, minimum_content: int, error_depth: int | None, capacity_depth: int, critical_depth: int) -> str:
    """First exact obstruction for the frozen projective-lift architecture."""
    if minimum_content <= 0 or capacity_depth < 0 or critical_depth <= 0:
        raise ValueError("invalid obstruction thresholds")
    if not seed_integral_and_in_range:
        return "seed_integrality_or_range"
    if content < minimum_content:
        return "projective_content"
    if error_depth is not None and error_depth < critical_depth:
        return "error_supported_depth"
    if capacity_depth < critical_depth:
        return "denominator_capacity"
    return "seeded_deep_packet"


def verify_all() -> dict[str, object]:
    # alpha=1/2, E=3/2, alpha_target=5/4; both source and target seeds are exact.
    data = projective_data(d=2, b=1, q=2, a=3)
    if data != {"D": 4, "N": 5, "g": 1, "Q": 4, "A": 5}:
        raise RuntimeError("signed projective data")
    if lift_identity(alpha_source=Q(1, 2), alpha_target=Q(5, 4), edge_ratio=Q(3, 2), d=2, b=1, q=2, a=3) != 0:
        raise RuntimeError("exact lift")
    seed = transported_seed_residual(h=30, j=15, beta=Q(0), alpha_source=Q(1, 2), alpha_target=Q(5, 4), edge_ratio=Q(3, 2), q=2, a=3)
    if seed != {"h_plus": 20, "j_plus": 25, "source_residual": Q(0), "target_residual": Q(0)}:
        raise RuntimeError("seed preservation")
    load = error_load(a=3, d=2, b=1, source_constant=Q(1), source_depth=2, edge_constant=Q(1), edge_depth=3)
    if load != Q(17, 6):
        raise RuntimeError("error load")
    depths = depth_ledger(content=17, load=Q(17, 6), h_cap=20, denominator=4)
    if depths != {"error_depth": 6, "capacity_depth": 5, "target_depth": 5}:
        raise RuntimeError("depth split")
    if not certifies_reduced_packet(load=Q(17, 6), content=17, depth=5, denominator=4, h_cap=20):
        raise RuntimeError("positive-load packet certification")
    zero_depths = depth_ledger(content=17, load=Q(0), h_cap=20, denominator=4)
    if zero_depths != {"error_depth": None, "capacity_depth": 5, "target_depth": 5}:
        raise RuntimeError("zero-load convention")
    if not certifies_reduced_packet(load=Q(0), content=17, depth=5, denominator=4, h_cap=20):
        raise RuntimeError("zero-load packet certification")
    if obstruction_reason(seed_integral_and_in_range=True, content=17, minimum_content=1, error_depth=6, capacity_depth=5, critical_depth=5) != "seeded_deep_packet":
        raise RuntimeError("deep classifier")
    if obstruction_reason(seed_integral_and_in_range=True, content=17, minimum_content=1, error_depth=4, capacity_depth=5, critical_depth=5) != "error_supported_depth":
        raise RuntimeError("error obstruction")
    if obstruction_reason(seed_integral_and_in_range=True, content=17, minimum_content=1, error_depth=6, capacity_depth=4, critical_depth=5) != "denominator_capacity":
        raise RuntimeError("capacity obstruction")
    return {
        "identity": "D alpha_L-N=a delta+(qE-a)(d+b+delta), with Q=|D|/g and A=sgn(D)N/g",
        "seed": "an integral reduced-rational edge carries the original beta seed to the target with its exact transported residual",
        "error": "under |delta|<=C_S/(K_S X)<=1 and |qE-a|<=C_E/(K_E X), the full lifted error is at most Lambda/X and the reduced error at most Lambda/(gX)",
        "depth": "error-supported depth floor(g/Lambda), interpreted as infinity when Lambda=0, and denominator capacity floor(H/Q) are separate; their minimum certifies both the packet inequality and QK<=H",
        "classifier": "seed/range, content, error-supported depth, and denominator capacity are ordered obstruction gates",
        "boundary": "This is a finite projective-lift classifier. It does not prove a compatible population, a mass lower bound, recurrence, skeleton, density, or interval gain.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
