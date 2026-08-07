# Lifted-matroid specialization criterion for generic Lane B tightness

## Claim boundary

`PROVED`: the common-independent-set criterion below is sufficient for an
exact nonzero `d_w` minor of a canonical all-spin-structure flattening.

`OBSERVED`: exact `GF(2)` matroid intersection meets the criterion at widths
`w=3,4,5,6,7` for the frozen checkerboard coordinates.  These finite widths
do not prove the arbitrary-width claim.

`CONJECTURED`: for every `w>=3`, a sufficiently long checkerboard strip has a
canonical cut satisfying the criterion.  The remaining theorem is the
explicit rank inequality in Section 4, not an exponential determinant
calculation.

Width two is exceptional: the chosen checkerboard embedding has genus zero,
so its complete spin-structure tensor is scalar.  No statement
`R_infinity(2)=2^3` is made.

## 1. Two lifted graphic matroids

Fix a canonical handle cut.  Let `C_1(G;F_2)` have the graph edges as its
distinguished basis, let

```
partial: C_1 -> C_0^0
```

be the vertex-edge incidence map with one vertex row deleted, and split the
canonical homology label as

```
rho=(rho_L,rho_R): ker(partial) -> H_L direct-sum H_R.
```

For an edge `e`, form the two represented-matroid columns

```
v_L(e)=(partial e,rho_L(e)),
v_R(e)=(partial e,rho_R(e)).
```

The use of edge labels in this display is harmless: changing a label by a
coboundary is an elementary row operation adding an incidence row.  Thus the
two represented matroids depend only on the corresponding homology
projections.

### Lemma 1 (rank formula)

For every edge set `X`,

```
r_L(X)=r_G(X)+rank rho_L(Z_1(X)),
r_R(X)=r_G(X)+rank rho_R(Z_1(X)).                 (1)
```

`PROVED`: row-reduce the incidence columns of `X`.  Their kernel is exactly
`Z_1(X)`.  The only additional rank supplied by the homology rows is the rank
of their restriction to that kernel.

### Lemma 2 (connected common-independent specialization)

Put `m=w^2-1`.  Suppose an edge set `H` is independent in both lifted
matroids, is connected and has

```
|H|=|V|-1+m.                                      (2)
```

Then `dim Z_1(H)=m`, and both restrictions

```
rho_L|Z_1(H), rho_R|Z_1(H)
```

have rank `m`.

`PROVED`: connectedness gives `r_G(H)=|V|-1`.  Apply (1) and independence,
which says `r_L(H)=r_R(H)=|H|`.

Conversely, a connected `H` with `dim Z_1(H)=m` and both projections
injective is common-independent.  Thus the tree-plus-chords language and the
lifted-matroid language are equivalent, but the latter does not guess a
spanning tree first.

## 2. Exact flattening minor

Let `U=Z_1(H)`.  Choose bases of the two `m`-dimensional images.  Restrict the
left and right Walsh transforms to the corresponding `2^m` characters.  Set
all edge variables outside `H` to zero.  Every surviving even subgraph is a
unique `z in U`, so the doubly Walsh-transformed minor has one nonzero entry
in every row and column:

```
W_L M W_R^T = 2^(2m) P_L diag((-1)^Q(z) x^z) P_R. (3)
```

Here `P_L,P_R` are coordinate permutations; a different unnormalised-Walsh
convention moves the displayed power of two between the two sides but does
not affect nonvanishing.  Equation (3) is obtained directly from character
orthogonality:

```
sum_alpha (-1)^<alpha,u+rho_L(z)> = 2^m [u=rho_L(z)],
```

and similarly on the right.  No Arf sum is used.

Every diagonal entry in (3) is a nonzero monomial.  Therefore the selected
minor is nonzero over the integer edge-weight polynomial ring.  Specializing
the retained edge variables to one gives determinant magnitude

```
2^(m 2^m)                                           (4)
```

in the original, unnormalised flattening convention used by the width-three
replay.  For `m>=3` its sign is positive.  Indeed, every affine quadratic
`Q` with `Q(0)=0` has even truth-table weight in at least three variables;
and every generator of `GL(m,2)` permutes `F_2^m` evenly (a transvection or
coordinate swap has a multiple of `2^(m-2)` transpositions).  Hence the
quadratic diagonal and both coordinate permutations have determinant `+1`.

It follows that one such `H` proves

```
generic rank >= 2^m.
```

Together with the already proved frontier upper bound, it proves equality.
Although the witness specialization uses zero edge weights, a nonzero real
polynomial cannot vanish on the open positive orthant.  Thus the conclusion
is generic also among strictly ferromagnetic nonuniform weights.  It does
not imply homogeneous anisotropic or isotropic tightness.

## 3. Exact finite-width outcomes

The deterministic exact audit uses the checkerboard atomic coordinates and
Edmonds' augmenting-path algorithm over `GF(2)`.  It constructs no
`2^m x 2^m` matrix.

| `w` | `n` | handle cut | target `|V|-1+m` | maximum common size | result |
|---:|---:|---:|---:|---:|:---|
| 3 | 10 | 5 | 97 | 97 | criterion met |
| 4 | 10 | 9 | 174 | 174 | criterion met |
| 5 | 7 | 12 | 198 | 198 | criterion met |
| 6 | 8 | 20 | 322 | 323 | trim one nonbridge |
| 7 | 7 | 27 | 390 | 390 | criterion met |

These are `OBSERVED` until promoted through the proof-grade sealing scaffold.
The width-three case also has an independently reconstructed dense
`256 x 256` minor; at unit retained weights its determinant is exactly
`+2^2048`, with its reductions replayed modulo `1000000007` and
`1000000009`.

## 4. The arbitrary-width bridge

By the matroid-intersection min--max theorem, the desired `H` exists exactly
when, for every edge partition `E=X disjoint-union Y`,

```
r_L(X)+r_R(Y) >= |V|-1+m.                           (5)
```

Let

```
lambda_G(X)=r_G(X)+r_G(Y)-r_G(E)
```

be the graphic connectivity across the partition.  Substitution of (1)
turns (5) into the intrinsic inequality

```
lambda_G(X)
 + rank rho_L(Z_1(X))
 + rank rho_R(Z_1(Y)) >= w^2-1.                     (6)
```

`PROVED`: (6) is equivalent to the required common-independent-set
existence for each fixed strip and cut.

`CONJECTURED`: the filtration-adapted checkerboard labels satisfy (6) once
both sides contain at least `w^2-1` canonical coordinate bits.  Exact dual
partitions through width seven attain or exceed the right-hand side, but
that finite audit is not an arbitrary-width proof.

The geometric form of the missing lemma is: a moving canonical separator of
`w^2` marked points admits on each side a homology-injective relative
spanning tree, and the two trees glue to a connected `H` with cycle dimension
`w^2-1`.  A flat longitudinal plane is insufficient; that restricted family
was already falsified.  The separator must move around the checkerboard
co-cores exactly as in the upper-bound proof.

## 5. Failure boundary

Literal nesting of the selected width-four edge set into width five fails:
the transported set has lifted ranks `174/173`.  This is a canonical-basis
transport defect, not a failure of (6); an independent width-five target set
exists.  Likewise, all longitudinal rails plus transverse trees only on the
two terminal slices sees ranks `3/8` at width three and `5/15` at width four.
Internal co-core slabs are essential.

