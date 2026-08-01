# Cycle 5 conditional density-to-short-interval map v1

## Claim boundary

`PROVED`, conditional on the same explicit-formula, near-one density,
zero-free, multiplicity, and range inputs closed in G0: replacing the uniform
density coefficient \(B=30/13\) by a proof-grade coefficient

\[
B_\eta=\frac{30}{13}-\eta
\]

changes the two exponent identities in the published Guth--Maynard
short-interval deduction to

\[
\theta_{\rm unif}(\eta)=1-\frac1{B_\eta}
=\frac{17-13\eta}{30-13\eta},
\]

and

\[
\theta_{\rm aa}(\eta)=1-\frac2{B_\eta}
=\frac{4-13\eta}{30-13\eta}.
\]

This document proves only the exact conditional propagation algebra. It does
not prove a density coefficient below \(30/13\), a new prime theorem, or the
uniformity of any hypothetical density input. The near-one and zero-free
inputs must remain available with the required logarithmic losses; a local
density gain that does not control the full explicit-formula supremum cannot
be inserted here.

## Exact improvements

For \(0<\eta<4/13\), both displayed endpoints remain positive and

\[
\frac{17}{30}-\theta_{\rm unif}(\eta)
=\frac{169\eta}{30(30-13\eta)},
\qquad
\frac{2}{15}-\theta_{\rm aa}(\eta)
=\frac{169\eta}{15(30-13\eta)}.
\]

Thus the almost-all endpoint moves by twice the uniform endpoint improvement
within this frozen algebra. These are endpoint conversions, not assertions
that the analytic hypotheses needed for either conclusion have been proved.

## Why these formulas are the right gates

The uniform explicit formula uses height \(T\asymp x/y\). A density bound
with coefficient \(B\) makes the zero contribution decay once
\(T^B<x\), equivalently \(\theta>1-1/B\) for \(y=x^\theta\). The frozen
almost-all second-moment calculation replaces this by \(T^B<X^2\), giving
\(\theta>1-2/B\). The G0 two-route reconstruction already checked the
remaining published hypotheses at \(B=30/13\); this result does not claim
they automatically persist for a new density theorem.

## Replay

```sh
python3 proof/build_cycle_5_conditional_short_interval_map_v1.py --check
python3 -m unittest tests.test_cycle_5_conditional_short_interval_map_v1 -v
```
