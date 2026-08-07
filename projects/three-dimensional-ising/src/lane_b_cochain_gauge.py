"""Pinned transverse cochains for the width-three Lane B gauge quotient."""

from __future__ import annotations

from src.conventions import Edge, cubic_box


SLICE_VERTICES, SLICE_EDGES = cubic_box((1, 3, 3))

# In the nested symplectic coordinates, a bulk slice alternates these two
# ordered mode quadruples (b_left, a_left, b_right, a_right).  Bit positions
# refer to the canonical SLICE_EDGES order.
BULK_MODE_MASKS = (
    (1080, 1056, 452, 320),
    (452, 320, 1080, 1056),
)

# The two b-mode representatives are exact coboundaries.  Potentials are
# 9-bit masks in row-major (y,z) order; complements give the same coboundary.
B_MODE_POTENTIALS = {1080: 79, 452: 27}


def slice_edge_boundary(edge: Edge) -> int:
    return (1 << (3 * edge.u[1] + edge.u[2])) | (1 << (3 * edge.v[1] + edge.v[2]))


def coboundary_mask(potential: int) -> int:
    """Return ``delta potential`` in the pinned transverse-edge order."""
    result = 0
    for index, edge in enumerate(SLICE_EDGES):
        endpoints = slice_edge_boundary(edge)
        if (potential & endpoints).bit_count() & 1:
            result |= 1 << index
    return result


def subset_boundary(edge_subset: int) -> int:
    result = 0
    for index, edge in enumerate(SLICE_EDGES):
        if (edge_subset >> index) & 1:
            result ^= slice_edge_boundary(edge)
    return result


def one_handle_transform_scaled() -> tuple[tuple[int, ...], ...]:
    """Twice the local map from Walsh characters G(mu) to F(lambda)."""
    return (
        (1, 1, 1, -1),
        (1, 1, -1, 1),
        (1, -1, 1, 1),
        (-1, 1, 1, 1),
    )

