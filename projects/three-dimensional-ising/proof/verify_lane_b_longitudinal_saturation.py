#!/usr/bin/env python3
"""Exact longitudinal-rank certificates for the corrected width-three family."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.verify_lane_b_cochain_gauge import semantic_edge_data, semantic_transport_rows  # noqa: E402
from src.conventions import cubic_box  # noqa: E402


PRIMARY_PRIME = 1_000_000_007
CONTROL_PRIME = 1_000_000_009


def _compile_transfer(directory: Path, prime: int) -> tuple[Path, str]:
    source = ROOT / "proof" / "lane_b_gauge_reduced_character_transfer.cpp"
    executable = directory / f"transfer-{prime}"
    command = [
        "g++", "-std=c++20", "-O3", "-DNDEBUG", "-fopenmp",
        f"-DMODULUS={prime}ULL", str(source), "-o", str(executable),
    ]
    subprocess.run(command, check=True, text=True, capture_output=True)
    version = subprocess.run(
        ["g++", "--version"], check=True, text=True, capture_output=True
    ).stdout.splitlines()[0]
    return executable, version


def _independent_gauge_control(directory: Path, optimized: Path) -> dict[str, object]:
    source = ROOT / "proof" / "lane_b_width4_character_transfer.cpp"
    legacy = directory / "legacy-transfer-control"
    subprocess.run([
        "g++", "-std=c++20", "-O3", "-DNDEBUG", "-fopenmp",
        f"-DMODULUS={PRIMARY_PRIME}ULL", str(source), "-o", str(legacy),
    ], check=True, text=True, capture_output=True)
    text, _ = _edge_input(9, 2)
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    left = subprocess.run(
        [str(legacy)], input=text, text=True, capture_output=True, check=True,
        env=environment, timeout=1800,
    ).stdout
    right = subprocess.run(
        [str(optimized)], input=text, text=True, capture_output=True, check=True,
        env=environment, timeout=1800,
    ).stdout
    if left != right:
        raise AssertionError("gauge-reduced transfer disagrees with the frozen legacy engine")
    return {
        "shape": [9, 3, 3],
        "regime": "homogeneous_isotropic",
        "characters": 1 << 16,
        "legacy_and_gauge_reduced_outputs_identical": True,
    }


def _compile_certificate(directory: Path, prime: int, mode: str, target: int) -> Path:
    source = ROOT / "proof" / "lane_b_modular_determinant.cpp"
    executable = directory / f"certificate-{prime}-{mode}-{target}"
    command = [
        "g++", "-std=c++20", "-O3", "-DNDEBUG",
        f"-DMODULUS={prime}ULL", f"-DMODE={1 if mode == 'F' else 0}",
        f"-DRANK_TARGET={target}", str(source), "-lntl", "-lgmp", "-o", str(executable),
    ]
    subprocess.run(command, check=True, text=True, capture_output=True)
    return executable


def _edge_input(length: int, regime: int) -> tuple[str, dict[str, object]]:
    labels, canonical = semantic_edge_data(length)
    transport = semantic_transport_rows(length)
    _, edges = cubic_box((length, 3, 3))
    lines = []
    for edge, label in zip(edges, labels):
        axis = next(index for index in range(3) if edge.u[index] != edge.v[index])
        left = 3 * edge.u[1] + edge.u[2]
        right = 3 * edge.v[1] + edge.v[2]
        lines.append(f"{edge.u[0]} {axis} {left} {right} {label}")
    dimension = 2 * (length - 1)
    header = f"{length} 3 {dimension} {len(edges)} {regime}\n"
    metadata = {
        "shape": [length, 3, 3],
        "genus": length - 1,
        "homology_bits": dimension,
        "homology_labels_sha256": hashlib.sha256(
            json.dumps(labels, separators=(",", ":")).encode()
        ).hexdigest(),
        "symplectic_transport_sha256": hashlib.sha256(
            json.dumps(transport, separators=(",", ":")).encode()
        ).hexdigest(),
        "canonical_intersection_rows": canonical,
        "edge_order": "src.conventions.cubic_box lexicographic",
        "coordinate_order": "(a0,b0,a1,b1,...) in corrected nested symplectic coordinates",
        "cut_order": "low coordinate bits are rows; high coordinate bits are columns",
    }
    return header + "\n".join(lines) + "\n", metadata


def _run_case(
    transfer: Path,
    certificates: dict[tuple[str, int], Path],
    prime: int,
    length: int,
    regime: int,
) -> dict[str, object]:
    text, metadata = _edge_input(length, regime)
    dimension = 2 * (length - 1)
    side = 1 << (dimension // 2)
    target = min(side, 256)
    environment = dict(os.environ)
    environment["OMP_NUM_THREADS"] = "3"
    started = time.perf_counter()
    transfer_result = subprocess.run(
        [str(transfer)], input=text, text=True, capture_output=True, check=True,
        env=environment, timeout=1800,
    )
    transfer_seconds = time.perf_counter() - started
    if len(transfer_result.stdout.splitlines()) != 1 << dimension:
        raise AssertionError("character engine returned the wrong tensor size")
    evidence: dict[str, object] = {}
    for mode in ("G", "F"):
        certificate = subprocess.run(
            [str(certificates[mode, target])],
            input=f"{dimension}\n" + transfer_result.stdout,
            text=True, capture_output=True, check=True, timeout=1800,
        )
        record = json.loads(certificate.stdout)
        if record["rank_lower_bound"] != target or not int(record["projected_determinant"]):
            raise AssertionError("projected rank certificate vanished")
        evidence[mode] = record
    names = {
        0: ("nonuniform", "deterministic independent nonzero edge values"),
        1: ("homogeneous_anisotropic", "(t_x,t_y,t_z)=(2,3,5)"),
        2: ("homogeneous_isotropic", "t_x=t_y=t_z=2"),
    }
    name, specialization = names[regime]
    return {
        **metadata,
        "regime": name,
        "weight_specialization": specialization,
        "field": f"GF({prime})",
        "central_cut_type": "pair" if (dimension // 2) % 2 == 0 else "internal",
        "central_side": side,
        "proved_upper_bound": min(side, 256),
        "exact_central_rank": target,
        "certificates": evidence,
        "normalization": {
            "inverse_Walsh_denominator": 1 << dimension,
            "denominator_invertible": (1 << dimension) % prime != 0,
            "one_handle_transform_denominator": 2,
            "two_invertible": 2 % prime != 0,
        },
        "transfer_wall_seconds": round(transfer_seconds, 6),
    }


def verify() -> dict[str, object]:
    with tempfile.TemporaryDirectory(prefix="lane-b-longitudinal-") as temporary_name:
        temporary = Path(temporary_name)
        audits: dict[str, object] = {}
        compiler = ""
        gauge_control: dict[str, object] | None = None
        schedule = {
            PRIMARY_PRIME: [(length, regime) for length in range(4, 13) for regime in range(3)],
            CONTROL_PRIME: [(length, 2) for length in range(9, 13)],
        }
        for prime, jobs in schedule.items():
            transfer, compiler = _compile_transfer(temporary, prime)
            if prime == PRIMARY_PRIME:
                gauge_control = _independent_gauge_control(temporary, transfer)
            targets = {min(1 << (length - 1), 256) for length, _ in jobs}
            certificates = {
                (mode, target): _compile_certificate(temporary, prime, mode, target)
                for target in targets for mode in ("G", "F")
            }
            cases = [
                _run_case(transfer, certificates, prime, length, regime)
                for length, regime in jobs
            ]
            audits[str(prime)] = {
                "prime": prime,
                "cases": cases,
                "schedule": (
                    "all regimes n=4..12" if prime == PRIMARY_PRIME
                    else "independent isotropic control n=9..12"
                ),
            }
    primary = audits[str(PRIMARY_PRIME)]["cases"]
    for regime in ("nonuniform", "homogeneous_anisotropic", "homogeneous_isotropic"):
        sequence = [case["exact_central_rank"] for case in primary if case["regime"] == regime]
        if sequence != [8, 16, 32, 64, 128, 256, 256, 256, 256]:
            raise AssertionError(f"longitudinal rank sequence changed for {regime}: {sequence}")
    return {
        "claim_status": "CERTIFIED_NUMERICAL with PROVED cochain upper bound",
        "compiler": compiler,
        "arithmetic": {
            "primary_prime": PRIMARY_PRIME,
            "control_prime": CONTROL_PRIME,
            "lifting": (
                "Each projected determinant is a determinant of fixed integer linear "
                "combinations of flattening rows and columns. Nonzero reduction proves rank "
                "at least the target over the corresponding symbolic coefficient field."
            ),
        },
        "independent_gauge_reduction_control": gauge_control,
        "central_rank_law_n4_to_n12": "min(2^(n-1),256) in all three primary-prime regimes",
        "saturation": {
            "R_infinity_pair_w3": 256,
            "first_pair_witness_n": 9,
            "R_infinity_internal_w3": 256,
            "first_internal_witness_n": 10,
            "upper_bound_source": "proof/lane_b_cochain_gauge_proof.md",
        },
        "prime_audits": audits,
        "claim_boundary": (
            "The exact equality is proved for the saturation suprema by combining the local "
            "all-length upper bound with the recorded finite-field lower witnesses. The displayed "
            "central sequence is certified only for n=4..12. A symbolic recurrence at every n, "
            "a growing-width estimate, and a cubic-box result are not claimed."
        ),
    }


if __name__ == "__main__":
    print(json.dumps(verify(), indent=2, sort_keys=True))
