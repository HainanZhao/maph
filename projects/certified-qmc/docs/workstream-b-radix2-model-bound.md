# Reference radix-two model bound

## Arithmetic model

Let \(u=2^{-53}\).  Every normal binary64 real operation is modeled as
\(\operatorname{fl}(x\circ y)=(x\circ y)(1+\delta)\),
\(|\delta|\le u\).  Overflow and harmful underflow are excluded.

The reference complex product uses four real multiplications and two
real additions.  Stored twiddles satisfy
\[
 |\widehat w-w|\le\tau,\qquad \tau=8u
\]
in the baseline model.  This covers both argument formation and the
stored sine/cosine values in the reference implementation. Sensitivity
runs use \(16u\).

## Local butterfly

For \(c=\operatorname{fl}_{\mathbb C}(\widehat w b)\), the two-term
dot-product bound gives
\[
 |c-wb|
 \le \mu |b|,\qquad
 \mu=\tau+\frac32\gamma_2(1+\tau),
 \quad
 \gamma_2=\frac{2u}{1-2u}.
\]
The rational \(3/2\) safely replaces \(\sqrt2\).

Rounding the final complex additions/subtractions yields
\[
 |\widehat{a\pm wb}-(a\pm wb)|
 \le \eta(|a|+|b|),
\quad
\eta=\mu+u(1+\mu).
\]

## Transform induction

After \(L\) radix-two-equivalent levels, induction on the butterfly
tree gives
\[
 \|\widehat{F x}-Fx\|_\infty
 \le \left((1+\eta)^L-1\right)\|x\|_1.
\]
For a radix-two transform of length \(N=2^m\), \(L=m\).  A radix-four
pipeline is admitted only with a declared radix-two-equivalent depth
at least \(m\).  A normalized inverse divides the right side by \(N\);
for power-of-two \(N\), that scaling is exact for normal results.

All constants in the executable certificate are rational.  Arb is used
only to validate the reference transform and its stored twiddles against
the exact DFT, not to define the theorem.

## Model-class boundary

This proves the transform component for pipelines satisfying the local
butterfly and depth assumptions.  It does not claim that an unknown
historical implementation used this operation graph.  Workstream B
therefore reports conclusions explicitly as “under model class
\(\mathcal M\)” and logs doubled-twiddle and doubled-depth sensitivity
variants.

Implementation: `src/radix2_model.py`.
