# Cycle 67 endpoint pullbacks and equality blow-up

## Four rational endpoint simplexes

Write the six nonnegative `S3` function values in source order as
`(a0,a1,a2,a5,a3,a4)`.  Within-class permutations preserve the deficit.
The four C64 fiber endpoints are therefore represented by

```text
cycle_equal = (z0,z1,z2,z3,z4/2,z4/2)
cycle_zero  = (z0,z1,z2,z3,z4,0)
trans_equal = (z0,z1/2,z1/2,z2,z3,z4)
trans_zero  = (z0,z1,z2,0,z3,z4),
```

where every `zi` is nonnegative and their sum is one.  These are exact
four-simplex parameterizations: the factors `1/2` convert the mass assigned to
a repeated pair into its two equal function values.

For each point put

```text
T = a1+a2+a5,   C = a3+a4,
a_cl = (a0,T/3,T/3,T/3,C/2,C/2).
```

The pullback program evaluates the frozen C63 source polynomial at `a` and
`a_cl` and subtracts.  At three rational points per family, that result agrees
exactly with the independently derived invariant polynomial under

```text
e=a0, t=T/3, c=C/2,
r2=sum_i (ai-t)^2, u=product_i(ai-t), s2=((a3-a4)/2)^2.
```

## Equality strata

The class-constant zero set in the four simplex coordinates is respectively

```text
cycle_equal: z1=z2=z3
cycle_zero:  z1=z2=z3 and z4=0
trans_equal: z1=2*z2 and z3=z4
trans_zero:  z1=z2=0 and z3=z4.
```

The denominator-16 grid zeros agree exactly with these conditions.  This is a
finite identity check, not a proof that there are no other real zeros.

## Nine radial charts

Every transposition probability triple can, after permutation, be written as

```text
(1-r)*(1/3,1/3,1/3) + r*(lambda,1-lambda,0),
```

with `r,lambda` in `[0,1]`.  Every cycle probability pair can, after swapping
the two cycles, be written as

```text
(1-s)*(1/2,1/2) + s*(1,0)
```

with `s` in `[0,1]`.  For a boundary family whose equality condition requires
two nonnegative deviations to vanish simultaneously, use
`rho=max(r,s)` and the two charts `(r,s)=(rho,rho*h)` and
`(rho*h,rho)`.  The two-equal transposition line has two directions from its
center, producing two further discrete charts.  This gives exactly nine
compact four-dimensional charts:

- one for `cycle_equal`;
- two for `cycle_zero`;
- four for `trans_equal`;
- two for `trans_zero`.

The formulas preserve normalization and are surjective onto their endpoint
families up to the proved within-class symmetries.  At `rho=0` they land on the
class-constant set.  Exact substitution proves that every chart deficit is
divisible by `rho^2`; no appeal to floating differentiation is used.  The
quotient is the object sent to domain-aware Bernstein certification.

## Secondary equality geometry

Exact integer polynomial division gives the global nonnegative factors

```text
cycle_equal: y^3 (1-x)^3
trans_equal: (1-x)^3
```

on the corresponding radial quotients.  The `r=0` restrictions of the
reduced `cycle_equal` and all four reduced `trans_equal` charts are divisible
by

```text
q(x,y)^2,  q(x,y)=1-y-3x+xy.
```

The zero curve is `x=(1-y)/(3-y)`.  Since `3-y >= 2`, the two charts

```text
x=(1-y)(1-s)/(3-y),  x=(1-y+2s)/(3-y)
```

cover the regions below and above it without changing sign after clearing the
positive denominator.  The full restriction to `q=0` is divisible by `r^2`.
The two max charts `(s,r)=(rho,rho*k)` and `(rho*k,rho)` cover the complete
unit square, including `rho=0` and the transition `s=r`.

For `trans_zero`, the analogous `r=0` factor is `(3x-1)^2`.  The charts
`x=(1-s)/3` and `x=(1+2s)/3`, followed by the same max blow-up, cover the
complete `x,r` square.  For `cycle_zero`, the trans-dominant radial chart
certifies directly.  The cycle-dominant chart is covered by
`(x,r)=(rho,rho*k)` and `(rho*k,rho)`; these are global square charts, not
merely local corner neighborhoods.

Every division above is an exact polynomial division.  Its zero divisor is
retained as the `rho=0`, `s=0`, `r=0`, or endpoint face of the transformed
closed cube, so no exceptional divisor is discarded.

## Exact Bernstein certificates

For a polynomial on a unit cube, nonnegative tensor-Bernstein coefficients
imply pointwise nonnegativity because the Bernstein basis functions are
nonnegative and sum to one.  The checker converts integer monomial
coefficients exactly and uses exact dyadic de Casteljau subdivision.  The
binomial table covers degrees through 63; the largest final chart degree is
41.  A prior degree-31 implementation was extended when the degree-40
`trans_zero` chart exposed the bound.  All final certificates were regenerated
with the extended checker.

The complete final cover is:

```text
cycle_equal and trans_equal: 20 joint charts, complete, depth <= 2
trans_zero:                    8 joint charts, complete, depth <= 1
cycle_zero cycle-dominant:     2 joint charts, complete at root
cycle_zero trans-dominant:     1 direct chart, complete, depth 4
```

The optimized source-pullback expansion and the independently derived
invariant expansion agree coefficient-for-coefficient on all nine radial
charts after accounting for their positive common scales.  The source route
uses the exact denominator LCM `11943936`; an earlier exploratory optimizer
incorrectly assumed denominator 64 and is not evidence for this result.

`PROVED`: for every nonnegative `S3` function in any of the four C64 endpoint
families,

```text
N(a)-N(a_cl) >= 0.
```

This proves the C67 boundary gate only.  It does not prove positivity at an
interior critical point of a C64 fiber, the full fixed-`S3` comparison, Zhao's
universal finite-group hypothesis, or Sidorenko for the Möbius graph.
