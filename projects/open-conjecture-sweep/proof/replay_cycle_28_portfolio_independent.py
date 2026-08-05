#!/usr/bin/env python3
"""Independent full selector and LP-separation replay for Cycle 28."""
from __future__ import annotations

import csv
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import sys
import time
import traceback

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"
C21 = ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv"
C22 = ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv"
TARGETS = ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv"
RESULTS = OUT / "results.tsv"
ROUND_CAP = 512
TOL = 1e-9
AUDIT_WALL = 6500
SPECS = (("c22_b4_l952", C22, 4, 952, 65528, 65440), ("c21_b4_l83", C21, 4, 83, 4091, 4090), ("c21_b4_l104", C21, 4, 104, 65539, 65448), ("c21_b3_l94", C21, 3, 94, 4107, 4080))


def read(path):
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse(text):
    return tuple(tuple(map(int, item.split("-"))) for item in text.split(","))


def text(blocks):
    return ",".join("-".join(map(str, block)) for block in blocks)


def count(block, allowed):
    value = 1
    for coordinate in block:
        value *= len(allowed[coordinate])
    if not 0 < value <= 14**5:
        raise AssertionError("option count")
    return value


def source_weight(row):
    answer = np.zeros(coupled.P * coupled.C, dtype=np.int64)
    clauses = list(map(int, row["source_clauses"].split(",")))
    values = list(map(int, row["weights"].split(",")))
    if len(clauses) != len(values) or not clauses:
        raise AssertionError("support")
    for clause, value in zip(clauses, values, strict=True):
        index = clause - width4.FIRST_TIME
        if not 0 <= index < len(answer) or value <= 0 or answer[index]:
            raise AssertionError("source index")
        answer[index] = value
    return answer


def load_portfolio():
    answer = []
    for label, path, base, leaf, total, upper in SPECS:
        found = [row for row in read(path) if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (base, leaf, "CERTIFIED_DEFICIT")]
        if len(found) != 1:
            raise AssertionError(f"source {label}")
        row = found[0]; weight = source_weight(row)
        if int(weight.sum()) != total or (int(row["W"]), int(row["U"])) != (total, upper):
            raise AssertionError(f"source total {label}")
        answer.append((label, base, leaf, parse(row["partition"]), weight, total, upper))
    return tuple(answer)


def max_columns(block, allowed, coverage, weights):
    """Independent streamed all-option maximum for integer columns."""
    prefix, tail = block[:3], block[3:]
    states = np.zeros((1, coverage.shape[0]), dtype=bool)
    for coordinate in prefix:
        digits = list(allowed[coordinate])
        states = np.logical_or(states[:, None, :], coverage[:, coordinate, digits].T[None, :, :]).reshape(-1, coverage.shape[0])
    if len(tail) <= 1:
        heads, final, final_digits = [()], tail[0] if tail else None, tuple(allowed[tail[0]]) if tail else ((),)
    else:
        heads, final, final_digits = itertools.product(*[tuple(allowed[c]) for c in tail[:-1]]), tail[-1], tuple(allowed[tail[-1]])
    best = np.full(weights.shape[1], -1, dtype=np.int64); enumerated = 0
    for head in heads:
        base = states
        for coordinate, digit in zip(tail[:-1] if tail else (), head, strict=True):
            base = base | coverage[:, coordinate, digit]
        flat = base[:, None, :].reshape(-1, coverage.shape[0]) if final is None else np.logical_or(base[:, None, :], coverage[:, final, list(final_digits)].T[None, :, :]).reshape(-1, coverage.shape[0])
        best = np.maximum(best, (flat @ weights).max(axis=0)); enumerated += len(flat)
    if enumerated != count(block, allowed):
        raise AssertionError("maximum census")
    return best


def max_option(block, allowed, coverage, weights):
    prefix, tail = block[:3], block[3:]
    states = np.zeros((1, coverage.shape[0]), dtype=bool); prefixes = [()]
    for coordinate in prefix:
        digits = tuple(allowed[coordinate])
        states = np.logical_or(states[:, None, :], coverage[:, coordinate, list(digits)].T[None, :, :]).reshape(-1, coverage.shape[0])
        prefixes = [prior + (digit,) for prior in prefixes for digit in digits]
    if len(tail) <= 1:
        heads, final, final_digits = [()], tail[0] if tail else None, tuple(allowed[tail[0]]) if tail else ((),)
    else:
        heads, final, final_digits = itertools.product(*[tuple(allowed[c]) for c in tail[:-1]]), tail[-1], tuple(allowed[tail[-1]])
    best_value = -float("inf"); best_option = None; best_mask = None; enumerated = 0
    for head in heads:
        base = states
        for coordinate, digit in zip(tail[:-1] if tail else (), head, strict=True):
            base = base | coverage[:, coordinate, digit]
        if final is None:
            flat = base[:, None, :].reshape(-1, coverage.shape[0]); digits = ((),)
        else:
            flat = np.logical_or(base[:, None, :], coverage[:, final, list(final_digits)].T[None, :, :]).reshape(-1, coverage.shape[0]); digits = final_digits
        scores = flat @ weights; index = int(np.argmax(scores)); first, last = divmod(index, len(digits)); option = prefixes[first] + head + (() if final is None else (digits[last],)); value = float(scores[index])
        if value > best_value or (value == best_value and (best_option is None or option < best_option)):
            best_value, best_option, best_mask = value, option, flat[index].copy()
        enumerated += len(flat)
    if enumerated != count(block, allowed) or best_option is None or best_mask is None:
        raise AssertionError("option census")
    return best_value, best_option, best_mask


def capacities(blocks, allowed, coverage, weights):
    return sum((max_columns(block, allowed, coverage, weights) for block in blocks), np.zeros(weights.shape[1], dtype=np.int64))


def rotations():
    base = ((0, 1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12))
    answer = []
    for r in range(coupled.K):
        answer.append((r, tuple(sorted(tuple(sorted((x + r) % coupled.K for x in block)) for block in base))))
    if len({blocks for _r, blocks in answer}) != 13:
        raise AssertionError("rotation census")
    return tuple(answer)


def control(portfolio):
    output = {}
    for label, base, leaf, blocks, weight, total, upper in portfolio:
        allowed = direct.allowed_digits(coupled.read_bases()[base], leaf); coverage = width4.raw_coverage(direct.CNFS[base])
        observed = int(capacities(blocks, allowed, coverage, weight[:, None])[0])
        if observed != upper:
            raise AssertionError(f"control {label}")
        output[label] = {"W": total, "U": observed}
    return output


def select(job):
    base, leaf, portfolio, deadline = job
    if time.monotonic() >= deadline:
        raise AssertionError("selection deadline")
    allowed = direct.allowed_digits(coupled.read_bases()[base], leaf); coverage = width4.raw_coverage(direct.CNFS[base]); matrix = np.column_stack([entry[4] for entry in portfolio])
    choices = []
    for rotation, blocks in rotations():
        if time.monotonic() >= deadline:
            raise AssertionError("selection deadline")
        values = tuple(map(int, capacities(blocks, allowed, coverage, matrix)))
        score = sum((Fraction(value, entry[5]) for value, entry in zip(values, portfolio, strict=True)), Fraction())
        choices.append((score, text(blocks), rotation, values))
    score, partition, rotation, values = min(choices, key=lambda value: (value[0], value[1]))
    return base, leaf, rotation, partition, f"{score.numerator}/{score.denominator}", ",".join(map(str, values))


def solve(job):
    row, deadline = job; base, leaf = int(row["base_index"]), int(row["leaf_ordinal"]); blocks = parse(row["partition"])
    allowed = direct.allowed_digits(coupled.read_bases()[base], leaf); coverage = width4.raw_coverage(direct.CNFS[base]); n = len(coverage)
    cuts = []; seen = [set() for _ in blocks]
    for block_id, block in enumerate(blocks):
        option = tuple(allowed[c][0] for c in block); mask = np.logical_or.reduce([coverage[:, c, d] for c, d in zip(block, option, strict=True)])
        cuts.append((block_id, option, mask)); seen[block_id].add(option)
    obj = np.r_[np.zeros(n), np.ones(len(blocks))]; eq = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + len(blocks)))
    for round_number in range(1, ROUND_CAP + 1):
        if time.monotonic() >= deadline:
            raise AssertionError("LP deadline")
        data=[]; rr=[]; cc=[]
        for r, (block_id, _option, mask) in enumerate(cuts):
            selected = np.flatnonzero(mask); rr.extend([r] * len(selected)); cc.extend(selected); data.extend([1.0] * len(selected)); rr.append(r); cc.append(n + block_id); data.append(-1.0)
        result = linprog(obj, A_ub=csr_matrix((data, (rr, cc)), shape=(len(cuts), n + len(blocks))), b_ub=np.zeros(len(cuts)), A_eq=eq, b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds", options={"presolve": True})
        if result.status != 0:
            raise AssertionError(result.message)
        added=[]
        for block_id, block in enumerate(blocks):
            value, option, mask = max_option(block, allowed, coverage, result.x[:n])
            if value > float(result.x[n + block_id]) + TOL:
                if option in seen[block_id]:
                    raise AssertionError("repeat separation")
                added.append((block_id, option, mask))
        if not added:
            return base, leaf, float(result.fun), round_number, len(cuts)
        for block_id, option, mask in added:
            cuts.append((block_id, option, mask)); seen[block_id].add(option)
    raise AssertionError("round cap")


def audit():
    started = time.monotonic(); deadline = started + AUDIT_WALL; portfolio = load_portfolio(); source = control(portfolio)
    target_rows = read(TARGETS); output_rows = read(RESULTS)
    if len(target_rows) != len(output_rows) != 0 or len(target_rows) != 60:
        raise AssertionError("row count")
    jobs = [(int(row["base_index"]), int(row["leaf_ordinal"]), portfolio, deadline) for row in target_rows]
    with multiprocessing.Pool(processes=3) as pool:
        selected = pool.map(select, jobs, chunksize=1)
    for row, choice in zip(output_rows, selected, strict=True):
        base, leaf, rotation, partition, score, values = choice
        if (base, leaf) != (int(row["base_index"]), int(row["leaf_ordinal"])) or (rotation, partition, score, values) != (int(row["selected_rotation"]), row["partition"], row["selector_score"], row["selector_capacities"]):
            raise AssertionError("selection mismatch")
    with multiprocessing.Pool(processes=3) as pool:
        replay = pool.map(solve, [(row, deadline) for row in output_rows], chunksize=1)
    for row, observed in zip(output_rows, replay, strict=True):
        base, leaf, value, rounds, cuts = observed
        if row["status"] != "UNRESOLVED" or (base, leaf) != (int(row["base_index"]), int(row["leaf_ordinal"])) or abs(value - float(row["objective"])) > 1e-8 or (rounds, cuts) != (int(row["separation_rounds"]), int(row["cuts"])):
            raise AssertionError("LP mismatch")
        if value < 1 - TOL:
            raise AssertionError("unexpected strict value")
    return {"status": "PASS", "epistemic_status": "OBSERVED", "source_controls": source, "targets": 60, "independent_selector_replays": 60, "independent_lp_separations": 60, "wall_seconds": time.monotonic() - started}


if __name__ == "__main__":
    target = OUT / "independent-replay.json"
    try:
        outcome = audit()
    except Exception as error:
        target = OUT / "independent-replay-error.json"
        temporary = target.with_suffix(".json.tmp")
        temporary.write_text(json.dumps({"status": "FAIL", "error_type": type(error).__name__, "error": str(error), "traceback": traceback.format_exc()}, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        temporary.replace(target)
        raise
    temporary = target.with_suffix(".json.tmp")
    temporary.write_text(json.dumps(outcome, indent=2, sort_keys=True) + "\n", encoding="utf-8"); temporary.replace(target)
    print(json.dumps(outcome, indent=2, sort_keys=True))
