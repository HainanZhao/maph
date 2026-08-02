# Cycle 84: averaging resonances closes a fourth Fourier band

## Claim boundary

`PROVED`: summing the smooth resonance projector jointly over a dyadic
frequency block and the curve index gives Fourier-`L1` exponent

```text
max(xi+3/5,14/15,xi+2/3).                          (1)
```

Consequently every block `xi<43/75` is strictly closed.  This adds
`37/75<=xi<43/75`, of width `2/25`, beyond Cycle 83.  Equality at `43/75`
ties and is not promoted.

No estimate for `43/75<=xi<=83/75`, packet closure, density gain, or interval
gain is proved.

## Joint Fejer incidence

Let `K=X^(xi+o(1))` and, at dyadic projector radius `L/Q`, define the
cumulative incidence

```text
I_L(K)=#{(k,d): k~K,d~D,
          ||k c0 exp(2pi d/D)||<<L/Q}.
```

A Fejer majorant of bandwidth `H~Q/L` gives

```text
I_L(K)<<KD L/Q+(L/Q)sum_(1<=j<=Q/L)|B_j|,          (2)
B_j=sum_(k~K,d~D)e(jk c0 exp(2pi d/D)).             (3)
```

All weights are fixed smooth dyadic weights; endpoints change constants
only.

## Crossing lemma

For fixed `j`, sum (3) first in `k`.  Smooth Poisson summation gives a rapidly
decaying projector onto

```text
||j c0 exp(2pi d/D)||<<1/K.                        (4)
```

The real function in (4) is monotone, has derivative comparable to `j/D`,
and crosses `O(j)` integers on the frozen compact support.  In a neighborhood
of radius `M/K` around all crossings, the number of integer `d` is at most

```text
O(j)+O(DM/K):                                      (5)
```

there is at most one discretization point per crossing plus the total length
of all crossing intervals.  Multiplying (5) by the `K M^(-A)` projector
weight and summing dyadic `M`, with fixed `A>2`, proves

```text
|B_j|<<D+jK.                                       (6)
```

This includes exact rational-anchor multiples: they occupy crossing points
and are charged to `jK`, not removed as exceptions.

Substituting (6) into (2) yields

```text
I_L(K)<<KD L/Q+D+KQ/L.                             (7)
```

## Fourier ledger

The Cycle-82 outer projector contributes `Q L^(-5)`.  At `L=1`, the three
terms of (7) therefore have exponents

```text
volume:   xi+3/5,
length:   14/15,
crossing: xi+2/3.                                  (8)
```

For larger dyadic `L`, the incidence terms grow by at most `L`, remain
constant, or decay by `L^-1`; `L^-5` makes every annulus strictly smaller.
On the active range, the crossing term in (8) dominates.  It is below the
raw target precisely when

```text
xi+2/3<31/25,
xi<43/75.                                          (9)
```

The newly closed width is

```text
43/75-37/75=2/25.                                  (10)
```

## Exact remaining lock

The formal volume term `xi+3/5` would close through

```text
xi<31/25-3/5=16/25.                               (11)
```

Thus the one-point-per-crossing discretization term stops the incidence
engine `1/15` earlier than volume at the new endpoint.  The next theorem
must show that only a power-saving fraction of the `O(j)` crossings carry an
integer `d`, or classify the saturated crossings as an explicit anchor web.
Above `xi=16/25`, even a volume-optimal unsigned incidence count is
insufficient and signed cancellation must replace triangle inequality.

## Gate effect

E14 advances to
`AVERAGED_RESONANCE_BAND_CLOSED_CROSSING_INVERSE_OPEN`.

