# Cycle 97: algebraic-root inverse atlas

## Claim boundary

`PROVED`: every real zero of the projective Laurent residual has a positive
algebraic exponential coordinate of explicitly bounded defining degree and
coefficient norm. A small nonzero residual either lies quantitatively close
to such a simple root or carries a simultaneous small-derivative certificate;
in the strongly localized latter case it lies near an explicit algebraic
critical point.

No effective lower bound for the resulting logarithmic linear form, complete
alias estimate, moment theorem, density gain, or interval gain is proved.

## Algebraic root encoding

Let

```text
f(t)=A-B exp(at)-C exp(bt),
```

where `A,B,C` are positive integers and `a,b` are integers not both zero.
Put

```text
M=max(|a|,|b|),   s=max(0,-a,-b),   W=A+B+C
```

and collect equal powers in

```text
P(Y)=A Y^s-B Y^(s+a)-C Y^(s+b).                    (1)
```

All exponents in (1) are nonnegative. The exponent-coincidence split from
Cycle 95 shows directly that `P` cannot be identically zero in a noncentral
mode. Moreover

```text
deg(P)<=2M,       ||P||_1<=W,                      (2)
f(t)=exp(-st)P(exp(t)).                            (3)
```

Thus a real root `r` of `f` gives a positive algebraic number
`alpha=exp(r)` with `P(alpha)=0`. Its degree is at most `2M`. The standard
Mahler-measure factor bound and `M(P)<=||P||_2<=W` give the safe, deliberately
loose height ledger

```text
h(alpha)<=log W + (1/2)log(2M+1).                  (4)
```

## Concavity and the explicit critical point

Differentiation gives

```text
f'(t) =-Ba exp(at)-Cb exp(bt),
f''(t)=-Ba^2exp(at)-Cb^2exp(bt)<0.                 (5)
```

Hence `f'` is strictly decreasing, `f` has at most one real critical point,
and `f` has at most two real roots. A critical point can exist only when
`ab<0`; in that case it is unique and satisfies

```text
exp((a-b)t*)=-Cb/(Ba).                             (6)
```

Therefore `exp(t*)` is itself an explicitly presented positive algebraic
number of degree at most `|a-b|`.

## Local inverse theorem

Fix `x>0` and write

```text
delta=|f(x)|, eta=|f'(x)|, S2=Ba^2+Cb^2,
L=S2 exp(M(x+1)), ell=S2 exp(-M(x+1)),
tau=max(2delta,2sqrt(L delta)).                     (7)
```

Assume first that `delta>0` and `eta>=tau`. Set
`z=-2f(x)/f'(x)`. Then `|z|<=1`; Taylor's theorem and (7) give

```text
f(x+z)=-f(x)+R,       |R|<=Lz^2/2<=delta/2.
```

Thus `f(x)` and `f(x+z)` have opposite signs. There is a real root `r`
between them, and

```text
|r-x|<=2delta/eta.                                 (8)
```

By (3), `alpha=exp(r)` is algebraic with the ledger (2)--(4).

If instead `eta<tau`, the output is the simultaneous certificate

```text
|f(x)|=delta,       |f'(x)|<tau.                   (9)
```

This is the near-double-root branch; no root is inferred merely from (9).
If additionally `eta<=ell/2`, same-sign modes are impossible: from (5) their
derivative magnitude is at least
`exp(-Mx)S2/M>ell/2`. Hence `ab<0`. On `[x-1,x+1]`, (5) has magnitude at
least `ell`; monotonicity locates the unique critical point from (6) within

```text
|t*-x|<=2eta/ell.                                  (10)
```

Taylor's theorem also gives

```text
|f(t*)|<=delta+2eta^2/ell+2Leta^2/ell^2.           (11)
```

Equations (9)--(11) are an explicit rational coefficient/mode certificate,
not an anonymous analytic loss.

## Entropy linear-form contract

For the actual substitution

```text
(A,B,C,a,b,x)=(p0n,p0n',q0m,u,u+v,2pi/D),
```

the simple-root output (8) becomes

```text
|D log(alpha)-2pi|<=2D delta/eta.                  (12)
```

Cycle 97 therefore isolates the remaining external input exactly: an
effective lower bound for (12) at the degree, height, coefficient, and mode
scales actually reached by the Poisson support. The near-double branch must
instead be counted through the explicit critical relation (6).

## Gate effect

E14D-L advances to
`ALGEBRAIC_ROOT_OR_NEAR_DOUBLE_INVERSE_BANKED_EFFECTIVE_SEPARATION_OPEN`.
