# Synthetic sparse-graph benchmark

## Purpose

This benchmark asks a narrow algorithm-development question:

> Does minimizing a buswise physical phase-residual surrogate improve the
> sufficient local-repair certificate relative to weighted phase least
> squares or spanning-tree recovery?

It does not simulate a full OPF relaxation or establish operational
superiority.

## Protocol

The graph is a four-bus square with diagonal \((0,2)\).  For every trial:

1. draw a physical base angle vector and scale its largest edge difference
   to the scenario loading;
2. draw edge weights log-uniformly from \([0.5,2]\);
3. add independent Gaussian phase inconsistency;
4. recover angles by the minimax LP, weighted least squares, and every
   spanning tree;
5. give the tree comparator the most favorable possible treatment by
   reporting the tree with minimum composed certificate score;
6. calculate \(\rho\), \(\beta=\|J^{-1}\|_\infty\), the global \(L\), and
   \(\overline h=\beta^2L\rho\).

A trial is certified when \(\overline h\leq1/2\).  The random seed is
`20260726`, with 500 trials per scenario.

## Results

| Scenario | Method | Certified | Median \(h\) | 90% \(h\) | Median \(\rho\) |
|---|---|---:|---:|---:|---:|
| Secure / moderate noise | Minimax LP | 485/500 | 0.1438 | 0.3322 | 0.01177 |
|  | Weighted LS | 480/500 | 0.1565 | 0.3738 | 0.01316 |
|  | Conditioned selection | 485/500 | 0.1438 | 0.3322 | 0.01177 |
|  | Oracle tree | 475/500 | 0.1631 | 0.3920 | 0.01344 |
| Loaded / moderate noise | Minimax LP | 363/500 | 0.2988 | 0.8250 | 0.01250 |
|  | Weighted LS | 337/500 | 0.3424 | 0.8967 | 0.01380 |
|  | Conditioned selection | 363/500 | 0.2988 | 0.8250 | 0.01250 |
|  | Oracle tree | 334/500 | 0.3419 | 0.9615 | 0.01396 |
| Near-boundary / high noise | Minimax LP | 61/500 | 1.5752 | 6.6208 | 0.03645 |
|  | Weighted LS | 56/500 | 1.7852 | 7.0632 | 0.04112 |
|  | Conditioned selection | 61/500 | 1.5752 | 6.5164 | 0.03645 |
|  | Oracle tree | 51/500 | 1.8176 | 7.0804 | 0.04192 |

The LP beat least squares in residual in all 1,500 trials.  It also beat
least squares in the composed score in 497/500, 496/500, and 450/500 trials.
Conditioning therefore reversed 3, 4, and 50 residual rankings as the cases
moved toward the boundary.

The conditioned selection evaluates seven minimax LP trust regions centered
at the least-squares point and also includes the two endpoint candidates.
It matched the LP certification counts and slightly reduced the
near-boundary 90th-percentile score.  It did not create an additional
certified case in this sample.

## Reproduce

```bash
.venv/bin/python scripts/benchmark_sparse_phase_recovery.py \
  --trials 500 --seed 20260726
```

## Interpretation and limitations

- The LP improvement is measurable but modest in certification count.
- Near the boundary, residual minimization becomes less reliable because
  small angle changes can strongly affect \(\|J^{-1}\|\).
- The oracle-tree baseline is intentionally generous but is not scalable;
  it enumerates all spanning trees of this small graph.
- The fixed-magnitude lossless model omits reactive power, voltage recovery,
  inequality constraints, generation limits, losses, and optimization cost.
- The phase perturbations are synthetic, not outputs from SOCP or SDP OPF
  relaxations.
- The global Lipschitz constant is conservative and may suppress otherwise
  valid local certificates.

The benchmark justifies proceeding to a conditioning-aware method and a
standard-data experiment.  It does not yet justify a paper-level performance
claim.
