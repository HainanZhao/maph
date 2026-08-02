# Cycle 186: actual-curve convexity grid exclusion

## Claim boundary

`PROVED`: three deep shifted rational rays on the actual curve can be
excluded without an arithmetic-progression assumption whenever their weighted
exponential convexity lies strictly between the retained rational
approximation error and the cleared three-denominator grid.

`PROVED`: in the explicit scale fixture `Delta=T^15`, `X=T^25`, depths at
least `T^2+1`, and denominators in `[T^9,2T^9]`, this excludes three
consecutive labels for all sufficiently large `T` in a fixed compact chart.
The replay certifies a conservative `T=100`, `C=1`, chart-cap-`1000` instance.

This is local crowding exclusion only. It does not bound a critical box of
separated labels, defeat the Cycle 185 AP-free occupancy, force a recurrence,
or prove a density or prime-interval improvement.

## The sandwich

Let `z=exp(2*pi/Delta)`, `a<b<c`, `q=b-a`, `p=c-b`, and `r=p+q`. Set
`B_i=A_i+U_i`, so `B_i/U_i` approximates `z^i` with the retained C182 error.
The curve has positive weighted convexity

```text
C_curve = p*z^a + q*z^c - r*z^b > 0.                     (1)
```

For `f(x)=exp((2*pi/Delta)x)`, the linear-interpolation remainder and
`f''(x)=(2*pi/Delta)^2*f(x)` give, in the compact chart,

```text
p*q*r*(2*pi/Delta)^2/2 <= C_curve
 <= p*q*r*(2*pi/Delta)^2*exp(2*pi*c0)/2.                  (2)
```

The corresponding rational difference has denominator dividing
`U_a*U_b*U_c`. If `E` bounds its retained row-depth error and

```text
E < lower(C_curve),
upper(C_curve)+E < 1/(U_a*U_b*U_c),                        (3)
```

then it is both positive and a nonzero rational smaller than its denominator
grid, a contradiction. This uses the actual curve `z^i=1+alpha_i`, not a
mass/capacity model.

## Explicit local regime

For consecutive labels, take `Delta=T^15`, `X=T^25`,
`N_i-1>=T^2`, and `T^9<=U_i<=2T^9`. C182 gives total weighted error at most
`8C/T^36`. Using `6<2*pi<44/7`, (2) is between `36/T^30` and
`(44/7)^2*exp(2*pi*c0)/T^30`; the rational grid is at least `1/(8T^27)`.
Thus (3) holds once `T` is large relative to the fixed chart and strip
constants.

## Gate effect

The result adds an actual-curve local-density constraint missing from Cycle
185. Its present packing strength is insufficient: forbidding only local
triples still permits a sparse separated support at the critical mass scale.
The next archive-oriented cycle should test whether full rectangle weights can
amplify this, or bank a separated-support model showing why they cannot.

