"""Pinned minimum-genus candidate rotation for the held-out 5x3x3 box.

Integer vertex labels are ``9*x + 3*y + z``. Exact minimum-genus validation
is performed by the Cycle 4 verifier before this rotation is used.
"""

from __future__ import annotations

from src.conventions import Vertex


_ROTATION_INDICES: tuple[tuple[int, ...], ...] = (
    (3, 1, 9), (2, 10, 0, 4), (1, 5, 11), (12, 6, 4, 0),
    (1, 3, 7, 13, 5), (4, 14, 8, 2), (15, 7, 3), (6, 8, 16, 4),
    (7, 5, 17), (12, 0, 10, 18), (1, 11, 13, 19, 9), (14, 10, 2, 20),
    (3, 9, 21, 13, 15), (14, 4, 16, 12, 22, 10), (13, 11, 23, 17, 5),
    (16, 24, 6, 12), (25, 15, 13, 7, 17), (26, 16, 8, 14),
    (9, 19, 27, 21), (10, 22, 20, 28, 18), (29, 19, 23, 11),
    (30, 24, 22, 12, 18), (19, 13, 21, 25, 31, 23), (14, 20, 22, 32, 26),
    (33, 15, 25, 21), (24, 16, 26, 34, 22), (23, 35, 25, 17),
    (28, 36, 30, 18), (27, 19, 29, 31, 37), (32, 28, 20, 38),
    (31, 33, 21, 27, 39), (30, 40, 28, 32, 22, 34), (41, 35, 23, 31, 29),
    (24, 30, 34, 42), (33, 31, 25, 35, 43), (26, 32, 44, 34),
    (39, 27, 37), (36, 28, 40, 38), (41, 29, 37), (40, 30, 36, 42),
    (31, 39, 43, 41, 37), (40, 44, 32, 38), (39, 33, 43),
    (42, 34, 44, 40), (43, 35, 41),
)


def _vertex(index: int) -> Vertex:
    return index // 9, (index % 9) // 3, index % 3


BOX_5X3X3_GENUS_FOUR_ROTATION: dict[Vertex, tuple[Vertex, ...]] = {
    _vertex(index): tuple(_vertex(neighbour) for neighbour in cyclic)
    for index, cyclic in enumerate(_ROTATION_INDICES)
}
