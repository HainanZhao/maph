# Exact encoding notes for C(23,6,2)

Claim boundary: this note proves equivalence between existence of a 20-block
cover and satisfiability of `cover_23_6_2_sat.py`'s CNF. It does not decide
the CNF. A solver's UNSAT line is not proof without independent certificate
checking.

## Necessary replication structure

`PROVED`: Let `r_v` be the number of blocks containing point `v`. Each such
block covers at most five of the 22 pairs incident with `v`, hence `r_v >= 5`.
Since 20 blocks of size six have 120 point incidences,

```text
sum_v r_v = 120 = 23*5 + 5.
```

Consequently at most five points have replication greater than five, and at
least eighteen have replication exactly five.

Choose a replication-five point and call it 0. Its five incident blocks have
25 nonzero-point slots. Coverage of the 22 pairs `{0,v}` forces all other 22
points to occur in those slots, leaving exactly three repeated incidences.

## Symmetry choices

`PROVED`: Relabel one block through point 0 as block 0 and its other points as
1 through 5. The remaining points are 6 through 22. At least twelve of these
17 outside points have replication five. At most three outside points repeat
in the five-block star at 0, so at least

```text
17 - 5 - 3 = 9
```

outside points are simultaneously replication-five and occur exactly once in
that star. Relabel nine of them 6 through 14 and three further
replication-five outside points 15 through 17.

Within each resulting interchangeable point class, columns may be sorted
lexicographically. Blocks may independently be sorted lexicographically.
After block sorting, the five blocks containing point 0 occur first. Block 0
remains first because it contains all of points 1 through 5, while every
distinct competing block through 0 omits at least one of them. Thus all unit,
degree, star, row-order, and column-order constraints in the CNF are jointly
without loss of generality.

## CNF semantics

`PROVED`: Variable `x[b][v]` says that block `b` contains point `v`. The two
Sinz counters on each row impose exactly six true entries. For each block and
point pair, `y[b,u,v]` is constrained in both directions to equal
`x[b][u] AND x[b][v]`; the long clause over the twenty corresponding `y`
variables therefore says that pair `{u,v}` is covered.

Every satisfying assignment consequently decodes to twenty six-subsets that
cover all 253 pairs. Conversely, the symmetry argument above maps every
20-block covering to a satisfying assignment. The model checker ignores all
auxiliary variables and directly recounts the 253 pairs.

## Independent decision requirements

- `SAT`: decode the twenty blocks and pass the direct pair counter.
- `UNSAT`: retain the exact DIMACS file and CaDiCaL proof, then verify the
  proof with the pinned independent `drat-trim` executable.
- Any interrupted run, resource limit, or unchecked solver decision remains
  `OBSERVED` and does not determine the covering number.
