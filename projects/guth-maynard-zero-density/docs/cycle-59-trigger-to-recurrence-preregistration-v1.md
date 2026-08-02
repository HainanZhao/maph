# Cycle 59 preregistration: trigger margin versus recurrence strength

## Question

If a Cycle-58 hybrid crosses the penultimate diagonal by surplus `mu>0`,
determine exactly what popular-correlation deficit follows from the generic
phase-aligned Halasz--Montgomery ledger. Compare this with the Cycle-52/48
target deficit `7/50`.

## Frozen variables

- `R=X^r` rows.
- Coefficient energy and support exponents are `a,n`.
- The selected level satisfies `r+2v=a+n+mu` after the adjusted diagonal.
- The phase-aligned inequality forces off-diagonal mass at exponent
  `r+n+mu`.
- A correlation is `eta`-large if its size is at least `X^(n-eta)`.
- Use only the trivial bound of `R^2` ordered off-diagonal pairs.
- Evaluate at `r=21/25` and desired `eta=7/50`.

## Outcomes

- `BARE_TRIGGER_SUFFICES`: every `mu>0` forces deficit at most `7/50` at the
  target row exponent.
- `GRAPH_AMPLIFICATION_NEEDED`: generic counting gives popular edges only
  for `eta>r-mu`; obtaining `eta=7/50` at `r=21/25` requires `mu>7/10`.

This cycle distinguishes a direct E12 restriction theorem from a
trigger-only theorem. It proves no such analytic estimate and no density or
interval gain.
