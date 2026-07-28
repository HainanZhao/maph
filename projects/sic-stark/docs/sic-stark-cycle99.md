# SIC--Stark research cycle 99: exhaustive scalar-twist gate

Date: 2026-07-28

## Question

Could the level-\(756\) weight-one form be a scalar Dirichlet twist of a
lower-level form?  Such a descent would preserve the projective
representation while perhaps separating the \(\mathbf Q(\sqrt{-3})\)
orientation from a simpler rational regulator.

## Exact invariant

For an unramified prime \(p\), a scalar twist changes

\[
 a_p(f)\longmapsto \xi(p)a_p(f).
\]

Since \(\xi(p)\ne0\), it cannot change whether \(a_p(f)\) vanishes.
Moreover, a scalar twist does not change the projective Galois type.
Thus any lower-level scalar-twist source must:

1. be a weight-one eigenform of projective type \(D_{12}\); and
2. have the same trace-zero pattern as the target at every prime
   unramified in both forms.

## Exhaustive calculation

The certificate

```text
scripts/dimension_six_scalar_twist_gate.gp
```

enumerates every projective-\(D_{12}\) weight-one eigenform at every
level \(N<756\).  There are \(113\).  Each candidate has a prime
\(p\le41\), with \(p\nmid756N\), at which exactly one of the target and
candidate Hecke traces is zero.

Therefore none can be a scalar twist of the target:

\[
\boxed{\text{the level-\(756\) form has no lower-level scalar-twist
descent.}}
\]

This includes nonquadratic twists; it is stronger than merely testing
PARI's quadratic `mftwist` operation.

## Consequence

The coefficient-field orientation is intrinsic to this conductor-minimal
linear realization.  The modular reformulation from cycles 95--98 does
not descend to a lower-level rational dihedral form.  The remaining
identity is still the oriented mixed-signature regulator formula, rather
than a twist of a class-number formula.

