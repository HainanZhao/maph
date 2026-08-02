# Cycle 165 addendum preregistration v2: beta-anchored cross-fibre detector

## Status and scope

This is a post-trace addendum to the immutable typed-factorization
preregistration v1. The detector family derived before this addendum is
`EXPLORATORY`; the exact normalization and inverse question below are frozen
before the next proof attempt. It neither changes a sealed artifact nor
asserts an improvement in density, primes in intervals, or any L-function
family.

## Frozen state and kernel

- `Delta=X^(3/5)`, `H=X^(11/25)`, and
  `alpha_ell=exp(2pi ell/Delta)-1` on the registered compact curve chart.
- `beta` is one fixed external circular shift throughout the census.
- With the frozen Cycle-63 strip constant `C`, set
  `R=floor(X/(8C))` for sufficiently large `X`, and use
  `phi_R(t)=F_R(t)/R`, with `F_R` the Fejer kernel.
- Source atoms are `(h,ell,w_(h,ell))`, with `H<=h<=2H`, `0<=w<=1`, and
  `x_(h,ell)=h alpha_ell (mod 1)`. The integer `j` is recovered only when
  `beta` is within the Cycle-63 strip of `x_(h,ell)`.

## Registered identities and advance condition

Define

```text
D_(R,ell)(beta)=sum_h w_(h,ell) phi_R(beta-x_(h,ell)),
D_R=sum_ell D_(R,ell),
E_cross=int D_R^2-sum_ell int D_(R,ell)^2.
```

Prove, with the frozen constants, the physical-space identity

```text
E_cross=2 sum_(ell<ell') int D_(R,ell)D_(R,ell') >= 0,
```

and the implication

```text
T(beta0)>=X^(16/25+o(1))  =>  E_cross >> X^(7/25+o(1)),
```

using `t_ell<=H+O(1)` and Fejer positivity. The substantive advance condition is
then one of:

1. a proved diffuse-energy-versus-beta-localized-web inverse sufficient to
   bound the critical census; or
2. an explicit legal diffuse cross-energy saturator, with all labels and
   beta-cell occupancies recorded, showing exactly why this `L2` engine is
   insufficient.

## Falsifiers and prohibited substitutions

- A strip hit outside a uniform positive lobe of the frozen kernel falsifies
  the normalization.
- A legal chart with critical cross energy but subcritical every beta cell and
  no localized rational/low-rank web falsifies the desired inverse.
- Do not substitute the Cycle-66 primitive-Poisson phase as source ancestry:
  it is beta-free and may be used only later as an analytic estimate template.
- Do not call a same-ell hit family a Cycle-67 deep packet without separately
  checking the packet-depth approximation and its error.
