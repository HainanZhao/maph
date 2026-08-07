# An abstract separator theorem for pre-Arf Ising tensors

## Status and scope

`PROVED`: Theorem 1 below is an algebraic gluing theorem for any finite
zero-field Ising even-subgraph model satisfying the stated filtration and
quadratic-phase hypotheses.  It does not assume a grid, minimum genus, or
translation invariance.

`PROVED`: The checkerboard grid-strip theorem is a corollary with separator
size `w^2`.

`PROVED`: Iterated toroidal two-sums of cellular `K_(3,3)` gadgets give a
non-grid, unbounded-genus corollary with four-state handle-site bond at most
two and binary-coordinate bond at most four.  This family also shows why H3
is essential: middle internal cuts attain four even though pair cuts have
rank two.

Generic minimality is not part of Theorem 1.  Theorem 2 gives a sufficient
lower-bound criterion used by the G1 campaign.

## 1. Algebraic setup

Let `G=(V,E)` be a finite graph cellularly embedded in a closed orientable
surface `Sigma`.  Work over a commutative integral domain `R` containing the
independent edge variables `t_e`.  Let

```
Z_1(G)={A in F_2^E: partial A=0}
```

and let `pi:Z_1(G)->H=H_1(Sigma;F_2)` be the homology map.  Fix a symplectic
basis `(a_1,b_1,...,a_g,b_g)` and put

```
q_lambda(x,y)=sum_i x_i y_i+lambda_a dot x+lambda_b dot y.
```

The complete pre-Arf tensor is

```
F(lambda)=sum_(A in Z_1(G)) (-1)^q_lambda(pi A) product_(e in A)t_e.   (1)
```

No Arf-weighted sum is performed in (1).

A cut datum consists of an edge partition `E=E_L disjoint-union E_R`, an
interface set `S`, and boundary maps

```
partial_L:F_2^E_L -> F_2^S,
partial_R:F_2^E_R -> F_2^S
```

such that `A_L+A_R` is even precisely when
`partial_L A_L=partial_R A_R=m`.  Since every edge has two endpoints, all
attainable masks lie in

```
V(S)={m in F_2^S: sum_s m_s=0},    |V(S)|=2^(|S|-1)                 (2)
```

when the interface is connected.  With `c_L(m),c_R(m)` fixed linear
completion chains, denote the completed homology classes by
`h_L(A_L,m)` and `h_R(A_R,m)`.

## 2. Filtration-adapted spin structures

For a cut of the ordered spin coordinates into `lambda_L|lambda_R`, require:

**H1 — support/exactness.**  Every linear character belonging to
`lambda_L`, when restricted to right partial chains, is a coboundary plus a
fixed function of `m`; every character belonging to `lambda_R` has the
left-right reversed property.  Intrinsically, the corresponding restricted
classes vanish in relative `H^1` after quotienting the interface trace.

Precisely, put

```
P_R={c in C_1(E_R;F_2): support(partial c) subset S},
tau_R(c)=partial c|S,
```

and define `P_L,tau_L` similarly.  For a character cochain `alpha`, the
right-exact assertion means that there are a zero-cochain `s` on the right
subgraph and a linear functional `phi` on `im(tau_R)` such that

```
<alpha,c>=<delta s,c>+phi(tau_R(c))
         =<s,tau_R(c)>+phi(tau_R(c))
```

for every `c in P_R`.  Thus it is an equality of functionals on the relative
chain space, independent of a chosen representative.  Left-exactness is the
same statement with `L` and `R` exchanged.

**H2 — quadratic gluing.**  There are binary functions `Q_L,Q_R,kappa` such
that, for every compatible pair,

```
q_0(pi(A_L+A_R))
 = Q_L(A_L,m)+Q_R(A_R,m)+kappa(m).                  (3)
```

Affine changes of the quadratic origin are included among the linear
characters in H1.

**H3 — internal-handle trace.**  At a cut `lambda_(a_i)|lambda_(b_i)`, the
unemitted `b_i` evaluation on the exposed half is a function `rho_i(m)`.
Equivalently its cochain restriction is exact relative to the interface.
The product `a_i b_i` is assigned to the `a_i` side conditional on
`rho_i(m)`.

These are sufficient hypotheses, not claimed necessary.  Literal cochain exactness is not
necessary: only equality of the induced phase on all partial configurations
with the same interface mask is necessary.  H1 is the local, checkable
cohomological condition that guarantees that equality.  More generally, the
rank conclusion requires only a factorization of all cross-cut phases through
the attainable trace module; accidental algebraic cancellation can give the
same rank bound even when H1--H3 fail.

## 3. Upper-bound theorem

### Theorem 1 (separator compression)

Suppose every pair cut of a canonical spin-coordinate ordering admits a cut
datum with `|S|<=k` satisfying H1--H2.  Then every pair flattening of the
complete tensor (1) has rank at most

```
2^(k-1).                                                       (4)
```

Equivalently, the four-state handle-site TT/MPS has that bond bound.  If H3
also holds at every internal handle cut, the same bound holds for the binary
coordinate TT.  Without H3, the unconditional binary-coordinate bound is
twice (4).

### Proof

Fix a cut.  By H1, all dependence of a left spin coordinate on `A_R` can be
replaced by a sign depending on `m`; absorb it into the left factor.  Do the
opposite for every right coordinate.  By H2, the remaining quadratic sign
splits into a left sign, a right sign, and `(-1)^kappa(m)`.  Therefore

```
F(lambda_L,lambda_R)
 = sum_(m in V(S)) X(lambda_L,m)(-1)^kappa(m)Y(m,lambda_R),     (5)
```

where

```
X(lambda_L,m)
 = sum_(A_L:partial_L A_L=m)
   (-1)^(Q_L plus the left character phases) product_(e in A_L)t_e,
```

and `Y` is defined analogously.  Equation (5) is coefficientwise in the
independent edge variables.  It is a factorization through at most
`|V(S)|<=2^(k-1)` states, proving (4).

At an internal handle cut, H3 makes the `lambda_(b_i)` sign a diagonal
function of the same `m`; the conditional `a_i b_i` sign remains in `X`.
Thus the index set in (5) is unchanged and there is no extra factor two.

Applying (5) successively at all pair cuts gives four-state TT cores.
Splitting a four-state core of adjacent bond at most `D` gives an internal
bond at most `2D`; H3 improves this to `D` by the preceding paragraph.
Explicitly, the core between two successive separators is the polynomial matrix obtained by
summing its edge subsets with fixed incoming/outgoing masks and the local
phase from H1--H3.  Multiplying cores performs each compatible gluing exactly
once, proving the MPS identity.  This completes the proof.

For disconnected interfaces, replace `(2)` by the actually attainable mask
space; the bound is its cardinality, not automatically `2^(|S|-1)`.

## 4. Boundary conditions

Free boundaries use the zero-mask boundary vectors.  An antiperiodic seam is
a fixed edge cocycle and is absorbed into `Q_L` or `Q_R`.  Periodic closure is
a trace over the same separator state space after choosing and cutting a
seam.  Fixed-spin boundaries are covariant, rather than invariant, under a
gauge change and must be transformed with it.  None of these operations
changes the local rank bound.

## 5. Corollaries

### Corollary 1 (checkerboard grid strips)

The checkerboard co-core filtration of
`P_n square P_w square P_w` has a connected separator meeting `w^2` graph
strands.  Its canonical Lagrangian basis satisfies H1 and H2 by discrete
Stokes; at a co-core midpoint its longitude satisfies H3.  Theorem 1 gives

```
rank Flat(F_(n,w)) <= 2^(w^2-1).
```

This recovers Cycle 7 as a direct corollary.

### Corollary 2 (toroidal two-sum chains)

Take the cellular torus rotation

```
0,1,2: (3,4,5),       3,4,5: (0,1,2)
```

of `K_(3,3)`, with disjoint port edges `(0,3)` and `(1,5)`.  Its three face
walks are hexagons, so Euler's formula gives genus one.  Concatenate `r`
copies by the oriented edge-two-sum of the right port of one copy and the
left port of the next.  This is the connected sum of the explicit tori; call
the resulting ribbon graph `C_r`.

The surface has genus `r`, and deleting both ports from one gadget leaves two
cycles forming its canonical torus handle.  Their ordered union is therefore
a canonical handle basis for `C_r`.  Between gadgets the graph meets the
separator in two marked points, whose attainable masks are `00` and `11`.
Handles behind and ahead of the separator have disjoint support, so H1--H2
hold.  The pair-cut part of Theorem 1 gives an exact four-state
all-spin-structure TT with

```
handle-site bond <= 2,
binary-coordinate bond <= 4
```

for every `r` and arbitrary nonuniform edge weights.

H3 does not hold for the two-point separator of an interior gadget.

`PROVED` (infinite sharpness).  For generic independent edge weights, every
nontrivial pair cut of `C_r`, `r>=2`, has rank exactly two, and every internal
cut of a non-end handle of `C_r`, `r>=3`, has rank exactly four.  To prove the
lower bounds, use the frozen zero-port witnesses.  At a chosen pair cut, set
all edges outside the two adjacent gadgets to zero and identify the remaining
weights with the two-gadget witness, whose `2 x 2` minor is nonzero.  At an
interior cut, do the same with the three gadgets centered at that handle; the
standalone outer port weights are also zero, so the surviving tensor is
literally the frozen three-gadget tensor, whose central `4 x 4` minor is
nonzero.  Fixing all exterior spin-structure coordinates to zero embeds each
minor in the larger flattening.  Hence the corresponding symbolic minors are
not identically zero.  The upper bounds two and four were proved above, so
equality holds on a nonempty Zariski-open set.

`PROVED`: the interior generic rank remains four under every local affine
symplectic relabeling of that handle.  In genus one these are all 24
permutations of its four quadratic refinements; the replay supplies a
nonzero rank-four minor for each permutation of the zero-port witness.  The
same embedding argument applies at arbitrary chain length.  Thus no local
canonical relabeling restores the H3 conclusion.  This is both a non-grid,
unbounded-genus application and a sharp obstruction showing the
internal-trace hypothesis cannot be dropped.

## 6. A sufficient generic-tightness criterion

### Theorem 2 (homology-injective tree criterion)

At a cut with connected separator `S`, suppose each side contains a tree
whose vertex set includes `S`.  Fix a reference tree on `S`.  Closing the
unique side-tree T-join for every `m in V(S)` with the reference T-join gives
maps

```
c_L:V(S)->H_L,       c_R:V(S)->H_R.
```

If both maps are injective, then the flattening in Theorem 1 has generic rank
`2^(|S|-1)` for independent edge weights.

### Proof

Set every edge outside the two side trees and the reference completions to
zero.  A tree has exactly one edge subset with any prescribed even boundary,
so each side factor contains exactly one surviving monomial for each `m`.
After a Walsh transform in the spin-structure coordinates, injectivity of
`c_L` and `c_R` turns the two factor matrices into submatrices of character
tables of `H_L` and `H_R`.  Their selected `|V(S)|` rows are invertible Walsh
matrices, multiplied by nonzero monomial diagonals.  Hence their product has
rank `|V(S)|` at this specialization.  The corresponding symbolic minor is
not identically zero, proving generic tightness.

The checkerboard rectangular-detour trees tested in Cycle 8 do not satisfy
this criterion; Theorem 2 remains a sufficient criterion, not a proof of G1.
