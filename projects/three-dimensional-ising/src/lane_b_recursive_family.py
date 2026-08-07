"""Period-two deletion-compatible rotation family for Lx3x3, L >= 4.

The two local extension rules are extracted from the pinned 4->5 and 5->6
rotations.  This module defines the candidate family; proof code verifies its
face and homology properties before use.
"""

from __future__ import annotations

from src.conventions import Vertex
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION
from src.lane_b_recursive import BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION
from src.lane_b_recursive6 import BOX_6X3X3_RECURSIVE_GENUS_FIVE_ROTATION


Rotation = dict[Vertex, tuple[Vertex, ...]]


def _translate(vertex: Vertex, shift: int) -> Vertex:
    return vertex[0] + shift, vertex[1], vertex[2]


def _extend(
    rotation: dict[Vertex, list[Vertex]],
    old_length: int,
    prototype_old: Rotation,
    prototype_extended: Rotation,
    prototype_old_x: int,
) -> None:
    target_old_x=old_length-1
    shift=target_old_x-prototype_old_x
    for y in range(3):
        for z in range(3):
            prototype_vertex=(prototype_old_x,y,z)
            prototype_new=(prototype_old_x+1,y,z)
            old_cyclic=prototype_old[prototype_vertex]
            augmented=prototype_extended[prototype_vertex]
            special=augmented.index(prototype_new)
            predecessor=augmented[(special-1)%len(augmented)]
            successor=augmented[(special+1)%len(augmented)]
            if tuple(neighbour for neighbour in augmented if neighbour!=prototype_new) != old_cyclic:
                raise AssertionError("prototype deletion rule is not exact")
            target_vertex=_translate(prototype_vertex,shift)
            target_predecessor=_translate(predecessor,shift)
            target_successor=_translate(successor,shift)
            target_new=_translate(prototype_new,shift)
            cyclic=rotation[target_vertex]
            position=cyclic.index(target_predecessor)
            if cyclic[(position+1)%len(cyclic)] != target_successor:
                raise AssertionError("translated insertion gap is absent")
            cyclic.insert(position+1,target_new)

    prototype_new_x=prototype_old_x+1
    for y in range(3):
        for z in range(3):
            prototype_vertex=(prototype_new_x,y,z)
            target_vertex=_translate(prototype_vertex,shift)
            rotation[target_vertex]=[
                _translate(neighbour,shift)
                for neighbour in prototype_extended[prototype_vertex]
            ]


def recursive_rotation(length: int) -> Rotation:
    """Return the exact period-two candidate rotation for ``length x 3 x 3``."""
    if length<4:
        raise ValueError("the recursive family starts at length four")
    rotation={vertex:list(cyclic) for vertex,cyclic in BOX_4X3X3_GENUS_THREE_ROTATION.items()}
    for old_length in range(4,length):
        if old_length%2==0:
            _extend(
                rotation,old_length,
                BOX_4X3X3_GENUS_THREE_ROTATION,
                BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION,
                3,
            )
        else:
            _extend(
                rotation,old_length,
                BOX_5X3X3_RECURSIVE_GENUS_FOUR_ROTATION,
                BOX_6X3X3_RECURSIVE_GENUS_FIVE_ROTATION,
                4,
            )
    return {vertex:tuple(cyclic) for vertex,cyclic in rotation.items()}


def cyclically_equal(left: tuple[Vertex, ...], right: tuple[Vertex, ...]) -> bool:
    if len(left)!=len(right):
        return False
    return any(left==right[offset:]+right[:offset] for offset in range(len(right)))
