# Cycle 47 soundness boundary: raw and compressed affine descent

## Occurrence-labeled source system

Fix a finite collection of ordered type quadruples.  For an occurrence
(o=(Q,i)), deleting part (i) gives an ordered triple (T_o).  Let (W_o)
be the rational coordinate space on the owner triples allowed by the frozen
rank-one, rank-two, and rank-three deletions.  Its affine subspace (A_o) is
cut out by the three prescribed pair marginals.  Repeated type entries impose
the corresponding stabilizer equations.

For each quadruple (Q), let (Z_Q) be the rational coordinate space on its
allowed owner tetrahedra.  The raw system has variables

\[
 (x_o)_{o=(Q,i)}\quad\text{and}\quad (y_Q)_Q.
\]

It imposes (x_o\in A_o), the literal transport equalities between every two
occurrences of the same unordered labeled type triple, and

\[
 \partial y_Q=\sum_{i=0}^3(-1)^i x_{(Q,i)}.
\]

All signs come from the increasing part order.  No quotient or selected fill
is used in this definition.

## Canonical face coordinates

For an unordered type triple (T=(t_0\le t_1\le t_2)), let (W_T) be the
allowed owner-coordinate space in that order, fixed by the stabilizer

\[
 G_T=\{\sigma\in S_3:(t_{\sigma(0)},t_{\sigma(1)},t_{\sigma(2)})=T\}.
\]

If (o) is an occurrence of (T), choose a permutation from sorted type
positions to increasing part positions and let (P_o:W_T\to W_o) permute the
owner coordinates.  `PROVED`: (P_o) is independent of the chosen
permutation on (W_T^{G_T}), since two choices differ by an element of
(G_T).  The deletion rules and pair-marginal equations are equivariant under
this action, so (P_o) restricts to the corresponding affine face spaces.

## Descent equivalence

The compressed system has one variable (x_T\in A_T^{G_T}) for every
unordered face class and retains every (y_Q\in Z_Q).  In the boundary
equation for occurrence (o), substitute (P_o x_T).

`PROVED`: raw and compressed solutions are in bijection.  A compressed
solution maps to a raw one by (x_o=P_o x_T), and all literal gluing equations
then hold.  Conversely, choose any occurrence (o_T) of each face class and
put (x_T=P_{o_T}^{-1}x_{o_T}).  The raw stabilizer and gluing equations make
this independent of the occurrence and force every other occurrence to be
(P_o x_T).  The tetrahedral variables are unchanged in both directions, so
the four boundary equations commute with the correspondence.

This proof does not depend on connectivity between different face classes.
Connectivity and positive incidence-cycle rank instead ensure that the
principal finite test contains nontrivial gluing constraints.

## Exact certificate transport

Write the raw affine system as (A_r u=b_r).  Pivot each literal gluing
equation on its nonrepresentative occurrence coordinate, using exact rational
row operations, substitute it in the remaining rows, and then delete the
resulting pivot row and column.  Stabilizer pivots are treated identically.
The resulting matrix is the compressed system (A_c v=b_c) in its frozen
order.

`PROVED`: every step is an invertible affine row operation followed by removal
of a variable having a unique solved equality.  It preserves consistency and
gives explicit forward/back substitutions for solutions.  Applying the
inverse transposes of the recorded row operations transports a left-null
certificate and preserves its pairing with the right-hand side.  Thus an
exact nonzero affine pairing in either presentation is not created or erased
by compression.  The executable controls verify the gluing-pivot rank identity
and both forward and backward solution maps; matching ranks without these
maps is not accepted.

## Constructive fast path

A face rule depending only on the unordered labeled triple defines one
compressed face assignment before any quadruple is tested.  If its three pair
marginals and stabilizer equations hold, and an allowed tetrahedral chain
fills the resulting four-face cycle for every quadruple, the collected face
and tetrahedral coefficients are an explicit global section.  `PROVED`: this
direct verification solves the full affine system; Gaussian elimination is
unnecessary for a positive consistency result.  Each restriction also proves
that its local stalk is nonempty.

## Frozen connected-patch result

`PROVED`: the outcome-blind selector produced 256 p199 type quadruples, none
of which occurs in the Cycle 43/44 principal corpora.  Their bipartite
quadruple/face incidence graph is connected, has 185 face vertices, 887
incidence edges, 175 repeated face classes, maximum face degree 9, and cycle
rank 447.  Hence the gluing problem contains many incidence cycles and is not
a disjoint collection of local tests.

The canonical triple-face rule determined solely by the frozen lower pair
transports gives one exact rational face tensor on every one of the 185 face
classes.  `PROVED` by exact certificate replay, the resulting four-face cycle
has an allowed tetrahedral fill for every one of the 256 quadruples.  The
routes are 122 explicit distinguished-vertex cones, 133 localized incidence
fills, and one full exact elimination.  Witness supports have size at most
114 and all recorded coefficients have numerator and denominator bit length
at most 3.

The independent target-only replay reconstructs the relevant p199 rank-two,
rank-three, and mediated pair-transport data through a different preparation
route.  It checks all 185 face classes, all 1,024 raw occurrences, all 839
independent repeated-face identifications, every stabilizer and orientation,
and every one of the 256 local fills.  Seven outcome-blind material rows cover
every solver route, and no nonzero residual survives the full audit.  On the
frozen first 32 quadruples, the stabilizer-invariant raw occurrence coordinates have
56,466 variables, the compressed coordinates have 40,820 variables, and the
literal gluing block has exact rank 15,646, verifying

\[
 56,466-40,820=15,646.
\]

The explicit section transports and replays in both presentations.  Generic
controls also retain a three-stalk system whose local spaces are all nonempty
but whose global gluing has primitive dual ((1,1,1)) with affine pairing 1;
thus the implementation does not force every descent problem to succeed.

## Strategic interpretation

`PROVED` on the frozen patch, shared-face compatibility is not the missing
obstruction: a single outcome-independent canonical face rule already glues
across all 447 incidence cycles.  This is a substantive finite global-section
theorem, but it does not supply a new universal mechanism.  In particular,
the positive section reuses the lower-marginal canonical rule from Cycles
43--44; only the densely overlapping, entirely new patch and raw/compressed
descent theorem are new.  The next engine must therefore ask what arithmetic
or functorial constraint is absent from this affine sheaf, rather than enlarge
another finite local or shared-face census.

## Claim boundary

The raw/compressed equivalence above is generic finite-dimensional rational
linear algebra.  The finite computation proves only one exact section on its
frozen connected patch.  It does not prove
that every p199 type quadruple fills, that every connected patch has a
section, that the affine sheaf is acyclic, that a full degree-four functional
exists, or that LRC(13) holds.
