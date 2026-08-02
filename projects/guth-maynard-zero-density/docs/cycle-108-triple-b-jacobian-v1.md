# Cycle 108: the triple-B scale Jacobian is summable

## Exact leading amplitude

`PROVED`. The three frozen one-dimensional stationary amplitudes are

```text
J_k=sqrt(c Delta)/m,
J_r=sqrt(c H)/n,
J_r'=sqrt(c(H-Delta))/n'.                          (1)
```

Their product is

```text
J=c^(3/2)sqrt(Delta H(H-Delta))/(m n n').          (2)
```

Along the Cycle-107 actual scale ray, all five variables
`(H,Delta,m,n,n')` are multiplied by `ell`. The numerator of (2) gains
`ell^(3/2)` and the denominator gains `ell^3`; hence

```text
J_ell=ell^(-3/2)J0.                                (3)
```

The three stationary evaluation points

```text
k*=c c0 Delta/m,
r*=c H/n,
r'*=c(H-Delta)/n'                                 (4)
```

are invariant. Smooth factors depending only on these points therefore do
not change along the scale ray.

## Absolute and BV summability

`PROVED`. Monotonicity and the integral test give

```text
sum_(ell<=L)ell^(-3/2)
 <=1+integral_1^L x^(-3/2)dx<3.                   (5)
```

The finite bounded-variation norm telescopes exactly:

```text
L^(-3/2)+sum_(ell<L)(ell^(-3/2)-(ell+1)^(-3/2))=1. (6)
```

Consequently, for arbitrary residual weights `omega_ell`,

```text
sum_(ell<=L)|omega_ell J_ell|
 <=3 J0 sup_(ell<=L)|omega_ell|.                   (7)
```

Thus the leading perfect-power stationary contribution loses no power from
the raw scale multiplicity whenever the residual envelope is `X^o(1)`. This
holds even at exact Cycle-107 phase resonance; geometric cancellation is an
optional stronger input.

## Boundary

The result isolates rather than assumes the remaining payload: arithmetic
weights, cutoff factors not expressible through the invariant stationary
points, and nonleading B-process remainders. No bound for those inputs,
aggregation across different cores, weak/simple-root estimate, complete
moment, density gain, or interval gain is proved.
