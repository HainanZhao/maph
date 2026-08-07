"""Pinned recursively compatible genus-four rotation for the 5x3x3 box.

Deleting vertices with x=4 and their incident darts recovers exactly the
pinned 4x3x3 rotation. Exact genus and homology-inclusion checks are performed
by the recursive Lane B verifier before use.
"""

from __future__ import annotations

from src.conventions import Vertex


_ROTATION_INDICES: tuple[tuple[int, ...], ...] = (
    (3,9,1),(10,4,2,0),(11,1,5),(0,6,4,12),(7,5,1,13,3),(8,14,2,4),
    (15,7,3),(6,16,8,4),(5,7,17),(12,18,10,0),(9,19,11,13,1),(20,2,14,10),
    (21,9,3,13,15),(14,22,16,12,4,10),(23,13,11,5,17),(6,24,12,16),
    (7,15,13,25,17),(8,16,26,14),(9,21,27,19),(22,20,10,18,28),
    (11,19,23,29),(18,12,24,22,30),(25,13,23,19,31,21),(32,20,22,14,26),
    (25,21,15,33),(16,22,24,34,26),(35,23,17,25),(18,30,36,28),
    (31,19,27,37,29),(32,28,38,20),(39,27,21,31,33),(28,32,40,34,30,22),
    (35,41,31,29,23),(42,30,34,24),(31,43,35,25,33),(34,44,32,26),
    (27,39,37),(36,40,38,28),(41,29,37),(42,40,36,30),(41,37,39,43,31),
    (38,40,32,44),(43,39,33),(34,40,42,44),(43,41,35),
)


def _vertex(index: int) -> Vertex:
    return index // 9, (index % 9) // 3, index % 3


BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION: dict[Vertex, tuple[Vertex, ...]] = {
    _vertex(index): tuple(_vertex(neighbour) for neighbour in cyclic)
    for index, cyclic in enumerate(_ROTATION_INDICES)
}
