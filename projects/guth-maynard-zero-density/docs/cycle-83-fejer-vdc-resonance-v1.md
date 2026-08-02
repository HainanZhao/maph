# Cycle 83: fixed-center resonance closes a third Fourier band

## Claim boundary

`PROVED`: a Fejer majorant and the classical second-derivative exponential-
sum estimate give, uniformly for `k=X^(xi+o(1))` in the stated range,

```text
R_k=#{d~D: ||kc0 exp(2pi d/D)||<=1/Q}
 <<X^(xi/2+1/6+o(1)).                               (1)
```

The weighted annular version combines with the Cycle-82 smooth projector to
close every Fourier block `xi<37/75`.  The newly closed band is
`94/225<=xi<37/75`, of width `17/225`.  Equality at `37/75` ties and is not
promoted.

No estimate for `37/75<=xi<=83/75`, packet closure, density gain, or interval
gain is proved.

## Fejer majorant

Let `H` be an integer comparable to `Q`.  The nonnegative Fejer kernel

```text
F_H(x)=sum_(|j|<H)(1-|j|/H)e(jx)
```

has size `>>H` on `||x||<=1/Q`, after choosing the fixed comparison constant
in `H~Q`.  Therefore

```text
R_k << D/Q + Q^(-1)sum_(1<=j<=Q)|E_j|,             (2)
E_j=sum_(d~D)e(jkc0 exp(2pi d/D)).
```

Smooth dyadic endpoints cost only fixed derivative norms.

## Second-derivative estimate

For

```text
f_j(d)=jkc0 exp(2pi d/D),
```

the second derivative has fixed sign and satisfies

```text
|f_j''(d)|asymp jk/D^2                             (3)
```

on the frozen compact `d/D` support.  The classical van der Corput
second-derivative estimate therefore gives

```text
|E_j|<<D(jk/D^2)^(1/2)+(jk/D^2)^(-1/2)
      <<sqrt(jk)+D/sqrt(jk).                       (4)
```

Its hypotheses hold uniformly: at the proposed endpoint and `j<=Q`, the
largest second-derivative exponent is

```text
37/75+1/3-2(3/5)=-28/75<0.                         (5)
```

The same first/second derivative bounds are explicitly invoked in the
primary Guth--Maynard manuscript `arXiv:2405.20552v2`, in the proof of its
Poisson functional-equation lemma; the normalization in (4) is derived here
directly from (3).

Average (4) in (2).  Since

```text
Q^(-1)sum_(j<=Q)sqrt(jk)       <<sqrt(kQ),
Q^(-1)sum_(j<=Q)D/sqrt(jk)    <<D/sqrt(kQ),
```

we obtain

```text
R_k<<D/Q+sqrt(kQ)+D/sqrt(kQ).                      (6)
```

For every `xi>=94/225`, the middle term dominates the other two, giving
(1).

## Weighted annuli

Cycle 82 needs more than the central interval.  At dyadic radius `L/Q`, use
a Fejer kernel of bandwidth `H~Q/L`.  Formula (6) remains valid with `Q`
replaced by `Q/L`.  The smooth projector supplies a factor `L^(-A)` for any
fixed `A`; choosing `A=5` dominates the possible `L`, `L^(1/2)` growth in all
three terms.  Summing dyadic `1<=L<=Q` thus preserves the central power in
(1).

## Fourier ledger

The projector contributes `Q R_k` per frequency, with exponent

```text
1/3+(xi/2+1/6)=xi/2+1/2.
```

A block of `X^(xi+o(1))` frequencies has exponent

```text
3xi/2+1/2.                                         (7)
```

This is strictly below `31/25` exactly when

```text
xi<37/75.                                          (8)
```

The added width is

```text
37/75-94/225=17/225.                               (9)
```

## Strategic implication

The remaining range is `37/75<=xi<=83/75`.  In (6), the square-root
derivative term is now the exact one-variable lock.  The next routes are:

1. replace the classical `(1/2,1/2)` second-derivative behavior by a better
   exponent pair on the exponential phase;
2. average the fixed-center resonant counts over `k` before taking the
   Fourier `L1` norm;
3. classify saturation of the Fejer--VdC estimate as a rational/valuation
   web and hand it to E16.

## Gate effect

E14/E14D advance jointly to
`FEJER_VDC_BAND_CLOSED_HIGH_FREQUENCY_EXPONENT_PAIR_OPEN`.

