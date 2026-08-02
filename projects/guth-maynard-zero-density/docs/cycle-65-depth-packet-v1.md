# Cycle 65: depth reveals the exact recurrence threshold

## Claim boundary

`PROVED`: Cycle 64's harmonic packet mass is a sufficient upper bound that
forgets whether a primitive approximation persists under multiplication.
After retaining packet depth `K`, a dyadic packet `(q,K)` has weight exponent
`11/25+kappa`, and the sufficient packet-count target is

```text
N(theta,kappa) < X^(6/25-kappa)  (strictly),
theta+kappa<=11/25.                              (1)
```

A single packet can reach the pair-census target only at depth
`K>=X^(6/25)`. Such a packet can exist only when `q<=X^(1/5)`; strict
target excess requires strict inequalities. Thus the dangerous logarithmic
major-arc branch meets the Cycle-19 synchronization average-degree exponent
`6/25` exactly.

No bound for (1), recurrence theorem, powered saving, density gain, or
interval gain is proved.

## Exact depth ledger

Write

```text
epsilon_(ell,a/q)=|q alpha_ell-a|,
K=min(floor(H/q),floor(C/(X epsilon_(ell,a/q)))),
```

with the second entry interpreted as infinity for an exact rational value.
Then precisely the multiples `d=kq` with `k<=K` are certified by the packet,
and their pair-census weight is

```text
W(q,K)=sum_(k<=K)(H-kq)
      =KH-qK(K+1)/2.                              (2)
```

On a dyadic scale `q=X^(theta+o(1))`, `K=X^(kappa+o(1))`, the admissibility
condition is `theta+kappa<=11/25`, and (2) has exponent
`11/25+kappa`. Summing `N(theta,kappa)` packets and comparing with the strict
pair target `17/25` gives (1).

At maximal depth `kappa=11/25-theta`, (1) becomes

```text
N(theta,11/25-theta) < X^(theta-1/5).              (3)
```

Cycle 64's harmonic-mass target is exactly the maximal-depth envelope (3),
not the correct description of every low-denominator packet. In particular,
a shallow packet with `q<X^(1/5)` is not automatically a recurrence object.
The earlier conjectural phrase that a low-denominator packet by itself
"forces many differences" is superseded by the depth condition.

## The threshold coincidence

One packet reaches exponent `17/25` precisely when

```text
11/25+kappa >= 17/25,
```

or `kappa>=6/25`. Admissibility then gives

```text
theta <= 11/25-6/25=1/5.                           (4)
```

Thus the structured branch is not merely "small denominator." It is the
joint condition

```text
q <= X^(1/5+o(1)),   K >= X^(6/25-o(1)).           (5)
```

The exponent `6/25` is independently the popular-graph average-degree scale
at the critical skeleton target. Condition (5) therefore supplies a precise
interface: logarithmic transport should either prove discrepancy for the
shallow packet census or hand an `X^(6/25)` arithmetic-progression fan to the
existing recurrence/detector-surgery engines.

## Volume benchmark by depth

Depth `K` requires

```text
|alpha_ell-a/q| <= C/(q K X).
```

For `q` in a dyadic block of exponent `theta`, the union of these windows has
volume exponent `theta-kappa-1`. Sampling `Delta=X^(3/5)` curve points gives
the `OBSERVED` random-count exponent

```text
theta-kappa-2/5.
```

The gap from this benchmark to the target in (1) is

```text
(6/25-kappa)-(theta-kappa-2/5)=16/25-theta >= 1/5.
```

This uniform `1/5` reserve suggests that a dyadic first/second-spacing or
large-sieve theorem need not be sharp. It is only a scale benchmark, not a
proved discrepancy estimate for the exponential curve.

## New analytic target

`CONJECTURED` depth-packet dichotomy: after a subpower dyadic decomposition,
all scales with `K<X^(6/25)` satisfy (1) with a fixed or explicit endpoint
margin; every remaining scale either also satisfies (1) or produces a deep
packet satisfying (5), whose `K` multiples yield an arithmetic-progression
recurrence input with its approximation error retained.

The next proof attempt should preserve the approximation error rather than
rounding a packet to an exact rational progression. Candidate tools are a
depth-weighted large sieve on the curve `exp(2pi ell/Delta)-1`, a determinant
bound for three packets, and differencing in `ell` within fixed denominator
blocks.

## Gate effect

E13 advances to
`LOG_DEPTH_PACKET_DISCREPANCY_OR_X6_25_AP_RECURRENCE_OPEN`.
