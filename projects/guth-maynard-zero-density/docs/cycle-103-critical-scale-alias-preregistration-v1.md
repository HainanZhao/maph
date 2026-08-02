# Cycle 103 preregistration: critical-scale alias inverse

Date frozen: 2026-08-02 UTC.

## Claim boundary

This cycle reinserts the small critical-value condition into one fixed
Cycle-102 cross core. It may prove a one-dimensional scale-alias inverse for
the coefficient multiplier `lambda`. It does not claim an irrationality
measure for the resulting algebraic number, an aggregate exceptional-web
bound, weak/simple-root control, a complete moment, or a density/interval
gain.

## Frozen data

- `s,t>0`, `W=s+t`, reduced `r=N/R>0`, and the exact critical equation
  `r=C0*t/(B0*s)`.
- `B=lambda*B0`, `C=lambda*C0`, `1<=lambda<=Lambda`.
- `t*=log(r)/W` and
  `K=B0*r^(s/W)+C0*r^(-t/W)`.
- `A` is an integer and the critical residual is `|A-lambda*K|`.
- The near-double critical-value tolerance is the explicit Cycle-97 bound;
  the scale-alias lemma denotes any valid frozen upper bound by `epsilon`.
- All norms `||z||` mean distance to the nearest integer.

## Gates

1. **Homogeneity gate.** Prove the critical point is independent of
   `lambda` and `f(t*)=A-lambda*K` exactly.
2. **Algebraic gate.** Prove `K` is positive algebraic of degree at most `W`
   by placing it in `Q(r^(1/W))`. Do not claim a useful height or separation
   bound unless independently derived.
3. **Near-double transfer gate.** Record that Cycle 97 supplies
   `|A-lambda*K|<=epsilon` at the critical point; do not replace its explicit
   tolerance by the residual at the observation point.
4. **Alias inverse gate.** If `J>=2` distinct scales in `[1,Lambda]` satisfy
   the tolerance, prove that some
   `1<=q<=floor((Lambda-1)/(J-1))` obeys `||qK||<=2epsilon`. Equivalently, if
   `q_epsilon` is the least positive `q<=Lambda-1` with
   `||qK||<=2epsilon`, prove `J<=1+floor((Lambda-1)/q_epsilon)`; if no such
   `q` exists, prove `J<=1`.
5. **Exact replay gate.** Test the inverse lemma with rational surrogates
   using exact arithmetic, including ties and the no-alias case. Verify the
   critical identity on exhaustive small Cycle-102 cores.
6. **Boundary gate.** Treat a small `q` as structured E16 output, not as
   cancellation. Any aggregate theorem must still count core splits or use
   the actual phases.

## Outcomes

- Passing all gates replaces raw `lambda` multiplicity by the dichotomy
  `one hit or a short algebraic scale alias`.
- A failed identity preserves the first exact counterexample and stops this
  formulation.
- No hostile paper-stage audit is authorized.

## Replay

```sh
python3 proof/build_cycle_103_critical_scale_alias_v1.py --check
python3 -m unittest tests/test_cycle_103_critical_scale_alias_v1.py
```
