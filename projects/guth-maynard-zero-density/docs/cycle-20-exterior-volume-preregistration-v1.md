# Cycle 20 exterior-volume preregistration v1

## Claim boundary

This cycle may prove the sharp abstract determinant consequence of a common
large coefficient vector and translate it at the separated-skeleton scales.
It may formulate, but not assume or promote, a lower bound for actual
prime-phase Gram determinants. No density or interval result may be promoted.

## Frozen determinant problem

Let `u_1,...,u_k` be vectors with squared norm `M`, Gram matrix `G`, and let
`a` have squared norm `A`. Suppose `|<a,u_j>|>=V` for every `j`. Align the
projections by a unit vector `z` and put

```text
w=V^2/A,    rho=w/M.
```

The registered theorem applies when `kw>=M`. It uses

```text
lambda_max(G)>=kw,    trace(G)=kM
```

and arithmetic--geometric mean on the remaining eigenvalues to prove

```text
det(G)/M^k
 <= k rho [k(1-rho)/(k-1)]^(k-1).
```

The right side is registered as the volume-collapse factor `D(k,rho)`.

## Sharpness model

Let `z` be the all-ones unit direction and set

```text
mu = k(M-w)/(k-1),
G  = mu I + (kw-mu) zz*.
```

Here `zz*` denotes the orthogonal projector, so `G` has eigenvalue `kw` in
the `z` direction and eigenvalue `mu` on its orthogonal complement. Its
diagonal is exactly `M`. A Gram realization admits a vector of squared norm
`A` whose aligned projections all equal `V`; the minimal such squared norm is
exactly `A`. Therefore the determinant upper bound is sharp in the abstract
Hilbert architecture.

## Frozen critical translation

At

```text
M=A=X,    V=X^(7/10),    rho=X^(-3/5),
k=X^(21/25),    k rho=X^(6/25),
```

the elementary inequalities `log(1-rho)<=-rho` and
`log(1+1/(k-1))<=1/(k-1)` give

```text
log D(k,rho) <= log(k rho)+1-(k-1)rho
              = -X^(6/25+o(1)).
```

Thus a sufficient prime-log theorem is the uniform lower bound

```text
det(G_C/M) >= exp(-X^(theta+o(1)))
```

for all `X^(3/5)`-separated prime-phase row sets of size
`k=X^(21/25)`, with any fixed `theta<6/25`. The less quantitative lower bound
`exp(-o(X^(6/25)))` is also sufficient. This is a conditional implication,
not a proved prime determinant bound.

## Cauchy--Binet target

For the prime sampling matrix `U_C=(p^(-it))`, register the exact identity

```text
det(U_C U_C*) = sum_(S subset primes, |S|=k) |det U_(C,S)|^2.
```

The next cycle may seek either one sufficiently large generalized
Vandermonde minor or a collective lower bound for the minor sum. It must keep
the time horizon and `X^(3/5)` separation explicit; unbounded-time
nonvanishing alone is insufficient.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  finite models and exponent translations.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
