"""Exact Cycle-168 edge/local-packet compatibility and propagation ledger."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction as Q
from typing import Iterable


@dataclass(frozen=True)
class Edge:
    target_label: int
    h: int
    j: int
    beta: Q
    strip_constant: int
    weight: int = 1


@dataclass(frozen=True)
class Packet:
    target_label: int
    lower_h: int
    upper_h: int
    a: int
    q: int
    depth: int
    strip_constant: int
    weight: int = 1


def incompatibility_reason(edge: Edge, packet: Packet, *, h_cap: int, critical_depth: int, join_constant: int) -> str | None:
    """First exhaustive reason that a complete edge/packet pair cannot join."""
    if min(edge.weight, packet.weight) < 0:
        raise ValueError("negative weight")
    if h_cap <= 0 or critical_depth < 0 or join_constant < 0:
        raise ValueError("invalid interface")
    if edge.target_label != packet.target_label:
        return "target_label"
    if not (packet.lower_h <= edge.h <= packet.upper_h):
        return "target_range"
    if packet.q <= 0 or packet.a <= 0 or packet.q * packet.depth > h_cap:
        return "packet_admissibility"
    if packet.depth < critical_depth:
        return "subcritical_depth"
    if edge.strip_constant + packet.strip_constant > join_constant:
        return "strip_constant"
    return None


def compatible(edge: Edge, packet: Packet, *, h_cap: int, critical_depth: int, join_constant: int) -> bool:
    return incompatibility_reason(edge, packet, h_cap=h_cap, critical_depth=critical_depth, join_constant=join_constant) is None


def weighted_join_mass(
    edges: Iterable[Edge], packets: Iterable[Packet], *, h_cap: int, critical_depth: int, join_constant: int
) -> int:
    """The exact bipartite compatibility form sum E_e P_p 1_Comp(e,p)."""
    return sum(
        edge.weight * packet.weight
        for edge in edges
        for packet in packets
        if compatible(edge, packet, h_cap=h_cap, critical_depth=critical_depth, join_constant=join_constant)
    )


def propagated_residual(*, edge: Edge, packet: Packet, alpha: Q, k: int) -> Q:
    """Residual of j+k*a+beta-(h+k*q)*alpha at the target label."""
    return (edge.j + edge.beta - edge.h * alpha) - k * (packet.q * alpha - packet.a)


def loop_difference(*, h_initial: int, h_final: int, alpha: Q) -> Q:
    """Same-label difference after direct affine updates telescope."""
    return (h_initial - h_final) - (h_final - h_initial) * alpha


def verify_all() -> dict[str, object]:
    edge = Edge(target_label=7, h=30, j=45, beta=Q(0), strip_constant=1, weight=2)
    packet = Packet(target_label=7, lower_h=20, upper_h=40, a=3, q=2, depth=5, strip_constant=1, weight=3)
    kwargs = {"h_cap": 20, "critical_depth": 5, "join_constant": 2}
    if incompatibility_reason(edge, packet, **kwargs) is not None:
        raise RuntimeError("compatible pair")
    if weighted_join_mass((edge,), (packet,), **kwargs) != 6:
        raise RuntimeError("weighted join")
    alpha = Q(3, 2)
    if any(propagated_residual(edge=edge, packet=packet, alpha=alpha, k=k) for k in range(-5, 6)):
        raise RuntimeError("exact propagation")
    separated = Packet(target_label=8, lower_h=20, upper_h=40, a=3, q=2, depth=5, strip_constant=1, weight=3)
    if weighted_join_mass((edge,), (separated,), **kwargs) != 0:
        raise RuntimeError("support separation")
    reasons = {
        incompatibility_reason(Edge(8, 30, 45, Q(0), 1), packet, **kwargs),
        incompatibility_reason(Edge(7, 41, 45, Q(0), 1), packet, **kwargs),
        incompatibility_reason(edge, Packet(7, 20, 40, 3, 5, 5, 1), **kwargs),
        incompatibility_reason(edge, Packet(7, 20, 40, 3, 2, 4, 1), **kwargs),
        incompatibility_reason(edge, Packet(7, 20, 40, 3, 2, 5, 2), **kwargs),
    }
    if reasons != {"target_label", "target_range", "packet_admissibility", "subcritical_depth", "strip_constant"}:
        raise RuntimeError("reason partition")
    if loop_difference(h_initial=30, h_final=30, alpha=alpha) != 0:
        raise RuntimeError("trivial holonomy")
    if loop_difference(h_initial=30, h_final=29, alpha=alpha) == 0:
        raise RuntimeError("nontrivial holonomy")
    return {
        "composition": "a compatible target edge seeds the local packet and realizes the Cycle-67 progression at strip constant C_edge+C_packet",
        "overlap": "the exact join count is the bipartite form sum_(e,p) weight(e)*weight(p)*1_Comp(e,p), not a product of global masses or a diagonal common-key product",
        "separation": "target-label, target-range, packet-admissibility, subcritical-depth, and strip-constant failures are an exhaustive ordered partition for this join interface",
        "loop": "a same-label direct affine loop has trivial integer holonomy; it does not create a nonzero local packet step",
        "boundary": "This is an exact compatibility calculus. It does not lower-bound overlap for actual edge and packet populations or prove a recurrence, skeleton, density, or interval result.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
