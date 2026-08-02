# Cycle 162 preregistration: mass-sensitive high-cell extraction

Date frozen: 2026-08-02 UTC.

## Frozen input and conventions

Assume the conditional Cycle-89 upper-band excess in the actual Cycle-160
atom model. Retain every Cycle-160 off-diagonal cell `I`, its labels, and

```text
L_I=sum_(r in I)|b_r|,
rho_I=sum_(r in I)|b_r|^2,
C_I=L_I^2/rho_I  (zero when rho_I=0).
```

Freeze `eta_*=1/75`, `theta_*=1/100`, `tau=X^(-1/300)`, the Cycle-160
nonnegative smooth cutoff and its Schur constant, and Cycle 161's `B=288`
half-open circular difference/phase refinement. Thus
`eta_*-theta_*=1/300`; all `o(1)` slack is strictly below `1/600`.

Let `N` be the frozen number of nonzero labelled atoms. Assign every
positive-codegree cell deterministically to the half-open dyadic level

```text
2^j X^theta_* <= C_I < 2^(j+1) X^theta_*,
0 <= j <= ceil(log_2(N(N-1)/X^theta_*)).
```

The lower-bound boundary is included and the upper boundary belongs to the
next level. Zero-codegree cells are excluded after recording their zero
contribution.

## Required result

Derive from Cycle 160 and the forced excess

```text
sum_I C_I rho_I = sum_I L_I^2 >> A2^2 X^(eta_*-o(1)).             (1)
```

Cells below `X^theta_*` contribute at most
`A2^2X^theta_*`, negligible against (1) by the frozen `1/300` margin.
After the frozen dyadic partition, retain a level `R<=C_I<2R`,
`R>=X^theta_*`, with

```text
sum_(I in level)L_I^2 >> A2^2X^(eta_*-o(1)).                     (2)
```

Apply Cycle 161 to every refined class of every cell in this level. Since
`sum_jL_(I,j)^2>=L_I^2/B`, retain only classes with
`C_(I,j)>=X^theta_*/(2B)`. The discarded refined classes carry at most
`L_I^2/(2B)`, so the retained classes carry at least `L_I^2/(2B)`. One
aggregate output is therefore either:

1. coefficient-weighted positive-real, four-distinct-atom mass of scale
   `>>A2^2X^(eta_*-o(1))`; or
2. a consistently oriented labelled star family with certificate provenance
   `sum L_(I,j)^2 >>_B A2^2X^(eta_*-o(1))`, actual oriented squared edge mass
   `sum D_(I,j,or)^2 >>_B A2^2X^(1/150-o(1))`, and individual effective
   neighbor degree at least
   `tau^2X^theta_*/(8B)=X^(1/300-o(1))/(8B)`.

## Falsifier and boundary

An admissible Cycle-89 excess row whose high-codegree levels do not carry
(2), or for which the Cycle-161 alternatives together lose a fixed fraction
of (2), falsifies this target and halts its promotion.

No rational web, coordinate pullback, moment estimate, density improvement,
or interval improvement is claimed. The post-Cycle-162 decision is only
whether to pull back the globally massed four-cycle arm or the weighted
star-family arm through `z_(d,q)=c0 q exp(2pi d/D)`.

## Companion checkpoint

The persistent companion `/root/guth_maynard_session_mentor` was checked
live, reactivated under the same stable identity, and recommended this target
on 2026-08-02 UTC. It identified mass-sensitive extraction as a prerequisite
to either coordinate pullback. The primary adopts that recommendation and
freezes the stated constants, deterministic levels, falsifier, and no-
promotion boundary.
