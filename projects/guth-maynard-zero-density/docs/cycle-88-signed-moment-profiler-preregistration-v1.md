# Cycle 88 preregistration: signed-moment finite-scale profiler

## Claim boundary

This is discovery only.  Every output is `OBSERVED`; finite-scale slopes,
normalizations, and anchor comparisons are not proofs and cannot close a
moment or Fourier gate.

## Frozen experiment

- `D in {64,96,128,192,256,384}`.
- `Q=round(D^(5/9))`, reflecting `Q=X^(1/3)`, `D=X^(3/5)`.
- Anchors `c0 in {3/2,5/3,8/5}`.
- Curve indices are all integers `d` with `D/4<=d<3D/4`.
- Denominators are all integers `Q<=q<2Q`, with unit weights.
- Frequencies are `K<=k<2K`, where
  `K=round(D^(xi/(3/5)))` and
  `xi in {16/25,7/10,58/75,9/10,83/75}`.
- The inner `q`-sum is evaluated by the exact finite geometric series, with
  its removable singularity assigned the value `Q`.
- No RNG, sample rejection, adaptive truncation, or post-result anchor choice.

## Frozen outputs

For every row report:

1. `M2/(K*N)`, where `N=#d*Q` and `M2=sum_(k~K)|S_k|^2`;
2. `L1/(K*sqrt(N))`;
3. `max_k |S_k|/sqrt(N)`;
4. the top five normalized large values and their `k` indices.

For each `(anchor,xi)`, fit the least-squares slope of
`log(M2/(KN))` against `log D` using all six frozen `D` values.  Classify only
as `OBSERVED_GROWING`, `OBSERVED_FLAT`, or `OBSERVED_DECAYING` using frozen
thresholds `slope>0.15`, `|slope|<=0.15`, and `slope<-0.15`.

## Failure rule

Any nonfinite row, geometric-series disagreement at an exact singularity,
or unavailable NumPy dependency preserves the row as failed and halts the
aggregate classification.  No row may be dropped.

