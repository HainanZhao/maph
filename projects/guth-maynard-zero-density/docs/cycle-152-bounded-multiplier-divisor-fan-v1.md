# Cycle 152: order-one strict-halo cancellation has a bounded-multiplier divisor fan

## Claim boundary

`PROVED`: conditional on the already licensed smooth strict-halo class
carrying normalized negative relative mass at least a fixed `kappa>0`, and on
a fixed uniform complete per-mode bound `n_b<=Cw_b/m_b`, a single bounded
multiplier `m_0<=ceil(2C/kappa)` carries a positive fixed fraction of that
negative mass.  Its denominators form the explicit labelled fan

```text
h_b=m_0 d_b,       d_b|h,       gcd(m_0,h/d_b)=1.
```

This is an inverse/concentration reduction, not an incidence upper bound.
It does not bound the fan, exclude its negative tails, treat boundary
denominators or other escape classes, or prove a full moment, density, or
prime-interval result.

## The normalized strict-halo input

Fix the Cycle-149 witness denominator `h`.  For every selected smooth,
positive-chart, strict-denominator halo mode, retain the Cycle-151 labels

```text
d_b=gcd(h,h_b),       m_b=h_b/d_b,
L_b=h m_b,
tau_b=KQ(c0g^b-r_b/h_b),       gcd(r_b,h_b)=1.    (1)
```

The selected class remains inside the literal Cycle-151 region

```text
h_b <= QX^(-delta_*),       L_b<=cK,              (2)
```

with fixed `delta_*,c>0`.  Let `w_b>=0` be its positive chart weights,
normalized by `sum_b w_b<=1`.  Write `n_b>=0` for actual negative relative
mass after the fixed tail-transform/Riemann error and all admitted aggregate
negligible errors have been included.  The sole analytic input needed here is
the uniform complete bound

```text
0 <= n_b <= C w_b/m_b,                             (3)
```

for a fixed `C<infinity`.  It follows in the intended application from the
Cycle-151 relative capacity `d_b/h_b=1/m_b` and a uniform bound for the
complete fixed-chart tail contribution.  This document does not establish
that uniform analytic bound for new classes; it uses it only as the explicit
condition of the inverse.

Assume the strict class has target negative mass

```text
sum_b n_b >= kappa>0,                              (4)
```

where `kappa` is fixed independently of `X`.

## Large multipliers cannot carry the target

Set

```text
M_0=ceil(2C/kappa).                                (5)
```

For modes with `m_b>M_0`, (3) and weight normalization give

```text
sum_(m_b>M_0) n_b
 <= C sum_(m_b>M_0) w_b/m_b
 <= C/M_0 sum_b w_b
 <= C/M_0
 <= kappa/2.                                       (6)
```

Consequently the modes with `m_b<=M_0` carry at least `kappa/2` negative
mass.  There are at most `M_0` possible positive values of `m_b` in this
range, so one value `m_0` satisfies

```text
1<=m_0<=M_0,
sum_(m_b=m_0)n_b >= kappa/(2M_0).                  (7)
```

This is the bounded-multiplier concentration step.  It uses neither an
absolute aggregation nor a spacing or curvature estimate.

## Exact divisor fan

For every mode in the extracted `m_0` class, (1) gives

```text
h_b=m_0d_b,       d_b|h.                           (8)
```

Since `d_b=gcd(h,h_b)`, substitute (8) and divide by `d_b` to obtain

```text
gcd(h/d_b,m_0)=1.                                  (9)
```

Conversely, (8)--(9) imply `gcd(h,m_0d_b)=d_b`; the fan description is exact,
not merely a containment.  The extracted inverse therefore retains

```text
(b,d_b,m_0,r_b,tau_b,w_b,n_b),
```

including numerator, tail, sign, and coefficient information.  It does not
collapse to a count of divisors of `h`.

## Consequence and remaining problem

The E14D-L alternative “produce a divisor-fan inverse” is now met in the
conditional strict smooth-halo branch: order-one negative mass forces a
bounded-multiplier fan with a quantitative retained mass.  What remains is
to estimate or classify this labelled fan—using spacing, order-three
curvature, or a sharper fan model—without discarding its tail and coefficient
data.  Boundary denominators, phase-changing charts, nonsmooth payload, and
unbounded-tail regimes remain outside this theorem.
