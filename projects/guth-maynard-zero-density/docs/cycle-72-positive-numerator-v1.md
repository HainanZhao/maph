# Cycle 72: primitivity sharpens the curvature loss to `X^theta`

## Claim boundary

`PROVED`: every primitive packet with `q>1` has positive numerator `a>=1`.
Consequently

```text
ell >> Delta/q,                                     (1)
```

and the Cycle-70 factored Hessian satisfies

```text
det Hess_(r,q') Psi(rq',k)
 >> X^(-theta-o(1)).                                (2)
```

Thus the relevant determinant loss is `X^theta`, replacing the nonsharp
Cycle-70 worst-case loss `X^(9/25+kappa)`. The earlier bound remains true;
it is superseded only as the strategic estimate.

No two-variable exponential-sum estimate, full packet theorem, recurrence
theorem, powered saving, density gain, or interval gain is proved.

## Positive numerator

Since `alpha_ell>0` and the packet error is `o(1)`, its nearest integer
numerator satisfies `a>=0`. If `a=0`, then

```text
gcd(a,q)=gcd(0,q)=q.
```

The reduced condition `(a,q)=1` therefore forces `q=1`. On every growing
dyadic denominator scale, `q>1` and hence `a>=1`.

The packet inequality gives

```text
q alpha_ell >= 1-o(1).
```

On the registered fixed small-proportion range,
`alpha_ell asymp ell/Delta`, proving (1). At
`q=X^(theta+o(1))`, the curve-index exponent must satisfy

```text
lambda>=3/5-theta.                                  (3)
```

## Curvature consequence

At the Cycle-70 stationary point,

```text
x=ell/Delta >> 1/q=X^(-theta+o(1)).
```

Since `exp(4pi x)-1 asymp x` near zero, the exact factored Hessian obeys
(2). At the largest denominator `theta=11/25`, the loss is at most `11/25`;
for smaller denominators it improves proportionally.

Cycle 70 used only packet cardinality and obtained determinant exponent at
least `-9/25-kappa`. Primitivity gives the stronger cellwise exponent
`-theta`. The denominator `q=1` is a constant-size branch and must be handled
separately rather than included in (2).

## Numerator-scale parametrization

Writing `a=X^(alpha+o(1))`, the relation
`a asymp q ell/Delta` gives

```text
alpha=theta+lambda-3/5,
0<=alpha<=theta.                                    (4)
```

This supplies a natural fifth coordinate for the unfurled atlas. The
near-endpoint `alpha=0` corresponds to bounded positive numerators, not to a
zero numerator or a vanishing primitive packet.

## Gate effect

E13 becomes
`FACTORED_CURVATURE_LOSS_XTHETA_ON_RESIDUAL_ATLAS_OPEN`.
