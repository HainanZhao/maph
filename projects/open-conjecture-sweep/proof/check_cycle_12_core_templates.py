#!/usr/bin/env python3
"""Read-only structural and optional full replay for Cycle 12."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import subprocess
import sys
import tempfile
import time


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import (
    CADICAL, CORES, CORE_PROOFS, DRAT, MUS, RUN11, clauses, embed,
    external_bases, full_formula, normalize, sample_bases, sha256, write_rows,
)


def table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"), strict=True)) for line in lines[1:]]


def check_deletion_models(core: list[frozenset[int]]) -> None:
    with tempfile.TemporaryDirectory(prefix="cycle12-mus-") as directory:
        candidate_path = Path(directory) / "candidate.cnf"
        for omitted in range(len(core)):
            candidate = core[:omitted] + core[omitted + 1:]
            write_rows(candidate_path, candidate)
            solved = subprocess.run([str(CADICAL), "-q", str(candidate_path)], capture_output=True, text=True, check=False)
            if solved.returncode != 10:
                raise AssertionError(f"single deletion {omitted} is not SAT")
            literals = [int(token) for line in solved.stdout.splitlines() if line.startswith("v ") for token in line.split()[1:] if token != "0"]
            model = {abs(literal): literal > 0 for literal in literals}
            if any(not any(abs(literal) in model and model[abs(literal)] == (literal > 0) for literal in clause) for clause in candidate):
                raise AssertionError(f"single deletion {omitted} model fails CNF")


def structural() -> None:
    core_rows = table(ROOT / "discovery/out/cycle12-core-template/cores.tsv")
    if len(core_rows) != 100 or any(row["status"] != "CERTIFIED" for row in core_rows):
        raise AssertionError("core table certification mismatch")
    bases = sample_bases()
    for row in core_rows:
        index = int(row["index"])
        _, source = clauses(RUN11 / f"{index:03d}.cnf")
        _, core = clauses(CORES / f"{index:03d}.cnf")
        if Counter(core) - Counter(source):
            raise AssertionError("core is not a source multiset subset")
        if sha256(CORES / f"{index:03d}.cnf") != row["core_sha256"]:
            raise AssertionError("core hash mismatch")
        if sha256(CORE_PROOFS / f"{index:03d}.drat") != row["proof_sha256"]:
            raise AssertionError("core proof hash mismatch")
        result = embed(normalize(core, bases[index]), full_formula(bases[index]), time.monotonic() + 60)
        if result.status != "MATCH":
            raise AssertionError("source self-embedding failed")
    scores = table(ROOT / "discovery/out/cycle12-core-template/validation-scores.tsv")
    if len(scores) != 80 or any(int(row["validation_matches"]) != 0 for row in scores):
        raise AssertionError("whole-core validation result mismatch")
    selected = min(scores, key=lambda row: (-int(row["validation_matches"]), int(row["core_clauses"]), row["core_sha256"]))
    if int(selected["template"]) != 76 or int(selected["core_clauses"]) != 302:
        raise AssertionError("frozen template selection mismatch")
    external = table(ROOT / "discovery/out/cycle12-core-template/external-results.tsv")
    if len(external) != 100 or any(row["status"] != "NO_MATCH" for row in external):
        raise AssertionError("whole-core external result mismatch")
    deletions = table(MUS / "deletions.tsv")
    if len(deletions) != 302 or Counter(row["status"] for row in deletions) != Counter({"RETAIN_SAT": 293, "DELETE_CERTIFIED": 9}):
        raise AssertionError("deletion audit mismatch")
    _, original = clauses(CORES / "076.cnf")
    _, shrunk = clauses(MUS / "076.cnf")
    if len(original) != 302 or len(shrunk) != 293 or Counter(shrunk) - Counter(original):
        raise AssertionError("shrunk core containment mismatch")
    check_deletion_models(shrunk)
    checked = subprocess.run([str(DRAT), str(MUS / "076.cnf"), str(MUS / "076.drat")], capture_output=True, text=True, check=False)
    if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
        raise AssertionError("shrunk core proof rejected")
    validation = table(MUS / "validation.tsv")
    shrunk_external = table(MUS / "external.tsv")
    if len(validation) != 20 or any(row["status"] != "NO_MATCH" for row in validation):
        raise AssertionError("shrunk validation mismatch")
    if len(shrunk_external) != 100 or any(row["status"] != "NO_MATCH" for row in shrunk_external):
        raise AssertionError("shrunk external mismatch")


def replay_embeddings() -> None:
    bases = sample_bases()
    validation_indices = [index for index in range(100) if index % 10 >= 8]
    validation = {index: full_formula(bases[index]) for index in validation_indices}
    for template in [index for index in range(100) if index % 10 < 8]:
        _, raw = clauses(CORES / f"{template:03d}.cnf")
        core = normalize(raw, bases[template])
        for target in validation_indices:
            if embed(core, validation[target], time.monotonic() + 120).status != "NO_MATCH":
                raise AssertionError("whole-core no-match replay failed")
    _, raw = clauses(MUS / "076.cnf")
    core = normalize(raw, bases[76])
    for target in validation_indices:
        if embed(core, validation[target], time.monotonic() + 120).status != "NO_MATCH":
            raise AssertionError("shrunk validation replay failed")
    for base in external_bases():
        if embed(core, full_formula(base), time.monotonic() + 120).status != "NO_MATCH":
            raise AssertionError("shrunk external replay failed")


def replay_proofs() -> None:
    for index in range(100):
        checked = subprocess.run([str(DRAT), str(CORES / f"{index:03d}.cnf"), str(CORE_PROOFS / f"{index:03d}.drat")], capture_output=True, text=True, check=False)
        if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            raise AssertionError(f"core proof {index} rejected")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--embeddings", action="store_true")
    parser.add_argument("--proofs", action="store_true")
    args = parser.parse_args()
    started = time.monotonic()
    structural()
    if args.embeddings:
        replay_embeddings()
    if args.proofs:
        replay_proofs()
    print(f"PASS cores=100 self_embeddings=100 whole_validation_no_match=1600 shrunk_validation_no_match=20 shrunk_external_no_match=100 embeddings_replayed={int(args.embeddings)} proofs_replayed={100 if args.proofs else 0} wall_seconds={time.monotonic()-started:.6f}")


if __name__ == "__main__":
    main()
