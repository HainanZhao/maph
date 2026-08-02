# Cycle 80: phase occupancy closes the first high-frequency band

## Claim boundary

`PROVED`: for every Fourier frequency `k=X^(xi+o(1))` in the Cycle-79
support, the maximum number of primal phases

```text
x_d=k c_0 exp(2pi d/Delta) mod 1
```

in a circular interval of length `O(1/Q)` is

```text
A_k<=X^(22/45+o(1)).                                (1)
```

A clustered large sieve then gives

```text
|S_k|<=X^(79/90+o(1)).                              (2)
```

Consequently every dyadic block

```text
4/15<=xi<163/450                                   (3)
```

is strictly below the raw Fourier target `31/25`. This extends the Cycle-79
trivial cutoff by `43/450`. Equality at `xi=163/450` ties and is not promoted.

No full high-frequency bound, ACSI, packet closure, powered saving, density
gain, or interval gain is proved.

## Occupancy estimate

For a circular interval centered at `t`, membership is equivalent, after
choosing an integer translate, to an integer lying within `O(1/Q)` of

```text
f(d)=k c_0 exp(2pi d/Delta)-t.
```

On `d~Delta`, the third derivative has exponent

```text
xi-3*(3/5)=xi-9/5.
```

The checked order-three theorem has exponents

```text
derivative: 3/10+xi/6,
tube:       22/45,
ratio:      22/45-xi/3,
constant:   0.                                      (4)
```

Uniformly for `0<=xi<=83/75`, the tube term `22/45` dominates: at the upper
endpoint the derivative term is `109/225`, smaller by `1/225`. This proves
(1), uniformly in the interval center and primitive anchor.

## Clustered large sieve

For arbitrary coefficients `b_d`, the standard circle-kernel Schur argument,
partitioned into intervals of length `1/Q`, gives

```text
sum_(q~Q)|sum_d b_d e(qx_d)|^2
 <<X^o(1) Q A_k sum_d|b_d|^2.                       (5)
```

The `X^o(1)` absorbs the logarithmic annular sum. Taking `b_d=1` and applying
Cauchy over the `Q` values of `q` yields

```text
|S_k|<=Q(A_k Delta)^(1/2).
```

Its exponent is

```text
1/3+(22/45+3/5)/2=79/90,                           (6)
```

proving (2).

## Fourier block ledger

A dyadic `k` block has `X^(xi+o(1))` frequencies. Combining this count with
(2) gives block exponent

```text
xi+79/90.                                           (7)
```

It is strictly below `31/25` exactly when

```text
xi<31/25-79/90=163/450.                            (8)
```

Since Cycle 79 already closes `xi<4/15`, the genuinely new width is

```text
163/450-4/15=43/450.                               (9)
```

## Strategic implication

The high-frequency problem is now restricted to

```text
163/450<=xi<=83/75.                                (10)
```

The argument is entirely primal and does not depend on an unsealed
stationary-phase remainder. The Cycle-79 double B-process is reserved for
(10), while Cycle-78 valuation webs remain the structured inverse branch.

## Gate effect

E14 advances to
`PRIMAL_OCCUPANCY_BAND_CLOSED_DUAL_HIGH_FREQUENCY_OPEN`.
