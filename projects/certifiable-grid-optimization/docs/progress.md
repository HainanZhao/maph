# Progress and claim ledger

## 2026-07-26 — research cycle 0

### Objective selected

Develop certifiable AC-OPF methods, beginning with unicyclic networks and
cycle-local relaxation defects.

### Proved

1. Edge moments on a connected graph admit a global rank-one voltage
   completion exactly when every edge saturates its \(2\times2\) PSD
   inequality and the normalized phases have trivial holonomy on a cycle
   basis.
2. On a unicyclic graph, only one independent holonomy condition is needed.
3. Spanning-tree voltage recovery has the exact per-edge residual identity
   recorded as Eq. (2) in `mathematics.md`.
4. The residual can be written exactly using the radial defect and the
   tree-induced phase defect, Eq. (3).
5. AC bus-injection residuals obey the local admittance-weighted certificate
   in Theorem 2.

These are foundational lemmas.  Novelty has not been claimed.

### Counterexample

Zero phase holonomy alone is insufficient: a triangle with unit diagonals and
all edge moments \(\rho\in(0,1)\) has zero angular defect but has no rank-one
completion.

### Computational

A dependency-free checker and tests were added for radial defects, holonomy,
tree recovery, and the phase-only counterexample.

### Conjectural target

The next conjectural step is a **feasibility repair theorem**: under explicit
Jacobian nonsingularity and constraint-margin assumptions, sufficiently
small certified injection residual should imply a nearby AC-feasible voltage
whose displacement and cost increase are quantitatively bounded.

### Main risk

Even a sharp voltage-recovery theorem may not control the global objective
gap.  A useful certificate will likely need both:

- a convex-relaxation lower bound; and
- a separately feasible recovered upper bound.

## 2026-07-26 — research cycle 1

### Assumptions challenged

1. **Cycle recovery is not new.** Farivar and Low already gave a cycle-angle
   recovery condition and spanning-tree algorithm in the branch-flow model.
2. **Generic local solvability is not new.** Fixed-point,
   Newton--Kantorovich, and quadratic-solvability-region methods already
   certify power-flow solutions under regularity assumptions.
3. **Small physical residual is insufficient.** At a voltage-collapse
   boundary, an arbitrarily small injection residual can correspond to an
   infeasible target.
4. **A basic feasible-lower/upper-bound workflow is established practice.**
   The project needs a sharper or cheaper certificate, not merely that
   workflow restated.

### New proved counterexample

On the unit lossless triangle, the point
\((\theta_1,\theta_2)=(\pi/2,\pi/2)\) produces injection \((1,1)\).
For every \(\epsilon>0\), the target
\((1+\epsilon,1+\epsilon)\) is only \(\epsilon\) away in infinity norm but is
infeasible because every feasible injection satisfies \(P_1+P_2\leq2\).

### Implemented

- Exact two-angle lossless triangle injections and Jacobian.
- A dependency-free Newton solver.
- A conservative Newton--Kantorovich certificate.
- Tests for certified repair, singularity, and arbitrarily small infeasible
  residuals.

### Refined research question

Can relaxation-specific radial and holonomy defects be combined with
Jacobian conditioning to produce a certificate that is materially sharper
or cheaper than applying a generic power-flow solvability test after the
fact?

The most promising form is an **adaptive safety certificate**:

- if the combined defect and condition number are small, certify fast local
  repair and a resulting objective upper bound;
- if conditioning is poor, identify the buses/cycles responsible and add
  targeted convex constraints or request a stronger solve.

### Conditional theorem

The exact defect residual and a standard Newton--Kantorovich argument compose
to give Theorem 3 in `mathematics.md`: if
\(\beta^2L\rho\leq1/2\), where \(\rho\) is obtained from radial and holonomy
defects, then a power-flow solution exists within an explicit radius of the
tree-recovered voltage.  This is a valid theorem but not yet a novelty claim.

### New algorithmic counterexample

Spanning-tree recovery is not error optimal.  On a unit triangle with
holonomy angle \(\delta\), it has squared edge error
\(4\sin^2(\delta/2)\).  Equally distributing the inconsistency has error
\(12\sin^2(\delta/6)\), which is strictly smaller for
\(0<|\delta|\leq\pi\) and three times smaller asymptotically as
\(\delta\to0\).

This suggests replacing tree recovery by **certificate-aware phase
projection**.  The novelty risk is substantial because angular
synchronization and state-estimation-based AC recovery already exist.  The
distinguishing objective would be minimizing a rigorous downstream repair
bound rather than an unweighted phase or measurement loss.

## 2026-07-26 — research cycle 2

### Questions answered

1. **Does smaller squared phasor error imply a better repair certificate?**
   Not automatically; the relevant buswise objective is a weighted minimax
   sum of edge residuals.
2. **Is equal distribution still optimal for that objective?** Yes on the
   equal-weight triangle.  Theorem 4 proves it minimizes the exact nonlinear
   worst-bus bound.
3. **Is equal distribution optimal with unequal line weights?** No.  The
   \((5,1,1)\) example makes it worse than the best tree.
4. **Is minimizing the residual bound \(\rho\) sufficient?** No.  The
   inverse-Jacobian factor depends on the recovered angles and dominates near
   voltage collapse.

### Proved

For a unit-weight triangle with principal holonomy
\(\delta\in[0,\pi]\), equal allocation minimizes the exact worst-bus
injection certificate, with optimum \(4\sin(\delta/6)\).

### Computational

- For weights \((5,1,1)\) and \(\delta=0.6\), a 600-step grid search improves
  the best-tree bound from \(0.591040\) to \(0.544306\), while balanced
  recovery is much worse at \(1.198001\).
- For weights \((4,2,1)\), the grid optimum is a tree allocation.
- A conditioning-aware grid search detects that the same small phase defect
  can be certifiable in a well-conditioned region and uncertifiable closer
  to collapse.

### Refined target

Optimize the composed safety quantity

\[
\beta(\widehat\theta)^2 L(\widehat\theta)\rho(\widehat\theta),
\]

not phase error or injection residual alone.  The main question is whether a
tractable upper surrogate can retain enough of this conditioning dependence
to outperform state-estimation recovery on certification rate.

### New scalable surrogate

On a fixed winding branch, minimizing the worst-bus weighted sum of absolute
phase corrections is a linear program.  Theorem 5 proves that its solution
approximates the exact nonlinear injection-certificate optimum within

\[
\frac{\gamma}{2\sin(\gamma/2)}
\]

when all corrections have magnitude at most \(\gamma\).  The factor tends to
one quadratically as \(\gamma\to0\) and is never worse than \(\pi/2\) on a
principal branch.

This creates a scalable candidate algorithm, but robust
\(\ell_1\)-synchronization is prior art.  The publishable question is whether
the OPF-specific buswise objective and its conditioning-aware composition
produce materially higher certification rates.

## 2026-07-26 — research cycle 3

### Implemented and verified

- A general fixed-winding sparse-graph LP using the pinned
  `scipy==1.13.1` HiGHS interface.
- Independent reconstruction of all phase corrections and the LP objective.
- Weighted phase least squares and exact spanning-tree recovery comparators.
- A reduced fixed-magnitude lossless Jacobian, a conservative global
  Jacobian-Lipschitz constant, and the composed
  \(\overline h=\beta^2L\rho\) score.
- Twenty-six passing exact, adversarial, and regression tests.

### Assumption challenged

The hypothesis that lower physical residual should mean a better repair
certificate is false.  A four-bus witness has

\[
\rho_{\rm LP}<\rho_{\rm LS}
\quad\text{but}\quad
\overline h_{\rm LP}=0.5000405>
\overline h_{\rm LS}=0.4967503.
\]

The weighted least-squares point is certified by the current sufficient
condition while the residual-optimal LP point is not.  The reversal is caused
by the recovered Jacobian condition number.

### Synthetic benchmark

A deterministic 1,500-instance study on a four-bus square with a diagonal
compared the minimax LP, weighted least squares, and an oracle choice among
all spanning trees.  LP versus least-squares certification counts were:

| Regime | Minimax LP | Weighted LS | Oracle tree |
|---|---:|---:|---:|
| Secure, moderate noise | 485/500 | 480/500 | 475/500 |
| Loaded, moderate noise | 363/500 | 337/500 | 334/500 |
| Near-boundary, high noise | 61/500 | 56/500 | 51/500 |

The LP had a strictly lower residual than least squares in every sampled
instance, but conditioning reversed the composed-score ordering in 3, 4,
and 50 instances respectively.  These are synthetic algorithm-development
results, not evidence of operational superiority.

### Current assessment

The LP is a viable scalable baseline and modestly improves certification rate
in the controlled experiment.  The novel opportunity is no longer the LP
alone.  It is a conditioning-aware candidate-selection or optimization
method whose advantage survives on standard OPF relaxation outputs.

The next decisive step is a PGLib study.  Before that, the model must be
extended beyond fixed magnitudes and lossless active-power equations to
include complex voltages, radial moment defects, reactive power, voltage
limits, and the same input data used by established recovery methods.

## 2026-07-26 — research cycle 4

### New proved tool

Theorem 6 gives an inverse-Jacobian bound throughout an angle trust region:

\[
\|J(\theta)^{-1}\|
\leq
\frac{\beta_0}{1-\beta_0Lr}
\quad\text{when}\quad
\|\theta-\theta_0\|\leq r,\ \beta_0Lr<1.
\]

This is a direct Banach/Neumann perturbation result, not a novelty claim.
Its useful consequence is algorithmic: adding an infinity-norm trust region
to the phase minimax program preserves linearity and supplies a rigorous
conditioning penalty for every chosen radius.

### Implemented

- Optional angle trust regions in the sparse minimax LP.
- A checked reference-conditioning bound.
- A radius-sweep method that evaluates the actual composed score and selects
  among the reference, trust-region solutions, and unconstrained LP.
- Three additional tests, bringing the suite to 29 passing tests.

### Result

On the existing 1,500-instance benchmark, conditioned selection never
reduced the certification count relative to the minimax LP.  It did not add
certified instances at the current sample size, but reduced the near-boundary
90th-percentile score from \(6.6208\) to \(6.5164\).  This is too small to be
a contribution, but it validates the algorithmic plumbing and honestly
shows that the present radius grid does not solve the hard cases.

### Literature challenge

Lee et al.'s convex restriction of power-flow feasibility already constructs
scalable inner regions around a known feasible nonsingular point, includes
operational constraints, and uses fixed-point bounds.  Consequently, the
trust-region idea alone is established territory.  Any contribution must
come from its coupling to relaxation-specific defects and demonstrated
recovery/certification gains.

## 2026-07-26 — research cycle 5

### Full-AC infrastructure

- Pinned PGLib-OPF v23.07 and vendored checksummed PJM-5 and IEEE-14 cases.
- Added a safe MATPOWER-v2 numeric parser that does not execute MATLAB.
- Implemented MATPOWER-compatible \(Y_{\rm bus}\), including line charging,
  bus shunts, transformer taps, and phase shifters.
- Implemented full complex \(P/Q\) injections and their polar Jacobian.
- Verified every IEEE-14 Jacobian column against centered finite
  differences.
- Implemented and tested REF/PV/PQ Newton power flow and arbitrary-injection
  repair.
- The suite now contains 39 passing tests.

### New theorem

Theorem 7 extends the fixed-winding LP to edge-radial slack.  The fixed
radial defects enter as buswise offsets, while phase corrections remain
linear.  Under \(|W_{ij}|/\sqrt{W_{ii}W_{jj}}\geq\kappa>0\), the LP has an
explicit approximation factor for the exact complex moment-residual
certificate.  This is proved, but novelty has not been established.

### Real-topology experiment

Synthetic locally PSD edge moments were generated around solved PJM-5 and
IEEE-14 operating points.  At phase/radial noise \(0.01/0.005\), the
radial-aware LP minimized the conservative \(\beta\rho\) score in 337 of 400
trials.  However, weighted phase least squares had smaller median exact
injection mismatch and required smaller Newton corrections.

At stronger IEEE-14 noise \(0.2/0.1\), repair succeeded for:

| Method | Successful repairs |
|---|---:|
| Radial-aware minimax LP | 74/100 |
| Phase-only minimax LP | 77/100 |
| Weighted phase least squares | 91/100 |
| Maximum-weight tree | 74/100 |

At noise \(0.4/0.2\), least squares still repaired 12/100 targets while the
radial-aware LP repaired 4/100.

### Assumption rejected

Optimizing the rigorous buswise moment-residual bound does **not** reliably
minimize actual repair distance or maximize the Newton basin.  The bound is
valuable for safety accounting, but its triangle inequalities discard
directional cancellation that matters to the nonlinear solver.

### Decision

Stop tuning the buswise minimax objective on synthetic defects.  The next
cycle should:

1. obtain actual QC/SOCP/SDP relaxation moments rather than independent edge
   perturbations;
2. compare against the full state-estimation recovery of Taheri--Molzahn;
3. test a sensitivity-aware objective based on
   \(J^{-1}r\), while keeping the buswise bound only as a separate safety
   certificate.

## 2026-07-27 — research cycle 6

### Genuine SOCP relaxation

The project now solves the full edge-based SOCP AC-OPF relaxation, including:

- affine complex \(P/Q\) balance from \(W\);
- generator and voltage bounds;
- every edge \(2\times2\) PSD cone;
- phase-angle wedges;
- both-end apparent-power limits;
- and convex polynomial generation costs.

CVXPY 1.6.1 and Clarabel 0.11.1 are pinned.  A separate audit recomputes
every constraint and objective without trusting the modeling layer.
The complete project suite now has 42 passing tests.

The returned objectives agree with the published PGLib scales:

| Case | SOCP objective | Maximum audit violation |
|---|---:|---:|
| PJM-5 typical | 14999.715931 | \(2.40\times10^{-9}\) |
| IEEE-14 typical | 2175.704548 | \(1.49\times10^{-9}\) |
| PJM-5 congested | 77571.356004 | \(3.66\times10^{-7}\) |
| IEEE-14 congested | 5691.798475 | \(8.69\times10^{-9}\) |

### Recovery result

All four recovery rules reached the same power-flow branch in two or three
Newton iterations.  Lower moment residual did not change the repaired
dispatch.

After aggregate reactive-limit switching:

- IEEE-14 typical produced a fully audited AC dispatch costing
  2178.082069, giving a certified 0.1092% gap against the untouched SOCP
  lower bound.
- PJM-5 typical still overloaded a line by 43.3249 MVA.
- PJM-5 congested still overloaded a line by 11.1932 MVA.
- IEEE-14 congested still overloaded a line by 4.08226 MVA.

Thus local voltage consistency can be repaired while OPF feasibility remains
false.  In particular, the congested PJM-5 instance has
\(\beta\rho\approx0.00719\) but an 11.19 MVA thermal violation.  This is a
concrete counterexample to interpreting a small injection-repair score as an
OPF-feasibility certificate without inequality margins.

### Adaptive tightening rejected

A recovery-informed loop tightened only branches overloaded after physical
recovery while retaining the original SOCP value as the lower bound.

- PJM-5 typical reduced the overload but became relaxation-infeasible before
  reaching an AC-feasible point under the default update.
- PJM-5 congested could not tolerate even the first direct tightening.
- IEEE-14 congested reduced its overload from 4.08226 to only 3.83946 MVA
  after twelve solves.
- Smaller-gain sweeps through twenty iterations did not converge.

The mechanism is flawed: tightening the relaxed flow does not directly
control the rank-recovered physical flow and can exclude valid original AC
solutions.

### Project decision

The current certificate is mathematically sound as a diagnostic but is not a
competitive recovery objective.  The simplest adaptive strengthening rule
also fails.  Pause this direction rather than manufacture a positive story.
Resume only if a new method retains directional residual information or
couples moment defects to operational inequality margins without destroying
the original feasible set.
