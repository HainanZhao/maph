#!/usr/bin/env python3
"""Cycle 11 exact first-lift CNF generator and certified solver runner."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import hashlib
import itertools
import math
import os
from pathlib import Path
import queue
import shutil
import signal
import subprocess
import threading
import time


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "discovery/out/cycle11-tools"
CADICAL = TOOLS / "cadical-f13d74439a5b5c963ac5b02d05ce93a8098018b8/build/cadical"
DRAT_TRIM = TOOLS / "drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f/drat-trim"
OUTPUT = ROOT / "discovery/out/cycle11-certified-sat"
P47_INPUT = ROOT / "discovery/out/partitioned-k6.txt"
P199_INPUT = ROOT / "discovery/out/cycle8-p199-strata.txt"
CPUS = (0, 1, 2)
PER_INSTANCE_SECONDS = 300
AGGREGATE_SECONDS = 3600
AGGREGATE_DISK_BYTES = 107_374_182_400
PER_PROCESS_FILE_BYTES = 32_212_254_720
PER_PROCESS_MEMORY_BYTES = 5_368_709_120


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prime_factors(value: int) -> tuple[int, ...]:
    factors: list[int] = []
    divisor = 2
    while divisor * divisor <= value:
        if value % divisor == 0:
            factors.append(divisor)
            while value % divisor == 0:
                value //= divisor
        divisor += 1
    if value > 1:
        factors.append(value)
    return tuple(factors)


def is_bad(k: int, q: int, speed: int, point: int) -> bool:
    residue = point * speed % q
    return (k + 1) * min(residue, q - residue) < q


def improper_direct(base: tuple[int, ...], p: int, c: int, digits: tuple[int, ...]) -> bool:
    k = len(base)
    q = p * c
    speeds = tuple(value + p * digit for value, digit in zip(base, digits, strict=True))
    for omitted in range(k):
        divisor = c
        for index, speed in enumerate(speeds):
            if index != omitted:
                divisor = math.gcd(divisor, speed)
        if divisor > 1:
            return False
    return all(any(is_bad(k, q, speed, point) for speed in speeds) for point in range(q))


def base_improper(base: tuple[int, ...], p: int) -> bool:
    k = len(base)
    return all(any(is_bad(k, p, speed, point) for speed in base) for point in range(p))


@dataclass(frozen=True)
class Formula:
    variables: int
    clauses: tuple[tuple[int, ...], ...]
    k: int
    p: int
    c: int

    def x(self, coordinate: int, digit: int) -> int:
        return 1 + coordinate * self.c + digit


def encode(base: tuple[int, ...], p: int, c: int) -> Formula:
    k = len(base)
    q = p * c
    factors = prime_factors(c)
    x_variables = k * c

    def x(coordinate: int, digit: int) -> int:
        return 1 + coordinate * c + digit

    def y(factor_index: int, coordinate: int) -> int:
        return x_variables + 1 + factor_index * k + coordinate

    clauses: list[tuple[int, ...]] = []
    for coordinate in range(k):
        choices = tuple(x(coordinate, digit) for digit in range(c))
        clauses.append(choices)
        clauses.extend((-left, -right) for left, right in itertools.combinations(choices, 2))
    for point in range(q):
        cover = tuple(
            x(coordinate, digit)
            for coordinate in range(k)
            for digit in range(c)
            if is_bad(k, q, base[coordinate] + p * digit, point)
        )
        clauses.append(cover)
    for factor_index, factor in enumerate(factors):
        for coordinate in range(k):
            divisible = tuple(
                x(coordinate, digit)
                for digit in range(c)
                if (base[coordinate] + p * digit) % factor == 0
            )
            if not divisible:
                raise AssertionError("missing divisible digit")
            clauses.extend((-literal, y(factor_index, coordinate)) for literal in divisible)
            clauses.append((-y(factor_index, coordinate), *divisible))
        for selected in itertools.combinations(range(k), k - 1):
            clauses.append(tuple(-y(factor_index, coordinate) for coordinate in selected))
    if any(not clause for clause in clauses):
        raise AssertionError("encoding generated an empty input clause")
    return Formula(x_variables + len(factors) * k, tuple(clauses), k, p, c)


def write_dimacs(formula: Formula, path: Path) -> None:
    lines = [f"p cnf {formula.variables} {len(formula.clauses)}"]
    lines.extend(" ".join(map(str, clause)) + " 0" for clause in formula.clauses)
    path.write_text("\n".join(lines) + "\n")


def parse_model(output: str, variables: int) -> dict[int, bool]:
    literals: list[int] = []
    for line in output.splitlines():
        if line.startswith("v "):
            literals.extend(int(token) for token in line.split()[1:] if token != "0")
    model = {abs(literal): literal > 0 for literal in literals}
    if any(variable not in model for variable in range(1, variables + 1)):
        raise AssertionError("incomplete SAT model")
    return model


def check_model(formula: Formula, base: tuple[int, ...], model: dict[int, bool]) -> tuple[int, ...]:
    for clause in formula.clauses:
        if not any(model[abs(literal)] == (literal > 0) for literal in clause):
            raise AssertionError("SAT model fails emitted CNF clause")
    digits = tuple(
        next(digit for digit in range(formula.c) if model[formula.x(coordinate, digit)])
        for coordinate in range(formula.k)
    )
    if not improper_direct(base, formula.p, formula.c, digits):
        raise AssertionError("SAT model fails direct improper-lift predicate")
    return digits


def directory_bytes(path: Path) -> int:
    return sum(item.stat().st_size for item in path.rglob("*") if item.is_file())


@dataclass(frozen=True)
class Job:
    family: str
    index: int
    base: tuple[int, ...]
    p: int
    c: int


@dataclass(frozen=True)
class Result:
    job: Job
    status: str
    seconds: float
    variables: int
    clauses: int
    cnf_sha256: str
    proof_sha256: str
    digits: tuple[int, ...]
    detail: str


def timed_command(cpu: int, metrics: Path, command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    wrapped = [
        "taskset", "-c", str(cpu), "/usr/bin/time", "-v", "-o", str(metrics),
        "prlimit", f"--as={PER_PROCESS_MEMORY_BYTES}", f"--fsize={PER_PROCESS_FILE_BYTES}", "--",
        *command,
    ]
    process = subprocess.Popen(
        wrapped,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        start_new_session=True,
    )
    try:
        stdout, stderr = process.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        try:
            process.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGKILL)
            process.communicate()
        raise
    return subprocess.CompletedProcess(wrapped, process.returncode, stdout, stderr)


def solve(job: Job, cpu: int, deadline: float) -> Result:
    family_dir = OUTPUT / job.family
    family_dir.mkdir(parents=True, exist_ok=True)
    stem = family_dir / f"{job.index:03d}"
    cnf = stem.with_suffix(".cnf")
    proof = stem.with_suffix(".drat")
    solver_metrics = stem.with_suffix(".solver.time")
    checker_metrics = stem.with_suffix(".checker.time")
    formula = encode(job.base, job.p, job.c)
    write_dimacs(formula, cnf)
    start = time.monotonic()
    remaining = max(0, int(deadline - start))
    if remaining == 0 or directory_bytes(OUTPUT) > AGGREGATE_DISK_BYTES:
        return Result(job, "CAP", 0.0, formula.variables, len(formula.clauses), sha256(cnf), "-", (), "aggregate cap before solve")
    timeout = min(PER_INSTANCE_SECONDS + 10, remaining)
    try:
        process = timed_command(cpu, solver_metrics, [str(CADICAL), "-q", "-t", str(PER_INSTANCE_SECONDS), str(cnf), str(proof)], timeout)
    except subprocess.TimeoutExpired:
        return Result(job, "CAP", time.monotonic() - start, formula.variables, len(formula.clauses), sha256(cnf), "-", (), "solver timeout")
    elapsed = time.monotonic() - start
    if process.returncode == 10:
        digits = check_model(formula, job.base, parse_model(process.stdout, formula.variables))
        return Result(job, "SAT", elapsed, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof) if proof.exists() else "-", digits, "direct model and CNF check passed")
    if process.returncode != 20:
        return Result(job, "CAP", elapsed, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof) if proof.exists() else "-", (), f"solver exit {process.returncode}")
    remaining = max(0, int(deadline - time.monotonic()))
    if remaining == 0 or directory_bytes(OUTPUT) > AGGREGATE_DISK_BYTES:
        return Result(job, "CAP", elapsed, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof), (), "aggregate cap before proof check")
    try:
        checked = timed_command(cpu, checker_metrics, [str(DRAT_TRIM), str(cnf), str(proof)], min(PER_INSTANCE_SECONDS + 10, remaining))
    except subprocess.TimeoutExpired:
        return Result(job, "CAP", time.monotonic() - start, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof), (), "checker timeout")
    checker_text = checked.stdout + checked.stderr
    if checked.returncode != 0 or "VERIFIED" not in checker_text:
        return Result(job, "ERROR", time.monotonic() - start, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof), (), f"DRAT rejected with exit {checked.returncode}")
    return Result(job, "UNSAT", time.monotonic() - start, formula.variables, len(formula.clauses), sha256(cnf), sha256(proof), (), "drat-trim VERIFIED")


def run_jobs(jobs: list[Job], deadline: float) -> list[Result]:
    pending: queue.Queue[Job] = queue.Queue()
    for job in jobs:
        pending.put(job)
    results: list[Result] = []
    lock = threading.Lock()

    def worker(cpu: int) -> None:
        while time.monotonic() < deadline:
            try:
                job = pending.get_nowait()
            except queue.Empty:
                return
            result = solve(job, cpu, deadline)
            with lock:
                results.append(result)
            pending.task_done()

    workers = [threading.Thread(target=worker, args=(cpu,)) for cpu in CPUS]
    for worker_thread in workers:
        worker_thread.start()
    for worker_thread in workers:
        worker_thread.join()
    while not pending.empty():
        job = pending.get_nowait()
        formula = encode(job.base, job.p, job.c)
        results.append(Result(job, "CAP", 0.0, formula.variables, len(formula.clauses), "-", "-", (), "aggregate wall cap"))
    return sorted(results, key=lambda result: result.job.index)


def h11_jobs() -> list[Job]:
    bases = [base for base in itertools.product(range(1, 11), repeat=3) if base_improper(base, 11)]
    if len(bases) != 240:
        raise AssertionError("H11 control census mismatch")
    return [Job("h11", index, base, 11, 4) for index, base in enumerate(bases)]


def file_jobs(family: str, path: Path, expected: int, p: int, c: int, k: int) -> list[Job]:
    bases = [tuple(map(int, line.split())) for line in path.read_text().splitlines() if line.strip()]
    if len(bases) != expected or any(len(base) != k or not base_improper(base, p) for base in bases):
        raise AssertionError(f"{family} frozen input mismatch")
    return [Job(family, index, base, p, c) for index, base in enumerate(bases)]


def write_results(results: list[Result], path: Path) -> None:
    lines = ["family\tindex\tstatus\tseconds\tvariables\tclauses\tcnf_sha256\tproof_sha256\tdigits\tdetail"]
    for result in results:
        lines.append("\t".join([
            result.job.family, str(result.job.index), result.status, f"{result.seconds:.6f}",
            str(result.variables), str(result.clauses), result.cnf_sha256, result.proof_sha256,
            ",".join(map(str, result.digits)) or "-", result.detail,
        ]))
    path.write_text("\n".join(lines) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", choices=("all",), required=True)
    args = parser.parse_args()
    del args
    if not CADICAL.is_file() or not DRAT_TRIM.is_file():
        raise SystemExit("pinned solver/checker missing")
    usage = shutil.disk_usage(OUTPUT.parent)
    if usage.free - 5 * 1024**3 < AGGREGATE_DISK_BYTES:
        raise SystemExit("frozen disk cap no longer leaves the 5 GiB reserve")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic()
    deadline = started + AGGREGATE_SECONDS
    controls = run_jobs(h11_jobs(), deadline)
    controls += run_jobs(file_jobs("p47", P47_INPUT, 53, 47, 7, 6), deadline)
    write_results(controls, OUTPUT / "controls.tsv")
    if len(controls) != 293 or any(result.status != "UNSAT" for result in controls):
        raise SystemExit("control gate failed; p199 not started")
    p199 = run_jobs(file_jobs("p199", P199_INPUT, 100, 199, 14, 13), deadline)
    write_results(p199, OUTPUT / "p199.tsv")
    summary = [
        f"controls_verified_unsat={sum(result.status == 'UNSAT' for result in controls)}",
        *[f"p199_{status.lower()}={sum(result.status == status for result in p199)}" for status in ("SAT", "UNSAT", "CAP", "ERROR")],
        f"wall_seconds={time.monotonic() - started:.6f}",
        f"output_bytes={directory_bytes(OUTPUT)}",
    ]
    (OUTPUT / "summary.txt").write_text("\n".join(summary) + "\n")
    print(" ".join(summary))


if __name__ == "__main__":
    main()
