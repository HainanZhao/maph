# Cycle 41: first multiplied ownership-ideal layer

## Claim boundary

`PROVED`: on p199 base 4 / leaf 78, there is a mass-one rational signed
degree-three ownership functional satisfying all Cycle 40 one-hot, totality,
marginal, lifted rank-one, rank-two, and rank-three constraints, together with
every Boolean-reduced product of one ownership literal and every rank-two
blocker.

This is not positive, not a global ownership distribution, not a functional
on the full ownership ideal, not a leaf certificate, and not LRC(13). It does
not include ownership-literal multiples of rank-three blockers or higher-degree
generator multiples.

## Boundary-filling translation

For three distinct times of complete types (s,t,u), put one vertex
((s,i)) for every rank-one-allowed owner (i), and similarly for (t,u).
Join vertices in different parts unless their common owner is a rank-two
blocker for that type pair. The allowed triangles are exactly the ownership
monomials not killed by a one-literal multiple of a rank-two blocker.

Orient every edge from the earlier to the later part and orient a triangle by
((s,t,u)). If its three (unsigned) pair marginals are
(M_{st},M_{su},M_{tu}), the associated chain is explicitly

\[
z=M_{st}-M_{su}+M_{tu}.
\]

At an (s)-vertex its boundary is the (s)-marginal of (M_{st}) minus
that of (M_{su}); at a (t)-vertex it is the (t)-marginal of (M_{st})
minus that of (M_{tu}), up to the common orientation sign; and similarly at
(u). All vanish because the three pair matrices have the same frozen
singleton marginals. Hence (z) is a cycle. A triple tensor has the prescribed
pair marginals precisely when its oriented triangle 2-chain has boundary
(z). The executable matrices use plus signs on all three pair blocks; negating
the entire ((s,u))-row block is the stated oriented matrix and does not change
rank or solvability. Rank-three blockers remove the specified diagonal
triangle cells. Thus the omitted Cycle 40 generator family is exactly a
chain-filling problem, not a positivity problem.

## Forced-zero closure and pair moments

An allowed pair cell ((s,i),(t,j)) has no triangle extension through type
(u) exactly when every owner in (A_u) equals (i) and is blocked against (s),
or equals (j) and is blocked against (t). Because only equal-owner diagonals
are forbidden, this can happen only when (|A_u|\le 2).

- If (A_u={a}), the multiplied equations force the corresponding entire
  pair row or column to zero, hence force singleton marginal (a_{s,a}) or
  (a_{t,a}) to zero.
- If (A_u={a,b}), they force precisely the cross cell ((a,b)) when the
  two rank-two diagonals cover the two mediator owners (and symmetrically for
  the opposite orientation).

`PROVED`: the complete 1,318-type closure has 17 singleton and 36 binary
mediator types. It forces 52 singleton owner deletions and off-diagonal zero
cells in 1,811 pair classes. Together with the 228,252 Cycle 40 rank-three-
induced pair diagonals, the exact component-balance system has 15,371
singleton variables, 1,405 deduplicated equations, and 58 disconnected pair
classes. Rational elimination is consistent and selects one allowed owner
with mass one for every type. Deterministic spanning-tree transport in each
allowed pair component therefore constructs exact signed pair matrices.
Same-type matrices are symmetrized.

This zero inference deliberately does not iterate by treating a newly zero
singleton or pair marginal as a smaller rank-one support. Such a marginal is
a signed sum: its individual triple cells may be nonzero and cancel. Declaring
those cells absent would impose a product with an additional literal, hence a
degree-four constraint not present in Cycle 41. The preceding singleton and
binary cases are complete for degree three because individual triple cells
are absent only from the original rank-one supports or an original rank-two
forbidden diagonal; a pair edge can lack every extension only when that
original mediator support is contained in the at-most-two forbidden owner
labels. Rank-three-induced pair zeros are retained as marginal equations but
likewise are not misused as new cell prohibitions.

## Complete small-support boundary

The realized owner-support sizes have a gap:

\[
1,2,3,4,5,6,9,10,11,12,13.
\]

Call a type small when its support has size at most six. The exact engine
checks every realized multiset of three complete types having at least two
small members, respecting the 2,786 raw-time multiplicities. There are
11,279,048 such type triples and 352,495 distinct support/deletion interfaces.

For each interface, the triangle-boundary rank is computed exactly over
(\mathbb F_2). If its first homology vanishes over (\mathbb F_2), its rational
boundary rank already equals the full rational cycle-space dimension, so every
compatible rational pair chain fills. The remaining 7,892 interfaces account
for 69,927 type triples. Their integer boundary matrices have 199,452 rows
and 125,358 allowed cells in aggregate. Exact rational row reduction produces
a complete left-null basis; all 1,808,327 basis evaluations on the constructed
pair chains are zero. Hence every small-boundary pair chain fills over
(\mathbb Q). Re-enumeration of all 19,661,454 frozen rank-three type tuples
finds no rank-three blocker class with two small supports.

## Dense-support theorem

It remains to consider a type triple with at most one small support. By the
support-size gap, two parts, say (A) and (B), have at least nine owners.
Discard pair-edge coordinates forced to zero because they have no triangle
extension; the singleton/binary closure above proves their pair moments are
zero.

Cover the remaining triangle complex by the closed stars (U_c) of vertices
(c\in C). Each (U_c) is a cone. For distinct (c_1,c_2), their intersection
is a bipartite graph on subsets of (A,B) obtained by removing at most two
owners from each side, with at most a matching of equal-label edges deleted.
Both sides have size at least seven, so this graph is nonempty and connected.
Every triple intersection similarly has sides of size at least six and is
nonempty. The homological nerve theorem in degree one therefore identifies
the first homology of the union with that of a nerve having a complete
2-skeleton. Both vanish. Here the needed degree-one nerve statement follows
directly from the Mayer--Vietoris/Čech double complex: contractible cover
members kill the total-complex terms in internal degree one, connected pair
intersections kill the internal-degree-zero obstruction on nerve edges, and
nonempty triple intersections supply every nerve 2-face. Consequently the
only possible total-degree-one group is (H_1) of that complete 2-skeleton,
which is zero. Thus every compatible dense-support rational pair cycle has a
triangle filling.

Rank-three diagonal zeros are imposed after this filling. If a diagonal cell
is already pair-forbidden, it is absent. If the third support is the singleton
({i}), the frozen induced condition (M_{AB}(i,i)=0) already forces its
coefficient to zero. Otherwise choose distinct alternate owners
(a\in A\setminus\{i\}), (b\in B\setminus\{i,a\}), and
(c\in C\setminus\{i\}) with (a,b,c) pairwise distinct. The eight-cell tensor

\[
(e_i-e_a)\otimes(e_i-e_b)\otimes(e_i-e_c)
\]

has zero pair marginals because summing in any one tensor factor gives zero.
It has coefficient one at ((i,i,i)) and no other all-equal coefficient because
(a,b,c) are pairwise distinct and distinct from (i). Every one of its eight
cells chooses in each position either (i) or that position's alternate. Equal
owners can therefore occur only as the pair ((i,i)), whose three pair
diagonals are allowed in the nontrivial case; all alternates are distinct.
Two supports of size at least nine allow (a) and (b) to avoid
({i,c}) and each other, while (|C|\ge2) supplies (c\ne i). Thus all eight cells
are allowed. Subtracting the needed multiple zeros that rank-three entry
without changing lower moments. Multiple blocked owners are corrected
independently because each correction has no other all-equal coefficient. If
type positions repeat, averaging over their stabilizer gives the required
symmetric tensor without changing any constraint. Complete coverage types
fix every owner support and deleted diagonal; permutations of raw times inside
one type therefore preserve every equation, which proves the quotient lift.

## Falsifiers

Any missing raw multiplier, incorrect Boolean reduction, unsupported pair
cell with nonzero moment, component imbalance, incomplete left-null basis,
nonzero exact relation evaluation, dense-star intersection failure, forbidden
octahedral cell, multiplicity mismatch, repeated-type asymmetry, or independent
replay disagreement invalidates the affected claim.
