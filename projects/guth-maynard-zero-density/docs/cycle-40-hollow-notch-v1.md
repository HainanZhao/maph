# Cycle 40: global collision means cannot see the hollow target

## Claim boundary

`PROVED`: every amplified polynomial `F_(m,s)` has a large positive-kernel
mean-value floor caused by its compressed frequency bandwidth and positive
coefficient mass. Summed over the harmonic vector, that floor exceeds
`AMPR_3` by exponent `19/10` and `AMPR_4` by `29/10`.

This is a scoped obstruction to an **unmodified global positive-kernel
mean-value proof**. It is not a counterexample to the hollow discrete
estimates, because their row sets exclude `|t|<Delta`, while the floor may be
entirely supplied by the coherent neighborhood of zero.

`OBSERVED`: no kernel-count, density, or interval improvement is proved.

## 1. Bandwidth after removing the carrier

Write

```text
F_(m,s)(t)=sum_n a_n n^(-it),       sum_n a_n=M^(s+1),
```

with `a_n` the nonnegative multiplicities from Cycle 39. Multiplication by
the common phase `X^((s+m)it)` does not change the modulus. The centered
frequencies

```text
lambda_n=log(n/X^(s+m))
```

lie in an interval of length at most `(s+m)log 2 < s+m`. Thus the relevant
bandwidth is `O(s+m)`, not `(s+m)log X`.

## 2. A positive-kernel floor

For any exponential polynomial `G(t)=sum_j a_j exp(-it lambda_j)`, direct
integration gives

```text
integral_(-H)^H (1-|t|/H)|G(t)|^2 dt
 =H sum_(j,k) a_j a_k sinc^2(H(lambda_j-lambda_k)/2). (1)
```

Partition an interval of length `s+m` into bins of width `1/H`. There are at
most `3H(s+m)` bins when `H(s+m)>=1`. Pairs in one bin have sinc-square at
least `1/4`. If `A_r` is the coefficient mass in bin `r`, positivity and
Cauchy--Schwarz give

```text
(1) >=(H/4)sum_r A_r^2
     >=(H/4)(sum_r A_r)^2/[3H(s+m)]
     =M^(2s+2)/[12(s+m)].                             (2)
```

This proof uses only nonnegative coefficients and the frozen bandwidth. It
is uniform in `m>=2`.

## 3. Exponent comparison

At `m<=A=X^(3/10)`, the fixed-`m` floor in (2) has exponent at least

```text
2s+2-3/10.
```

Summing (2) over `m<=A` actually gives exponent `2s+2`, since
`sum_(m<=A)1/(s+m)` is logarithmic. The registered comparisons are:

| `s` | global vector floor | `AMPR_s` target | excess |
|---:|---:|---:|---:|
| 3 | `8` | `61/10` | `19/10` |
| 4 | `10` | `71/10` | `29/10` |

Therefore a global Fejer/mean-value upper bound cannot possibly occur at the
`AMPR_s` scale. Counting ordinary `1/H` near collisions without first
removing the coherent component is mis-scaled by a fixed power.

## 4. The new analytic object

The desired estimate is discrete and hollow:

```text
Delta<=|t|<=H,       Delta=X^(3/5).
```

The positive floor (2) can be concentrated in a neighborhood of zero of
width `O(1/m)`, so it does not refute `AMPR_s`. It instead forces the proof to
use a **notched restriction operator**: remove or orthogonally project away
the coherent zero packet before measuring arithmetic off-diagonal mass.

A viable next theorem must provide one of:

1. an annular sampling inequality whose kernel vanishes on the coherent
   packet but remains positive on the hollow row set;
2. a centred Gram operator with the zero-packet rank-one component removed,
   followed by a spectral bound on the residual; or
3. a shifted/differenced formulation in which the constant phase packet
   cancels before the prime-monomial near-collision count is formed.

No bound for this notched operator is asserted here.

## Gate effect

`PROVED` route correction: raw global collision counting is removed from the
lead actions. E7 is now `HOLLOW_NOTCHED_AMPLIFIED_RESTRICTION_OPEN`.
`AMPR_3` and `AMPR_4` remain live, but their proof must hollow the operator
before invoking frequency spacing. The independent E9 shifted-prime route
already performs a difference and therefore becomes a natural candidate for
constructing the notch.
