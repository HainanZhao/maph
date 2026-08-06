#!/usr/bin/env python3
"""
SAT generator for (n,k) Erdős–Szekeres-style constraints.

Key pieces:
  - One variable per unordered triple {i<j<k}, interpreted as χ(i,j,k)=+ for the sorted order.
  - Reduced AX5 (Knuth CC-style) implications, as in the original script: P(n,5)/3 clauses.
  - 14 selector variables per 4-set encoding the realizable cyclic triple-orientation patterns.
  - "No convex k-set" constraints via the 4-set convexity criterion: each k-set has at least one
    non-convex 4-subset (using the 8 non-convex patterns per 4-set).
  - Optional convex-layer (hull template) anchoring constraints with optional wedge anchoring via offsets.

This generator writes DIMACS CNF *streaming* (does not keep all clauses in memory).
"""

from __future__ import annotations

import argparse
import itertools
import math
from typing import Dict, Iterable, List, Optional, Tuple

# --- 4-set cyclic-triple patterns ---
# Order matters: last 8 are treated as NON-convex and are used in the k-set exclusion clauses.
CONVEX_PATTERNS = ["++++", "----", "++--", "--++", "-++-", "+--+"]
NONCONVEX_PATTERNS = ["+---", "-+++", "-+--", "+-++", "--+-", "++-+", "---+", "+++-"]
ALL_PATTERNS = CONVEX_PATTERNS + NONCONVEX_PATTERNS


def perm(n: int, r: int) -> int:
    """Return n*(n-1)*...*(n-r+1) for small r (no floats)."""
    out = 1
    for t in range(n, n - r, -1):
        out *= t
    return out


def parse_int_list(s: str) -> List[int]:
    """Parse a comma/space-separated list of integers: '5,5,5' or '5 5 5' or '5, 5 5'."""
    s = s.strip()
    if not s:
        return []
    parts: List[str] = []
    for chunk in s.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        parts.extend(chunk.split())
    return [int(p) for p in parts]


def build_triple_var_map(n: int) -> Dict[Tuple[int, int, int], int]:
    """
    Assign variable ids 1..C(n,3) to all unordered triples (i<j<k).

    The dictionary maps (i,j,k) with i<j<k to its variable id.
    """
    triple_var: Dict[Tuple[int, int, int], int] = {}
    vid = 1
    for i, j, k in itertools.combinations(range(n), 3):
        triple_var[(i, j, k)] = vid
        vid += 1
    return triple_var


def triple_lit(a: int, b: int, c: int, triple_var: Dict[Tuple[int, int, int], int]) -> int:
    """
    Return the signed literal representing χ(a,b,c)=+ in terms of the base variable for {a,b,c}.

    Convention:
      - For the sorted triple s=(i<j<k), variable x_s is True iff χ(i,j,k)=+.
      - For an ordered (a,b,c), χ(a,b,c)=+ is represented by:
          +x_s  if (a,b,c) is an even permutation of s (i.e., a cyclic rotation),
          -x_s  if (a,b,c) is an odd permutation of s.
    """
    s = tuple(sorted((a, b, c)))
    v = triple_var[s]

    # For 3 elements, even permutations are exactly the cyclic rotations.
    if (a, b, c) == s or (a, b, c) == (s[1], s[2], s[0]) or (a, b, c) == (s[2], s[0], s[1]):
        return v
    return -v


def reify_and(t: int, lits: List[int]) -> List[List[int]]:
    """
    CNF for t <-> AND(lits) using 1 + len(lits) clauses:
      (¬l1 ∨ ¬l2 ∨ ... ∨ t) ∧ ∧i (li ∨ ¬t).
    """
    assert lits, "reify_and expects at least one literal"
    clauses: List[List[int]] = []
    clauses.append([-lit for lit in lits] + [t])
    for lit in lits:
        clauses.append([lit, -t])
    return clauses


def geometric_4set_clauses(
    q: Tuple[int, int, int, int],
    t_start: int,
    triple_var: Dict[Tuple[int, int, int], int],
) -> Tuple[List[List[int]], List[int]]:
    """
    Generate the 71 CNF clauses for one 4-set q=(a<b<c<d) using 14 selector vars.

    - t_start is the "base id" for selectors: this function creates t_start+1..t_start+14.
    - Returns (clauses, t_ids).

    The 4 cyclic triples are:
      (a,b,c), (b,c,d), (c,d,a), (d,a,b).
    Each of the 14 realizable sign patterns gets a selector t_p <-> conjunction of the 4 literals.
    We also add one clause asserting at least one selector holds.
    """
    a, b, c, d = q
    base = [
        triple_lit(a, b, c, triple_var),
        triple_lit(b, c, d, triple_var),
        triple_lit(c, d, a, triple_var),
        triple_lit(d, a, b, triple_var),
    ]

    t_ids = list(range(t_start + 1, t_start + 15))
    clauses: List[List[int]] = []

    for idx, pat in enumerate(ALL_PATTERNS):
        t = t_ids[idx]
        conj: List[int] = []
        for lit, ch in zip(base, pat):
            conj.append(lit if ch == "+" else -lit)
        clauses.extend(reify_and(t, conj))

    clauses.append(t_ids[:])  # at least one realizable pattern
    assert len(clauses) == 71
    return clauses, t_ids


def ax5_clauses(n: int, triple_var: Dict[Tuple[int, int, int], int]) -> Iterable[List[int]]:
    """
    Yield the reduced AX5 clauses exactly as in your original nested-loop generator.

    For each generated ordered 5-tuple (p1,p2,p3,p4,p5), we emit one clause:
      ¬A1 ∨ ¬A2 ∨ ¬A3 ∨ ¬A4 ∨ ¬A5 ∨ C
    where
      A1 = (χ(p1,p2,p3)=+), A2 = (χ(p1,p2,p4)=+), A3 = (χ(p1,p2,p5)=+),
      A4 = (χ(p1,p3,p4)=+), A5 = (χ(p1,p4,p5)=+),
      C  = (χ(p1,p3,p5)=+).

    Each χ(...)=+ is represented by triple_lit(...).
    """
    rng = range(n)
    for p1 in rng:
        for p2 in rng:
            if p2 == p1:
                continue
            for p3 in rng:
                if p3 == p1 or p3 == p2:
                    continue

                # p4, p5 are ordered picks from {p3+1,...,n-1}, distinct, excluding p1,p2
                for p4 in range(p3 + 1, n):
                    if p4 == p1 or p4 == p2:
                        continue
                    for p5 in range(p3 + 1, n):
                        if p5 == p1 or p5 == p2 or p5 == p3 or p5 == p4:
                            continue

                        A1 = triple_lit(p1, p2, p3, triple_var)
                        A2 = triple_lit(p1, p2, p4, triple_var)
                        A3 = triple_lit(p1, p2, p5, triple_var)
                        A4 = triple_lit(p1, p3, p4, triple_var)
                        A5 = triple_lit(p1, p4, p5, triple_var)
                        C = triple_lit(p1, p3, p5, triple_var)

                        yield [-A1, -A2, -A3, -A4, -A5, C]


def hull_clauses(
    n: int,
    layers: List[int],
    offsets: List[int],
    triple_var: Dict[Tuple[int, int, int], int],
) -> Iterable[List[int]]:
    """
    Yield unit clauses for convex-layer anchoring (hull templates).

    layers[i] = size of layer i, starting at s_i = sum_{j<i} layers[j].
    offsets[i] = wedge offset within layer i:
      - offsets[0] is ignored (no previous layer to anchor against).
      - For i>=1:
          * offsets[i] == 0 disables the extra wedge anchoring at this layer.
          * offsets[i]  > 0 anchors w = s_i + offsets[i].

    IMPORTANT: This matches your paper statement: when w_i = 0, extra anchoring is omitted.
    """
    assert len(layers) == len(offsets)

    v = 0    # start index of current layer
    pv = 0   # start index of previous layer

    for i, k in enumerate(layers):
        # within-layer convexity
        for v1, v2, v3 in itertools.combinations(range(v, v + k), 3):
            yield [triple_lit(v1, v2, v3, triple_var)]

        # nesting: points beyond this layer lie inside each oriented edge of this layer
        for v1 in range(v, v + k - 1):
            v2 = v1 + 1
            for x in range(v + k, n):
                yield [triple_lit(v1, v2, x, triple_var)]

        # closing edge (v+k-1 -> v)
        if k > 0:
            v1 = v + k - 1
            v2 = v
            for x in range(v + k, n):
                yield [triple_lit(v1, v2, x, triple_var)]

        # optional wedge anchoring between previous layer pv and current layer i (paper-style)
        if i >= 1 and offsets[i] != 0:
            w = v + offsets[i]

            # all later points on one side of ray (pv -> v)
            for x in range(v + 1, n):
                yield [triple_lit(pv, v, x, triple_var)]

            # all later points (except w itself) on opposite side of ray (pv -> w)
            for x in range(v + 1, n):
                if x == w:
                    continue
                yield [-triple_lit(pv, w, x, triple_var)]

        pv = v
        v += k


def count_hull_clauses(n: int, layers: List[int], offsets: List[int]) -> int:
    """Count hull unit clauses without generating them."""
    assert len(layers) == len(offsets)
    v = 0
    cnt = 0
    for i, k in enumerate(layers):
        cnt += math.comb(k, 3)              # within-layer
        cnt += k * (n - (v + k))            # nesting along k edges
        if i >= 1 and offsets[i] != 0:
            cnt += (n - (v + 1))            # pv, v, x
            cnt += (n - (v + 1)) - 1        # pv, w, x (skip x==w)
        v += k
    return cnt


def write_dimacs(
    path: str,
    nvars: int,
    nclauses: int,
    clauses: Iterable[List[int]],
    comments: Optional[List[str]] = None,
) -> None:
    """
    Stream-write DIMACS CNF file.

    Also verifies that the number of written clauses matches the header count.
    """
    with open(path, "w", buffering=1 << 20) as f:
        if comments:
            for c in comments:
                f.write(f"c {c}\n")
        f.write(f"p cnf {nvars} {nclauses}\n")

        written = 0
        for cl in clauses:
            f.write(" ".join(map(str, cl)))
            f.write(" 0\n")
            written += 1

        if written != nclauses:
            raise RuntimeError(f"Clause count mismatch: header {nclauses}, wrote {written}")


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate DIMACS CNF for the (n,k) Erdős–Szekeres SAT encoding (streaming writer)."
    )
    ap.add_argument("--n", type=int, default=33, help="Number of points (default: 33)")
    ap.add_argument("--k", type=int, default=7, help="Forbidden convex k-gon size (default: 7)")

    ap.add_argument(
        "--layers",
        type=str,
        default="",
        help="Convex layer sizes, e.g. '5,5,5,5,5,5'. Empty disables hull constraints.",
    )
    ap.add_argument(
        "--offsets",
        type=str,
        default="",
        help="Layer offsets (same length as layers), e.g. '0,4,4,4,4,4'. "
             "If omitted, defaults to all zeros.",
    )

    ap.add_argument("--out", type=str, default=None, help="Output DIMACS path (.cnf)")
    ap.add_argument("--count-only", action="store_true", help="Print counts and exit")

    ap.add_argument("--no-ax5", action="store_true", help="Disable reduced AX5 clauses")
    ap.add_argument("--no-geo4", action="store_true", help="Disable 4-set selector encoding")
    ap.add_argument("--no-nocvx", action="store_true", help="Disable 'no convex k-set' clauses")
    ap.add_argument("--no-hull", action="store_true", help="Disable hull constraints even if layers are given")

    args = ap.parse_args()

    n = args.n
    k = args.k
    if n < 3:
        raise SystemExit("n must be >= 3")
    if k < 4:
        raise SystemExit("k must be >= 4 for the 4-set-based exclusion")
    if k > n:
        raise SystemExit("k must be <= n")

    layers = parse_int_list(args.layers)
    offsets = parse_int_list(args.offsets) if args.offsets.strip() else [0] * len(layers)

    if len(offsets) != len(layers):
        raise SystemExit("offsets must have the same length as layers (or be omitted).")

    if layers:
        if any(h < 3 for h in layers):
            raise SystemExit("Each layer size must be >= 3.")
        if sum(layers) > n:
            raise SystemExit(f"sum(layers)={sum(layers)} must be <= n={n}")
        # Validate offsets with your semantics: 0 disables; otherwise must be within layer
        for i, (h, off) in enumerate(zip(layers, offsets)):
            if i == 0:
                continue  # ignored
            if off == 0:
                continue
            if not (1 <= off < h):
                raise SystemExit(f"offset[{i}]={off} must satisfy 1 <= off < layer_size[{i}]={h}, or be 0.")

    # Variable count: triples + 14 selectors per 4-set
    nvars = math.comb(n, 3) + 14 * math.comb(n, 4)

    # Clause counts (must match what we will emit)
    ax5_cnt = 0 if args.no_ax5 else (perm(n, 5) // 3)
    geo4_cnt = 0 if args.no_geo4 else (71 * math.comb(n, 4))
    nocvx_cnt = 0 if args.no_nocvx else math.comb(n, k)
    hull_cnt = 0
    if (not args.no_hull) and layers:
        hull_cnt = count_hull_clauses(n, layers, offsets)

    nclauses = ax5_cnt + geo4_cnt + nocvx_cnt + hull_cnt

    # Default output name if not provided
    if args.out is None:
        if layers and (not args.no_hull):
            tag = f"{'-'.join(map(str, layers))}+{'-'.join(map(str, offsets))}"
        else:
            tag = "no-hull"
        out_path = f"es_{n}_{k}_{tag}.cnf"
    else:
        out_path = args.out

    print("=== configuration ===")
    print(f"n={n}  k={k}")
    print(f"layers={layers}")
    print(f"offsets={offsets}")
    print("--- counts ---")
    print(f"vars = {nvars}")
    print(f"clauses: ax5={ax5_cnt}  geo4={geo4_cnt}  nocvx={nocvx_cnt}  hull={hull_cnt}")
    print(f"total clauses = {nclauses}")
    print(f"out = {out_path}")

    if args.count_only:
        return

    triple_var = build_triple_var_map(n)
    base_triples = math.comb(n, 3)

    # Precompute non-convex selector ids for each 4-set (needed for k-set clauses)
    # Store as a tuple of 8 ints to make clause building fast.
    nonconvex_by_4set: Dict[Tuple[int, int, int, int], Tuple[int, ...]] = {}
    for idx, q in enumerate(itertools.combinations(range(n), 4)):
        t_start = base_triples + 14 * idx
        nonconvex_by_4set[q] = tuple(range(t_start + 7, t_start + 15))  # last 8 selectors

    def clause_stream() -> Iterable[List[int]]:
        # AX5 block
        if not args.no_ax5:
            yield from ax5_clauses(n, triple_var)

        # 4-set selector consistency block
        if not args.no_geo4:
            for idx, q in enumerate(itertools.combinations(range(n), 4)):
                t_start = base_triples + 14 * idx
                cls, _ = geometric_4set_clauses(q, t_start, triple_var)
                for cl in cls:
                    yield cl

        # k-set exclusion block (no convex k-set)
        if not args.no_nocvx:
            for K in itertools.combinations(range(n), k):
                clause: List[int] = []
                for Q in itertools.combinations(K, 4):
                    clause.extend(nonconvex_by_4set[Q])
                yield clause

        # Hull constraints (unit clauses)
        if (not args.no_hull) and layers:
            yield from hull_clauses(n, layers, offsets, triple_var)

    comments = [
        f"generated by es_sat_gen.py",
        f"n={n} k={k}",
        f"layers={layers} offsets={offsets}",
        f"vars={nvars} clauses={nclauses} (ax5={ax5_cnt}, geo4={geo4_cnt}, nocvx={nocvx_cnt}, hull={hull_cnt})",
        "NOTE: offsets[i]=0 disables wedge anchoring at layer i (paper semantics).",
    ]

    write_dimacs(out_path, nvars, nclauses, clause_stream(), comments=comments)
    print("done.")


if __name__ == "__main__":
    main()
