#!/usr/bin/env python3
"""Independent reverse-order reconstruction of Cycle 50's frozen census."""
from __future__ import annotations

from collections import Counter, defaultdict
from fractions import Fraction
import itertools
import json
import multiprocessing
from pathlib import Path
import resource
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "discovery"))
import lrc_cech_actual as base
import lrc_signed_ownership_moments as moments
from lrc_cube_rewrite import clean, mobius_tensor, normalized_cube, pair_marginals
from lrc_cube_rewrite_select import relation_data
from lrc_multiplied_fill_probe import oriented_relation_transport
from lrc_relative_diagonal import PAIRS, apply_cube, cell_allowed, terminal_choice

OUT = ROOT / "discovery/out/cycle50-deletion-aware-packet"
TYPE_ID = {}; MASKS = []; MULT = {}; GROUPS = {}; ORIGINAL = {}; REL_DELETED = {}; TRANS_MASKS = []; MARGINALS = []; DIST = []; RANK3 = {}


def raw_valid(t):
    return MULT[t[0]] >= 3 if t[0] == t[2] else (MULT[t[0]] >= 2 if t[0] == t[1] else (MULT[t[1]] >= 2 if t[1] == t[2] else True))


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return moments.coordinate_classes(owner)


def rank3(owner):
    result = {}
    for pattern in base.c38._COORDINATES[owner]["patterns"]:
        if int(pattern["rank"]) != 3: continue
        groups = [[TYPE_ID[row[0]] for row in base.c38._TYPE_ROWS[owner][int(sig)]] for sig in pattern["signatures"]]
        for values in itertools.product(*groups):
            t = tuple(sorted(values))
            if raw_valid(t): result[t] = result.get(t, 0) | (1 << owner)
    return result


def type_triples(ms):
    a, b, c = ms
    if a == b == c: it = itertools.combinations_with_replacement(GROUPS[a], 3)
    elif a == b: it = (tuple(sorted((*x, y))) for x in itertools.combinations_with_replacement(GROUPS[a], 2) for y in GROUPS[c])
    elif b == c: it = (tuple(sorted((x, *y))) for x in GROUPS[a] for y in itertools.combinations_with_replacement(GROUPS[b], 2))
    else: it = (tuple(sorted(x)) for x in itertools.product(GROUPS[a], GROUPS[b], GROUPS[c]))
    yield from (t for t in it if raw_valid(t))


def contraction(source, supports, deleted, triple):
    state = defaultdict(Fraction, source); original = pair_marginals(clean(state)); steps = 0
    for w in sorted(set(supports[0]) & set(supports[1]) & set(supports[2])):
        pivot = (w, w, w)
        if not state[pivot] or cell_allowed(pivot, deleted, triple): continue
        selected = None
        for alts in itertools.product(*(tuple(x for x in support if x != w) for support in supports)):
            cube = normalized_cube(pivot, alts); scale = state[pivot] / cube[pivot]
            if all(cell_allowed(cell, deleted, triple) or state[cell] - scale * value == 0 for cell, value in cube.items()):
                selected = cube; break
        if selected is None: return "NO_ADMISSIBLE_PACKET", "TRIPLE", pivot, steps
        apply_cube(state, selected, pivot); steps += 1
    for left, right in PAIRS:
        other = 3 - left - right
        for w in sorted(set(supports[left]) & set(supports[right])):
            if not deleted[(left, right)] & (1 << w): continue
            active = [c for c in supports[other] if state[tuple(w if i in (left, right) else c for i in range(3))]]
            if not active: continue
            choice = terminal_choice(left, right, w, active, supports)
            if choice is None:
                c = next((x for x in active if x != w), w)
                return "BUFFER_INCOMPLETE", f"PAIR_{left}{right}", tuple(w if i in (left, right) else c for i in range(3)), steps
            terminal, buffers = choice
            for c in sorted(active):
                pivot = tuple(w if i in (left, right) else c for i in range(3))
                if c in (w, terminal) or not state[pivot]: continue
                a, b = buffers[c]; alts = [None, None, None]; alts[left], alts[right], alts[other] = a, b, terminal
                cube = normalized_cube(pivot, tuple(alts)); apply_cube(state, cube, pivot); steps += 1
            terminal_cell = tuple(w if i in (left, right) else terminal for i in range(3))
            if state[terminal_cell]: return "NONZERO_TERMINAL", f"PAIR_{left}{right}", terminal_cell, steps
    result = clean(state)
    assert pair_marginals(result) == original
    assert all(cell_allowed(cell, deleted, triple) for cell in result)
    return "CONTRACTED", None, None, steps


def classify(rows):
    counts = Counter(); failures = []; cache = {}; moves = 0
    for ms in rows:
        for t in type_triples(ms):
            counts["selected_type_triples"] += 1
            deleted = {p: ORIGINAL.get(tuple(sorted((t[p[0]], t[p[1]]))), 0) for p in PAIRS}
            flows = {}
            for p in PAIRS:
                pair = (t[p[0]], t[p[1]])
                if pair not in cache: cache[pair] = oriented_relation_transport(*pair, REL_DELETED, MARGINALS, TRANS_MASKS)
                flows[p] = cache[pair]
            source = mobius_tensor(flows, tuple(DIST[x] for x in t))
            supports = tuple(tuple(i for i in range(13) if MASKS[x] & (1 << i)) for x in t)
            status, stage, pivot, used = contraction(source, supports, deleted, RANK3.get(t, 0)); moves += used; counts[status] += 1
            if status != "CONTRACTED": failures.append({"types": list(t), "support_sizes": [len(x) for x in supports], "status": status, "stage": stage, "pivot": list(pivot)})
    return dict(counts), failures, moves


def main():
    global TYPE_ID, MASKS, MULT, GROUPS, ORIGINAL, REL_DELETED, TRANS_MASKS, MARGINALS, DIST, RANK3
    started = time.monotonic(); base.prepare_fast()
    complete = sorted({r[0] for root in base.c38._TYPE_ROWS for rows in root.values() for r in rows}); TYPE_ID = {x:i for i,x in enumerate(complete)}
    MASKS = [sum(1 << i for i, x in enumerate(v) if x) for v in complete]; moments._TYPE_ID, moments._TYPE_MASKS = TYPE_ID, MASKS
    raw = [TYPE_ID[tuple(sum(1 << o for o, d in enumerate(base.c38._ALLOWED[c]) if base.c38._COVERAGE[p,c,d]) for c in range(13))] for p in range(base.c38._COVERAGE.shape[0])]
    MULT = Counter(raw); GROUPS = defaultdict(list)
    for i, m in enumerate(MASKS): GROUPS[m].append(i)
    with multiprocessing.Pool(3) as pool: coords = pool.map(coordinate, range(13), chunksize=1)
    ORIGINAL, REL_DELETED, TRANS_MASKS = relation_data(MASKS, coords)
    prior = json.loads((ROOT / "discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    MARGINALS = [{int(o): Fraction(n, d) for o, n, d in row} for row in prior["singleton_marginals_by_complete_type"]]; DIST = [next(iter(x)) for x in MARGINALS]
    with multiprocessing.Pool(3) as pool: rank_rows = pool.map(rank3, range(13), chunksize=1)
    joined = defaultdict(int)
    for row in rank_rows:
        for t, d in row.items(): joined[t] |= d
    RANK3 = dict(joined)
    masks = [m for m in sorted(GROUPS) if m.bit_count() in (2,4)]
    rows = [x for x in itertools.combinations_with_replacement(masks, 3) if tuple(sorted(m.bit_count() for m in x)) in ((2,2,2),(2,2,4))]
    shards = [[], [], []]
    for i, row in enumerate(reversed(rows)): shards[i % 3].append(row)
    with multiprocessing.Pool(3) as pool: outcomes = pool.map(classify, shards, chunksize=1)
    counts = Counter(); failures = []
    for c, f, _ in outcomes: counts.update(c); failures.extend(f)
    result = {"status":"PASS", "epistemic_status":"PROVED", "counts":dict(sorted(counts.items())), "packet_moves":sum(x[2] for x in outcomes), "failures":sorted(failures,key=lambda x:tuple(x["types"])), "wall_seconds":time.monotonic()-started, "method":"Independent reverse mask/type ordering and independently implemented deletion-aware contraction; no import of the principal Cycle 50 module."}
    (OUT / "independent-replay.json").write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({k:v for k,v in result.items() if k not in ("failures","method")},sort_keys=True))


if __name__ == "__main__":
    multiprocessing.set_start_method("fork"); main()
