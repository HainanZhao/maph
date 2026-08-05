# Cycle 27: direct width-five time-weight LP boundary

## Claim boundary

`OBSERVED` only: for each of the 60 frozen Cycle-25 survivors, the specified
floating cutting-plane program reached full finite separation on its one
restriction-selected (5+4+4) coordinate partition and did not meet the
frozen strict-deficit/integerization rule.  This is not a lower bound for the
LP, an infeasibility theorem for that geometry, a width-five no-go theorem, or
a statement about (LRC(13)).

## Finite interface

For a frozen base and leaf, let (T) be the 199 raw times and let
(C_{i,a}\subseteq T) be the times covered by allowed digit (a) at
coordinate (i).  For a partition into blocks (B), and an option
(o\in\prod_{i\in B}A_i), write

\[
S_B(o)=\bigcup_{i\in B}C_{i,o_i}.
\]

The program used nonnegative raw-time weights and block bounds:

\[
\min\sum_B q_B,\qquad
\sum_{t\in T}w_t=1,\qquad
\sum_{t\in S_B(o)}w_t\le q_B
\quad(B,o).
\]

It starts from the first lexicographic option of every block and, after each
solve, exhaustively enumerates every option in every block to add the first
maximum violated row.  The enumeration is combinatorially complete for that
finite option set; the LP solve and comparisons are floating point, so the
result is observational rather than a certified inequality.

The selected partition rule orders coordinates by `(allowed-digit count,
coordinate index)`, takes consecutive groups of sizes (5,4,4), sorts within
and between blocks, and is frozen in the Cycle-27 preregistration.  In this
family it gives `0-1-2-3-4,5-6-7-8,9-10-11-12` for every target.

## Exact control and promotion rule

`PROVED` as a direct finite replay: the already sealed Cycle-22 integer
witness has (W=65528) and direct block capacity (U=65440) on its stated
source partition, with margin (88).  The identity is an exact integer
recalculation of the frozen witness; it does not validate a fresh LP optimum.

For a target, only an LP value strictly below (1-10^{-9}) could enter the
frozen denominator sequence (4096,65536,1048576,16777216).  Promotion would
then require an exact recomputation with positive support at most 256 and
(U<W).  No target entered this branch.

## Observed run outcome

The source run completed all 60 targets in 486.297737 seconds.  It recorded
21--69 separation rounds and 58--149 rows, with every row labelled
`UNRESOLVED`.  Printed objectives are within ordinary floating tolerance of
one (some print as `1.0000000000000009`); they are not exact values and must
not be reported as a proof that the optimum is at least one.

An independently written streamed separator/LP replay is required as a seal
input.  It must reproduce all 60 target identities, final objectives within
`1e-8`, separation-round counts, and cut counts.  Its agreement is an
independent implementation check of this bounded experiment, not a second
mathematical proof route.

## Falsifiers

Any mismatch in the frozen target order, selected partition, direct source
recovery, exhaustive option census, final separation data, or exact
integerization replay invalidates the affected statement.  A strict,
replayable integer (U<W) witness would supersede the all-unresolved outcome
for that target.
