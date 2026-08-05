#!/usr/bin/env python3
"""Cycle 28: exact portfolio-selected cyclic width-five direct LPs."""
from __future__ import annotations

import csv
from fractions import Fraction
import itertools
import json
import multiprocessing
import os
from pathlib import Path
import sys
import time
from typing import NamedTuple

os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")

import numpy as np
from scipy.optimize import linprog
from scipy.sparse import csr_matrix

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_coupled_incidence as coupled
import lrc_pair_choice as direct
import lrc_width_four_stage_a as width4

OUT = ROOT / "discovery/out/cycle28-portfolio-cyclic-width-five"
TRANCHE_ONE_SELECTION = OUT / "selection-tranche1.tsv"
TRANCHE_ONE_RESULTS = OUT / "results-tranche1.tsv"
C21 = ROOT / "discovery/out/cycle21-coupled-incidence/results.tsv"
C22 = ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv"
C25 = ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv"
TOL = 1e-9
ROUND_CAP = 512
EXECUTION_WALL_SECONDS = 3500
DENOMINATORS = (4096, 65536, 1048576, 16777216)
MAX_OPTIONS = 14**5
PREFIX_COORDINATES = 3
PORTFOLIO_SPECS = (("c22_b4_l952", C22, 4, 952, 65528, 65440), ("c21_b4_l83", C21, 4, 83, 4091, 4090), ("c21_b4_l104", C21, 4, 104, 65539, 65448), ("c21_b3_l94", C21, 3, 94, 4107, 4080))


class Source(NamedTuple):
    label: str
    base: int
    leaf: int
    partition: tuple[tuple[int, ...], ...]
    weights: np.ndarray
    total: int
    upper: int


class Selection(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    selected_rotation: int
    partition: str
    score: str
    capacities: str


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    selected_rotation: int
    partition: str
    selector_score: str
    selector_capacities: str
    objective: str
    separation_rounds: int
    cuts: int
    denominator: int
    support: int
    W: int
    U: int
    block_maxima: str
    detail: str


def rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def partition_text(blocks: tuple[tuple[int, ...], ...]) -> str:
    return ",".join("-".join(map(str, block)) for block in blocks)


def option_count(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...]) -> int:
    value = 1
    for coordinate in block:
        value *= len(allowed[coordinate])
    if not 0 < value <= MAX_OPTIONS:
        raise AssertionError("option cap")
    return value


def option_mask(block: tuple[int, ...], option: tuple[int, ...], coverage: np.ndarray) -> np.ndarray:
    return np.logical_or.reduce([coverage[:, coordinate, digit] for coordinate, digit in zip(block, option, strict=True)])


def maximum_values(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...], coverage: np.ndarray, weights: np.ndarray) -> np.ndarray:
    """Return exact maxima for every integer weight column with streamed states."""
    if weights.ndim != 2 or weights.shape[0] != coverage.shape[0]:
        raise AssertionError("weight shape")
    prefix, tail = block[:min(PREFIX_COORDINATES, len(block))], block[min(PREFIX_COORDINATES, len(block)):]
    states = np.zeros((1, coverage.shape[0]), dtype=bool)
    for coordinate in prefix:
        choices = coverage[:, coordinate, list(allowed[coordinate])].T
        states = np.logical_or(states[:, None, :], choices[None, :, :]).reshape(-1, coverage.shape[0])
    if len(states) > 14**PREFIX_COORDINATES:
        raise AssertionError("prefix cap")
    if len(tail) <= 1:
        suffixes, final_coordinate, final_digits = [()], tail[0] if tail else None, tuple(allowed[tail[0]]) if tail else ((),)
    else:
        suffixes, final_coordinate, final_digits = itertools.product(*[tuple(allowed[c]) for c in tail[:-1]]), tail[-1], tuple(allowed[tail[-1]])
    maximum = np.full(weights.shape[1], -1, dtype=np.int64)
    enumerated = 0
    for suffix in suffixes:
        candidate = states
        for coordinate, digit in zip(tail[:-1] if tail else (), suffix, strict=True):
            candidate = candidate | coverage[:, coordinate, digit]
        if final_coordinate is None:
            flat = candidate[:, None, :].reshape(-1, coverage.shape[0])
        else:
            flat = np.logical_or(candidate[:, None, :], coverage[:, final_coordinate, list(final_digits)].T[None, :, :]).reshape(-1, coverage.shape[0])
        maximum = np.maximum(maximum, (flat @ weights).max(axis=0))
        enumerated += len(flat)
    if enumerated != option_count(block, allowed):
        raise AssertionError("option census")
    return maximum


def maximum_option(block: tuple[int, ...], allowed: tuple[tuple[int, ...], ...], coverage: np.ndarray, weights: np.ndarray) -> tuple[float, tuple[int, ...], np.ndarray]:
    """One streamed pass gives the maximum, lexicographic option, and mask."""
    prefix, tail = block[:min(PREFIX_COORDINATES, len(block))], block[min(PREFIX_COORDINATES, len(block)):]
    states = np.zeros((1, coverage.shape[0]), dtype=bool); prefixes = [()]
    for coordinate in prefix:
        digits = tuple(allowed[coordinate]); choices = coverage[:, coordinate, list(digits)].T
        states = np.logical_or(states[:, None, :], choices[None, :, :]).reshape(-1, coverage.shape[0])
        prefixes = [prior + (digit,) for prior in prefixes for digit in digits]
    if len(states) != len(prefixes) or len(states) > 14**PREFIX_COORDINATES:
        raise AssertionError("prefix census")
    if len(tail) <= 1:
        suffixes, final_coordinate, final_digits = [()], tail[0] if tail else None, tuple(allowed[tail[0]]) if tail else ((),)
    else:
        suffixes, final_coordinate, final_digits = itertools.product(*[tuple(allowed[c]) for c in tail[:-1]]), tail[-1], tuple(allowed[tail[-1]])
    best_value = -float("inf"); best_option = None; best_mask = None; enumerated = 0
    for suffix in suffixes:
        candidate = states
        for coordinate, digit in zip(tail[:-1] if tail else (), suffix, strict=True):
            candidate = candidate | coverage[:, coordinate, digit]
        if final_coordinate is None:
            flat = candidate[:, None, :].reshape(-1, coverage.shape[0]); digits = ((),)
        else:
            flat = np.logical_or(candidate[:, None, :], coverage[:, final_coordinate, list(final_digits)].T[None, :, :]).reshape(-1, coverage.shape[0]); digits = final_digits
        scores = flat @ weights; index = int(np.argmax(scores)); prefix_index, digit_index = divmod(index, len(digits))
        value = float(scores[index]); option = prefixes[prefix_index] + suffix + (() if final_coordinate is None else (digits[digit_index],))
        if value > best_value or (value == best_value and (best_option is None or option < best_option)):
            best_value, best_option, best_mask = value, option, flat[index].copy()
        enumerated += len(flat)
    if enumerated != option_count(block, allowed) or best_option is None or best_mask is None:
        raise AssertionError("option census")
    return best_value, best_option, best_mask


def exact_capacities(blocks: tuple[tuple[int, ...], ...], allowed: tuple[tuple[int, ...], ...], coverage: np.ndarray, weights: np.ndarray) -> np.ndarray:
    return sum((maximum_values(block, allowed, coverage, weights) for block in blocks), np.zeros(weights.shape[1], dtype=np.int64))


def extracted_weights(row: dict[str, str]) -> np.ndarray:
    clauses = list(map(int, row["source_clauses"].split(",")))
    values = list(map(int, row["weights"].split(",")))
    if not clauses or len(clauses) != len(values):
        raise AssertionError("source support")
    answer = np.zeros(coupled.P * coupled.C, dtype=np.int64)
    for clause, value in zip(clauses, values, strict=True):
        point = clause - width4.FIRST_TIME
        if not 0 <= point < len(answer) or value <= 0 or answer[point]:
            raise AssertionError("source weight")
        answer[point] = value
    return answer


def load_sources() -> tuple[Source, ...]:
    answer = []
    for label, path, base, leaf, total, upper in PORTFOLIO_SPECS:
        matches = [row for row in rows(path) if (int(row["base_index"]), int(row["leaf_ordinal"]), row["status"]) == (base, leaf, "CERTIFIED_DEFICIT")]
        if len(matches) != 1:
            raise AssertionError(f"source row {label}")
        row = matches[0]
        weights = extracted_weights(row)
        if int(weights.sum()) != total or int(row["W"]) != total or int(row["U"]) != upper:
            raise AssertionError(f"source total {label}")
        answer.append(Source(label, base, leaf, parse_partition(row["partition"]), weights, total, upper))
    return tuple(answer)


def source_control(sources: tuple[Source, ...]) -> dict[str, object]:
    result = {}
    for source in sources:
        allowed = direct.allowed_digits(coupled.read_bases()[source.base], source.leaf)
        coverage = width4.raw_coverage(direct.CNFS[source.base])
        observed = int(exact_capacities(source.partition, allowed, coverage, source.weights[:, None])[0])
        if observed != source.upper:
            raise AssertionError(f"source capacity {source.label}")
        result[source.label] = {"base_index": source.base, "leaf_ordinal": source.leaf, "W": source.total, "U": observed, "margin": source.total - observed}
    return result


def cyclic_partitions() -> tuple[tuple[int, tuple[tuple[int, ...], ...]], ...]:
    baseline = ((0, 1, 2, 3, 4), (5, 6, 7, 8), (9, 10, 11, 12))
    result = []
    for rotation in range(coupled.K):
        blocks = tuple(sorted(tuple(sorted((coordinate + rotation) % coupled.K for coordinate in block)) for block in baseline))
        result.append((rotation, blocks))
    if len({blocks for _rotation, blocks in result}) != coupled.K:
        raise AssertionError("cyclic candidate census")
    return tuple(result)


def selection_job(job: tuple[int, int, tuple[Source, ...], float]) -> Selection:
    base, leaf, sources, deadline = job
    if time.monotonic() >= deadline:
        return Selection(base, leaf, "CAP", -1, "", "", "")
    allowed = direct.allowed_digits(coupled.read_bases()[base], leaf)
    coverage = width4.raw_coverage(direct.CNFS[base])
    matrix = np.column_stack([source.weights for source in sources])
    candidates = []
    for rotation, blocks in cyclic_partitions():
        if time.monotonic() >= deadline:
            return Selection(base, leaf, "CAP", -1, "", "", "")
        capacities = tuple(map(int, exact_capacities(blocks, allowed, coverage, matrix)))
        score = sum((Fraction(value, source.total) for value, source in zip(capacities, sources, strict=True)), Fraction())
        candidates.append((score, partition_text(blocks), rotation, capacities))
    score, text, rotation, capacities = min(candidates, key=lambda item: (item[0], item[1]))
    return Selection(base, leaf, "SELECTED", rotation, text, f"{score.numerator}/{score.denominator}", ",".join(map(str, capacities)))


def lp_solution(blocks: tuple[tuple[int, ...], ...], allowed: tuple[tuple[int, ...], ...], coverage: np.ndarray, deadline: float):
    n, block_count = coverage.shape[0], len(blocks)
    cuts: list[tuple[int, tuple[int, ...], np.ndarray]] = []
    seen = [set() for _block in blocks]
    for block_id, block in enumerate(blocks):
        option = tuple(allowed[coordinate][0] for coordinate in block)
        cuts.append((block_id, option, option_mask(block, option, coverage)))
        seen[block_id].add(option)
    objective = np.concatenate((np.zeros(n), np.ones(block_count)))
    equality = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + block_count))
    for round_number in range(1, ROUND_CAP + 1):
        if time.monotonic() >= deadline:
            return None, round_number - 1, len(cuts), "CAP"
        data: list[float] = []; row_indices: list[int] = []; column_indices: list[int] = []
        for row_id, (block_id, _option, mask) in enumerate(cuts):
            selected = np.flatnonzero(mask)
            row_indices.extend([row_id] * len(selected)); column_indices.extend(selected); data.extend([1.0] * len(selected))
            row_indices.append(row_id); column_indices.append(n + block_id); data.append(-1.0)
        solved = linprog(objective, A_ub=csr_matrix((data, (row_indices, column_indices)), shape=(len(cuts), n + block_count)), b_ub=np.zeros(len(cuts)), A_eq=equality, b_eq=np.array([1.0]), bounds=(0, None), method="highs-ds", options={"presolve": True})
        if solved.status != 0:
            return None, round_number, len(cuts), f"LP_ERROR:{solved.message}"
        violations = []
        for block_id, block in enumerate(blocks):
            value, best_option, best_mask = maximum_option(block, allowed, coverage, solved.x[:n])
            if value > float(solved.x[n + block_id]) + TOL:
                if best_option in seen[block_id]:
                    return None, round_number, len(cuts), "SEPARATION_REPEAT"
                violations.append((block_id, best_option, best_mask))
        if not violations:
            return solved, round_number, len(cuts), "PASS"
        for block_id, option, mask in violations:
            cuts.append((block_id, option, mask)); seen[block_id].add(option)
    return None, ROUND_CAP, len(cuts), "CAP"


def solve_job(job: tuple[Selection, float]) -> Result:
    selection, deadline = job
    base, leaf = selection.base_index, selection.leaf_ordinal
    allowed = direct.allowed_digits(coupled.read_bases()[base], leaf)
    coverage = width4.raw_coverage(direct.CNFS[base])
    blocks = parse_partition(selection.partition)
    solved, rounds, cuts, status = lp_solution(blocks, allowed, coverage, deadline)
    common = (base, leaf)
    if status != "PASS" or solved is None:
        return Result(*common, status, selection.selected_rotation, selection.partition, selection.score, selection.capacities, "nan", rounds, cuts, 0, 0, 0, 0, "", status)
    objective = float(solved.fun)
    if objective >= 1 - TOL:
        return Result(*common, "UNRESOLVED", selection.selected_rotation, selection.partition, selection.score, selection.capacities, f"{objective:.17g}", rounds, cuts, 0, 0, 0, 0, "", "fully separated LP has no strict deficit")
    for denominator in DENOMINATORS:
        weights = np.rint(solved.x[:coverage.shape[0]] * denominator).astype(np.int64); weights[weights < 0] = 0
        support = int(np.count_nonzero(weights))
        if not 0 < support <= 256:
            continue
        maxima = exact_capacities(blocks, allowed, coverage, weights[:, None])
        upper, total = int(maxima[0]), int(weights.sum())
        if upper < total:
            return Result(*common, "CERTIFIED_DEFICIT", selection.selected_rotation, selection.partition, selection.score, selection.capacities, f"{objective:.17g}", rounds, cuts, denominator, support, total, upper, ",".join(map(str, maxima)), "fresh portfolio-selected direct-CNF width-five integer deficit")
    return Result(*common, "UNRESOLVED", selection.selected_rotation, selection.partition, selection.score, selection.capacities, f"{objective:.17g}", rounds, cuts, 0, 0, 0, 0, "", "strict float LP did not integerize under frozen rule")


def targets() -> list[tuple[int, int]]:
    value = rows(C25)
    answer = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in value]
    if len(answer) != len(set(answer)) != 0 or len(answer) != 60 or any(row["status"] != "UNRESOLVED" for row in value):
        raise AssertionError("target boundary")
    return answer


def write_tsv(path: Path, records: list[NamedTuple]) -> None:
    path.write_text("\t".join(records[0]._fields) + "\n" + "\n".join("\t".join(map(str, record)) for record in records) + "\n", encoding="utf-8")


def frozen_selection() -> list[Selection]:
    value = [Selection(int(row["base_index"]), int(row["leaf_ordinal"]), row["status"], int(row["selected_rotation"]), row["partition"], row["score"], row["capacities"]) for row in rows(TRANCHE_ONE_SELECTION)]
    if len(value) != 60 or [(row.base_index, row.leaf_ordinal) for row in value] != targets() or any(row.status != "SELECTED" for row in value):
        raise AssertionError("frozen selection boundary")
    return value


def frozen_results() -> list[Result]:
    value = [Result(int(row["base_index"]), int(row["leaf_ordinal"]), row["status"], int(row["selected_rotation"]), row["partition"], row["selector_score"], row["selector_capacities"], row["objective"], int(row["separation_rounds"]), int(row["cuts"]), int(row["denominator"]), int(row["support"]), int(row["W"]), int(row["U"]), row["block_maxima"], row["detail"]) for row in rows(TRANCHE_ONE_RESULTS)]
    if len(value) != 60 or [(row.base_index, row.leaf_ordinal) for row in value] != targets() or any(row.status not in {"UNRESOLVED", "CAP"} for row in value):
        raise AssertionError("frozen result boundary")
    return value


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    started = time.monotonic(); deadline = started + EXECUTION_WALL_SECONDS
    sources = load_sources(); control = source_control(sources)
    (OUT / "control.json").write_text(json.dumps(control, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if TRANCHE_ONE_SELECTION.is_file() and TRANCHE_ONE_RESULTS.is_file():
        selected, prior = frozen_selection(), frozen_results()
        write_tsv(OUT / "selection.tsv", selected)
    else:
        with multiprocessing.Pool(processes=3) as pool:
            selected = pool.map(selection_job, [(base, leaf, sources, deadline) for base, leaf in targets()], chunksize=1)
        write_tsv(OUT / "selection.tsv", selected)
        prior = None
    baseline = partition_text(cyclic_partitions()[0][1])
    if any(row.status != "SELECTED" for row in selected):
        text = "targets=60 selection=CAP wall_seconds=" + f"{time.monotonic()-started:.6f}"
        (OUT / "result.txt").write_text(text + "\n", encoding="utf-8"); print(text); return
    changed = sum(row.partition != baseline for row in selected)
    if not changed:
        text = "targets=60 selection=CONTAINED nonbaseline=0 wall_seconds=" + f"{time.monotonic()-started:.6f}"
        (OUT / "result.txt").write_text(text + "\n", encoding="utf-8"); print(text); return
    pending = selected if prior is None else [selection for selection, old in zip(selected, prior, strict=True) if old.status == "CAP"]
    with multiprocessing.Pool(processes=3) as pool:
        refreshed = pool.map(solve_job, [(row, deadline) for row in pending], chunksize=1)
    if prior is None:
        result = refreshed
    else:
        by_key = {(row.base_index, row.leaf_ordinal): row for row in refreshed}
        result = [by_key.get((old.base_index, old.leaf_ordinal), old) for old in prior]
    write_tsv(OUT / "results.tsv", result)
    counts = {status: sum(row.status == status for row in result) for status in sorted({row.status for row in result})}
    text = "targets=60 nonbaseline=" + str(changed) + " " + " ".join(f"{status.lower()}={count}" for status, count in counts.items()) + f" wall_seconds={time.monotonic()-started:.6f}"
    (OUT / "result.txt").write_text(text + "\n", encoding="utf-8"); print(text)


if __name__ == "__main__":
    if sys.argv[1:] == ["--control"]:
        OUT.mkdir(parents=True, exist_ok=True)
        print(json.dumps(source_control(load_sources()), indent=2, sort_keys=True))
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit("usage: lrc_portfolio_cyclic_width_five.py [--control]")
