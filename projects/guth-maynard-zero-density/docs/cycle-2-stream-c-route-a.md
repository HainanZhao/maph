# Cycle 2, Stream C, Route A: short-interval replay

## Outcome and claim boundary

`OBSERVED`: Route A exactly reproduces the power thresholds, epsilon margins,
truncation choices, VK absorption, second-moment scale, and Chebyshev
conversion in Guth--Maynard §13.2.  It does **not** independently prove either
short-interval corollary: the truncated explicit formula, a uniform near-one
density input, and the local zero/pair-count input remain indirect.  The
result is therefore a conditional full replay, not a G0 analytic pass.

No new density estimate, prime-gap result, or short-interval exponent is
claimed.

## Frozen inputs inspected

- Guth--Maynard arXiv:2405.20552v2 §13.2, TeX SHA-256
  `36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
- Jutila, *Zero-density estimates for L-functions*, *Acta Arithmetica* XXXII
  (1977), accessible scan SHA-256
  `cbe2d1e7115717cf28f9ffaffdc1fe232958595b17c5c2ee59fc968e8ff0d5a1`.
  Printed p. 57, Corollary (1.8), was visually inspected.
- Ford, *Zero-free regions for the Riemann zeta function* (2002), PDF
  SHA-256 `a43a2c37cf0f34b05bf80d9e58bcef176371437eedf7aae17d72f2c55b04c948`.
  Theorem 5 supplies a reachable VK-shaped zero-free region.

Put \(b=30/13\).  The exact identities are

\[
\frac1b=\frac{13}{30},\qquad \frac2b=\frac{13}{15},\qquad
1-\frac1b=\frac{17}{30},\qquad 1-\frac2b=\frac2{15}.
\]

## Uniform intervals

GM use the displayed truncated explicit formula with

\[
T=\frac{x}{y}\exp(2(\log x)^{1/4}).
\]

For \(y\ge x^{17/30+\epsilon}\), exact power bookkeeping gives, for large
\(x\),

\[
T<x^{13/30-\epsilon/2}=x^{1/b-\epsilon/2}.
\]

The displayed truncation error is
\(x(\log x)^3/T\), which is at most
\(y\exp(- (\log x)^{1/4})\) eventually.  The upper range
\(y\le x^{0.99}\) ensures \(2\le T\le x\) and \(\log T\asymp\log x\).

Conditional on the near-one density input asserted by GM,

\[
N(\sigma,T)\ll T^{(b+o(1))(1-\sigma)}(\log T)^{O(1)},
\]

and the VK cutoff, the source's supremum becomes

\[
x^{\sigma-1}N(\sigma,T)
\ll (\log T)^{O(1)}
\left(\frac{T^{b+o(1)}}x\right)^{1-\sigma}.
\]

Ford's Theorem 5 gives the stronger zero-free scale
\((\log T)^{-2/3}(\log\log T)^{-1/3}\).  It contains GM's weaker
\((\log T)^{-5/7}\) cutoff because
\((\log T)^{1/21}/(\log\log T)^{1/3}\to\infty\).  The resulting negative
power is \(\exp(-c_\epsilon(\log x)^{2/7})\), stronger than the required
\(\exp(- (\log x)^{1/4})\).

The zero sum is reduced to this supremum by
\[
\left|\frac{(x+y)^\rho-x^\rho}{\rho}\right|
 =\left|\int_x^{x+y}t^{\rho-1}\,dt\right|
 \ll yx^{\Re\rho-1}.
\]
Grouping real parts at spacing \(1/\log x\) costs the explicit \(\log x\)
factor in GM.  This factor is dominated by the VK-powered decay above.

`OBSERVED` blocker: the locally accessible Jutila corollary gives an
\(\epsilon\)-power near-one estimate (with exponent 2 for
\(\alpha\ge11/14\)); it does not directly provide the uniform
logarithmic-loss form throughout a VK strip whose width shrinks with \(T\).
Its inspected display also does not explicitly state multiplicity.  GM's
alternative Montgomery citation is not pinned.  The explicit-formula source
(Davenport, Chapter 17) is likewise unpinned.

## Almost-all intervals

Freeze

\[
\delta=X^{-13/15+\epsilon/2},\qquad
T=\delta^{-1}\exp(4(\log X)^{1/4}).
\]

Then \(\delta X=X^{2/15+\epsilon/2}\), and

\[
T\le X^{13/15-\epsilon/3}=X^{2/b-\epsilon/3}
\]

for large \(X\).  Thus the same conditional density/VK calculation gives

\[
\sup_\sigma X^{2\sigma+1}N(\sigma,T)
\ll X^3\exp(-10(\log X)^{1/4}).
\]

The exact second-moment reduction in GM has a remainder \(O(\delta^2X^3)\).
It is harmless at the claimed lower range because

\[
\frac{\delta^2X^3}{y^2X}=\left(\frac{\delta X}{y}\right)^2\le X^{-\epsilon}
\le \exp(-3(\log X)^{1/4})
\]

eventually.  Conditional on the local zero/pair estimate, expansion of the
zero sum yields the required L2 bound
\(\ll y^2X\exp(-3(\log X)^{1/4})\).  Chebyshev at threshold
\(y\exp(- (\log X)^{1/4})\) then leaves at most
\(O(X\exp(- (\log X)^{1/4}))\) exceptional starting points.

`OBSERVED` blocker: GM's pair-kernel bound uses an \(O(\log T)\) local zero
count.  Given that count, summing the positive-real-part kernel over unit
height strips gives the claimed \((\log T)^2\) bound.  The local count has
not yet been pinned with its multiplicity convention, so this transfer is
not promoted.

More explicitly, \(|((1+\delta)^\rho-1)/\rho|\ll\delta\) for the zero
range in the source.  After expansion,
\[
\left|\int_X^{3X}x^{\rho_1+\overline{\rho_2}}\,dx\right|
\ll \frac{X^{\Re\rho_1+\Re\rho_2+1}}
{|1+\rho_1+\overline{\rho_2}|}.
\]
Use \(X^{\beta_1+\beta_2+1}\le X^{2\beta_1+1}+X^{2\beta_2+1}\), then
the conditional pair-kernel bound, to obtain GM's
\[\delta^2(\log X)^3\sup_\sigma X^{2\sigma+1}N(\sigma,T).\]
This supplies the stated L2 target once the conditional density supremum is
inserted.

## Retained blockers and falsifiers

1. A pinned explicit formula must match the height, endpoint, multiplicity,
   and truncation-error conventions used by GM.
2. A single near-one density theorem must yield a uniform logarithmic-loss
   estimate in the shrinking VK strip; Jutila's visible \(\epsilon\)-power
   display alone is insufficient.
3. A primary local zero-count theorem must support the separated-set and
   pair-kernel losses with multiplicity.

Any failure of these conditions invalidates the affected analytic branch;
the exact \(17/30\) and \(2/15\) arithmetic does not repair it.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_route_a.py -v
```

The first command checks all frozen local source hashes and GM §13.2
declarations, then writes `artifacts/cycle-2-stream-c-route-a-v1.json` with
its own canonical audit hash, script hash, tool version, and timing.
