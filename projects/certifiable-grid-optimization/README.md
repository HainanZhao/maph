# Certifiable grid optimization

This project studies mathematical certificates for alternating-current
optimal power flow (AC-OPF).  The long-term objective is an algorithm that
returns both a feasible dispatch and a rigorous bound on its distance from
global optimality.

The first target is deliberately narrower:

> Quantify when edge-local convex moment data on a unicyclic network can be
> recovered as one globally consistent voltage vector, and determine how
> those recovery defects control an AC-OPF relaxation gap.

The distinction between **voltage recoverability** and **objective
optimality** is essential.  A rank-one completion theorem addresses the
former; it does not by itself prove that a relaxation solves AC-OPF.

**Current status:** paused after genuine PGLib SOCP experiments showed that
the certificates are useful diagnostics but the tested recovery objectives
do not improve dispatch-level operational feasibility.  See the
[research summary](docs/research-summary.md) for the results, negative
evidence, and restart criterion.

## Layout

- `src/cycle_certificate.py`: dependency-free cycle and edge-rank defects.
- `src/sparse_phase_lp.py`: sparse minimax LP, least-squares, and tree
  phase-recovery rules.
- `src/lossless_graph.py`: reduced Jacobian and conservative repair score.
- `src/conditioning_aware.py`: angle-trust-region LP sweep and verified
  candidate selection.
- `src/matpower.py`: safe numeric MATPOWER-v2 parser.
- `src/ac_power_flow.py`: full complex AC injections, polar Jacobian, and
  Newton REF/PV/PQ power flow.
- `src/full_ac_recovery.py`: radial-aware complex-moment recovery and
  residual scoring.
- `src/socp_relaxation.py`: independently audited edge-SOCP AC-OPF
  relaxation using pinned CVXPY and Clarabel.
- `src/ac_feasibility.py`: generator allocation and operational AC audits.
- `src/adaptive_thermal.py`: recovery-informed thermal-tightening experiment.
- `tests/test_cycle_certificate.py`: exact and adversarial unit tests.
- `scripts/explore_triangle.py`: reproducible three-bus examples.
- `scripts/benchmark_sparse_phase_recovery.py`: deterministic sparse-graph
  comparison.
- `scripts/benchmark_full_ac_recovery.py`: recovery experiments on pinned
  PGLib topologies.
- `scripts/experiment_socp_recovery.py`: recovery from genuine SOCP moments.
- `scripts/experiment_adaptive_thermal.py`: adaptive-tightening stress test.
- `docs/mathematics.md`: definitions, proved statements, and proof drafts.
- `docs/research-summary.md`: executive result summary and stopping record.
- `docs/progress.md`: dated claim ledger.
- `docs/literature-audit.md`: primary-source comparison and novelty guardrail.
- `docs/synthetic-benchmark.md`: protocol, results, and limitations.
- `docs/full-ac-benchmark.md`: full-AC PGLib-topology experiment.
- `docs/actual-relaxation-benchmark.md`: genuine SOCP results and project
  decision.
- `docs/roadmap.md`: staged research plan and exit criteria.

## Quick start

Run commands from this directory:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/explore_triangle.py
.venv/bin/python scripts/explore_feasibility_repair.py
.venv/bin/python scripts/explore_phase_projection.py
.venv/bin/python scripts/benchmark_sparse_phase_recovery.py
.venv/bin/python scripts/benchmark_full_ac_recovery.py
.venv/bin/python scripts/experiment_socp_recovery.py
.venv/bin/python scripts/experiment_adaptive_thermal.py
```

The sparse LP uses SciPy's HiGHS interface.  Its version is pinned in
`requirements.txt`; every solver result used by the code is independently
checked against the returned angles.

The SOCP experiments pin CVXPY 1.6.1, the final supported line for the
workspace's Python 3.9 runtime, and explicitly select Clarabel 0.11.1.  Every
reported conic point is independently audited after solving.

## Claim standard

1. A feasible voltage recovery is not automatically an optimal dispatch.
2. Numerical success is not evidence of universal relaxation exactness.
3. Every computational certificate must be independently checkable.
4. General AC-OPF is hard; theorems must state their topology, parameter, and
   regularity assumptions explicitly.
