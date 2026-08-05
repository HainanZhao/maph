# C72 generalized blocker theorem

## Claim boundary

`PROVED`: with the conventions below, every intersecting six-partite
six-uniform hypergraph (H) with (	au(H)=6) satisfies (D(H)ge 6).
This is a necessary-condition theorem.  It does not prove Ryser for (r=6),
classify the (D=6) case, justify a defect ladder, or establish novelty.

For an intersecting hypergraph put

\[
 D(H)=\sum_{\{e,f\}\subseteq E(H)} (|e\cap f|-1).
\]

## Structural reduction

Cycle 71 proves (D(H)ge5).  If equality held, its equality analysis and
the reduction in `cycle72_universal_blocker_reduction.md` give a vertex (v)
on six star lines and five witness lines.  Each witness contains one repeated
star vertex (r_j) on exactly two star lines.  Their union is an eleven-line
generalized equality core (C), and (D(C)=D(H)=5).

Every other line of (H) meets every core line exactly once: intersection
gives at least one point, while any excess would contribute positively to
(D(H)-D(C)).  Its old core vertices therefore form one of the compatible
extension traces enumerated below.  Hence a set of at most five core vertices
meeting the eleven core lines and every compatible trace is a transversal of
all of (H), contradicting (	au(H)=6).

It remains only to prove that every generalized equality core has such a
blocker.

## Complete finite theorem

`PROVED`: every generalized rooted (D=5) equality core has a fixed set of at
most five core vertices meeting its eleven core lines and every individually
compatible extension trace.

Repeated vertices occupying one noncentral part have pairwise-disjoint
two-subsets of the six star indices.  Three such vertices would occupy all six
indices.  A witness whose own repeated vertex lies in another part would then
be forced to use a repeated vertex in this part, creating a second excess
star contact and violating the equality structure.  Thus every side
multiplicity is at most two.  The only side shapes are
(1+1+1+1+1), (2+1+1+1), and (2+2+1).  Witness and noncentral-part
relabeling reduces each shape to one representative, as proved in
`cycle72_side_shape_reduction.md`.

For each representative, the exact enumeration ranges over all 52 central
restricted-growth strings, all (15^5) star-pair tuples, and every compatible
map tuple.  Each domain has (52\cdot15^5=39{,}487{,}500) outer cases.  The
numbers of realized cores are respectively

- (20{,}383{,}920) for (1+1+1+1+1);
- (4{,}013{,}280) for (2+1+1+1);
- (1{,}831{,}680) for (2+2+1).

The total is (26{,}228{,}880).  The maximum numbers of compatible traces are
18, 6, and 5.  No core lacks a blocker of size at most five.

Two independent exhaustive implementations establish this finite statement.
The primary engine represents core lines as vertex bitsets, enumerates traces
by part recursion, and uses a memoized uncovered-line blocker search.  The
independent engine represents vertices by 11-bit line-incidence signatures,
enumerates traces as exact signature partitions, and uses memo-free
iterative-deepening branch and bound.  For every shape they agree on the full
outer-case count, realized-core count, maximum trace count, and two
order-independent 64-bit accumulators over canonical core-plus-trace
signatures.  The independent checker rejects any mismatch.

## Falsifiers

A legal reconstructed core whose core-line/trace family has transversal
number at least six falsifies the finite theorem.  A domain-count or canonical
hash mismatch falsifies the computational closure.  An intersecting
six-partite six-uniform (H) with (	au(H)=6) and (D(H)\le5) falsifies the
final theorem.
