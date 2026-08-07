"""Pinned growing-genus rotation system for the Lane B experiment.

The integer vertex label is ``9*x + 3*y + z``.  The rotation was found by the
exploratory search in ``discovery/search_rotation.cpp`` and is independently
validated by the proof script before use.
"""

from __future__ import annotations

from src.conventions import Vertex


_ROTATION_INDICES: tuple[tuple[int, ...], ...] = (
    (3, 9, 1),
    (10, 4, 2, 0),
    (11, 1, 5),
    (0, 6, 4, 12),
    (7, 5, 1, 13, 3),
    (8, 14, 2, 4),
    (15, 7, 3),
    (6, 16, 8, 4),
    (5, 7, 17),
    (12, 18, 10, 0),
    (9, 19, 11, 13, 1),
    (20, 2, 14, 10),
    (21, 9, 3, 13, 15),
    (14, 22, 16, 12, 4, 10),
    (23, 13, 11, 5, 17),
    (6, 24, 12, 16),
    (7, 15, 13, 25, 17),
    (8, 16, 26, 14),
    (9, 21, 27, 19),
    (22, 20, 10, 18, 28),
    (11, 19, 23, 29),
    (18, 12, 24, 22, 30),
    (25, 13, 23, 19, 31, 21),
    (32, 20, 22, 14, 26),
    (25, 21, 15, 33),
    (16, 22, 24, 34, 26),
    (35, 23, 17, 25),
    (18, 30, 28),
    (31, 19, 27, 29),
    (32, 28, 20),
    (27, 21, 31, 33),
    (28, 32, 34, 30, 22),
    (35, 31, 29, 23),
    (30, 34, 24),
    (31, 35, 25, 33),
    (34, 32, 26),
)


def _vertex(index: int) -> Vertex:
    return index // 9, (index % 9) // 3, index % 3


BOX_4X3X3_GENUS_THREE_ROTATION: dict[Vertex, tuple[Vertex, ...]] = {
    _vertex(index): tuple(_vertex(neighbour) for neighbour in cyclic)
    for index, cyclic in enumerate(_ROTATION_INDICES)
}
