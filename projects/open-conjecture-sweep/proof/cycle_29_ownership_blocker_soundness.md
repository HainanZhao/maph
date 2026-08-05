# Cycle 29: ownership-blocker semantic primal lift

## Claim boundary

The theorem below is `PROVED` for every finite direct-cover interface. The
complete synthetic and H11 computations are exact implementation controls.
The p199 census is an exact finite result for base 4 / leaf 78 only; it does
not exclude that leaf, close the other 59 survivors, or prove (LRC(13)).

## Ownership equivalence

Let (T) be a finite set of times. For each labeled coordinate (i), let
(A_i) be a nonempty finite digit set and (M_{i,d}\subseteq T) the times
covered by digit (d\in A_i).

`PROVED`: the following are equivalent.

1. There are digits (d_i\in A_i) with
   (T=\bigcup_i M_{i,d_i}).
2. There is a labeled disjoint partition (T=\bigsqcup_i O_i) such that for
   every (i), some (d\in A_i) satisfies (O_i\subseteq M_{i,d}).

For (1) to (2), assign every time to the least-index coordinate whose chosen
mask covers it. The resulting cells are disjoint, exhaustive, label-preserving,
and lie in their chosen masks. For (2) to (1), choose the least allowed digit
covering each cell. Every time belongs to its owner's chosen mask, so their
union is (T). These maps preserve full-cover feasibility and therefore its
negation, the exclusion status of the frozen direct interface.

## Blockers and the signature quotient

For one coordinate, call a cell legal if it lies in some allowed mask. A
blocker is an inclusion-minimal illegal cell.

`PROVED`: a cell is legal exactly when it contains no blocker. One direction
is immediate because subsets of a legal cell are legal. Conversely, every
illegal finite cell contains an inclusion-minimal illegal subset.

For each time define its digit-support signature

\[
D_t=\{d\in A_i:t\in M_{i,d}\}.
\]

A cell is legal exactly when
\(\bigcap_{t\in O_i}D_t\ne\varnothing\).
Consequently a blocker is exactly a minimal family of time signatures with
empty intersection.

`PROVED`: a blocker never contains two times with the same signature; removing
either would leave the intersection unchanged. Hence every minimal signature
pattern lifts to exactly the product of its signature-class sizes concrete
blockers. Conversely every concrete blocker projects to one such pattern.
This proves both completeness and the multiplicity formula used by the p199
census.

If a minimal empty-intersection family has (r) signatures, removing its
(j)-th member leaves a witness digit (x_j) in all other signatures but not
that member. The (x_j) are distinct, so `PROVED` (r\le |A_i|). This is the
frozen rank-14 safety bound, not the observed rank-three result.

## Exact controls and p199 outcome

`PROVED` by exhaustive finite replay: the implementation compares direct
assignments, all ownership labelings, canonical maps, local blockers, and the
signature quotient on all 65,536 two-coordinate/two-digit/four-time interfaces
and all 262,144 three-coordinate/two-digit/three-time interfaces. It also
checks all 64,000 H11 lifted assignments, finds 720 raw full covers whose maps
reconstruct exactly, partitions all 32,000 gcd-admissible assignments equally
among four parity signatures, and reproduces zero retained improper bases.

`PROVED` as a finite exact census for the named target: p199 base 4 / leaf 78
has 12,264 minimal signature patterns representing 190,867,444 concrete
blockers. The symbolic rank counts are 13, 9,311, and 2,940 at ranks 1, 2,
and 3; no higher-rank pattern occurs. The exact concrete counts are 4,844,
27,482,360, and 163,380,240. A same-divisor-color distinction survives:
coordinate 0 digits 0 and 4 both have color `(not divisible by 2, not divisible
by 7)`, but raw time 1 is covered by digit 0 and not digit 4.

This rank-three compression is a new structural interface, not yet a leaf
certificate. A later invariant must exploit the asymmetric singleton/pair/
triple coloring constraints rather than merely regenerate the original digit
choices.

## Falsifiers

Any mismatch in a map direction, coordinate label, direct feasibility,
minimality, signature class, exact multiplicity, H11 count, p199 target, raw
mask, or independent pattern census invalidates the affected statement. A
surviving rank-four pattern would refute the named p199 rank-three result but
not the general ownership theorem.
