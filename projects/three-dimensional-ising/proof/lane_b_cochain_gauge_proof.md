# Width-three cochain quotient and exact rank closure

## Claim boundary

`PROVED`: in the corrected nested symplectic coordinates for
`G_(n,3)=P_n square P_3 square P_3`, every handle-pair and handle-internal
flattening of both the Walsh character tensor `G` and the quadratic-refinement
tensor `F` has rank at most `256`, for every `n>=4` and arbitrary edge weights.
The proof is a local `F_2` cochain/gauge quotient, not a numerical plateau.

`CERTIFIED_NUMERICAL`: the lower-bound minors at the decisive longitudinal
sizes are recorded separately.  No growing-width statement is made here.

## 1. Correction to the Cycle 4 handle coordinates

Let the old pinned homology dimension be `d`.  Cycle 4 correctly found that

```
d_new = e_(d-1) + e_d
```

is orthogonal to the old homology space and pairs with the raw new generator
`e_(d+1)`.  It did not check that `e_(d+1)` itself is orthogonal to the old
space.  It is not.  Solving the exact intersection equations gives

```
c_new = e_(d-2) + e_(d+1).
```

For every audited transition `4->5,...,11->12`, the correction is exactly
`e_(d-2)`.  With both corrections, the old symplectic basis followed by
`(d_new,c_new)` has the canonical block-diagonal intersection matrix.  Thus
the Cycle 4 all-length rank bound remains an upper bound in spirit, but its
displayed assertion `c=raw_new_b` and every downstream canonical-`q` rank
computed from it must be superseded.

## 2. Local cochain identity

Let `E_perp` be the twelve edges of a `3x3` transverse slice and let
`C^k=C^k(E_perp;F_2)`.  For an edge subset `S` and a vertex cochain `s`,
discrete Stokes is

```
<delta s,S> = <s,partial S>.                         (1)
```

The corrected recursive labels are not literally bounded-window labels.  The
orthogonal correction to each new `c` generator propagates old coordinate
bits into later slices.  The coordinate-error firewall checks every such bit,
not only the four newest ones.  All extra old modes are nevertheless exact
coboundaries.  Modulo `B^1=im(delta)`, the only nonzero modes at an interior
slice `i` are the two active `a` coordinates `(a_(i-1),a_i)`.

The four newest representatives have the period-two window

```
(b_left,a_left,b_right,a_right)
  = (1080,1056,452,320)
or  (452,320,1080,1056)
```

in the pinned twelve-edge bit order.  The two exact representatives used by
all `b` modes and all propagated old modes are:

```
1080 = delta(79),     452 = delta(27),               (2)
```

where the potentials are nine-bit row-major vertex masks.  The verifier
checks (1) for all `4096` transverse edge subsets and both identities (2).

In spin language, if `D_eta` is the transverse Boltzmann diagonal and

```
U_s |sigma> = |sigma+s>,
```

then coefficientwise in arbitrary edge weights

```
D_(eta+delta s) = U_s^(-1) D_eta U_s.                (3)
```

The longitudinal connector kernel commutes with simultaneous `U_s`, since
each of its factors depends only on `sigma_v sigma'_v`.  Equations (1) and
(3) are the parity- and spin-transfer forms of the same gauge identity.

## 3. Gluing through only the physical frontier

Cut the tube at a spatial separator aligned with the last occurrence of the
`a` coordinate adjacent to a chosen twist-coordinate cut.  A partial even
subgraph meets the separator in an even mask

```
x in P={x in F_2^9: |x| even},   |P|=256.
```

Every inactive old-coordinate and `b` contribution on a side of the separator
is a sum of the exact slice cochains (2).  By (1), its value is a known linear
function of the exposed mask `x`; it is not an independent topological memory
bit.  The firewall verifies that the only nonexact modes in an interior slice
are `a_(i-1)` and `a_i`, with the expected one-mode truncation at each end.
Aligning the separator after the last occurrence of the adjacent `a`
coordinate leaves no nonexact historical mode crossing it.  The remaining
`a` sector coordinate is additive across the separator.  Its
linear Walsh phase splits immediately.  Its quadratic-refinement phase

```
(-1)^(a*b)
```

also splits conditional on `x`, because the two partial `b` values are
functions of `x`.  Consequently, for every handle-pair cut,

```
G(mu_L,mu_R) = sum_(x in P) L_x(mu_L) R_x(mu_R),
F(lambda_L,lambda_R) = sum_(x in P) L'_x(lambda_L) R'_x(lambda_R).   (4)
```

The finite three-handle prefix and terminal windows are absorbed into the
corresponding boundary factors; their smaller cuts are trivially at most
`256`.

For a cut inside one handle, the `lambda_b b` phase depends on the right
output bit but `b` is already a function of `x`.  It is therefore a diagonal
factor on the same carrier in (4), while the `lambda_a a` phase stays on the
other side.  No factor of two is introduced.  Hence, for every binary or
four-state handle ordering cut,

```
rank G <= 256,       rank F <= 256.                   (5)
```

This improves the former `1024/2048` bounds and proves exact recursive closure
on the ordinary flip-even spin carrier.

## 4. Boundary and normalization audit

- Free boundaries use the all-spin-sum vector, which is `U_s` invariant.
- Periodic longitudinal closure uses a trace, invariant under conjugation.
- An antiperiodic seam is a fixed one-cocycle.  Adding `delta s` changes its
  representative but not its cohomology class, so the same proof applies for
  single-valued periodic `s`.
- Fixed spin boundaries are mapped to gauge-transformed fixed spins; no
  invariance is claimed unless those boundary data are transformed too.
- Gauge maps are permutations and add no normalization.  Walsh denominators
  are powers of two; the one-handle `G->F` map is one half of the pinned
  integer Hadamard matrix.
- Adding an exact cochain does not change any class in `C^1/B^1`, so other
  frozen twist coordinates and boundary sectors are unchanged.

## 5. Consequence and remaining width question

Once one exact `256 x 256` nonzero minor is certified for each cut type and
weight family, (5) proves the corresponding saturation value is exactly
`256`.  This means the width-three simultaneous spin-structure tensor has no
auxiliary topological dimension beyond the conventional physical carrier.

For growing width, the relevant local invariant is still

```
h(w)=dim(W_w/(W_w intersect B^1)),
```

but no formula or sub-area bound for `h(w)` is proved here.  In particular,
the result is not a cubic-box solution or a controlled three-dimensional
thermodynamic limit.
