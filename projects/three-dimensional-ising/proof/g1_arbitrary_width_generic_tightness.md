# Generic arbitrary-width tightness from buffered one-sided encoders

## Claim boundary

`PROVED`, conditional only on the already proved canonical separator theorem
and its pinned checkerboard conventions.  For generic independent nonuniform
edge weights, the complete pre-Arf tensor of

```
G_(n,w)=P_n square P_w square P_w
```

has, already at `n=11`, a canonical pair flattening of generic nonuniform rank

```
d_w=2^(w^2-1).
```

Consequently

```
R_infinity(w)=2^(w^2-1)                              (1)
```

for generic independent edge weights and every `w>=3`.  Width three uses the
separately frozen paired-cycle certificate; Sections 1--8 prove every
`w>=4`.  “Generic” means a
nonempty Zariski-open set; because the certified minor is a nonzero real
polynomial, it is also nonzero on a nonempty open set of strictly positive
ferromagnetic weights.  No homogeneous anisotropic or isotropic lower bound
is asserted.

The proof does **not** glue the two encoder trees into one sparse subgraph.
That stronger construction is false, as Section 5 records.  Instead it proves
that the two polynomial factors at a canonical separator have full column
and row rank separately; their edge-variable sets are disjoint and the
intervening two-slab propagation has a nonzero diagonal specialization.

Width two is planar in this embedding and is not covered by (1).  No
homogeneous anisotropic or isotropic lower bound is asserted.

## 1. Notation and the two trees

Put `Gamma_w=G_(5,w)` and let

```
S_w={(4,y,z):0<=y,z<w}
```

be its terminal slice.  Write `e_x(x,y,z)`, `e_y(x,y,z)`, and `e_z(x,y,z)`
for the grid edge from `(x,y,z)` in the positive indicated direction.

The **gauge tree** is

```
T0_w = {all e_x}
       union {e_y(0,y,z):0<=y<w-1, 0<=z<w}
       union {e_z(0,0,z):0<=z<w-1}.                 (2)
```

It has `5w^2-1` edges and is a spanning tree: every vertex first moves in
the `x` direction to layer zero, then in `y` to row zero, then in `z` to the
root.  Gauge every homology cochain to vanish on `T0_w`.  Thus the label of a
chord is the homology class of its fundamental cycle relative to `T0_w`.

The **encoder tree** `T_w` is recursive.  Its width-four base is the frozen
79-edge list in the proof verifier.  Given `T_o`, embed it in width `o+1`
and add the `10o+5` shell edges in Table 1.  Here `r=0,1,2` and every range
is empty when its lower endpoint exceeds its upper endpoint.

| old width | added shell edges |
|:--|:--|
| even `o` | `e_x(r,o,z)` for `0<=z<=o`; `e_x(r,y,o)` for `0<=y<o`; `e_y(0,o-1,z)` for `0<=z<=o`; `e_y(0,0,o)`; `e_y(0,y,o)` for odd `y`; `e_z(0,y,o-1)` for even `2<=y<o`; `e_y(1,o-2,o)`; `e_x(3,o,o)` and `e_x(3,y,o)` for even `2<=y<o`; for even `0<=z<o`, the three edges `e_y(4,o-1,z),e_y(4,z,o),e_z(4,o,z)`; and `e_z(4,0,o-1)` |
| odd `o` | `e_x(r,o,z)` for `0<=z<=o`; `e_x(r,y,o)` for `0<=y<o`; `e_y(0,o-1,z)` for odd `3<=z<=o`; `e_y(0,y,o)` for `y=0,o-2` and even `2<=y<o`; `e_z(0,o,0)` and `e_z(0,o,z)` for odd `z`; `e_y(1,o-1,1)`; `e_z(1,y,o-1)` for odd `y`; `e_x(3,o,z)` for even `z` and for `z=o`, together with `e_x(3,0,o)`; for odd `z`, `e_y(4,o-1,z),e_y(4,z,o)`; and `e_z(4,y,o-1)` for odd `y` |

The entries in each row are disjoint and total `10o+5`, exactly the number
of new vertices.  Directly following the displayed rails and teeth connects
every new vertex to the old tree.  Hence no added edge closes a cycle and
`T_(o+1)` is a spanning tree.  This is the first finite parity check in
Table 3 below.

## 2. The common chord set

Let `k=floor(w/2)`.  Inside `T_w-T0_w`, define the exceptional set

```
X_w = {e_z(0,3,2)}
      union {e_z(0,y,0): y=5,7,...,2k-1}
      union {e_z(1,2a+1,2b):
             1<=a<=k-3, a+2<=b<=k-1}.             (3)
```

Set

```
P_w=(T_w-T0_w)-X_w.                                (4)
```

Widths `2k` and `2k+1` have the same old exceptional set.  Subtracting
(3) from Table 1 gives the much simpler nested recursion in Table 2.  It
adds exactly `2o+1` edges, so the width-four base `|P_4|=15` implies

```
|P_w|=w^2-1.                                       (5)
```

| old width | `P_(o+1)-P_o` |
|:--|:--|
| even `o` | `e_z(0,y,o-1)` for even `2<=y<o`; `e_y(1,o-2,o)`; at `x=4`: `e_z(4,0,o-1)`, `e_y(4,y,o)` for even `0<=y<o`, `e_y(4,o-1,z)` for even `0<=z<o`, and `e_z(4,o,z)` for even `0<=z<o` |
| odd `o` | `e_z(0,o,z)` for odd `z`; `e_z(1,1,o-1)`, `e_z(1,o-2,o-1)`, `e_y(1,o-1,1)`; at `x=4`: `e_z(4,y,o-1)` for odd `y`, `e_y(4,y,o)` for odd `y`, and `e_y(4,o-1,z)` for odd `z` |

All ranges in Table 2 lie in the new L-shaped transverse shell, apart from
the explicitly displayed `x=0,1` teeth.

## 3. Three combinatorial lemmas

Let `D_w` be the face-dual graph of the cellular checkerboard rotation of
`Gamma_w`.  The rotation is the restriction of the boundary of the union of
unit cubes whose lower corner has at least two even coordinates.  Consequently
all but one face are elementary boundary squares; the remaining face is the
outer walk.  Two faces are adjacent in `D_w` precisely across their common
grid edge.

### Lemma 1 (terminal cut basis)

Every component of `T_w-P_w` contains exactly one vertex of `S_w`.

**Proof.**  The width-four assertion is the frozen base check.  Since
`T_w-P_w` is a subgraph of a tree, it is a forest.  In the step `o -> o+1`,
substitute Tables 1--2 and contract every old component.  The new component
types are exactly those in the left half of Table 3.  Each listed component
contains its displayed old or new terminal anchor.  Their counts exhaust all
`(o+1)^2` terminals and all `5(2o+1)` new vertices.  Thus no anchor-free
component remains.  Induction proves the claim.  The entries are obtained by
following only the rails and teeth in Tables 1--2; no topological claim is
used in this check.  `QED`

### Lemma 2 (homology basis)

The dual graph

```
D_w - (T0_w union P_w)^*                            (6)
```

is connected.  Hence the fundamental-cycle homology labels
`{h_e:e in P_w}` are linearly independent.

**Proof.**  For a cellular embedding, the matrix with columns
`(partial e,h_e)` represents the cographic matroid of `D_w`: its kernel is
the span of face boundaries.  Since `T0_w` is a primal spanning tree,
independence of the chord set `P_w` is therefore equivalent to (6).

For the connectivity check, split the square faces at a width extension into
those common to the two restricted rotations and the changed/new faces.
Contract the connected components induced on the two classes.  Direct
substitution of the cube parity rule and Table 2 gives the right half of
Table 3.  The quotient has the displayed breadth-first layers, every vertex
outside layer zero has one displayed parent in the preceding layer, and the
edge count is one less than the vertex count.  It is therefore a tree.
Each induced component is connected by definition, so (6) follows.  The
width-four row is checked directly and the two parity rows prove the
induction.  `QED`

### Lemma 3 (exceptional modes do not mix)

```
span{h_e:e in P_w} intersection span{h_e:e in X_w} = {0}.       (7)
```

**Proof.**  Deleting `T0_w union X_w` from the dual and deleting
`T0_w union X_w union P_w` give the same component partition.  Its number
of components is `k=floor(w/2)`.  For `k>=3` the nonlarge components, in
the square notation of Table 3, are

```
I_3={(0;0,y,2):0<=y<=2},
I_5={(0;0,y,0):0<=y<=4},
I_(2,r)={(0;0,2r-1,0),(0;0,2r,0)},  3<=r<=k-1.     (8)
```

The remaining faces form the large component.  Thus the small component
sizes are `3,5` and `k-3` copies of `2`.  At `k=2`, only `I_3` and the large
component occur.  Formula (8) follows by applying the boundary-cube parity
rule along the `x=0` row: `e_z(0,3,2)` closes `I_3`, the first `z=0`
tooth closes `I_5`, and the subsequent odd-row teeth close the displayed
disjoint pairs.  The triangular `x=1` teeth lie inside the large component.
Substitution of Table 2 shows that every edge of `P_w` has both incident
faces in the same member of (8), or both in the large component.

For a chord set `A` relative to the primal tree `T0_w`, the homology rank is

```
rank h(A)=|A|-c(D_w-(T0_w union A)^*)+1.             (9)
```

Apply (9) to `X_w` and `P_w union X_w`, use Lemma 2 for `P_w`, and use the
equality of component partitions just proved.  The ranks add, which is
equivalent to (7).  `QED`

### Table 3: exhaustive shell checks

Write `o` for the old width and `W=o+1` for the new width.  A component size
in the primal columns counts new vertices only.  “Old 0” means an unchanged
old terminal component.

| case | components of `T_W-P_W` | quotient layers for (6) |
|:--|:--|:--|
| base `W=4` | 16 components, one per terminal | direct connected dual check |
| even `o>=6`, odd `W` | new anchors: `3o/2+1` of size 1, `o/2-1` of size 9, one of size 13; old anchors: `o-2` of size 4, one of size 8, all others old 0 | `1, 3W-4, W-1, W-1, 1` |
| exceptional `o=4,W=5` | new anchors: 7 of size 1, one of size 9, one of size 13; old anchors: two of size 4, one of size 8, all others old 0 | direct 22-vertex quotient tree |
| odd `o>=5`, even `W` | new anchors: `3(o-1)/2` of size 1, `(o-1)/2` of size 5, two of size 9, one of size 17; old anchors: `(o-3)/2` of size 4, `(o-5)/2` of size 8, all others old 0 | `1, 3W-6, W-2, W-2` |

For completeness, the dual parent families behind the last column are as
follows.  A square is denoted `(a;x,y,z)`, where `a` is its fixed coordinate
axis and `(x,y,z)` is its lower corner.

* If `W` is odd, layer one contains the unchanged bulk components and the
  two boundary families `(2;3,j,W-2)` and `(1;3,W-2,j)`, for even
  `0<=j<=W-3`.  Their new children are respectively
  `(0;0,j,W-2)` and `(0;1,W-2,j)`; the next children are
  `(2;1,j,W-2)` and `(1;1,W-2,j)`.  The distinguished `j=W-3`
  first arm has the sole layer-four child `(0;0,W-3,W-2)`.
  All other layer-one components are leaves at the outer component.
* If `W` is even, for odd `1<=j<=W-3` the old component
  `(1;0,W-2,j)` has child `(0;1,j,W-2)`, which has the two leaf
  children `(2;0,j,W-2)` and `(2;2,j,W-2)`.  The one old component
  containing `(0;0,0,W-3)` has the leaf children `(0;0,W-2,j)`.
  All remaining old components attach directly to the outer component.

The face adjacency in each sentence is across the unique transverse grid
edge shared by the two displayed boundary squares.  The checkerboard cube
condition decides which of the two incident squares belongs to the outer or
bulk component.  Thus these families are exhaustive by parity and provide
the promised parent in the preceding breadth-first layer.

## 4. Injectivity of the terminal map

Root `S_w` at `s_0=(4,0,0)`.  For every other terminal `s`, close the unique
`T_w` path from `s_0` to `s` by the `T0_w` path.  In the fundamental cycles
of `T0_w`, its homology is

```
c(s)=sum_(e in P_w) U(s,e) h_e
     +sum_(e in X_w) U(s,e) h_e.                   (10)
```

The matrix `U_P=(U(s,e))_(s,e in P_w)` is invertible.  Indeed, for a tree,
the column of an edge is the indicator of the terminal vertices on its
root-away side.  Such columns form a basis precisely when deletion of the
selected edges leaves one terminal per component, which is Lemma 1.

By Lemmas 2--3, choose `m=w^2-1` homology functionals that are dual to
`{h_e:e in P_w}` and annihilate `span h(X_w)`.  Applying them to (10) gives
exactly `U_P`.  Consequently

```
c: V(S_w) -> H_1(Sigma_(5,w);F_2)
```

is injective.

## 5. Falsified gluing step

We use the following slight extension of the lower-bound criterion.  It is
proved here because Cycle 10 stated the convenient special case in which the
reference completion tree lies on the separator.

### Invalid proposed Lemma 4 (side-completion lower bound)

The following statement is false without an additional global-compatibility
hypothesis.  At a canonical separator, let `c_L(m)` and `c_R(m)` be arbitrary fixed
linear completion chains contained in the left and right half graphs, with
boundary `m`; they need not lie on the separator itself.  Suppose a retained
left tree and a retained right tree have unique partial chains `p_L(m)` and
`p_R(m)`, and both maps

```
m -> [p_L(m)+c_L(m)] in H_L,
m -> [p_R(m)+c_R(m)] in H_R                         (11)
```

are injective.  Then the corresponding complete pre-Arf flattening has
generic rank `|V(S)|`.

**Invalid argument.**  Put `d(m)=c_L(m)+c_R(m)`.  It is a global cycle depending only
on `m`.  For the surviving configuration,

```
p_L(m)+p_R(m)
 = [p_L(m)+c_L(m)]+[p_R(m)+c_R(m)]+d(m).            (12)
```

The first two completed cycles lie in the filtration-adapted orthogonal
handle spaces `H_L` and `H_R`.  Every term involving `d(m)` in the quadratic
refinement or its polarization is a fixed mask-dependent phase, or a phase
depending on one side and `m`; absorb these into the corresponding side
factor.  Walsh transformation in the left spin coordinates turns the left
factor into a selected character table of the first map in (11), times
nonzero monomial and sign diagonals.  Injectivity makes it square and
invertible.  The last step is wrong: one global cochain gauge need not make
both side completions zero.  The projection of `d(m)` changes the actual
right character map and need not preserve injectivity; it is not merely a
harmless mask diagonal.

Take `G_(9,w)` and cut at its middle slice.  The left layers `0,...,4` and
the reflected right layers `4,...,8` each carry the preceding injective
tree, using the corresponding copy of `T0_w` for its side completion.  The
checkerboard handle ordering is slabwise; reflection across four slabs
preserves the parity convention.  Length-deletion compatibility identifies
the two prefix homology groups with the left and right canonical handle
blocks.  The final inference is false for the reflected right tree.  Exact
global-label checks give:

| `w` | target | left rank | reflected-right rank |
|---:|---:|---:|---:|
| 4 | 15 | 15 | 7 |
| 5 | 24 | 24 | 12 |
| 6 | 35 | 35 | 15 |

Set all edge variables outside the two trees and their fixed completions to
zero.  Because the right map is deficient, no full minor follows.  A valid
G1 proof requires an independently constructed right encoder in the same
global canonical labeling, or a different lower-bound mechanism.

The one-sided result alone makes no claim about the complete flattening rank.
The next sections use it only as a rank certificate for one factor of the
canonical separator decomposition; they do not reuse the invalid gluing.

## 6. The opposite-phase suffix encoder

Let `Gamma_w^-` be the five-layer ribbon graph obtained by restricting
`Sigma_(6,w)` to longitudinal layers `1,...,5` and translating these layers
to `0,...,4`.  It is the longitudinal reflection of the last five layers of
`Sigma_(11,w)`.  Its gauge tree is still (2).

There is a second recursive spanning tree `T_w^-`.  Its width-four base is
the 13-edge exchange of `T_4` frozen in
`discovery/audit_g1_opposite_explicit_all_width.py`.  In a width extension
`o -> o+1`, retain the old tree and add the following edges.  The notation
is that of Section 1; every displayed range is empty if its endpoints are
reversed.

First add, for `x=1,2`, every longitudinal edge on the new transverse
L-shell,

```
e_x(x,y,o), 0<=y<o;       e_x(x,o,z), 0<=z<=o.       (13)
```

For odd `o`, add

```
e_x(0,y,o), y!=1;                  e_x(0,o,z), all z;
e_x(3,y,o), y=0 or y odd;          e_x(3,o,0),e_x(3,o,o);
e_y(0,y,o), y even, y<o-1;         e_y(0,o-1,z), 2<=z<=o;
e_y(1,1,o),e_y(1,o-2,o);
e_y(4,y,o), y odd;                 e_y(4,o-1,z), z odd;
e_z(0,y,o-1), y odd;               e_z(0,o,0);
e_z(1,o,1);                        e_z(4,o,z), z odd.               (14)
```

For even `o>=6`, add

```
e_x(0,y,o), all y;                 e_x(0,o,z), all z;
e_x(3,o,z), z odd or z=o;
e_y(0,y,o), 0<=y<o-1;
e_y(0,o-1,z), z=0,1,2 or positive even z;
e_y(4,y,o), y even;                e_y(4,o-1,z), z even;
e_z(0,o,z), z=2,4,...,o-2;         e_z(1,0,o-1);
e_z(4,y,o-1), y even.                                      (15)
```

The `o=4` row replaces the three `x=3` positions by `z=1,2,4`, the
`x=4` shell positions by `z=0,3`, and uses `e_z(0,4,0)`.  Equations
(13)--(15) contain exactly `10o+5` edges, the number of new vertices.

Put

```
X_w^- = empty                                      if w is odd,
        {e_z(0,3,2)}                               if w=4,
        {e_z(0,w-1,0)}                             if w>=6 is even,
P_w^- = (T_w^- - T0_w) - X_w^-.                    (16)
```

### Lemma 4 (opposite encoder)

For every `w>=4`, `T_w^-` is a spanning tree and its terminal map

```
V(S_w) -> H_1(Gamma_w^-;F_2)                       (17)
```

is injective.

**Proof.**  The extension contains one parent edge for every new vertex and
no edge joining two already reached vertices.  Thus its `10o+5` edges attach
the new shell as a forest to `T_o^-`, proving the tree assertion.

There are exactly `w^2-1` edges in `P_w^-`.  Deleting them from `T_w^-`
leaves one terminal in every component.  Substitution of (13)--(16) gives
the following exhaustive component table.  A size counts vertices in the
new transverse shell; “old 0” is an unchanged old terminal component.

| new width | new terminal components | old terminal components |
|:--|:--|:--|
| odd `w=2k+1>=5` | `3k` of size 1, `k` of size 5, one of size `4w+1` | `k` of size 4, all other `(w-1)^2-k` old 0 |
| even `w=2k>=6` | `3(k-1)` of size 1, one of size 4, one of size 6, `k` of size 9 | `w-3` of size 4, all other `w^2-3w+4` old 0 |

The width-four base has new sizes `1,4,4,5,5,6,6`, one old size 4 and
eight old-0 components.  The counts in every row are `w^2`, and following
the rails in (13)--(15) assigns every vertex to the displayed unique
terminal.  Hence the terminal-cut matrix of `P_w^-` is invertible.

In the face dual, delete `(T0_w union P_w^-)^*`.  At `w=4` the remainder is
connected.  In an extension, contract separately the unchanged square-face
components and the changed/new-face components.  The quotient is a tree.
Its breadth-first layer sizes from the outer face are

```
w=5:              1,11;
w=6:              1,8,4,4,3;
odd w>=7:         1,2w-4,w-2,w-1;
even w>=8:        1,2w-5,w-2,w-2,3.                (18)
```

Every quotient edge is the unique undeleted transverse edge between the two
adjacent boundary squares specified by (13)--(15).  The layer totals equal
the number of contracted components, and every nonroot component has the
displayed parent in the preceding layer; hence no component is omitted.
Thus the dual remainder is connected.  The tree--cotree rank formula gives
linear independence of `{h_e:e in P_w^-}`.

For odd `w`, (16) has no exceptional edge, so the invertible terminal-cut
matrix and the independent homology columns prove (17).  For even `w>=6`,
the sole homology relation of the exceptional chord is

```
h_X = sum_(j=0)^(w/2-1) h_(e_y(4,2j,1)),             (19)
```

whereas its terminal-cut column, expressed in the `P_w^-` terminal-cut
basis, is the column of `e_z(1,w-1,1)`.  The latter edge is absent from the
sum in (19).  Thus the matrix-determinant-lemma scalar is zero over `F_2`,
and the rank-one update preserves determinant one.  At `w=4`, the relation
uses `e_y(4,0,1),e_y(4,2,1)` while the terminal column uses
`e_z(1,2,1),e_y(2,2,2)`; the supports are again disjoint.  These relations
are read from the unique dual cut created by deleting the exceptional edge
and from the unique tree cuts, respectively.  This proves (17).  `QED`

The tables and the rank-one update are replayed directly from the edge
formulas; no finite-width search is used in the statement of the lemma.

## 7. Buffered factor ranks

Fix `w>=4` and work in `G_(11,w)`.  Order the canonical handles slabwise as
in the arbitrary-width closure theorem and cut after the handles in slabs
`0,1,2,3`.  Their number is exactly

```
h_w=g(5,w).                                         (20)
```

At the corresponding canonical separator the all-spin-structure tensor has
the proved factorization

```
F(lambda_L,lambda_R)=X(lambda_L,m) D(m) Y(m,lambda_R),  m in V_w,       (21)
```

where `D` is a nonzero diagonal sign matrix and `|V_w|=d_w`.

### Lemma 5 (left reachability)

Over the fraction field of the independent edge weights, `X` has column
rank `d_w`.

**Proof.**  Retain the normal encoder `T_w` in layers `0,...,4` and set all
other left-edge variables to zero.  A tree contains a unique partial even
subgraph for each terminal mask.  By Section 4 its completed homology labels
are pairwise distinct.  Apply the Walsh transform in the first `h_w`
spin-structure coordinates.  The selected `d_w` rows form a character table
of these labels times a nonzero monomial diagonal.  It is invertible, so
`rank X=d_w`.  `QED`

### Lemma 6 (right observability)

Over the fraction field of the independent edge weights, `Y` has row rank
`d_w`.

**Proof.**  The last five layers `6,...,10`, after longitudinal reflection,
are `Gamma_w^-`.  The last four checkerboard slabs supply a symplectic
handle subsystem isomorphic to `H_1(Gamma_w^-;F_2)`.  This follows directly
from the slab co-core decomposition: adding these four slabs increases genus
by `g(5,w)`, their co-cores are disjoint from all earlier co-cores, and their
local longitudes give the conjugate subsystem.  Hence the inclusion is
symplectic and injective, and all its spin coordinates belong to
`lambda_R`.

Retain `T_w^-` in those last five layers.  Lemma 4 and a Walsh transform in
the corresponding suffix coordinates give a `d_w`-rank suffix factor at
the flat mask slice `x=6`.

It remains to propagate masks from the separator at `x=4` to `x=6`.  Fix
the spin coordinates of slabs 4 and 5.  Set every transverse edge in the
two-slab buffer to zero and retain both longitudinal edges

```
(4,y,z)(5,y,z), (5,y,z)(6,y,z)
```

with nonzero independent weights.  For each even mask `m`, the unique buffer
configuration uses both longitudinal edges exactly at the marked vertices.
The buffer transfer is therefore diagonal on `V_w`, with nonzero monomial
diagonal.  Multiplying the suffix factor by this invertible matrix preserves
row rank `d_w`.  Thus `rank Y=d_w`.  `QED`

## 8. Proof of G1

Choose a left inverse `L` of `X` and a right inverse `R` of `Y` over the
edge-weight fraction field.  From (20),

```
L F R = D.
```

Since `D` is invertible,

```
rank F >= d_w.                                     (22)
```

The arbitrary-width closure theorem gives `rank F<=d_w` at every canonical
cut.  Therefore the displayed cut of `G_(11,w)` has rank exactly `d_w` for
every `w>=4`.  The frozen width-three certificate supplies the same equality
at `w=3`.  Taking the supremum in longitudinal length proves (1).

All matrices have polynomial entries.  A full-rank minor over their fraction
field is a nonzero polynomial in the independent edge variables.  Its
nonvanishing locus is Zariski open.  Because a nonzero real polynomial cannot
vanish on the entire positive orthant, the equality also holds on a nonempty
open set of strictly positive ferromagnetic nonuniform weights.

This proves generic nonuniform G1.  It does not prove tightness after the
homogeneous anisotropic or isotropic restrictions, and it leaves the physical
area-exponential carrier `2^(w^2-1)` unchanged.
