#!/usr/bin/env python3
"""Independent reverse-order full replay of Cycle 49's residual classification."""
from __future__ import annotations

from collections import Counter, defaultdict, deque
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
from lrc_multiplied_fill_probe import oriented_relation_transport

OUT = ROOT / "discovery/out/cycle49-relative-diagonal"
PAIRS = ((0, 1), (0, 2), (1, 2))
TYPE_ID = {}
MASKS = []
MULT = {}
TARGET = set()
GROUPS = {}
ORIGINAL = {}
DELETED = {}
TRANSPORT_MASKS = []
MARGINALS = []
DISTINGUISHED = []
RANK3 = {}


def raw_valid(triple):
    a, b, c = triple
    return MULT[a] >= 3 if a == c else MULT[a] >= 2 if a == b else MULT[b] >= 2 if b == c else True


def coordinate(owner):
    resource.setrlimit(resource.RLIMIT_AS, (2_000_000_000, 2_000_000_000))
    return moments.coordinate_classes(owner)


def rank3_owner(owner):
    found = {}
    for pattern in reversed(base.c38._COORDINATES[owner]["patterns"]):
        if int(pattern["rank"]) != 3:
            continue
        groups = [[TYPE_ID[row[0]] for row in reversed(base.c38._TYPE_ROWS[owner][int(signature)])] for signature in reversed(pattern["signatures"])]
        for values in itertools.product(*groups):
            triple = tuple(sorted(values))
            if tuple(sorted(MASKS[value] for value in triple)) in TARGET and raw_valid(triple):
                found[triple] = found.get(triple, 0) | (1 << owner)
    return found


def relation_inputs(masks, rows):
    original = defaultdict(int)
    induced = defaultdict(int)
    for owner in reversed(range(13)):
        for pair in reversed(rows[owner]["rank_two_pairs"]): original[tuple(pair)] |= 1 << owner
        for pair in reversed(rows[owner]["induced_pair_deletions"]): induced[tuple(pair)] |= 1 << owner
    binary = {index for index, mask in enumerate(masks) if mask.bit_count() <= 2}
    blocked = defaultdict(list)
    for pair, owner_mask in original.items():
        for owner in reversed(range(13)):
            if owner_mask & (1 << owner):
                if pair[0] in binary: blocked[(pair[0], owner)].append(pair[1])
                if pair[1] in binary: blocked[(pair[1], owner)].append(pair[0])
    transport_masks = list(masks)
    for mediator in sorted(binary, reverse=True):
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) == 1:
            for neighbor in blocked[(mediator, owners[0])]: transport_masks[neighbor] &= ~(1 << owners[0])
    deleted = defaultdict(int)
    for pair in set(original) | set(induced):
        for owner in range(13):
            if (original.get(pair, 0) | induced.get(pair, 0)) & (1 << owner): deleted[pair] |= 1 << (13 * owner + owner)
    for mediator in binary:
        owners = [owner for owner in range(13) if masks[mediator] & (1 << owner)]
        if len(owners) != 2: continue
        a, b = owners
        for left in blocked[(mediator, a)]:
            for right in blocked[(mediator, b)]:
                if left <= right:
                    deleted[(left, right)] |= 1 << (13 * a + b)
                    if left == right: deleted[(left, right)] |= 1 << (13 * b + a)
                else: deleted[(right, left)] |= 1 << (13 * b + a)
    return dict(original), dict(deleted), transport_masks


def allowed(cell, pair_deleted, triple_deleted):
    return not any(cell[a] == cell[b] and pair_deleted[(a, b)] & (1 << cell[a]) for a, b in PAIRS) and not (cell[0] == cell[1] == cell[2] and triple_deleted & (1 << cell[0]))


def cube(pivot, alternatives):
    pairs = [tuple(sorted((pivot[index], alternatives[index]))) for index in range(3)]
    return {tuple(pairs[index][bits[index]] for index in range(3)): Fraction((-1) ** sum(bits)) for bits in itertools.product((0, 1), repeat=3)}


def triple_choices(w, supports):
    return sorted(values for values in itertools.product(*(tuple(owner for owner in support if owner != w) for support in supports)) if len(set(values)) == 3)


def exact_pair_possible(left, right, w, supports, pair_deleted, triple_deleted):
    other = 3 - left - right
    if not any(c != w for c in supports[other]): return True
    for terminal in supports[other]:
        if terminal == w: continue
        for c in supports[other]:
            if c in (w, terminal): continue
            pivot = tuple(w if index in (left, right) else c for index in range(3))
            terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
            found = False
            for a in supports[left]:
                if a == w: continue
                for b in supports[right]:
                    if b == w: continue
                    alternatives = [None, None, None]
                    alternatives[left], alternatives[right], alternatives[other] = a, b, terminal
                    if {cell for cell in cube(pivot, alternatives) if not allowed(cell, pair_deleted, triple_deleted)} <= {pivot, terminal_cell}:
                        found = True
                        break
                if found: break
            if not found: break
        else: return True
    return False


def structural(types, pair_deleted, triple_deleted, cache):
    supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
    key = (tuple(MASKS[value] for value in types), tuple(pair_deleted[pair] for pair in PAIRS), triple_deleted)
    if key in cache: return cache[key]
    common = MASKS[types[0]] & MASKS[types[1]] & MASKS[types[2]]
    active = common & (triple_deleted | pair_deleted[(0, 1)] | pair_deleted[(0, 2)] | pair_deleted[(1, 2)])
    for w in reversed(range(13)):
        if active & (1 << w) and not triple_choices(w, supports): cache[key] = False; return False
    for left, right in reversed(PAIRS):
        for w in reversed(range(13)):
            if pair_deleted[(left, right)] & (1 << w) and not exact_pair_possible(left, right, w, supports, pair_deleted, triple_deleted):
                cache[key] = False; return False
    cache[key] = True
    return True


def mobius(flows, distinguished):
    state = defaultdict(Fraction)
    d0, d1, d2 = distinguished
    for (b, c), value in reversed(sorted(flows[(1, 2)].items())): state[(d0, b, c)] += value
    for (a, c), value in reversed(sorted(flows[(0, 2)].items())): state[(a, d1, c)] += value
    for (a, b), value in reversed(sorted(flows[(0, 1)].items())): state[(a, b, d2)] += value
    state[(d0, d1, d2)] -= 2
    return {cell: value for cell, value in state.items() if value}


def contract_frozen(source, supports, pair_deleted, triple_deleted):
    state = defaultdict(Fraction, source)
    steps = 0
    common = set(supports[0]) & set(supports[1]) & set(supports[2])
    for w in sorted(common):
        pivot = (w, w, w)
        if not state[pivot] or allowed(pivot, pair_deleted, triple_deleted): continue
        choices = triple_choices(w, supports)
        if not choices: return "BUFFER_INCOMPLETE", steps
        packet = cube(pivot, choices[0]); scale = state[pivot] / packet[pivot]
        for cell, value in packet.items(): state[cell] -= scale * value
        steps += 1
    for left, right in PAIRS:
        other = 3 - left - right
        for w in sorted(set(supports[left]) & set(supports[right])):
            if not pair_deleted[(left, right)] & (1 << w): continue
            active = [c for c in supports[other] if state[tuple(w if index in (left, right) else c for index in range(3))]]
            if not active: continue
            choice = None
            for terminal in supports[other]:
                if terminal == w: continue
                buffers = {}
                for c in active:
                    if c in (w, terminal): continue
                    for a in supports[left]:
                        if a in {w, c, terminal}: continue
                        for b in supports[right]:
                            if b not in {w, c, terminal, a}: buffers[c] = (a, b); break
                        if c in buffers: break
                    if c not in buffers: break
                else: choice = (terminal, buffers); break
            if choice is None: return "BUFFER_INCOMPLETE", steps
            terminal, buffers = choice
            for c in sorted(active):
                pivot = tuple(w if index in (left, right) else c for index in range(3))
                if c in (w, terminal) or not state[pivot]: continue
                alternatives = [None, None, None]
                alternatives[left], alternatives[right], alternatives[other] = *buffers[c], terminal
                packet = cube(pivot, alternatives); scale = state[pivot] / packet[pivot]
                for cell, value in packet.items(): state[cell] -= scale * value
                steps += 1
            terminal_cell = tuple(w if index in (left, right) else terminal for index in range(3))
            if state[terminal_cell]: return "NONZERO_TERMINAL", steps
    final = {cell: value for cell, value in state.items() if value}
    assert not any(not allowed(cell, pair_deleted, triple_deleted) for cell in final)
    return "CONTRACTED", steps


def triples_for_masks(masks):
    a, b, c = masks
    if a == c: iterator = (tuple(sorted(values)) for values in itertools.combinations_with_replacement(reversed(GROUPS[a]), 3))
    elif a == b: iterator = (tuple(sorted((*pair, value))) for pair in itertools.combinations_with_replacement(reversed(GROUPS[a]), 2) for value in reversed(GROUPS[c]))
    elif b == c: iterator = (tuple(sorted((value, *pair))) for value in reversed(GROUPS[a]) for pair in itertools.combinations_with_replacement(reversed(GROUPS[b]), 2))
    else: iterator = (tuple(sorted(values)) for values in itertools.product(reversed(GROUPS[a]), reversed(GROUPS[b]), reversed(GROUPS[c])))
    for triple in iterator:
        if raw_valid(triple): yield triple


def classify(rows):
    counts = Counter(); failures = []; flow_cache = {}; semantic = {}
    for row in reversed(rows):
        for types in triples_for_masks(tuple(row["support_masks"])):
            counts["type_triples"] += 1
            pair_deleted = {pair: ORIGINAL.get(tuple(sorted((types[pair[0]], types[pair[1]]))), 0) for pair in PAIRS}
            triple_deleted = RANK3.get(types, 0)
            if structural(types, pair_deleted, triple_deleted, semantic): counts["structural_closed"] += 1; continue
            counts["mobius_attempted"] += 1
            flows = {}
            for pair in PAIRS:
                key = (types[pair[0]], types[pair[1]])
                if key not in flow_cache: flow_cache[key] = oriented_relation_transport(key[0], key[1], DELETED, MARGINALS, TRANSPORT_MASKS)
                flows[pair] = flow_cache[key]
            start = mobius(flows, tuple(DISTINGUISHED[value] for value in types))
            supports = tuple(tuple(owner for owner in range(13) if MASKS[value] & (1 << owner)) for value in types)
            if not any(value and not allowed(cell, pair_deleted, triple_deleted) for cell, value in start.items()): counts["mobius_already_allowed"] += 1; continue
            status, steps = contract_frozen(start, supports, pair_deleted, triple_deleted)
            counts["packet_moves"] += steps
            if status == "CONTRACTED": counts["mobius_contracted"] += 1
            else: counts[status] += 1; failures.append(list(types))
    return dict(counts), sorted(failures)


def main():
    global TYPE_ID, MASKS, MULT, TARGET, GROUPS, ORIGINAL, DELETED, TRANSPORT_MASKS, MARGINALS, DISTINGUISHED, RANK3
    started = time.monotonic(); base.prepare_fast()
    complete = sorted({row[0] for root in base.c38._TYPE_ROWS for rows in root.values() for row in rows})
    TYPE_ID = {value:index for index,value in enumerate(complete)}
    MASKS = [sum(1 << owner for owner, signature in enumerate(value) if signature) for value in complete]
    moments._TYPE_ID = TYPE_ID; moments._TYPE_MASKS = MASKS
    raw=[]
    for point in reversed(range(base.c38._COVERAGE.shape[0])):
        value=tuple(sum(1 << offset for offset,digit in enumerate(base.c38._ALLOWED[coordinate]) if base.c38._COVERAGE[point,coordinate,digit]) for coordinate in range(13))
        raw.append(TYPE_ID[value])
    MULT=Counter(raw); GROUPS=defaultdict(list)
    for index,mask in enumerate(MASKS): GROUPS[mask].append(index)
    rows=json.loads((OUT/"deletion-classification.json").read_text())["unresolved"]
    TARGET={tuple(row["support_masks"]) for row in rows}
    with multiprocessing.Pool(3) as pool: coordinate_rows=pool.map(coordinate,reversed(range(13)),chunksize=1)
    # Restore owner indexing after reversed scheduling.
    coordinate_rows=list(reversed(coordinate_rows))
    ORIGINAL,DELETED,TRANSPORT_MASKS=relation_inputs(MASKS,coordinate_rows)
    prior=json.loads((ROOT/"discovery/out/cycle41-multiplied-ideal/zero-support-closure.json").read_text())
    MARGINALS=[{int(owner):Fraction(n,d) for owner,n,d in values} for values in prior["singleton_marginals_by_complete_type"]]
    DISTINGUISHED=[next(iter(values)) for values in MARGINALS]
    with multiprocessing.Pool(3) as pool: maps=pool.map(rank3_owner,reversed(range(13)),chunksize=1)
    rank3=defaultdict(int)
    for mapping in reversed(maps):
        for triple,deleted in mapping.items(): rank3[triple]|=deleted
    RANK3=dict(rank3)
    shards=[[],[],[]]; loads=[0,0,0]
    for row in sorted(rows,key=lambda value:value["type_triples"],reverse=True):
        target=min(range(3),key=lambda index:loads[index])
        shards[target].append(row); loads[target]+=row["type_triples"]
    with multiprocessing.Pool(3) as pool: outcomes=pool.map(classify,shards,chunksize=1)
    combined=Counter(); failures=[]
    for counts,rows_failed in outcomes: combined.update(counts); failures.extend(rows_failed)
    counts=dict(combined); failures=sorted(failures)
    expected=json.loads((OUT/"full-audit.json").read_text())
    expected_counts=dict(expected["counts"]); expected_counts["packet_moves"]=expected["packet_moves"]
    expected_failures=[row["types"] for row in expected["failures"]]
    diagnostic={
        "counts_equal":counts==expected_counts,
        "independent_failures":failures,
        "principal_failures":expected_failures,
        "only_independent":[row for row in failures if row not in expected_failures],
        "only_principal":[row for row in expected_failures if row not in failures],
        "rank3_residual_type_triples":len(RANK3),
    }
    (OUT/"independent-diagnostic.json").write_text(json.dumps(diagnostic,indent=2,sort_keys=True)+"\n")
    assert counts==expected_counts
    assert failures==expected_failures
    result={"status":"PASS","epistemic_status":"PROVED","stage":"INDEPENDENT_REVERSE_FULL_RESIDUAL_REPLAY","counts":counts,"failures":failures,"rank3_residual_type_triples":len(RANK3),"shard_type_triples":loads,"wall_seconds":time.monotonic()-started,"claim_boundary":"Independent reverse-order reconstruction of the complete 12,208,506-triple residual domain only; earlier universal layers are checked by their exact multiplicity identities."}
    (OUT/"independent-replay.json").write_text(json.dumps(result,indent=2,sort_keys=True)+"\n")
    print(json.dumps({key:result[key] for key in result if key not in ("failures","claim_boundary")},sort_keys=True))


if __name__=="__main__":
    multiprocessing.set_start_method("fork"); main()
