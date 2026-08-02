# Cycle 86 discovery candidate: signed-regime split

## Status

`CONJECTURED`: discovery note selecting the next signed architecture.  Exact
identities and exponent thresholds require a separate proof artifact.

## Candidate observations

For the smooth `q`-projector

```text
Theta_Q(x)=sum_q V(q/Q)e(qx),
```

the circle mean is its zero Fourier coefficient `V(0)`.  The frozen weight
is supported inside `(0,infinity)`, so `V(0)=0`.  Thus the continuous volume
mode that forced the Cycle-85 unsigned boundary is absent exactly in the
signed sum.

Let `N=DQ=X^(14/15+o(1))` be the number of `(d,q)` atoms in one `S_k`.
Square-root size is `N^(1/2)=X^(7/15+o(1))`, so a dyadic `k` block would have
Fourier-`L1` exponent

```text
xi+7/15.                                           (1)
```

This meets `31/25` at `xi=58/75`.  Therefore:

- on `16/25<=xi<58/75`, a diagonal-strength signed second moment suffices;
- on `58/75<=xi<=83/75`, even pointwise square-root size is insufficient,
  so the theorem must prove a sparse large-value distribution in `k`.

At the Fourier ceiling, the permitted average per-frequency exponent is only
`31/25-83/75=2/15`.

## Falsifiers

1. The frozen smooth projector has a nonzero circle mean.
2. The atom count or square-root exponent differs from `14/15`, `7/15`.
3. The regime boundary is not exactly `58/75`.
4. A second-moment statement weaker than diagonal strength is mistakenly
   treated as sufficient below `58/75`.
5. Pointwise square-root cancellation is claimed sufficient above `58/75`.

