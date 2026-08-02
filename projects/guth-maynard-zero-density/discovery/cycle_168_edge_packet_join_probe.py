#!/usr/bin/env python3
"""Exact finite probe for Cycle 168 edge/local-packet joins.

Discovery-only: it checks the labelled composition and why global masses do
not force their support intersection.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q


@dataclass(frozen=True)
class Edge:
    beta: Q
    target_label: int
    h: int
    j: int
    strip_constant: int
    tag: str


@dataclass(frozen=True)
class Packet:
    target_label: int
    a: int
    q: int
    depth: int
    strip_constant: int
    tag: str


def compatible(edge: Edge, packet: Packet, *, h_scale: int) -> bool:
    return edge.target_label == packet.target_label and h_scale <= edge.h <= 2 * h_scale and packet.q * packet.depth <= h_scale


def weighted_join_mass(edges: tuple[Edge, ...], packets: tuple[Packet, ...], *, h_scale: int) -> int:
    """Count labelled compatible pairs; never multiply global totals."""
    return sum(compatible(edge, packet, h_scale=h_scale) for edge in edges for packet in packets)


def propagated_residuals(
    *, edge: Edge, packet: Packet, alpha: Q, x: int
) -> tuple[Q, ...]:
    """Exact Cycle-67 propagation from a target edge endpoint."""
    if edge.target_label != packet.target_label or x <= 0:
        raise ValueError("incompatible target")
    base = edge.j + edge.beta - edge.h * alpha
    packet_error = packet.q * alpha - packet.a
    return tuple(base - k * packet_error for k in range(-packet.depth, packet.depth + 1))


def loop_holonomy_difference(*, h0: int, h_final: int, alpha: Q) -> Q:
    """Difference of two same-label affine-loop strip residuals at zero error."""
    # Along each direct edge j_next-j_current=h_current-h_next.
    delta_j = h0 - h_final
    return delta_j - (h_final - h0) * alpha


def exact_examples() -> dict[str, object]:
    h_scale, x = 20, 1000
    edge = Edge(Q(0), 7, 30, 45, 1, "edge-A")
    packet = Packet(7, 3, 2, 5, 1, "packet-A")
    alpha = Q(3, 2)
    # The edge is an exact target seed, and q*alpha-a=0.
    if any(propagated_residuals(edge=edge, packet=packet, alpha=alpha, x=x)):
        raise RuntimeError("seeded local propagation")
    if weighted_join_mass((edge,), (packet,), h_scale=h_scale) != 1:
        raise RuntimeError("labelled join")
    separated = Packet(8, 3, 2, 5, 1, "packet-B")
    if weighted_join_mass((edge,), (separated,), h_scale=h_scale) != 0:
        raise RuntimeError("support separation")
    if loop_holonomy_difference(h0=30, h_final=30, alpha=alpha) != 0:
        raise RuntimeError("trivial loop")
    if loop_holonomy_difference(h0=30, h_final=29, alpha=alpha) == 0:
        raise RuntimeError("nontrivial loop cannot close exactly")
    return {
        "compatible_join_mass": 1,
        "disjoint_support_join_mass": 0,
        "seeded_propagation": "exact",
        "loop_holonomy": "nontrivial same-label loop has nonzero residual difference",
    }


if __name__ == "__main__":
    print(exact_examples())
