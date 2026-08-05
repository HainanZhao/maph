#!/usr/bin/env python3
"""Cycle 15 LRAT dependency slicing and fresh candidate checks."""

from __future__ import annotations

import argparse
from array import array
from collections import Counter, deque
from dataclasses import dataclass
import hashlib
import multiprocessing
import os
from pathlib import Path
import queue
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import C, K, CADICAL, DRAT, clauses, normalize, sample_bases, sha256
from lrc_proof_diversification import discriminating

OUT = ROOT / "discovery/out/cycle15-resolution-slicing"
SOURCE = ROOT / "discovery/out/cycle14-proof-diversification/cores/007/noelimprobe/default.cnf"
LRAT = OUT / "source.lrat"
CANDIDATES = OUT / "candidates"
PROOFS = OUT / "proofs"
MODELS = OUT / "models"
CPUS = (0, 1, 2)
INPUTS = 2329
PROTECTED_ID = 1000
PROCESS_MEMORY = 5_368_709_120


def parsed_addition(line: bytes) -> tuple[int, list[int]] | None:
    values = list(map(int, line.split()))
    if len(values) > 1 and values[1] == 100:  # ASCII 'd' is not parsed as int; retained for type clarity.
        return None
    clause_id = values[0]
    first_zero = values.index(0, 1)
    return clause_id, values[first_zero + 1:-1]


def scan() -> tuple[int, int, int]:
    maximum = 0
    empty = 0
    edges = 0
    with LRAT.open("rb") as handle:
        for line in handle:
            fields = line.split()
            if len(fields) > 1 and fields[1] == b"d":
                continue
            values = list(map(int, fields))
            clause_id = values[0]
            maximum = max(maximum, clause_id)
            first_zero = values.index(0, 1)
            hints = values[first_zero + 1:-1]
            if any(hint <= 0 or hint >= clause_id for hint in hints):
                raise AssertionError("LRAT antecedent ordering mismatch")
            if first_zero == 1:
                empty = clause_id
            edges += len(hints)
    if empty == 0:
        raise AssertionError("missing LRAT empty clause")
    return maximum, empty, edges


def build_graph() -> tuple[array, array, int]:
    maximum, empty, expected_edges = scan()
    starts = array("q", [-1]) * (maximum + 1)
    ends = array("q", [-1]) * (maximum + 1)
    hints = array("i")
    with LRAT.open("rb") as handle:
        for line in handle:
            fields = line.split()
            if len(fields) > 1 and fields[1] == b"d":
                continue
            values = list(map(int, fields))
            clause_id = values[0]
            first_zero = values.index(0, 1)
            starts[clause_id] = len(hints)
            hints.extend(values[first_zero + 1:-1])
            ends[clause_id] = len(hints)
    if len(hints) != expected_edges:
        raise AssertionError("LRAT edge count mismatch")
    return starts, ends, empty, hints


def candidate_ids(ranking: list[int], size: int) -> tuple[int, ...]:
    selected = ranking[:size]
    if PROTECTED_ID not in selected:
        selected[-1] = PROTECTED_ID
    return tuple(sorted(selected))


def write_cnf(path: Path, rows: list[frozenset[int]]) -> None:
    lines = [f"p cnf {K * C + 2 * K} {len(rows)}"]
    lines.extend(" ".join(map(str, sorted(row, key=lambda literal: (abs(literal), literal)))) + " 0" for row in rows)
    path.write_text("\n".join(lines) + "\n")


def analyze() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    CANDIDATES.mkdir(parents=True, exist_ok=True)
    starts, ends, empty, hints = build_graph()
    maximum = len(starts) - 1
    distance = array("i", [-1]) * (maximum + 1)
    frequency = array("i", [0]) * (INPUTS + 1)
    reached = bytearray(maximum + 1)
    reached[empty] = 1
    distance[empty] = 0
    pending = deque([empty])
    while pending:
        node = pending.popleft()
        start, end = starts[node], ends[node]
        if start < 0:
            continue
        for antecedent in hints[start:end]:
            if antecedent <= INPUTS:
                frequency[antecedent] += 1
            if not reached[antecedent]:
                reached[antecedent] = 1
                distance[antecedent] = distance[node] + 1
                pending.append(antecedent)
            elif distance[antecedent] > distance[node] + 1:
                distance[antecedent] = distance[node] + 1

    reached_inputs = [clause_id for clause_id in range(1, INPUTS + 1) if reached[clause_id]]
    if len(reached_inputs) != 2294:
        raise AssertionError("LRAT input support mismatch")
    distance_rank = sorted(reached_inputs, key=lambda clause_id: (distance[clause_id], clause_id))
    frequency_rank = sorted(reached_inputs, key=lambda clause_id: (-frequency[clause_id], clause_id))

    # A strict dominator of the input super-sink must be reachable from every
    # immediate child of the empty clause.  Propagate exact child bitmasks; an
    # empty intersection proves that there are no strict derived dominators,
    # avoiding a costly general dominator computation.
    root_children = list(hints[starts[empty]:ends[empty]])
    masks = [0] * (maximum + 1)
    for bit, child in enumerate(root_children):
        masks[child] |= 1 << bit
    for node in range(empty - 1, INPUTS, -1):
        mask = masks[node]
        if not mask or starts[node] < 0:
            continue
        for antecedent in hints[starts[node]:ends[node]]:
            masks[antecedent] |= mask
    full_mask = (1 << len(root_children)) - 1
    common = [node for node in range(INPUTS + 1, empty) if masks[node] == full_mask]
    dominator_candidates = 0
    if common:
        raise RuntimeError("common-reachable nodes require full dominator continuation")

    _, source_rows = clauses(SOURCE)
    normalized = normalize(source_rows, sample_bases()[7])
    if not discriminating(normalized[PROTECTED_ID - 1]):
        raise AssertionError("protected input is not discriminating")
    records = []
    seen = set()
    for family, ranking in (("distance", distance_rank), ("frequency", frequency_rank)):
        for size in (128, 256, 500):
            ids = candidate_ids(ranking, size)
            selected = [source_rows[clause_id - 1] for clause_id in ids]
            digest = hashlib.sha256("\n".join(",".join(map(str, sorted(row))) for row in selected).encode()).hexdigest()
            if digest in seen:
                continue
            seen.add(digest)
            path = CANDIDATES / f"{family}-{size}.cnf"
            write_cnf(path, selected)
            discriminating_count = sum(discriminating(normalized[clause_id - 1]) for clause_id in ids)
            records.append((family, size, len(ids), discriminating_count, digest, path.name))
    lines = ["family\tparameter\tclauses\tdiscriminating_clauses\tselection_sha256\tcnf"]
    lines.extend("\t".join(map(str, row)) for row in records)
    (OUT / "candidates.tsv").write_text("\n".join(lines) + "\n")
    summary = f"empty_id={empty} reached_inputs={len(reached_inputs)} root_children={len(root_children)} common_reachable_derived={len(common)} dominator_candidates={dominator_candidates} emitted_candidates={len(records)}"
    (OUT / "analysis.result").write_text(summary + "\n")
    print(summary)


@dataclass(frozen=True)
class Result:
    family: str
    parameter: int
    status: str
    clauses: int
    discriminating_clauses: int
    cnf_sha256: str
    proof_sha256: str
    seconds: float
    detail: str


def read_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"), strict=True)) for line in lines[1:]]


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


def solve_one(row: dict[str, str], cpu: int, deadline: float) -> Result:
    started = time.monotonic()
    family, parameter = row["family"], int(row["parameter"])
    cnf = CANDIDATES / row["cnf"]
    PROOFS.mkdir(parents=True, exist_ok=True)
    proof = PROOFS / f"{family}-{parameter}.drat"
    try:
        remaining = max(1, min(300, int(deadline - time.monotonic())))
        solved = run_checked([str(CADICAL), "-t", str(remaining), str(cnf), str(proof)], cpu, remaining + 10)
        if solved.returncode == 10:
            _, candidate = clauses(cnf)
            literals = [int(token) for line in solved.stdout.splitlines() if line.startswith("v ") for token in line.split()[1:] if token != "0"]
            model = {abs(literal): literal > 0 for literal in literals}
            if any(not any(abs(literal) in model and model[abs(literal)] == (literal > 0) for literal in clause) for clause in candidate):
                raise AssertionError("SAT model fails candidate CNF")
            MODELS.mkdir(parents=True, exist_ok=True)
            model_path = MODELS / f"{family}-{parameter}.model"
            model_path.write_text(" ".join(map(str, sorted(literals, key=abs))) + " 0\n")
            return Result(family, parameter, "SAT", len(candidate), int(row["discriminating_clauses"]), sha256(cnf), sha256(model_path), time.monotonic() - started, "model preserved and directly checked")
        if solved.returncode == 0:
            return Result(family, parameter, "CAP", int(row["clauses"]), int(row["discriminating_clauses"]), sha256(cnf), sha256(proof) if proof.exists() else "-", time.monotonic() - started, "solver timeout")
        if solved.returncode != 20:
            raise RuntimeError(f"solver exit {solved.returncode}")
        checked = run_checked([str(DRAT), str(cnf), str(proof)], cpu, max(1, min(300, int(deadline - time.monotonic()))))
        if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            raise RuntimeError("proof rejected")
        return Result(family, parameter, "CERTIFIED_UNSAT", int(row["clauses"]), int(row["discriminating_clauses"]), sha256(cnf), sha256(proof), time.monotonic() - started, "fresh DRAT VERIFIED")
    except subprocess.TimeoutExpired:
        return Result(family, parameter, "CAP", int(row["clauses"]), int(row["discriminating_clauses"]), sha256(cnf), sha256(proof) if proof.exists() else "-", time.monotonic() - started, "wrapper timeout")
    except Exception as error:
        return Result(family, parameter, "ERROR", int(row["clauses"]), int(row["discriminating_clauses"]), sha256(cnf), sha256(proof) if proof.exists() else "-", time.monotonic() - started, str(error))


def solve() -> None:
    rows = read_table(OUT / "candidates.tsv")
    deadline = time.monotonic() + 3000
    pending: multiprocessing.Queue = multiprocessing.Queue()
    for row in rows:
        pending.put(row)
    output: multiprocessing.Queue = multiprocessing.Queue()

    def worker(cpu: int) -> None:
        while time.monotonic() < deadline:
            try:
                row = pending.get_nowait()
            except queue.Empty:
                return
            output.put(solve_one(row, cpu, deadline))

    processes = [multiprocessing.Process(target=worker, args=(cpu,)) for cpu in CPUS]
    for process in processes:
        process.start()
    for process in processes:
        process.join()
    results = [output.get(timeout=5) for _ in rows]
    results.sort(key=lambda row: ({"distance": 0, "frequency": 1, "dominator": 2}[row.family], row.parameter))
    lines = ["family\tparameter\tstatus\tclauses\tdiscriminating_clauses\tcnf_sha256\tevidence_sha256\tseconds\tdetail"]
    lines.extend("\t".join(map(str, (row.family, row.parameter, row.status, row.clauses, row.discriminating_clauses, row.cnf_sha256, row.proof_sha256, f"{row.seconds:.6f}", row.detail))) for row in results)
    (OUT / "results.tsv").write_text("\n".join(lines) + "\n")
    statuses = Counter(row.status for row in results)
    summary = " ".join(f"{key.lower()}={statuses[key]}" for key in ("CERTIFIED_UNSAT", "SAT", "CAP", "ERROR"))
    (OUT / "solve.result").write_text(summary + "\n")
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["analyze", "solve"])
    args = parser.parse_args()
    if args.command == "analyze":
        analyze()
    else:
        solve()


if __name__ == "__main__":
    main()
