#!/usr/bin/env python3
"""Exact homogeneous restrictions of the frozen Cycle 8 width-three minor."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_g1_paired_cycle_w3 import (  # noqa: E402
    CHORDS,
    EXPECTED_LABELS,
    HANDLE_CUT,
    N,
    TREE_EDGES,
    W,
    _fundamental_labels,
    _independent_row_positions,
    _labels,
)
from proof.verify_lane_b_arbitrary_width_frontier import _case, _rank  # noqa: E402
from proof.verify_lane_b_universal_canonical_ranks import _canonical_reindex  # noqa: E402
from proof.verify_lane_b_width_scaling import (  # noqa: E402
    _det_certificate,
    _edge_payload,
    _f_values_from_walsh,
)
from src.conventions import cubic_box  # noqa: E402
from src.lane_b_universal_embedding import (  # noqa: E402
    universal_checkerboard_rotation,
    universal_embedding_genus,
)


PRIMES = (1_000_000_007, 1_000_000_009)
ANISOTROPIC_POINTS = ((2, 3, 5), (7, 11, 13), (17, 19, 23))
ISOTROPIC_POINTS = (2, 3, 5)


def _parameterized_source() -> str:
    source = (ROOT / "proof/lane_b_width4_character_transfer.cpp").read_text()
    replacements = {
        "int n, w, dimension, edge_count, regime;":
            "int n, w, dimension, edge_count, regime; u64 tx, ty, tz;",
        "if (!(std::cin >> n >> w >> dimension >> edge_count >> regime)) return 2;":
            "if (!(std::cin >> n >> w >> dimension >> edge_count >> regime >> tx >> ty >> tz)) return 2;",
        "auto base_weight = [regime](int edge_index, int axis) -> u64 {":
            "auto base_weight = [regime, tx, ty, tz](int edge_index, int axis) -> u64 {",
        "static constexpr u64 axis_weight[3] = {2, 3, 5};":
            "const u64 axis_weight[3] = {tx, ty, tz};",
    }
    for old, new in replacements.items():
        if source.count(old) != 1:
            raise RuntimeError(f"parameterization anchor changed: {old}")
        source = source.replace(old, new)
    return source


def _compile(temporary: Path, prime: int, source_text: str) -> tuple[Path, str]:
    source = temporary / "homogeneous-transfer.cpp"
    source.write_text(source_text)
    executable = temporary / f"homogeneous-transfer-{prime}"
    command = [
        "g++", "-std=c++20", "-O3", "-DNDEBUG", "-fopenmp",
        f"-DMODULUS={prime}ULL", str(source), "-o", str(executable),
    ]
    result = subprocess.run(command, text=True, capture_output=True, check=True)
    if result.stderr:
        raise RuntimeError(result.stderr)
    version = subprocess.run(
        ["g++", "--version"], text=True, capture_output=True, check=True
    ).stdout.splitlines()[0]
    return executable, version


def _frozen_indices() -> dict[str, object]:
    structural = _case(W, N)["length_rows"][-1]
    genus = structural["genus"]
    vertices, edges = cubic_box((N, W, W))
    labels = _labels(structural, edges)
    fundamental = _fundamental_labels(vertices, edges, labels)
    if fundamental != EXPECTED_LABELS:
        raise AssertionError("Cycle 8 fundamental labels changed")
    shift = 2 * HANDLE_CUT
    left_columns = [label & ((1 << shift) - 1) for label in fundamental]
    right_columns = [label >> shift for label in fundamental]
    target = W * W - 1
    if _rank(left_columns) != target or _rank(right_columns) != target:
        raise AssertionError("Cycle 8 projected cycle images changed")
    selected_left = _independent_row_positions(left_columns, shift)
    selected_right = _independent_row_positions(right_columns, 2 * genus - shift)
    left_characters = [
        sum(((character >> j) & 1) << coordinate for j, coordinate in enumerate(selected_left))
        for character in range(1 << target)
    ]
    right_characters = [
        sum(((character >> j) & 1) << coordinate for j, coordinate in enumerate(selected_right))
        for character in range(1 << target)
    ]
    return {
        "genus": genus,
        "shift": shift,
        "selected_left_dual_coordinates": selected_left,
        "selected_right_dual_coordinates": selected_right,
        "left_characters": left_characters,
        "right_characters": right_characters,
    }


def _evaluate_point(
    executable: Path,
    prime: int,
    point: tuple[int, int, int],
    edge_text: str,
    intersection: list[int],
    indices: dict[str, object],
) -> dict[str, object]:
    _, edges = cubic_box((N, W, W))
    genus = int(indices["genus"])
    tx, ty, tz = point
    header = f"{N} {W} {2 * genus} {len(edges)} 1 {tx} {ty} {tz}\n"
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    started = time.perf_counter()
    result = subprocess.run(
        [str(executable)],
        input=header + edge_text + "\n",
        text=True,
        capture_output=True,
        check=True,
        env=environment,
        timeout=1800,
    )
    raw_g = [int(value) for value in result.stdout.splitlines()]
    if len(raw_g) != 1 << (2 * genus):
        raise AssertionError("character transfer returned the wrong tensor size")
    raw_f = _f_values_from_walsh(raw_g, intersection, prime)
    structural = _case_structural()
    canonical_f, correction = _canonical_reindex(raw_f, structural)
    shift = int(indices["shift"])
    matrix = [
        [
            canonical_f[left | (right << shift)]
            for right in indices["right_characters"]
        ]
        for left in indices["left_characters"]
    ]
    certificate = _det_certificate(matrix, prime)
    return {
        "point": list(point),
        "prime": prime,
        "determinant": certificate["determinant"],
        "nonzero": certificate["determinant"] != 0,
        "pivot_original_rows": certificate.get("pivot_original_rows", []),
        "pivot_values_before_normalization": certificate.get(
            "pivot_values_before_normalization", []
        ),
        "row_swaps": certificate.get("row_swaps", []),
        "canonical_affine_correction": correction,
        "canonical_tensor_sha256": hashlib.sha256(
            b"".join(int(value).to_bytes(4, "little") for value in canonical_f)
        ).hexdigest(),
        "normalization_invertible": (1 << (2 * genus)) % prime != 0,
        "wall_seconds": round(time.perf_counter() - started, 6),
    }


def _case_structural() -> dict[str, object]:
    return _case_frontier()["length_rows"][-1]


def _case_frontier() -> dict[str, object]:
    # Kept behind a named wrapper so the imported `_case` graph constructor is
    # never shadowed by a point evaluator.
    from proof.verify_lane_b_arbitrary_width_frontier import _case as frontier_case
    return frontier_case(W, N)


def verify() -> dict[str, object]:
    if platform.python_version() != "3.12.3":
        raise RuntimeError("Cycle 14 requires the repository-pinned CPython 3.12.3")
    indices = _frozen_indices()
    rotation = universal_checkerboard_rotation(N, W)
    genus = universal_embedding_genus(N, W)
    if genus != indices["genus"]:
        raise AssertionError("embedding genus changed")
    edge_text, labels, intersection = _edge_payload(N, W, rotation, genus)
    source_text = _parameterized_source()
    rows: list[dict[str, object]] = []
    compilers: dict[str, str] = {}
    started = time.perf_counter()
    with tempfile.TemporaryDirectory(prefix="lane-b-homogeneous-w3-") as name:
        temporary = Path(name)
        for prime in PRIMES:
            executable, compiler = _compile(temporary, prime, source_text)
            compilers[str(prime)] = compiler
            for point in ANISOTROPIC_POINTS:
                row = _evaluate_point(executable, prime, point, edge_text, intersection, indices)
                row["locus"] = "anisotropic"
                rows.append(row)
            for t in ISOTROPIC_POINTS:
                row = _evaluate_point(executable, prime, (t, t, t), edge_text, intersection, indices)
                row["locus"] = "isotropic"
                rows.append(row)
    anisotropic_nonzero = any(row["nonzero"] for row in rows if row["locus"] == "anisotropic")
    isotropic_nonzero = any(row["nonzero"] for row in rows if row["locus"] == "isotropic")
    return {
        "claim_status": "PROVED_BY_EXACT_SPECIALIZATION" if anisotropic_nonzero and isotropic_nonzero else "SYMBOLIC_BRANCH_REQUIRED",
        "shape": [N, W, W],
        "genus": genus,
        "minor_size": 1 << (W * W - 1),
        "handle_cut": HANDLE_CUT,
        "primes": list(PRIMES),
        "anisotropic_points": [list(point) for point in ANISOTROPIC_POINTS],
        "isotropic_points": list(ISOTROPIC_POINTS),
        "frozen_tree_edges": list(TREE_EDGES),
        "frozen_chords": list(CHORDS),
        "selected_left_dual_coordinates": indices["selected_left_dual_coordinates"],
        "selected_right_dual_coordinates": indices["selected_right_dual_coordinates"],
        "edge_label_sha256": hashlib.sha256(
            json.dumps(labels, separators=(",", ":")).encode()
        ).hexdigest(),
        "parameterized_source_sha256": hashlib.sha256(source_text.encode()).hexdigest(),
        "compilers": compilers,
        "degree_bounds": {
            "entry_multidegree": {"tx": 81, "ty": 60, "tz": 60},
            "determinant_multidegree": {"tx": 20736, "ty": 15360, "tz": 15360},
            "isotropic_determinant_degree": 51456,
        },
        "anisotropic_nonzero_polynomial": anisotropic_nonzero,
        "isotropic_nonzero_polynomial": isotropic_nonzero,
        "rows": rows,
        "lifting": (
            "Each nonzero determinant modulo a declared prime is a nonzero value of "
            "the frozen integer-polynomial minor. Hence its anisotropic or isotropic "
            "restriction is not identically zero."
        ),
        "isotropic_exception_rule": (
            "The exceptional physical set is {t in (0,1): D_iso(t)=0}; it is finite "
            "with cardinality at most 51456. No every-temperature claim is made."
        ),
        "claim_boundary": (
            "This concerns width three and the frozen G_(10,3) minor only. It does "
            "not prove arbitrary-width homogeneous tightness or nonvanishing at a "
            "specified temperature."
        ),
        "runtime": {
            "python": platform.python_version(),
            "wall_seconds": round(time.perf_counter() - started, 6),
        },
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
