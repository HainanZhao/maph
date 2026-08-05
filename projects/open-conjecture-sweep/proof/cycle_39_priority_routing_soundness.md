# Cycle 39: full priority-section routing obstruction

## Claim boundary

`PROVED`: on p199 base 4 / leaf 78, no mass-one signed linear
combination of the 53,248 deterministic priority/fallback ownership sections
annihilates every unmultiplied Cycle 29 ownership/blocker generator. Rank-two
blockers already prove the obstruction.

This does not constrain arbitrary pair-correlated or nonlocal ownership
routing, generator multiples, the full ownership ideal, the leaf, or
(LRC(13)).

## Complete priority-section basis

Fix a fallback coordinate (r). A deterministic priority order assigns a
covered time to its first covering coordinate and an uncovered time to (r).
For the event that (r) owns a time, only the subset (P) of the other twelve
coordinates preceding (r) matters; the order within (P) and after (r)
does not. Conversely every (P\subseteq[13]\setminus\{r\}) is realized by a
priority order.

`PROVED`: the (2^{12}=4096) predecessor subsets give the complete moment
basis of all priority orders with fallback (r). Across thirteen fallbacks
there are 53,248 labeled sections. Every section satisfies ownership totality
and exclusivity pointwise. A blocker at (i\ne r) vanishes pointwise because
ownership by (i) implies coverage by its one selected digit. Hence the
blocker matrix is block diagonal by fallback.

## Exact moment transform

Let (C_{t,j}) indicate that coordinate (j)'s selected digit covers (t),
and let (F_t) indicate global noncoverage. The root-ownership indicator is

\[
R_t(P)=F_t+C_{t,r}\prod_{j\in P}(1-C_{t,j}).
\]

The summands are disjoint. For a root blocker (B), expand
(prod_{t\in B}R_t(P)) by the subset (S\subseteq B) routed to the fallback
because it is globally uncovered. The root digit must miss (S) and cover
(B\setminus S); coordinates in (P) must miss all of (B); coordinates
outside (P\cup\{r\}) must miss (S). `PROVED`: product-measure
factorization gives the exact integer moment used by the engine.

Cycle 38's empty-predecessor column is reproduced exactly. Complete synthetic
controls prove predecessor-subset equivalence, and the complete labeled global
coverage types preserve every local contraction and exact multiplicity.

## CEGAR and certificates

For each fallback block, the exact engine starts with its Cycle 38 violated
pair, solves the selected affine equations, and returns the first nonzero
rank-one/rank-two type tuple under complete lexicographic separation. Each
added row is independent of the previous selected equations because the exact
candidate satisfies every previous row and violates the new one. All thirteen
blocks become inconsistent at rank two. The selected-row counts are

\[
(1,134,1,1,78,1,102,20,1,231,1,1,1),
\]

for 573 rows total.

Each block stores an integer left-null vector for its mass row plus selected
blocker rows. Its mass coefficient is respectively

\[
(150,4500,1,1,3,5,75,3,25,150,20,4,1),
\]

and is nonzero. `PROVED`: every certificate annihilates all 4,096 predecessor
columns, while its product with the affine right side is the nonzero mass
coefficient. Therefore a blocker-annihilating combination in each fallback
block has mass zero. Block diagonality then forces every global combination
annihilating all blockers to have mass zero, ruling out mass one.

## Independent replay

The independent replay reconstructs all 573 moment rows and substitutes every
integer certificate into all 53,248 labeled section columns. It also selects
the first, middle, and last row of every block and rebuilds the entire 4,096-
column row by direct enumeration of the Cycle 37 signed support followed by an
independent subset transform. All 331,338 direct support-assignment checks
agree. The largest certificate coefficient uses 13 bits.

## Falsifiers

Any priority/predecessor mismatch, off-fallback nonzero event, coverage label,
complete type, multiplicity, local contraction, CEGAR row, direct support row,
or nonzero certificate-column product invalidates the affected statement.
The theorem does not imply that a pair-correlated routing functional is
impossible.
