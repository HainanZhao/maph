# Cycle 83 discovery candidate: Fejer--van der Corput resonance count

## Status

`CONJECTURED`: discovery-only candidate.

## Candidate

Use a Fejer majorant at bandwidth `Q` for

```text
R_k=#{d~D: ||kc0 exp(2pi d/D)||<=1/Q}.
```

It should give

```text
R_k << D/Q + Q^(-1) sum_(1<=j<=Q)
                 |sum_(d~D)e(jkc0 exp(2pi d/D))|.  (1)
```

The phase has second derivative `asymp jk/D^2`.  The classical second
derivative estimate predicts

```text
E_j << sqrt(jk)+D/sqrt(jk).                         (2)
```

Averaging (2) in (1) yields

```text
R_k << D/Q + sqrt(kQ)+D/sqrt(kQ).                  (3)
```

For `xi>=94/225`, the middle term dominates, so the resonance exponent is
`xi/2+1/6`.  The Cycle-82 projector then gives block exponent
`3xi/2+1/2`, closing strictly for `xi<37/75`.  The proposed new width is
`37/75-94/225=17/225`.

For the projector tails, repeat the same majorant at dyadic radius `L/Q`
with bandwidth `Q/L`.  This gives the analogous cumulative count with `Q`
replaced by `Q/L`.  Multiplication by the Schwartz weight `L^(-A)` and
summation over dyadic `L` should cost only a constant when `A` is fixed large.

## Falsifiers

1. The Fejer polynomial fails to majorize the entire `1/Q` interval with a
   fixed constant.
2. The second derivative is not uniformly comparable on the frozen dyadic
   `d` support.
3. Its published theorem requires a derivative range violated for some
   `j<=Q` or `xi<37/75`.
4. Averaging the reciprocal derivative term costs a hidden power.
5. The dyadic annular extension loses a power of `L` not absorbed by the
   fixed Schwartz decay.
