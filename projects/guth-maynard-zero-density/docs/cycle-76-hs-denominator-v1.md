# Cycle 76: denominator curvature closes a second wedge

## Claim boundary

`PROVED`: applying the checked order-three Huxley--Sargos theorem in `q` for
each fixed numerator gives fixed-`a` exponent

```text
u(theta,alpha)
 =min(theta,1/10+alpha/6+theta/3).                  (1)
```

After summing the `X^(alpha+o(1))` numerators, the packet-count exponent is
at most `alpha+u`. This closes a nonempty part of the combined Cycle-75
residual. In particular,

```text
(theta,kappa,alpha)=(6/25,0,0)                     (2)
```

ties the prior banked target at `6/25`, while (1) gives `9/50`, a strict
margin `3/50`.

No full denominator-average theorem, seed extraction, powered saving,
density gain, or interval gain is proved.

## Checked theorem specialization

For fixed positive `a`, put

```text
Y_a(q)=C log(1+a/q), C=Delta/(2pi).
```

On `a=X^(alpha+o(1))`, `q=X^(theta+o(1))`, direct differentiation gives

```text
|Y_a'''(q)|asymp Delta*a/q^4
                =X^(3/5+alpha-4theta+o(1)).         (3)
```

The tube exponent remains `-2/5-theta-kappa`. The Cycle-47 theorem therefore
has the fixed-`a` exponents

```text
derivative: 1/10+alpha/6+theta/3,
tube:       2theta/3-2/15-kappa/3,
ratio:      (-1+3theta-alpha-kappa)/3,
constant:   0.                                      (4)
```

On the registered atlas, the derivative term exceeds the tube term by

```text
7/30+alpha/6-theta/3+kappa/3 >=13/150,
```

and exceeds the ratio term by

```text
13/30+alpha/2-2theta/3+kappa/3 >=7/50.
```

It is also positive. Taking the minimum with the trivial denominator count
`X^theta` proves (1).

## New closed band

The estimate improves the trivial fixed-`a` count precisely when

```text
theta>3/20,
alpha<4theta-3/5.                                  (5)
```

On this branch, strict packet closure is equivalent to

```text
7alpha/6+theta/3+kappa<7/50.                       (6)
```

The genuinely new region is the intersection of (5)--(6) with Cycle 75's
live condition `B+kappa>=6/25`. The witness (2) lies in that intersection.
At `(theta,kappa,alpha)=(6/25,0,9/175)`, (6) is an equality and is not
promoted.

## Strategic implication

This is the first proof-grade regional gain obtained by averaging in the
denominator direction. It confirms that the affine E14 geometry contains
usable cancellation, but the unique Cycle-75 worst point
`(1/3,1/3,8/75)` remains untouched: there (1) reproduces the banked exponent
`3/5`. The next theorem must therefore be genuinely two-dimensional or use
the shifted multiplicative structure of E15.

## Gate effect

E13 advances to
`DENOMINATOR_HS_WEDGE_CLOSED_TWOD_OR_SHIFTED_RESIDUAL_OPEN`.
