# Full-AC recovery on pinned PGLib topologies

## Scope

This experiment advances beyond the fixed-magnitude lossless model:

- complex conductance and susceptance;
- voltage magnitudes;
- active and reactive injections;
- bus shunts and line charging;
- transformer taps and phase shifts;
- REF/PV/PQ power-flow structure;
- and the full reduced polar Jacobian.

It uses real PGLib network data but synthetic edge-relaxed moments.  It is
not yet an experiment on the output of an OPF relaxation.

## Data and validation

PGLib-OPF release v23.07 is pinned.  The vendored PJM-5 and IEEE-14 files are
checksummed in `data/pglib-opf-v23.07/README.md`.

The analytic \(2n\)-dimensional polar Jacobian is checked against centered
finite differences on IEEE-14.  Newton power flow converges from the flat
case initialization on both networks.

## Moment model

Starting from a solved voltage \(V\), every network edge receives

\[
W_{ij}
=V_i\overline V_j
\exp(-|\xi_{ij}|)\exp(i\eta_{ij}),
\]

where the displayed multiplication means the physical edge moment is
multiplied by the two factors, with
\(\xi_{ij}\sim N(0,\sigma_r^2)\) and
\(\eta_{ij}\sim N(0,\sigma_\theta^2)\).  Diagonal moments remain
\(|V_i|^2\).  Thus every edge obeys

\[
|W_{ij}|^2\leq W_{ii}W_{jj},
\]

although the partial moment data need not have a global PSD completion.

Four recoveries are compared:

1. radial-aware buswise minimax LP;
2. phase-only buswise minimax LP;
3. weighted phase least squares;
4. maximum-admittance-weight spanning-tree recovery.

## Moderate-defect results

For 200 trials per case with
\((\sigma_\theta,\sigma_r)=(0.01,0.005)\):

| Case | Method | Median exact residual | Median moment bound | Median \(\beta\rho\) | Score wins | Repairs |
|---|---|---:|---:|---:|---:|---:|
| PJM-5 | Radial-aware LP | 1.01109 | 1.17221 | 0.06144 | 166/200 | 200/200 |
|  | Phase-only LP | 1.02080 | 1.23415 | 0.06455 | 22/200 | 200/200 |
|  | Weighted LS | 0.95364 | 1.21512 | 0.06357 | 7/200 | 200/200 |
|  | Maximum-weight tree | 1.32658 | 1.55199 | 0.08119 | 5/200 | 200/200 |
| IEEE-14 | Radial-aware LP | 0.18045 | 0.21955 | 0.55663 | 171/200 | 200/200 |
|  | Phase-only LP | 0.18162 | 0.23437 | 0.59407 | 19/200 | 200/200 |
|  | Weighted LS | 0.16059 | 0.24947 | 0.63276 | 10/200 | 200/200 |
|  | Maximum-weight tree | 0.23246 | 0.29252 | 0.74210 | 0/200 | 200/200 |

The radial-aware LP improves the certificate it was designed to optimize.
Weighted least squares nevertheless has the smaller actual mismatch.

Median Newton correction on PJM-5 was 0.00644 for radial-aware LP versus
0.00379 for least squares.  On IEEE-14 it was 0.04908 versus 0.04352.

## Stress test

At \((\sigma_\theta,\sigma_r)=(0.2,0.1)\), IEEE-14 repair success was:

| Method | Repairs |
|---|---:|
| Radial-aware LP | 74/100 |
| Phase-only LP | 77/100 |
| Weighted LS | 91/100 |
| Maximum-weight tree | 74/100 |

At \((0.4,0.2)\), the corresponding counts were 4, 4, 12, and 2.

## Interpretation

The negative result is substantive.  The rigorous moment bound uses absolute
values and triangle inequalities, intentionally discarding cancellation.
That makes it suitable for certification but a poor proxy for typical
Newton correction size.  Optimizing it can move the recovered point away
from a favorable nonlinear basin even while reducing the certified
worst-case residual.

The next candidate objective should retain directional information, for
example a local sensitivity score based on

\[
\|J(\widehat V)^{-1}r(\widehat V)\|,
\]

while the buswise moment bound remains a separate safety certificate.

The experiment must also be repeated on actual relaxation outputs.  Random
edgewise PSD moments do not reproduce the correlations introduced by a QC,
SOCP, or SDP optimization.

## Reproduce

```bash
.venv/bin/python scripts/benchmark_full_ac_recovery.py \
  --trials 200 --seed 20260726

.venv/bin/python scripts/benchmark_full_ac_recovery.py \
  --trials 100 --seed 20260726 \
  --phase-sigma 0.2 --radial-sigma 0.1
```
