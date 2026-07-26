# Initial literature audit

This is a preliminary map, not yet a systematic review.

## Baseline facts

1. AC-OPF is a nonconvex optimization problem and is NP-hard in general.
2. Semidefinite and second-order-cone relaxations can be exact on important
   restricted instances, but not universally.
3. Chordal and cycle decompositions reduce the computational cost of
   semidefinite constraints.
4. A rank-one moment matrix permits recovery of a physical complex voltage
   vector.  Positive semidefiniteness without rank one does not.

## Closest starting points

- A. S. Zamzam, N. D. Sidiropoulos, and E. Dall'Anese,
  “Beyond Relaxation and Newton-Raphson: Solving AC OPF for Multi-phase
  Systems with Renewables,” 2016.
  <https://arxiv.org/abs/1612.07255>
- L. Fan, H. Ghassempour Aghamolki, Z. Miao, and B. Zeng,
  “Achieving SDP Tightness Through SOCP Relaxation with Cycle-Based SDP
  Feasibility Constraints for AC OPF,” 2018.
  <https://arxiv.org/abs/1804.05128>
- M. S. Andersen, A. Hansson, and L. Vandenberghe,
  “Reduced-Complexity Semidefinite Relaxations of Optimal Power Flow
  Problems,” 2013.
  <https://arxiv.org/abs/1308.6718>
- S. Babaeinejadsarookolaee et al.,
  “The Power Grid Library for Benchmarking AC Optimal Power Flow
  Algorithms,” 2019.
  <https://arxiv.org/abs/1908.02788>
- IEEE PES Power Grid Library, AC-OPF benchmarks.
  <https://github.com/power-grid-lib/pglib-opf>

## Prior art that narrows our claim

- M. Farivar and S. H. Low, “Branch Flow Model: Relaxations and
  Convexification,” 2012.  This work already gives the exact cycle-angle
  recovery condition and a spanning-tree recovery algorithm for mesh
  networks.  We must not present cycle holonomy itself as new.
  <https://arxiv.org/abs/1204.4865>
- K. Dvijotham, H. Nguyen, and K. Turitsyn, “Solvability Regions of Affinely
  Parameterized Quadratic Equations,” 2017.  This already constructs local
  solvability regions around a nonsingular nominal solution, including power
  systems.  A generic inverse-function or Newton certificate is not new.
  <https://arxiv.org/abs/1703.08881>
- D. Lee, H. D. Nguyen, K. Dvijotham, and K. Turitsyn, “Convex Restriction
  of Power Flow Feasibility Sets,” 2018.  This constructs convex inner
  restrictions around a feasible base point using fixed-point arguments,
  includes operational constraints, and has a formulation whose constraint
  count grows linearly with buses and lines.  A trust region around a
  nonsingular power-flow point is therefore a tool, not a standalone
  contribution.
  <https://arxiv.org/abs/1803.00818>
- C. Wang, A. Bernstein, J.-Y. Le Boudec, and M. Paolone, “Explicit
  Conditions on Existence and Uniqueness of Load-Flow Solutions in
  Distribution Networks,” 2016.  This gives efficiently checkable
  existence/uniqueness conditions on radial and meshed distribution models.
  <https://arxiv.org/abs/1602.08372>
- B. Kocuk, S. S. Dey, and X. A. Sun, “Inexactness of SDP Relaxation and
  Valid Inequalities for Optimal Power Flow,” 2014.  Even two-bus radial
  examples can have an inexact relaxation or a feasible relaxation for an
  infeasible OPF instance.
  <https://arxiv.org/abs/1410.1004>
- F. Zohrizadeh et al., “Penalized Parabolic Relaxation for Optimal Power
  Flow Problem,” 2018.  Penalized sequential relaxations already recover
  feasible near-global solutions under assumptions and at large benchmark
  scale.
  <https://arxiv.org/abs/1809.09809>
- B. Taheri and D. K. Molzahn, “Restoring AC Power Flow Feasibility from
  Relaxed and Approximated Optimal Power Flow Models,” 2022.  This uses a
  state-estimation viewpoint to combine inconsistent phasors, injections,
  and flows, and is the closest comparator for any optimized projection
  proposed here.
  <https://arxiv.org/abs/2209.04399>
- A. Singer, “Angular Synchronization by Eigenvectors and Semidefinite
  Programming,” 2009.  Globally distributing inconsistent relative phases
  is a mature problem; angular synchronization itself cannot be claimed as
  new.
  <https://arxiv.org/abs/0905.3174>
- L. Wang and A. Singer, “Exact and Stable Recovery of Rotations for Robust
  Synchronization,” 2012.  Robust synchronization using a sum of unsquared
  deviations is also established; replacing least squares by an absolute
  phase loss is not by itself a novelty.
  <https://arxiv.org/abs/1211.2441>
- A. Venzke, S. Chatzivasileiadis, and D. K. Molzahn, “Inexact Convex
  Relaxations for AC Optimal Power Flow: Towards AC Feasibility,” 2019.
  Their 96-case study shows that small optimality gaps need not imply small
  distances to AC feasibility, and that penalized recovery can fail.  Any
  benchmark must report both certification and recovery failures.
  <https://arxiv.org/abs/1902.04815>

The surviving research niche is therefore not a qualitative recovery
condition.  It is a quantitative and operationally competitive bridge from
the *specific defects returned by a cheap relaxation* to one of:

1. a sharper feasibility region than existing generic certificates;
2. an a priori guarantee for a fast repair step;
3. an adaptive choice of additional convex constraints;
4. or a certified reason that repair is unsafe near a solvability boundary.

The narrower possible contribution is a **certificate-aware projection**:
select recovered phases to minimize a rigorous downstream injection or
Newton-repair bound, rather than an unweighted state-estimation loss.

Robust synchronization with unsquared deviations also exists, so an
\(\ell_1\) phase objective alone is not new.  The remaining distinction is
the buswise admittance weighting, minimax structure, approximation guarantee
for the physical injection certificate, and composition with a feasibility
condition number.

The first synthetic comparison supports only a modest claim: the minimax LP
usually lowers the certificate score relative to weighted phase least
squares, but conditioning can reverse that ranking near a solvability
boundary.  This motivates direct conditioning-aware selection; it does not
yet establish superiority over full state-estimation recovery.

## Novelty guardrail

The elementary rank-one cycle criterion in this project is foundational, not
yet a publishable novelty claim.  The potentially new contribution would
need to be one of:

- a sharp quantitative stability theorem from edge/cycle defects to voltage
  and power-flow residuals;
- a useful a posteriori optimality-gap certificate;
- a topology-parameterized exactness theorem stronger than known conditions;
- or an adaptive algorithm that materially improves certified benchmark
  performance.

Before any novelty claim, we must audit work on:

- angle recovery in branch-flow models;
- matrix completion on chordal graphs;
- error bounds for approximate rank-one PSD matrices;
- moment/SOS hierarchies for OPF;
- feasible recovery from SOCP/SDP relaxations;
- and cycle-space formulations of Kirchhoff voltage laws.
