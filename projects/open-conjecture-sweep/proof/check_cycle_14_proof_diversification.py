#!/usr/bin/env python3
"""Read-only structural and selected-proof audit for Cycle 14."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import CORES, DRAT, RUN11, clauses, normalize, sample_bases, sha256
from lrc_proof_diversification import ALT_CORES, ALT_CORE_PROOFS, OUT, discriminating


def table(path: Path) -> list[dict[str, str]]:
    lines = path.read_text().splitlines()
    header = lines[0].split("\t")
    return [dict(zip(header, line.split("\t"), strict=True)) for line in lines[1:]]


def audit(check_proof: bool = True) -> dict[str, int]:
    bases = sample_bases()
    census = table(OUT / "census.tsv")
    if len(census) != 80:
        raise AssertionError("census size mismatch")
    recomputed = []
    for row in census:
        index = int(row["index"])
        path = CORES / f"{index:03d}.cnf"
        _, raw = clauses(path)
        core = normalize(raw, bases[index])
        count = sum(discriminating(clause) for clause in core)
        if count != int(row["discriminating_clauses"]) or sha256(path) != row["core_sha256"]:
            raise AssertionError("census row mismatch")
        recomputed.append((-count, len(core), sha256(path), index))
    recomputed.sort()
    if [row[3] for row in recomputed[:3]] != [7, 4, 3]:
        raise AssertionError("base selection mismatch")

    diversified = table(OUT / "diversified.tsv")
    statuses = Counter(row["status"] for row in diversified)
    if len(diversified) != 27 or statuses != Counter({"CERTIFIED": 16, "CAP": 11}):
        raise AssertionError("diversified status mismatch")
    candidates = []
    for index in (7, 4, 3):
        path = CORES / f"{index:03d}.cnf"
        _, raw = clauses(path)
        count = sum(discriminating(clause) for clause in normalize(raw, bases[index]))
        candidates.append((len(raw), -count, sha256(path), index, "existing", "default", path))
    for row in diversified:
        if row["status"] != "CERTIFIED":
            continue
        index = int(row["index"])
        path = ALT_CORES / f"{index:03d}/{row['config']}/{row['mode']}.cnf"
        proof = ALT_CORE_PROOFS / f"{index:03d}/{row['config']}/{row['mode']}.drat"
        _, raw = clauses(path)
        _, source = clauses(RUN11 / f"{index:03d}.cnf")
        if Counter(raw) - Counter(source):
            raise AssertionError("diversified core is not source subset")
        count = sum(discriminating(clause) for clause in normalize(raw, bases[index]))
        if len(raw) != int(row["clauses"]) or count != int(row["discriminating_clauses"]):
            raise AssertionError("diversified classification mismatch")
        if sha256(path) != row["core_sha256"] or sha256(proof) != row["proof_sha256"]:
            raise AssertionError("diversified hash mismatch")
        candidates.append((len(raw), -count, sha256(path), index, row["config"], row["mode"], path))
    selected = min(candidates)
    if selected[0:6] != (2329, -1180, "f7b635e24d15054e13cbd302c746eb72f996ad6d5508483da3679756e9917c33", 7, "noelimprobe", "default"):
        raise AssertionError("candidate selection mismatch")

    deletions = table(OUT / "shrunk/deletions.tsv")
    deletion_statuses = Counter(row["status"] for row in deletions)
    if len(deletions) != 2329 or deletion_statuses != Counter({"RETAIN_CAP": 2328, "RETAIN_PROTECTED": 1}):
        raise AssertionError("shrink outcome mismatch")
    _, source = clauses(selected[6])
    _, final = clauses(OUT / "shrunk/007.cnf")
    if Counter(source) != Counter(final):
        raise AssertionError("zero-deletion final core changed")
    if sum(discriminating(clause) for clause in normalize(final, bases[7])) != 1180:
        raise AssertionError("final discriminating count mismatch")
    groups = table(OUT / "role-groups/groups.tsv")
    if [row["group"] for row in groups] != ["discriminating_coverage", "invariant_positive_x", "choice_pairs", "remaining"]:
        raise AssertionError("role-group order mismatch")
    if any(row["status"] != "RETAIN_SAT" or int(row["remaining_clauses"]) != 2329 for row in groups):
        raise AssertionError("role-group outcome mismatch")
    _, grouped_final = clauses(OUT / "role-groups/007.cnf")
    if Counter(grouped_final) != Counter(source):
        raise AssertionError("role-group final core mismatch")
    if sha256(OUT / "role-groups/007.drat") != "958a383fc710c9c1f1fb8649fe266987cdb7d23179ba61fb370b1d6fa01faafc":
        raise AssertionError("role-group final proof hash mismatch")
    if check_proof:
        checked = subprocess.run([str(DRAT), str(OUT / "shrunk/007.cnf"), str(OUT / "shrunk/007.drat")], capture_output=True, text=True, check=False, timeout=120)
        if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            raise AssertionError("final core proof rejected")
    return {"census": 80, "certified": 16, "caps": 11, "role_groups_retained": 4, "final_clauses": 2329, "final_discriminating": 1180}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--structure-only", action="store_true")
    args = parser.parse_args()
    result = audit(not args.structure_only)
    print("PASS " + " ".join(f"{key}={value}" for key, value in result.items()))
