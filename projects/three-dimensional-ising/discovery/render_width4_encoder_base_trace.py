#!/usr/bin/env python3
"""Render the complete opposite width-four encoder base trace as LaTeX.

The generated table is a human-readable finite witness.  This renderer is an
audit/convenience tool; the printed parent and component data, not this script,
are what the manuscript asks a reader to check.
"""

from __future__ import annotations

from collections import deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_gauge_tree_dual import _gauge_tree  # noqa: E402
from discovery.audit_g1_explicit_all_width_induction import (  # noqa: E402
    _base_tree as normal_base_tree,
)
from discovery.audit_g1_explicit_common_basis import excluded_pairs  # noqa: E402
from discovery.audit_g1_opposite_explicit_all_width import (  # noqa: E402
    base_tree_pairs,
    exceptional_pairs,
    opposite_checkerboard_rotation,
)
from proof.verify_g1_arbitrary_width_generic_tightness import (  # noqa: E402
    _square_descriptor,
)
from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _rotation_faces,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
)


def _vertex(value):
    return "$({},{},{})$".format(*value)


def _face(walk):
    if len(walk) != 4:
        return "$O$"
    axis, x, y, z = _square_descriptor(walk)
    return f"$({axis};{x},{y},{z})$"


def _tree_parents(vertices, edges, selected, root):
    adjacency = {vertex: [] for vertex in vertices}
    for index in selected:
        edge = edges[index]
        adjacency[edge.u].append((edge.v, index))
        adjacency[edge.v].append((edge.u, index))
    seen = {root}
    queue = deque([root])
    parents = []
    while queue:
        parent = queue.popleft()
        for child, index in sorted(adjacency[parent]):
            if child not in seen:
                seen.add(child)
                queue.append(child)
                parents.append((child, parent, index))
    return adjacency, parents, seen


def _root_away_terminals(vertices, edges, tree, removed, terminals, root):
    adjacency = {vertex: [] for vertex in vertices}
    for index in tree:
        if index == removed:
            continue
        edge = edges[index]
        adjacency[edge.u].append(edge.v)
        adjacency[edge.v].append(edge.u)
    seen = {root}
    stack = [root]
    while stack:
        vertex = stack.pop()
        for neighbour in adjacency[vertex]:
            if neighbour not in seen:
                seen.add(neighbour)
                stack.append(neighbour)
    return sorted(set(terminals) - seen)


def build(phase="opposite"):
    width = 4
    vertices, edges = cubic_box((5, width, width))
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    if phase == "opposite":
        tree = {edge_index[pair] for pair in base_tree_pairs()}
        exceptional = {edge_index[pair] for pair in exceptional_pairs(width)}
        rotation = opposite_checkerboard_rotation(width)
    elif phase == "normal":
        tree = set(normal_base_tree())
        exceptional = {edge_index[pair] for pair in excluded_pairs(width)}
        rotation = universal_checkerboard_rotation(5, width)
    else:
        raise ValueError(phase)
    faces, walks = _rotation_faces(
        vertices, edges, rotation
    )
    genus = (2 - (len(vertices) - len(edges) + len(faces))) // 2
    cycles = _cycle_basis(vertices, edges)
    _labels, _face_rank = _edge_homology_labels(
        len(edges), faces, cycles, genus
    )
    gauge = _gauge_tree(len(edges), faces, cycles, genus)
    chords = (tree - gauge) - exceptional

    adjacency, tree_parents, reached = _tree_parents(
        vertices, edges, tree, (0, 0, 0)
    )
    if len(tree) != len(vertices) - 1 or reached != set(vertices):
        raise AssertionError("opposite width-four tree witness failed")

    forest_edges = tree - chords
    unseen = set(vertices)
    components = []
    terminals = {vertex for vertex in vertices if vertex[0] == 4}
    while unseen:
        start = min(unseen)
        unseen.remove(start)
        part = {start}
        stack = [start]
        while stack:
            vertex = stack.pop()
            for neighbour, index in adjacency[vertex]:
                if index in forest_edges and neighbour in unseen:
                    unseen.remove(neighbour)
                    part.add(neighbour)
                    stack.append(neighbour)
        anchors = sorted(part & terminals)
        if len(anchors) != 1:
            raise AssertionError("terminal-forest witness failed")
        components.append((anchors[0], sorted(part)))

    incidences = [[] for _ in edges]
    for face, walk in enumerate(walks):
        for left, right in zip(walk, walk[1:] + walk[:1]):
            incidences[edge_index[tuple(sorted((left, right)))]].append(face)
    if any(len(pair) != 2 for pair in incidences):
        raise AssertionError("noncellular face incidence")
    dual_edges = set(range(len(edges))) - gauge - chords
    dual_adjacency = [[] for _ in faces]
    for index in dual_edges:
        left, right = incidences[index]
        dual_adjacency[left].append((right, index))
        dual_adjacency[right].append((left, index))
    outer = next(index for index, walk in enumerate(walks) if len(walk) != 4)
    dual_seen = {outer}
    queue = deque([outer])
    dual_parents = []
    while queue:
        parent = queue.popleft()
        for child, index in sorted(
            dual_adjacency[parent],
            key=lambda item: (repr(_square_descriptor(walks[item[0]])), item[1]),
        ):
            if child not in dual_seen:
                dual_seen.add(child)
                queue.append(child)
                dual_parents.append((child, parent, index))
    if len(dual_parents) != len(faces) - 1 or len(dual_seen) != len(faces):
        raise AssertionError("dual parent witness failed")

    lines = []
    lines.append(f"\\section{{Complete {phase} width-four encoder base trace}}")
    lines.append(f"\\label{{app:width4-{phase}-trace}}")
    lines.append(
        f"This appendix discharges the finite base case used by the {phase} "
        r"shell induction.  Vertices and edge indices use the convention of "
        r"\cref{app:encoders}.  A face $(a;x,y,z)$ is the unit square with "
        r"fixed coordinate axis $a$ and lower corner $(x,y,z)$; $O$ denotes "
        r"the nonsquare outer face.  Each row below is an explicit incidence "
        r"check, so no program output is needed to infer connectivity."
    )
    lines.append(
        f"The {phase} base contains 80 vertices and the 79 selected tree "
        r"edges printed in \cref{app:encoders}.  Starting at $(0,0,0)$, the "
        r"following table gives one parent edge for every other vertex."
    )
    lines.extend([
        r"\begin{longtable}{@{}rrr@{}}",
        r"\toprule child & parent & edge index\\ \midrule",
        r"\endfirsthead \toprule child & parent & edge index\\ \midrule \endhead",
    ])
    for child, parent, index in tree_parents:
        lines.append(f"{_vertex(child)} & {_vertex(parent)} & ${index}$\\\\")
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    lines.append(
        r"Thus all 80 vertices are reached by 79 selected edges, proving that "
        r"the selected graph is a tree.  Removing the 15 retained chords "
        r"partitions it into the following 16 components; the left entry is "
        r"the unique terminal in the component."
    )
    lines.extend([
        r"\begin{longtable}{@{}p{.13\textwidth}p{.79\textwidth}@{}}",
        r"\toprule terminal & complete vertex set\\ \midrule",
        r"\endfirsthead \toprule terminal & complete vertex set\\ \midrule \endhead",
    ])
    for terminal, part in sorted(components):
        members = ", ".join(_vertex(vertex) for vertex in part)
        lines.append(f"{_vertex(terminal)} & {members}\\\\")
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    lines.append(
        r"Finally delete from the face dual the duals of the 79 gauge-tree "
        r"edges and the 15 retained chords.  The remainder has 90 face "
        r"vertices.  The following 89 parent incidences reach every face from "
        r"$O$; the last column is the primal grid edge crossed by the dual "
        r"parent edge."
    )
    lines.extend([
        r"\begin{longtable}{@{}rrr@{}}",
        r"\toprule child face & parent face & primal edge index\\ \midrule",
        r"\endfirsthead \toprule child face & parent face & primal edge index\\ \midrule \endhead",
    ])
    for child, parent, index in dual_parents:
        lines.append(f"{_face(walks[child])} & {_face(walks[parent])} & ${index}$\\\\")
    lines.extend([r"\bottomrule", r"\end{longtable}"])
    lines.append(
        r"The table is a spanning tree of the retained dual remainder and "
        r"therefore proves its connectivity.  Together, these three printed "
        r"witnesses establish the tree, one-terminal-per-component, and dual "
        f"connectivity assertions for the {phase} width-four base."
    )
    if phase == "opposite":
        without_exceptional = dual_edges - exceptional
        split_adjacency = [[] for _ in faces]
        for index in without_exceptional:
            left, right = incidences[index]
            split_adjacency[left].append(right)
            split_adjacency[right].append(left)
        cut = {outer}
        stack = [outer]
        while stack:
            face = stack.pop()
            for neighbour in split_adjacency[face]:
                if neighbour not in cut:
                    cut.add(neighbour)
                    stack.append(neighbour)
        crossing_chords = []
        for index in tree - gauge:
            left, right = incidences[index]
            if (left in cut) != (right in cut):
                crossing_chords.append(index)
        crossing_chords.sort()
        if crossing_chords != [37, 163, 177]:
            raise AssertionError(crossing_chords)
        cut_faces = ", ".join(_face(walks[face]) for face in sorted(cut))
        lines.append(
            r"For the exceptional width-four relation, remove also edge "
            r"37 from the retained dual remainder.  The component containing "
            r"$O$ is the following complete face set:"
        )
        lines.append(r"\begin{quote}\small " + cut_faces + r".\end{quote}")
        lines.append(
            r"Its non-gauge chord boundary consists exactly of primal edge "
            r"indices $37,163,177$, namely $X=e_z(0,3,2)$, "
            r"$e_y(4,0,1)$, and $e_y(4,2,1)$.  Its face-boundary relation is "
            r"therefore $h_X=h_{e_y(4,0,1)}+h_{e_y(4,2,1)}$."
        )
        terminals_list = sorted(terminals)
        terminal_sides = {
            index: _root_away_terminals(
                vertices, edges, tree, index, terminals_list, (4, 0, 0)
            )
            for index in (37, 65, 109)
        }
        if terminal_sides != {
            37: [(4, 3, 3)],
            65: [(4, 3, 2), (4, 3, 3)],
            109: [(4, 3, 2)],
        }:
            raise AssertionError(terminal_sides)
        lines.append(
            r"For the terminal relation, deleting edge 37 leaves terminal "
            r"set $\{(4,3,3)\}$ away from the root; deleting edge 65 "
            r"($e_z(1,2,1)$) leaves "
            r"$\{(4,3,2),(4,3,3)\}$; and deleting edge 109 "
            r"($e_y(2,2,2)$) leaves $\{(4,3,2)\}$.  Symmetric difference "
            r"therefore gives $u_X=u_{e_z(1,2,1)}+u_{e_y(2,2,2)}$."
        )
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("normal", "opposite"), default="opposite")
    args = parser.parse_args()
    print(build(args.phase), end="")
