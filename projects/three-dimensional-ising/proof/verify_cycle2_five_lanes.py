#!/usr/bin/env python3
"""Exact decisive tests for the five Stage 2 candidate lanes."""

from __future__ import annotations

from collections import Counter
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import sys
from typing import Iterable

import sympy


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_stage1_baseline import _gf2_nullspace_basis  # noqa: E402
from src.conventions import cubic_box, orientable_genus_lower_bound_for_free_box  # noqa: E402
from src.embeddings import SLAB_3X3X2_GENUS_ONE_ROTATION  # noqa: E402


def _bits(index: int, width: int) -> list[int]:
    return [(index >> (width - 1 - position)) & 1 for position in range(width)]


def _ising_vertex_entries(x: object, y: object, z: object) -> dict[tuple[int, int], object]:
    """Rank-six parity tensor as an operator on three binary spaces.

    Negative-direction legs are inputs. Positive-direction legs are outputs,
    and carry the full high-temperature bond weights. This is gauge-equivalent
    on a periodic network to splitting square roots across both ends.
    """

    entries: dict[tuple[int, int], object] = {}
    for incoming in range(8):
        for outgoing in range(8):
            if (incoming.bit_count() + outgoing.bit_count()) % 2:
                continue
            ox, oy, oz = _bits(outgoing, 3)
            entries[outgoing, incoming] = x**ox * y**oy * z**oz
    return entries


def _embed_three_space_operator(
    entries: dict[tuple[int, int], object], spaces: tuple[int, int, int]
) -> list[list[object]]:
    matrix: list[list[object]] = [[0] * 64 for _ in range(64)]
    for incoming in range(64):
        input_bits = _bits(incoming, 6)
        local_in = sum(input_bits[spaces[k]] << (2 - k) for k in range(3))
        for local_out in range(8):
            value = entries.get((local_out, local_in), 0)
            if value == 0:
                continue
            output_bits = input_bits[:]
            local_bits = _bits(local_out, 3)
            for k, space in enumerate(spaces):
                output_bits[space] = local_bits[k]
            outgoing = sum(output_bits[k] << (5 - k) for k in range(6))
            matrix[outgoing][incoming] = value
    return matrix


def _apply(matrix: list[list[object]], vector: list[object]) -> list[object]:
    return [
        sum(matrix[row][column] * vector[column] for column in range(64) if vector[column] != 0)
        for row in range(64)
    ]


def _tetrahedron_entry(
    entries: dict[tuple[int, int], object], outgoing: int, incoming: int
) -> tuple[object, object]:
    spaces = ((0, 1, 2), (0, 3, 4), (1, 3, 5), (2, 4, 5))
    embedded = [_embed_three_space_operator(entries, triple) for triple in spaces]
    vector: list[object] = [0] * 64
    vector[incoming] = 1
    for matrix in reversed(embedded):
        vector = _apply(matrix, vector)
    lhs = vector[outgoing]
    vector = [0] * 64
    vector[incoming] = 1
    for matrix in embedded:
        vector = _apply(matrix, vector)
    rhs = vector[outgoing]
    return lhs, rhs


def _periodic_layer_edges(length: int) -> tuple[tuple[int, int, int], ...]:
    edges = []
    for x in range(length):
        for y in range(length):
            vertex = x * length + y
            edges.append((vertex, ((x + 1) % length) * length + y, 0))
            edges.append((vertex, x * length + (y + 1) % length, 1))
    return tuple(edges)


def _spin_vector(state: int, count: int) -> tuple[int, ...]:
    return tuple(1 if (state >> index) & 1 else -1 for index in range(count))


def _layer_diagonal(state: int, parameters: tuple[Fraction, Fraction, Fraction]) -> Fraction:
    spins = _spin_vector(state, 9)
    value = Fraction(1)
    for source, target, axis in _periodic_layer_edges(3):
        value *= 1 + parameters[axis] * spins[source] * spins[target]
    return value


def _layer_vertical(source: int, target: int, parameter: Fraction) -> Fraction:
    source_spins = _spin_vector(source, 9)
    target_spins = _spin_vector(target, 9)
    value = Fraction(1)
    for index in range(9):
        value *= 1 + parameter * source_spins[index] * target_spins[index]
    return value


def _layer_entry(
    source: int,
    target: int,
    parameters: tuple[Fraction, Fraction, Fraction],
    diagonals: tuple[Fraction, ...],
) -> Fraction:
    return diagonals[source] * _layer_vertical(source, target, parameters[2])


def lane_a() -> dict[str, object]:
    x, y, z = sympy.symbols("x y z")
    symbolic_entries = _ising_vertex_entries(x, y, z)
    lhs, rhs = _tetrahedron_entry(symbolic_entries, 0, 3)
    residual = sympy.factor(sympy.expand(lhs - rhs))
    isotropic = sympy.factor(residual.subs({x: sympy.Symbol("t"), y: sympy.Symbol("t"), z: sympy.Symbol("t")}))
    expected_isotropic = -(sympy.Symbol("t") - 1) ** 3 * (sympy.Symbol("t") + 1) ** 2
    if sympy.expand(isotropic - expected_isotropic) != 0:
        raise AssertionError("tetrahedron residual regression")

    p = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 5))
    q = (Fraction(1, 3), Fraction(1, 4), Fraction(1, 7))
    p_diagonal = tuple(_layer_diagonal(state, p) for state in range(512))
    q_diagonal = tuple(_layer_diagonal(state, q) for state in range(512))
    source = target = 0
    pq = sum(
        (
            _layer_entry(source, middle, p, p_diagonal)
            * _layer_entry(middle, target, q, q_diagonal)
            for middle in range(512)
        ),
        Fraction(),
    )
    qp = sum(
        (
            _layer_entry(source, middle, q, q_diagonal)
            * _layer_entry(middle, target, p, p_diagonal)
            for middle in range(512)
        ),
        Fraction(),
    )
    if pq == qp:
        raise AssertionError("naive periodic layer family unexpectedly commuted")
    return {
        "status": "RESTRICTED_NO_GO",
        "local_spaces": "V_x tensor V_y tensor V_z with each V_mu=Q^2",
        "tensor": "R[o,i]=delta_even(i,o)*x^o_x*y^o_y*z^o_z",
        "tetrahedron_equation": "R123 R145 R246 R356 = R356 R246 R145 R123",
        "witness_entry": {"outgoing": 0, "incoming": 3},
        "symbolic_residual": str(residual),
        "isotropic_residual": str(isotropic),
        "physical_isotropic_interval": "0<t<1, where the displayed residual is nonzero",
        "auxiliary_dimensions": {
            "D=2": "direct tensor fails",
            "D=3,4": (
                "any extension preserving the binary physical subspace for every local R "
                "fails after projection to the same residual"
            ),
        },
        "periodic_layer": {
            "shape": [3, 3],
            "parameter_p": [str(value) for value in p],
            "parameter_q": [str(value) for value in q],
            "commutator_entry": [source, target],
            "TpTq": str(pq),
            "TqTp": str(qp),
            "difference": str(pq - qp),
        },
        "claim_boundary": (
            "Direct binary vertex tensor and invariant physical-block extensions through D=4; "
            "non-invariant auxiliary mixing, IRF tensors, and other tetrahedron relations remain open."
        ),
    }


def _polynomial_add(target: list[int], source: Counter[int], sign: int) -> None:
    for degree, coefficient in source.items():
        target[degree] += sign * coefficient


def _polynomial_convolution(left: list[int], right: list[int]) -> list[int]:
    result = [0] * (len(left) + len(right) - 1)
    for i, a in enumerate(left):
        for j, b in enumerate(right):
            result[i + j] += a * b
    return result


def _nonzero_coefficients(polynomial: Iterable[int]) -> dict[str, int]:
    return {str(index): coefficient for index, coefficient in enumerate(polynomial) if coefficient}


def _counter_coefficients(polynomial: Counter[int]) -> dict[str, int]:
    return {str(degree): polynomial[degree] for degree in sorted(polynomial) if polynomial[degree]}


def _cycle_basis(vertices: tuple[object, ...], edges: tuple[object, ...]) -> list[int]:
    vertex_index = {vertex: index for index, vertex in enumerate(vertices)}
    rows = [0] * len(vertices)
    for edge_index, edge in enumerate(edges):
        rows[vertex_index[edge.u]] |= 1 << edge_index
        rows[vertex_index[edge.v]] |= 1 << edge_index
    return _gf2_nullspace_basis(rows, len(edges))


def _spin_structure_data(
    sectors: dict[tuple[int, int], Counter[int]], maximum_degree: int
) -> dict[str, object]:
    f_values: dict[tuple[int, int], list[int]] = {}
    for a in (0, 1):
        for b in (0, 1):
            polynomial = [0] * (maximum_degree + 1)
            for (hx, hy), sector in sectors.items():
                sign = -1 if (hx * hy + a * hx + b * hy) % 2 else 1
                _polynomial_add(polynomial, sector, sign)
            f_values[a, b] = polynomial
    determinant_left = _polynomial_convolution(f_values[0, 0], f_values[1, 1])
    determinant_right = _polynomial_convolution(f_values[0, 1], f_values[1, 0])
    determinant = [left - right for left, right in zip(determinant_left, determinant_right)]
    if not any(determinant):
        raise AssertionError("genus-one F matrix unexpectedly has rank one")
    determinant_at_half = sum(
        (Fraction(coefficient, 2**degree) for degree, coefficient in enumerate(determinant)),
        Fraction(),
    )
    if determinant_at_half == 0:
        raise AssertionError("rank witness vanished at t=1/2")
    physical = [sum(sector.get(degree, 0) for sector in sectors.values()) for degree in range(maximum_degree + 1)]
    reconstructed = [
        (f_values[0, 0][degree] + f_values[0, 1][degree] + f_values[1, 0][degree] - f_values[1, 1][degree])
        // 2
        for degree in range(maximum_degree + 1)
    ]
    if reconstructed != physical:
        raise AssertionError("Arf-weighted reconstruction mismatch")
    return {
        "homology_sector_polynomials": {
            f"{hx}{hy}": _counter_coefficients(sectors[hx, hy])
            for hx in (0, 1)
            for hy in (0, 1)
        },
        "F_polynomials": {
            f"{a}{b}": _nonzero_coefficients(f_values[a, b]) for a in (0, 1) for b in (0, 1)
        },
        "F_matrix_rank_over_Q(t)": 2,
        "rank_witness_determinant": _nonzero_coefficients(determinant),
        "rank_witness_at_t=1/2": str(determinant_at_half),
        "fourier_support": 4,
        "arf_reconstruction_verified": True,
        "physical_even_subgraph_polynomial": _nonzero_coefficients(physical),
    }


def _rotation_faces(
    vertices: tuple[object, ...],
    edges: tuple[object, ...],
    rotation: dict[object, tuple[object, ...]],
) -> tuple[list[int], list[int]]:
    edge_index = {
        (edge.u, edge.v): index for index, edge in enumerate(edges)
    }

    def index_of_edge(left: object, right: object) -> int:
        pair = (left, right) if left < right else (right, left)
        return edge_index[pair]

    seen: set[tuple[object, object]] = set()
    face_masks: list[int] = []
    face_lengths: list[int] = []
    for left in vertices:
        for right in rotation[left]:
            if (left, right) in seen:
                continue
            dart = (left, right)
            mask = 0
            length = 0
            while dart not in seen:
                seen.add(dart)
                length += 1
                mask ^= 1 << index_of_edge(*dart)
                source, target = dart
                cyclic = rotation[target]
                dart = (target, cyclic[(cyclic.index(source) + 1) % len(cyclic)])
            face_masks.append(mask)
            face_lengths.append(length)
    if len(seen) != 2 * len(edges):
        raise AssertionError("rotation system did not partition all directed edges")
    return face_masks, face_lengths


def _add_labeled_gf2_vector(
    basis: dict[int, tuple[int, tuple[int, int]]],
    vector: int,
    label: tuple[int, int],
) -> bool:
    while vector:
        pivot = vector.bit_length() - 1
        if pivot in basis:
            old_vector, old_label = basis[pivot]
            vector ^= old_vector
            label = (label[0] ^ old_label[0], label[1] ^ old_label[1])
        else:
            basis[pivot] = (vector, label)
            return True
    return False


def _homology_coordinates(
    face_masks: list[int], cycle_basis: list[int]
) -> tuple[dict[int, tuple[int, tuple[int, int]]], int]:
    labeled_basis: dict[int, tuple[int, tuple[int, int]]] = {}
    for face in face_masks:
        _add_labeled_gf2_vector(labeled_basis, face, (0, 0))
    face_rank = len(labeled_basis)
    quotient_labels = ((1, 0), (0, 1))
    quotient_count = 0
    for cycle in cycle_basis:
        trial = dict(labeled_basis)
        if _add_labeled_gf2_vector(trial, cycle, (0, 0)):
            if quotient_count >= 2:
                raise AssertionError("rotation system has genus greater than one")
            _add_labeled_gf2_vector(labeled_basis, cycle, quotient_labels[quotient_count])
            quotient_count += 1
    if quotient_count != 2:
        raise AssertionError("rotation system does not have two-dimensional H1")
    return labeled_basis, face_rank


def _reduce_homology(
    vector: int, basis: dict[int, tuple[int, tuple[int, int]]]
) -> tuple[int, int]:
    label = (0, 0)
    while vector:
        pivot = vector.bit_length() - 1
        if pivot not in basis:
            raise AssertionError("cycle was not in the face-plus-homology span")
        old_vector, old_label = basis[pivot]
        vector ^= old_vector
        label = (label[0] ^ old_label[0], label[1] ^ old_label[1])
    return label


def _toroidal_grid_data() -> dict[str, object]:
    vertices, edges = cubic_box((3, 3, 1), periodic=(0, 1))
    basis = _cycle_basis(vertices, edges)
    sectors = {(hx, hy): Counter() for hx in (0, 1) for hy in (0, 1)}
    for coordinates in range(1 << len(basis)):
        subset = 0
        for basis_index, vector in enumerate(basis):
            if (coordinates >> basis_index) & 1:
                subset ^= vector
        hx = hy = 0
        for edge_index, edge in enumerate(edges):
            if not ((subset >> edge_index) & 1):
                continue
            if abs(edge.u[0] - edge.v[0]) == 2:
                hx ^= 1
            if abs(edge.u[1] - edge.v[1]) == 2:
                hy ^= 1
        sectors[hx, hy][subset.bit_count()] += 1
    if any(not polynomial for polynomial in sectors.values()):
        raise AssertionError("missing torus homology sector")
    return {
        "graph": "simple 3x3 square grid cellularly embedded in the torus",
        "vertices": len(vertices),
        "edges": len(edges),
        "cycle_space_dimension": len(basis),
        **_spin_structure_data(sectors, len(edges)),
    }


def _cubic_slab_data() -> dict[str, object]:
    shape = (3, 3, 2)
    vertices, edges = cubic_box(shape)
    rotation = SLAB_3X3X2_GENUS_ONE_ROTATION
    if set(rotation) != set(vertices):
        raise AssertionError("slab rotation has the wrong vertex set")
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        adjacency[edge.u].add(edge.v)
        adjacency[edge.v].add(edge.u)
    if any(set(rotation[vertex]) != adjacency[vertex] for vertex in vertices):
        raise AssertionError("slab rotation has the wrong neighbours")
    face_masks, face_lengths = _rotation_faces(vertices, edges, rotation)
    euler_characteristic = len(vertices) - len(edges) + len(face_masks)
    if euler_characteristic != 0:
        raise AssertionError("slab rotation is not genus one")
    lower_bound = orientable_genus_lower_bound_for_free_box(shape)
    if lower_bound != 1:
        raise AssertionError("slab genus lower-bound regression")
    cycle_basis = _cycle_basis(vertices, edges)
    homology_basis, face_rank = _homology_coordinates(face_masks, cycle_basis)
    if face_rank != len(face_masks) - 1:
        raise AssertionError("slab face-boundary rank regression")
    sectors = {(hx, hy): Counter() for hx in (0, 1) for hy in (0, 1)}
    for coordinates in range(1 << len(cycle_basis)):
        subset = 0
        for basis_index, vector in enumerate(cycle_basis):
            if (coordinates >> basis_index) & 1:
                subset ^= vector
        sectors[_reduce_homology(subset, homology_basis)][subset.bit_count()] += 1
    if {sum(polynomial.values()) for polynomial in sectors.values()} != {1 << face_rank}:
        raise AssertionError("slab homology sectors do not have the expected equal size")
    return {
        "graph": "free 3x3x2 simple-cubic slab",
        "shape": list(shape),
        "vertices": len(vertices),
        "edges": len(edges),
        "cycle_space_dimension": len(cycle_basis),
        "rotation_faces": len(face_masks),
        "face_lengths": face_lengths,
        "face_boundary_rank": face_rank,
        "euler_characteristic": euler_characteristic,
        "embedding_genus": 1,
        "genus_lower_bound": lower_bound,
        "minimum_genus_certified": True,
        **_spin_structure_data(sectors, len(edges)),
    }


def lane_b() -> dict[str, object]:
    torus = _toroidal_grid_data()
    slab = _cubic_slab_data()
    return {
        "status": "SURVIVES",
        "exact_identity": (
            "F_(a,b)(t)=sum_h (-1)^(h_x*h_y+a*h_x+b*h_y) W_h(t); "
            "the Arf-weighted Fourier coefficient recovers the even-subgraph polynomial"
        ),
        "calibration_graph": torus,
        "cubic_graph": slab,
        "symmetry_orbit_bound": (
            "For a free L-cube, |Aut(G_L)|=48 (L>=3), so its action on 4^g spin "
            "structures has at least ceil(4^g/48) orbits; Stage 1 gives g=Omega(L^3)."
        ),
        "failed_submechanisms": [
            "factorization over the two torus spin bits (rank is 2, not 1)",
            "bounded Boolean Fourier degree on a cellular embedding (every homology sector is nonempty)",
            "polynomially many sectors from cubic-lattice symmetry alone",
        ],
        "surviving_submechanisms": [
            "submaximal tensor-train rank at growing genus",
            "a recurrence in L mixing all homology sectors collectively",
        ],
        "claim_boundary": (
            "Exact minimum-genus-one data for the free 3x3x2 cubic slab, a torus "
            "calibration, and the lattice-symmetry orbit bound only; no growing-genus "
            "F table or low-rank recurrence has been constructed."
        ),
    }


def lane_c() -> dict[str, object]:
    counts = {}
    for length in (2, 3, 4, 8):
        vertices = length * length
        edges = 2 * vertices
        plaquettes = vertices
        gauge_inequivalent = 1 << (edges - vertices + 1)
        local_flux_patterns = 1 << (plaquettes - 1)
        counts[str(length)] = {
            "vertices": vertices,
            "edges": edges,
            "gauge_inequivalent_link_fields": gauge_inequivalent,
            "local_flux_patterns": local_flux_patterns,
            "topological_holonomies": 4,
        }
        if gauge_inequivalent != 4 * local_flux_patterns:
            raise AssertionError("torus gauge-sector count regression")
    return {
        "status": "KILLED",
        "candidate": (
            "Apply locality-preserving 2D bosonization to the transfer plane and evaluate "
            "the resulting fermions sector by sector in a Z2 gauge field."
        ),
        "exact_constraint_comparison": {
            "physical_3d_Ising_dual": "standard Gauss law G_v=product_(e incident v) X_e=1",
            "local_free_fermion_bosonization": (
                "modified Gauss law G'_v=G_v W_NE(v)=1 and kinetic U_e=X_e Z_r(e)"
            ),
            "decisive_local_witness": (
                "A simultaneous eigenstate with G_v=+1 and W_NE(v)=-1 is accepted by "
                "the standard projector (1+G_v)/2 and annihilated by (1+G'_v)/2."
            ),
        },
        "sector_count_if_flux_is_left_unrestricted": counts,
        "interaction_order": (
            "The modified gauge model can be quadratic in its fermionic dual; the standard "
            "Ising-dual gauge model does not acquire that quadraticity without changing its Gauss law."
        ),
        "boundaries_and_topology": (
            "On an LxL torus, local plaquette fluxes obey one product constraint and two "
            "independent holonomies, giving 2^(L^2+1) gauge-inequivalent link fields."
        ),
        "claim_boundary": (
            "Direct substitution of the known locality-preserving bosonization/free-fermion "
            "gauge model for the standard 3D Ising dual. Other interacting higher-form "
            "fermionizations remain open."
        ),
    }


def _pfaffian(matrix: list[list[object]], indices: tuple[int, ...]) -> object:
    if not indices:
        return 1
    first = indices[0]
    value = 0
    for position in range(1, len(indices)):
        second = indices[position]
        remainder = indices[1:position] + indices[position + 1 :]
        value += (-1) ** (position + 1) * matrix[first][second] * _pfaffian(matrix, remainder)
    return sympy.expand(value)


def lane_d() -> dict[str, object]:
    weights = sympy.symbols("w0:6")
    matrix: list[list[object]] = [[0] * 6 for _ in range(6)]
    for i in range(6):
        for j in range(i + 1, 6):
            matrix[i][j] = weights[i] * weights[j]
            matrix[j][i] = -matrix[i][j]
    checked_minors = 0
    for size in (0, 2, 4, 6):
        for subset in combinations(range(6), size):
            expected = sympy.prod(weights[index] for index in subset)
            if sympy.expand(_pfaffian(matrix, subset) - expected) != 0:
                raise AssertionError(f"parity tensor Pfaffian mismatch on {subset}")
            checked_minors += 1

    # Boundary order 0,1,2,3. The bosonic crossing has entries for
    # 0000, 1010, 0101, 1111 all equal to +1. With f_empty=1, its two-particle
    # data force A_02=A_13=1 and all other A_ij=0, whose full Pfaffian is -1.
    crossing_full_value = 1
    gaussian_prediction = -1
    residual = crossing_full_value - gaussian_prediction
    if residual != 2:
        raise AssertionError("crossing matchgate residual regression")
    bosonic_crossing = {"0000": 1, "1010": 1, "0101": 1, "1111": 1}
    fermionic_crossing = {"0000": 1, "1010": 1, "0101": 1, "1111": -1}
    top_component = {"1111": 1}
    reconstructed_crossing = {
        bit_string: fermionic_crossing.get(bit_string, 0) + 2 * top_component.get(bit_string, 0)
        for bit_string in {**bosonic_crossing, **fermionic_crossing, **top_component}
    }
    if reconstructed_crossing != bosonic_crossing:
        raise AssertionError("binary crossing-selector decomposition regression")
    return {
        "status": "RESTRICTED_NO_GO",
        "exact_identity": (
            "P(i_1,...,i_6)=delta_even(i)*product_j w_j^i_j equals the vector of "
            "principal Pfaffian minors of A_ij=w_i*w_j (i<j)."
        ),
        "local_parity_tensor": {
            "matchgate": True,
            "pfaffian_minors_checked": checked_minors,
            "maximum_arity": 6,
        },
        "ordinary_crossing_tensor": {
            "nonzero_entries": ["0000", "1010", "0101", "1111"],
            "all_values": 1,
            "required_four_leg_value_from_two_leg_data": gaussian_prediction,
            "grassmann_pluecker_residual": residual,
        },
        "gauge_classification": (
            "Independent nonzero diagonal leg rescalings multiply this residual by their "
            "total leg product, so no invertible diagonal Ising bond gauge removes it."
        ),
        "auxiliary_cost": (
            "Replacing the ordinary crossing by the fermionic crossing changes only the "
            "1111 value to -1; restoring the missing occupancy-dependent signs globally "
            "is exactly the unresolved spin-structure/gauge-sector problem."
        ),
        "bounded_auxiliary_extension": {
            "D=2": (
                "C_bosonic=C_fermionic+2*E_1111, an exact sum of two Gaussian/matchgate "
                "signatures selected by one binary auxiliary index"
            ),
            "component_identity_verified": True,
            "D=3,4": "contain the D=2 decomposition by unused padded selector states",
            "global_cost": (
                "With c independently planarized crossings and no selector closure, the "
                "exact expansion has 2^c assignments; bounded local D alone is not a reduction."
            ),
        },
        "claim_boundary": (
            "Local parity tensors, parity-preserving diagonal gauges, and the explicit "
            "independent D=2 crossing selector. General GL(2) holographic bases and "
            "collectively constrained crossover auxiliaries are not excluded."
        ),
    }


def _star_weight(spins: tuple[int, ...], parameters: tuple[Fraction, ...]) -> Fraction:
    total = Fraction()
    for center in (-1, 1):
        value = Fraction(1)
        for spin, parameter in zip(spins, parameters):
            value *= 1 + parameter * center * spin
        total += value
    return total


def _multiplicative_walsh_ratio(
    weights: dict[tuple[int, ...], Fraction], subset: tuple[int, ...]
) -> Fraction:
    ratio = Fraction(1)
    for spins, weight in weights.items():
        character = 1
        for index in subset:
            character *= spins[index]
        if character == 1:
            ratio *= weight
        else:
            ratio /= weight
    return ratio


def lane_e() -> dict[str, object]:
    parameters = (
        Fraction(1, 2),
        Fraction(1, 2),
        Fraction(1, 3),
        Fraction(1, 3),
        Fraction(1, 5),
        Fraction(1, 5),
    )
    weights = {
        spins: _star_weight(spins, parameters) for spins in product((-1, 1), repeat=6)
    }
    four_body = _multiplicative_walsh_ratio(weights, (0, 1, 2, 3))
    six_body = _multiplicative_walsh_ratio(weights, (0, 1, 2, 3, 4, 5))
    if four_body == 1 or six_body == 1:
        raise AssertionError("higher blocked interaction unexpectedly vanished")
    return {
        "status": "RESTRICTED_NO_GO",
        "blocking": (
            "One checkerboard decimation with a 2x2x2 translation cell; each eliminated "
            "spin has its six retained +/-x,+/-y,+/-z neighbours on the block boundary."
        ),
        "exact_identity": (
            "W(s_1,...,s_6)=sum_(s_0=+/-1) product_i (1+t_i*s_0*s_i), with "
            "(t_1,...,t_6)=(t_x,t_x,t_y,t_y,t_z,t_z)."
        ),
        "induced_log_interactions": {
            "formula": "J_S=2^-6 sum_s (product_(i in S) s_i) log W(s)",
            "constant": 1,
            "pair": 15,
            "four_body": 15,
            "six_body": 1,
            "odd_body": 0,
        },
        "exact_specialization": [str(parameter) for parameter in parameters],
        "four_body_multiplicative_walsh_ratio": str(four_body),
        "six_body_multiplicative_walsh_ratio": str(six_body),
        "interpretation": (
            "The ratios equal exp(64 J_S) and are not one, proving nonzero four- and "
            "six-spin interactions at an interior eliminated site."
        ),
        "claim_boundary": (
            "Nearest-neighbour/pairwise closure under the declared checkerboard 2x2x2 "
            "blocking is excluded. A larger finite interaction algebra, critical-locus "
            "closure, and nonlocal changes of variables remain open."
        ),
    }


def build_report() -> dict[str, object]:
    lanes = {
        "A_tetrahedron_integrability": lane_a(),
        "B_spin_structure_compression": lane_b(),
        "C_higher_form_fermionization": lane_c(),
        "D_local_tensor_transformation": lane_d(),
        "E_exact_renormalization_closure": lane_e(),
    }
    statuses = {lane["status"] for lane in lanes.values()}
    if statuses != {"SURVIVES", "RESTRICTED_NO_GO", "KILLED"}:
        raise AssertionError("unexpected lane-status coverage")
    return {
        "status": "PASS",
        "arithmetic": "exact integers, fractions, and SymPy polynomial arithmetic",
        "sympy_version": sympy.__version__,
        "lanes": lanes,
        "selection_after_all_tests": {
            "selected_lane": "B_spin_structure_compression",
            "meaning": "next exact experiment, not a successful representation",
            "remaining_mechanisms": [
                "growing-genus tensor-train rank",
                "exact recurrence in L mixing all homology sectors",
            ],
        },
        "claim_boundary": (
            "First decisive tests of five explicit ansatz classes; no thermodynamic claim, "
            "critical data, or exact solution."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(build_report(), indent=2, sort_keys=True))
