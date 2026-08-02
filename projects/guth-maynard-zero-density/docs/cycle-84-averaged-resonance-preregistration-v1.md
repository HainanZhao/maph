# Cycle 84 preregistration: averaged resonance incidence

## Claim boundary

This cycle tests only the dyadic Fourier-`L1` consequence of averaging the
smooth resonance projector jointly over `(k,d)`.  It will not claim the
endpoint `43/75`, higher frequencies, packet closure, density gain, or
interval gain.

## Frozen ranges and conventions

- `D=X^(3/5+o(1))`, `Q=X^(1/3+o(1))`, `K=X^(xi+o(1))`.
- Active input range `37/75<=xi<43/75`.
- All `k,d,q` weights are fixed smooth compact dyadic weights.
- The outer `q`-projector uses the Cycle-81 Fourier convention.
- A dyadic annulus `L/Q` uses Fejer bandwidth `H~Q/L` and frozen Schwartz
  decay `L^-A` with `A=5`.
- The rational anchor `c0=n0/q0`, `q0~Q`, remains fixed; its exact multiples
  are included in the crossing term and are not discarded.

## Frozen gates

The cycle passes only if:

1. joint Fejer majorization yields
   `I_L<<KD L/Q+(L/Q)sum_(j<=Q/L)|B_j|`;
2. smooth summation in `k` and monotonicity in `d` give `|B_j|<<D+jK`,
   including annular tails at scale `1/K`;
3. consequently `I_L<<KD L/Q+D+KQ/L`;
4. after the outer factor `Q` and `L^-5` summation, the exact exponents are
   `xi+3/5`, `14/15`, and `xi+2/3`;
5. the third term dominates on the active range;
6. the strict cutoff is `43/75`, the added width is `2/25`, and equality is
   recorded as a tie;
7. the formal volume term alone would permit `xi<16/25`, identifying the
   crossing-discretization gap `1/15` at the new endpoint.

## Verification plan

- Pin the full central and annular ledger in
  `conventions/averaged_resonance_v1.py`.
- Independently test crossing counts, all three exponents, dominance,
  strictness, width, and the volume-versus-crossing gap.
- Seal against Cycles 81--83 with deterministic hashes.
- Preserve the `KQ` term as the next inverse/major-arc object; hostile audit
  remains deferred to paper stage.

