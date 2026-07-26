# Progress and claim ledger

## 2026-07-27 — Cycle 0: problem selection

### Scope decision

Selected gas-aware routing across parallel constant-product AMMs as the next
research problem.  The focus is fixed-input, two-token routing with fixed
per-pool execution costs.

The project explicitly excludes, for now:

- arbitrary multi-token CFMM networks;
- stochastic transaction ordering and sandwich attacks;
- liquidity-provider strategy;
- claims about realized trading profit without a historical execution model.

### Prior-art boundary

The initial audit found:

1. Angeris, Evans, Chitra, and Boyd formulate general CFMM routing as convex
   optimization without fixed costs and as a mixed-integer convex problem
   with fixed costs.  They propose relaxation and randomized/threshold
   heuristics.
2. Escudero, Lara, and Sama analyze gas-aware heterogeneous CFMM routing,
   KKT systems, activation thresholds, no-trade regions, and relaxation
   bounds.
3. The remaining plausible niche is not the mixed-integer formulation
   itself.  It is the exact computational structure and certifiable
   algorithms of parallel constant-product pools.
4. General fixed-charge resource allocation is an established operations
   research topic, so any complexity or approximation result must be audited
   there as well as in the AMM literature.

Primary starting points:

- <https://stanford.edu/~boyd/papers/cfmm_routing.html>
- <https://arxiv.org/abs/2603.02844>

### Mathematical progress

- Derived the closed-form water-filling allocation for a fixed pool set.
- Derived exact aggregation for equal-price, zero-proportional-fee pools.
- Constructed a candidate SUBSET-SUM reduction showing weak NP-hardness in
  that restricted class.
- Identified a separable Lagrangian upper bound for route certification.
- Implemented a dependency-free exhaustive active-set oracle with a
  closed-form water-filling subproblem.

### Claim status

| Item | Status |
| --- | --- |
| Fixed-set water filling | derived; standard |
| Equal-price aggregation | derived; proof straightforward |
| Weak-NP-hardness reduction | candidate; proof/prior-art audit required |
| Pseudo-polynomial dynamic program | hypothesis |
| Equal-price FPTAS | hypothesis |
| Useful heterogeneous dual certificate | hypothesis |

### Immediate challenge to the project

The broad gas-aware problem was addressed in March 2026.  This project
continues only if the constant-product special structure yields a result
that is both sharper than generic MICP machinery and operationally relevant.

## 2026-07-27 — Cycle 1: tractable subclass and certificates

### New closest prior art

Xi and Moallemi's July 22, 2026 preprint studies the same parallel,
same-token-pair, fixed-activation-cost routing problem and evaluates it on
2.98 million WETH-USDC swaps.  Its gas-aware exact method enumerates all
pool subsets and solves each fixed-support concave problem by marginal-price
bisection:

- <https://arxiv.org/abs/2607.20762>

This independently covers the project's exhaustive active-set oracle and
most of the intended empirical motivation.  The remaining technical niche
is narrower:

1. exact pseudo-polynomial routing for commensurate equal-price
   constant-product pools;
2. additive reserve-discretization guarantees in that subclass;
3. analytic Lagrangian bounds and a certifying branch-and-bound method that
   avoids full subset enumeration on heterogeneous pools.

No novelty is claimed yet for any of these items.

### Mathematical and computational progress

- Proved the equal-price integer-reserve dynamic program in
  \(O(m\sum_i a_i)\) time and implemented route reconstruction.
- Proved an additive \(pm\delta\) loss bound for reserve flooring.
- Derived every constant-product dual activation threshold and minimized
  the piecewise analytic Lagrangian bound by enumerating thresholds and
  interval stationary points.
- Verified the bound against exhaustive enumeration on 210 deterministic
  random instances with up to seven pools.
- Added compact counterexamples to gross-output water filling, standalone
  profitability thresholds, dual-threshold tie breaking, and initial
  marginal-price ranking.
- Added deterministic benchmarks for the equal-price dynamic program and
  for certificate/heuristic gaps.

### Claim status

| Item | Status |
| --- | --- |
| Equal-price integer-reserve DP | proved and oracle-tested |
| Additive reserve rounding | proved; conservative |
| Analytic Lagrangian bound | derived and oracle-tested |
| Threshold/marginal baselines | falsified by exact counterexamples |
| Equal-price weak NP-hardness | reduction validated; novelty audit pending |
| Certifying branch-and-bound | prototype implemented and oracle-tested |

### Decision

The first branch-and-bound prototype often closes the seeded heterogeneous
instances at the root and matches exhaustive enumeration in randomized
tests.  Structured SUBSET-SUM reductions require materially more nodes,
including 1,243 explored nodes in one 16-pool seed.  Continue to a broader
adversarial benchmark and dominance rules, but treat the July 2026 paper as
a substantial narrowing event.  The project should stop if this advantage
does not persist beyond the initial generator, or if the equal-price
algorithm is already a standard fixed-charge resource-allocation corollary
with no useful AMM-specific strengthening.
