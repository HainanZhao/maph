# Cycle 46 soundness boundary: owner-star Čech injection

## Exact cover and total differential

Let (K) be a finite simplicial complex and (U_0,\ldots,U_{m-1}) a
finite family of subcomplexes.  For a nonempty index set (I), write
(U_I=\bigcap_{i\in I}U_i), and put

\[
 D_n=\bigoplus_{p+q=n}\ \bigoplus_{|I|=p+1} C_q(U_I;\mathbb Q).
\]

Orient both simplices and index sets increasingly.  On bidegree ((p,q))
use

\[
 d_D=(-1)^p d_{\rm simp}+d_{\rm Cech},
\]

where the horizontal differential deletes one index with its alternating
sign.  The two raw differentials commute, hence `PROVED`
(d_D^2=0).  The executable constructs both matrices and verifies this
identity on the generic controls.

For Cycle 46, fix a pivot part.  Its cover members are the closed stars of
*all* allowed vertices in that part.  No generated remainder is permitted.
Every tetrahedron belongs to the star of its pivot vertex, and so does every
face of that tetrahedron.  A residual is eligible for this cover only when
every nonzero cell belongs to at least one cover member.  The least eligible
pivot is selected before quotient membership is computed.

## Canonical horizontal contraction

For a cell \(\sigma\), let

\[
 S(\sigma)=\{i:\sigma\in U_i\}.
\]

When (S(\sigma)\ne\varnothing), the augmented horizontal complex over that
cell is the simplicial chain complex of the full simplex on (S(\sigma)).
Let (b(\sigma)=\min S(\sigma)).  Its standard cone contraction sends an
index simplex (I) not containing (b(\sigma)) to
((b(\sigma),I)), and sends a simplex already containing the base to zero.
On every augmented horizontal cycle (y), `PROVED`

\[
 d_{\rm Cech}H(y)=y.
\]

Let (zin C_n(K;\mathbb Q)) be a cycle supported in the cover union.
Assign each cell of (z) to its least cover member to obtain (x_0) in
bidegree ((0,n)).  Recursively define

\[
 x_{p+1}=H\bigl((-1)^{p+1}d_{\rm simp}x_p\bigr).
\]

The first contracted argument is horizontally augmented-zero because
(d z=0).  Inductively,

\[
 d_{\rm Cech}x_p=(-1)^p d_{\rm simp}x_{p-1}
\]

and commutation of the raw differentials makes the next contracted argument
a horizontal cycle.  Therefore the finite sum

\[
 L(z)=x_0+x_1+\cdots+x_n
\]

satisfies (d_D L(z)=0).  Its augmentation is exactly (z).  All choices
are deterministic and (L) is linear.

## Why compact elimination is exact

The augmented Čech complex of a finite cover is a resolution of the chain
complex of its union: cell by cell, its horizontal augmented row is the
contractible full simplex on (S(\sigma)).  Consequently augmentation
induces an isomorphism on homology.  In particular, `PROVED`, for a covered
cycle (z),

\[
 [L(z)]=0\text{ in }H_n(D)
 \quad\Longleftrightarrow\quad
 [z]=0\text{ in }H_n\!\left(\bigcup_i U_i\right).
\]

Every allowed tetrahedron lies in the owner-star union.  Hence its boundary
maps to a total boundary, and linearity gives

\[
 z=\sum_t c_t\,d t
 \quad\Longleftrightarrow\quad
 L(z)=\sum_t c_t\,L(d t).
\]

It is therefore theorem-equivalent—and much smaller—to solve the exact
sorted triangle-by-tetrahedron system first, then verify the same certificate
after applying (L).  This is not a numerical shortcut: every rational
coefficient is retained and both recombinations are checked exactly.  If the
compact system is inconsistent, its exact left-null vector annihilates every
tetrahedron boundary and pairs nontrivially with (z); augmentation transports
that obstruction to the injected quotient.

## Non-tautology controls

`PROVED` by exact replay:

- the boundary of a filled tetrahedron is covered and bounds in both the full
  total complex and the injected quotient;
- the boundary of an unfilled tetrahedron has a cell outside each single-owner
  pivot cover and is reported as uncovered, not silently repaired;
- the suspension of a four-edge bipartite cycle is covered by two owner stars
  but is nonboundary, and both the full total complex and the injected solver
  retain a nonzero exact dual.

Thus coverage alone does not force quotient vanishing, and the canonical
injection does not erase a covered homology class.

## Frozen p199 corpus result

`PROVED` by the primary exact execution and an independently written replay,
all 457 frozen Cycle 45 residuals are boundaries in their selected owner-star
unions.  The selection rule chose pivot part zero in every row.  The compact
triangle-by-tetrahedron system and the injected total-complex system agree
exactly on every row.

The primary execution classified 425 rows by local incidence elimination
(401 at radius one and 24 at radius two) and 32 by full exact elimination.
The resulting rational witnesses have between 6 and 178 nonzero
coefficients, occupy 96 distinct support sizes, and have coefficient bit
length at most 4.  The reconstructed corpus contains 876 target types, 2,536
pair candidates, 1,726 triple candidates, 2,382 deleted target pairs, and 15
deleted target triples.  These are exact finite-corpus statements, not
statistics about all p199 type quadruples.

The independent replay selected six rows outcome-blindly: the first, median,
and last row together with the least-witness representative of each of the
three solver classes.  It reconstructed allowed types, pair and triple
deletions, residual masks, and reversed-orientation boundary matrices without
calling the primary solver.  Reversed highest-pivot elimination filled all
six rows exactly.  Together with the generic filled-tetrahedron, uncovered-
sphere, and covered-nonboundary controls, this checks both the positive result
and the mechanism's ability to retain a real obstruction.

## Structural no-go

`PROVED`: for any covered cycle, the owner-star Čech lift is related to the
ordinary chain complex of the cover union by a chain resolution and homology
isomorphism.  Therefore quotient membership after this lift is neither a new
global closure relation nor a stronger degree-four test; it is a coordinate
reformulation of ordinary boundary membership.  The observed pivot-zero
coverage is likewise automatic for these four-partite tetrahedral boundaries,
because each tetrahedron and every one of its faces lie in the star of its
pivot vertex.

The Cycle 41 lower marginal relations cannot simply be added as degree-four
boundary columns: they live in a different graded interface.  Doing so without
a proved descent or compatibility map would invent relations and make the
test unsound.  A genuinely new engine must instead expose shared face
variables and prove that locally admissible fillings descend to one globally
compatible section, or produce a global cocycle obstructing such descent.

## Claim boundary

The generic chain construction, equivalence, 457-row boundary classification,
and stated coordinate-reformulation no-go are proved.  This does not establish
one globally compatible degree-four section, classify all p199 type
quadruples, certify a leaf, or prove LRC(13).  The local witnesses may disagree
on shared labeled faces; Cycle 46 deliberately does not identify those face
variables.
