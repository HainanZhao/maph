# Cycle 100: exact critical-fiber divisor switch

## Claim boundary

`PROVED`: the oriented Cycle-99 critical fiber has an exact one-dimensional
divisor-switch formula. Its generic part satisfies an explicit divisor bound;
every nongeneric row is an identified cross-valuation web between the mode
split and the reduced rational label.

No bound for that exceptional web, weak near-double rows, complete alias
moment, density gain, or interval gain is proved. No Möbius sign is imported
from a different representation.

## Exact fiber parametrization

Fix a nonzero signed `w`, put `W=|w|`, and write

```text
s=|a|,       t=|b|,       s+t=W.                  (1)
```

The sign of `w` fixes which of `a,b` is positive, so (1) does not introduce
an extra orientation factor. Let `(N,R)=1` be the reduced critical label. The
fiber equation is

```text
CtR=BsN,       1<=B,C<=Q.                          (2)
```

For a fixed split, put `g=gcd(sN,tR)`. Reducing the ratio in (2) proves that
all solutions, without omission or repetition, are

```text
B=lambda*tR/g,       C=lambda*sN/g,
1<=lambda<=Q*g/max(sN,tR).                         (3)
```

Therefore the exact unsigned fiber size is

```text
F=sum_(s=1)^(W-1)
  floor(Q*gcd(sN,(W-s)R)/max(sN,(W-s)R)).          (4)
```

## Exact valuation factorization

Let `g0=gcd(s,t)` and write `s=g0s1`, `t=g0t1`. Since
`(s1,t1)=(N,R)=1`, prime-by-prime valuation gives

```text
gcd(sN,tR)=g0*gcd(s1,R)*gcd(t1,N).                 (5)
```

The three factors in (5) have distinct meanings:

1. `g0` is the ordinary gcd of the mode split;
2. `gcd(s1,R)` is a cross-valuation from the positive mode part to the label
   denominator;
3. `gcd(t1,N)` is the opposite cross-valuation.

The atlas records the side and every prime-power valuation in factors 2--3.

## Generic fiber bound

Define the generic sector by both cross-valuations in (5) being one. Then
`g=g0`. Also

```text
max(sN,tR)>=min(N,R)max(s,t)>=min(N,R)W/2.
```

Using `floor(y)<=y` and

```text
sum_(s=1)^(W-1) gcd(s,W)<=W tau(W),
```

equation (4) gives

```text
F_generic<=2Q tau(W)/min(N,R).                     (6)
```

Thus large generic multiplicity is possible only for a low-height critical
label. Every other excess is already routed to the explicit cross-valuation
web in (5).

## Sign provenance correction

Cycle 66 has a Möbius sign in its primitive packet representation. The
Cycle-87 stationary-alias expansion used here is currently recorded with
smooth atom weights and oscillatory B-process phases; no proved bridge maps
the Cycle-66 divisor variable to `(B,C,s,t)`. Consequently (4)--(6) are
unsigned structural statements. Later cancellation must reinsert the actual
stationary phases and amplitudes, rather than assume an unavailable sign.

## Gate effect

E14D-L advances to
`GENERIC_CRITICAL_FIBER_BOUNDED_CROSS_VALUATION_WEB_AND_LOW_HEIGHT_OPEN`.
