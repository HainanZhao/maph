# Cycle 77: the critical cell is an anchored anisotropic saddle

## Claim boundary

At the unique worst cell

```text
(theta,alpha,kappa)=(1/3,1/3,8/75),                (1)
```

`PROVED`: after choosing one packet as an anchor, every other packet is
equivalent up to absolute tube constants to an integer point near the fixed
saddle

```text
|n-c_0 q exp(2pi d/Delta)| << X^(-83/75),          (2)
```

where `d=ell-ell_0`, `c_0=n_0/q_0`,
`Delta=X^(3/5+o(1))`, and `q,n=X^(1/3+o(1))`. The exact theorem target is a
uniform bound strictly below `X^(2/15)` for (2).

`PROVED`: discarding the anchor and retaining only ratios creates a formal
volume exponent `37/75`, exceeding the squared target `4/15` by `17/75`.
The anchor is therefore quantitatively essential to this reduction.

No anchored-saddle estimate, full packet closure, seed-extraction theorem,
powered saving, density gain, or interval gain is proved.

## Anchored reduction

Write

```text
E_ell=exp(2pi ell/Delta), n=q+a,
|n-qE_ell|<=eta, eta=X^(-83/75+o(1)).               (3)
```

Choose one packet `(ell_0,n_0,q_0)` and set `c_0=n_0/q_0`. For another
packet, put `d=ell-ell_0`. Since

```text
|c_0-E_(ell_0)|<=eta/q_0
```

and all ratios in the dyadic cell are bounded above and below, (3) implies
(2). Conversely, (2) together with the anchor implies (3) with another
absolute tube constant. Thus the anchored formulations are equivalent at
exponent scale.

Normalize

```text
x=d/Delta, y=q/Q, z=n/Q, Q=X^(1/3).
```

Then (2) is the graph

```text
z=f(x,y)=c_0 y exp(2pi x)                           (4)
```

sampled on anisotropic mesh

```text
(Delta^-1,Q^-1,Q^-1)                               (5)
```

and normalized vertical tube

```text
eta/Q=X^(-36/25+o(1)).                              (6)
```

Its Hessian satisfies

```text
det Hess f=-(2pi c_0 exp(2pi x))^2,                (7)
```

uniformly bounded away from zero on the frozen compact cell. In unnormalized
`(d,q)` variables the determinant is comparable to `Delta^-2`.

The formal random-volume exponent of (2) is

```text
3/5+1/3-83/75=-13/75,                              (8)
```

far below the required `2/15`. Equation (8) is a benchmark, not a proved
count.

## Why the ratio-only census is too weak

For two packets, let

```text
U=nq', V=n'q, d=ell-ell'.
```

Direct subtraction gives the necessary condition

```text
|U-exp(2pi d/Delta)V| << Q eta=X^(-58/75+o(1)).    (9)
```

Both `U` and `V` are products of two `Q`-scale integers; their representation
multiplicity is divisor-bounded and hence `X^o(1)`. Squaring the packet target
requires the census in (9) to be strictly below

```text
X^(4/15+o(1)).                                      (10)
```

If one forgets the anchor and treats `d,V` as free, the formal volume is

```text
3/5+2/3-58/75=37/75.                               (11)
```

The gap between (11) and (10) is `17/75`. This explains precisely why a
ratio-only energy argument is not the desired E15 theorem: it erases the
absolute packet phase that (2) retains.

## Checked source boundary

`OBSERVED` source check: Huang, *Rational points near planar curves and
Diophantine approximation*, arXiv:1403.7388, Definition (1.1) and Theorem 1,
uses two rational coordinates with one common denominator. Huang,
*The density of rational points near hypersurfaces*, arXiv:1711.01390v4,
Theorem 1 and equations (1.9)--(1.10), likewise works in common-denominator
Monge geometry with Hessian determinant bounded away from zero. Their
curvature hypotheses match (7), but their denominator geometry does not
match (5).

Even granting integer `Delta`, forcing a common denominator
`R=Delta Q=X^(14/15)` gives tolerance parameter
`Delta eta=X^(-38/75)`. The standard planar bound
`delta R^2+R^(1+epsilon)`, combined with the original trivial count, leaves
best exponent `14/15`, still `4/5` above the target `2/15`. This is a scoped
non-applicability calculation, not a universal obstruction to adapting the
projective-duality method.

## New theorem contract

`CONJECTURED` anisotropic critical-saddle incidence (`ACSI`): uniformly for
every primitive anchor in the frozen compact ratio cell,

```text
#{(d,q,n): (2) holds} << X^(2/15-epsilon)           (12)
```

for some explicit `epsilon>0`, or else the exceptional points yield a
phase-bearing rational web from which E16 extracts a genuine seed.

The natural construction is a sublattice-aware projective duality or
stopping-time decomposition that preserves the mesh (5). Isotropic
common-denominator embeddings and anchor-free pair energy are baselines only.

## Gate effect

E13 advances to
`CRITICAL_ANCHORED_SADDLE_ACSI_OR_PHASE_WEB_OPEN`.
