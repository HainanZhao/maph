#!/usr/bin/env python3
"""Exact finite Cech total complexes for Cycle 46."""
from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
import itertools

from lrc_moment_h2_coupling import sparse_solve
from lrc_morse_critical_projection import boundary, boundary_cell, clean


def downward_closure(facets):
    cells = {()}
    for facet in facets:
        facet = tuple(sorted(facet))
        for size in range(1, len(facet) + 1):
            cells.update(itertools.combinations(facet, size))
    return cells


def closed_star(all_cells, vertex):
    """Closed star as a downward-closed set, including the empty cell."""
    return {cell for cell in all_cells if tuple(sorted(set(cell) | {vertex})) in all_cells}


def owner_star_cover(all_cells, pivot_part):
    vertices = sorted(cell[0] for cell in all_cells if len(cell) == 1 and cell[0][0] == pivot_part)
    return vertices, [closed_star(all_cells, vertex) for vertex in vertices]


def intersection_cells(cover, indices):
    common = set(cover[indices[0]])
    for index in indices[1:]:
        common.intersection_update(cover[index])
    return common


def total_basis(cover, degree):
    """Basis (cover-index tuple, nonempty simplex) with p+q=degree."""
    rows = []
    for width in range(1, min(len(cover), degree + 2) + 1):
        p = width - 1
        q = degree - p
        if q < 0:
            continue
        for indices in itertools.combinations(range(len(cover)), width):
            for cell in sorted(intersection_cells(cover, indices)):
                if len(cell) - 1 == q:
                    rows.append((indices, cell))
    return rows


def total_boundary(source_basis, target_basis):
    """Columns of d=(-1)^p d_simplicial+d_Cech, as target sparse rows."""
    target_id = {item: index for index, item in enumerate(target_basis)}
    rows = [dict() for _ in target_basis]
    for column, (indices, cell) in enumerate(source_basis):
        p = len(indices) - 1
        for face, incidence in boundary_cell(cell).items():
            if not face:
                continue
            key = (indices, face)
            if key not in target_id:
                raise AssertionError(("missing vertical face", key))
            rows[target_id[key]][column] = Fraction((-1) ** p) * incidence
        if p:
            for position in range(len(indices)):
                target_indices = indices[:position] + indices[position + 1 :]
                key = (target_indices, cell)
                if key not in target_id:
                    raise AssertionError(("missing horizontal face", key))
                row = rows[target_id[key]]
                row[column] = row.get(column, Fraction(0)) + Fraction((-1) ** position)
    return rows


def apply_matrix(rows, vector):
    result = []
    for row in rows:
        result.append(sum(value * vector.get(column, Fraction(0)) for column, value in row.items()))
    return result


def verify_square_zero(dn, dnm1):
    """Check d_{n-1} d_n=0 using sparse columns."""
    for column in range(max((max(row, default=-1) for row in dn), default=-1) + 1):
        middle = {row_id: row[column] for row_id, row in enumerate(dn) if column in row}
        if any(apply_matrix(dnm1, middle)):
            return False, column
    return True, None


def serialize_chain(chain):
    return [
        [list(indices), [list(vertex) for vertex in cell], value.numerator, value.denominator]
        for (indices, cell), value in sorted(chain.items())
        if value
    ]


def horizontal_boundary(chain):
    result = defaultdict(Fraction)
    for (indices, cell), coefficient in chain.items():
        if len(indices) == 1:
            continue
        for position in range(len(indices)):
            target = (indices[:position] + indices[position + 1 :], cell)
            result[target] += coefficient * Fraction((-1) ** position)
    return clean(result)


def raw_vertical_boundary(chain):
    result = defaultdict(Fraction)
    for (indices, cell), coefficient in chain.items():
        for face, incidence in boundary_cell(cell).items():
            if face:
                result[(indices, face)] += coefficient * incidence
    return clean(result)


def total_chain_boundary(chain):
    result = defaultdict(Fraction, horizontal_boundary(chain))
    for (indices, cell), coefficient in raw_vertical_boundary(chain).items():
        result[(indices, cell)] += Fraction((-1) ** (len(indices) - 1)) * coefficient
    return clean(result)


def horizontal_cone(chain, memberships):
    """Contract an exact positive Cech chain toward the least cover index."""
    result = defaultdict(Fraction)
    for (indices, cell), coefficient in chain.items():
        base = min(memberships[cell])
        if base not in indices:
            result[((base,) + indices, cell)] += coefficient
    result = clean(result)
    if horizontal_boundary(result) != clean(chain):
        raise AssertionError("horizontal contraction identity")
    return result


def canonical_cycle_lift(cycle, cover):
    """Linear exact lift of a covered simplicial cycle into the Cech total complex."""
    memberships = {}
    for cell in set().union(*cover):
        memberships[cell] = tuple(index for index, member in enumerate(cover) if cell in member)
    uncovered = sorted(cell for cell in cycle if cell not in memberships)
    if uncovered:
        return None, uncovered
    current = {((min(memberships[cell]),), cell): value for cell, value in cycle.items() if value}
    lifted = defaultdict(Fraction, current)
    degree = max((len(cell) - 1 for cell in cycle), default=-1)
    for p in range(degree):
        vertical = raw_vertical_boundary(current)
        target = {key: Fraction((-1) ** (p + 1)) * value for key, value in vertical.items()}
        current = horizontal_cone(target, memberships)
        for key, value in current.items():
            lifted[key] += value
    lifted = clean(lifted)
    if total_chain_boundary(lifted):
        raise AssertionError("canonical lift is not a total cycle")
    return lifted, []


def direct_boundary_solve(all_cells, cycle):
    triangles = sorted(cell for cell in all_cells if len(cell) == 3)
    tetrahedra = sorted(cell for cell in all_cells if len(cell) == 4)
    triangle_id = {cell: index for index, cell in enumerate(triangles)}
    column_faces = []
    incident = defaultdict(list)
    for column, tetrahedron in enumerate(tetrahedra):
        faces = [(triangle_id[face], coefficient) for face, coefficient in boundary_cell(tetrahedron).items()]
        column_faces.append(faces)
        for row, _coefficient in faces:
            incident[row].append(column)
    rhs = [cycle.get(cell, Fraction(0)) for cell in triangles]
    active = {column for row, value in enumerate(rhs) if value for column in incident[row]}
    for radius in range(4):
        touched = {row for column in active for row, _coefficient in column_faces[column]}
        touched.update(row for row, value in enumerate(rhs) if value)
        ordered_rows = sorted(touched)
        row_id = {row: index for index, row in enumerate(ordered_rows)}
        ordered_columns = sorted(active)
        column_id = {column: index for index, column in enumerate(ordered_columns)}
        local_rows = [dict() for _ in ordered_rows]
        for column in ordered_columns:
            for row, coefficient in column_faces[column]:
                local_rows[row_id[row]][column_id[column]] = coefficient
        local_rhs = [rhs[row] for row in ordered_rows]
        local = sparse_solve(local_rows, local_rhs, len(ordered_columns))
        if local["status"] == "CONSISTENT":
            witness = {tetrahedra[ordered_columns[index]]: value for index, value in enumerate(local["solution"]) if value}
            if boundary(witness) != cycle:
                raise AssertionError("localized boundary witness")
            return {"status": "BOUNDARY", "witness": witness, "rank": local["rank"], "route": "LOCAL_INCIDENCE", "radius": radius, "local_triangles": len(ordered_rows), "local_tetrahedra": len(ordered_columns)}
        expanded = set(active)
        for row in touched:
            expanded.update(incident[row])
        if expanded == active or len(expanded) > 10_000:
            break
        active = expanded

    rows = [dict() for _ in triangles]
    for column, faces in enumerate(column_faces):
        for row, coefficient in faces:
            rows[row][column] = coefficient
    solved = sparse_solve(rows, rhs, len(tetrahedra), track_relation=True)
    if solved["status"] == "CONSISTENT":
        witness = {tetrahedra[index]: value for index, value in enumerate(solved["solution"]) if value}
        if boundary(witness) != cycle:
            raise AssertionError("direct boundary witness")
        return {"status": "BOUNDARY", "witness": witness, "rank": solved["rank"], "route": "FULL_EXACT", "radius": None, "local_triangles": len(triangles), "local_tetrahedra": len(tetrahedra)}
    relation = solved["relation"]
    pairing = sum(relation[index] * rhs[index] for index in relation)
    if not pairing:
        raise AssertionError("direct dual pairing")
    dual = {triangles[index]: value for index, value in relation.items() if value}
    return {"status": "NONBOUNDARY", "dual": dual, "pairing": pairing, "rank": solved["rank"], "route": "FULL_EXACT", "radius": None, "local_triangles": len(triangles), "local_tetrahedra": len(tetrahedra)}


def solve_injected_class(all_cells, cover, cycle):
    """Solve in the canonical Cech injection without full resolution elimination."""
    lifted, uncovered = canonical_cycle_lift(cycle, cover)
    if uncovered:
        return {"status": "UNCOVERED", "first_uncovered": uncovered[0], "uncovered_nonzero": len(uncovered)}
    solved = direct_boundary_solve(all_cells, cycle)
    result = {
        "status": solved["status"], "cover_members": len(cover),
        "cover_union_cells": len(set().union(*cover)), "lift_nonzero": len(lifted),
        "lift": serialize_chain(lifted), "relation_rank": solved["rank"],
        "solve_route": solved["route"], "solve_radius": solved["radius"],
        "solve_triangles": solved["local_triangles"], "solve_tetrahedra": solved["local_tetrahedra"],
    }
    if solved["status"] == "BOUNDARY":
        recombined = defaultdict(Fraction)
        for tetrahedron, coefficient in solved["witness"].items():
            relation, relation_uncovered = canonical_cycle_lift(boundary_cell(tetrahedron), cover)
            if relation_uncovered:
                raise AssertionError("tetrahedron relation is uncovered")
            for key, value in relation.items():
                recombined[key] += coefficient * value
        if clean(recombined) != lifted:
            raise AssertionError("injected relation recombination")
        result.update({
            "witness_nonzero": len(solved["witness"]),
            "witness": [[[list(vertex) for vertex in cell], value.numerator, value.denominator] for cell, value in sorted(solved["witness"].items())],
        })
    else:
        pairing = solved["pairing"]
        result.update({
            "dual_nonzero": len(solved["dual"]), "pairing": [pairing.numerator, pairing.denominator],
            "dual": [[[list(vertex) for vertex in cell], value.numerator, value.denominator] for cell, value in sorted(solved["dual"].items())],
        })
    return result


def solve_total_class(all_cells, cover, cycle):
    """Lift a 2-cycle to Tot(Cech cover) and test whether it bounds there."""
    if boundary(cycle):
        raise AssertionError("input is not a cycle")
    union = set().union(*cover) if cover else set()
    uncovered = sorted(cell for cell in cycle if cell not in union)
    if uncovered:
        return {"status": "UNCOVERED", "first_uncovered": uncovered[0], "uncovered_nonzero": len(uncovered)}

    bases = {degree: total_basis(cover, degree) for degree in range(4)}
    matrices = {degree: total_boundary(bases[degree], bases[degree - 1]) for degree in range(1, 4)}
    for degree in (2, 3):
        good, column = verify_square_zero(matrices[degree], matrices[degree - 1])
        if not good:
            return {"status": "SQUARE_ZERO_FAILURE", "degree": degree, "column": column}

    triangles = sorted(cell for cell in all_cells if len(cell) == 3)
    triangle_id = {cell: index for index, cell in enumerate(triangles)}
    lift_rows = [dict(row) for row in matrices[2]] + [dict() for _ in triangles]
    lift_rhs = [Fraction(0)] * len(matrices[2]) + [cycle.get(cell, Fraction(0)) for cell in triangles]
    for column, (indices, cell) in enumerate(bases[2]):
        if len(indices) == 1 and len(cell) == 3:
            lift_rows[len(matrices[2]) + triangle_id[cell]][column] = Fraction(1)
    lifted = sparse_solve(lift_rows, lift_rhs, len(bases[2]), track_relation=True)
    if lifted["status"] != "CONSISTENT":
        return {"status": "LIFT_FAILURE", "pairing": [lifted["pairing"].numerator, lifted["pairing"].denominator]}
    lifted_chain = {bases[2][index]: value for index, value in enumerate(lifted["solution"]) if value}
    if any(apply_matrix(matrices[2], {index: value for index, value in enumerate(lifted["solution"]) if value})):
        raise AssertionError("lift is not a total cycle")

    rhs = [lifted_chain.get(item, Fraction(0)) for item in bases[2]]
    bounded = sparse_solve(matrices[3], rhs, len(bases[3]), track_relation=True)
    result = {
        "status": "BOUNDARY" if bounded["status"] == "CONSISTENT" else "NONBOUNDARY",
        "cover_members": len(cover),
        "cover_union_cells": len(union),
        "basis_counts": {str(degree): len(bases[degree]) for degree in bases},
        "lift_nonzero": len(lifted_chain),
        "lift": serialize_chain(lifted_chain),
    }
    if bounded["status"] == "CONSISTENT":
        witness = {bases[3][index]: value for index, value in enumerate(bounded["solution"]) if value}
        if apply_matrix(matrices[3], {index: value for index, value in enumerate(bounded["solution"]) if value}) != rhs:
            raise AssertionError("invalid total boundary witness")
        result.update({"witness_nonzero": len(witness), "witness": serialize_chain(witness)})
    else:
        relation = bounded["relation"]
        pairing = sum(relation[index] * rhs[index] for index in relation)
        if not pairing:
            raise AssertionError("zero total dual pairing")
        result.update({"dual_nonzero": len(relation), "pairing": [pairing.numerator, pairing.denominator]})
    return result


def direct_boundary_class(all_cells, cycle):
    return direct_boundary_solve(all_cells, cycle)["status"]


def cone(vertex, chain):
    result = defaultdict(Fraction)
    for cell, coefficient in chain.items():
        upper = tuple(sorted(cell + (vertex,)))
        index = upper.index(vertex)
        result[upper] += coefficient / Fraction((-1) ** index)
    return clean(result)
