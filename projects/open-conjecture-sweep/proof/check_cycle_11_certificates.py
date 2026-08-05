#!/usr/bin/env python3
"""Independent structural and DRAT replay for Cycle 11."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import math
import os
from pathlib import Path
import queue
import signal
import subprocess
import threading
import time


ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "discovery/out/cycle11-certified-sat"
CHECKER = ROOT / "discovery/out/cycle11-tools/drat-trim-2e5e29cb0019d5cfd547d4208dca1b3ec290349f/drat-trim"
CPUS = (0, 1, 2)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def factors(c: int) -> tuple[int, ...]:
    return tuple(prime for prime in range(2, c + 1) if c % prime == 0 and all(prime % d for d in range(2, math.isqrt(prime) + 1)))


def bad(k: int, q: int, speed: int, point: int) -> bool:
    residue = speed * point % q
    return (k + 1) * min(residue, q - residue) < q


def direct(base: tuple[int, ...], p: int, c: int, digits: tuple[int, ...]) -> bool:
    speeds = tuple(value + p * digit for value, digit in zip(base, digits, strict=True))
    k = len(speeds)
    for omitted in range(k):
        common = c
        for index, speed in enumerate(speeds):
            if index != omitted:
                common = math.gcd(common, speed)
        if common != 1:
            return False
    return all(any(bad(k, p * c, speed, point) for speed in speeds) for point in range(p * c))


def base_cover(base: tuple[int, ...], p: int) -> bool:
    return all(any(bad(len(base), p, speed, point) for speed in base) for point in range(p))


def expected_clauses(base: tuple[int, ...], p: int, c: int) -> tuple[int, list[tuple[int, ...]]]:
    k = len(base)
    primes = factors(c)
    x_count = k * c
    x = lambda i, d: 1 + i * c + d
    y = lambda r_index, i: x_count + 1 + r_index * k + i
    clauses: list[tuple[int, ...]] = []
    for i in range(k):
        row = tuple(x(i, d) for d in range(c))
        clauses.append(row)
        for left in range(c):
            for right in range(left + 1, c):
                clauses.append((-x(i, left), -x(i, right)))
    for point in range(p * c):
        clauses.append(tuple(x(i, d) for i in range(k) for d in range(c) if bad(k, p * c, base[i] + p * d, point)))
    for r_index, prime in enumerate(primes):
        for i in range(k):
            selected = tuple(x(i, d) for d in range(c) if (base[i] + p * d) % prime == 0)
            for literal in selected:
                clauses.append((-literal, y(r_index, i)))
            clauses.append((-y(r_index, i), *selected))
        for omitted in range(k):
            clauses.append(tuple(-y(r_index, i) for i in range(k) if i != omitted))
    return x_count + len(primes) * k, clauses


def parse_cnf(path: Path) -> tuple[int, list[tuple[int, ...]]]:
    lines = [line for line in path.read_text().splitlines() if line and not line.startswith("c ")]
    header = lines[0].split()
    if len(header) != 4 or header[:2] != ["p", "cnf"]:
        raise AssertionError(f"bad DIMACS header: {path}")
    variables, count = map(int, header[2:])
    clauses: list[tuple[int, ...]] = []
    for line in lines[1:]:
        values = tuple(map(int, line.split()))
        if not values or values[-1] != 0 or 0 in values[:-1]:
            raise AssertionError(f"bad DIMACS clause: {path}")
        clauses.append(values[:-1])
    if len(clauses) != count:
        raise AssertionError(f"DIMACS clause count mismatch: {path}")
    return variables, clauses


def read_table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"), strict=True)) for line in lines[1:]]


def bases() -> dict[str, list[tuple[int, ...]]]:
    h11 = [base for base in itertools.product(range(1, 11), repeat=3) if base_cover(base, 11)]
    p47 = [tuple(map(int, line.split())) for line in (ROOT / "discovery/out/partitioned-k6.txt").read_text().splitlines()]
    p199 = [tuple(map(int, line.split())) for line in (ROOT / "discovery/out/cycle8-p199-strata.txt").read_text().splitlines()]
    if tuple(map(len, (h11, p47, p199))) != (240, 53, 100):
        raise AssertionError("base census mismatch")
    return {"h11": h11, "p47": p47, "p199": p199}


def parameters(family: str) -> tuple[int, int]:
    return {"h11": (11, 4), "p47": (47, 7), "p199": (199, 14)}[family]


def structural_check() -> list[tuple[Path, Path]]:
    by_family = bases()
    controls = read_table(RUN / "controls.tsv")
    frontier = read_table(RUN / "p199.tsv")
    if len(controls) != 293 or len(frontier) != 100:
        raise AssertionError("result table length mismatch")
    if any(row["status"] != "UNSAT" or row["detail"] != "drat-trim VERIFIED" for row in controls):
        raise AssertionError("control certificate status mismatch")
    if {int(row["index"]) for row in frontier if row["status"] == "CAP"} != {0, 2}:
        raise AssertionError("frontier initial CAP set mismatch")
    if any(row["status"] not in {"UNSAT", "CAP"} for row in frontier):
        raise AssertionError("unexpected frontier status")
    for index in (0, 2):
        text = (RUN / f"p199/{index:03d}.recheck.txt").read_text()
        if "VERIFIED" not in text:
            raise AssertionError("extended proof check missing")
    jobs: list[tuple[Path, Path]] = []
    for row in controls + frontier:
        family = row["family"]
        index = int(row["index"])
        base = by_family[family][index]
        p, c = parameters(family)
        if not base_cover(base, p):
            raise AssertionError("frozen base is not l=1 improper")
        cnf = RUN / f"{family}/{index:03d}.cnf"
        proof = RUN / f"{family}/{index:03d}.drat"
        if sha256(cnf) != row["cnf_sha256"] or sha256(proof) != row["proof_sha256"]:
            raise AssertionError("recorded proof-instance hash mismatch")
        actual_variables, actual_clauses = parse_cnf(cnf)
        expected_variables, clauses = expected_clauses(base, p, c)
        if actual_variables != expected_variables or Counter(actual_clauses) != Counter(clauses):
            raise AssertionError("independent CNF reconstruction mismatch")
        jobs.append((cnf, proof))
    for index, base in enumerate(by_family["h11"]):
        variables, clauses = expected_clauses(base, 11, 4)
        del variables
        for digits in itertools.product(range(4), repeat=3):
            model: dict[int, bool] = {}
            for i in range(3):
                for digit in range(4):
                    model[1 + i * 4 + digit] = digit == digits[i]
            for i in range(3):
                model[13 + i] = (base[i] + 11 * digits[i]) % 2 == 0
            cnf_value = all(any(model[abs(literal)] == (literal > 0) for literal in clause) for clause in clauses)
            if cnf_value != direct(base, 11, 4, digits):
                raise AssertionError(f"H11 truth-table mismatch at {index}, {digits}")
    return jobs


def check_proof(cpu: int, cnf: Path, proof: Path) -> None:
    command = [
        "taskset", "-c", str(cpu), "prlimit", "--as=5368709120", "--",
        str(CHECKER), str(cnf), str(proof),
    ]
    process = subprocess.Popen(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, start_new_session=True)
    try:
        stdout, stderr = process.communicate(timeout=1200)
    except subprocess.TimeoutExpired:
        os.killpg(process.pid, signal.SIGTERM)
        process.wait(timeout=5)
        raise AssertionError(f"proof replay timeout: {proof}")
    if process.returncode != 0 or "VERIFIED" not in stdout + stderr:
        raise AssertionError(f"proof replay rejected: {proof}")


def proof_replay(jobs: list[tuple[Path, Path]]) -> None:
    queues = [queue.Queue() for _ in CPUS]
    for index, job in enumerate(jobs):
        queues[index % len(CPUS)].put(job)
    errors: list[BaseException] = []
    lock = threading.Lock()

    def worker(cpu: int, pending: queue.Queue[tuple[Path, Path]]) -> None:
        try:
            while True:
                try:
                    cnf, proof = pending.get_nowait()
                except queue.Empty:
                    return
                check_proof(cpu, cnf, proof)
        except BaseException as error:
            with lock:
                errors.append(error)

    threads = [threading.Thread(target=worker, args=(cpu, pending)) for cpu, pending in zip(CPUS, queues, strict=True)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    if errors:
        raise errors[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proofs", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    jobs = structural_check()
    if args.proofs:
        proof_replay(jobs)
    print(f"PASS structure=393 h11_truth_rows={240 * 4**3} proofs={len(jobs) if args.proofs else 0} wall_seconds={time.monotonic()-started:.6f}")


if __name__ == "__main__":
    main()
