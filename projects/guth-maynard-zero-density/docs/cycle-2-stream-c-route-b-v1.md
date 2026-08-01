# Cycle 2 — Stream C Route B short-interval audit

Claim boundary: the exact transfer calculations below are conditional on two
external inputs that remain `OBSERVED`, not `PROVED`: a near-one density bound
with the stated logarithmic uniformity, and the local zero-counting estimate
in the almost-all second moment. This document therefore does **not** promote
either Guth--Maynard short-interval corollary as independently re-proved.

## Source freeze and blockers

The source ledger is
[cycle-2-stream-c-source-ledger-v1.json](../artifacts/cycle-2-stream-c-source-ledger-v1.json).

`PROVED`: Guth--Maynard's frozen TeX source gives the truncated explicit
formula and the displayed uniform/almost-all deductions at lines 2407–2471.

`PROVED` (scoped): Ford's Theorem 5 gives a directly checked
Vinogradov--Korobov region for \(|t|\geq3\), with explicit constant \(57.54\).
It yields the required asymptotic cutoff shape, but its scope does not itself
close the low-height portion of the all-ordinate count \(N(\sigma,T)\).

`OBSERVED` blockers retained:

- Jutila's 1977 near-one density source was downloaded and hashed but is
  scan-only; its exact theorem and conventions were not read.
- The available Huxley alternative is likewise scan-only.
- The second-moment unit-strip zero count and reciprocal-distance estimate are
  asserted by Guth--Maynard but are not tied there to a uniquely checked
  external source.

## Uniform replay, conditional on the density/cutoff inputs

Set (b=30/13), (E(z)=\exp((\log z)^{1/4})), and take the nonvacuous
range (0<\epsilon<127/300):
\[
x^{17/30+\epsilon}\leq y\leq x^{99/100},\qquad
T=xy^{-1}E(x)^2.
\]
The truncated explicit formula has error
\(x(\log x)^3/T=y(\log x)^3E(x)^{-2}=O(yE(x)^{-1})\). Its zero sum is
bounded by
\[
y\log x\sup_\sigma x^{\sigma-1}N(\sigma,T).
\]

The epsilon bookkeeping is exact at power scale:
\[
T\leq x^{13/30-\epsilon}E(x)^2
\leq x^{13/30-\epsilon/2}=x^{1/b-\epsilon/2}
\]
once (2(\log x)^{1/4}\leq(\epsilon/2)\log x). If the density exponent's
(o(1)) coefficient is bounded by \(\eta\leq b^2\epsilon/4\), then
\[
(b+\eta)(1/b-\epsilon/2)-1\leq-b\epsilon/4.
\]
Thus the base in the density supremum is a negative fixed power of (x).

Ford's checked region has width
\((\log T)^{-2/3}(\log\log T)^{-1/3}\); asymptotically it contains a
cutoff of width (c(\log T)^{-5/7}), since (5/7-2/3=1/21>0). The latter
turns the negative fixed power into
\(\exp(-c'(\log x)^{2/7})\), which absorbs log powers and dominates
\(E(x)^{-1}\). The upper range ensures both (T\to\infty) and (T\leq x),
while prime-power and local partial-summation errors are negligible because
(17/30>1/2) and (y/x\leq x^{-1/100}).

Conditional conclusion:
\[
\pi(x+y)-\pi(x)=\frac y{\log x}+O(yE(x)^{-1}).
\]

## Almost-all replay, conditional on the pair/count input

Put
\[
\delta=X^{-13/15+\epsilon/2},\qquad T=\delta^{-1}E(X)^4.
\]
Then (\delta X=X^{2/15+\epsilon/2}\leq y), with spare exponent
\(\epsilon/2), and after subpower absorption
\[
T\leq X^{13/15-\epsilon/3}=X^{2/b-\epsilon/3}.
\]
With \(\eta\leq b^2\epsilon/12\),
\[
(b+\eta)(2/b-\epsilon/3)-2\leq-b\epsilon/6.
\]
The same cutoff argument gives the stronger decay needed to make
\[
I\ll\delta^2X^3E(X)^{-3}.
\]

The split interval inequality then gives a long-interval second moment at
most (y^2XE(X)^{-3}), plus \(O(\delta^2X^3)\). The latter divided by
\(y^2X\) is at most (X^{-\epsilon}\), hence is also absorbed. Chebyshev
at threshold (yE(X)^{-1}) leaves (O(XE(X)^{-1})) exceptional starts.
The deterministic prime-power and partial-summation conversion uses the same
frozen lower/upper ranges as in the uniform branch.

Conditional conclusion:
\[
\pi(x+y)-\pi(x)=\frac y{\log x}+O(yE(X)^{-1})
\]
outside (O(XE(X)^{-1})) starts in ([X,2X]\cap\mathbb Z).

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_short_intervals_stream_c_route_b_v1.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-route-b-v1.json
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The first command is an exact arithmetic replay only; it intentionally fails
to claim analytic G0 completion while the listed source blockers remain.
