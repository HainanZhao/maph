#!/usr/bin/env python3
"""Cycle 14 targeted proof/core diversification."""

from __future__ import annotations

import argparse
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import (
    C, K, CADICAL, CORES, DRAT, RUN11, clauses, coordinate, normalize,
    run_checked, sample_bases, sha256,
)

OUT = ROOT / "discovery/out/cycle14-proof-diversification"
TRACES = OUT / "traces"
ALT_CORES = OUT / "cores"
ALT_CORE_PROOFS = OUT / "core-proofs"
CPUS = (0, 1, 2)
CONFIGS = (
    ("default", ("--seed=0",)),
    ("plain", ("--plain", "--seed=1")),
    ("noelimprobe", ("--elim=false", "--probe=false", "--seed=2")),
)
MODES = (("default", ()), ("unit", ("-u",)), ("forward", ("-f",)))


def variable_type(literal: int) -> str:
    variable = abs(literal)
    return "x" if variable <= K * C else ("y2" if variable <= K * C + K else "y7")


def residue(literal: int) -> int:
    return (abs(literal) - 1) % C


def color(value: int) -> tuple[bool, bool]:
    return value % 2 == 0, value % 7 == 0


COLORS = tuple(sorted({color(value) for value in range(C)}))


def discriminating(clause: frozenset[int]) -> bool:
    if not clause or any(literal < 0 or variable_type(literal) != "x" for literal in clause):
        return False
    by_coordinate: dict[int, set[int]] = {}
    for literal in clause:
        by_coordinate.setdefault(coordinate(literal), set()).add(residue(literal))
    for values in by_coordinate.values():
        for divisor_color in COLORS:
            color_class = {value for value in range(C) if color(value) == divisor_color}
            if values & color_class and not color_class <= values:
                return True
    return False


def census() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    bases = sample_bases()
    rows = []
    for index in range(100):
        if index % 10 >= 8:
            continue
        path = CORES / f"{index:03d}.cnf"
        _, raw = clauses(path)
        core = normalize(raw, bases[index])
        coverage = [clause for clause in core if clause and all(literal > 0 and variable_type(literal) == "x" for literal in clause)]
        split = [clause for clause in coverage if discriminating(clause)]
        rows.append((index, len(core), len(coverage), len(split), sha256(path)))
    rows.sort(key=lambda row: (-row[3], row[1], row[4], row[0]))
    lines = ["rank\tindex\tclauses\tpositive_x_clauses\tdiscriminating_clauses\tcore_sha256"]
    lines.extend("\t".join(map(str, (rank, *row))) for rank, row in enumerate(rows))
    (OUT / "census.tsv").write_text("\n".join(lines) + "\n")
    selected = rows[:3]
    summary = "selected=" + ",".join(str(row[0]) for row in selected) + " discriminating=" + ",".join(str(row[3]) for row in selected)
    (OUT / "census.result").write_text(summary + "\n")
    print(summary)


@dataclass(frozen=True)
class Diversified:
    index: int
    config: str
    mode: str
    status: str
    clauses: int
    discriminating_clauses: int
    core_sha256: str
    proof_sha256: str
    seconds: float
    detail: str


def selected_indices() -> list[int]:
    lines = (OUT / "census.tsv").read_text().splitlines()[1:4]
    result = [int(line.split("\t")[1]) for line in lines]
    if result != [7, 4, 3]:
        raise AssertionError("frozen census selection mismatch")
    return result


def diversify_one(index: int, config: str, options: tuple[str, ...], cpu: int, deadline: float) -> list[Diversified]:
    started = time.monotonic()
    cnf = RUN11 / f"{index:03d}.cnf"
    trace_dir = TRACES / f"{index:03d}"
    trace_dir.mkdir(parents=True, exist_ok=True)
    proof = trace_dir / f"{config}.drat"
    remaining = max(1, min(600, int(deadline - time.monotonic())))
    try:
        solved = run_checked([str(CADICAL), *options, "-q", "-t", str(remaining), str(cnf), str(proof)], cpu, remaining + 10)
    except Exception as error:
        return [Diversified(index, config, mode, "CAP", 0, 0, "-", "-", time.monotonic() - started, type(error).__name__) for mode, _ in MODES]
    if solved.returncode != 20:
        status = "CAP" if solved.returncode == 0 else "ERROR"
        return [Diversified(index, config, mode, status, 0, 0, "-", sha256(proof) if proof.exists() else "-", time.monotonic() - started, f"solver exit {solved.returncode}") for mode, _ in MODES]
    verified = run_checked([str(DRAT), str(cnf), str(proof)], cpu, max(1, min(600, int(deadline - time.monotonic()))))
    if verified.returncode != 0 or "VERIFIED" not in verified.stdout + verified.stderr:
        return [Diversified(index, config, mode, "ERROR", 0, 0, "-", sha256(proof), time.monotonic() - started, "source proof rejected") for mode, _ in MODES]
    results = []
    bases = sample_bases()
    for mode, mode_options in MODES:
        mode_started = time.monotonic()
        directory = ALT_CORES / f"{index:03d}/{config}"
        proof_directory = ALT_CORE_PROOFS / f"{index:03d}/{config}"
        directory.mkdir(parents=True, exist_ok=True)
        proof_directory.mkdir(parents=True, exist_ok=True)
        core = directory / f"{mode}.cnf"
        core_proof = proof_directory / f"{mode}.drat"
        try:
            extracted = run_checked([str(DRAT), str(cnf), str(proof), *mode_options, "-c", str(core)], cpu, max(1, min(600, int(deadline - time.monotonic()))))
            if extracted.returncode != 0 or "VERIFIED" not in extracted.stdout + extracted.stderr:
                raise RuntimeError("core extraction rejected")
            _, source_rows = clauses(cnf)
            _, core_rows = clauses(core)
            if Counter(core_rows) - Counter(source_rows):
                raise RuntimeError("core is not source subset")
            solved_core = run_checked([str(CADICAL), "-q", "-t", "300", str(core), str(core_proof)], cpu, max(1, min(310, int(deadline - time.monotonic()))))
            if solved_core.returncode != 20:
                raise RuntimeError(f"core solver exit {solved_core.returncode}")
            checked_core = run_checked([str(DRAT), str(core), str(core_proof)], cpu, max(1, min(300, int(deadline - time.monotonic()))))
            if checked_core.returncode != 0 or "VERIFIED" not in checked_core.stdout + checked_core.stderr:
                raise RuntimeError("core proof rejected")
            normalized = normalize(core_rows, bases[index])
            count = sum(discriminating(clause) for clause in normalized)
            results.append(Diversified(index, config, mode, "CERTIFIED", len(core_rows), count, sha256(core), sha256(core_proof), time.monotonic() - mode_started, "source subset and fresh DRAT VERIFIED"))
        except Exception as error:
            capped = isinstance(error, subprocess.TimeoutExpired) or time.monotonic() >= deadline
            results.append(Diversified(index, config, mode, "CAP" if capped else "ERROR", 0, 0, sha256(core) if core.exists() else "-", sha256(core_proof) if core_proof.exists() else "-", time.monotonic() - mode_started, str(error)))
    return results


def diversify() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    deadline = time.monotonic() + 2400
    pending: queue.Queue[tuple[int, str, tuple[str, ...]]] = queue.Queue()
    for index in selected_indices():
        for config, options in CONFIGS:
            pending.put((index, config, options))
    results: list[Diversified] = []
    lock = threading.Lock()

    def worker(cpu: int) -> None:
        while time.monotonic() < deadline:
            try:
                index, config, options = pending.get_nowait()
            except queue.Empty:
                return
            rows = diversify_one(index, config, options, cpu, deadline)
            with lock:
                results.extend(rows)

    workers = [threading.Thread(target=worker, args=(cpu,)) for cpu in CPUS]
    for worker in workers:
        worker.start()
    for worker in workers:
        worker.join()
    while not pending.empty():
        index, config, _ = pending.get_nowait()
        results.extend(Diversified(index, config, mode, "CAP", 0, 0, "-", "-", 0.0, "aggregate cap") for mode, _ in MODES)
    results.sort(key=lambda row: (row.index, row.config, row.mode))
    lines = ["index\tconfig\tmode\tstatus\tclauses\tdiscriminating_clauses\tcore_sha256\tproof_sha256\tseconds\tdetail"]
    lines.extend("\t".join(map(str, (row.index, row.config, row.mode, row.status, row.clauses, row.discriminating_clauses, row.core_sha256, row.proof_sha256, f"{row.seconds:.6f}", row.detail))) for row in results)
    (OUT / "diversified.tsv").write_text("\n".join(lines) + "\n")
    summary = f"certified={sum(row.status == 'CERTIFIED' for row in results)} cap={sum(row.status == 'CAP' for row in results)} error={sum(row.status == 'ERROR' for row in results)}"
    (OUT / "diversified.result").write_text(summary + "\n")
    print(summary)


def reclassify() -> None:
    path = OUT / "diversified.tsv"
    lines = path.read_text().splitlines()
    repaired = [lines[0]]
    for line in lines[1:]:
        fields = line.split("\t")
        if fields[3] == "ERROR" and (fields[9].startswith("solver exit 0") or "timed out after" in fields[9]):
            fields[3] = "CAP"
        repaired.append("\t".join(fields))
    path.write_text("\n".join(repaired) + "\n")
    statuses = Counter(line.split("\t")[3] for line in repaired[1:])
    summary = f"certified={statuses['CERTIFIED']} cap={statuses['CAP']} error={statuses['ERROR']}"
    (OUT / "diversified.result").write_text(summary + "\n")
    print(summary)


def write_cnf(path: Path, rows: list[frozenset[int]]) -> None:
    lines = [f"p cnf {K * C + 2 * K} {len(rows)}"]
    lines.extend(" ".join(map(str, sorted(row, key=lambda literal: (abs(literal), literal)))) + " 0" for row in rows)
    path.write_text("\n".join(lines) + "\n")


def shrink() -> None:
    # The frozen candidate ordering over existing plus accepted diversified
    # cores selects base 7 / noelimprobe / default.
    index, config, mode = 7, "noelimprobe", "default"
    source = ALT_CORES / f"{index:03d}/{config}/{mode}.cnf"
    _, raw = clauses(source)
    normalized = normalize(raw, sample_bases()[index])
    candidates = [(tuple(sorted(clause)), position) for position, clause in enumerate(normalized) if discriminating(clause)]
    if len(raw) != 2329 or len(candidates) != 1180:
        raise AssertionError("frozen shrink candidate mismatch")
    protected_normalized, protected_index = min(candidates)
    current = list(enumerate(raw))
    target_dir = OUT / "shrunk"
    target_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = target_dir / "candidate.cnf"
    candidate_proof = target_dir / "candidate.drat"
    deadline = time.monotonic() + 1000
    records = []
    for original_index in range(len(raw)):
        started = time.monotonic()
        if original_index == protected_index:
            records.append((original_index, "RETAIN_PROTECTED", len(current), 0.0))
            continue
        candidate = [entry for entry in current if entry[0] != original_index]
        write_cnf(candidate_path, [clause for _, clause in candidate])
        remaining = int(deadline - time.monotonic())
        if remaining <= 0:
            records.append((original_index, "RETAIN_CAP", len(current), time.monotonic() - started))
            continue
        try:
            solved = run_checked([str(CADICAL), "-q", "-t", str(min(10, remaining)), str(candidate_path), str(candidate_proof)], 0, min(12, remaining))
            if solved.returncode == 10:
                records.append((original_index, "RETAIN_SAT", len(current), time.monotonic() - started))
                continue
            if solved.returncode != 20:
                records.append((original_index, "RETAIN_CAP" if solved.returncode == 0 else "RETAIN_ERROR", len(current), time.monotonic() - started))
                continue
            checked = run_checked([str(DRAT), str(candidate_path), str(candidate_proof)], 0, max(1, min(10, int(deadline - time.monotonic()))))
            if checked.returncode == 0 and "VERIFIED" in checked.stdout + checked.stderr:
                current = candidate
                records.append((original_index, "DELETE_CERTIFIED", len(current), time.monotonic() - started))
            else:
                records.append((original_index, "RETAIN_ERROR", len(current), time.monotonic() - started))
        except subprocess.TimeoutExpired:
            records.append((original_index, "RETAIN_CAP", len(current), time.monotonic() - started))
        if original_index % 100 == 0:
            print(f"shrink position={original_index} remaining={len(current)}", flush=True)
    final_cnf = target_dir / "007.cnf"
    final_proof = target_dir / "007.drat"
    write_cnf(final_cnf, [clause for _, clause in current])
    solved = run_checked([str(CADICAL), "-q", "-t", "120", str(final_cnf), str(final_proof)], 0, 130)
    if solved.returncode != 20:
        raise RuntimeError("final core did not certify UNSAT")
    checked = run_checked([str(DRAT), str(final_cnf), str(final_proof)], 0, 120)
    if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
        raise RuntimeError("final core proof rejected")
    final_normalized = normalize([clause for _, clause in current], sample_bases()[index])
    final_discriminating = sum(discriminating(clause) for clause in final_normalized)
    if tuple(protected_normalized) not in {tuple(sorted(clause)) for clause in final_normalized} or final_discriminating < 1:
        raise AssertionError("protected discriminating clause lost")
    lines = ["original_clause\tstatus\tremaining_clauses\tseconds"]
    lines.extend("\t".join(map(str, (position, status, count, f"{seconds:.6f}"))) for position, status, count, seconds in records)
    (target_dir / "deletions.tsv").write_text("\n".join(lines) + "\n")
    statuses = Counter(status for _, status, _, _ in records)
    summary = f"source_clauses={len(raw)} final_clauses={len(current)} final_discriminating={final_discriminating} protected_original_index={protected_index} certified_deletions={statuses['DELETE_CERTIFIED']} caps={statuses['RETAIN_CAP']} errors={statuses['RETAIN_ERROR']} cnf_sha256={sha256(final_cnf)} proof_sha256={sha256(final_proof)}"
    (target_dir / "shrink.result").write_text(summary + "\n")
    print(summary)


def role_groups() -> None:
    source = ALT_CORES / "007/noelimprobe/default.cnf"
    _, raw = clauses(source)
    normalized = normalize(raw, sample_bases()[7])
    protected = min((tuple(sorted(clause)), position) for position, clause in enumerate(normalized) if discriminating(clause))[1]

    def group_of(position: int, clause: frozenset[int]) -> str:
        if position == protected:
            return "protected"
        if discriminating(clause):
            return "discriminating_coverage"
        if clause and all(literal > 0 and variable_type(literal) == "x" for literal in clause):
            return "invariant_positive_x"
        if len(clause) == 2 and all(literal < 0 and variable_type(literal) == "x" for literal in clause) and len({coordinate(literal) for literal in clause}) == 1:
            return "choice_pairs"
        return "remaining"

    order = ("discriminating_coverage", "invariant_positive_x", "choice_pairs", "remaining")
    current = list(enumerate(raw))
    target_dir = OUT / "role-groups"
    target_dir.mkdir(parents=True, exist_ok=True)
    candidate_path = target_dir / "candidate.cnf"
    candidate_proof = target_dir / "candidate.drat"
    deadline = time.monotonic() + 90
    records = []
    final_cnf = target_dir / "007.cnf"
    final_proof = target_dir / "007.drat"
    accepted = False
    for name in order:
        started = time.monotonic()
        removed = [entry for entry in current if group_of(entry[0], normalized[entry[0]]) == name]
        candidate = [entry for entry in current if group_of(entry[0], normalized[entry[0]]) != name]
        write_cnf(candidate_path, [clause for _, clause in candidate])
        remaining = int(deadline - time.monotonic())
        status = "RETAIN_CAP"
        if remaining > 0:
            try:
                solved = run_checked([str(CADICAL), "-q", "-t", str(min(25, remaining)), str(candidate_path), str(candidate_proof)], 0, min(30, remaining))
                if solved.returncode == 10:
                    status = "RETAIN_SAT"
                elif solved.returncode == 20:
                    checked = run_checked([str(DRAT), str(candidate_path), str(candidate_proof)], 0, max(1, min(20, int(deadline - time.monotonic()))))
                    if checked.returncode == 0 and "VERIFIED" in checked.stdout + checked.stderr:
                        current = candidate
                        shutil.copyfile(candidate_path, final_cnf)
                        shutil.copyfile(candidate_proof, final_proof)
                        accepted = True
                        status = "DELETE_CERTIFIED"
                    else:
                        status = "RETAIN_ERROR"
                elif solved.returncode != 0:
                    status = "RETAIN_ERROR"
            except subprocess.TimeoutExpired:
                status = "RETAIN_CAP"
        records.append((name, len(removed), status, len(current), time.monotonic() - started))
        print(f"group={name} removed={len(removed)} status={status} remaining={len(current)}", flush=True)
    if not accepted:
        shutil.copyfile(source, final_cnf)
        shutil.copyfile(ALT_CORE_PROOFS / "007/noelimprobe/default.drat", final_proof)
    checked = run_checked([str(DRAT), str(final_cnf), str(final_proof)], 0, 30)
    if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
        raise RuntimeError("role-group final proof rejected")
    final_normalized = normalize([clause for _, clause in current], sample_bases()[7])
    count = sum(discriminating(clause) for clause in final_normalized)
    if count < 1:
        raise AssertionError("role-group pass lost all discriminating clauses")
    lines = ["group\tattempted_clauses\tstatus\tremaining_clauses\tseconds"]
    lines.extend("\t".join(map(str, (name, attempted, status, remaining, f"{seconds:.6f}"))) for name, attempted, status, remaining, seconds in records)
    (target_dir / "groups.tsv").write_text("\n".join(lines) + "\n")
    summary = f"final_clauses={len(current)} final_discriminating={count} certified_groups={sum(status == 'DELETE_CERTIFIED' for _, _, status, _, _ in records)} caps={sum(status == 'RETAIN_CAP' for _, _, status, _, _ in records)} cnf_sha256={sha256(final_cnf)} proof_sha256={sha256(final_proof)}"
    (target_dir / "groups.result").write_text(summary + "\n")
    print(summary)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["census", "diversify", "reclassify", "shrink", "role-groups"])
    args = parser.parse_args()
    if args.command == "census":
        census()
    elif args.command == "diversify":
        diversify()
    elif args.command == "reclassify":
        reclassify()
    elif args.command == "shrink":
        shrink()
    elif args.command == "role-groups":
        role_groups()


if __name__ == "__main__":
    main()
