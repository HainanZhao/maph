# Cycle 86 preregistration: signed projector regime split

## Claim boundary

This cycle will prove only the zero-mode identity and exact moment/large-
value exponent contracts for the remaining signed range.  It will not prove
the required second moment, a large-value estimate, any new Fourier-band
closure, packet closure, density gain, or interval gain.

## Frozen conventions and ranges

- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`, atom exponent `14/15`.
- `V in C_c^infinity((0,infinity))`; hence `V(0)=0`.
- `Theta_Q(x)=sum_q V(q/Q)e(qx)` with the Cycle-81 Fourier sign.
- Remaining range `16/25<=xi<=83/75` and raw block target `31/25`.
- “Diagonal-strength second moment” means
  `sum_(k~K)|S_k|^2<=X^(xi+14/15+o(1))`.

## Frozen gates

The cycle passes only if:

1. `int_(R/Z)Theta_Q(x)dx=V(0)=0` exactly;
2. the unsigned per-frequency exponent is `3/5`, while square-root atom size
   is `7/15`, a signed saving `2/15`;
3. Cauchy plus the diagonal-strength second moment gives block exponent
   `xi+7/15`;
4. its strict cutoff is `58/75`, and equality ties;
5. the required saving over unsigned volume is `xi-16/25`;
6. the high-range average allowance is `31/25-xi`, equal to `2/15` at
   `xi=83/75`;
7. the plan separates a moment regime `[16/25,58/75)` from a large-value
   sparsity regime `[58/75,83/75]`.

## Verification plan

- Pin the exact ledger in `conventions/signed_regime_split_v1.py`.
- Test the zero mode, all threshold identities, endpoint ties, and required
  savings independently.
- Seal against Cycles 81 and 85.
- Hostile audit remains deferred to paper stage.

