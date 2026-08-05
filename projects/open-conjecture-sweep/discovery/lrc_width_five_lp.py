#!/usr/bin/env python3
"""Cycle 27 fresh direct time-weight LP with exhaustive option separation."""
from __future__ import annotations

import csv
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

OUT = ROOT / "discovery/out/cycle27-width-five-lp"
SOURCE = ROOT / "discovery/out/cycle22-width-four/stage-b-results.tsv"
TARGETS = ROOT / "discovery/out/cycle25-quadratic-crt/results.tsv"
TOL = 1e-9
SOURCE_ROUNDS, TARGET_ROUNDS = 512, 512
DENOMINATORS = (4096, 65536, 1048576, 16777216)
MAX_OPTIONS = 14**5
SEPARATION_PREFIX_COORDINATES = 3


class Result(NamedTuple):
    base_index: int
    leaf_ordinal: int
    status: str
    partition: str
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


def source_row() -> dict[str, str]:
    found = [row for row in rows(SOURCE) if row["status"] == "CERTIFIED_DEFICIT"]
    if len(found) != 1 or (int(found[0]["base_index"]), int(found[0]["leaf_ordinal"]), int(found[0]["support"]), int(found[0]["W"]), int(found[0]["U"])) != (4, 952, 176, 65528, 65440):
        raise AssertionError("source boundary")
    return found[0]


def source_weights() -> np.ndarray:
    row = source_row(); clauses = list(map(int, row["source_clauses"].split(","))); values = list(map(int, row["weights"].split(",")))
    if not len(clauses) == len(values) == 176: raise AssertionError("source support")
    result = np.zeros(coupled.P * coupled.C, dtype=np.int64)
    for clause, value in zip(clauses, values, strict=True):
        point = clause - width4.FIRST_TIME
        if not 0 <= point < len(result) or value <= 0 or result[point]: raise AssertionError("source point")
        result[point] = value
    if int(result.sum()) != 65528: raise AssertionError("source total")
    return result


def parse_partition(text: str) -> tuple[tuple[int, ...], ...]:
    return tuple(tuple(map(int, block.split("-"))) for block in text.split(","))


def target_rows() -> list[dict[str, str]]:
    value = rows(TARGETS)
    keys = [(int(row["base_index"]), int(row["leaf_ordinal"])) for row in value]
    if not (len(value) == len(set(keys)) == 60) or any(row["status"] != "UNRESOLVED" for row in value): raise AssertionError("target boundary")
    return value


def target_partition(allowed: tuple[tuple[int, ...], ...]) -> tuple[tuple[int, ...], ...]:
    order = sorted(range(coupled.K), key=lambda coordinate: (len(allowed[coordinate]), coordinate))
    blocks = tuple(sorted((tuple(sorted(order[:5])), tuple(sorted(order[5:9])), tuple(sorted(order[9:13])))))
    if sorted(map(len, blocks)) != [4, 4, 5] or sorted(item for block in blocks for item in block) != list(range(coupled.K)): raise AssertionError("partition")
    return blocks


def partition_text(blocks) -> str:
    return ",".join("-".join(map(str, block)) for block in blocks)


def option_count(block, allowed) -> int:
    count = 1
    for coordinate in block: count *= len(allowed[coordinate])
    if not 0 < count <= MAX_OPTIONS: raise AssertionError("option cap")
    return count


def option_mask(block, option, coverage) -> np.ndarray:
    return np.logical_or.reduce([coverage[:, coordinate, digit] for coordinate, digit in zip(block, option, strict=True)])


def maximum_option(block, allowed, coverage, weights) -> tuple[float, tuple[int, ...], np.ndarray]:
    """Exact finite maximization in bounded deterministic option batches.

    Materializing every 5-coordinate union used several GiB per worker.  A
    three-coordinate vectorized prefix and lexicographic tail loop enumerate
    the same options while bounding the largest Boolean table by 14**3 rows.
    """
    prefix_size = min(SEPARATION_PREFIX_COORDINATES, len(block))
    prefix, tail = block[:prefix_size], block[prefix_size:]
    states = np.zeros((1, coverage.shape[0]), dtype=bool)
    prefixes = [()]
    for coordinate in prefix:
        digits = tuple(allowed[coordinate])
        choices = coverage[:, coordinate, list(digits)].T
        states = np.logical_or(states[:, None, :], choices[None, :, :]).reshape(-1, coverage.shape[0])
        prefixes = [prior + (digit,) for prior in prefixes for digit in digits]
    if len(states) != len(prefixes) or len(states) > 14**SEPARATION_PREFIX_COORDINATES:
        raise AssertionError("prefix census")
    best_value = -float("inf"); best_option = None; best_mask = None; enumerated = 0
    tail_digits = [tuple(allowed[coordinate]) for coordinate in tail]
    if len(tail) <= 1:
        tail_prefixes, final_coordinate, final_digits = [()], tail[0] if tail else None, tail_digits[0] if tail else ((),)
    else:
        tail_prefixes, final_coordinate, final_digits = itertools.product(*tail_digits[:-1]), tail[-1], tail_digits[-1]
    for suffix_prefix in tail_prefixes:
        candidate = states
        for coordinate, digit in zip(tail[:-1] if tail else (), suffix_prefix, strict=True):
            candidate = candidate | coverage[:, coordinate, digit]
        if final_coordinate is None:
            candidates = candidate[:, None, :]
            digits = ((),)
        else:
            candidates = np.logical_or(candidate[:, None, :], coverage[:, final_coordinate, list(final_digits)].T[None, :, :])
            digits = final_digits
        flat = candidates.reshape(-1, coverage.shape[0]); scores = flat @ weights
        index = int(np.argmax(scores)); prefix_index, digit_index = divmod(index, len(digits)); value = float(scores[index])
        suffix = suffix_prefix + (() if final_coordinate is None else (digits[digit_index],))
        option = prefixes[prefix_index] + suffix
        if value > best_value or (value == best_value and (best_option is None or option < best_option)):
            best_value, best_option, best_mask = value, option, flat[index].copy()
        enumerated += len(flat)
    if enumerated != option_count(block, allowed) or best_option is None or best_mask is None:
        raise AssertionError("option census")
    return best_value, best_option, best_mask


def lp_solution(blocks, allowed, coverage, round_cap: int, deadline: float | None = None):
    n, bcount = coverage.shape[0], len(blocks)
    cuts: list[tuple[int, tuple[int, ...], np.ndarray]] = []
    seen = [set() for _ in blocks]
    for block_id, block in enumerate(blocks):
        option = tuple(allowed[coordinate][0] for coordinate in block)
        cuts.append((block_id, option, option_mask(block, option, coverage))); seen[block_id].add(option)
    objective = np.concatenate((np.zeros(n), np.ones(bcount)))
    equality = csr_matrix((np.ones(n), (np.zeros(n, dtype=int), np.arange(n))), shape=(1, n + bcount))
    for round_number in range(1, round_cap + 1):
        if deadline is not None and time.monotonic() >= deadline:
            return None, round_number - 1, len(cuts), "CAP"
        data=[]; row_indices=[]; col_indices=[]
        for row_id, (block_id, _option, mask) in enumerate(cuts):
            selected=np.flatnonzero(mask)
            row_indices.extend([row_id] * len(selected)); col_indices.extend(selected); data.extend([1.0] * len(selected))
            row_indices.append(row_id); col_indices.append(n + block_id); data.append(-1.0)
        inequalities=csr_matrix((data,(row_indices,col_indices)),shape=(len(cuts),n+bcount))
        solved=linprog(objective,A_ub=inequalities,b_ub=np.zeros(len(cuts)),A_eq=equality,b_eq=np.array([1.0]),bounds=(0,None),method="highs-ds",options={"presolve":True})
        if deadline is not None and time.monotonic() >= deadline:
            return None, round_number, len(cuts), "CAP"
        if solved.status != 0: return None, round_number, len(cuts), f"LP_ERROR:{solved.message}"
        violations=[]
        for block_id, block in enumerate(blocks):
            value, option, mask = maximum_option(block, allowed, coverage, solved.x[:n])
            if value > float(solved.x[n + block_id]) + TOL:
                if option in seen[block_id]: return None, round_number, len(cuts), "SEPARATION_REPEAT"
                violations.append((block_id, option, mask))
        if not violations: return solved, round_number, len(cuts), "PASS"
        for block_id, option, mask in violations: cuts.append((block_id, option, mask)); seen[block_id].add(option)
    return None, round_cap, len(cuts), "CAP"


def exact_capacity(blocks, allowed, coverage, integer_weights) -> tuple[int, list[int]]:
    active=np.flatnonzero(integer_weights); active_coverage=coverage[active]; active_weights=integer_weights[active]; maxima=[]
    for block in blocks:
        states=np.zeros((1,len(active)),dtype=bool)
        for coordinate in block:
            choices=active_coverage[:,coordinate,list(allowed[coordinate])].T
            states=np.logical_or(states[:,None,:],choices[None,:,:]).reshape(-1,len(active))
        if len(states)!=option_count(block,allowed): raise AssertionError("integer option census")
        maxima.append(int((states@active_weights).max()))
    return sum(maxima),maxima


def source_control() -> dict[str, object]:
    row=source_row(); weights=source_weights(); blocks=parse_partition(row["partition"]); allowed=direct.allowed_digits(coupled.read_bases()[4],952); coverage=width4.raw_coverage(direct.CNFS[4])
    upper,maxima=exact_capacity(blocks,allowed,coverage,weights)
    if (int(weights.sum()),upper,maxima)!=(65528,65440,[7587,12454,21481,23918]): raise AssertionError("source direct replay")
    solved, rounds, cuts, status=lp_solution(blocks,allowed,coverage,SOURCE_ROUNDS)
    if status != "PASS" or solved is None:
        return {"status": status, "source_W": 65528, "source_U": 65440, "source_margin": 88, "lp_rounds": rounds, "lp_cuts": cuts}
    if float(solved.fun) >= 1 - 1e-7:
        return {"status": "NONSTRICT", "source_W": 65528, "source_U": 65440, "source_margin": 88, "lp_objective": float(solved.fun), "lp_rounds": rounds, "lp_cuts": cuts}
    return {"status":"PASS","source_W":65528,"source_U":65440,"source_margin":88,"lp_objective":float(solved.fun),"lp_rounds":rounds,"lp_cuts":cuts}


def solve(job: tuple[int,int,float]) -> Result:
    base_index,ordinal,deadline=job; allowed=direct.allowed_digits(coupled.read_bases()[base_index],ordinal); blocks=target_partition(allowed); coverage=width4.raw_coverage(direct.CNFS[base_index])
    solved,rounds,cuts,status=lp_solution(blocks,allowed,coverage,TARGET_ROUNDS,deadline)
    if status!="PASS" or solved is None: return Result(base_index,ordinal,status,partition_text(blocks),"nan",rounds,cuts,0,0,0,0,"",status)
    objective=float(solved.fun)
    if objective>=1-TOL: return Result(base_index,ordinal,"UNRESOLVED",partition_text(blocks),f"{objective:.17g}",rounds,cuts,0,0,0,0,"","fully separated LP has no strict deficit")
    for denominator in DENOMINATORS:
        weights=np.rint(solved.x[:coverage.shape[0]]*denominator).astype(np.int64);weights[weights<0]=0;support=int(np.count_nonzero(weights))
        if not 0<support<=256: continue
        upper,maxima=exact_capacity(blocks,allowed,coverage,weights);total=int(weights.sum())
        if upper<total:return Result(base_index,ordinal,"CERTIFIED_DEFICIT",partition_text(blocks),f"{objective:.17g}",rounds,cuts,denominator,support,total,upper,",".join(map(str,maxima)),"fresh direct-CNF width-five integer deficit")
    return Result(base_index,ordinal,"UNRESOLVED",partition_text(blocks),f"{objective:.17g}",rounds,cuts,0,0,0,0,"","strict float LP did not integerize under frozen rule")


def main() -> None:
    OUT.mkdir(parents=True,exist_ok=True); started=time.monotonic(); control=source_control();(OUT/"control.json").write_text(json.dumps(control,indent=2,sort_keys=True)+"\n")
    if control["status"] != "PASS":
        text=f"control_status={control['status']} wall_seconds=0";(OUT/"result.txt").write_text(text+"\n");print(text);return
    deadline=started+3600
    with multiprocessing.Pool(processes=3) as pool: result=pool.map(solve,[(int(row["base_index"]),int(row["leaf_ordinal"]),deadline) for row in target_rows()],chunksize=1)
    (OUT/"results.tsv").write_text("\t".join(Result._fields)+"\n"+"\n".join("\t".join(map(str,row)) for row in result)+"\n")
    counts={status:sum(row.status==status for row in result) for status in sorted({row.status for row in result})};text="targets=60 "+" ".join(f"{status.lower()}={count}" for status,count in counts.items())+f" wall_seconds={time.monotonic()-started:.6f}";(OUT/"result.txt").write_text(text+"\n");print(text)


if __name__=="__main__":
    if sys.argv[1:] == ["--control"]:
        OUT.mkdir(parents=True, exist_ok=True)
        value = source_control()
        (OUT / "control.json").write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
        print(json.dumps(value, sort_keys=True))
    elif not sys.argv[1:]:
        main()
    else:
        raise SystemExit("usage: lrc_width_five_lp.py [--control]")
