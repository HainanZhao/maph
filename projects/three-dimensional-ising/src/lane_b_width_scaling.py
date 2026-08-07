"""Width-scaling constructions and certified genus bounds for Gate B5."""

from __future__ import annotations

from itertools import product

from src.conventions import Vertex, cubic_box


Rotation = dict[Vertex, tuple[Vertex, ...]]


def physical_frontier_dimension(w: int) -> int:
    if w < 1:
        raise ValueError("width must be positive")
    return 1 << (w * w - 1)


def constructed_genus_slope(w: int) -> int:
    """Per-slice genus slope in the Millichap--Salinas constructions."""
    if w < 2:
        return 0
    return ((w - 1) * (w - 1)) // 4


def genus_bounds(n: int, w: int) -> tuple[int, int]:
    """Return proved orientable-genus bounds used in Gate B5.

    Widths two and three use Millichap--Salinas Theorems 3 and 4.  At width
    four, even ``n`` is the all-odd-parameter quadrangulation of Proposition 2;
    odd ``n`` uses the girth lower bound and Proposition 3 upper construction.
    """
    if n < 2 or w not in (2, 3, 4):
        raise ValueError("the certified table covers n>=2 and w in {2,3,4}")
    if w == 2:
        return 0, 0
    if w == 3:
        return n - 1, n - 1
    if n % 2 == 0:
        return 2 * n - 3, 2 * n - 3
    return 2 * n - 3, 2 * n - 2


def checkerboard_boundary_rotation(n: int, w: int) -> Rotation:
    """Quadrangular embedding for even ``n,w`` from Proposition 2.

    The surface is the oriented boundary of the union of unit cubes whose
    lower corner has at least two even coordinates.  All three grid parameters
    ``(n-1,w-1,w-1)`` are then odd.
    """
    if n < 2 or w < 2 or n % 2 or w % 2:
        raise ValueError("the checkerboard boundary requires even n and w")
    shape = (n, w, w)
    parameters = tuple(size - 1 for size in shape)
    cells = {
        cell
        for cell in product(*(range(parameter) for parameter in parameters))
        if sum(coordinate % 2 == 0 for coordinate in cell) >= 2
    }
    cross = {
        (1, 2): (0, 1),
        (2, 0): (1, 1),
        (0, 1): (2, 1),
        (2, 1): (0, -1),
        (0, 2): (1, -1),
        (1, 0): (2, -1),
    }
    successor: dict[tuple[Vertex, Vertex], Vertex] = {}
    for cell in sorted(cells):
        for axis in range(3):
            for sign in (-1, 1):
                neighbour = list(cell)
                neighbour[axis] += sign
                if tuple(neighbour) in cells:
                    continue
                base = list(cell)
                if sign == 1:
                    base[axis] += 1
                first, second = (coordinate for coordinate in range(3) if coordinate != axis)
                if cross[first, second] != (axis, sign):
                    first, second = second, first
                face: list[Vertex] = []
                for delta_first, delta_second in ((0, 0), (1, 0), (1, 1), (0, 1)):
                    vertex = base[:]
                    vertex[first] += delta_first
                    vertex[second] += delta_second
                    face.append(tuple(vertex))
                for index, vertex in enumerate(face):
                    key = vertex, face[index - 1]
                    value = face[(index + 1) % 4]
                    if key in successor and successor[key] != value:
                        raise AssertionError("oriented surface faces are inconsistent")
                    successor[key] = value

    vertices, edges = cubic_box(shape)
    adjacency = {vertex: [] for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    rotation: Rotation = {}
    for vertex in vertices:
        neighbours = adjacency[vertex]
        cyclic = [min(neighbours)]
        while len(cyclic) < len(neighbours):
            cyclic.append(successor[vertex, cyclic[-1]])
        if successor[vertex, cyclic[-1]] != cyclic[0] or set(cyclic) != set(neighbours):
            raise AssertionError("boundary faces did not define a rotation system")
        rotation[vertex] = tuple(cyclic)
    return rotation


def symbolic_rank_upper_bound(w: int) -> int:
    """Candidate binary-coordinate bound for a local repeated-handle ansatz.

    A slice frontier contributes ``2^(w^2-1)``.  If a construction adds at most
    ``d=floor((w-1)^2/4)`` handles per step.  Its ``2d`` homology bits can cross
    a local character cut, and the quadratic-refinement sign has cross rank at
    most ``2^(2d)``.  Multiplying the two rank bounds gives the result.  This
    helper does not assert that the required local construction exists for all
    ``w``; Gate B6 must settle that premise.
    """
    d = constructed_genus_slope(w)
    return 1 << (w * w - 1 + 4 * d)
