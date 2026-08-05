#!/usr/bin/env python3
"""Deterministic coherent orientation packet for C77 (not a proof)."""

from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
import heapq
import json

import numpy as np

from cycle77_spin_packet import alignment_operator, target_operator


MASK = (1 << 64) - 1
SEEDS = (0x9E3779B97F4A7C15, 0xD1B54A32D192ED03, 0x94D049BB133111EB)
Q_NUMERATORS = tuple(range(33, 64))
EPS = 1e-8


def xorshift64(state: int) -> int:
    state ^= (state << 13) & MASK
    state ^= state >> 7
    state ^= (state << 17) & MASK
    return state & MASK


def vectors(seed: int, count: int):
    state = seed
    for _ in range(count):
        entries = []
        for _ in range(8):
            state = xorshift64(state)
            real = int(state % 7) - 3
            state = xorshift64(state)
            imag = int(state % 7) - 3
            entries.append(complex(real, imag))
        if not any(entries):
            entries[0] = 1.0
        yield entries


def marginals(entries):
    vec = np.asarray(entries, dtype=np.complex128)
    rho = np.outer(vec, vec.conj()) / float(np.vdot(vec, vec).real)
    tensor = rho.reshape((2,) * 6)
    return (np.trace(tensor, axis1=2, axis2=5),
            np.trace(tensor, axis1=1, axis2=4),
            np.trace(tensor, axis1=0, axis2=3))


def worker(shard: int, count: int):
    targets = {a: np.cumsum(np.linalg.eigvalsh(target_operator(a / 64.0))[::-1])
               for a in Q_NUMERATORS}
    heap = []
    hits = 0
    rows = 0
    for entries in vectors(SEEDS[shard], count):
        state_marginals = marginals(entries)
        for a in Q_NUMERATORS:
            spectrum = np.linalg.eigvalsh(
                alignment_operator(*state_marginals, a / 64.0)
            )[::-1]
            for k, excess in enumerate(np.cumsum(spectrum)[:-1] - targets[a][:-1], 1):
                rows += 1
                if excess <= EPS:
                    continue
                hits += 1
                row = (float(excess), a, k,
                       [[int(z.real), int(z.imag)] for z in entries])
                if len(heap) < 32:
                    heapq.heappush(heap, row)
                elif row[0] > heap[0][0]:
                    heapq.heapreplace(heap, row)
    return {"shard": shard, "states": count, "ky_fan_rows": rows,
            "recognized_hits": hits, "top": sorted(heap, reverse=True)}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--samples-per-worker", type=int, default=8192)
    args = parser.parse_args()
    with ProcessPoolExecutor(max_workers=3) as pool:
        futures = [pool.submit(worker, shard, args.samples_per_worker)
                   for shard in range(3)]
        rows = [future.result() for future in futures]
    top = []
    for row in rows:
        top.extend(row.pop("top"))
    top.sort(reverse=True)
    print(json.dumps({"claim_tag": "OBSERVED", "samples_per_worker": args.samples_per_worker,
                      "q_numerators": list(Q_NUMERATORS), "shards": rows,
                      "top_candidates": [
                          {"recognized_excess": value, "q_numerator": q, "k": k,
                           "entries": entries}
                          for value, q, k, entries in top[:32]
                      ]}, sort_keys=True))


if __name__ == "__main__":
    main()
