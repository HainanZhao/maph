# Cycle 70: factorization restores transport curvature

## Claim boundary

`PROVED`: the zero Hessian in Cycle 69 is caused by collapsing the product
frequency `m=rq'`. Holding the stationary index `k` fixed and restoring the
factors gives

```text
det Hess_(r,q') Psi(rq',k)
 =(u/(rq'))^2-1
 =exp(4pi x)-1,                                     (1)
```

where `x=ell/Delta` at stationarity. This is positive for every `ell>0`.

`PROVED`: dyadic `ell` blocks below exponent `6/25-kappa` are already
subcritical by packet uniqueness. On the remaining range, the determinant
in (1) has exponent at worst `-9/25-kappa`.

No two-variable exponential-sum estimate, full packet bound, recurrence
theorem, powered saving, density gain, or interval gain is proved.

## Factored Hessian

Write `psi(m)=Psi(m,k)` for fixed `k`, and put `m=rq'`. From Cycle 69,

```text
psi'(m)=u/m-1,
psi''(m)=-u/m^2.
```

For `F(r,q')=psi(rq')`, direct differentiation gives

```text
F_rr  =psi''(m)(q')^2,
F_q'q'=psi''(m)r^2,
F_rq' =psi''(m)m+psi'(m).
```

Therefore

```text
det Hess F
 =m^2(psi'')^2-(m psi''+psi')^2
 =-(psi')^2-2m psi' psi''
 =(u/m)^2-1.                                        (2)
```

At the stationary point, `u/m=exp(2pi x)`, proving (1). The full folding
`(r,q')->m` projects away exactly the direction in which (2) is nonzero.

## Small-endpoint split

Let a dyadic curve-index block have `ell=X^(lambda+o(1))`. Cycle 64 gives at
most one primitive packet per `ell`, so the block contains at most
`X^(lambda+o(1))` packets. The desired count exponent is
`6/25-kappa`. Consequently every block with

```text
lambda<6/25-kappa                                  (3)
```

is automatically subcritical, with a strict exponent margin after the usual
fixed dyadic buffer.

On the complementary range, `x=ell/Delta` has exponent at least

```text
(6/25-kappa)-3/5=-9/25-kappa.                       (4)
```

Since `exp(4pi x)-1 asymp x` near zero, (4) is also the weakest determinant
exponent. For `kappa=0` the loss is at most `9/25`; at the critical depth
`kappa=6/25` it is at most `3/5`.

## New analytic target

`CONJECTURED` unfurled-curvature estimate: on each surviving dyadic
`ell,r,q',b,k` block, retain `(r,q')` until after applying a two-variable
oscillatory estimate to the phase (2), paying less than the available packet
margin after the determinant loss in (4). The `b` sum remains outside this
phase estimate with its Möbius sign intact.

The immediate calculation required next is an exponent ledger for a
two-dimensional van der Corput, determinant, or decoupling bound on the very
unbalanced box

```text
r << bKX,   q' asymp Q/b,
```

whose product size `KXQ` is independent of `b`. A generic theorem that
depends only on product size and the determinant loss is preferable; a bound
paying the long `r` side trivially is unlikely to close.

## Gate effect

E13 advances to
`FACTORED_R_QPRIME_CURVATURE_WITH_ENDPOINT_LOSS_OPEN`.
