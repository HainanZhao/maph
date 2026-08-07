# Lane B Gate B6.2: corrected longitudinal saturation

## Outcome first

`PROVED`: after correcting the nested symplectic handles, the complete
width-three spin-structure tensor has an exact all-length TT/MPS
factorization through only the ordinary 256-state even frontier carrier.
Both cuts between handles and cuts inside a handle have rank at most `256`.

`CERTIFIED_NUMERICAL`: for nonuniform, homogeneous anisotropic, and
homogeneous isotropic weights, the corrected central ranks at the primary
prime are

```
n                 4   5   6   7    8    9   10   11   12
pair/internal      P   P   P   P    P    P    I    P    I
rank               8  16  32  64  128  256  256  256  256
```

The isotropic cases `n=9,...,12` replay identically in rank over a second
prime.  Each rank lower bound is a nonzero determinant of a fixed exact
Walsh-diagonal projection; the record freezes the projection and determinant.

Combining the lower witnesses at `n=9` and `n=10` with the all-length upper
factorization gives

```
R_infinity_pair(3) = 256,
R_infinity_internal(3) = 256.
```

Thus the simultaneous twist/spin-structure family has no auxiliary bond
dimension beyond the conventional zero-field slice carrier at width three.
This is a quasi-one-dimensional strip theorem, not a solution of cubic Ising.

## Correction that changed the answer

Cycle 4 used the correct new defect generator
`d=old_last+raw_new_a`, but its asserted conjugate `c=raw_new_b` was not
orthogonal to the old homology space.  The exact correction is

```
c=old_second_last+raw_new_b.
```

The prior `1024/2048` canonical-`F` claim is withdrawn.  Applying the
canonical quadratic form in the partially corrected coordinates produced
spurious ranks as large as `512`; those values are killed, not repaired.

## Structural mechanism

Correct orthogonalization gives raw edge labels whose support grows with
length.  This apparent nonlocality is pure gauge.  On every transverse
`3x3` slice, all inactive old modes and all `b` modes are one of the exact
cochains

```
1080=delta(79),       452=delta(27).
```

Modulo transverse coboundaries, only two adjacent `a` modes remain active.
Discrete Stokes converts every exact-mode phase into a character of the
current even frontier mask.  At a canonical cut the left and right sums
therefore glue through exactly

```
V_3={m in F_2^9: |m| even},    |V_3|=256.
```

At an internal `lambda_a|lambda_b` cut, the `lambda_b b` phase is already a
function of that same frontier mask and adds no factor of two.  The full proof
and boundary audit are in `proof/lane_b_cochain_gauge_proof.md`.

## Exact-computation discipline

The optimized transfer first identifies and gauges away every exact local
mode, leaving at most two nonexact modes in each cache.  On the full `n=9`
isotropic character tensor its 65,536 outputs agree entrywise with the frozen
legacy engine.  The optimized full replay used three threads, completed in
`775.45` wall seconds, and peaked at `401188` KiB.  An earlier arithmetically
matching run peaked at `14017920` KiB and is excluded for violating the
declared resource cap.

For a central matrix `M`, the lower certificate forms

```
H D_row M D_column H
```

with pinned nonzero diagonal formulas and unnormalized Walsh matrices, then
takes its first `r x r` block, where `r=min(2^(n-1),256)`.  A nonzero projected
determinant proves `rank(M)>=r` because all pre-transformations are invertible.
Together with the proved upper bound this determines the exact rank.

## Classification and next gate

At fixed width three the outcome is `B1 — fixed topological overhead`, with
overhead exactly one relative to the physical carrier.  It is also `B0` at the
carrier-novelty layer: the carrier itself is conventional transfer space.

The arbitrary-width question is open.  For cubic boxes `w=L`, even the desired
closure would leave bond dimension `2^(L^2-1)`.  No polynomial cubic algorithm,
thermodynamic free energy, critical temperature, or critical exponent is
claimed.
