#!/usr/bin/env python3
"""Cycle 16 complete canonical gcd-witness leaf certification."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
import itertools
import multiprocessing
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import CADICAL, DRAT, clauses, coordinate, normalize, sample_bases, sha256
from lrc_proof_diversification import color, discriminating, residue, variable_type

SOURCE = ROOT / "discovery/out/cycle11-certified-sat/p199/007.cnf"
OUT = ROOT / "discovery/out/cycle16-gcd-witness-tree"
CNFS = OUT / "cnfs"
PROOFS = OUT / "proofs"
CORES = OUT / "cores"
CORE_PROOFS = OUT / "core-proofs"
CPUS = (0, 1, 2)
K, P, C = 13, 199, 14
DISK_CAP = 21_474_836_480
PROCESS_MEMORY = 5_368_709_120


@dataclass(frozen=True)
class Result:
    ordinal: int
    pair2: tuple[int, int]
    pair7: tuple[int, int]
    status: str
    units: int
    cnf_sha256: str
    proof_sha256: str
    proof_bytes: int
    seconds: float
    detail: str


def pairs() -> list[tuple[int, int]]:
    return list(itertools.combinations(range(K), 2))


def requirements(pair: tuple[int, int]) -> dict[int, bool]:
    first, second = pair
    result = {index: True for index in range(first)}
    result[first] = False
    result.update({index: True for index in range(first + 1, second)})
    result[second] = False
    return result


def leaf_units(base: tuple[int, ...], pair2: tuple[int, int], pair7: tuple[int, int]) -> tuple[int, ...]:
    req2, req7 = requirements(pair2), requirements(pair7)
    units = set()
    for coordinate in range(K):
        for digit in range(C):
            residue = (base[coordinate] + P * digit) % C
            allowed = True
            if coordinate in req2:
                allowed &= (residue % 2 == 0) == req2[coordinate]
            if coordinate in req7:
                allowed &= (residue % 7 == 0) == req7[coordinate]
            if not allowed:
                units.add(-(1 + coordinate * C + digit))
    return tuple(sorted(units, key=abs))


def write_leaf(path: Path, source: list[frozenset[int]], units: tuple[int, ...]) -> None:
    lines = [f"p cnf 208 {len(source) + len(units)}"]
    lines.extend(" ".join(map(str, sorted(clause, key=lambda literal: (abs(literal), literal)))) + " 0" for clause in source)
    lines.extend(f"{unit} 0" for unit in units)
    path.write_text("\n".join(lines) + "\n")


def run_checked(command: list[str], cpu: int, timeout: int) -> subprocess.CompletedProcess[str]:
    wrapped = ["taskset", "-c", str(cpu), "prlimit", f"--as={PROCESS_MEMORY}", "--", *command]
    process = subprocess.Popen(wrapped, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=5)
        raise
    return subprocess.CompletedProcess(wrapped, process.returncode, stdout, stderr)


def solve_leaf(job: tuple[int, tuple[int, int], tuple[int, int]], cpu: int, source: list[frozenset[int]], base: tuple[int, ...], deadline: float) -> Result:
    ordinal, pair2, pair7 = job
    started = time.monotonic()
    stem = f"{ordinal:04d}"
    cnf, proof = CNFS / f"{stem}.cnf", PROOFS / f"{stem}.drat"
    units = leaf_units(base, pair2, pair7)
    write_leaf(cnf, source, units)
    try:
        remaining = max(1, min(60, int(deadline - time.monotonic())))
        solved = run_checked([str(CADICAL), "-q", "-t", str(remaining), str(cnf), str(proof)], cpu, remaining + 5)
        if solved.returncode == 0:
            return Result(ordinal, pair2, pair7, "CAP", len(units), sha256(cnf), sha256(proof) if proof.exists() else "-", proof.stat().st_size if proof.exists() else 0, time.monotonic() - started, "solver timeout")
        if solved.returncode != 20:
            return Result(ordinal, pair2, pair7, "ERROR", len(units), sha256(cnf), sha256(proof) if proof.exists() else "-", proof.stat().st_size if proof.exists() else 0, time.monotonic() - started, f"solver exit {solved.returncode}")
        checked = run_checked([str(DRAT), str(cnf), str(proof)], cpu, max(1, min(60, int(deadline - time.monotonic()))))
        if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            return Result(ordinal, pair2, pair7, "ERROR", len(units), sha256(cnf), sha256(proof), proof.stat().st_size, time.monotonic() - started, "proof rejected")
        return Result(ordinal, pair2, pair7, "CERTIFIED_UNSAT", len(units), sha256(cnf), sha256(proof), proof.stat().st_size, time.monotonic() - started, "fresh DRAT VERIFIED")
    except subprocess.TimeoutExpired:
        return Result(ordinal, pair2, pair7, "CAP", len(units), sha256(cnf), sha256(proof) if proof.exists() else "-", proof.stat().st_size if proof.exists() else 0, time.monotonic() - started, "wrapper timeout")


def tree() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CNFS.mkdir(parents=True, exist_ok=True)
    PROOFS.mkdir(parents=True, exist_ok=True)
    _, source = clauses(SOURCE)
    base = sample_bases()[7]
    all_pairs = pairs()
    jobs = [(ordinal, pair2, pair7) for ordinal, (pair2, pair7) in enumerate(itertools.product(all_pairs, repeat=2))]
    if len(jobs) != 6084 or len({(pair2, pair7) for _, pair2, pair7 in jobs}) != 6084:
        raise AssertionError("canonical leaf partition enumeration mismatch")
    deadline = time.monotonic() + 3500
    pending: queue.Queue[tuple[int, tuple[int, int], tuple[int, int]]] = queue.Queue()
    for job in jobs:
        pending.put(job)
    results = []
    total_bytes = 0
    lock = threading.Lock()
    halted = threading.Event()

    def worker(cpu: int) -> None:
        nonlocal total_bytes
        while time.monotonic() < deadline and not halted.is_set():
            try:
                job = pending.get_nowait()
            except queue.Empty:
                return
            result = solve_leaf(job, cpu, source, base, deadline)
            with lock:
                results.append(result)
                total_bytes += (CNFS / f"{result.ordinal:04d}.cnf").stat().st_size + result.proof_bytes
                if total_bytes > DISK_CAP:
                    halted.set()
                if len(results) % 100 == 0:
                    print(f"completed={len(results)} certified={sum(row.status == 'CERTIFIED_UNSAT' for row in results)} bytes={total_bytes}", flush=True)

    workers = [threading.Thread(target=worker, args=(cpu,)) for cpu in CPUS]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    while not pending.empty():
        ordinal, pair2, pair7 = pending.get_nowait()
        results.append(Result(ordinal, pair2, pair7, "CAP", 0, "-", "-", 0, 0.0, "aggregate resource cap"))
    results.sort(key=lambda row: row.ordinal)
    lines = ["ordinal\ti\tj\tu\tv\tstatus\tunits\tcnf_sha256\tproof_sha256\tproof_bytes\tseconds\tdetail"]
    lines.extend("\t".join(map(str, (row.ordinal, *row.pair2, *row.pair7, row.status, row.units, row.cnf_sha256, row.proof_sha256, row.proof_bytes, f"{row.seconds:.6f}", row.detail))) for row in results)
    (OUT / "leaves.tsv").write_text("\n".join(lines) + "\n")
    statuses = Counter(row.status for row in results)
    summary = f"certified_unsat={statuses['CERTIFIED_UNSAT']} cap={statuses['CAP']} error={statuses['ERROR']} corpus_bytes={total_bytes}"
    (OUT / "tree.result").write_text(summary + "\n")
    print(summary)


def read_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"), strict=True)) for line in lines[1:]]


def extract_cores() -> None:
    CORES.mkdir(parents=True, exist_ok=True)
    CORE_PROOFS.mkdir(parents=True, exist_ok=True)
    leaves = read_table(OUT / "leaves.tsv")
    if len(leaves) != 6084 or any(row["status"] != "CERTIFIED_UNSAT" for row in leaves):
        raise AssertionError("complete tree required before core extraction")
    selected = sorted(leaves, key=lambda row: (int(row["proof_bytes"]), int(row["ordinal"])))[:608]
    pending: queue.Queue[dict[str, str]] = queue.Queue()
    for row in selected:
        pending.put(row)
    deadline = time.monotonic() + 2500
    results = []
    lock = threading.Lock()
    base = sample_bases()[7]

    def worker(cpu: int) -> None:
        while time.monotonic() < deadline:
            try:
                row = pending.get_nowait()
            except queue.Empty:
                return
            ordinal = int(row["ordinal"])
            stem = f"{ordinal:04d}"
            cnf, proof = CNFS / f"{stem}.cnf", PROOFS / f"{stem}.drat"
            core, core_proof = CORES / f"{stem}.cnf", CORE_PROOFS / f"{stem}.drat"
            started = time.monotonic()
            status, detail = "ERROR", "unclassified"
            count = discriminating_count = 0
            try:
                extracted = run_checked([str(DRAT), str(cnf), str(proof), "-c", str(core)], cpu, max(1, min(120, int(deadline - time.monotonic()))))
                if extracted.returncode != 0 or "VERIFIED" not in extracted.stdout + extracted.stderr:
                    raise RuntimeError("extraction rejected")
                _, source_rows = clauses(cnf)
                _, core_rows = clauses(core)
                if Counter(core_rows) - Counter(source_rows):
                    raise RuntimeError("core is not residual subset")
                solved = run_checked([str(CADICAL), "-q", "-t", "60", str(core), str(core_proof)], cpu, max(1, min(65, int(deadline - time.monotonic()))))
                if solved.returncode != 20:
                    raise RuntimeError(f"core solver exit {solved.returncode}")
                checked = run_checked([str(DRAT), str(core), str(core_proof)], cpu, max(1, min(60, int(deadline - time.monotonic()))))
                if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
                    raise RuntimeError("core proof rejected")
                count = len(core_rows)
                discriminating_count = sum(discriminating(clause) for clause in normalize(core_rows, base))
                status, detail = "CERTIFIED", "residual subset and fresh DRAT VERIFIED"
            except subprocess.TimeoutExpired:
                status, detail = "CAP", "timeout"
            record = (ordinal, int(row["i"]), int(row["j"]), int(row["u"]), int(row["v"]), status, count, discriminating_count, sha256(core) if core.exists() else "-", sha256(core_proof) if core_proof.exists() else "-", time.monotonic() - started, detail)
            with lock:
                results.append(record)
                if len(results) % 100 == 0:
                    print(f"cores_completed={len(results)} certified={sum(item[5] == 'CERTIFIED' for item in results)}", flush=True)

    workers = [threading.Thread(target=worker, args=(cpu,)) for cpu in CPUS]
    for worker_thread in workers:
        worker_thread.start()
    for worker_thread in workers:
        worker_thread.join()
    while not pending.empty():
        row = pending.get_nowait()
        results.append((int(row["ordinal"]), int(row["i"]), int(row["j"]), int(row["u"]), int(row["v"]), "CAP", 0, 0, "-", "-", 0.0, "aggregate cap"))
    results.sort()
    lines = ["ordinal\ti\tj\tu\tv\tstatus\tclauses\tdiscriminating_clauses\tcore_sha256\tproof_sha256\tseconds\tdetail"]
    lines.extend("\t".join(map(str, (*row[:-2], f"{row[-2]:.6f}", row[-1]))) for row in results)
    (OUT / "cores.tsv").write_text("\n".join(lines) + "\n")
    eligible = [row for row in results if row[5] == "CERTIFIED" and row[7] > 0]
    if eligible:
        chosen = min(eligible, key=lambda row: (row[6], -row[7], row[1:5], row[8]))
        summary = f"certified={sum(row[5] == 'CERTIFIED' for row in results)} cap={sum(row[5] == 'CAP' for row in results)} error={sum(row[5] == 'ERROR' for row in results)} selected_ordinal={chosen[0]} selected_clauses={chosen[6]} selected_discriminating={chosen[7]} core_sha256={chosen[8]} proof_sha256={chosen[9]}"
    else:
        summary = f"certified={sum(row[5] == 'CERTIFIED' for row in results)} cap={sum(row[5] == 'CAP' for row in results)} error={sum(row[5] == 'ERROR' for row in results)} selected_ordinal=-1"
    (OUT / "cores.result").write_text(summary + "\n")
    print(summary)


def clause_signature(clause: frozenset[int]) -> dict[int, tuple[int, int, int, int]]:
    colors = sorted({color(value) for value in range(C)})
    result = {}
    for coord in sorted({coordinate(literal) for literal in clause}):
        counts = Counter(color(residue(literal)) for literal in clause if coordinate(literal) == coord)
        result[coord] = tuple(counts[item] for item in colors)
    return result


def validate() -> None:
    selected_ordinal = 74
    pair2, pair7 = (0, 1), (9, 12)
    _, source_raw = clauses(CORES / f"{selected_ordinal:04d}.cnf")
    source_base = sample_bases()[7]
    source = normalize(source_raw, source_base)
    positive = [clause for clause in source if clause and all(literal > 0 and variable_type(literal) == "x" for literal in clause)]
    if len(source) != 27 or len(positive) != 1 or len(positive[0]) != 26:
        raise AssertionError("selected leaf core form mismatch")
    source_clause = positive[0]
    if Counter(source) != Counter([source_clause] + [frozenset({-literal}) for literal in source_clause]):
        raise AssertionError("selected core is not a direct cover deficit")
    source_signature = clause_signature(source_clause)
    colors = sorted({color(value) for value in range(C)})
    validation_dir = OUT / "validation"
    validation_dir.mkdir(parents=True, exist_ok=True)
    records = []
    bases = sample_bases()
    for target_index, cpu in zip((4, 3), (0, 1), strict=True):
        target_cnf = ROOT / f"discovery/out/cycle11-certified-sat/p199/{target_index:03d}.cnf"
        _, target_source = clauses(target_cnf)
        units = leaf_units(bases[target_index], pair2, pair7)
        raw_residual = target_source + [frozenset({unit}) for unit in units]
        normalized = normalize(raw_residual, bases[target_index])
        unit_set = {next(iter(clause)) for clause in normalized if len(clause) == 1}
        match = None
        mapping = None
        for raw_clause, clause in zip(raw_residual, normalized, strict=True):
            if not clause or any(literal < 0 or variable_type(literal) != "x" for literal in clause):
                continue
            if any(-literal not in unit_set for literal in clause):
                continue
            target_signature = clause_signature(clause)
            if sorted(source_signature.values()) != sorted(target_signature.values()):
                continue
            coord_map = {}
            for signature in sorted(set(source_signature.values())):
                left = sorted(coord for coord, value in source_signature.items() if value == signature)
                right = sorted(coord for coord, value in target_signature.items() if value == signature)
                coord_map.update(zip(left, right, strict=True))
            literal_map = {}
            for source_coord, target_coord in coord_map.items():
                source_values = [residue(literal) for literal in source_clause if coordinate(literal) == source_coord]
                target_values = [residue(literal) for literal in clause if coordinate(literal) == target_coord]
                for divisor_color in colors:
                    source_present = sorted(value for value in source_values if color(value) == divisor_color)
                    target_present = sorted(value for value in target_values if color(value) == divisor_color)
                    source_rest = sorted(value for value in range(C) if color(value) == divisor_color and value not in source_present)
                    target_rest = sorted(value for value in range(C) if color(value) == divisor_color and value not in target_present)
                    for left, right in zip(source_present + source_rest, target_present + target_rest, strict=True):
                        literal_map[1 + source_coord * C + left] = 1 + target_coord * C + right
            mapped = Counter(frozenset((1 if literal > 0 else -1) * literal_map[abs(literal)] for literal in source_row) for source_row in source)
            if not (mapped - Counter(normalized)):
                match = raw_clause
                mapping = (coord_map, literal_map)
                break
        if match is None or mapping is None:
            records.append((target_index, "NO_MATCH", 0, "-", "-", "-"))
            continue
        target_core = [match] + [frozenset({-literal}) for literal in match]
        core_path = validation_dir / f"{target_index:03d}.cnf"
        proof_path = validation_dir / f"{target_index:03d}.drat"
        write_leaf(core_path, [], ())
        lines = [f"p cnf 208 {len(target_core)}"] + [" ".join(map(str, sorted(row, key=lambda literal: (abs(literal), literal)))) + " 0" for row in target_core]
        core_path.write_text("\n".join(lines) + "\n")
        solved = run_checked([str(CADICAL), "-q", str(core_path), str(proof_path)], cpu, 60)
        checked = run_checked([str(DRAT), str(core_path), str(proof_path)], cpu, 60)
        if solved.returncode != 20 or checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            raise RuntimeError("validation core certificate failed")
        mapping_path = validation_dir / f"{target_index:03d}.mapping"
        coord_map, literal_map = mapping
        mapping_path.write_text("coordinates " + " ".join(f"{left}:{right}" for left, right in sorted(coord_map.items())) + "\nchoices " + " ".join(f"{left}:{right}" for left, right in sorted(literal_map.items())) + "\n")
        records.append((target_index, "CERTIFIED_MATCH", len(target_core), sha256(core_path), sha256(proof_path), sha256(mapping_path)))
    lines = ["target_index\tstatus\tclauses\tcnf_sha256\tproof_sha256\tmapping_sha256"]
    lines.extend("\t".join(map(str, row)) for row in records)
    (validation_dir / "results.tsv").write_text("\n".join(lines) + "\n")
    summary = f"certified_matches={sum(row[1] == 'CERTIFIED_MATCH' for row in records)} no_match={sum(row[1] == 'NO_MATCH' for row in records)}"
    (validation_dir / "validation.result").write_text(summary + "\n")
    print(summary)


def forbidden_normalized(pair2: tuple[int, int], pair7: tuple[int, int]) -> frozenset[int]:
    req2, req7 = requirements(pair2), requirements(pair7)
    forbidden = set()
    for coord in range(K):
        for value in range(C):
            allowed = True
            if coord in req2:
                allowed &= (value % 2 == 0) == req2[coord]
            if coord in req7:
                allowed &= (value % 7 == 0) == req7[coord]
            if not allowed:
                forbidden.add(1 + coord * C + value)
    return frozenset(forbidden)


def exact_clause_map(source_clause: frozenset[int], target_clause: frozenset[int]) -> bool:
    source_signature, target_signature = clause_signature(source_clause), clause_signature(target_clause)
    if sorted(source_signature.values()) != sorted(target_signature.values()):
        return False
    coord_map = {}
    for signature in sorted(set(source_signature.values())):
        left = sorted(coord for coord, value in source_signature.items() if value == signature)
        right = sorted(coord for coord, value in target_signature.items() if value == signature)
        coord_map.update(zip(left, right, strict=True))
    if len(coord_map) != K or sorted(coord_map.values()) != list(range(K)):
        return False
    colors = sorted({color(value) for value in range(C)})
    mapped = set()
    for source_coord, target_coord in coord_map.items():
        source_values = [residue(literal) for literal in source_clause if coordinate(literal) == source_coord]
        target_values = [residue(literal) for literal in target_clause if coordinate(literal) == target_coord]
        for divisor_color in colors:
            source_present = sorted(value for value in source_values if color(value) == divisor_color)
            target_present = sorted(value for value in target_values if color(value) == divisor_color)
            source_rest = sorted(value for value in range(C) if color(value) == divisor_color and value not in source_present)
            target_rest = sorted(value for value in range(C) if color(value) == divisor_color and value not in target_present)
            for left, right in zip(source_present + source_rest, target_present + target_rest, strict=True):
                if left in source_present:
                    mapped.add(1 + target_coord * C + right)
    return mapped == set(target_clause)


def census_base(index: int) -> tuple[int, list[tuple[int, int]], int]:
    bases = sample_bases()
    _, source_core_raw = clauses(CORES / "0074.cnf")
    source_core = normalize(source_core_raw, bases[7])
    source_clause = next(clause for clause in source_core if len(clause) > 1)
    target_path = ROOT / f"discovery/out/cycle11-certified-sat/p199/{index:03d}.cnf"
    _, target_raw = clauses(target_path)
    target_normalized = normalize(target_raw, bases[index])
    signature = sorted(clause_signature(source_clause).values())
    candidate_clauses = [(clause_index, clause) for clause_index, clause in enumerate(target_normalized) if clause and all(literal > 0 and variable_type(literal) == "x" for literal in clause) and sorted(clause_signature(clause).values()) == signature]
    all_pairs = pairs()
    matches = []
    for ordinal, (pair2, pair7) in enumerate(itertools.product(all_pairs, repeat=2)):
        forbidden = forbidden_normalized(pair2, pair7)
        for clause_index, clause in candidate_clauses:
            if clause.issubset(forbidden) and exact_clause_map(source_clause, clause):
                # The mapped source core is exactly this target clause plus its
                # negated units, all present in the canonical residual.
                matches.append((ordinal, clause_index))
                break
    return index, matches, len(candidate_clauses)


def census_templates() -> None:
    with multiprocessing.Pool(processes=3) as pool:
        results = pool.map(census_base, range(100))
    results.sort()
    certificate_lines = ["base_index\tleaf_ordinal\ttarget_clause_index"]
    summary_lines = ["base_index\tmatches\tcandidate_clauses"]
    for index, matches, candidate_count in results:
        certificate_lines.extend(f"{index}\t{ordinal}\t{clause_index}" for ordinal, clause_index in matches)
        summary_lines.append(f"{index}\t{len(matches)}\t{candidate_count}")
    census_dir = OUT / "census"
    census_dir.mkdir(parents=True, exist_ok=True)
    (census_dir / "certificates.tsv").write_text("\n".join(certificate_lines) + "\n")
    (census_dir / "summary.tsv").write_text("\n".join(summary_lines) + "\n")
    counts = [len(matches) for _, matches, _ in results]
    summary = f"tests={100 * 6084} matches={sum(counts)} complete_bases={sum(count == 6084 for count in counts)} min_matches={min(counts)} max_matches={max(counts)}"
    (census_dir / "census.result").write_text(summary + "\n")
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["tree", "cores", "validate", "census"])
    args = parser.parse_args()
    if args.command == "tree":
        tree()
    elif args.command == "cores":
        extract_cores()
    elif args.command == "validate":
        validate()
    else:
        census_templates()


if __name__ == "__main__":
    main()
