# Cycle 81: exact q-transform removes the stationary remainder

## Claim boundary

`PROVED`: for fixed smooth compactly supported positive-scale weights, the
Cycle-79 two-dimensional Poisson integral admits an exact one-variable
Fourier representation.  On its central support this representation equals
the predicted logarithmic-saddle main term with error
`O_(W,V)(D/(Qr^2))`.  The errors sum to `O_(W,V)(1)` for each `k`, and hence
to `X^(83/75+o(1))` across the full Fourier range, a strict `2/15` margin to
the `X^(31/25)` target.

No cancellation in the dual main sum, closure of
`163/450<=xi<=83/75`, packet closure, density gain, or interval gain is
proved.

## Exact transform

Freeze

```text
e(x)=exp(2 pi i x),   beta=2 pi,
hat V(y)=int V(t)e(-yt)dt.
```

After two-dimensional Poisson summation, one integral is

```text
I_(h,r)=int int W(d/D)V(q/Q)
 e(kc0 q exp(beta d/D)-hd-rq) dq dd.               (1)
```

Integrating first in `q` gives

```text
Q int W(d/D) hat V(Q(r-kc0 exp(beta d/D)))e(-hd)dd.
```

Put

```text
u=kc0 exp(beta d/D),  y=Q(u-r),
x_r=beta^(-1)log(r/(kc0)),
L=hD/beta,            a=L/(Qr).
```

The changes of variables are exact and give

```text
I_(h,r)=D/(beta r)e(L log(kc0/r))
 int hat V(-y) [r/(r+y/Q)]
 W(x_r+beta^(-1)log(1+y/(Qr)))
 e(-L log(1+y/(Qr)))dy.                            (2)
```

The weights are extended smoothly by zero, so (2) also covers support
boundaries without a separate sharp cutoff.

## Uniform expansion

On the central chart, `r~k`, `a` lies in a fixed compact set, and `Qr>=2`.
For `|y|<=cQr`, Taylor's theorem gives

```text
r/(r+y/Q)=1+O(|y|/(Qr)),
W(x_r+beta^(-1)log(1+y/(Qr)))=W(x_r)+O(|y|/(Qr)),
L[log(1+y/(Qr))-y/(Qr)]=O(a y^2/(Qr)).             (3)
```

Since `hat V` is Schwartz, its moments of every fixed order are finite; the
complement `|y|>cQr` is smaller than any fixed power of `Qr`.  Substituting
(3) into (2), then using

```text
int hat V(-y)e(-ay)dy=V(a),                        (4)
```

proves

```text
I_(h,r)=D/(beta r)W(x_r)V(a)e(L log(kc0/r))
        +O_(W,V)(D/(Qr^2)).                        (5)
```

This also independently fixes the sign: the leading weight is `V(a)`, not
`V(-a)`, and the phase is the Cycle-79 phase
`(hD/beta)log(kc0/r)` with no signature factor.

## Boundary and nonstationary charts

Enlarge the fixed supports of `W` and `V` once.  Outside the corresponding
`r~k`, `h~kQ/D` chart, either

```text
|kc0 exp(beta d/D)-r| >> k
```

or, after the `r` localization,

```text
|beta q r/D-h| >> kQ/D.
```

Repeated integration by parts in `q`, respectively `d`, followed by the
rapid decay of the smooth transforms, makes the summed complement
`O_A(X^-A)` for every fixed `A`, uniformly on the active high-frequency
range `k>=X^(163/450+o(1))`.  Transition indices remain in the central chart
and are already covered by the smooth zero extensions in (2)--(5).

## Error ledger

For `k=X^(xi+o(1))`, Cycle 79 gives

```text
#r=X^(xi+o(1)),
#h=X^(xi+1/3-3/5+o(1)),
error per (h,r)=X^(3/5-1/3-2xi+o(1)).
```

The exponents sum to zero.  Thus the central error is `X^o(1)` per `k`.
Summing all `k<=X^(83/75+o(1))` costs at most

```text
X^(83/75+o(1)),
31/25-83/75=2/15.                                  (6)
```

The remainder is therefore harmless for the exact Cycle-79 Fourier target.

## Strategic implication

The E14D gate is no longer a stationary-phase theorem.  It is the explicit
smooth dual inequality

```text
sum_k | sum_(r~k) D/(beta r) W(x_r)
             sum_(h~kQ/D) V(hD/(beta Qr))
             e((hD/beta)log(kc0/r)) |
 < X^(31/25+o(1)).                                 (7)
```

The next cycle should exploit the inner smooth `h`-sum as a resonance
projector and quantify the resulting logarithmic resonant set in `(k,r)`.
Exact Cycle-78 valuation webs remain the structured exceptional branch.

## Gate effect

E14D advances to
`EXACT_Q_TRANSFORM_SEALED_LOG_RESONANCE_PROJECTOR_OPEN`.

