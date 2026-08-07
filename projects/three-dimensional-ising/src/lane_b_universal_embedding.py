"""Deletion-compatible checkerboard ribbon embeddings for all grid strips."""

from __future__ import annotations

from src.conventions import Vertex, cubic_box
from src.lane_b_width_scaling import checkerboard_boundary_rotation


Rotation = dict[Vertex, tuple[Vertex, ...]]


def next_even(value: int) -> int:
    if value < 2:
        raise ValueError("grid dimensions must be at least two")
    return value if value % 2 == 0 else value + 1


def universal_checkerboard_rotation(n: int, w: int) -> Rotation:
    """Restrict the next-even checkerboard boundary rotation to ``n x w x w``.

    The parent rotation is the oriented boundary of the union of unit cubes
    whose lower corner has at least two even coordinates.  Restriction means
    deleting absent neighbours from each cyclic vertex order.  The resulting
    rotation is orientable and cellular by the standard ribbon-graph capping
    construction, and is deletion-compatible as ``n`` increases.
    """
    parent_n, parent_w = next_even(n), next_even(w)
    parent = checkerboard_boundary_rotation(parent_n, parent_w)
    vertices, _ = cubic_box((n, w, w))
    retained = set(vertices)
    rotation = {
        vertex: tuple(neighbour for neighbour in parent[vertex] if neighbour in retained)
        for vertex in vertices
    }
    if any(len(cyclic) == 0 for cyclic in rotation.values()):
        raise AssertionError("restriction isolated a grid vertex")
    return rotation


def universal_embedding_genus(n: int, w: int) -> int:
    """Closed formula for the restricted checkerboard rotation genus."""
    if n < 2 or w < 2:
        raise ValueError("grid dimensions must be at least two")
    if w == 2:
        return 0
    if w % 2:
        half = (w - 1) // 2
        return half * half * (n - 1)
    base = 1 + (n * w * (w - 2) - w * w) // 4
    return base if n % 2 == 0 else base + (w - 2) // 2


def interior_atomic_count(w: int) -> int:
    """Number of nonexact transverse atoms on an interior slice."""
    if w < 2:
        raise ValueError("width must be at least two")
    return ((w - 1) * (w - 1)) // 2

