# Cycle 77 preregistration: critical anchored saddle

## Question

At the unique Cycle-75 worst point, derive a genuinely joint observable that
retains one packet anchor. Compare it exactly with the anchor-free ratio
census and with checked rational-point theorems.

## Frozen scales

```text
theta=alpha=1/3,
kappa=8/75,
Delta exponent=3/5,
Q exponent=1/3,
packet error |q alpha_ell-a| exponent=-1-kappa=-83/75,
packet target exponent=6/25-kappa=2/15.
```

Use `n=q+a`, so a packet is equivalently
`|n-q exp(2pi ell/Delta)|<=X^(-83/75+o(1))`.

## Exact checks

1. Choose one actual packet as an anchor and derive the translated incidence
   in `(d,q,n)` with every error prefactor charged.
2. Normalize the resulting graph and derive its Hessian determinant,
   anisotropic mesh, tube width, volume benchmark, and exact count target.
3. Derive the anchor-free ratio-product necessary census, its divisor
   multiplicity, pair target, and random-volume exponent; quantify the loss
   caused by discarding the anchor.
4. Check a reachable primary rational-point theorem at theorem and hypothesis
   level. Record whether its denominator geometry matches. If not, calculate
   the loss from a common-denominator embedding without treating that mismatch
   as a universal obstruction.

## Outcomes

- `CRITICAL_SADDLE_REDUCTION`: the anchored target is exact but no checked
  theorem closes it; seal the new anisotropic theorem contract.
- `CRITICAL_CELL_CLOSED`: a checked theorem applies with strict exponent
  margin and closes the packet target.
- `REDUCTION_CORRECTION`: an identity, scale, multiplicity, or source
  hypothesis fails; record the corrected form.

No powered saving, density gain, or interval gain is asserted unless the
critical cell and every required atlas cell close with strict margin.
