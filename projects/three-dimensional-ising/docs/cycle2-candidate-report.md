# Stage 2 candidate report: five exact first falsification tests

## Claim boundary and outcome

`PROVED`: all five lanes underwent their declared exact first test before any
selection. One lane, spin-structure compression, remains `SURVIVES`, but only
because growing-genus tensor-train rank and a recurrence in `L` remain
untested. The other results are scoped no-go statements or a killed direct
candidate. No lane yet provides commuting physical transfer matrices,
polynomially many exact sectors, subexponential auxiliary complexity, exact
recursive closure, or a controlled thermodynamic limit. There is no Stage 2
success and no exact-solution claim.

The exact replay is

```bash
python3 proof/verify_cycle2_five_lanes.py
```

The algebraic criteria and their primary sources are recorded in the
[Cycle 2 source audit](../discovery/cycle2-source-audit.md).

## Summary

| Lane | Decisive result | Status |
|---|---|---|
| A — tetrahedron integrability | Direct binary `R`, diagonal gauges, and invariant `D=3,4` extensions fail the standard tetrahedron equation; naive physical layers also fail to commute | `RESTRICTED NO-GO` |
| B — spin-structure compression | Handle factorization, bounded Fourier degree, and symmetry-orbit compression fail; growing-genus TT rank/recurrence remain open | `SURVIVES` |
| C — higher-form fermionization | Known local free-fermion bosonization uses the wrong Gauss law; an unrestricted flux sum is exponential | `KILLED` |
| D — local tensor transformation | Site tensor is exactly Gaussian, but an ordinary crossing is not; an independent `D=2` correction recreates exponentially many selectors | `RESTRICTED NO-GO` |
| E — exact renormalization | One exact checkerboard block produces nonzero four- and six-spin interactions | `RESTRICTED NO-GO` |

## Lane A — tetrahedron integrability

### 1. Exact proposed identity

Let `V_x=V_y=V_z=Q^2`. Orient the three negative-direction legs of a cubic
site as inputs `i=(i_x,i_y,i_z)` and the positive legs as outputs
`o=(o_x,o_y,o_z)`. The anisotropic high-temperature Ising tensor is

```text
R(x,y,z)^o_i
 = 1[i_x+i_y+i_z+o_x+o_y+o_z even]
   x^o_x y^o_y z^o_z.                                  (A.1)
```

On a periodic network every bond weight occurs at exactly one positive end,
so (A.1) is exactly the bond-dimension-two Ising tensor. Splitting weights
between both ends is related by invertible diagonal leg gauges. More
generally, inserting `G_mu` and `G_mu^-1` at the two ends of every contracted
bond preserves the partition function. Coherent conjugation of every local
space also conjugates, and cannot erase a nonzero residual of, the standard
vertex tetrahedron equation

```text
R_123 R_145 R_246 R_356 = R_356 R_246 R_145 R_123.      (A.2)
```

The intended spectral parameters are `(x,y,z)=(t_x,t_y,t_z)`, a
three-dimensional physical locus rather than one fitted point.

### 2. Escape from Stage 1

If a nontrivial spectral family containing (A.1) satisfied (A.2), the
Bazhanov--Stroganov train argument would yield commuting layer transfer
operators without expanding over surface spin structures.

### 3. Auxiliary dimension or sectors

The direct tensor has `D=2`. The first auxiliary tests embed its binary
physical subspace invariantly in `D=3` and `D=4`; projection of (A.2) then
recovers the binary equation, so these extensions cannot repair a binary
residual. Non-invariant auxiliary mixing is outside this no-go.

### 4--5. Decisive experiments and results

`PROVED`: the `(out,in)=(0,3)` matrix entry of (left minus right) in (A.2) is

```text
x^2 y^2 + 2x^2yz + 2x^2y + x^2z - xy^2z^2 - xyz^2
- xy - xz^2 - y^2z^2 + y^2z - yz^2 - y - z^2 + 1.
```

On the physical isotropic line it is
`-(t-1)^3(t+1)^2`, hence is nonzero for `0<t<1`. Thus the physical tensor is
not on a nontrivial standard vertex-TE family.

Independently, define the exact unsymmetrized `3x3` periodic-layer transfer
matrix

```text
T_p(s,s') = product_(e in layer)(1+t_e s_u s_v)
            product_v(1+t_z s_v s'_v).
```

At `p=(1/2,1/3,1/5)` and `q=(1/3,1/4,1/7)`, `PROVED`:

```text
[T_p,T_q]_(0,0) = 25050585732481024 / 54045009375 != 0.
```

### 6. Status

`RESTRICTED NO-GO`.

### 7. Unproved assumptions/open variants

An interaction-round-a-cube relation, a different local tensorization,
non-invariant `D=3,4` auxiliaries, a higher-dimensional auxiliary space, or a
spectral curve with a new intertwiner remains untested.

## Lane B — spin-structure compression

### 1. Exact proposed identity

For a cellular genus-`g` embedding, group even subgraphs by
`h in H_1(Sigma;F_2)`:

```text
W_h(t) = sum_[A]=h t^|A|,
F_lambda(t) = sum_h (-1)^q_lambda(h) W_h(t),             (B.1)
Z_even(t) = 2^-g sum_lambda (-1)^Arf(lambda) F_lambda(t). (B.2)
```

Equations (B.1)--(B.2) are the exact generalized Kac--Ward square-root and
Arf transform. The candidate treats `lambda` as `2g` Boolean variables and
seeks a low-rank tensor train or exact recurrence that evaluates the one
required coefficient collectively.

### 2. Escape from Stage 1

This does not enumerate determinants term by term. Success would mean that
the Boolean function `F(lambda)` has a representation whose rank or recursive
state count is subexponential even though its truth table has `4^g` entries.

### 3. Auxiliary dimension or sectors

The raw sector count is `4^g`. The surviving target is a tensor-train bond
rank or recurrence state count polynomial in `L`; no such bound is proved.

### 4--5. Decisive experiments and results

First, the simple `3x3` toroidal square grid supplies a genus-one calibration.
Its cycle space has dimension ten. Exact enumeration of all `2^10` cycles
gives all four `W_h` and all four `F_lambda` polynomials. The `2x2` matrix of
`F` values across the two spin bits has rank two over `Q(t)`, witnessed at
`t=1/2` by determinant
`-1412718083/67108864`. `PROVED`: handle-bit factorization (rank one) fails.

Second, a pinned rotation system gives the free `3x3x2` cubic slab 15 cellular
faces of lengths
`4,4,4,4,4,4,4,4,8,6,4,4,4,4,4`. With `V=18`, `E=33`, and `F=15`, its Euler
characteristic is zero, so the embedding has genus one. The Stage 1
Euler/girth bound is also one. `PROVED`: this is a minimum-genus embedding.
Its cycle space has dimension 16 and its face-boundary space dimension 14.
Exact enumeration of all `2^16` cycles gives `2^14` cycles in each homology
sector. Its `F` matrix again has exact rank two, not one. Full coefficients and
the rotation system are emitted by the replay.

`PROVED`: bounded Boolean Fourier degree cannot hold for a positive-weight
cellular embedding. The graph cycles surject onto `H_1(Sigma;F_2)`, so every
homology class occurs; each `W_h(t)` is nonzero for `t>0`. Therefore every one
of the `4^g` Fourier characters is present, including degree `2g` in any
chosen Boolean basis.

`PROVED`: geometric cubic symmetry alone also cannot give polynomially many
orbits. For `L>=3`, the free cubic graph has the 48 coordinate permutations
and reflections as its full automorphism group. Its action on `4^g` spin
structures has at least `ceil(4^g/48)` orbits, still exponential using the
Stage 1 genus bound.

### 6. Status

`SURVIVES`, but only for growing-genus tensor-train rank or an exact recurrence
mixing the dense Fourier sectors. This is not a success result.

### 7. Unproved assumptions/open variants

No minimum-genus embedding or `F` table for genus greater than one has yet
been constructed. No handle ordering with submaximal TT rank, recurrence in
`L`, or collective determinant evaluation is proved.

## Lane C — higher-form fermionization

### 1. Exact proposed identity

The direct candidate was to identify the standard `Z2` gauge theory dual of
the 3D Ising model with the local gauge theory in exact two-dimensional
bosonization, then evaluate a quadratic fermion trace in each remaining
topological sector.

The physical gauge theory has standard Gauss constraint

```text
G_v = product_(e incident v) X_e = 1.                   (C.1)
```

The locality-preserving free-fermion bosonization instead uses, in the square
lattice convention of Chen--Kapustin--Radicevic,

```text
G'_v = G_v W_NE(v) = 1,
U_e = X_e Z_r(e),                                       (C.2)
```

with explicit spin-structure/topological data in non-simply-connected
geometry.

### 2. Escape from Stage 1

If (C.1) and (C.2) described the same physical subspace and operator algebra,
Jordan--Wigner strings would become local gauge redundancy and only bounded
torus holonomies would remain.

### 3. Auxiliary dimension or sectors

There is one binary gauge variable per layer edge. On an `LxL` torus, quotient
by `2^(L^2-1)` vertex gauges leaves `2^(L^2+1)` link-field classes: one of
`2^(L^2-1)` local flux patterns and four holonomies.

### 4--5. Decisive experiments and results

`PROVED`: the projectors differ locally. A joint eigenstate with
`G_v=+1` and `W_NE(v)=-1` is accepted by `(1+G_v)/2` and annihilated by
`(1+G'_v)/2`. Replacing the physical constraint by the modified one therefore
changes the Hilbert space/operator representation; it is not an exact
fermionization of the Ising-dual gauge transfer operator.

`PROVED`: if the mismatch is avoided by retaining unrestricted physical flux
sectors, their gauge-inequivalent count is `2^(L^2+1)`, not a bounded
topological factor. No exact collective evaluation was found.

### 6. Status

`KILLED` for the direct known-bosonization substitution.

### 7. Unproved assumptions/open variants

An interacting fermion theory with the standard constraint, a different
higher-form field, or a new exact flux summation remains open.

## Lane D — local tensor transformation

### 1. Exact proposed identity

The high-temperature network has a rank-six site tensor

```text
P(i_1,...,i_6) = 1[sum i_j even] product_j w_j^i_j.      (D.1)
```

Let `A_ij=w_i w_j` for `i<j` and `A_ji=-A_ij`. `PROVED`: every even component
of (D.1) is the corresponding principal Pfaffian minor of `A`; all 32 minors
through arity six were checked symbolically. The local Ising tensor is already
a Gaussian Grassmann/matchgate signature.

### 2. Escape from Stage 1

A planar network of such signatures contracts by one Pfaffian. A successful
local transformation would also have to turn every planarization crossing
into a compatible matchgate with bounded, collectively contractible
auxiliaries.

### 3. Auxiliary dimension or sectors

The site bond dimension is two. The ordinary crossing has the exact bounded
extension

```text
C_bosonic = C_fermionic + 2 E_1111,                     (D.2)
```

a sum of two Gaussian signatures selected by one `D=2` auxiliary. `D=3,4`
contain this construction by padding unused states.

### 4--5. Decisive experiments and results

In cyclic boundary-leg order, the ordinary crossing has entries
`C_0000=C_1010=C_0101=C_1111=1`. Its two-leg data force the Gaussian
four-leg value `-1`, so its Grassmann--Pluecker residual is exactly `2`.
`PROVED`: nonzero diagonal leg gauges merely rescale this residual and cannot
remove it.

The fermionic crossing changes `C_1111` to `-1` and is Gaussian. Equation
(D.2) repairs one crossing, but with `c` independent crossings and no further
selector identity it expands to `2^c` assignments. `PROVED`: bounded local
dimension alone has not reduced the contraction.

### 6. Status

`RESTRICTED NO-GO` for diagonal Ising gauges and independent crossing
selectors.

### 7. Unproved assumptions/open variants

General `GL(2)` holographic bases, correlated crossover auxiliaries, and an
exact recursive selector closure remain open.

## Lane E — exact renormalization closure

### 1. Exact proposed identity

Use checkerboard decimation with a `2x2x2` translation cell. For each
eliminated spin `s_0`, retain its six boundary neighbours in the
`+/-x,+/-y,+/-z` directions. The exact normalized block weight is

```text
W(s_1,...,s_6)
 = sum_(s_0=+/-1) product_i (1+t_i s_0 s_i),             (E.1)
(t_1,...,t_6)=(t_x,t_x,t_y,t_y,t_z,t_z).
```

The complete log-Walsh coordinates are

```text
J_S = 2^-6 sum_s (product_(i in S) s_i) log W(s).        (E.2)
```

Global spin flip kills every odd `S`. Every induced boundary interaction is
therefore recorded by one constant, 15 pair terms, 15 four-spin terms, and
one six-spin term.

### 2. Escape from Stage 1

If these couplings lay on a finite-dimensional invariant algebra under
repeated blocking, (E.1) would give exact recursive closure without a surface
spin-structure sum.

### 3. Auxiliary dimension or sectors

The first blocked star has 32 even Walsh coordinates. No bounded dimension
for repeated blocking is proved.

### 4--5. Decisive experiment and result

At the exact rational point
`(t_x,t_y,t_z)=(1/2,1/3,1/5)`, exponentiating 64 times a Walsh coefficient
gives a rational multiplicative invariant. `PROVED`:

```text
exp(64 J_{1234})
 = 690618655925447181028866289 / 4205503500998020172119140625 != 1,

exp(64 J_{123456})
 = 451735884769 / 338520330625 != 1.
```

Hence both four- and six-spin interactions are genuinely induced; the
nearest-neighbour and general pairwise families do not close. Because one
exact specialization is nonzero, neither symbolic coefficient vanishes
identically in `(t_x,t_y,t_z)`.

### 6. Status

`RESTRICTED NO-GO` for nearest-neighbour or pairwise closure.

### 7. Unproved assumptions/open variants

A larger finite interaction algebra, closure only on a critical manifold,
asymptotic closure, or a nonlocal change of variables remains open. No
numerical truncation is promoted.

## Post-test selection

Only after all five tests above, Lane B is selected for the next attack.
This is a choice of experiment, not a successful representation.

The criteria are mathematical:

- (B.1)--(B.2) are already exact for the physical partition function and do
  not change its gauge constraint or local weights.
- The remaining questions—minimum TT rank under handle orderings and a
  recurrence in `L`—have exact rank/recurrence falsifiers.
- Lane A's direct physical locus, Lane C's physical constraint, Lane D's
  independent crossing closure, and Lane E's pairwise closure have already
  failed their first necessary conditions.

`SPECULATIVE`: growing-genus `F(lambda)` may still have a collective low-rank
description despite full Fourier support. The next decisive test must build a
minimum-genus embedding with `g>=2`, compute the exact homology-sector table,
and measure TT ranks over all symplectic handle orderings feasible at that
size. Rank growth matching `2^g`, or failure of any `L`-recurrence ansatz at
the declared order, would falsify the surviving mechanism.
