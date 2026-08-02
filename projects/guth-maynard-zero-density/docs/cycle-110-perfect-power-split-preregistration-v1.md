# Cycle 110 preregistration: weighted aggregation across perfect-power splits

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle asks whether the Cycle-109 fixed-core bound loses a power when it
is summed over the primitive splits and cross valuations belonging to one
perfect-power critical label. It does not claim a complete moment, density,
or interval theorem.

## Frozen input and variables

- Use the Cycle-102 core with `u+v=d`, `(u,v)=1`,
  `x=(u,r0^d)`, `y=(v,n0^d)`.
- Use the Cycle-106 exact formulas

  ```text
  K=d*n0^u*r0^v/(x*y),
  B0=v*r0^d/(x*y),
  C0=u*n0^d/(x*y).
  ```

- Factor the fixed compact-chart and anchor contribution out of the
  Cycle-109 kernel. The arithmetic split weight is

  ```text
  J(u,v)=1/sqrt(K*B0*C0).
  ```

  Actual-scale lcm factors may only decrease this weight and will be retained
  in exact test enumeration.

## Gate and outcomes

Prove a constant independent of `d,n0,r0` for

```text
sum_{u+v=d,(u,v)=1} J(u,v).
```

The proof must separate the unit base `(1,1)`, the two one-sided unit bases,
and the genuinely nonunit base. A finite search through `d<=80` and
`n0,r0<=12` is a falsifier, not proof.

- `SPLIT_SUM_UNIFORMLY_BOUNDED`: prove the stated uniform bound and combine
  it with `d|w` and Cycle-99 label injectivity to obtain at most a divisor
  factor per mode.
- `POLYNOMIAL_SPLIT_LOSS`: prove the sharp polynomial loss and propagate it
  to the exponent ledger.
- `FROZEN_SATURATOR`: preserve an explicit family contradicting the proposed
  bound, together with its exact weights.

## Stop rule

Do not infer a complete E14D-low closure. The output still carries the common
compact-chart/anchor prefactor and does not address nonsmooth arithmetic
payloads, irrational large-degree cores, or weak/simple-root branches.
