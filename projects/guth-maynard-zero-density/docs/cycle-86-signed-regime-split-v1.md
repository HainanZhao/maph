# Cycle 86: zero-mode removal splits the signed range

## Claim boundary

`PROVED`: the smooth signed `q`-projector has exactly zero circle mean, so
the continuous unsigned volume mode identified in Cycle 85 is absent from
the signed architecture.  Exact exponent bookkeeping splits the remaining
range into:

```text
moment regime:      16/25<=xi<58/75,
large-value regime: 58/75<=xi<=83/75.              (1)
```

A diagonal-strength signed second moment would close the first regime.
Pointwise square-root cancellation cannot close the second.

No second-moment estimate, large-value theorem, new Fourier-band closure,
packet closure, density gain, or interval gain is proved.

## Exact zero mode

With the frozen Cycle-81 convention,

```text
Theta_Q(x)=sum_(q in Z)V(q/Q)e(qx).
```

Integration over the circle selects `q=0`:

```text
int_(R/Z)Theta_Q(x)dx=V(0).                        (2)
```

The fixed smooth dyadic weight `V` is compactly supported inside
`(0,infinity)`, hence `V(0)=0`.  Equation (2) is exact.  In the Poisson
representation this is the cancellation of the continuous volume mode; all
remaining terms are nonzero logarithmic resonances.

## Moment regime

One `S_k` has

```text
N=DQ=X^(14/15+o(1))
```

atoms.  Square-root size has exponent `7/15`, a saving `2/15` over the
unsigned per-frequency exponent `D=X^(3/5)`.

Freeze the diagonal-strength moment target

```text
sum_(k~K)|S_k|^2<=X^(xi+14/15+o(1)).               (3)
```

Cauchy applied to (3) gives block `L1` exponent

```text
xi/2+(xi+14/15)/2=xi+7/15.                        (4)
```

It is strictly below `31/25` exactly for

```text
xi<31/25-7/15=58/75.                               (5)
```

Equality ties and is not promoted.  Thus (3), if proved uniformly, closes
the entire first interval in (1).

## Large-value regime

The saving required over unsigned volume is

```text
(xi+3/5)-31/25=xi-16/25.                           (6)
```

At `xi=58/75`, this equals the full `2/15` square-root saving.  For larger
`xi`, pointwise square-root size no longer suffices.  The correct object is a
large-value distribution

```text
M_xi(s)=#{k~X^xi: |S_k|>=X^s},                     (7)
```

with a bound strong enough that every dyadic contribution satisfies

```text
s+log_X M_xi(s)<31/25.                             (8)
```

At the Fourier ceiling `xi=83/75`, the allowed average per-frequency
exponent is only

```text
31/25-83/75=2/15.                                  (9)
```

Therefore the upper third of the frequency range requires most `S_k` to be
far smaller than square-root size, with exceptional large values routed to
E16.

## Gate effect

E14D splits into
`SIGNED_DIAGONAL_MOMENT_OPEN` below `58/75` and
`SIGNED_LARGE_VALUE_SPARSITY_OPEN` above it.

