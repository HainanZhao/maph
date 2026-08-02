"""Cycle 126 Freiman-web recurrence and chain-depth ledger."""

from __future__ import annotations

from fractions import Fraction
from math import ceil


def popular_difference_edges(R: int, D: int) -> int:
    if not 2 <= R <= D:
        raise ValueError("require 2<=R<=D")
    return ceil(R * (R - 1) / (2 * D - 2))


def longest_chain_edges(R: int, L: int) -> int:
    if not 1 <= L < R:
        raise ValueError("a nonzero-difference forest requires 1<=L<R")
    return ceil(L / (R - L))


def sufficient_edges_for_depth(R: int, J: int) -> int:
    if R < 2 or J < 1:
        raise ValueError("positive depth and at least two vertices required")
    return ceil(J * R / (J + 1))


def error_margin(xi: Fraction) -> Fraction:
    if not Fraction(16, 25) <= xi < Fraction(58, 75):
        raise ValueError("xi outside lower band")
    return xi - Fraction(4, 15)


def theorem_record() -> dict[str, object]:
    return {
        "difference_multiplier": (
            "for E_d={a in A:a+d in A}, Freiman multiplicativity applied to "
            "(a+d)+b=a+(b+d) makes rho_d=r_(a+d)/r_a independent of a in E_d"
        ),
        "popular_difference": (
            "if A has R points in D consecutive integers, some nonzero d has "
            "L_d>=ceil(R(R-1)/(2D-2)) oriented edges"
        ),
        "chain_bound": (
            "the d-edge graph is a disjoint union of paths; with R vertices and "
            "L_d edges, one path has at least ceil(L_d/(R-L_d)) edges"
        ),
        "depth_gate": (
            "L_d>=ceil(JR/(J+1)) is sufficient for a J-edge chain; popular-edge "
            "pigeonholing alone does not approach this density unless A is nearly full"
        ),
        "geometric_chain": (
            "on a chain a0,a0+d,...,a0+Jd, one has exactly "
            "r_(a0+jd)=r_a0 rho_d^j"
        ),
        "approximation": (
            "rho_d=g^d(1+O(1/(KQ))); on a supported J<=D chain, "
            "rho_d^J=g^(Jd)(1+O(J/(KQ))) and the worst total error is "
            "O(D/(KQ))=X^(-(xi-4/15)+o(1))"
        ),
        "anchor_gate": (
            "the recurrence retains d,rho_d and rational labels, but E16 must "
            "still tie one chain vertex to the original packet anchor and verify "
            "that the required depth is supplied"
        ),
        "boundary": (
            "no long chain follows from energy alone; no seed realization, "
            "low-multiplicity bound, simple-root closure, complete moment, density, "
            "or prime intervals is proved"
        ),
    }
