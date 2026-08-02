# Cycle 91 preregistration: equal-height saddle-collision profiler

## Claim boundary

This is discovery only. Every finite count, fitted slope, and web statistic is
`OBSERVED`; no asymptotic collision estimate, equal-height bound, moment
theorem, Fourier-band closure, density gain, or interval gain may be promoted.

## Frozen experiment

- `D in {512,1024,2048,4096,8192,16384,32768}`.
- `Q=round(D^(5/9))`, reflecting `Q=X^(1/3)`, `D=X^(3/5)`.
- `xi in {16/25,7/10,3/4}` and `K=round(D^(xi/(3/5)))`.
- `n` ranges over every integer `Q<=n<2Q`.
- `a` ranges over every integer
  `-floor(D log(2)/(4pi))<=a<=floor(D log(2)/(4pi))`.
- Set `y=n exp(2pi a/D)`, choose `n'=round(y)` using NumPy's frozen
  nearest-even rule, and retain the row only if `Q<=n'<2Q` and
  `|n'-y|<=1/K`.
- The exact diagonal `(a,n,n')=(0,n,n)` is reported separately and excluded
  from off-diagonal counts.
- No RNG, subsampling, adaptive scale, or post-result threshold choice.

## Frozen outputs

For every `(D,xi)` report:

1. off-diagonal collision count `C`;
2. `C/(DQ/K)` and `C/Q`;
3. number of occupied nonzero `a`, maximum collisions for one `a`, maximum
   collisions for one `n`, and the ten smallest off-diagonal scaled errors
   `K|n'-y|` with their labels.

For each `xi`, fit slopes of `log(max(C,1))`, `log(max(C,1)/(DQ/K))`, and
`log(max(C,1)/Q)` against `log D` across all seven scales. Classify
`C/Q` only as `OBSERVED_GROWING`, `OBSERVED_FLAT`, or `OBSERVED_DECAYING`
using thresholds `slope>0.15`, `|slope|<=0.15`, and `slope<-0.15`.

## Failure rule

Any nonfinite exponential, missing row, retained out-of-range `n'`, diagonal
leak into the off-diagonal count, or unavailable NumPy dependency halts the
aggregate output. No row may be dropped.

