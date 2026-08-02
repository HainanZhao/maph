# Cycle 58 preregistration: strict hybrid-margin correction

## Question

Audit only the strict inequality in the Cycle-54 hybrid trigger and propagate
its exact consequence to the Cycle-55--57 analytic targets.

## Frozen ledger

- The penultimate trigger exceeds the selected level by exactly `3/50`.
- A hybrid analytic saving `gamma` replaces the trigger by
  `trigger-gamma`.
- Off-diagonal production requires the adjusted trigger to be strictly below
  the selected level.
- Without the Cycle-48 `7/50`, the penultimate gap is `1/5`.

## Outcomes

- `STRICT_SURPLUS_REQUIRED`: closure requires `gamma>3/50`; equality needs a
  separately proved logarithmic or constant margin. The standalone powered
  saving must similarly exceed `1/5`.
- `EQUALITY_SUFFICES`: exact exponent equality alone forces the strict
  off-diagonal.

This correction changes target wording only. It does not alter the proved
Cycle-54 gaps or the Cycle-55--57 algebraic identities.
