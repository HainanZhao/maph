# Cycle 85: logarithmic crossing occupancy reaches the volume limit

## Claim boundary

`PROVED`: applying the checked order-three Huxley--Sargos theorem to the
inverse-log crossing curve removes the entire Cycle-84 crossing-
discretization loss.  The Fourier-`L1` exponent becomes

```text
xi+3/5.                                             (1)
```

Thus every block `xi<16/25` is strictly closed, adding
`43/75<=xi<16/25`, of width `1/15`.  Equality at `16/25` ties and is not
promoted.

No estimate for `16/25<=xi<=83/75`, signed cancellation, packet closure,
density gain, or interval gain is proved.

## From real crossings to a logarithmic curve

For Fejer frequency `j=X^(nu+o(1))`, an occupied crossing satisfies

```text
|j c0 exp(2pi d/D)-r|<<1/K,   r~j.                 (2)
```

The inverse map has derivative comparable to `D/j`, so (2) implies, with
uniform constants,

```text
||(D/(2pi))log(r/(j c0))||<<D/(jK).                (3)
```

Write

```text
g_j(r)=(D/(2pi))log(r/(j c0)),
delta=D/(jK).
```

On each fixed dyadic `r/j` interval, every derivative has fixed sign and

```text
|g_j^(s)(r)|asymp D/j^s.                           (4)
```

These are exactly the hypotheses and normalization checked for the
order-three Huxley--Sargos theorem in Cycle 47.

## Exact exponent specialization

For `D=X^(3/5)`, `K=X^xi`, and `j=X^nu`, the theorem's four terms are

```text
derivative: 1/10+nu/2,
tube:       1/5+2nu/3-xi/3,
ratio:      (2nu-xi)/3,
constant:   0.                                     (5)
```

Throughout

```text
43/75<=xi<=16/25,  0<=nu<=1/3,
```

the derivative term dominates.  Its smallest margin over the tube term
occurs at `(xi,nu)=(43/75,1/3)` and equals `8/225`.  Taking the minimum with
the trivial `j` crossings gives

```text
C_j<<X^(min(nu,1/10+nu/2)+o(1)).                   (6)
```

This is trivial for `nu<=1/5` and curvature-controlled for `nu>=1/5`.

## Summation and annuli

In a dyadic `j` block, the final Fourier-`L1` exponent contributed by the
crossings is

```text
xi+nu+min(nu,1/10+nu/2).                           (7)
```

For `nu<=1/5`, the last two terms total at most `2/5`.  For `nu>=1/5`, they
equal `1/10+3nu/2`, increasing to `3/5` at `nu=1/3`.  This proves (1).

At projector radius `L/Q`, the Fejer ceiling becomes `j<=Q/L`; the outer
coefficient supplies `L^(1-A)`.  With the frozen `A=5`, every positive power
from (7) is absorbed, so the central `L=1` exponent remains maximal.

## Structural boundary

At `xi=16/25`, (1) equals `31/25`.  This is also the Cycle-84 formal volume
term.  Therefore the complete unsigned smooth-incidence engine—not merely a
specific derivative bound—has reached its natural volume boundary.  Any
advance in `16/25<=xi<=83/75` must retain signs or output structured
exceptions that E16 can exploit; a sharper unsigned count alone cannot meet
the registered raw target.

## Gate effect

E14 advances to
`UNSIGNED_INCIDENCE_VOLUME_LIMIT_SIGNED_RESONANCE_OPEN`.

