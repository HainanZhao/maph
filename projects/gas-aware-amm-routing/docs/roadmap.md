# Research roadmap

## Objective

Develop a fast gas-aware router for parallel constant-product pools that
returns both a feasible route and a rigorous bound on lost net output.

## Phase 0 — theorem and novelty audit

- [x] Specify the parallel fixed-input problem.
- [x] Derive fixed-active-set water filling.
- [x] Derive equal-price aggregation.
- [x] Formalize and adversarially check the SUBSET-SUM reduction.
- [ ] Search fixed-charge resource-allocation literature for the same
  reduction or a stronger known result.
- [x] Identify the exact contribution beyond the March and July 2026
  gas-aware routing papers.

Exit criterion: a precise complexity boundary or structural theorem that is
not already present in the closest literature.

## Phase 1 — exact oracle and counterexamples

- [x] Implement exhaustive active-set enumeration for small instances.
- [x] Implement fixed-set water filling in closed form.
- [x] Test the equal-price reduction on small SUBSET-SUM instances.
- [x] Construct counterexamples to threshold rounding and naive
  marginal-price sorting.
- [x] Add a reproducible benchmark for heuristic and Lagrangian gaps.

Exit criterion: every future heuristic can be falsified against a trusted
small-instance oracle.

## Phase 2 — tractable special cases

- [x] Prove a pseudo-polynomial algorithm for commensurate equal-price pools.
- [ ] Determine whether an FPTAS is possible and choose additive or
  multiplicative error appropriately.
- [ ] Seek dominance rules for pools with ordered reserves, fees, or spot
  prices.
- [ ] Identify conditions under which the Lagrangian certificate is exact.

Exit criterion: one theorem yields a provable improvement over generic
subset enumeration.

## Phase 3 — certifying general parallel router

- [x] Combine water filling, Lagrangian bounds, and branching.
- [x] Report incumbent net output, upper bound, and additive gap.
- [ ] Compare against continuous relaxation, threshold rounding, randomized
  rounding, and a generic mixed-integer solver.
- [ ] Stress-test numerical stability at tiny trades and nearly equal prices.

Exit criterion: materially faster certified solutions on a transparent
synthetic benchmark.

## Phase 4 — economic validation

- [ ] Pin one chain, block range, and pool family.
- [ ] Reconstruct pool states and gas costs without look-ahead.
- [ ] Compare quoted and realized net output.
- [ ] Separate mathematical routing gains from latency, MEV, failed
  transactions, and state staleness.

Exit criterion: savings exceed solver and execution overhead on a meaningful
fraction of historical routes.

## Early kill criteria

Pause the project if any of these persists after the first two cycles:

1. the candidate complexity result and tractable subclasses are already
   standard consequences with no AMM-specific strengthening;
2. the dual bound is too loose to certify routes with more than a few pools;
3. generic MIP solves realistic parallel instances faster than the proposed
   structure can exploit;
4. fixed gas is economically negligible on the chosen execution venue;
5. public data cannot support an honest realized-cost comparison.
