# Cycle 177: an actual positive-exponential rational-root saturator

## Claim boundary

`PROVED`: within the continuous-scale formulation frozen in Cycle 63, the
raw uniform beta-free pair target

```text
P < X^(17/25+o(1))
```

is false. For every fixed label proportion `0<c<1`, there is an infinite
actual positive-exponential family with

```text
P >>_c X^(22/25).
```

The excess is a single explicit rational-root ray. At beta zero the same ray
has a genuine central seed and an exact packet of depth `X^(11/25+o(1))`,
but its contribution to the direct triple census is only
`X^(11/25+o(1))`, below the required `X^(16/25)` total-census threshold.

Thus this is a scoped saturation/no-go for the **raw pair-census route**, not
a counterexample to a diagonal-aware direct triple census, a density theorem,
or a prime-interval result. If the underlying application later imposes an
additional arithmetic restriction on `Delta`, that restriction is outside the
Cycle-63 formulation and must be checked before applying this result.

## Exact rational-root family

Fix `0<c<1`. Choose once and for all an integer `r>=1` such that

```text
log(1+1/r) < 2 pi c.                                (1)
```

For every positive integer `L`, define the continuous scale

```text
Delta_L = 2 pi L / log(1+1/r),
X_L = Delta_L^(5/3),
H_L = X_L^(11/25)=Delta_L^(11/15).                  (2)
```

At the admissible label `ell=L`, since

```text
L/Delta_L = log(1+1/r)/(2 pi) < c,
```

we have the exact positive-exponential identity

```text
alpha_L = exp(2 pi L/Delta_L)-1 = 1/r.              (3)
```

No approximation or numerical recognition occurs in (3).

## Pair saturation

For every `d=kr<=H_L`,

```text
d alpha_L = k,
```

so it is an exact hit in the Cycle-63 pair condition. With
`m=floor(H_L/r)`, its contribution alone is

```text
P >= sum_(1<=k<=m)(H_L-kr)
   = m H_L - r m(m+1)/2.                             (4)
```

For `H_L>=4r`, retain only `k<=floor(H_L/(2r))`. There are at least
`H_L/(4r)` such integers and each summand is at least `H_L/2`; hence

```text
P >= H_L^2/(8r) >>_r X_L^(22/25).                   (5)
```

The raw pair target is `X_L^(17/25+o(1))`. The gap in (5) is the fixed power
`X_L^(1/5-o(1))`. In particular no uniform theorem of the frozen raw pair
form can be used as the Cycle-63 advance condition.

## Why this does not refute the direct census

Set `beta=0`. On the same label, the exact triple-strip rows are

```text
h=rk in [H_L,2H_L],       j=k,
j+beta-h alpha_L=0.                                  (6)
```

Their number is

```text
floor(2H_L/r)-ceil(H_L/r)+1 = H_L/r+O(1)
                                 =X_L^(11/25+o(1)).  (7)
```

This is the contribution of the constructed label only. It lies a fixed
power below the `X^(16/25)` direct-total-census target, and therefore does
not assert any upper-bound or lower-bound obstruction for the full census.
The Cauchy step from `P` to `T` is simply too diagonal-sensitive for this
single-label spike.

## The spike is a seeded deep packet

For `H_L>=8r`, put

```text
K=floor(H_L/(4r)),
m0=ceil(3H_L/(2r)),
h0=r m0,       j0=m0,
q=r,           a=1.                                 (8)
```

Then `H_L<=h0-rK<=h0+rK<=2H_L`, `qK<=H_L`, and

```text
j0-h0 alpha_L=0,
q alpha_L-a=0.                                      (9)
```

Thus every `|u|<=K` gives the exact seeded progression
`(h0+uq,j0+ua)` inside the row range. Since

```text
K >= H_L/(8r) = X_L^(11/25-o(1)),                   (10)
```

this has depth above the Cycle-65/67 critical `X^(6/25)` threshold by a
fixed `1/5` exponent. The rational-root obstruction is therefore precisely
the structured seeded-recurrence branch that a diagonal-aware replacement
must retain, rather than generic pair-census noise.

## Consequence

The next analytic target is not another uniform pair estimate. It must do
one of the following:

1. prove a diagonal-aware direct triple census after extracting all heavy
   seeded packets; or
2. route every heavy actual packet, with its beta seed and approximation
   error, into a recurrence bound strong enough for the E7/E9 skeleton.

The Cycle-165--176 terminal-web machinery remains parked: this family already
has a local seed and does not supply the missing cross-state population.
