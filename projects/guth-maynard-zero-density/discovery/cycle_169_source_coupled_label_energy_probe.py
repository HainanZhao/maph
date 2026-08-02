#!/usr/bin/env python3
"""Exact finite probe for Cycle 169 unnormalized label energy.

Discovery-only: it demonstrates the correct pair-energy identity and why
separate marginal masses cannot establish a common target label.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass


@dataclass(frozen=True)
class SourceAtom:
    source: str
    weight: int
    edge_label: int | None
    packet_label: int | None
    edge_multiplicity: int = 1
    packet_multiplicity: int = 1


def pushforwards(atoms: tuple[SourceAtom, ...]) -> tuple[dict[int, int], dict[int, int]]:
    edges: dict[int, int] = defaultdict(int)
    packets: dict[int, int] = defaultdict(int)
    for atom in atoms:
        if atom.weight < 0 or atom.edge_multiplicity < 0 or atom.packet_multiplicity < 0:
            raise ValueError("negative source data")
        if atom.edge_label is not None:
            edges[atom.edge_label] += atom.weight * atom.edge_multiplicity
        if atom.packet_label is not None:
            packets[atom.packet_label] += atom.weight * atom.packet_multiplicity
    return dict(edges), dict(packets)


def mixed_label_energy(edges: dict[int, int], packets: dict[int, int]) -> int:
    return sum(edges.get(label, 0) * packets.get(label, 0) for label in set(edges) | set(packets))


def pair_sum_identity(atoms: tuple[SourceAtom, ...]) -> int:
    """The two-independent-source-copy expansion of sum_L E_L P_L."""
    return sum(
        left.weight * left.edge_multiplicity * right.weight * right.packet_multiplicity
        for left in atoms
        for right in atoms
        if left.edge_label is not None and left.edge_label == right.packet_label
    )


def separator(atoms: tuple[SourceAtom, ...]) -> dict[str, tuple[str, ...]]:
    """Retain source provenance for edge-only, packet-only, and common labels."""
    edges, packets = pushforwards(atoms)
    edge_only = {label for label in edges if label not in packets}
    packet_only = {label for label in packets if label not in edges}
    common = set(edges) & set(packets)
    return {
        "edge_only_sources": tuple(atom.source for atom in atoms if atom.edge_label in edge_only),
        "packet_only_sources": tuple(atom.source for atom in atoms if atom.packet_label in packet_only),
        "common_sources": tuple(atom.source for atom in atoms if atom.edge_label in common or atom.packet_label in common),
    }


def exact_examples() -> dict[str, object]:
    anticorrelated = (
        SourceAtom("e1", 7, 1, None),
        SourceAtom("p1", 11, None, 2),
    )
    edges, packets = pushforwards(anticorrelated)
    if (sum(edges.values()), sum(packets.values()), mixed_label_energy(edges, packets)) != (7, 11, 0):
        raise RuntimeError("anticorrelation model")
    if pair_sum_identity(anticorrelated) != 0:
        raise RuntimeError("pair identity anticorrelation")
    correlated = (
        SourceAtom("e2", 3, 4, None, edge_multiplicity=2),
        SourceAtom("p2", 5, None, 4, packet_multiplicity=3),
    )
    edge2, packet2 = pushforwards(correlated)
    energy = mixed_label_energy(edge2, packet2)
    if energy != 90 or pair_sum_identity(correlated) != energy:
        raise RuntimeError("mixed identity")
    if separator(anticorrelated)["edge_only_sources"] != ("e1",):
        raise RuntimeError("separator provenance")
    return {
        "anticorrelated_margins": {"edge": 7, "packet": 11, "energy": 0},
        "mixed_pair_identity": energy,
        "provenanced_separator": separator(anticorrelated),
    }


if __name__ == "__main__":
    print(exact_examples())
