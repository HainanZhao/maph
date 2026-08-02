# Cycle 68: generic large sieve misses by `3/50+theta+kappa`

## Claim boundary

`PROVED`: folding the primitive Poisson form by `m=rq'` produces coefficients
bounded by a divisor function and supported on
`|m|<<KXQ`. Their square norm has exponent at most
`1+theta+kappa`. Nevertheless, Cauchy--Schwarz followed by the generic
separated-point large sieve gives raw exponent

```text
13/10+theta+kappa,                                  (1)
```

which misses the target `31/25` by

```text
3/50+theta+kappa.                                   (2)
```

This is a scoped baseline for coefficient folding plus the generic large
sieve. It is not a barrier to estimates retaining Möbius cancellation or the
specific exponential transport phase. No packet, recurrence, powered,
density, or interval gain is proved.

## Folded coefficient

In Cycle 66 write `m=rq'`. The raw off-diagonal becomes

```text
T(Q,K)=sum_(m!=0) A_m sum_ell e(m alpha_ell),
```

where

```text
A_m=sum_(q'|m) sum_(b: bq'~Q)
    mu(b)/b fhat_C(m/(q'bKX)).                       (3)
```

For each divisor `q'|m`, the `b` variable lies in one fixed-ratio dyadic
interval. Consequently

```text
sum_(b: bq'~Q) 1/b << 1,
```

and the fixed majorant gives

```text
|A_m| <<_f tau(|m|).                                (4)
```

The Fourier support in Cycle 66 also gives

```text
|m| << KXQ=:M,
M=X^(1+theta+kappa+o(1)).                           (5)
```

The elementary divisor-square estimate then yields

```text
sum_(|m|<=M)|A_m|^2 <= M X^o(1).                   (6)
```

Thus folding itself creates no fixed-power coefficient explosion.

## Generic large-sieve ledger

The values `alpha_ell` range over a fixed interval and consecutive values
are separated by `asymp Delta^(-1)`. Splitting at the finitely many integer
crossings makes their fractional parts `Delta^(-1)`-separated within each
colour. The standard finite Fourier large sieve therefore gives

```text
sum_ell |sum_m A_m e(m alpha_ell)|^2
 << (M+Delta) sum_m |A_m|^2.
```

Since `M>=X` and `Delta=X^(3/5)`, (6) makes the right side
`M^2X^o(1)`. Cauchy in `ell` gives

```text
|T(Q,K)| <= Delta^(1/2) M X^o(1),
```

which is exactly (1). Subtracting `31/25` gives (2). At the smallest scale
the gap is `3/50`; at the maximal admissible scale
`theta+kappa=11/25`, it is `1/2`.

## Strategic implication

`PROVED` scoped no-go: treating (3) as an arbitrary divisor-bounded
coefficient vector and using only fractional-part separation cannot prove the
Cycle-66 target. The next estimate must retain at least one of:

- cancellation in the signed `b`-sum before taking absolute values;
- the exact phase `m(exp(2pi ell/Delta)-1)` through Poisson/stationary-phase
  analysis in `ell`;
- a major/minor-arc split whose major arcs produce seeded recurrence.

The equality of the smallest-scale deficit with the earlier `3/50` hybrid
gap is an exact exponent coincidence. No causal equivalence is asserted.

## Gate effect

E13 remains `PRIMITIVE_POISSON_X31_25_OR_SEEDED_RECURRENCE_OPEN`, now with
the generic folded-large-sieve route marked insufficient.
