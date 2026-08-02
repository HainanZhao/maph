# Cycle 93: the strict sub-alias branch is power-negligible

## Claim boundary

`PROVED`: for every fixed stationary buffer, the Cycle-87 branch

```text
0<|h-h'|<=c_* K/D                                  (1)
```

has arbitrary power decay after the smooth `k` sum, uniformly throughout
`16/25<=xi<58/75`.  Its complete contribution is `O_B(X^-B)` for every
fixed `B` after charging all polynomial support sums.

The transition `|h-h'|~K/D`, all nonzero stationary aliases, the unresolved
equal-height analytic branch, the full moment, and all density/interval
consequences remain open.

## Poisson kernel

Put

```text
t=D(h-h')/(2pi).
```

The crossed `k` phase from Cycle 87 is `t log k`. For a fixed smooth dyadic
weight, Poisson summation and `k=Kx` give kernels

```text
K integral U(x)e(t log(Kx)-mKx) dx,  m in Z.       (2)
```

Because `h-h'` is a nonzero integer,

```text
|t| >> D.                                          (3)
```

The fixed constant in (1) is chosen so that `|t|/(Kx)<=1/4` on the support.

## Derivative separation

For `m=0`, the derivative in (2) is `t/x`, whose magnitude is `>>D` by
(3). For `m!=0`, it is

```text
t/x-mK.
```

The stationary buffer gives magnitude `>>K` for `|m|=1`; for larger `|m|`
it is `>>(1+|m|)K`. Thus no Poisson integer is stationary anywhere on the
registered branch.

Repeated integration by parts, including derivatives of the fixed smooth
amplitudes, gives for every `A`

```text
sum_m |kernel_m| <<_A K D^-A.                      (4)
```

The `m!=0` tail is summable after two additional integrations if necessary.

## Complete support ledger

At `K=X^(xi+o(1))`, the support exponents are

```text
r,r' : xi,
h     : xi+1/3-3/5,
Delta h in (1): xi-3/5.
```

Their total is polynomial in `X`. Since `A` in (4) is arbitrary and
`D=X^(3/5+o(1))`, choose `A` after any requested fixed saving `B`; (4)
absorbs the full support and every smooth amplitude derivative. This proves
`O_B(X^-B)`.

## Gate effect

E14D-L advances to
`EQUAL_HEIGHT_BOUND_OR_WEB_AND_STATIONARY_ALIAS_TRANSITION_OPEN`.

