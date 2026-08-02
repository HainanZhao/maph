# Cycle 73: numerator resolution closes more cells and sharpens curvature

## Claim boundary

Let `a=X^(alpha+o(1))` with `0<=alpha<=theta`. `PROVED`: the numerator cell
closes both the strict packet and weighted pair targets whenever

```text
theta+alpha+kappa<6/25.                             (1)
```

On the remaining cells, the exact factored-Hessian loss is

```text
X^(theta-alpha),                                    (2)
```

not the coarse denominator loss `X^theta`.

Equality in (1) ties. No full packet theorem, two-variable exponential-sum
estimate, recurrence theorem, powered saving, density gain, or interval gain
is proved.

## Cellwise fraction budget

There are `X^(theta+o(1))` denominators `q` in the registered block and only
`X^(alpha+o(1))` numerators in the dyadic `a` block. Packet injectivity gives

```text
N(theta,kappa,alpha)
 <=X^(theta+alpha+o(1)).                             (3)
```

Comparing (3) with `X^(6/25-kappa)` proves (1). Multiplying by the packet
weight `X^(11/25+kappa)` yields pair exponent

```text
11/25+kappa+theta+alpha,
```

which is strictly below `17/25` under exactly the same condition.

Cycle 71 is recovered by maximizing `alpha` at `theta`, which turns (1) into
`2theta+kappa<6/25`. Numerator resolution is strictly stronger on cells near
the primitive endpoint. For example, bounded numerators at `theta=1/5` and
`kappa=0` close with margin `1/25`, although the coarse fraction wedge does
not.

## Relation to the curve index

Packet accuracy and `alpha_ell asymp ell/Delta` give

```text
a asymp q ell/Delta.
```

If `ell=X^(lambda+o(1))`, then

```text
alpha=theta+lambda-3/5,
lambda=3/5+alpha-theta.                             (4)
```

The positive-numerator cutoff in Cycle 72 is the endpoint `alpha=0` of (4).

## Cellwise curvature

Cycle 70 gives

```text
det Hess_(r,q')=exp(4pi ell/Delta)-1.
```

On a small-ratio dyadic cell, (4) implies

```text
ell/Delta asymp a/q=X^(alpha-theta),
```

so the determinant has exponent `alpha-theta` and the loss is (2). In the
bulk `alpha=theta`, curvature is constant-scale; only small numerators pay a
power loss.

## Residual atlas

The shallow analytic problem is now restricted to

```text
theta+alpha+kappa>=6/25,
0<=alpha<=theta,
theta+kappa<=11/25.                                 (5)
```

The desired two-variable theorem should be tested on (5) with determinant
loss `theta-alpha`, not on the coarser denominator atlas.

## Gate effect

E13 advances to
`NUMERATOR_RESOLVED_RESIDUAL_CURVATURE_OPEN`.
