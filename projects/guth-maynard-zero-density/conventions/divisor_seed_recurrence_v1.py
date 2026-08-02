"""Cycle 141 divisor-seed transition and continuation ledger."""

from __future__ import annotations

from fractions import Fraction
from math import ceil, gcd


def forced_transition(a: int, b: int, u: int, v: int) -> tuple[Fraction, Fraction]:
    if min(a, b, u, v) <= 0 or gcd(a, b) != 1 or a % u or b % v:
        raise ValueError("primitive compatible class data required")
    return Fraction(a, u * v), Fraction(b, u * v)


def repeated_transition_possible(a: int, b: int, u: int, v: int) -> bool:
    left, right = forced_transition(a, b, u, v)
    return left.denominator == right.denominator == 1 and left * right == 1


def continuation_ledger(vertices: int, colored_edges: int, depth: int) -> dict[str, int]:
    if vertices < 2 or not 1 <= colored_edges < vertices or depth < 2:
        raise ValueError("invalid path-forest parameters")
    return {
        "longest_chain_edges": ceil(colored_edges / (vertices - colored_edges)),
        "length_two_starts": max(0, 2 * colored_edges - vertices),
        "depth_starts": max(0, depth * colored_edges - (depth - 1) * vertices),
        "edges_sufficient_for_depth": ceil(depth * vertices / (depth + 1)),
    }


def theorem_record() -> dict[str, object]:
    return {
        "core_columns": (
            "in one divisor class the rational columns are "
            "c0=(v*p0,u*q0)^T and c1=((A/u)*p0,(B/v)*q0)^T"
        ),
        "transition_rigidity": (
            "if one linear transition maps c0 to c1 for two distinct core "
            "ratios p0/q0, it must equal diag(A/(uv),B/(uv))"
        ),
        "unimodular_no_go": (
            "an integral unimodular forced diagonal has positive integer entries "
            "with product one, hence A=B=uv=1; injective labels then force d=0. "
            "For nonzero d, a fixed GL_2(Z) transition labels at most one edge"
        ),
        "color_count": (
            "the cross-gcd colors number at most tau(A)tau(B)=X^{o(1)}, so one "
            "class contains J X^{-o(1)} edges"
        ),
        "continuation": (
            "with R vertices and L colored d-edges, the graph is a path forest; "
            "one chain has ceil(L/(R-L)) edges, length-two starts number at least "
            "max(0,2L-R), and depth k needs L>=ceil(kR/(k+1))"
        ),
        "independence": (
            "fiber saturation compares L with the arithmetic capacity N^2/H, "
            "whereas chain depth compares L with the mode-set size R; neither "
            "comparison controls the other"
        ),
        "replacement_invariant": (
            "the next engine must retain class-colored continuation density, "
            "equivalently intersections of consecutive edge-start sets, together "
            "with the signed tails; transition-matrix repetition must not be used"
        ),
        "boundary": (
            "no positive continuation density, recurrence, full paired norm, "
            "endpoint, moment, density, or prime-interval theorem is proved"
        ),
    }
