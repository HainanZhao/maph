# Cycle 64: logarithmic transport reduces to primitive Farey mass

## Claim boundary

`PROVED`: every Cycle-63 beta-free resonance belongs to a unique primitive
packet `(ell,a/q)` at the frozen scales. Distinct packets do not share `ell`
or the reduced rational `a/q`. All hits in a packet have `d=kq,j=ka`, and
their total weight in the Cycle-63 pair census is at most `H^2/(2q)`.

Consequently, the sufficient pair target `P<X^(17/25)` reduces to

```text
sum_(primitive logarithmic packets) 1/q < X^(-1/5)  (strictly).   (1)
```

No estimate for the packet mass in (1) is proved, and no powered, density, or
interval gain follows.

## Packet uniqueness

A hit satisfies

```text
|d alpha_ell-j|<=C/X,
alpha_ell=exp(2pi ell/Delta)-1.
```

After reducing `j/d=a/q`, with `d=kq`,

```text
|alpha_ell-a/q|<=C/(dX)<=C/(qX).                    (2)
```

Two distinct reduced fractions of denominators at most `H` differ by at
least `H^(-2)=X^(-22/25)`. The combined worst-case windows in (2) have scale
`X^(-1)`, smaller by `X^(-3/25)`. Thus one `ell` cannot have two reduced
approximants.

On the fixed-proportion `ell` range,

```text
alpha_(ell+1)-alpha_ell asymp Delta^(-1)=X^(-3/5).
```

This is larger than the windows in (2) by `X^(2/5)`, so one reduced fraction
cannot serve two distinct `ell`. The packets are therefore injective in both
coordinates.

## Multiplicity inside one packet

If `(ell,a/q)` is fixed, every hit has `d=kq,j=ka`. Ignoring the additional
error restriction only enlarges the packet, and

```text
sum_(k<=H/q)(H-kq) <= H^2/(2q).                     (3)
```

Summing (3) over packets gives

```text
P <= (H^2/2) sum_packets 1/q.                       (4)
```

Since `H^2=X^(22/25)`, Cycle 63's strict target
`P<X^(17/25)` becomes (1).

## Scale of the new target

For each denominator `q`, the union of the `O(q)` rational windows in a
bounded `alpha` interval has total length `O(1/X)`. Sampling
`Delta=X^(3/5)` curve points suggests packet count `X^(-2/5)` per
denominator scale in volume terms. With harmonic weight `1/q`, the random
packet-mass exponent is `-2/5` up to logarithms, leaving `1/5` exponent room
to the required `-1/5`.

This volume calculation is `OBSERVED` heuristic scale, not a discrepancy
theorem. Rational alignment of the logarithmic curve is the only remaining
source of excess mass.

## Analytic target

`CONJECTURED` logarithmic Farey-packet dichotomy: on every registered scale,
either

```text
sum_(ell,a/q reduced)
  1/q * 1_{|exp(2pi ell/Delta)-1-a/q|<=C/(qX)}
 <= X^(-1/5-epsilon)                                (5)
```

for some fixed `epsilon>0` (or at the endpoint with an explicit strict
logarithmic margin), or a packet with harmonic mass above this threshold is
extracted as a structured low-denominator branch.

The second branch is necessary: if `Delta` is allowed to vary, one can tune
`exp(2pi ell/Delta)-1` to a rational value for an individual `ell`. Thus a
uniform small-mass theorem without a structured exception is not the stated
target. A heavy packet fixes one unique `(ell,a/q)` and forces many
differences `d=kq`; it should be routed to an arithmetic-progression
recurrence or detector-surgery module rather than counted as generic noise.

Candidate mechanisms are a determinant bound for three packets, a
first/second spacing argument by denominator scale, or exponentiation to a
rational approximation for `exp(2pi ell/Delta)` followed by a quantitative
logarithmic-form estimate.

## Gate effect

E13 advances to
`LOG_FAREY_PACKET_MASS_OR_LOW_DENOMINATOR_RECURRENCE_OPEN`.
