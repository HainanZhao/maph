# Cycle 101: aggregate packing of generic critical fibers

## Claim boundary

`PROVED`: across all injective strong critical labels, the total Cycle-100
generic fiber has size

```text
<<_L Q M^(1/2+o(1)).                               (1)
```

At the actual maximal scales this has exponent `19/30`. Cross-valuation
webs, weak near-double rows, simple-root rows, the full alias moment, and all
density/interval consequences remain open.

## Compact rational packing

Let `N_j/R_j` be `J` distinct reduced positive rationals satisfying

```text
exp(-L)<=N_j/R_j<=exp(L),
z_j=min(N_j,R_j),       K_L=exp(L).                (2)
```

If `z_j<=Y`, then both numerator and denominator are at most `K_LY`.
Therefore

```text
#{j:z_j<=Y}<=K_L^2Y^2.                            (3)
```

Order the minimum heights increasingly. Equation (3) gives

```text
z_j>=sqrt(j)/K_L.
```

Consequently

```text
sum_(j<=J)1/z_j
 <=K_L sum_(j<=J)j^(-1/2)
 <=2K_L sqrt(J).                                   (4)
```

No Diophantine approximation theorem is needed; this is finite rational
packing.

## Summing the generic fibers

Cycle 100 proves for each label

```text
F_generic(j)<=2Q tau(|w_j|)/z_j.                  (5)
```

Put `T_M=max_(n<=2M)tau(n)`. The Cycle-99 strong compiler makes the rational
labels distinct across signed `w`, and `1<=|w|<=2M`, so `J<=4M`. Combining
(4)--(5),

```text
sum_j F_generic(j)
 <=4K_L Q T_M sqrt(J)
 <=8K_L Q T_M sqrt(M).                             (6)
```

The standard divisor bound gives `T_M=M^o(1)`, proving (1). With

```text
Q=X^(1/3+o(1)),       M<=X^(3/5+o(1)),
```

the exponent in (1) is

```text
1/3+(1/2)(3/5)=19/30.                              (7)
```

This is a square-root saving in the mode range compared with the naive
`QM` fiber envelope.

## Remaining structured rows

Equation (6) charges only Cycle-100 generic splits. Every excluded strong
row has a recorded cross-valuation

```text
gcd(s/g0,R)>1  or  gcd(t/g0,N)>1.
```

Thus the strong near-double branch has a rigorous generic estimate plus an
explicit exceptional web. Weak localization and simple algebraic roots remain
separate analytic branches.

## Gate effect

E14D-L advances to
`GENERIC_STRONG_CRITICAL_AGGREGATE_X19_30_CROSS_VALUATION_WEAK_SIMPLE_OPEN`.
