# Cycle 74: Huxley--Sargos closes a new numerator band

## Claim boundary

`PROVED`: the checked order-three Huxley--Sargos theorem applied in the
numerator variable gives fixed-denominator exponent

```text
w(theta,alpha)
 =min(alpha,max(0,alpha+1/10-theta/2)).              (1)
```

After summing denominators, a cell has packet-count exponent at most
`theta+w`. This closes a nonempty band beyond Cycle 73. For example,

```text
(theta,kappa,alpha)=(11/50,0,1/50)
```

ties the raw fraction target at `6/25`, but (1) gives count exponent `23/100`
and strict margin `1/100`.

No full residual-atlas estimate, recurrence theorem, powered saving, density
gain, or interval gain is proved.

## Checked theorem specialization

For fixed `q`, put

```text
y_q(a)=(Delta/(2pi))log(1+a/q).
```

On a dyadic numerator interval `a=X^(alpha+o(1))` with `a<=q`,

```text
|y_q^(3)(a)|asymp Delta/q^3
                =X^(3/5-3theta+o(1)).
```

The packet tube in the inverse-log coordinate has width

```text
Delta/(qKX)=X^(-2/5-theta-kappa+o(1)).
```

The order-three theorem used and hypothesis-checked in Cycle 47 gives four
fixed-`q` exponents:

```text
derivative: alpha+1/10-theta/2,
tube:       alpha-2/15-theta/3-kappa/3,
ratio:      (-1+2theta-kappa)/3,
constant:   0.
```

Throughout the registered atlas, the derivative term dominates the tube
term and the ratio term is negative. Taking the better of this theorem and
the trivial `X^alpha` numerator count proves (1).

The checked source chain is Zhao, arXiv:2407.01778, Theorem 2.1, together
with the primary Huxley--Sargos paper, *Acta Arithmetica* 69 (1995), 359--366,
as hash-pinned by Cycle 47.

## Closed pieces

For `theta<=1/5`, (1) equals the trivial exponent `alpha`, so Cycle 73 is
unchanged. For `theta>1/5`, write

```text
alpha_0=theta/2-1/10.
```

If `alpha<=alpha_0`, then `w=0`; the cell closes when

```text
theta+kappa<6/25.                                   (2)
```

If `alpha>=alpha_0`, then
`w=alpha+1/10-theta/2`; the cell closes when

```text
alpha+theta/2+kappa<7/50.                           (3)
```

Conditions (2)--(3) agree at `alpha=alpha_0`. The endpoint
`theta+kappa=6/25` ties on the lower piece and is not promoted.

## Strategic implication

The new band lies in `1/5<theta<6/25`. It is small but proof-grade: it shows
that classical one-denominator curvature already removes some cells after
the correct numerator resolution. The remaining cells require cancellation
across `q`, not a stronger pointwise application of the same theorem.

## Gate effect

E13 advances to
`NUMERATOR_HS_WEDGE_CLOSED_Q_AVERAGE_RESIDUAL_OPEN`.
