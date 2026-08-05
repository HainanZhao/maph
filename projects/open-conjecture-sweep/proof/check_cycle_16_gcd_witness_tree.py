#!/usr/bin/env python3
"""Read-only exact audit and optional full proof replay for Cycle 16."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import itertools
import multiprocessing
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import DRAT, clauses, normalize, sample_bases, sha256
from lrc_gcd_witness_tree import CNFS, CORES, CORE_PROOFS, OUT, PROOFS, SOURCE, census_base, leaf_units, pairs, read_table
from lrc_proof_diversification import discriminating


def check_leaf_proof(ordinal: int) -> bool:
    stem = f"{ordinal:04d}"
    result = subprocess.run([str(DRAT), str(CNFS / f"{stem}.cnf"), str(PROOFS / f"{stem}.drat")], capture_output=True, text=True, check=False)
    return result.returncode == 0 and "VERIFIED" in result.stdout + result.stderr


def audit(replay_proofs: bool = False) -> dict[str, int]:
    leaves = read_table(OUT / "leaves.tsv")
    expected_states = list(itertools.product(pairs(), repeat=2))
    if len(leaves) != 6084 or any(row["status"] != "CERTIFIED_UNSAT" for row in leaves):
        raise AssertionError("tree status mismatch")
    _, source = clauses(SOURCE)
    source_lines = [" ".join(map(str, sorted(clause, key=lambda literal: (abs(literal), literal)))) + " 0" for clause in source]
    base = sample_bases()[7]
    for ordinal, (row, (pair2, pair7)) in enumerate(zip(leaves, expected_states, strict=True)):
        if (int(row["ordinal"]), int(row["i"]), int(row["j"]), int(row["u"]), int(row["v"])) != (ordinal, *pair2, *pair7):
            raise AssertionError("leaf identity mismatch")
        units = leaf_units(base, pair2, pair7)
        encoded = ("\n".join([f"p cnf 208 {len(source) + len(units)}", *source_lines, *(f"{unit} 0" for unit in units)]) + "\n").encode()
        if hashlib.sha256(encoded).hexdigest() != row["cnf_sha256"] or sha256(CNFS / f"{ordinal:04d}.cnf") != row["cnf_sha256"]:
            raise AssertionError("leaf encoding/hash mismatch")
        if sha256(PROOFS / f"{ordinal:04d}.drat") != row["proof_sha256"]:
            raise AssertionError("leaf proof hash mismatch")
    if replay_proofs:
        with multiprocessing.Pool(processes=3) as pool:
            if not all(pool.map(check_leaf_proof, range(6084))):
                raise AssertionError("full leaf proof replay failed")

    core_rows = read_table(OUT / "cores.tsv")
    if len(core_rows) != 608 or any(row["status"] != "CERTIFIED" for row in core_rows):
        raise AssertionError("core census mismatch")
    eligible = []
    for row in core_rows:
        ordinal = int(row["ordinal"])
        _, leaf = clauses(CNFS / f"{ordinal:04d}.cnf")
        _, core = clauses(CORES / f"{ordinal:04d}.cnf")
        if Counter(core) - Counter(leaf) or sha256(CORES / f"{ordinal:04d}.cnf") != row["core_sha256"] or sha256(CORE_PROOFS / f"{ordinal:04d}.drat") != row["proof_sha256"]:
            raise AssertionError("core subset/hash mismatch")
        count = sum(discriminating(clause) for clause in normalize(core, base))
        if len(core) != int(row["clauses"]) or count != int(row["discriminating_clauses"]):
            raise AssertionError("core classification mismatch")
        if count:
            eligible.append(row)
    chosen = min(eligible, key=lambda row: (int(row["clauses"]), -int(row["discriminating_clauses"]), (int(row["i"]), int(row["j"]), int(row["u"]), int(row["v"])), row["core_sha256"]))
    if int(chosen["ordinal"]) != 74 or int(chosen["clauses"]) != 27:
        raise AssertionError("selected core mismatch")

    validation = read_table(OUT / "validation/results.tsv")
    if [int(row["target_index"]) for row in validation] != [4, 3] or any(row["status"] != "CERTIFIED_MATCH" for row in validation):
        raise AssertionError("validation result mismatch")
    for row in validation:
        index = int(row["target_index"])
        core_path, proof_path = OUT / f"validation/{index:03d}.cnf", OUT / f"validation/{index:03d}.drat"
        _, core = clauses(core_path)
        positive = [clause for clause in core if len(clause) > 1]
        if len(core) != 27 or len(positive) != 1 or Counter(core) != Counter([positive[0]] + [frozenset({-literal}) for literal in positive[0]]):
            raise AssertionError("validation direct-deficit form mismatch")
        checked = subprocess.run([str(DRAT), str(core_path), str(proof_path)], capture_output=True, text=True, check=False)
        if checked.returncode != 0 or "VERIFIED" not in checked.stdout + checked.stderr:
            raise AssertionError("validation proof rejected")

    with multiprocessing.Pool(processes=3) as pool:
        census = pool.map(census_base, range(100))
    certificate_rows = read_table(OUT / "census/certificates.tsv")
    expected_certificates = [(index, ordinal, clause_index) for index, matches, _ in census for ordinal, clause_index in matches]
    actual_certificates = [(int(row["base_index"]), int(row["leaf_ordinal"]), int(row["target_clause_index"])) for row in certificate_rows]
    if actual_certificates != expected_certificates or len(actual_certificates) != 34398:
        raise AssertionError("template census replay mismatch")
    counts = [len(matches) for _, matches, _ in census]
    return {"leaves": 6084, "leaf_proofs_replayed": 6084 if replay_proofs else 0, "cores": 608, "selected_clauses": 27, "validation_matches": 2, "census_tests": 608400, "census_matches": sum(counts), "complete_bases": sum(count == 6084 for count in counts)}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--proofs", action="store_true")
    args = parser.parse_args()
    result = audit(args.proofs)
    print("PASS " + " ".join(f"{key}={value}" for key, value in result.items()))
