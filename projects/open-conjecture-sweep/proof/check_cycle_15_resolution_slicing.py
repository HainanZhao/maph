#!/usr/bin/env python3
"""Read-only exact audit for Cycle 15's LRAT slices and SAT models."""

from __future__ import annotations

from array import array
from collections import Counter, deque
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
from lrc_core_templates import clauses, normalize, sample_bases, sha256
from lrc_proof_diversification import discriminating
from lrc_resolution_slicing import INPUTS, LRAT, MODELS, OUT, PROTECTED_ID, SOURCE, build_graph, read_table


def audit() -> dict[str, int]:
    starts, ends, empty, hints = build_graph()
    maximum = len(starts) - 1
    reached = bytearray(maximum + 1)
    reached[empty] = 1
    pending = deque([empty])
    while pending:
        node = pending.popleft()
        if starts[node] < 0:
            continue
        for antecedent in hints[starts[node]:ends[node]]:
            if not reached[antecedent]:
                reached[antecedent] = 1
                pending.append(antecedent)
    reached_inputs = sum(reached[clause_id] for clause_id in range(1, INPUTS + 1))
    if empty != 722343 or reached_inputs != 2294:
        raise AssertionError("LRAT closure mismatch")
    root_children = list(hints[starts[empty]:ends[empty]])
    masks = [0] * (maximum + 1)
    for bit, child in enumerate(root_children):
        masks[child] |= 1 << bit
    for node in range(empty - 1, INPUTS, -1):
        if not masks[node] or starts[node] < 0:
            continue
        for antecedent in hints[starts[node]:ends[node]]:
            masks[antecedent] |= masks[node]
    full = (1 << len(root_children)) - 1
    if any(masks[node] == full for node in range(INPUTS + 1, empty)):
        raise AssertionError("missed common-reachable derived node")

    candidates = read_table(OUT / "candidates.tsv")
    results = read_table(OUT / "results.tsv")
    if len(candidates) != 6 or len(results) != 6 or any(row["status"] != "SAT" for row in results):
        raise AssertionError("candidate/result census mismatch")
    _, source = clauses(SOURCE)
    normalized = normalize(source, sample_bases()[7])
    by_key = {(row["family"], row["parameter"]): row for row in candidates}
    for result in results:
        key = result["family"], result["parameter"]
        row = by_key[key]
        cnf = OUT / "candidates" / row["cnf"]
        _, candidate = clauses(cnf)
        if Counter(candidate) - Counter(source) or len(candidate) != int(row["clauses"]):
            raise AssertionError("candidate source-subset mismatch")
        if source[PROTECTED_ID - 1] not in candidate or not discriminating(normalized[PROTECTED_ID - 1]):
            raise AssertionError("protected clause missing")
        if sha256(cnf) != result["cnf_sha256"]:
            raise AssertionError("candidate hash mismatch")
        model_path = MODELS / f"{key[0]}-{key[1]}.model"
        if sha256(model_path) != result["evidence_sha256"]:
            raise AssertionError("model hash mismatch")
        literals = [int(token) for token in model_path.read_text().split() if token != "0"]
        model = {abs(literal): literal > 0 for literal in literals}
        if any(not any(abs(literal) in model and model[abs(literal)] == (literal > 0) for literal in clause) for clause in candidate):
            raise AssertionError("preserved model fails candidate")
    return {"empty_id": empty, "reached_inputs": reached_inputs, "root_children": len(root_children), "dominator_candidates": 0, "sat_candidates": 6}


if __name__ == "__main__":
    result = audit()
    print("PASS " + " ".join(f"{key}={value}" for key, value in result.items()))
