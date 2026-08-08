#!/usr/bin/env python3
"""Generate and audit the encoder boundary-incidence tables.

The symbolic route uses only unit-square boundary formulas.  The firewall
route independently selects square face walks from the fixed ribbon rotation.
No finite-field arithmetic enters this combinatorial identity.
"""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from discovery.audit_g1_explicit_common_basis import excluded_pairs  # noqa: E402
from discovery.audit_g1_opposite_explicit_all_width import (  # noqa: E402
    exceptional_pairs as opposite_exceptional_pairs,
    opposite_checkerboard_rotation,
)
from proof.verify_g1_arbitrary_width_generic_tightness import (  # noqa: E402
    _components,
    _edge_faces,
    _square_descriptor,
)
from proof.verify_g1_buffered_factorization import (  # noqa: E402
    _gauge_pairs,
    _opposite_tree_pairs,
)
from proof.verify_lane_b_genus3 import _rotation_faces  # noqa: E402
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
)


Axis = int
Vertex = tuple[int, int, int]
EdgePair = tuple[Vertex, Vertex]
EdgeKey = tuple[Axis, int, int, int]
FaceKey = tuple[Axis, int, int, int]


def edge_pair(axis: Axis, x: int, y: int, z: int) -> EdgePair:
    left = (x, y, z)
    right = [x, y, z]
    right[axis] += 1
    return tuple(sorted((left, tuple(right))))  # type: ignore[return-value]


def edge_key(pair: EdgePair) -> EdgeKey:
    left, right = pair
    axis = next(index for index in range(3) if left[index] != right[index])
    return (axis, *left)


def face_edges(face: FaceKey) -> tuple[EdgeKey, EdgeKey, EdgeKey, EdgeKey]:
    """Boundary of one positive unit square as unoriented edge keys."""
    fixed, x, y, z = face
    lower = [x, y, z]
    moving = [axis for axis in range(3) if axis != fixed]
    first, second = moving
    at_second = lower[:]
    at_second[second] += 1
    at_first = lower[:]
    at_first[first] += 1
    return (
        (first, *lower),
        (first, *at_second),
        (second, *lower),
        (second, *at_first),
    )


def incidence(faces: Iterable[FaceKey]) -> tuple[frozenset[EdgeKey], frozenset[EdgeKey]]:
    counts: Counter[EdgeKey] = Counter()
    for face in faces:
        counts.update(face_edges(face))
    if any(value not in (1, 2) for value in counts.values()):
        raise AssertionError(f"nonmanifold selected face incidence: {counts}")
    internal = frozenset(edge for edge, value in counts.items() if value == 2)
    boundary = frozenset(edge for edge, value in counts.items() if value == 1)
    return internal, boundary


def normal_face_sets(width: int) -> dict[str, frozenset[FaceKey]]:
    if width < 4:
        raise ValueError("normal island formulas start at width four")
    result = {
        "I_3": frozenset((0, 0, y, 2) for y in range(3)),
    }
    if width >= 6:
        result["I_5"] = frozenset((0, 0, y, 0) for y in range(5))
    for r in range(3, width // 2):
        result[f"I_{{2,{r}}}"] = frozenset({
            (0, 0, 2 * r - 1, 0),
            (0, 0, 2 * r, 0),
        })
    return result


def opposite_cut_faces(width: int) -> frozenset[FaceKey]:
    if width < 6 or width % 2:
        raise ValueError("the symbolic opposite cut is for even width at least six")
    result: set[FaceKey] = set()
    result |= {(1, x, y, 0) for x in (0, 2) for y in range(width)}
    result |= {(1, x, y, 0) for x in (1, 3) for y in (0, width - 1)}
    result |= {
        (2, x, y, 0)
        for x in (0, 2)
        for y in range(0, width - 1, 2)
    }
    result |= {
        (2, x, y, 0)
        for x in (1, 3)
        for y in range(width - 1)
    }
    result |= {
        (0, x, y, 0)
        for x in range(4)
        for y in range(1, width - 2, 2)
    }
    result |= {(0, 4, y, 0) for y in range(width - 1)}
    result |= {
        (2, x, y, 1)
        for x in (1, 3)
        for y in range(1, width - 2, 2)
    }
    return frozenset(result)


def expected_normal(width: int, name: str) -> dict[str, frozenset[EdgeKey]]:
    if name == "I_3":
        return {
            "internal": frozenset({(2, 0, 1, 2), (2, 0, 2, 2)}),
            "gauge": frozenset(
                {(1, 0, y, z) for y in range(3) for z in (2, 3)}
                | {(2, 0, 0, 2)}
            ),
            "exceptional": frozenset({(2, 0, 3, 2)}),
        }
    if name == "I_5":
        return {
            "internal": frozenset((2, 0, j, 0) for j in range(1, 5)),
            "gauge": frozenset(
                {(1, 0, y, z) for y in range(5) for z in (0, 1)}
                | {(2, 0, 0, 0)}
            ),
            "exceptional": frozenset({(2, 0, 5, 0)}),
        }
    if not name.startswith("I_{2,"):
        raise KeyError(name)
    r = int(name[5:-1])
    return {
        "internal": frozenset({(2, 0, 2 * r, 0)}),
        "gauge": frozenset(
            (1, 0, y, z)
            for y in (2 * r - 1, 2 * r)
            for z in (0, 1)
        ),
        "exceptional": frozenset({
            (2, 0, 2 * r - 1, 0),
            (2, 0, 2 * r + 1, 0),
        }),
    }


def expected_opposite_boundary(width: int) -> dict[str, frozenset[EdgeKey]]:
    return {
        "gauge": frozenset(
            {(2, 0, 0, 0)}
            | {(1, 0, y, 0) for y in range(width - 1)}
            | {(1, 0, y, 1) for y in range(1, width - 2, 2)}
            | {(0, x, y, 1) for x in range(4) for y in range(width)}
        ),
        "exceptional": frozenset({(2, 0, width - 1, 0)}),
        "retained": frozenset((1, 4, 2 * j, 1) for j in range(width // 2)),
    }


def face_walk_boundary(
    width: int,
    phase: str,
    selected: frozenset[FaceKey],
) -> frozenset[EdgeKey]:
    vertices, edges = cubic_box((5, width, width))
    rotation = (
        universal_checkerboard_rotation(5, width)
        if phase == "normal"
        else opposite_checkerboard_rotation(width)
    )
    _, walks = _rotation_faces(vertices, edges, rotation)
    descriptors = {
        _square_descriptor(walk): walk
        for walk in walks
        if _square_descriptor(walk) is not None
    }
    missing = selected - descriptors.keys()
    if missing:
        raise AssertionError(f"{phase} phase is missing selected square faces: {sorted(missing)}")
    boundary: set[EdgeKey] = set()
    for descriptor in selected:
        walk = descriptors[descriptor]
        for offset, left in enumerate(walk):
            right = walk[(offset + 1) % len(walk)]
            boundary.symmetric_difference_update({edge_key(tuple(sorted((left, right))))})
    return frozenset(boundary)


def pair_keys(pairs: Iterable[EdgePair]) -> frozenset[EdgeKey]:
    return frozenset(edge_key(pair) for pair in pairs)


def dual_components(
    width: int,
    phase: str,
    deleted: frozenset[EdgeKey],
) -> tuple[list[frozenset[int]], list[FaceKey | None]]:
    vertices, edges = cubic_box((5, width, width))
    rotation = (
        universal_checkerboard_rotation(5, width)
        if phase == "normal"
        else opposite_checkerboard_rotation(width)
    )
    face_masks, walks = _rotation_faces(vertices, edges, rotation)
    edge_faces = _edge_faces(edges, walks)
    retained = {
        index for index, edge in enumerate(edges)
        if edge_key((edge.u, edge.v)) not in deleted
    }
    components = _components(len(face_masks), edge_faces, retained)
    descriptors = [_square_descriptor(walk) for walk in walks]
    return components, descriptors


def descriptor_indices(
    descriptors: list[FaceKey | None], faces: frozenset[FaceKey]
) -> frozenset[int]:
    lookup = {descriptor: index for index, descriptor in enumerate(descriptors)}
    missing = faces - lookup.keys()
    if missing:
        raise AssertionError(f"missing component descriptors: {sorted(missing)}")
    return frozenset(lookup[face] for face in faces)


def audit_width(width: int) -> dict[str, object]:
    gauge = pair_keys(_gauge_pairs(width))
    normal_exceptional = pair_keys(excluded_pairs(width))
    opposite_tree = pair_keys(_opposite_tree_pairs(width))
    opposite_exceptional = pair_keys(opposite_exceptional_pairs(width))
    opposite_retained = opposite_tree - gauge - opposite_exceptional

    normal_rows = []
    normal_sets = normal_face_sets(width)
    normal_components, normal_descriptors = dual_components(
        width, "normal", gauge | normal_exceptional
    )
    expected_island_indices = {
        descriptor_indices(normal_descriptors, faces)
        for faces in normal_sets.values()
    }
    actual_island_indices = {
        component for component in normal_components
        if component in expected_island_indices
    }
    if actual_island_indices != expected_island_indices:
        raise AssertionError((width, "normal island component mismatch"))
    if len(normal_components) != len(expected_island_indices) + 1:
        raise AssertionError((width, "normal large-component count", len(normal_components)))
    for name, faces in normal_sets.items():
        internal, boundary = incidence(faces)
        expected = expected_normal(width, name)
        expected_boundary = expected["gauge"] | expected["exceptional"]
        if internal != expected["internal"] or boundary != expected_boundary:
            raise AssertionError((width, name, internal ^ expected["internal"], boundary ^ expected_boundary))
        if not expected["gauge"] <= gauge:
            raise AssertionError((width, name, "declared gauge edge is not in T0"))
        if not expected["exceptional"] <= normal_exceptional:
            raise AssertionError((width, name, "declared exceptional edge is not in X+"))
        walked = face_walk_boundary(width, "normal", faces)
        if walked != boundary:
            raise AssertionError((width, name, "normal face-walk firewall", walked ^ boundary))
        normal_rows.append({
            "name": name,
            "face_count": len(faces),
            "internal_count": len(internal),
            "gauge_boundary_count": len(expected["gauge"]),
            "exceptional_boundary_count": len(expected["exceptional"]),
            "is_dual_component": True,
            "unclassified_count": 0,
        })

    opposite_row: dict[str, object]
    if width == 4:
        opposite_row = {"case": "width-four base trace", "applicable": False}
    elif width % 2:
        if opposite_exceptional:
            raise AssertionError((width, "odd opposite exceptional set is nonempty"))
        opposite_row = {"case": "odd width: no exceptional chord", "applicable": False}
    else:
        faces = opposite_cut_faces(width)
        _, boundary = incidence(faces)
        expected = expected_opposite_boundary(width)
        expected_boundary = expected["gauge"] | expected["exceptional"] | expected["retained"]
        if boundary != expected_boundary:
            raise AssertionError((width, "opposite symbolic boundary", boundary ^ expected_boundary))
        if not expected["gauge"] <= gauge:
            raise AssertionError((width, "opposite gauge classification"))
        if expected["exceptional"] != opposite_exceptional:
            raise AssertionError((width, "opposite exceptional classification"))
        if not expected["retained"] <= opposite_retained:
            raise AssertionError((width, "opposite retained classification"))
        walked = face_walk_boundary(width, "opposite", faces)
        if walked != boundary:
            raise AssertionError((width, "opposite face-walk firewall", walked ^ boundary))
        connected_before, _ = dual_components(
            width, "opposite", gauge | opposite_retained
        )
        if len(connected_before) != 1:
            raise AssertionError((width, "opposite complement disconnected before X"))
        split_after, split_descriptors = dual_components(
            width, "opposite", gauge | opposite_retained | opposite_exceptional
        )
        cut_indices = descriptor_indices(split_descriptors, faces)
        if len(split_after) != 2 or cut_indices not in split_after:
            raise AssertionError((width, "opposite cut is not one bridge component"))
        opposite_row = {
            "case": "even symbolic cut",
            "applicable": True,
            "face_count": len(faces),
            "gauge_boundary_count": len(expected["gauge"]),
            "exceptional_boundary_count": len(expected["exceptional"]),
            "retained_boundary_count": len(expected["retained"]),
            "connected_before_exceptional_deletion": True,
            "components_after_exceptional_deletion": 2,
            "unclassified_count": 0,
        }
    return {
        "width": width,
        "normal": normal_rows,
        "opposite": opposite_row,
    }


def build_payload() -> dict[str, object]:
    rows = [audit_width(width) for width in range(4, 9)]
    return {
        "status": "PROVED symbolic unit-square boundary identities; finite face-walk firewall",
        "conventions": {
            "normal_phase": "global checkerboard layers 0..4",
            "opposite_phase": "global checkerboard layers 1..5 translated to 0..4",
            "width_firewall": [4, 5, 6, 7, 8],
            "arithmetic": "GF(2) cellular boundary only; no prime specialization enters",
        },
        "symbolic_patterns": {
            "normal": ["I_3", "I_5 for W>=6", "I_{2,r} for 3<=r<floor(W/2)"],
            "opposite": [
                "T0: e_z(0,0,0)",
                "T0: e_y(0,y,0), 0<=y<=W-2",
                "T0: e_y(0,y,1), odd 1<=y<=W-3",
                "T0: e_x(x,y,1), 0<=x<=3, 0<=y<W",
                "X-: e_z(0,W-1,0)",
                "P-: e_y(4,2j,1), 0<=j<W/2",
            ],
        },
        "rows": rows,
        "claim_boundary": (
            "The symbolic square-boundary identities are arbitrary-width algebraic identities. "
            "Widths 4..8 independently audit their placement in the fixed ribbon rotations; "
            "the finite rows do not prove the encoder parent recurrences."
        ),
    }


def render_latex(payload: dict[str, object]) -> str:
    rows = payload["rows"]
    lines = [
        "% Generated by proof/generate_encoder_incidence_tables.py; do not edit.",
        "\\begin{center}",
        "\\small",
        "\\begin{tabular}{c|c|c|c}",
        "\\toprule",
        "width & normal islands $(|I|;\\,\\mathrm{int}/T^0/X^+)$ & opposite $(|C|;\\,T^0/X^-/P^-)$ & unclassified \\\\",
        "\\midrule",
    ]
    for row in rows:  # type: ignore[assignment]
        normal = row["normal"]
        names = ";\\;".join(
            f'{item["name"]}:{item["face_count"]};'
            f'{item["internal_count"]}/{item["gauge_boundary_count"]}/'
            f'{item["exceptional_boundary_count"]}'
            for item in normal
        )
        opposite = row["opposite"]
        if opposite.get("applicable"):
            opposite_case = (
                f'${opposite["face_count"]};'
                f'{opposite["gauge_boundary_count"]}/'
                f'{opposite["exceptional_boundary_count"]}/'
                f'{opposite["retained_boundary_count"]}$'
            )
        else:
            opposite_case = str(opposite["case"]).replace("_", "\\_")
        unclassified = sum(item["unclassified_count"] for item in normal)
        unclassified += int(opposite.get("unclassified_count", 0))
        lines.append(
            f'{row["width"]} & ${names}$ & {opposite_case} & {unclassified} \\\\'
        )
    lines.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{center}",
        "",
    ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--emit-tex", type=Path)
    parser.add_argument("--check-tex", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    payload = build_payload()
    latex = render_latex(payload)
    if args.emit_tex:
        if args.emit_tex.exists() and args.emit_tex.read_text() != latex:
            raise FileExistsError(f"refusing to overwrite changed file: {args.emit_tex}")
        args.emit_tex.write_text(latex)
    if args.check_tex and args.check_tex.read_text() != latex:
        raise AssertionError(f"generated LaTeX differs from {args.check_tex}")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        print(hashlib.sha256(latex.encode()).hexdigest())


if __name__ == "__main__":
    main()
