# Research summary and stopping record

## Bottom line

This project developed a rigorous diagnostic framework for recovering an AC
voltage vector from edge-based convex moment data.  The framework detects
radial and phase inconsistency, proposes several phase-recovery rules, and
combines their residuals with local power-flow conditioning.

The central practical hypothesis did not survive testing on genuine SOCP
relaxation outputs.  On the tested PGLib cases, different recovery objectives
converged to the same power-flow branch and therefore did not repair the
dispatch-level constraint violations left by the relaxation.  A first
recovery-informed thermal-tightening scheme reduced some overloads but did
not reliably restore feasibility.  The project is therefore paused rather
than promoted as a successful AC-OPF algorithm.

This is a deliberate negative result: the certificate remains useful as a
diagnostic, but the current recovery objective is not a competitive route
from a loose relaxation to an operationally feasible dispatch.

## Mathematical results

The project established or recorded the following statements.  The detailed
assumptions and proofs are in `mathematics.md`.

1. **Rank-one edge completion.**  Connected edge moment data admit a global
   voltage vector exactly when every edge \(2\times2\) PSD constraint is
   saturated and the normalized edge phases have trivial holonomy on every
   cycle.  This is a foundational completion fact and is not claimed as the
   main novelty.
2. **Exact recovery-error decomposition.**  Each recovered edge mismatch
   splits exactly into radial slack and phase inconsistency.  This yields a
   buswise, admittance-weighted bound on the resulting complex-injection
   residual.
3. **Residual is not feasibility.**  A lossless-triangle construction shows
   that arbitrarily small injection residual does not guarantee a nearby
   feasible power-flow point when the Jacobian approaches singularity.
4. **Conditional local feasibility.**  A Newton--Kantorovich argument gives
   a nearby-solution certificate under an explicit regularity condition,
   including \(\beta^2L\rho\leq 1/2\), where \(\rho\) is the residual,
   \(\beta\) bounds the inverse Jacobian, and \(L\) bounds Jacobian variation.
5. **Sparse phase projection.**  For a fixed winding sector, phase recovery
   is a linear minimax problem.  On an equal-weight triangle, balanced cycle
   correction is minimax optimal.  The angular surrogate has approximation
   factor \(\gamma/(2\sin(\gamma/2))\) on \(|x|\leq\gamma\).
6. **Radial-aware approximation.**  For edge radius
   \(r=\sqrt{W_{ii}W_{jj}}\), magnitude \(a=|W_{ij}|\), radial deficit
   \(c=r-a\), and phase error \(x\), the exact mismatch is
   \[
   d=\sqrt{c^2+4ra\sin^2(x/2)}.
   \]
   The surrogate \(g=c+r|x|\) satisfies
   \[
   d\leq g\leq
   \sqrt{1+K_\gamma^2/\kappa}\,d
   \]
   when \(a/r\geq\kappa\) and \(|x|\leq\gamma\).  This validates a
   certificate approximation; it does not prove that its minimizer is the
   best practical repair.

Several useful counterexamples were also made explicit:

- zero cycle-phase defect is insufficient when radial slack remains;
- spanning-tree phase recovery can be strictly suboptimal;
- a smaller raw recovery residual can have a worse
  conditioning-aware score;
- a small equality residual can coexist with a material thermal-limit
  violation.

## Computational findings

### Synthetic phase and full-AC tests

In 1,500 four-bus phase-recovery trials, the sparse minimax LP produced more
conservative certificates than weighted least squares, but the ordering was
occasionally reversed after including Jacobian conditioning.  On stressed
IEEE-14 synthetic full-AC moments, weighted least squares more often reached
a converged repair: 91 versus 74 trials at phase/radial noise \(0.2/0.1\),
and 12 versus 4 at \(0.4/0.2\).  Thus minimax defect control did not translate
reliably into better nonlinear repair.

### Genuine SOCP relaxation tests

The edge-SOCP implementation was checked independently for equality, cone,
voltage, generation, and thermal constraints at the conic point.  It used
PGLib-OPF v23.07 data, CVXPY 1.6.1, and Clarabel 0.11.1.

Only the IEEE-14 typical case produced an operationally feasible recovered
upper bound in the tested set:

| Case | SOCP lower bound | Recovered outcome |
| --- | ---: | --- |
| IEEE-14 typical | 2175.704548 | feasible cost 2178.082069; certified gap 0.1092% |
| PJM-5 typical | 14999.715931 | thermal overload 43.3249 MVA |
| PJM-5 API | 77571.356004 | thermal overload 11.1932 MVA |
| IEEE-14 API | 5691.798475 | thermal overload 4.08226 MVA |

All tested recovery rules converged to the same power-flow branch within each
case.  For the congested PJM-5 case, the local equality score was small
(\(\beta\rho\approx0.00719\)) and Newton converged in two iterations, yet the
result still violated a thermal limit by 11.19 MVA.  This sharply separates
local equation solvability from operational feasibility.

### Adaptive thermal tightening

A simple recovery-informed tightening loop reduced the PJM-5 typical overload
from 43.32 to 18.83 MVA before the next tightened SOCP became infeasible.  It
could not take the first tightening step on PJM-5 API, and reduced IEEE-14 API
only from 4.082 to 3.839 MVA after 12 solves.  Gain sweeps over 20 iterations
did not achieve convergence.  These experiments reject the naive feedback
rule as a general remedy.

## Interpretation and claim boundary

What the work supports:

- exact, independently checkable voltage-recoverability diagnostics;
- an explicit distinction between cycle consistency, local power-flow
  solvability, and full OPF feasibility;
- reproducible counterexamples to using recovery residual alone as a proxy
  for operational quality;
- one small certified lower/upper-bound result on IEEE-14 typical.

What it does **not** support:

- a scalable globally certifiable AC-OPF solver;
- a claim that the proposed recovery rules improve feasible upper bounds;
- a claim that equality-residual minimization repairs thermal, voltage, or
  generator-limit violations;
- a publishable positive algorithmic advantage over established recovery and
  feasibility-restoration methods.

## Decision and possible restart condition

The current direction meets the project's kill criterion: once real
relaxation outputs were used, its certificate remained diagnostically sound
but failed to improve the operational recovery outcome.  Work stops here.

The project should be reopened only if there is a materially different idea,
such as a directional residual method that targets active inequality margins,
a joint recovery-and-dispatch formulation with a credible convergence
argument, or a stronger relaxation theorem for a clearly defined network
class.  More tuning of the present scalar recovery score is not, by itself, a
sufficient reason to resume.

## Reproducibility

From the project directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/benchmark_sparse_phase_recovery.py
.venv/bin/python scripts/benchmark_full_ac_recovery.py
.venv/bin/python scripts/experiment_socp_recovery.py
.venv/bin/python scripts/experiment_adaptive_thermal.py
```

The detailed claim ledger is in `progress.md`, the mathematical statements
are in `mathematics.md`, and the final numerical audit is in
`actual-relaxation-benchmark.md`.
