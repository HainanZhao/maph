# Recovery from genuine SOCP relaxation moments

## Question

Do the certificate-aware phase projections improve physical recovery when
the moment data come from a real AC-OPF relaxation rather than independent
synthetic perturbations?

The answer on the first four pinned benchmarks is **no**.

## Reproducible stack

- PGLib-OPF v23.07;
- CVXPY 1.6.1;
- Clarabel 0.11.1;
- SciPy 1.13.1;
- NumPy 2.0.2.

CVXPY 1.6.1 is used because the workspace runs Python 3.9.  Clarabel is
selected explicitly.

## Independent SOCP audit

| Case | Objective | Hermitian | Balance | Edge PSD | Thermal |
|---|---:|---:|---:|---:|---:|
| PJM-5 typical | 14999.715931 | 0 | \(1.46\cdot10^{-13}\) | \(2.40\cdot10^{-9}\) | 0 |
| IEEE-14 typical | 2175.704548 | 0 | \(4.88\cdot10^{-13}\) | \(1.49\cdot10^{-9}\) | 0 |
| PJM-5 congested | 77571.356004 | 0 | \(4.38\cdot10^{-10}\) | \(1.41\cdot10^{-8}\) | \(3.66\cdot10^{-7}\) |
| IEEE-14 congested | 5691.798475 | 0 | \(4.34\cdot10^{-14}\) | \(6.29\cdot10^{-9}\) | \(8.69\cdot10^{-9}\) |

Violations are in per-unit constraint scales except the objective, which is
recomputed exactly.  The objectives agree with the lower-bound scales in
PGLib's baseline table.

## Recovery comparison

The radial-aware minimax LP, phase-only LP, weighted phase least squares, and
maximum-weight spanning tree all converged to the same repaired power-flow
solution for each case.  Their initial moment bounds differed, but their
operational result did not.

| Case | SOCP lower bound | Best \(\beta\rho\) | Newton/Q switches | Repaired cost | Maximum operational violation |
|---|---:|---:|---:|---:|---:|
| PJM-5 typical | 14999.715931 | 0.033051 | 2 / 1 | 14999.715926 | 43.3249 MVA thermal |
| IEEE-14 typical | 2175.704548 | 0.503233 | 2 / 1 | 2178.082069 | \(1.19\cdot10^{-8}\) |
| PJM-5 congested | 77571.356004 | 0.007188 | 2 / 0 | 77571.071747 | 11.1932 MVA thermal |
| IEEE-14 congested | 5691.798475 | 0.173700 | 2 / 1 | 5690.637596 | 4.08226 MVA thermal |

Only IEEE-14 typical becomes an audited AC-feasible dispatch.  Its certified
gap using the untouched SOCP lower bound is

\[
100\frac{2178.082069-2175.704548}{2178.082069}
=0.1092\%.
\]

The other displayed repaired costs are not upper bounds because their points
violate thermal constraints.

## Counterexample to score interpretation

PJM-5 congested has a very small local score,

\[
\beta\rho\approx0.00719,
\]

and Newton converges in two iterations.  Nevertheless, the resulting
physical point overloads a line by 11.19 MVA.

Therefore, a small equality-repair score does not imply AC-OPF feasibility.
The missing quantity is the margin to every operational inequality.

## Adaptive thermal experiment

After each failed recovery, the implicated SOCP line rating was reduced by
the recovered overload and the relaxation was re-solved.  The original
untightened SOCP objective was retained as the only valid lower bound.

This did not work:

- PJM-5 typical reduced its overload from 43.32 to 18.83 MVA before the next
  tightened relaxation became infeasible.
- PJM-5 congested became infeasible after its first proposed tightening.
- IEEE-14 congested retained 3.84 MVA overload after twelve iterations.
- gains \(0.1,0.25,0.5\) over twenty iterations did not produce feasibility.

Tightening relaxed branch flow is not a reliable proxy for tightening the
flow of the rank-recovered voltage.

## Conclusion

The certificate remains useful for diagnosis:

- it measures rank-recovery damage;
- it identifies equality conditioning;
- and it separates locally repairable moment data from singular cases.

It has not demonstrated value as a recovery optimizer.  On genuine
relaxation outputs, conventional weighted least squares is already adequate
as an initializer, while material relaxation gaps require redispatch,
penalization, a stronger relaxation, or local AC-OPF.

This is a justified stopping point for the current algorithmic direction.

## Reproduce

```bash
.venv/bin/python scripts/experiment_socp_recovery.py
.venv/bin/python scripts/experiment_adaptive_thermal.py
```
