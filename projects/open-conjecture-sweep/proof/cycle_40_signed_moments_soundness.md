# Cycle 40: signed ownership moments through degree three

## Claim boundary

`PROVED`: for p199 base 4 / leaf 78 there is a mass-one rational signed
moment family through degree three which satisfies ownership totality and
one-hot reduction, is supported away from every lifted rank-one blocker,
has zero moment on every frozen rank-two blocker, and has zero moment on
every frozen rank-three blocker while retaining compatible lower marginals.

This is not a positive local distribution, a global ownership distribution,
a functional on the full ownership ideal, a leaf certificate, or LRC(13).
In particular, Cycle 40 does not impose arbitrary multiples of rank-two or
rank-three blocker generators.

## Pair transport

For a complete time type (s), let (A_s) be its allowed owner set after
removing rank-one blockers, and let (a_s) be a signed mass-one vector on
(A_s). For two types (s,t), form the bipartite graph on left (A_s) and right
(A_t), deleting edge ((i,i)) precisely when owner (i) has the corresponding
rank-two blocker.

`PROVED`: a signed matrix supported on this graph with row marginal (a_s)
and column marginal (a_t) exists if and only if each connected component has
equal left and right mass. Necessity follows by summing the two marginals in
a component. For sufficiency, choose a spanning tree in each component and
eliminate leaves: place a leaf's remaining marginal on its unique tree edge,
subtract it from the neighbor, and continue. Component balance makes the last
remainder zero. Signed coefficients remove every positivity obstruction.

The complete quotient has 1,318 types, 694,912 distinct pair classes after
all induced diagonal deletions, 7,497 graph classes, and 54 disconnected pair
classes. Its 1,426 deduplicated mass/component equations are rationally
consistent. The selected sparse solution assigns one allowed owner with mass
one to each type. Every pair transport therefore exists exactly.

## Triple completion

Given compatible pair moments, define

\[
T_0=M_{st}\otimes a_u+M_{su}\otimes a_t+M_{tu}\otimes a_s
      -2a_s\otimes a_t\otimes a_u.
\]

Direct summation shows that each of its three pair marginals is the prescribed
pair matrix. All corrections preserving those marginals lie in
(U_{A_s}\otimes U_{A_t}\otimes U_{A_u}), where (U_A) is the zero-sum space
supported on (A).

The diagonal restriction of this tensor kernel is surjective on the common
blocked owners except in two cases relevant here: one support is a singleton,
or all three supports are the same two-element set. This is checked by the
canonical difference bases frozen in the preregistration. Equivalently, the
diagonal evaluation functionals are independent when a support contains an
owner outside the common intersection; if all supports equal the intersection,
their cubic restrictions remain independent for intersection size at least
three. A singleton kills its diagonal direction, while three identical
two-point supports leave the single relation that the three pair diagonals
sum to one.

Among 693 realized support-mask triples, 36 initially have a singleton
exception. A rank-three blocker at singleton owner (i) forces the other
pair's ((i,i)) entry to zero, so the engine feeds this as an induced
rank-two deleted edge. There are 228,252 distinct induced pair deletion
classes, and the singleton/component system remains consistent after all of
them. No realized type triple has the exceptional common two-owner form.
Thus every triple blocker diagonal can be corrected to zero without changing
any pair marginal.

## Independent replay

The replay independently re-enumerates all 6,684,938 rank-two and 19,661,454
rank-three type tuples from the frozen Cycle 38 interface. It reconstructs
all deleted edges and graph components, substitutes every serialized rational
singleton marginal into every component balance, explicitly constructs
spanning-tree transports for the first, middle, and last pair classes, and
recomputes the 693 triple-mask classes. It agrees on all counts, the 36
initial exceptions, the 228,252 induced deletions, and zero unresolved or
binary exceptional triples.

## Falsifiers

Any mismatch in owner support, blocker rank, quotient type, deleted diagonal,
component balance, singleton mass, pair marginal, triple base marginal,
kernel classification, induced deletion, or independent reconstruction
invalidates the affected claim. A later failure of a multiplied blocker
relation does not contradict this theorem; it locates the next obstruction
beyond the unmultiplied degree-three interface.
