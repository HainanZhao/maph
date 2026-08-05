# Cycle 28: portfolio-selected cyclic width-five LP boundary

## Claim boundary

`OBSERVED` only: the frozen four-witness selector chose a nonbaseline cyclic
((5+4+4)) coordinate partition for each of the 60 Cycle-25 survivors.  The
specified floating cutting-plane program then reached full finite separation
on every selected geometry without meeting the strict-deficit/integerization
rule.  This is not an exact LP lower bound, a no-go for the thirteen cyclic
partitions, a width-five obstruction, or a statement about (LRC(13)).

## Exact selector interface

For a frozen witness (j), target leaf, and candidate partition (P), the
selector computes the exact integer direct capacity (U_j(P)).  It minimizes

\[
  S(P)=\sum_{j=1}^{4}\frac{U_j(P)}{W_j}
\]

over the thirteen cyclic shifts of the baseline blocks of sizes (5,4,4),
using exact rational arithmetic and lexicographic partition text as the frozen
tie-break.  The source controls exactly replayed these four prior witnesses:

| Source | (W) | (U) | Margin |
|---|---:|---:|---:|
| Cycle 22, base 4 / leaf 952 | 65,528 | 65,440 | 88 |
| Cycle 21, base 4 / leaf 83 | 4,091 | 4,090 | 1 |
| Cycle 21, base 4 / leaf 104 | 65,539 | 65,448 | 91 |
| Cycle 21, base 3 / leaf 94 | 4,107 | 4,080 | 27 |

`PROVED` as finite integer replays: these four (W,U) identities follow by
complete direct option enumeration for the frozen source rows and source
partitions.  They do not prove that the selector is useful on another leaf.

## Target LP and promotion rule

For each selected target geometry, the LP is the direct raw-time formulation
from Cycle 27: nonnegative normalized time weights (w_t), one upper bound
(q_B) for every block, and every block-option coverage inequality.  Its
separator exhaustively searches the finite option set after each floating LP
solve and adds the lexicographically first maximum violated option.

Only an objective strictly below (1-10^{-9}) could enter the frozen
denominator sequence (4096,65536,1048576,16777216).  Promotion would require
positive support at most 256 and a fresh exact integer replay with (U<W).
No target entered that branch.

## Observed finite outcome

`OBSERVED`: all 60 targets selected a nonbaseline geometry.  Rotations
2, 3, 4, and 5 were selected 6, 20, 17, and 17 times respectively.  All 60
LP rows were labelled `UNRESOLVED`, using 20--117 separation rounds and
58--236 cuts.  Their printed floating objectives range from approximately
`0.9999999999999979` to `1.0000000000000018`; these are tolerance-level
observations, never exact lower bounds.

## Independent-audit containment

`OBSERVED`: a separately written full audit replayed the four source controls
and passed the comparison of all thirteen selector scores and ties for all 60
targets, then failed its LP-trace comparison.  A row-local continuation
persisted 35 exact objective/round/cut matches before identifying the first
discrepancy at base 3 / leaf 91:

| Route | Objective | Rounds | Cuts |
|---|---:|---:|---:|
| Primary, pinned one-thread environment | 1 | 28 | 80 |
| Independent, initially unpinned environment | 1 | 26 | 74 |

A targeted control set `OMP_NUM_THREADS=1` and `OPENBLAS_NUM_THREADS=1` before
importing NumPy and reproduced the primary `(1,28,80)` trace.  This classifies
the differing cut path as thread-environment-sensitive numerical behavior.
It does not erase the failed audit: 24 target traces remain independently
unconfirmed, and neither trace proves an exact lower bound.

## Falsifiers and scope

Any mismatch in a source extraction, exact source capacity, candidate census,
rational score or tie, target identity, selected partition, separation row,
objective tolerance, round count, or cut count invalidates the affected
trace statement. A replayable integer (U<W) witness supersedes the primary
all-unresolved observation for that target. This record is an
`OBSERVED` incomplete-audit containment boundary, not a validated closure of
the four-witness/thirteen-rotation family. It preserves the finite primary
outcome and the audit defect so the project can change engines without
overstating either.
