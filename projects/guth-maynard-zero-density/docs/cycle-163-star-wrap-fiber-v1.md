# Cycle 163: star wrap-fiber dichotomy

## Claim boundary

`PROVED`: every labelled Cycle-162 oriented star has the exact effective
support factorization `R=R_wrap R_fiber`. Thus, conditionally on
`R>=X^(1/300-o(1))`, it has either integer-wrap complexity or common-wrap
fiber complexity at least `X^(1/600-o(1))`. Splitting the Cycle-162 stars by
their actual `D_s^2` weight, either the wrap-complexity stars retain a fixed
global share or the common-wrap stars do. In the latter case the aggregate
common-wrap squared edge mass is `>>A2^2X^(1/200-o(1))`; it is not asserted
for one fiber. The latter arm yields the stated labelled logarithmic relation.

No transport seed, moment, density, or interval result is proved.

## Exact split

For star leaf weights `x_v`, group leaves by their frozen half-open integer
wrap. With the preregistered notation, `sum_mE_(s,m)=E_s`, so cancellation
free algebra gives

```text
R_wrap R_fiber=(D_s^2/sum_mD_(s,m)^2)(sum_mD_(s,m)^2/E_s)=R_s.    (1)
```

Set `H=X^(1/600-o(1))`. If `R_wrap>=H`, preserve the weighted integer-wrap
complexity inverse. Otherwise `R_wrap<H`, so (1) and Cycle 162 force
`R_fiber>=H`, while `sum_mD_(s,m)^2=D_s^2/R_wrap>D_s^2/H`. Thus only this
complementary common-wrap arm has the claimed mass. Split the star family by
the actual weights `D_s^2`; one of the two arms has at least half that global
weight. If it is the common-wrap arm, summing the actual Cycle-162 star edge
scale `sum_sD_s^2>>A2^2X^(1/150-o(1))` gives the claimed aggregate `1/200`
scale.

For leaves with a common wrap, subtract their two frozen relations. Since
`z_(d,q)=c0q exp(2pi d/D)` and `z_v asymp Q`, the mean-value estimate for
`log` gives

```text
|log(q_v/q_w)+2pi(d_v-d_w)/D| << 1/(KQ).           (2)
```

All wrap, atom, coefficient, orientation, and phase-sector labels persist.

## Gate effect

This is a labelled coordinate pullback, not yet a usable transport seed. The
next action must either compile the common-wrap log web through E16 or bound
the explicit weighted integer-wrap complexity alternative.
