# Cycle 103: critical-scale algebraic alias inverse

## Exact critical homogeneity

`PROVED`. Fix one Cycle-102 core and write `W=s+t`, `r=N/R`,

```text
r=C0*t/(B0*s),  B=lambda*B0,  C=lambda*C0.
```

The critical point is `t*=log(r)/W`, independent of `lambda`. With

```text
K=B0*r^(s/W)+C0*r^(-t/W),
```

the full critical value is exactly

```text
f(t*)=A-lambda*K.                                  (1)
```

Indeed, the critical derivative identity is

```text
B0*s*r^(s/W)=C0*t*r^(-t/W),
```

because the ratio of the left side to the right side is
`(B0*s/(C0*t))*r=1`. Scaling `B0,C0` by `lambda` leaves the critical point
fixed and gives (1).

## Algebraic scale number

`PROVED`. Put `alpha=r^(1/W)`. It is a positive root of
`R alpha^W-N=0`; hence `[Q(alpha):Q]<=W`. Since

```text
K=B0*alpha^s+C0*alpha^(-t),
```

`K` is positive algebraic and `deg(K)<=W`. No useful height or irrationality
measure is asserted.

## Transfer of the near-double tolerance

`PROVED`. In the strongly localized Cycle-97 branch, its Taylor estimate at
the actual critical point gives

```text
|A-lambda*K|
 <= epsilon
 :=delta+2eta^2/ell+2Leta^2/ell^2.                (2)
```

Thus the scale multiplier is not a free divisor multiplicity: every surviving
scale is an `epsilon`-hit of the near-integer orbit `lambda*K`.

## Scale-alias inverse theorem

`PROVED`. Suppose `J>=2` distinct integers `lambda` in `[1,Lambda]` satisfy
`||lambda*K||<=epsilon`. Sorting the hit scales, one adjacent gap obeys

```text
1<=q<=floor((Lambda-1)/(J-1)).
```

Subtracting its two nearest-integer relations gives

```text
||qK||<=2epsilon.                                  (3)
```

If `q_epsilon` is the least positive `q<=Lambda-1` satisfying (3), every two
hit scales are separated by at least `q_epsilon`; consequently

```text
J<=1+floor((Lambda-1)/q_epsilon).                  (4)
```

If no such `q` exists, `J<=1`.

## Implication and boundary

Cycle 100's raw `lambda` multiplicity is replaced by the exact dichotomy
“one critical-value hit or a short algebraic scale alias.” A short alias is
structured output for E16, not cancellation. Closing the exceptional web
still requires a quantitative separation theorem for `K`, an aggregate
count of aliased cores, or cancellation from the actual stationary phases.
Weak near-double and simple-root rows remain open.
