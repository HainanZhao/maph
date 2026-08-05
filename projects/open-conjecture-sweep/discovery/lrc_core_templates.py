#!/usr/bin/env python3
"""Cycle 12 certified core extraction and exact template embedding."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
import hashlib
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
from lrc_certified_sat import encode, base_improper, write_dimacs

RUN11 = ROOT / "discovery/out/cycle11-certified-sat/p199"
OUT = ROOT / "discovery/out/cycle12-core-template"
CORES = OUT / "cores"
CORE_PROOFS = OUT / "core-proofs"
MUS = OUT / "mus"
EXTERNAL_CNFS = OUT / "external-cnfs"
CADICAL = ROOT / "discovery/out/cycle11-tools/cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8/build/cadical"
DRAT = ROOT / "discovery/out/cycle11-tools/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f/drat-trim"
SAMPLE = ROOT / "discovery/out/cycle8-p199-strata.txt"
CENSUS = ROOT / "discovery/out/k13-p199.txt"
CPUS = (0, 1, 2)
K, P, C = 13, 199, 14
TOTAL = 4_748_938
PROCESS_MEMORY = 5_368_709_120


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def clauses(path: Path) -> tuple[int, list[frozenset[int]]]:
    rows = [line for line in path.read_text().splitlines() if line and not line.startswith("c ")]
    header = rows[0].split()
    if header[:2] != ["p", "cnf"]:
        raise AssertionError(f"bad CNF header: {path}")
    variables, expected = map(int, header[2:])
    result = []
    for row in rows[1:]:
        values = tuple(map(int, row.split()))
        if not values or values[-1] != 0:
            raise AssertionError(f"bad clause: {path}")
        result.append(frozenset(values[:-1]))
    if len(result) != expected:
        raise AssertionError(f"clause count mismatch: {path}")
    return variables, result


def run_checked(command: list[str], cpu: int, timeout: int) -> subprocess.CompletedProcess[str]:
    wrapped = ["taskset", "-c", str(cpu), "prlimit", f"--as={PROCESS_MEMORY}", "--", *command]
    process = subprocess.Popen(wrapped, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.wait()
        raise
    return subprocess.CompletedProcess(wrapped, process.returncode, stdout, stderr)


@dataclass(frozen=True)
class CoreResult:
    index: int
    status: str
    clauses: int
    source_clauses: int
    core_sha256: str
    proof_sha256: str
    seconds: float
    detail: str


def extract_one(index: int, cpu: int, deadline: float) -> CoreResult:
    started = time.monotonic()
    source = RUN11 / f"{index:03d}.cnf"
    source_proof = RUN11 / f"{index:03d}.drat"
    core = CORES / f"{index:03d}.cnf"
    proof = CORE_PROOFS / f"{index:03d}.drat"
    timeout = max(1, min(1200, int(deadline - time.monotonic())))
    try:
        extracted = run_checked([str(DRAT), str(source), str(source_proof), "-c", str(core)], cpu, timeout)
    except subprocess.TimeoutExpired:
        return CoreResult(index, "CAP", 0, 0, "-", "-", time.monotonic() - started, "extract timeout")
    if extracted.returncode != 0 or "VERIFIED" not in extracted.stdout + extracted.stderr:
        return CoreResult(index, "ERROR", 0, 0, "-", "-", time.monotonic() - started, "source proof rejected")
    _, source_rows = clauses(source)
    variables, core_rows = clauses(core)
    if variables != 208 or Counter(core_rows) - Counter(source_rows):
        return CoreResult(index, "ERROR", len(core_rows), len(source_rows), sha256(core), "-", time.monotonic() - started, "core is not source-clause subset")
    timeout = max(1, min(300, int(deadline - time.monotonic())))
    try:
        solved = run_checked([str(CADICAL), "-q", "-t", str(timeout), str(core), str(proof)], cpu, timeout + 10)
    except subprocess.TimeoutExpired:
        return CoreResult(index, "CAP", len(core_rows), len(source_rows), sha256(core), "-", time.monotonic() - started, "core solve timeout")
    if solved.returncode != 20:
        return CoreResult(index, "ERROR", len(core_rows), len(source_rows), sha256(core), sha256(proof) if proof.exists() else "-", time.monotonic() - started, f"core solver exit {solved.returncode}")
    timeout = max(1, min(600, int(deadline - time.monotonic())))
    try:
        verified = run_checked([str(DRAT), str(core), str(proof)], cpu, timeout)
    except subprocess.TimeoutExpired:
        return CoreResult(index, "CAP", len(core_rows), len(source_rows), sha256(core), sha256(proof), time.monotonic() - started, "core proof timeout")
    if verified.returncode != 0 or "VERIFIED" not in verified.stdout + verified.stderr:
        return CoreResult(index, "ERROR", len(core_rows), len(source_rows), sha256(core), sha256(proof), time.monotonic() - started, "core proof rejected")
    return CoreResult(index, "CERTIFIED", len(core_rows), len(source_rows), sha256(core), sha256(proof), time.monotonic() - started, "source subset and fresh DRAT VERIFIED")


def extract_all() -> None:
    CORES.mkdir(parents=True, exist_ok=True)
    CORE_PROOFS.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 1800
    pending: queue.Queue[int] = queue.Queue()
    for index in range(100):
        pending.put(index)
    results: list[CoreResult] = []
    lock = threading.Lock()

    def worker(cpu: int) -> None:
        while time.monotonic() < deadline:
            try:
                index = pending.get_nowait()
            except queue.Empty:
                return
            result = extract_one(index, cpu, deadline)
            with lock:
                results.append(result)

    workers = [threading.Thread(target=worker, args=(cpu,)) for cpu in CPUS]
    for worker_thread in workers:
        worker_thread.start()
    for worker_thread in workers:
        worker_thread.join()
    while not pending.empty():
        results.append(CoreResult(pending.get_nowait(), "CAP", 0, 0, "-", "-", 0.0, "aggregate cap"))
    results.sort(key=lambda row: row.index)
    lines = ["index\tstatus\tclauses\tsource_clauses\tcore_sha256\tproof_sha256\tseconds\tdetail"]
    lines.extend("\t".join(map(str, (row.index, row.status, row.clauses, row.source_clauses, row.core_sha256, row.proof_sha256, f"{row.seconds:.6f}", row.detail))) for row in results)
    (OUT / "cores.tsv").write_text("\n".join(lines) + "\n")
    certified = sum(row.status == "CERTIFIED" for row in results)
    (OUT / "extract.result").write_text(f"certified={certified} cap={sum(row.status == 'CAP' for row in results)} error={sum(row.status == 'ERROR' for row in results)}\n")
    print((OUT / "extract.result").read_text().strip())


def write_rows(path: Path, rows: list[frozenset[int]]) -> None:
    lines = [f"p cnf 208 {len(rows)}"]
    lines.extend(" ".join(map(str, sorted(row, key=lambda literal: (abs(literal), literal)))) + " 0" for row in rows)
    path.write_text("\n".join(lines) + "\n")


def shrink_selected_core() -> None:
    MUS.mkdir(parents=True, exist_ok=True)
    _, original = clauses(CORES / "076.cnf")
    if len(original) != 302:
        raise AssertionError("selected core size mismatch")
    current = list(enumerate(original))
    candidate_path = MUS / "candidate.cnf"
    candidate_proof = MUS / "candidate.drat"
    deadline = time.monotonic() + 240
    records: list[tuple[int, str, int, float]] = []
    for original_index in range(len(original)):
        started = time.monotonic()
        candidate = [entry for entry in current if entry[0] != original_index]
        write_rows(candidate_path, [row for _, row in candidate])
        remaining = int(deadline - time.monotonic())
        if remaining <= 0:
            records.append((original_index, "RETAIN_CAP", len(current), time.monotonic() - started))
            continue
        try:
            solved = run_checked([str(CADICAL), "-q", "-t", str(min(10, remaining)), str(candidate_path), str(candidate_proof)], 0, min(12, remaining))
        except subprocess.TimeoutExpired:
            records.append((original_index, "RETAIN_CAP", len(current), time.monotonic() - started))
            continue
        if solved.returncode == 10:
            records.append((original_index, "RETAIN_SAT", len(current), time.monotonic() - started))
            continue
        if solved.returncode != 20:
            records.append((original_index, "RETAIN_ERROR", len(current), time.monotonic() - started))
            continue
        remaining = int(deadline - time.monotonic())
        try:
            verified = run_checked([str(DRAT), str(candidate_path), str(candidate_proof)], 0, max(1, min(10, remaining)))
        except subprocess.TimeoutExpired:
            records.append((original_index, "RETAIN_CAP", len(current), time.monotonic() - started))
            continue
        if verified.returncode == 0 and "VERIFIED" in verified.stdout + verified.stderr:
            current = candidate
            records.append((original_index, "DELETE_CERTIFIED", len(current), time.monotonic() - started))
        else:
            records.append((original_index, "RETAIN_ERROR", len(current), time.monotonic() - started))
    final_cnf = MUS / "076.cnf"
    final_proof = MUS / "076.drat"
    write_rows(final_cnf, [row for _, row in current])
    remaining = int(deadline - time.monotonic())
    if remaining <= 0:
        raise SystemExit("no time for final MUS certificate")
    solved = run_checked([str(CADICAL), "-q", "-t", str(min(30, remaining)), str(final_cnf), str(final_proof)], 0, min(35, remaining))
    if solved.returncode != 20:
        raise SystemExit("final MUS solver did not return UNSAT")
    remaining = int(deadline - time.monotonic())
    verified = run_checked([str(DRAT), str(final_cnf), str(final_proof)], 0, max(1, min(30, remaining)))
    if verified.returncode != 0 or "VERIFIED" not in verified.stdout + verified.stderr:
        raise SystemExit("final MUS proof rejected")
    lines = ["original_clause\tstatus\tremaining_clauses\tseconds"]
    lines.extend("\t".join(map(str, (index, status, count, f"{seconds:.6f}"))) for index, status, count, seconds in records)
    (MUS / "deletions.tsv").write_text("\n".join(lines) + "\n")
    summary = f"original_clauses={len(original)} final_clauses={len(current)} certified_deletions={sum(status == 'DELETE_CERTIFIED' for _, status, _, _ in records)} caps={sum(status == 'RETAIN_CAP' for _, status, _, _ in records)} errors={sum(status == 'RETAIN_ERROR' for _, status, _, _ in records)} cnf_sha256={sha256(final_cnf)} proof_sha256={sha256(final_proof)}"
    (MUS / "shrink.result").write_text(summary + "\n")
    print(summary)


def sample_bases() -> list[tuple[int, ...]]:
    result = [tuple(map(int, line.split())) for line in SAMPLE.read_text().splitlines()]
    if len(result) != 100:
        raise AssertionError("sample length mismatch")
    return result


def external_bases() -> list[tuple[int, ...]]:
    indices = [stratum * TOTAL // 10 + offset for stratum in range(10) for offset in range(10, 20)]
    wanted = set(indices)
    selected: dict[int, tuple[int, ...]] = {}
    with CENSUS.open() as handle:
        for index, line in enumerate(handle):
            if index in wanted:
                selected[index] = tuple(map(int, line.split()))
    if len(selected) != 100:
        raise AssertionError("external sample mismatch")
    rows = [selected[index] for index in indices]
    (OUT / "external-bases.txt").write_text("\n".join(" ".join(map(str, row)) for row in rows) + "\n")
    (OUT / "external-indices.txt").write_text("\n".join(map(str, indices)) + "\n")
    return rows


def normalized_literal(literal: int, base: tuple[int, ...]) -> int:
    sign = 1 if literal > 0 else -1
    variable = abs(literal)
    if variable <= K * C:
        coordinate, digit = divmod(variable - 1, C)
        residue = (base[coordinate] + (P % C) * digit) % C
        mapped = 1 + coordinate * C + residue
    else:
        mapped = variable
    return sign * mapped


def normalize(rows: list[frozenset[int]], base: tuple[int, ...]) -> list[frozenset[int]]:
    return [frozenset(normalized_literal(literal, base) for literal in row) for row in rows]


def coordinate(variable: int) -> int:
    variable = abs(variable)
    if variable <= K * C:
        return (variable - 1) // C
    if variable <= K * C + K:
        return variable - (K * C + 1)
    return variable - (K * C + K + 1)


def map_literal(literal: int, mapping: dict[int, int]) -> int:
    sign = 1 if literal > 0 else -1
    variable = abs(literal)
    if variable <= K * C:
        source, residue = divmod(variable - 1, C)
        mapped = 1 + mapping[source] * C + residue
    elif variable <= K * C + K:
        mapped = K * C + 1 + mapping[variable - (K * C + 1)]
    else:
        mapped = K * C + K + 1 + mapping[variable - (K * C + K + 1)]
    return sign * mapped


@dataclass(frozen=True)
class Embedding:
    status: str
    mapping: tuple[int, ...]
    nodes: int


@lru_cache(maxsize=1)
def universal_clauses() -> frozenset[frozenset[int]]:
    base = tuple(range(1, K + 1))
    formula = encode(base, P, C)
    prefix = K * (1 + C * (C - 1) // 2)
    suffix = prefix + P * C
    fixed = list(formula.clauses[:prefix]) + list(formula.clauses[suffix:])
    return frozenset(normalize([frozenset(row) for row in fixed], base))


def embed(core_rows: list[frozenset[int]], target_rows: list[frozenset[int]], deadline: float) -> Embedding:
    target = Counter(target_rows)
    # Exactly-one and gcd-channel clauses map universally.  They are retained
    # in the final exact containment check but cannot prune a permutation, so
    # backtrack only on the base-specific clauses.
    varying = [row for row in core_rows if row not in universal_clauses()]
    constrained = [(row, frozenset(coordinate(literal) for literal in row)) for row in varying]
    unary: list[list[frozenset[int]]] = [[] for _ in range(K)]
    degree = [0] * K
    for row, coords in constrained:
        for source in coords:
            degree[source] += 1
        if len(coords) == 1:
            unary[next(iter(coords))].append(row)
    domains: list[list[int]] = []
    for source in range(K):
        candidates = []
        for target_coordinate in range(K):
            mapping = {source: target_coordinate}
            if all(frozenset(map_literal(literal, mapping) for literal in row) in target for row in unary[source]):
                candidates.append(target_coordinate)
        domains.append(candidates)
    order = sorted(range(K), key=lambda source: (len(domains[source]), -degree[source], source))
    mapping: dict[int, int] = {}
    used: set[int] = set()
    nodes = 0

    def search(depth: int) -> bool:
        nonlocal nodes
        nodes += 1
        if nodes % 1024 == 0 and time.monotonic() > deadline:
            raise TimeoutError
        if depth == K:
            mapped = Counter(frozenset(map_literal(literal, mapping) for literal in row) for row in core_rows)
            return not (mapped - target)
        source = order[depth]
        for target_coordinate in domains[source]:
            if target_coordinate in used:
                continue
            mapping[source] = target_coordinate
            used.add(target_coordinate)
            valid = True
            assigned = mapping.keys()
            for row, coords in constrained:
                if source in coords and coords.issubset(assigned):
                    mapped_row = frozenset(map_literal(literal, mapping) for literal in row)
                    if mapped_row not in target:
                        valid = False
                        break
            if valid and search(depth + 1):
                return True
            used.remove(target_coordinate)
            del mapping[source]
        return False

    try:
        found = search(0)
    except TimeoutError:
        return Embedding("CAP", (), nodes)
    if not found:
        return Embedding("NO_MATCH", (), nodes)
    result = tuple(mapping[index] for index in range(K))
    mapped = Counter(frozenset(map_literal(literal, mapping) for literal in row) for row in core_rows)
    if mapped - target or sorted(result) != list(range(K)):
        raise AssertionError("embedding final check failed")
    return Embedding("MATCH", result, nodes)


def full_formula(base: tuple[int, ...], path: Path | None = None) -> list[frozenset[int]]:
    formula = encode(base, P, C)
    if path is not None:
        write_dimacs(formula, path)
    return normalize([frozenset(row) for row in formula.clauses], base)


def score_shard(
    template_indices: list[int],
    sample: list[tuple[int, ...]],
    validation: dict[int, list[frozenset[int]]],
    validation_indices: list[int],
    deadline: float,
    cpu: int,
    output: multiprocessing.Queue,
) -> None:
    os.sched_setaffinity(0, {cpu})
    try:
        rows: list[tuple[int, int, int, str, int]] = []
        for template in template_indices:
            _, raw_core = clauses(CORES / f"{template:03d}.cnf")
            core = normalize(raw_core, sample[template])
            matches = 0
            nodes = 0
            for target_index in validation_indices:
                result = embed(core, validation[target_index], deadline)
                if result.status == "CAP":
                    raise TimeoutError("validation embedding cap")
                matches += result.status == "MATCH"
                nodes += result.nodes
            rows.append((template, matches, len(core), sha256(CORES / f"{template:03d}.cnf"), nodes))
        output.put(("OK", rows))
    except BaseException as error:
        output.put(("ERROR", repr(error)))


def evaluation_shard(
    tasks: list[tuple[int, tuple[int, ...], str]],
    core: list[frozenset[int]],
    deadline: float,
    cpu: int,
    output: multiprocessing.Queue,
) -> None:
    os.sched_setaffinity(0, {cpu})
    try:
        rows = []
        for index, base, cnf_name in tasks:
            path = Path(cnf_name) if cnf_name else None
            target = full_formula(base, path)
            result = embed(core, target, deadline)
            rows.append((index, result.status, result.nodes, result.mapping, sha256(path) if path else "-"))
        output.put(("OK", rows))
    except BaseException as error:
        output.put(("ERROR", repr(error)))


def run_evaluation(
    tasks: list[tuple[int, tuple[int, ...], str]],
    core: list[frozenset[int]],
    deadline: float,
) -> list[tuple[int, str, int, tuple[int, ...], str]]:
    context = multiprocessing.get_context("fork")
    output: multiprocessing.Queue = context.Queue()
    shards = [tasks[offset::len(CPUS)] for offset in range(len(CPUS))]
    processes = [context.Process(target=evaluation_shard, args=(shard, core, deadline, cpu, output)) for shard, cpu in zip(shards, CPUS, strict=True)]
    for process in processes:
        process.start()
    rows = []
    for _ in processes:
        status, value = output.get()
        if status != "OK":
            for process in processes:
                process.terminate()
            raise SystemExit(value)
        rows.extend(value)
    for process in processes:
        process.join()
        if process.exitcode != 0:
            raise SystemExit(f"evaluation worker exit {process.exitcode}")
    return sorted(rows)


def search_templates() -> None:
    rows = (OUT / "cores.tsv").read_text().splitlines()
    if len(rows) != 101 or any(line.split("\t")[1] != "CERTIFIED" for line in rows[1:]):
        raise SystemExit("core certification gate failed")
    sample = sample_bases()
    validation_indices = [index for index in range(100) if index % 10 >= 8]
    training_indices = [index for index in range(100) if index % 10 < 8]
    validation = {index: full_formula(sample[index]) for index in validation_indices}
    deadline = time.monotonic() + 1000
    context = multiprocessing.get_context("fork")
    output: multiprocessing.Queue = context.Queue()
    shards = [training_indices[offset::len(CPUS)] for offset in range(len(CPUS))]
    processes = [
        context.Process(target=score_shard, args=(shard, sample, validation, validation_indices, deadline, cpu, output))
        for shard, cpu in zip(shards, CPUS, strict=True)
    ]
    for process in processes:
        process.start()
    score_rows: list[tuple[int, int, int, str, int]] = []
    for _ in processes:
        status, value = output.get()
        if status != "OK":
            for process in processes:
                process.terminate()
            raise SystemExit(value)
        score_rows.extend(value)
    for process in processes:
        process.join()
        if process.exitcode != 0:
            raise SystemExit(f"validation worker exit {process.exitcode}")
    score_rows.sort(key=lambda row: row[0])
    score_lines = ["template\tvalidation_matches\tcore_clauses\tcore_sha256\tnodes"]
    score_lines.extend("\t".join(map(str, row)) for row in score_rows)
    (OUT / "validation-scores.tsv").write_text("\n".join(score_lines) + "\n")
    selected = min(score_rows, key=lambda row: (-row[1], row[2], row[3]))
    template = selected[0]
    _, selected_raw_core = clauses(CORES / f"{template:03d}.cnf")
    selected_core = normalize(selected_raw_core, sample[template])
    external = external_bases()
    EXTERNAL_CNFS.mkdir(parents=True, exist_ok=True)
    result_lines = ["target\tcensus_index\tstatus\tnodes\tmapping\tcnf_sha256"]
    indices = list(map(int, (OUT / "external-indices.txt").read_text().splitlines()))
    matched = 0
    capped = 0
    for target_index, base in enumerate(external):
        if not base_improper(base, P):
            raise AssertionError("external base is not l=1 improper")
        cnf_path = EXTERNAL_CNFS / f"{target_index:03d}.cnf"
        target = full_formula(base, cnf_path)
        result = embed(selected_core, target, deadline)
        matched += result.status == "MATCH"
        capped += result.status == "CAP"
        result_lines.append("\t".join(map(str, (target_index, indices[target_index], result.status, result.nodes, ",".join(map(str, result.mapping)) or "-", sha256(cnf_path)))))
    (OUT / "external-results.tsv").write_text("\n".join(result_lines) + "\n")
    summary = f"selected_template={template} validation_matches={selected[1]} external_matches={matched} external_caps={capped} core_clauses={selected[2]}"
    (OUT / "search.result").write_text(summary + "\n")
    print(summary)


def search_shrunk_template() -> None:
    sample = sample_bases()
    _, raw_core = clauses(MUS / "076.cnf")
    core = normalize(raw_core, sample[76])
    deadline = time.monotonic() + 360
    validation_indices = [index for index in range(100) if index % 10 >= 8]
    validation_tasks = [(index, sample[index], "") for index in validation_indices]
    validation = run_evaluation(validation_tasks, core, deadline)
    validation_lines = ["target\tstatus\tnodes\tmapping"]
    validation_lines.extend("\t".join(map(str, (index, status, nodes, ",".join(map(str, mapping)) or "-"))) for index, status, nodes, mapping, _ in validation)
    (MUS / "validation.tsv").write_text("\n".join(validation_lines) + "\n")
    external = external_bases()
    indices = list(map(int, (OUT / "external-indices.txt").read_text().splitlines()))
    EXTERNAL_CNFS.mkdir(parents=True, exist_ok=True)
    external_tasks = [(index, base, str(EXTERNAL_CNFS / f"{index:03d}.cnf")) for index, base in enumerate(external)]
    evaluated = run_evaluation(external_tasks, core, deadline)
    external_lines = ["target\tcensus_index\tstatus\tnodes\tmapping\tcnf_sha256"]
    external_lines.extend("\t".join(map(str, (index, indices[index], status, nodes, ",".join(map(str, mapping)) or "-", digest))) for index, status, nodes, mapping, digest in evaluated)
    (MUS / "external.tsv").write_text("\n".join(external_lines) + "\n")
    validation_matches = sum(status == "MATCH" for _, status, _, _, _ in validation)
    external_matches = sum(status == "MATCH" for _, status, _, _, _ in evaluated)
    caps = sum(status == "CAP" for _, status, _, _, _ in validation + evaluated)
    summary = f"template=76 final_clauses={len(raw_core)} validation_matches={validation_matches} external_matches={external_matches} caps={caps}"
    (MUS / "search.result").write_text(summary + "\n")
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("extract", "search", "shrink", "search-shrunk"), required=True)
    args = parser.parse_args()
    if args.stage == "extract":
        extract_all()
    elif args.stage == "search":
        search_templates()
    elif args.stage == "shrink":
        shrink_selected_core()
    else:
        search_shrunk_template()


if __name__ == "__main__":
    main()
