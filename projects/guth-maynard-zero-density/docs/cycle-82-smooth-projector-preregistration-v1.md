# Cycle 82 preregistration: smooth q-projector band

## Claim boundary

This cycle tests whether the Cycle-81 smooth projector and Cycle-80 maximum
occupancy imply `|S_k|<<X^(37/45+o(1))`, closing a larger initial Fourier
band.  It will not claim the endpoint, the remaining high-frequency range,
packet closure, density gain, or interval gain.

## Frozen inputs and conventions

- Use the Cycle-81 convention
  `hat V(y)=int V(t)e(-yt)dt` and fixed `C_c^infinity` weight `V`.
- Use the Cycle-80 bound `A_k<=X^(22/45+o(1))` uniformly in `k` and interval
  center.
- Partition the circle into half-open intervals of length at most `1/Q`;
  endpoint overlap may cost a fixed factor only.
- Absorb logarithms and constants into `X^o(1)`, but no power of `X`.

## Frozen gates

The cycle passes only if:

1. smooth Poisson gives
   `|Theta_Q(x)|<<_A Q(1+Q||x||)^(-A)`;
2. occupancy summation gives `|S_k|<<Q A_k` with no power loss;
3. the per-`k` exponent is exactly `37/45`;
4. the strict block cutoff is exactly `94/225`;
5. the new width beyond `163/450` is exactly `1/18`;
6. equality at `94/225` is recorded as a tie, not promoted.

## Verification plan

- Encode the exact rational ledger in
  `conventions/smooth_phase_projector_v1.py`.
- Independently test projector decay accounting, exponent addition, cutoff,
  width, and endpoint behavior.
- Seal against Cycles 80 and 81 with a deterministic replay artifact.
- Hostile audit remains deferred to paper-stage promotion.

