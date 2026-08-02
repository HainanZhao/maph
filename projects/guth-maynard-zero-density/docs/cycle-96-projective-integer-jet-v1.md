# Cycle 96: quantitative integer-jet separation

## Claim boundary

`PROVED`: the Cycle-95 projective Laurent residual has an explicit
quantitative lower bound in four registered integer-jet cases. This closes a
nontrivial small-mode sector once the displayed size conditions hold.

It is not proved that these conditions cover the full Poisson support. No
complete alias estimate, moment theorem, density gain, or interval gain is
proved.

## Abstract residual and integer jets

Let

```text
f(x)=A-B exp(ax)-C exp(bx),
```

where `A,B,C` are positive integers, `a,b` are integers not both zero, and
`x>0`. Define

```text
J0=A-B-C,             J1=Ba+Cb,
M=max(|a|,|b|),       S1=B|a|+C|b|,
S2=Ba^2+Cb^2.
```

Both `J0` and `J1` are integers. The exact derivatives are

```text
f'(t) =-Ba exp(at)-Cb exp(bt),
f''(t)=-Ba^2 exp(at)-Cb^2 exp(bt)<0.               (1)
```

The strict inequality holds because the mode is noncentral.

## The trichotomy with the double-zero case

### Nonzero constant jet

If `J0!=0`, then `|f(0)|>=1`. By the first identity in (1),

```text
|f(x)-f(0)|<=x exp(xM)S1.
```

Thus

```text
x exp(xM)S1<=1/2  implies  |f(x)|>=1/2.            (2)
```

### Zero constant jet and positive linear jet

Suppose `J0=0` and `J1>0`. Then `f'(0)=-J1<=-1`. Since `f''<0`, the
derivative only decreases, so

```text
f(x)<=-x,  hence |f(x)|>=x.                        (3)
```

No smallness condition is needed in this sign.

### Zero constant jet and negative linear jet

Suppose `J0=0` and `J1<0`. Now `f'(0)=-J1>=1`, but concavity can turn the
derivative. From (1), uniformly for `0<=t<=x`,

```text
|f''(t)|<=exp(xM)S2.
```

Consequently

```text
x exp(xM)S2<=1/2  implies  f'(t)>=1/2
```

throughout the interval, and therefore

```text
|f(x)|>=x/2.                                        (4)
```

### Both integer jets vanish

Finally suppose `J0=J1=0`. Since
`exp(at),exp(bt)>=exp(-xM)` on `[0,x]`, (1) gives

```text
f''(t)<=-exp(-xM)S2.
```

Twice integrating from `f(0)=f'(0)=0` yields

```text
|f(x)|>=exp(-xM)x^2S2/2.                           (5)
```

Here `S2>=1` by positivity and noncentrality. Equations (2)--(5) exhaust all
integer-jet cases.

## Entropy substitution

For Cycle 95 take

```text
(A,B,C)=(p0n,p0n',q0m),
(a,b)=(u,u+v),
x=2pi/D.
```

The exact stationary equation is `f(x)=0`. Therefore (2)--(5) give explicit
separation from stationarity wherever their registered sector hypotheses
hold. The difficult residual sector is now localized: it requires either a
nonzero constant jet with a large exponential displacement or a negative
linear jet whose derivative can turn before `2pi/D`.

## Gate effect

E14D-L remains
`EXACT_ALIASES_CENTRAL_NEAR_PROJECTIVE_MODES_QUANTITATIVE_OPEN`, but its
near-mode task is reduced to the two turnover sectors excluded by (2) and
(4), plus the question of whether the lower bounds (3) and (5) are strong
enough after reinsertion into the oscillatory integral.
