# Cycle 35: three kernel engines and the entropy--volume match

## Claim boundary

`PROVED`: the Cycle 34 unweighted-kernel problem has three exact sufficient
formulations: a hollow fractional restriction estimate, a low-time
sieve-curvature estimate, and a phase-entropy accumulation estimate. An
elementary phase-histogram lemma supplies the entropy defect of each large
value, and ordinary integer correlations exhibit the required curvature
scale.

`OBSERVED`: none of the three prime-specific analytic inputs is proved. In
particular, cancellation for an unrestricted integer interval does not
transfer to a prime-pair subsequence. No kernel-count, zero-density, or
short-interval improvement is claimed.

Throughout,

```text
K(t)=sum_(X<p<=2X)p^(-it),       M=# {X<p<=2X}=X^(1+o(1)),
H=X^(12/5), Delta=X^(3/5),       V=X^(7/10),
delta=V/M=X^(-3/10+o(1)).
```

The point `t=0` is removed at a cost of one row.

## 1. Hollow fractional restriction

For `q=24/5`, every threshold row contributes

```text
V^q=X^(84/25).
```

Consequently the strong discrete estimate

```text
sum_(t in C)|K(t)|^(24/5) <= X^(21/5+o(1))             (1)
```

on every `Delta`-separated
`C subset {t:Delta<=|t|<=H}` implies

```text
|C|<=X^(21/5-84/25+o(1))=X^(21/25+o(1)).              (2)
```

`PROVED`: the frozen Cycle 14 global moment scale is `X^(24/5+o(1))`.
Thus (1) asks for exactly `X^(3/5)` more saving, equal to the row spacing.
This is not cosmetic: the coherent value at zero alone contributes
`|K(0)|^(24/5)=X^(24/5-o(1))`, so (1) is false unless the coherent spike is
hollowed out. The new object is therefore a separated, off-origin weak or
strong restriction theorem, not the old global fractional moment.

## 2. Sieve-curvature differencing

Let `a_n` be the indicator of primes in `[X,2X]`, extended by zero, and set

```text
C_r(t)=sum_n a_(n+r)a_n exp(-it log((n+r)/n)).          (3)
```

The finite van der Corput inequality with shift length comparable to `X`
gives

```text
|K(t)|^2 <= X^o(1)(X+sum_(1<=r<=X)|C_r(t)|).           (4)
```

Hence the aggregate prime-pair estimate

```text
sum_(1<=r<=X)|C_r(t)| <= X^(2+o(1))/|t|               (SPC)
```

would imply, for `|t|>=X^(3/5+eta)` and any fixed
`0<eta<2/5`,

```text
|K(t)|<=X^(7/10-eta/2+o(1)).                           (5)
```

Thus `(SPC)` excludes all threshold rows between
`X^(3/5+eta)` and the range on which it is proved. The boundary interval
`Delta<=|t|<=X^(3/5+eta)` contains only `X^(eta+o(1))` separated rows, below
the target for every fixed `eta<21/25`.

There is an exact elementary model for `(SPC)`. Removing the prime weights,
put

```text
I_r(t)=sum_n exp(-it log((n+r)/n)).                     (6)
```

When `|t|<=cX` and `r<=cX`, the phase derivative has constant sign, is
monotone, and has size comparable to `|t|r/X^2` without crossing a nonzero
multiple of `2pi`. The first-derivative estimate and the trivial bound give

```text
|I_r(t)| << min(X,X^2/(|t|r)),
sum_(r<=cX)|I_r(t)| << X^2 log X/|t|.                  (7)
```

`PROVED`: (7) reproduces precisely the curvature needed by (5) in the
low-time range. `OBSERVED`: (7) does **not** prove `(SPC)` because deleting
the composite indices can destroy cancellation. The first new analytic gate
is a sifted first-derivative principle for the shifted-prime correlations
(3), preferably on average over `r`. High times `X<|t|<=H` remain a separate
stationary/resonant branch even if that gate is closed.

## 3. Phase entropy and its exact budget

For one fixed `t`, let `mu_t` be the empirical distribution of
`-t log p mod 2pi` over the dyadic primes. Rotate so its first Fourier
coefficient is nonnegative. Partition the circle into `L` equal arcs, let
`q_j` be the empirical arc masses, `u_j=1/L`, and represent each arc by its
centre `z_j`.

The arc-centre approximation gives

```text
|sum_j q_j z_j| >= delta-pi/L.
```

Since `sum_j u_j z_j=0`, choosing `L>=2pi/delta` yields

```text
||q-u||_1>=delta/2.
```

Pinsker's inequality (natural logarithms) therefore gives the unconditional
finite-histogram lemma

```text
D(q||u)>=delta^2/8=X^(-3/5-o(1)).                      (8)
```

`PROVED`: every large kernel row carries an entropy defect on exponent
`-3/5`. Therefore a prime-log accumulation theorem

```text
sum_(t in C)D(q_t||u) <= X^(6/25+o(1))                 (PEA)
```

would imply

```text
|C|<=X^(6/25+3/5+o(1))=X^(21/25+o(1)).                (9)
```

The exponent `6/25` is exactly the residual spectral-shift/exterior-volume
scale from Cycles 20 and 23. This entropy--volume equality is an exact
cross-engine match: the total information carried by a target-sized family
is on the same scale as the determinant collapse forced by its common
projection.

## 4. Route selection

`PROVED` reduction: the three live targets see different information.

1. `(1)` asks for the spacing factor inside a hollow fractional restriction
   inequality.
2. `(SPC)` asks a sieve to preserve curvature cancellation in shifted-prime
   pairs and attacks low times pointwise.
3. `(PEA)` asks phase information to accumulate no faster than the already
   identified residual-volume budget.

The next cycle should first test whether `(PEA)` can be derived from a
relative-entropy/determinant identity for the normalized prime Gram matrix.
If that identity loses more than `X^o(1)`, pursue `(SPC)` via a bilinear
Selberg/Vaughan majorant that retains the oscillatory phase. The hollow
fractional estimate remains the common weak-type benchmark against which
either route is measured.
