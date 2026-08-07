#!/usr/bin/env python3
"""Physical quadratic refinements and exhaustive Sp(6,2) TT-rank test."""

from __future__ import annotations

from fractions import Fraction
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_genus3 import (  # noqa: E402
    _cycle_basis,
    _edge_homology_labels,
    _frontier_sector_polynomials,
    _rotation_faces,
    _tt_ranks,
)
from proof.verify_lane_b_intersection import (  # noqa: E402
    _gf2_inverse,
    _graph_result,
    _homology_representatives,
    _matrix_multiply,
    _transpose,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_genus3 import BOX_4X3X3_GENUS_THREE_ROTATION  # noqa: E402


PRIME = 1_000_000_007
EXPECTED_SP6_ORDER = 1_451_520


def _matrix_vector(rows: list[int], vector: int) -> int:
    return sum(((row & vector).bit_count() & 1) << index for index, row in enumerate(rows))


def _scaled_evaluate(polynomial: tuple[int, ...], numerator: int, denominator: int, degree: int) -> int:
    return sum(
        coefficient * numerator**power * denominator ** (degree - power)
        for power, coefficient in enumerate(polynomial)
    )


def _reference_quadratic(vector: int, genus: int) -> int:
    return sum(
        ((vector >> (2 * handle)) & 1) * ((vector >> (2 * handle + 1)) & 1)
        for handle in range(genus)
    ) & 1


def _arf_from_gauss(quadratic_values: list[int], genus: int) -> int:
    gauss = sum(-1 if value else 1 for value in quadratic_values)
    if abs(gauss) != 1 << genus:
        raise AssertionError("quadratic Gauss sum has the wrong magnitude")
    return int(gauss < 0)


def _quadratic_table(genus: int) -> tuple[list[list[int]], list[int]]:
    dimension = 2 * genus
    table: list[list[int]] = []
    arfs: list[int] = []
    for linear in range(1 << dimension):
        values = [
            _reference_quadratic(homology, genus)
            ^ ((linear & homology).bit_count() & 1)
            for homology in range(1 << dimension)
        ]
        # Independently check the defining polarization identity.
        for left in range(1 << dimension):
            for right in range(1 << dimension):
                pairing = sum(
                    (((left >> (2 * handle)) & 1) * ((right >> (2 * handle + 1)) & 1))
                    ^ (((left >> (2 * handle + 1)) & 1) * ((right >> (2 * handle)) & 1))
                    for handle in range(genus)
                ) & 1
                if values[left ^ right] ^ values[left] ^ values[right] != pairing:
                    raise AssertionError("quadratic-refinement polarization failure")
        arf_formula = _reference_quadratic(linear, genus)
        arf_gauss = _arf_from_gauss(values, genus)
        if arf_formula != arf_gauss:
            raise AssertionError("Arf formula disagrees with the exact Gauss sum")
        table.append(values)
        arfs.append(arf_gauss)
    if arfs.count(0) != 36 or arfs.count(1) != 28:
        raise AssertionError("genus-three even/odd spin-structure count regression")
    return table, arfs


def _compile_rank_search(directory: Path) -> tuple[Path, str]:
    source = ROOT / "proof" / "lane_b_symplectic_rank_search.cpp"
    executable = directory / "lane-b-rank-search"
    version = subprocess.run(
        ["g++", "--version"], check=True, capture_output=True, text=True
    ).stdout.splitlines()[0]
    subprocess.run(
        ["g++", "-O3", "-std=c++17", str(source), "-o", str(executable)],
        check=True,
    )
    return executable, version


def _run_rank_search(executable: Path, values: list[int]) -> dict[str, object]:
    payload = " ".join([str(PRIME), *(str(value % PRIME) for value in values)]) + "\n"
    completed = subprocess.run(
        [str(executable)], input=payload, check=True, capture_output=True, text=True
    )
    result = json.loads(completed.stdout)
    if result["symplectic_bases"] != EXPECTED_SP6_ORDER:
        raise AssertionError("Sp(6,2) enumeration count regression")
    return result


def _basis_image(basis: list[int], index: int) -> int:
    image = 0
    for bit, vector in enumerate(basis):
        if (index >> bit) & 1:
            image ^= vector
    return image


def _exact_rank_seven_witness(
    f_polynomials: list[tuple[int, ...]], basis: list[int]
) -> dict[str, object]:
    """Certify a polynomial row relation and a nonzero rank-seven minor."""
    if basis != [1, 34, 4, 8, 17, 32]:
        raise AssertionError("unexpected first modular survivor")
    # The middle 8x8 flattening has rows indexed by the low three bits and
    # columns by the high three bits. Rows 4 and 6 agree coefficientwise.
    for column in range(8):
        left = f_polynomials[_basis_image(basis, 4 | (column << 3))]
        right = f_polynomials[_basis_image(basis, 6 | (column << 3))]
        if left != right:
            raise AssertionError("candidate polynomial row identity failed")

    exact_ranks: dict[str, int] = {}
    minor_witnesses: dict[str, str] = {}
    for numerator, denominator in ((1, 2), (1, 3)):
        values = [
            _scaled_evaluate(polynomial, numerator, denominator, 75)
            for polynomial in f_polynomials
        ]
        matrix = sympy.Matrix(
            8,
            8,
            lambda row, column: values[
                _basis_image(basis, row | (column << 3))
            ],
        )
        rank = matrix.rank()
        if rank != 7:
            raise AssertionError("exact survivor does not have middle rank seven")
        # Rows 0..6 and columns 0..6 give a compact deterministic witness for
        # this candidate. Fall back to the first nonzero 7x7 minor if needed.
        determinant = matrix.extract(range(7), range(7)).det()
        selected_rows = list(range(7))
        selected_columns = list(range(7))
        if determinant == 0:
            determinant = None
            for omitted_row in range(8):
                for omitted_column in range(8):
                    rows = [row for row in range(8) if row != omitted_row]
                    columns = [column for column in range(8) if column != omitted_column]
                    candidate = matrix.extract(rows, columns).det()
                    if candidate:
                        determinant = candidate
                        selected_rows, selected_columns = rows, columns
                        break
                if determinant is not None:
                    break
        if determinant is None or determinant == 0:
            raise AssertionError("rank-seven minor witness was not found")
        key = f"{numerator}/{denominator}"
        exact_ranks[key] = rank
        minor_witnesses[key] = str(determinant)
    return {
        "ordered_symplectic_basis": basis,
        "middle_cut": "low parameter bits 0,1,2 | high parameter bits 3,4,5",
        "coefficientwise_row_identity": "row_4 - row_6 = 0",
        "constant_left_kernel": [0, 0, 0, 0, -1, 0, 1, 0],
        "exact_specialized_middle_ranks": exact_ranks,
        "nonzero_7x7_minor_determinants": minor_witnesses,
        "generic_TT_rank_over_Q(t)": [2, 4, 7, 4, 2],
        "proof": (
            "The coefficientwise row identity gives middle rank at most seven over Q(t). "
            "Either exact nonzero specialized 7x7 minor gives rank at least seven over Q(t). "
            "Full modular ranks at the other cuts give their exact generic maxima."
        ),
    }


def _swap_yz_symmetry(
    vertices: tuple[tuple[int, int, int], ...],
    edges: tuple[object, ...],
    face_masks: list[int],
    labels: list[int],
    cycles: list[int],
    transport: list[int],
    symplectic_sectors: list[tuple[int, ...]],
    f_polynomials: list[tuple[int, ...]],
) -> dict[str, object]:
    """Derive the rank-seven row identity from the y<->z box symmetry."""
    dimension = 6
    edge_index = {(edge.u, edge.v): index for index, edge in enumerate(edges)}
    permutation: list[int] = []
    for edge in edges:
        u = edge.u[0], edge.u[2], edge.u[1]
        v = edge.v[0], edge.v[2], edge.v[1]
        permutation.append(edge_index[tuple(sorted((u, v)))])

    def map_edges(mask: int) -> int:
        result = 0
        for edge, image in enumerate(permutation):
            if (mask >> edge) & 1:
                result ^= 1 << image
        return result

    def pinned_label(mask: int) -> int:
        result = 0
        for edge, label in enumerate(labels):
            if (mask >> edge) & 1:
                result ^= label
        return result

    if any(pinned_label(map_edges(face)) for face in face_masks):
        raise AssertionError("y-z swap does not preserve the facial boundary space")
    inverse_transport = _gf2_inverse(transport, dimension)
    representatives = _homology_representatives(cycles, labels, dimension)
    columns: list[int] = []
    for coordinate in range(dimension):
        pinned = _matrix_vector(transport, 1 << coordinate)
        cycle = 0
        for bit, representative in enumerate(representatives):
            if (pinned >> bit) & 1:
                cycle ^= representative
        image_pinned = pinned_label(map_edges(cycle))
        columns.append(_matrix_vector(inverse_transport, image_pinned))
    action = [
        sum(((columns[column] >> row) & 1) << column for column in range(dimension))
        for row in range(dimension)
    ]
    expected_action = [9, 2, 38, 8, 24, 32]
    if action != expected_action:
        raise AssertionError("y-z homology action regression")
    for homology in range(64):
        image = _matrix_vector(action, homology)
        if symplectic_sectors[homology] != symplectic_sectors[image]:
            raise AssertionError("sector polynomial is not invariant under y-z swap")
        if _reference_quadratic(homology, 3) != _reference_quadratic(image, 3):
            raise AssertionError("reference quadratic form is not y-z invariant")
    dual_action = _transpose(action, dimension)
    for linear in range(64):
        if f_polynomials[linear] != f_polynomials[_matrix_vector(dual_action, linear)]:
            raise AssertionError("F polynomial is not invariant under the dual affine action")

    rank_basis = [1, 34, 4, 8, 17, 32]
    for column in range(8):
        row_four = _basis_image(rank_basis, 4 | (column << 3))
        row_six = _basis_image(rank_basis, 6 | (column << 3))
        if _matrix_vector(dual_action, row_four) != row_six:
            raise AssertionError("y-z action does not derive the row-4/row-6 identity")
    return {
        "graph_automorphism": "(x,y,z) -> (x,z,y)",
        "facial_boundary_space_preserved": True,
        "symplectic_homology_action_rows": action,
        "dual_spin_structure_action_rows": dual_action,
        "quadratic_form_preserved": True,
        "sector_polynomials_preserved": True,
        "derived_flattening_identity": "row_4 = row_6 for all eight columns",
    }


def verify() -> dict[str, object]:
    genus = 3
    dimension = 2 * genus
    vertices, edges = cubic_box((4, 3, 3))
    face_masks, _ = _rotation_faces(vertices, edges, BOX_4X3X3_GENUS_THREE_ROTATION)
    cycles = _cycle_basis(vertices, edges)
    labels, _ = _edge_homology_labels(len(edges), face_masks, cycles, genus)
    sectors, maximum_states = _frontier_sector_polynomials(vertices, edges, labels)
    intersection_data = _graph_result(
        (4, 3, 3), BOX_4X3X3_GENUS_THREE_ROTATION, genus
    )
    transport = intersection_data["symplectic_transport_rows"]
    canonical = [1 << (index ^ 1) for index in range(dimension)]
    physical_intersection = intersection_data["intersection_matrix_rows"]
    if _matrix_multiply(
        _transpose(transport, dimension),
        _matrix_multiply(physical_intersection, transport, dimension),
        dimension,
    ) != canonical:
        raise AssertionError("physical-to-symplectic transport regression")

    # W in the explicit physical symplectic homology coordinates y, with
    # pinned coordinates h = transport*y.
    symplectic_sectors = [sectors[_matrix_vector(transport, y)] for y in range(1 << dimension)]
    quadratic_table, arfs = _quadratic_table(genus)
    f_polynomials: list[tuple[int, ...]] = []
    for linear in range(1 << dimension):
        polynomial = [0] * (len(edges) + 1)
        for homology, sector in enumerate(symplectic_sectors):
            sign = -1 if quadratic_table[linear][homology] else 1
            for degree, coefficient in enumerate(sector):
                polynomial[degree] += sign * coefficient
        f_polynomials.append(tuple(polynomial))
    evaluations: dict[str, object] = {}
    with tempfile.TemporaryDirectory(prefix="lane-b-rank-") as temporary:
        executable, compiler = _compile_rank_search(Path(temporary))
        for numerator, denominator in ((1, 2), (1, 3)):
            weights = [
                _scaled_evaluate(polynomial, numerator, denominator, len(edges))
                for polynomial in symplectic_sectors
            ]
            f_values = [
                _scaled_evaluate(polynomial, numerator, denominator, len(edges))
                for polynomial in f_polynomials
            ]
            arf_sum = sum(-value if arfs[index] else value for index, value in enumerate(f_values))
            if arf_sum % (1 << genus):
                raise AssertionError("Arf reconstruction is not integral")
            reconstructed = arf_sum // (1 << genus)
            if reconstructed != sum(weights):
                raise AssertionError("Arf reconstruction does not equal the physical sector sum")
            rational_values = [Fraction(value, denominator ** len(edges)) for value in f_values]
            canonical_ranks = _tt_ranks(rational_values, dimension)
            modular_search = _run_rank_search(executable, f_values)
            status = (
                "MODULAR_SURVIVORS_FOUND"
                if modular_search["submaximal_found"]
                else "ALL_SYMPLECTIC_BASES_MAXIMAL"
            )
            evaluations[f"{numerator}/{denominator}"] = {
                "scaled_common_denominator": str(denominator ** len(edges)),
                "canonical_exact_TT_ranks": canonical_ranks,
                "arf_reconstruction": True,
                "modular_prime": PRIME,
                "symplectic_search": modular_search,
                "status": status,
            }
    first_survivor = evaluations["1/2"]["symplectic_search"].get("first_bad_basis")
    if first_survivor is None:
        exact_survivor = None
    else:
        exact_survivor = _exact_rank_seven_witness(f_polynomials, first_survivor)
    symmetry = _swap_yz_symmetry(
        vertices,
        edges,
        face_masks,
        labels,
        cycles,
        transport,
        symplectic_sectors,
        f_polynomials,
    )
    return {
        "claim_status": "COMPUTATIONALLY_VERIFIED",
        "shape": [4, 3, 3],
        "genus": genus,
        "physical_intersection_matrix_rows": physical_intersection,
        "symplectic_transport_rows": transport,
        "quadratic_refinements": 1 << dimension,
        "even_spin_structures": arfs.count(0),
        "odd_spin_structures": arfs.count(1),
        "maximum_frontier_states": maximum_states,
        "compiler": compiler,
        "evaluations": evaluations,
        "exact_rank_seven_survivor": exact_survivor,
        "rank_reduction_symmetry_derivation": symmetry,
        "claim_boundary": (
            "A full modular rank at a rational specialization proves the corresponding integer "
            "minor is nonzero, so it proves exact full rank at that specialization. The search "
            "covers all ordered symplectic bases of the six-dimensional physical spin-structure "
            "coordinate space. It does not by itself prove generic rank over Q(t), a growing-size "
            "no-go, or any thermodynamic statement."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
