"""Pinned deletion-compatible minimum-genus rotation for the 6x3x3 box.

Deleting vertices with x=5 and their incident darts recovers exactly the
pinned recursive 5x3x3 rotation.  The exact genus-five certificate is checked
by ``proof/verify_lane_b_recursive6.py`` before this rotation is used.
"""

from __future__ import annotations

from src.conventions import Vertex


_ROTATION_INDICES: tuple[tuple[int, ...], ...] = (
    (3,9,1),(10,4,2,0),(11,1,5),(0,6,4,12),(7,5,1,13,3),(8,14,2,4),
    (15,7,3),(6,16,8,4),(5,7,17),(12,18,10,0),(9,19,11,13,1),
    (20,2,14,10),(21,9,3,13,15),(14,22,16,12,4,10),(23,13,11,5,17),
    (6,24,12,16),(7,15,13,25,17),(8,16,26,14),(9,21,27,19),
    (22,20,10,18,28),(11,19,23,29),(18,12,24,22,30),
    (25,13,23,19,31,21),(32,20,22,14,26),(25,21,15,33),
    (16,22,24,34,26),(35,23,17,25),(18,30,36,28),(31,19,27,37,29),
    (32,28,38,20),(39,27,21,31,33),(28,32,40,34,30,22),
    (35,41,31,29,23),(42,30,34,24),(31,43,35,25,33),(34,44,32,26),
    (27,39,45,37),(36,46,40,38,28),(41,47,29,37),(42,40,48,36,30),
    (41,37,49,39,43,31),(38,40,32,44,50),(43,39,33,51),
    (34,40,42,52,44),(43,53,41,35),(36,48,46),(45,47,49,37),
    (50,46,38),(45,39,49,51),(50,52,48,40,46),(41,53,49,47),
    (48,52,42),(43,51,49,53),(52,50,44),
)


def _vertex(index: int) -> Vertex:
    return index // 9, (index % 9) // 3, index % 3


BOX_6X3X3_RECURSIVE_GENUS_FIVE_ROTATION: dict[Vertex, tuple[Vertex, ...]] = {
    _vertex(index): tuple(_vertex(neighbour) for neighbour in cyclic)
    for index, cyclic in enumerate(_ROTATION_INDICES)
}
