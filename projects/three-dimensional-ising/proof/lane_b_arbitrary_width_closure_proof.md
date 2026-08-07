# Canonical spin-structure compression for grid strips

## Claim boundary

`PROVED`: for the explicit checkerboard ribbon embedding defined below, the
complete tensor of signed even-subgraph (equivalently, generalized
Kac--Ward square-root) values on

```
G_(n,w) = P_n square P_w square P_w,     n,w >= 2,
```

has an exact tensor-train representation of bond at most

```
d_w = 2^(w^2-1)
```

in a nested canonical handle ordering.  The bound applies both between
handle pairs and between the two binary coordinates of a handle.  It is an
identity over the polynomial ring in arbitrary edge weights.

`CONJECTURED`: the bound is generically tight for every `w`.  Exact finite
field witnesses currently prove tightness at `w=3`; the arbitrary-width
lower bound is not proved here.

The embedding is proved minimum-genus when all three grid parameters are
odd (equivalently `n,w` are even in the vertex convention), and at `w=3` by
the separately audited Millichap--Salinas theorem.  Minimum genus is not
claimed for the remaining parity cases.  Minimum genus is not used in the
compression proof.

The result removes the `2^(2g)` explicit spin-structure list.  It does not
compress the ordinary transverse carrier.  For `w=L` that carrier is still
`2^(L^2-1)`; no cubic free energy, critical point, or polynomial-time cubic
algorithm follows.

## 1. Graph, edge order, and the explicit surface

Put

```
V_(n,w) = {(i,y,z): 0<=i<n, 0<=y,z<w}.
```

Two vertices are adjacent when exactly one coordinate differs by one.  Edges
are unoriented and are ordered lexicographically by their ordered endpoints.
Slice `i` is the induced copy `Lambda_w={i} times P_w square P_w`; the nine in
the width-three case are not special in the construction.

For even `N,W`, take all unit cubes in
`[0,N-1] times [0,W-1]^2` whose lower corner has at least two even
coordinates.  Orient the boundary of their union.  At every grid vertex its
oriented boundary gives a cyclic order of incident grid edges.  For arbitrary
`n,w`, take `N` and `W` to be the least even integers not below `n,w`, and
delete from every cyclic order the neighbours outside `V_(n,w)`.  Capping the
boundary walks of this ribbon graph gives the closed orientable surface
`Sigma_(n,w)`.  This is exactly
`src.lane_b_universal_embedding.universal_checkerboard_rotation`.

Deletion of the terminal longitudinal slice only deletes neighbours from a
cyclic order.  Hence these embeddings are nested in `n`.

### Euler count

Let `p=floor((w-1)/2)`.  Directly following the checkerboard boundary walks,
or equivalently adding one longitudinal ribbon slab at a time, gives

```
g(n,2) = 0,
g(n,2p+1) = p^2 (n-1),
g(n,2p) = sum_(i=0)^(n-2) r_i,
r_i = (p-1)^2  if i is even,
      p^2-1    if i is odd.
```

The last line is the same as

```
g(n,2p)=1+(n(2p)(2p-2)-(2p)^2)/4
```

for even `n`, with an additional `p-1` for odd `n`.  The count follows from
Euler's formula after the following local boundary-walk classification.  At
an even-to-odd slab the disjoint odd/odd transverse squares are co-cores of
`(p-1)^2` new one-handles.  At an odd-to-even slab the `p^2` even/even
squares have one outer-boundary relation, leaving `p^2-1` one-handles.  For
odd width there is no outer-boundary relation and either colour supplies
`p^2` one-handles.  All other new boundary walks cap disks and do not change
genus.  These cases exhaust the parities of the new cube coordinates.

When `n,w` are even, every face is a quadrilateral.  The bipartite girth-four
Euler bound is therefore attained, so this embedding is minimum genus in
that case.  Other minimum-genus assertions are kept separate from the upper
factorization.

## 2. A canonical nested Lagrangian

Write `P_(i,y,z)` for the four-edge boundary of the transverse unit square
in slice `i` with lower corner `(i,y,z)`.  For the slab between slices `i`
and `i+1`, take the classes

```
[P_(i,y,z)],   y=z=i+1 (mod 2).
```

Here the congruence is applied separately to `y` and `z`.  If `w=2p` and
`i` is odd, omit the lexicographically last of the `p^2` classes.  Denote the
remaining ordered list by `A_i`.

The squares in one `A_i` are disjoint.  Lists belonging to different slabs
use different transverse slices.  They therefore have zero mod-two
intersection.  In the checkerboard cube body they are the boundaries of a
complete system of disjoint co-core disks: cutting the even-to-odd slab along
them removes `(p-1)^2` one-handles; cutting an odd-to-even even-width slab
removes `p^2-1`, because the sum of all `p^2` disks is the outer boundary;
and cutting an odd-width slab removes `p^2`.  The remainder is a collection
of balls joined along disks.  Thus the displayed classes are independent
apart from the one explicitly omitted relation.  Their total number is the
Euler genus `g(n,w)`, so their span `L` is a Lagrangian subspace of
`H_1(Sigma_(n,w);F_2)`.

Order these `a` cycles first by slab, then lexicographically inside a slab.
To construct their conjugates without a geometric guess, use the following
deterministic algebra.  In any pinned homology basis let `Omega` be the exact
intersection matrix and let the columns of `A` be the displayed Lagrangian
basis.  Solve

```
A^T Omega B = I.
```

Take the lexicographically least solutions with free bits zero.  Put
`C=B^T Omega B`, and let `U` be the strictly upper-triangular matrix whose
upper triangle equals that of `C`.  Replacing `B` by `B+A U` makes

```
A^T Omega B = I,    A^T Omega A=0,    B^T Omega B=0.
```

Interleave the columns as `(a_1,b_1,...,a_g,b_g)` to obtain `S_(n,w)`.
Consequently

```
S_(n,w)^T Omega S_(n,w) = J.
```

The construction preserves the old slab lists when a terminal slice is
added.  Hence it is nested.  The exact verifier uses the equivalent
filtration-adapted symplectic Gram--Schmidt and then the unique triangular
change to the same atomic `a` basis.

For `x=sum_i (x_i a_i+y_i b_i)`, define

```
q_lambda(x) = sum_i x_i y_i
              + sum_i lambda_(a_i) x_i
              + sum_i lambda_(b_i) y_i.
```

Then

```
q_lambda(x+x')=q_lambda(x)+q_lambda(x')+x^T J x',
Arf(q_lambda)=sum_i lambda_(a_i)lambda_(b_i).
```

These follow by expanding the displayed polynomial.  If a geometric
quadratic refinement is used as the affine origin, its correction is the
linear vector `q_geom(S e_j)` on the canonical generators; it must be added
to the displayed `lambda`.  The checkerboard convention used in the replay
has zero correction, but the formula, not that accident, is authoritative.

## 3. The separator lemma

Let a ribbon graph be split into left and right edge sets by a transverse
curve meeting the graph in a labelled set `B` of `k` points.  A partial even
subgraph has boundary mask

```
m in V(B)={m in F_2^B: |m|=0 mod 2}.
```

Fix, once and for all, a completion `c(m)` in a tree on the interface with
`partial c(m)=m`.  Closing a left or right partial subgraph with `c(m)` turns
it into a cycle.  Discrete Stokes,

```
<delta s,E'>=<s,partial E'>,
```

shows that changing a character representative by a coboundary changes a
partial weight only by a known sign depending on `m`.

Suppose the canonical handles are ordered as they are crossed by the curve.
At a cut in that ordering, every completed handle behind the curve has an
exact character representative on the right and every handle ahead has an
exact representative on the left.  The polarization term between the two
closures is supported in the interface collar and is therefore a fixed
function `kappa(m)`.  Hence, coefficient by coefficient in the edge weights,

```
F(lambda_L,lambda_R)
  = sum_(m in V(B)) X(lambda_L,m) (-1)^kappa(m) Y(m,lambda_R).   (1)
```

This proves `rank Flat_(L|R)(F) <= 2^(k-1)`.  Notice that (1) is about the
complete `F` tensor; no Arf sum has been taken.

For a cut between `lambda_(a_i)` and `lambda_(b_i)`, stop the curve halfway
through the corresponding one-handle.  The `b_i` character on the exposed
half is a coboundary.  Its phase is `<s_i,m>` and is a diagonal multiplier of
the same interface state.  The local polarization `a_i b_i` is assigned to
the half containing `a_i`, conditional on that known value.  Thus the same
factorization (1), with the same set `V(B)`, applies.  No extra binary state
is introduced.

This is the precise reason an arbitrary four-state-to-two-binary split would
give a spurious factor two, while the canonical geometric split does not.

## 4. Applying the separator lemma

The co-core disks in Section 2 are disjoint.  Starting with the plane between
two longitudinal slices, move it through a slab and around the co-cores in
their declared order.  Locally this replaces two intersection points on the
boundary of a checkerboard square by the other two; it neither creates nor
deletes a longitudinal strand.  At every regular position the curve meets
the grid in exactly `w^2` labelled points.  Immediately before, halfway
through, and immediately after every one-handle it has the exactness
properties in the separator lemma.  The halfway statement is the co-core
definition of `a_i`; the dual `b_i` is a longitude and restricts to the
coboundary of the side of the co-core exposed at the interface.

It follows at every pair and internal canonical cut that

```
rank Flat_(A|B)(F_(n,w)) <= |V_w| = 2^(w^2-1).       (2)
```

The first and last cuts use an empty partial graph and are smaller.  Free
longitudinal boundaries give the zero-mask boundary vectors.  A periodic
longitudinal closure replaces them by a trace over `V_w`; the same local
cores work, but (2) is asserted here only for the open-chain TT obtained by
cutting the periodic seam.  An antiperiodic seam multiplies the affected edge
weights by `-1` and does not change any rank argument.  Fixed-spin boundaries
must be gauge-transformed together with the edge characters.

## 5. Explicit all-spin-structure cores

Let `Gamma_0,...,Gamma_(2g)` be the successive separators just described,
including the half-handle separators.  Label every `V(Gamma_j)` by the fixed
set `V_w`, padding unused marked points by zero.  Let `E_j` be the edge block
between consecutive separators.  For its binary spin-structure coordinate
`epsilon_j`, define

```
A_j(epsilon_j)[m,m']
 = sum over S subset E_j,
       partial_left S=m, partial_right S=m'
   (-1)^(Q_j(S,m,m') + epsilon_j H_j(S,m,m'))
   product_(e in S) t_e.                              (3)
```

`H_j` is the corresponding canonical homology coordinate after closing by
the fixed interface trees; `Q_j` is the local part of `sum a_i b_i`, including
the interface correction `kappa`.  Both are explicit binary bilinear forms
obtained from the edge-label matrix `S_(n,w)^(-1) ell(e)` and the fixed
completion maps.  Formula (3) is therefore an exact polynomial-ring
definition, not a numerical decomposition.

With `ell=r=e_0`, repeated gluing gives

```
F_(n,w)(lambda_a1,lambda_b1,...,lambda_ag,lambda_bg)
 = ell^T A_1(lambda_a1) A_2(lambda_b1) ...
         A_(2g)(lambda_bg) r.                         (4)
```

Every matrix in (4) is `d_w` by `d_w`; zero rows and columns may be removed
at smaller boundary cuts.  Grouping consecutive binary cores gives the
four-state cores `A_i(a_i,b_i)`.  No Arf summation occurs in (4).

One value of `F` is obtained by fixing all physical indices.  Contracting
each pair with `(-1)^(lambda_ai lambda_bi)` performs the Arf-weighted sum.
Replacing a physical leg by a Walsh vector gives Fourier projection; summing
or fixing selected legs gives partial twist sums or fixed boundary twists.
The exponentially many entries cannot be explicitly printed in polynomial
time: (4) is a compressed representation of the function.

The checkerboard cores alternate with longitudinal parity for homogeneous
anisotropic weights.  For arbitrary nonuniform weights they remain exact but
do not repeat.

## 6. Complexity and tightness boundary

There are `2g=O(nw^2)` binary cores.  Dense storage uses
`O(g d_w^2)` polynomial entries and dense evaluation uses
`O(g d_w^3)` ring operations; the parity-toggle sparsity gives the usual
fixed-width transfer implementation with `O(n poly(w) d_w^2)` operations.
For fixed `w` all costs are linear in `n`.  For cubic boxes the bond remains
area-exponential.

`CERTIFIED_NUMERICAL`: the corrected width-three family reaches bond `256`,
so (2) is tight at `w=3` for generic nonuniform, homogeneous anisotropic, and
generic isotropic specializations.  Width-four small cases reach every
dimension allowed by their available spin-structure indices, but do not yet
reach `d_4=32768`.

`CONJECTURED`: for each fixed `w`, sufficiently large `n` gives generic
nonuniform rank `d_w`.  A proof requires a `d_w`-minor specialization or a
reachability/observability argument.  No homogeneous or critical-point
nonvanishing is inferred.

## 7. Coordinate firewall and the discarded construction

The verifier rejects a case unless the raw intersection form is alternating
and nondegenerate, the atomic change satisfies the exact symplectic
congruence, the quadratic polarization and Arf invariant are preserved, all
`b` restrictions to a transverse slice are coboundaries, the explicit
checkerboard meridians have rank `g` and zero mutual intersection, and the
same handle ordering is used at pair and internal cuts.

A deliberately retained failure illustrates why this is necessary.  At
`w=3,n=10`, applying the standard quadratic form directly to the pinned raw
coordinates gives an isotropic finite-field internal rank `512`.  After the
full raw-to-canonical transformation the same tensor has ranks
`256,256,256` at the central pair/internal/pair cuts.  The raw value is not a
topological obstruction; it is a noncanonical-coordinate artifact.

## 8. Novelty boundary

The generalized Kac--Ward formula supplies `2^(2g)` square roots and the Arf
sum, but does not itself give the all-spin-structure TT in (4).  Surface Arf
algorithms usually evaluate that sum sector by sector.  Bounded-pathwidth
Ising dynamic programming supplies the carrier `V_w`, but does not identify
why all canonical spin-structure phases fit into it, especially at an
internal handle cut.  Tensor-network gauge freedom explains changes by
coboundaries but not the checkerboard Lagrangian or its exact no-overhead
rank bound.

Accordingly, the potentially new statement is narrowly (2)--(4): for this
explicit nested surface family, genus growth contributes no bond dimension
beyond the ordinary parity frontier.  A publication-priority claim remains
subject to a full theorem-level literature audit.
