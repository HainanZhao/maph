"""Exact Cycle-169 unnormalized source-pushforward label-energy calculus."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class SourceAtom:
    source: str
    weight: int
    edge_label: int | None
    packet_label: int | None
    edge_multiplicity: int = 1
    packet_multiplicity: int = 1


def pushforwards(atoms: Iterable[SourceAtom]) -> tuple[dict[int, int], dict[int, int]]:
    edges: dict[int, int] = {}
    packets: dict[int, int] = {}
    for atom in atoms:
        if min(atom.weight, atom.edge_multiplicity, atom.packet_multiplicity) < 0:
            raise ValueError("negative source data")
        if atom.edge_label is not None:
            edges[atom.edge_label] = edges.get(atom.edge_label, 0) + atom.weight * atom.edge_multiplicity
        if atom.packet_label is not None:
            packets[atom.packet_label] = packets.get(atom.packet_label, 0) + atom.weight * atom.packet_multiplicity
    return edges, packets


def mixed_label_energy(edges: dict[int, int], packets: dict[int, int]) -> int:
    if any(value < 0 for value in (*edges.values(), *packets.values())):
        raise ValueError("negative pushforward")
    return sum(edges.get(label, 0) * packets.get(label, 0) for label in set(edges) | set(packets))


def pair_sum_identity(atoms: tuple[SourceAtom, ...]) -> int:
    """Expand sum_L E_L P_L over two independent labelled source copies."""
    return sum(
        left.weight * left.edge_multiplicity * right.weight * right.packet_multiplicity
        for left in atoms
        for right in atoms
        if left.edge_label is not None and left.edge_label == right.packet_label
    )


def source_diagonal_mass(atoms: Iterable[SourceAtom]) -> int:
    """Mass where one source atom was selected into both banks."""
    return sum(
        atom.weight * atom.edge_multiplicity * atom.packet_multiplicity
        for atom in atoms
        if atom.edge_label is not None and atom.edge_label == atom.packet_label
    )


def anticorrelated_model(edge_mass: int, packet_mass: int) -> tuple[SourceAtom, SourceAtom]:
    """A two-label common-source model with prescribed nonnegative margins and M=0."""
    if edge_mass < 0 or packet_mass < 0:
        raise ValueError("negative marginal")
    return (
        SourceAtom("edge-only", edge_mass, 0, None),
        SourceAtom("packet-only", packet_mass, None, 1),
    )


def verify_all() -> dict[str, object]:
    anticorrelated = anticorrelated_model(7, 11)
    edges, packets = pushforwards(anticorrelated)
    if edges != {0: 7} or packets != {1: 11}:
        raise RuntimeError("prescribed marginals")
    if mixed_label_energy(edges, packets) != 0 or pair_sum_identity(anticorrelated) != 0:
        raise RuntimeError("anticorrelation")
    if source_diagonal_mass(anticorrelated) != 0:
        raise RuntimeError("disjoint source selection")
    correlated = (
        SourceAtom("edge", 3, 4, None, edge_multiplicity=2),
        SourceAtom("packet", 5, None, 4, packet_multiplicity=3),
    )
    edge2, packet2 = pushforwards(correlated)
    if mixed_label_energy(edge2, packet2) != 90 or pair_sum_identity(correlated) != 90:
        raise RuntimeError("mixed pair identity")
    return {
        "identity": "sum_L E_L P_L equals the two-independent-source-copy labelled pair sum before any normalization",
        "diagonal_warning": "the same-source diagonal is not the mixed energy; disjoint branch selection can make it zero",
        "no_go": "with two target labels, arbitrary prescribed nonnegative total edge and packet masses admit a common-source anticorrelated model with zero mixed label energy",
        "boundary": "This is a source-pushforward calculus/no-go. It does not use the actual exponential geometry and does not lower-bound label energy, compatibility, recurrence, density, or intervals.",
    }


def theorem_record() -> dict[str, object]:
    return {"epistemic_status": "PROVED", **verify_all()}
