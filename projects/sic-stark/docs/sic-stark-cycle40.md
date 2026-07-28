# SIC--Stark research cycle 40: what the cyclic limit actually proves

Date: 2026-07-27

## Outcome

The cyclic-quantum-dilogarithm route gives a convention-correct analytic
approximation to \(x_{\mathrm{an}}^{-1}\), but it does not currently prove

\[
 x_{\mathrm{an}}=x_{\mathrm{alg}}.
\]

The distinction between two results is important:

1. Yalkinoglu's \(q\)-Pochhammer expression is proved in the 2024 paper
   and has since appeared in journal form.
2. The root-of-unity cyclic-dilogarithm replacement is still presented as
   an announcement whose complete proof is deferred.

No subsequent full proof was located as of 27 July 2026.

## Exact specialization

For

\[
 \beta=\frac{5+\sqrt{21}}2,\qquad
 T_0=2,\quad T_1=5,\quad T_{n+1}=5T_n-T_{n-1},
\]

put \(t_n=T_{n-1}/T_n\).  The matrix

\[
 U=\begin{pmatrix}5&-1\\1&0\end{pmatrix}
\]

satisfies

\[
 U\cdot t_n=t_{n-1},\qquad U^3\cdot t_{n+3}=t_n.
\]

Since the order of \(\beta\) modulo \((6)\) is three, the announced
cyclic formula specializes to

\[
 X_1((6))
 =
 \lim_{n\to\infty}
 \left|
 \frac{D_{t_n}(1/6)}
      {D_{t_{n+3}}(1/6)}
 \right|
 =x_{\mathrm{an}}^{-1}.
\]

The executable approximants converge to

\[
 0.451898706617609\ldots=x_{\mathrm{alg}}^{-1}
\]

to the tested accuracy.

## Why this is not the algebraicity proof

The proven \(q\)-Pochhammer formula and the announced cyclic formula are
representations of the already-defined analytic Shintani invariant.  A
limit of algebraic numbers in growing cyclotomic/Kummer fields need not be
algebraic.  To identify the limit with \(x_{\mathrm{alg}}\), one still
needs either:

- an exact finite-level relation stable under the limit;
- an independent algebraicity theorem with a usable degree and height
  bound; or
- a new special-value evaluation.

The cyclic pentagon relations do not immediately provide the first
option.  At level six, the characteristic formulas encounter zero cyclic
factors, and cycle 33 proved that the naive full-characteristic
substitution produces nonintegral boundary orders.

## Sources

- B. Yalkinoglu, *A note on Shintani's invariants*,
  <https://arxiv.org/abs/2408.07309>.
- B. Yalkinoglu, *Shintani's invariant via cyclic quantum
  dilogarithm*, Theorems 3.1--3.2,
  <https://arxiv.org/abs/2508.18320>.
