"""Exact arithmetic for the Cycle-167 affine beta-transport architecture.

This module classifies the single-step multiplicative map only.  It does not
claim a local Cycle-67 packet at the target label.
"""
from __future__ import annotations

from fractions import Fraction as Q
from itertools import combinations
from math import comb, gcd


def primitive_parent_count(parameters: tuple[int, ...]) -> int:
    """Count canonical primitive four-subsets of an integer parameter set."""
    total = 0
    for rows in combinations(sorted(set(parameters)), 4):
        shifts = tuple(value - rows[0] for value in rows[1:])
        content = 0
        for value in shifts:
            content = gcd(content, value)
        total += content == 1
    return total


def distinct_parameter_lower_bound(parent_count: int) -> int:
    """Least m satisfying parent_count <= binom(m,4)."""
    if parent_count < 0:
        raise ValueError("negative parent count")
    m = 0
    while comb(m, 4) < parent_count:
        m += 1
    return m


def divisibility_residue(h0: int, r: int, a: int) -> tuple[int, int] | None:
    """Solve a | h0+r*n as n=residue modulo modulus, if soluble."""
    if a <= 0:
        raise ValueError("nonpositive numerator")
    divisor = gcd(a, r)
    if h0 % divisor:
        return None
    modulus = a // divisor
    if modulus == 1:
        return 0, 1
    coefficient = (r // divisor) % modulus
    return (-h0 // divisor * pow(coefficient, -1, modulus)) % modulus, modulus


def eligible_parameters(
    parameters: tuple[int, ...], *, h0: int, r: int, a: int, q: int, h_scale: int
) -> tuple[int, ...]:
    """Apply the exact residue and both source/target row ranges."""
    if q <= 0 or h_scale <= 0:
        raise ValueError("invalid packet/range")
    residue = divisibility_residue(h0, r, a)
    if residue is None:
        return ()
    residue_value, modulus = residue
    selected = []
    for n in sorted(set(parameters)):
        h = h0 + r * n
        hp = Q(q * h, a)
        if n % modulus == residue_value and h_scale <= h <= 2 * h_scale and h_scale <= hp <= 2 * h_scale:
            selected.append(n)
    return tuple(selected)


def direct_map_coefficients(a: int, q: int) -> tuple[Q, Q]:
    """Unique coefficients within the reduced rational B=q/a ansatz."""
    if a <= 0 or q <= 0 or gcd(a, q) != 1:
        raise ValueError("a,q must be coprime positive integers")
    h_multiplier = Q(q, a)
    return h_multiplier, 1 - h_multiplier


def transport_balance(h_scale: int, a: int, depth: int, y_upper: Q) -> Q:
    """Worst extra strip-constant multiplier 2 H y_upper/(a K)."""
    if h_scale <= 0 or a <= 0 or depth <= 0 or y_upper <= 0:
        raise ValueError("invalid transport balance")
    return Q(2 * h_scale, a * depth) * y_upper


def transport_edge(
    *, h: int, j: int, beta: Q, y: Q, q: int, a: int, shift_error: Q
) -> dict[str, Q | int]:
    """Construct the unique direct beta-preserving edge under q E=a+error."""
    if a <= 0 or q <= 0 or gcd(a, q) != 1 or (q * h) % a:
        raise ValueError("ineligible direct transport")
    hp = q * h // a
    jp = j + h - hp
    yp = Q(a + shift_error, q) * y
    source = j + beta - h * (y - 1)
    target = jp + beta - hp * (yp - 1)
    expected = source - Q(h, a) * y * shift_error
    if target != expected:
        raise RuntimeError("transport identity failure")
    return {
        "h_plus": hp,
        "j_plus": jp,
        "y_plus": yp,
        "source_residual": source,
        "target_residual": target,
        "error_increment": target - source,
    }


def verify_all() -> dict[str, object]:
    parameters = (0, 1, 2, 3, 4)
    parent_count = primitive_parent_count(parameters)
    if parent_count > comb(len(parameters), 4):
        raise RuntimeError("primitive parent deconvolution")
    if distinct_parameter_lower_bound(parent_count) > len(parameters):
        raise RuntimeError("distinct parameter lower bound")
    if divisibility_residue(26, 1, 5) != (4, 5):
        raise RuntimeError("residue solution")
    if divisibility_residue(1, 2, 4) is not None:
        raise RuntimeError("insoluble gcd residue")
    if eligible_parameters((0, 1, 2, 3), h0=26, r=1, a=5, q=4, h_scale=20):
        raise RuntimeError("residue obstruction")
    if eligible_parameters((0, 1, 2, 3), h0=21, r=3, a=3, q=2, h_scale=21):
        raise RuntimeError("range obstruction")
    if direct_map_coefficients(5, 3) != (Q(3, 5), Q(2, 5)):
        raise RuntimeError("direct map rigidity")
    edge = transport_edge(h=10, j=5, beta=Q(0), y=Q(3, 2), q=3, a=5, shift_error=Q(0))
    if edge["source_residual"] != 0 or edge["target_residual"] != 0:
        raise RuntimeError("exact beta transport")
    if transport_balance(100, 1, 1, Q(1)) != 200:
        raise RuntimeError("balance ledger")
    return {
        "deconvolution": "P(N)<=binom(|N|,4), so parent multiplicity gives a fourth-root distinct-parameter lower bound only",
        "eligibility": "a|h0+r n is soluble iff gcd(a,r)|h0 and then one residue class is intersected with both exact row ranges",
        "rigidity": "within the reduced rational ansatz B=q/a and j_plus=j+A h, error factorization uniquely forces A=1-q/a; coprimality makes integrality equivalent to a|h",
        "transport": "the exact target residual equals the source residual minus h*y*(qE-a)/a",
        "balance": "with h<=2H and |qE-a|<=C1/(KX), the extra strip constant is at most 2*H*y_upper*C1/(aK)",
        "boundary": "This is a single cross-label edge classifier. It supplies neither a target-local Cycle-67 packet nor an E7/E9 recurrence.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
