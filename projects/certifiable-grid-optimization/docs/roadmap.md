# Research roadmap

## Objective

Build rigorous, useful certificates for nonconvex AC grid optimization.  The
desired output is not merely a low-cost numerical point, but a feasible point
with a verified optimality gap or a precise diagnosis of why certification
failed.

## Phase 0 — scope and claim discipline

- [x] Isolate the project from unrelated research.
- [x] Separate voltage recoverability from global optimality.
- [x] Define proof, computation, conjecture, and counterexample ledgers.
- [ ] Freeze a standard AC-OPF sign and orientation convention.

Exit criterion: every use of “exact” specifies whether it means rank-one
voltage recovery, equality of relaxation and nonconvex optima, or numerical
solver tolerance.

## Phase 1 — one-cycle geometry

- [x] Prove the exact rank-one completion criterion on a connected graph.
- [x] Specialize it to a unicyclic graph: edge saturation plus one holonomy.
- [x] Show that phase holonomy alone is insufficient.
- [x] Derive the exact edge residual of spanning-tree voltage recovery.
- [x] Express the residual identity exactly using radial and phase defects.
- [ ] Derive simplified norm bounds uniform over voltage boxes.
- [ ] Determine the sharp constants for a single cycle.
- [x] Show that spanning-tree recovery is suboptimal on an inconsistent
  triangle.
- [x] Prove the equal-weight certificate-optimal projection on a triangle.
- [x] Compute weighted triangle optima and falsify universal balancing.
- [ ] Derive the continuous weighted optimum on one cycle.
- [ ] Optimize or upper-bound the conditioning-aware objective
  \(\beta^2L\rho\).
- [x] Derive an LP surrogate and approximation ratio for the exact phase
  injection certificate on a fixed winding branch.
- [x] Implement the LP on general sparse graphs using a pinned solver.

Exit criterion: a self-contained theorem quantifies voltage recovery error
using both radial edge slack and cycle holonomy.

## Phase 2 — AC power-flow residuals

- [x] Fix the MATPOWER bus-admittance and bus-injection conventions.
- [x] Propagate voltage-recovery error to active/reactive balance residuals.
- [ ] Include thermal, voltage, and phase-difference constraints.
- [ ] Identify which constants depend on network size and which depend only
  on local admittances and cycle length.
- [x] Prove that arbitrarily small residual does not imply feasibility at a
  singular voltage-collapse point.
- [x] Implement a conditional Newton--Kantorovich repair certificate on the
  lossless triangle.
- [x] Implement full polar \(P/Q\) equations and verify their Jacobian by
  finite differences on IEEE-14.
- [x] Implement Newton REF/PV/PQ repair on pinned PGLib cases.

Exit criterion: edge moment defects give a rigorous, computable upper bound
on physical constraint violation.

## Phase 3 — objective and optimality certificates

- [ ] Pair a relaxation lower bound with a recovered feasible upper bound.
- [ ] Prove an a posteriori optimality-gap certificate.
- [ ] Test whether the certificate is informative on difficult unicyclic
  instances.
- [ ] Distinguish a theorem about a returned instance from a universal
  exactness theorem.

Exit criterion: for every tested instance the software either verifies a gap
or explicitly reports that no certificate was obtained.

## Phase 4 — topology extensions

- [ ] Extend from one cycle to cactus graphs.
- [ ] Study bounded cycle rank and cycle bases.
- [ ] Design adaptive selection of SDP or moment constraints.
- [x] Compare tree and weighted least-squares projections on a synthetic
  sparse graph.
- [ ] Compare angular-synchronization and state-estimation recovery on
  standard network data.
- [ ] Compare all recovery rules under the same relaxation outputs and
  measurement model.
- [ ] Replace exhaustive oracle-tree enumeration by scalable tree heuristics.
- [x] Prototype an angle-trust-region LP sweep for the composed
  \(\beta^2L\rho\) score.
- [ ] Extend the conditioning-aware surrogate to full complex-voltage AC
  recovery.
- [ ] Test whether local defects compose additively, quadratically, or not at
  all.

## Phase 5 — benchmark and operational study

- [x] Pin PGLib-OPF v23.07 and vendor checksummed 5- and 14-bus cases.
- [x] Add a deterministic synthetic certification-rate benchmark.
- [x] Run a full-AC experiment on PGLib topologies with synthetic edge-local
  relaxation defects.
- [x] Obtain and independently audit actual SOCP relaxation moment outputs.
- [x] Compare recovery rules on typical and congested 5- and 14-bus cases.
- [x] Test recovery-informed targeted thermal tightening.
- [ ] Implement a conventional local AC-OPF upper-bound solver if this
  project is resumed.
- [ ] Reproduce published baseline objectives.
- [ ] Benchmark typical, congested, and small-angle cases separately.
- [ ] Measure solve time, feasible cost, certified gap, and failure rate.
- [ ] Compare against full SDP, SOCP, nonlinear local solves, and available
  global bounds.

## Kill criteria

Reassess the direction if any of the following persists after the first
research cycle:

1. the unicyclic certificate reduces completely to an existing published
   bound;
2. constants necessarily grow so quickly that the bound is vacuous on
   three- to ten-bus cycles;
3. obtaining a feasible upper bound dominates all certification cost;
4. public benchmarks cannot distinguish the method from existing solvers.

## Current decision

The first three benchmark-relevant kill signals are now active:

- certificate minimization did not improve actual Newton repair;
- all recovery rules converged to the same dispatch on genuine SOCP moments;
- cases with material SOCP gaps remained thermally infeasible after recovery;
- naive targeted tightening was ineffective or made the SOCP infeasible.

Pause algorithm development unless a new directional certificate or a
relaxation-strengthening theorem addresses these failures directly.
