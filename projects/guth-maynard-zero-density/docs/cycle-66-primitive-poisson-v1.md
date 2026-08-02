# Cycle 66: a scale-invariant primitive Poisson target

## Claim boundary

`PROVED`: the depth-packet count admits a nonnegative majorant whose exact
Möbius--Poisson expansion preserves primitive rational labels. Its diagonal
term has exponent

```text
theta-kappa-2/5,
```

at least `1/5` below the required packet-count exponent. After removing the
normalizing factor `(KX)^(-1)`, every dyadic scale has the same strict raw
off-diagonal target

```text
X^(31/25).                                           (1)
```

The participating Fourier frequencies are at most
`X^(1+theta+kappa+o(1))<=X^(36/25+o(1))`.

No bound for the off-diagonal form, packet discrepancy theorem, recurrence
theorem, powered saving, density gain, or interval gain is proved.

## A band-limited packet majorant

Fix the Fourier convention `e(x)=exp(2pi i x)`. For the registered constant
`C`, choose

```text
f_C(u)=A_C [sin(pi u/(2C))/(pi u/(2C))]^4,
```

where `A_C=(pi/2)^4`. Then `f_C` is nonnegative, at least one on
`[-C,C]`, integrable, and its Fourier transform is supported in a fixed
interval depending only on `C`.

The number `N(Q,K)` of primitive packets on one dyadic scale is at most

```text
M(Q,K)=sum_ell sum_(q~Q) sum_((a,q)=1)
       f_C(KX(q alpha_ell-a)).                       (2)
```

Unlike a periodic majorant of `||q alpha_ell||`, (2) retains the actual
integer numerator and therefore permits exact coprimality inversion.

## Möbius inversion before Poisson summation

Use

```text
1_((a,q)=1)=sum_(b|a,b|q) mu(b),
q=bq', a=ba'.
```

For each `b,q'`, Poisson summation in `a'` gives

```text
sum_(a' in Z) f_C(bKX(q' alpha_ell-a'))
 =1/(bKX) sum_(r in Z)
   fhat_C(r/(bKX)) e(rq' alpha_ell).                 (3)
```

Substitution into (2) yields the exact primitive form

```text
M(Q,K)=1/(KX) sum_(b,q': bq'~Q) mu(b)/b
        sum_r fhat_C(r/(bKX))
        sum_ell e(rq' alpha_ell).                    (4)
```

Thus primitivity is not discarded and rational multiples do not appear as
independent packets. The Möbius signs in (4) are structural information; an
absolute-value estimate before summing in `b` may erase the intended gain.

## Diagonal and off-diagonal ledgers

The term `r=0` in (4) is

```text
fhat_C(0)/(KX) sum_(q~Q) phi(q)/q * Delta.
```

At `Q=X^(theta+o(1))`, `K=X^(kappa+o(1))`, its exponent is

```text
theta-kappa-2/5.                                    (5)
```

Cycle 65's packet target is `6/25-kappa`. The diagonal margin is therefore

```text
(6/25-kappa)-(theta-kappa-2/5)
 =16/25-theta >= 1/5,                               (6)
```

because `theta+kappa<=11/25`.

For the off-diagonal part, the prefactor in (4) has exponent `-1-kappa`.
To put the normalized result strictly below `X^(6/25-kappa)`, it suffices to
prove that the raw signed form

```text
T(Q,K)=sum_(b,q': bq'~Q) mu(b)/b
       sum_(r!=0) fhat_C(r/(bKX))
       sum_ell e(rq' alpha_ell)                      (7)
```

has exponent strictly below

```text
(6/25-kappa)+(1+kappa)=31/25.                        (8)
```

The cancellation of `kappa` in (8) is exact. It replaces a two-parameter
atlas of desired estimates by one uniform target.

Since `fhat_C(r/(bKX))` vanishes unless `|r|<<bKX`, every composite frequency
`m=rq'` satisfies

```text
|m| << KX(bq') << KXQ,
```

whose exponent is at most `1+11/25=36/25`.

## Analytic interpretation

`CONJECTURED`: (7) is the correct shallow-packet theorem. It is a
Möbius-weighted exponential sum along
`alpha_ell=exp(2pi ell/Delta)-1`, with a maximum frequency only one fifth of
a power above the target in (8). A useful proof may combine:

- cancellation in the divisor variable `b`, retained before absolute values;
- van der Corput or exponent-pair control of `sum_ell e(m alpha_ell)`;
- a major-arc decomposition in `m`, routing failures to the deep-packet
  recurrence branch.

The square-root phase-volume benchmark lies below (8), but it is only an
`OBSERVED` plausibility check because the coefficients in (7) are highly
correlated.

## Gate effect

E13 advances to
`PRIMITIVE_POISSON_X31_25_OR_DEEP_PACKET_RECURRENCE_OPEN`.
