# Cycle 47: classical near-curve machinery misses by `1/25`

## Claim boundary

`PROVED` from the checked theorem hypotheses and exact exponent arithmetic:
the Huxley--Sargos near-integer theorem gives the Cycle 46 inverse-log curve
count `X^(8/25+o(1))`; among derivative orders `3<=k<=20`, order three is
best. This improves the naive `X^(11/25)` alias count, but misses the required
`X^(7/25+o(1))` by exactly `X^(1/25)`.

`PROVED` correction: Cycle 46's `X^(-7/25)` quantity is the graph second
derivative `|y''|`, not Euclidean curvature. The Cycle 46 inverse-wrap
equivalence and exponent identities remain valid; only the geometric name
and the proposed comparison class require correction.

No de-aliasing theorem, `LCAM_s`, density, or interval gain is proved.

## 1. Checked Huxley--Sargos specialization

For

```text
y(j)=(Delta/(2pi))log(1+(j+beta)/h),
Delta=X^(3/5), h=X^(11/25), delta=X^(-21/25),
```

translate the `j=O(h)` interval to `[N,2N]` with `N asymp h`. For every
fixed order `k`, the logarithmic derivatives have constant sign and satisfy

```text
|y^(k)(j)| asymp Delta/h^k = X^((15-11k)/25),
```

with a comparison constant depending only on `k` and the frozen
fixed-proportion interval. Thus the hypotheses of the Huxley--Sargos theorem
displayed in Zhao, Theorem 2.1, hold uniformly in `beta`.

That theorem gives

```text
R << N lambda_k^(2/(k(k+1)))
     + N delta^(2/(k(k-1)))
     + (delta/lambda_k)^(1/k) + 1.                  (1)
```

For `k=3`, the four exponents in (1) are

```text
8/25, 4/25, -1/25, 0.
```

Hence `R<<X^(8/25+o(1))`. Exact enumeration of `3<=k<=20` shows no other
registered order improves `8/25`; the derivative/major-arc term is the lock.
The desired count `X^(7/25+o(1))` is therefore only `X^(1/25)` beyond this
classical input.

The source used for the formula and hypotheses is
[Zhao, arXiv:2407.01778, Theorem 2.1](https://arxiv.org/abs/2407.01778),
an exposition of the primary Huxley--Sargos theorem that also records and
repairs an oversight in the earlier proof presentation. The primary paper is
[Huxley--Sargos, Acta Arithmetica 69 (1995), 359--366](https://doi.org/10.4064/aa-69-4-359-366).

## 2. Euclidean geometry correction

At the critical scale,

```text
y'                 = X^(4/25),
|y''|              = X^(-7/25),
Euclidean arclength= X^(15/25),
Euclidean curvature=|y''|/(1+y'^2)^(3/2)=X^(-19/25),
radius of curvature= X^(19/25),
normal tube width  = X^(-21/25)/X^(4/25)=X^(-1).
```

The affine arclength is

```text
integral |y''(j)|^(1/3) dj = X^(26/75+o(1)).
```

Howard--Trifonov Theorem 7.7 applies after the vertical-to-normal tube
conversion: its small-tube hypotheses hold because `L delta_geo=X^(-10/25)`
and `delta_geo=X^(-1)<<1/R_2`. Its count term
`L/R_1^(1/3)` also has exponent `26/75`, larger than `8/25` and the target.
See [Howard--Trifonov, arXiv:2207.09532, Theorem 7.7](https://arxiv.org/abs/2207.09532).

Huxley's `7/11` lattice-discrepancy exponent concerns a differently scaled
closed-curve discrepancy problem. `OBSERVED`: its numeral coincides with the
Cycle 45 alias power, but no checked implication to this thin inverse-log
tube follows.

## 3. New research target

`CONJECTURED` logarithmic-major-arc saving (`LMAS`): for the above inverse-log
family, the order-three derivative term in (1) admits an extra
`X^(-1/25+o(1))`, uniformly in `beta`.

The Huxley--Sargos proof identifies that term with points organized into
low-degree rational major arcs. The next engine should use the special
differential-algebraic identity of the logarithm—or average over the prime
parameter before maximizing in `beta`—to rule out a full population of those
major arcs. Generic convexity or a higher derivative order will not close the
gate.

## Gate effect

`PROVED` partial de-aliasing: replace the naive alias exponent `11/25` by
`8/25`, leaving exactly `1/25`. E7 becomes
`LOG_MAJOR_ARC_SAVING_1_25_OR_NONLATTICE_ROW_OPEN`.
