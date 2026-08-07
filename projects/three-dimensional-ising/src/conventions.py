"""Pinned graph, coupling, boundary, and polynomial conventions.

Vertices are lexicographically ordered triples ``(x, y, z)``.  An edge is a
pair ``(u, v)`` with ``u < v`` and a sign ``eta in {+1, -1}``.  A periodic
seam joins coordinate ``n-1`` to coordinate ``0``; an antiperiodic boundary
puts ``eta=-1`` on that seam.  Periodic axes must have length at least three,
so the graph remains simple and no length-two parallel-edge convention is
hidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


Vertex = tuple[int, int, int]


@dataclass(frozen=True, order=True)
class Edge:
    u: Vertex
    v: Vertex
    eta: int = 1

    def __post_init__(self) -> None:
        if not self.u < self.v:
            raise ValueError("edges must use the canonical u < v ordering")
        if self.eta not in (-1, 1):
            raise ValueError("eta must be +1 or -1")


def cubic_box(
    shape: tuple[int, int, int],
    *,
    periodic: Iterable[int] = (),
    antiperiodic: Iterable[int] = (),
) -> tuple[tuple[Vertex, ...], tuple[Edge, ...]]:
    """Return a simple cubic box with pinned seam signs.

    ``periodic`` and ``antiperiodic`` contain axis indices.  An antiperiodic
    axis is periodic with negative seam couplings and must not also appear in
    ``periodic``.
    """

    if len(shape) != 3 or any(n < 1 for n in shape):
        raise ValueError("shape must contain three positive lengths")
    periodic_axes = frozenset(periodic)
    antiperiodic_axes = frozenset(antiperiodic)
    if periodic_axes & antiperiodic_axes:
        raise ValueError("an axis cannot be both periodic and antiperiodic")
    wrapped_axes = periodic_axes | antiperiodic_axes
    if not wrapped_axes <= {0, 1, 2}:
        raise ValueError("axis indices are 0, 1, 2")
    if any(shape[axis] < 3 for axis in wrapped_axes):
        raise ValueError("wrapped axes must have length at least three")

    vertices = tuple(
        (x, y, z)
        for x in range(shape[0])
        for y in range(shape[1])
        for z in range(shape[2])
    )
    edges: list[Edge] = []
    for u in vertices:
        for axis in range(3):
            coordinate = u[axis]
            if coordinate + 1 < shape[axis]:
                v_list = list(u)
                v_list[axis] += 1
                v = tuple(v_list)
                edges.append(Edge(min(u, v), max(u, v), 1))
            elif axis in wrapped_axes:
                v_list = list(u)
                v_list[axis] = 0
                v = tuple(v_list)
                eta = -1 if axis in antiperiodic_axes else 1
                edges.append(Edge(min(u, v), max(u, v), eta))
    if len({(edge.u, edge.v) for edge in edges}) != len(edges):
        raise AssertionError("cubic_box unexpectedly produced parallel edges")
    return vertices, tuple(sorted(edges))


def free_box_counts(shape: tuple[int, int, int]) -> tuple[int, int]:
    """Return ``(|V|, |E|)`` for a free rectangular cubic box."""

    a, b, c = shape
    return a * b * c, (a - 1) * b * c + a * (b - 1) * c + a * b * (c - 1)


def orientable_genus_lower_bound_for_free_box(shape: tuple[int, int, int]) -> int:
    """Euler/girth lower bound for the orientable genus of a free box graph.

    A cellular embedding of a simple bipartite bridgeless graph has face
    length at least four, hence ``g >= 1-|V|/2+|E|/4``.  Degenerate boxes with
    bridges are deliberately rejected rather than silently applying that
    argument.
    """

    if sum(n == 1 for n in shape) >= 2:
        raise ValueError("the face-length argument requires a bridgeless box")
    vertices, edges = free_box_counts(shape)
    numerator = 4 - 2 * vertices + edges
    # g >= (4 - 2V + E)/4; integer ceiling without floats.
    return max(0, -(-numerator // 4))
