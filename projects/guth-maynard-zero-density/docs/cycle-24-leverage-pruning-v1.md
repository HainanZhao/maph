# Cycle 24: leverage pruning and the stretched-exponential trichotomy

## Claim boundary

`PROVED`: Cycle 23's inverse-leverage branch decomposes into near-Cauchy
recurrence or stretched-exponential residual ill-conditioning after losing at
most half the rows. `OBSERVED`: neither prime-specific structure is excluded.
No skeleton, density, or interval result is promoted.

## Near-Cauchy recurrence

Normalize the rows and common coefficient vector. After phase alignment,

```text
x_t=sqrt(rho_t)b+sqrt(1-rho_t)e_t,    e_t perpendicular to b.
```

If `rho_t,rho_s>=1-delta`, the triangle inequality gives

```text
|<x_t,x_s>|>=1-2delta.
```

Freeze `delta=exp(-k rho/8)`. If at least half the rows are near-Cauchy,
they form a complete recurrence packet whose normalized prime kernel is at
least `1-2delta` on every pair. This is far stronger than Cycle 19's
`X^(-3/5)` popular-edge threshold.

## Regular residual branch

Otherwise retain `n>=k/2` rows satisfying `1-rho_t>delta`. For this subsystem

```text
||s||^2=sum_t rho_t/(1-rho_t)<=k/delta.
```

If the residual is positive definite and its spectral shift is larger than
`-n rho/2`, Cycle 23 gives

```text
L=s*B^(-1)s>exp(n rho/2)-1.
```

Provided `k rho/4>=log 2`, this and
`L<=||s||^2/lambda_min(B)` imply

```text
lambda_min(B)<=2k exp(-k rho/8).
```

The singular residual is retained separately. Hence every target-sized
common-vector family has one of four outcomes:

1. a half-sized complete near-maximal recurrence packet;
2. residual spectral shift at most `-n rho/2`;
3. a singular normalized residual; or
4. residual minimum eigenvalue at most `2k exp(-k rho/8)`.

At the critical scales, every non-shift structure is stretched exponential
in `X^(6/25)`. The next prime theorem can therefore focus on near-maximal
kernel recurrence and generalized-Vandermonde near-dependence, rather than an
unquantified large inverse.
