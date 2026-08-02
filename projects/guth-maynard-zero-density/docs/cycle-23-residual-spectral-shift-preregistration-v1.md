# Cycle 23 residual spectral-shift preregistration v1

## Claim boundary

This cycle may derive an exact determinant identity after removing the common
coefficient direction and prove a spectral-shift/inverse-leverage dichotomy.
It may not bound the residual leverage for prime rows, prove the skeleton
target, or promote a density or interval result.

## Frozen residual normalization

Let `U` have `k` rows `u_t`, each of squared norm `M`, and let `a` have
squared norm `A`. Put

```text
H=UU*/M,
q=Ua/sqrt(AM),
rho_t=|q_t|^2.
```

Assume `rho_t<1`. The common-direction residual is

```text
Z=H-qq*=U(I-aa*/A)U*/M >= 0.
```

Let `D=diag(sqrt(1-rho_t))`. When `Z` is positive definite, define

```text
B=D^(-1) Z D^(-1),    s=D^(-1)q.
```

Then `B` is positive definite with diagonal one and

```text
H=DBD+qq*.
```

## Frozen exact identity

The matrix determinant lemma gives

```text
det(H)/det(B)
 = product_t(1-rho_t) [1+s*B^(-1)s].
```

Equivalently,

```text
log det(H)-log det(B)
 = sum_t log(1-rho_t)+log(1+L),
L=s*B^(-1)s.
```

## Frozen dichotomy

Suppose every projection has size at least `V`, and set
`rho=V^2/(AM)`, so `rho_t>=rho`. For any `0<epsilon<1`, if

```text
L <= exp(epsilon k rho),
```

then

```text
log det(H)-log det(B)
 <= -(1-epsilon)k rho+log 2.
```

Conversely, if the shift is larger than `-c k rho`, `0<c<1`, then

```text
log(1+L) >= (1-c)k rho,
L >= exp((1-c)k rho)-1.
```

At the skeleton scales `k=X^(21/25)` and `rho=X^(-3/5)`, the dichotomy scale
is `k rho=X^(6/25)`. Thus ordinary spectral bulk is contained in `det(B)`;
the only offset to the additional common-direction loss is exponentially
large inverse leverage in the normalized residual.

If `Z` is singular, register a separate `RESIDUAL_SINGULAR` branch. Do not
silently apply an inverse or determinant ratio.

## Compute and review rules

- CPython `3.12.3`, optimization level zero, exact `Fraction` arithmetic for
  finite diagonal models and exponent checks.
- No RNG, third-party library, or network.
- Builder cap: 30 seconds and 256 MiB RSS.
- Hostile audit remains deferred to paper stage.
