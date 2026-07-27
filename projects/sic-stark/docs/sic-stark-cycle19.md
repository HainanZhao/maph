# SIC--Stark research cycle 19: the dimension-four common factor

Date: 2026-07-27

## Outcome

The first bounded four-point experiment produced a genuine
factorization in dimension four.

The symmetrized principal-ghost algorithm in `Zauner.jl` evaluates the
dimension-four double-sine table in terms of one positive unit \(x\).
After retaining the exceptional zero characteristic, every entry lies
in

\[
\{\sqrt5,\ \pm1,\ \pm x,\ \pm x^{-1}\}.
\]

Set

\[
t=\sqrt{3+\sqrt5}
=\frac{\sqrt2+\sqrt{10}}2.
\]

An exact calculation in

\[
\mathbb Q(\sqrt2,\sqrt5)[x,x^{-1}]
\]

shows that all \(36\) two-by-two minors of the dimension-four ghost
matrix lie in the principal ideal

\[
\boxed{(x^2-tx+1).}
\]

Equivalently, the single special-value identity

\[
\boxed{x+x^{-1}=\sqrt{3+\sqrt5}}
\]

implies every dimension-four minor and hence dimension-four TCC.

This is the first cycle in the four-point phase to find a common
RM-specific factor rather than another generic rank reformulation.
The remaining factor is one scalar double-sine evaluation.

## 1. The signed double-sine table

Let

\[
\beta=\frac{3+\sqrt5}{2}.
\]

Using the principal form \(Q_4=\langle1,-3,1\rangle\), the published
symmetrized triple-double-sine algorithm gives the following normalized
real table before the displacement chirp:

\[
\begin{pmatrix}
\sqrt5&-x&1&-x^{-1}\\
-x^{-1}&-x^{-1}&-x^{-1}&-x\\
1&-x^{-1}&1&x\\
-x&-x^{-1}&x&-x
\end{pmatrix}.
\]

The top-left value is exceptional.  Substituting the ordinary
triple-double-sine formula there would give the wrong normalization;
the algorithm explicitly replaces it by \(\sqrt{d+1}=\sqrt5\).

With

\[
\tau=-e^{\pi i/4},
\]

the ghost Weyl coefficients are the table entries divided by
\(\sqrt5\), with the prescribed displacement chirp.  The resulting
matrix entries belong to the displayed Laurent field.

## 2. Exact minor reduction

Before imposing a relation on \(x\), 34 of the 36 minors are nonzero
Laurent polynomials; two vanish structurally.  Reduce powers using

\[
x^{-1}=t-x,\qquad
x^{-2}=t^2-1-tx,\qquad
x^2=tx-1.
\]

Every minor then has a unique remainder \(A+Bx\), with

\[
A,B\in\mathbb Q(\sqrt2,\sqrt5).
\]

The exact executable calculation gives

\[
A=B=0
\]

for all 36 minors.  Thus no cancellation between different minors or
Zauner sectors is involved: the same scalar quadratic kills each
minor separately.

The calculation also caught an important radical simplification:

\[
\sqrt{3+\sqrt5}
=\frac{\sqrt2+\sqrt{10}}2.
\]

Treating the left side as an independent quadratic generator leaves
spurious nonzero symbolic remainders; selecting the correct positive
embedding removes them exactly.

## 3. Numerical double-sine audit

For the positive table unit,

\[
\begin{aligned}
x={}&
S_2\left(1+\frac{\beta}{4}\mid\beta,1\right)
S_2\left(\frac14\mid\beta,1\right)\\
&\times
S_2\left(1+\frac{3\beta-1}{4}\mid\beta,1\right).
\end{aligned}
\]

A standalone standard-library quadrature reproduces

\[
x=1.700015776309454\ldots
\]

and

\[
x+x^{-1}
=2.288245611547154\ldots,
\]

while

\[
\sqrt{3+\sqrt5}
=2.288245611270737\ldots.
\]

The \(2.8\times10^{-10}\) difference is consistent with the deliberately
simple fixed-grid quadrature.  This numerical computation discovered
and checks the identity; it is not its analytic proof.

## 4. Reduced analytic target

The double-sine shift and reflection laws simplify \(x\) to

\[
x
=\sqrt2\,
\frac{
S_2(\beta/4\mid\beta,1)
S_2(1/4\mid\beta,1)}
{S_2((\beta+1)/4\mid\beta,1)}.
\]

Therefore the remaining dimension-four problem is a quarter-period
double-sine identity:

\[
\sqrt2\,
\frac{
S_2(\beta/4)S_2(1/4)}
{S_2((\beta+1)/4)}
+
\frac1{\sqrt2}\,
\frac{
S_2((\beta+1)/4)}
{S_2(\beta/4)S_2(1/4)}
=\sqrt{3+\sqrt5}.
\]

Standard shift and reflection formulas alone do not evaluate this
quarter-period quotient.  An explicit modulus-four Shintani ray-class
evaluation, together with the cocycle square-root relation, is the
appropriate next tool.

## 5. Claim ledger

Proved exactly in this cycle:

- the signed one-unit form of the dimension-four table, conditional on
  the published principal-ghost algorithm;
- divisibility of every ghost minor by
  \(x^2-\sqrt{3+\sqrt5}x+1\);
- equivalence of that one unit relation to all dimension-four minor
  equations;
- reduction of the remaining unit to a quarter-period double-sine
  quotient.

Numerically checked:

- the double-sine unit satisfies the predicted reciprocal trace to
  approximately \(3\times10^{-10}\) using independent
  standard-library quadrature.

Still open:

- a direct analytic proof of the quarter-period special value;
- the corresponding common-factor mechanism in higher dimensions;
- general TCC.

## Sources

- S. Flammia et al., `Zauner.jl`, principal-ghost and double-sine
  implementations, [GitHub](https://github.com/sflammia/Zauner.jl).
- N. Kurokawa and M. Wakayama, *Algebraicity and transcendency of
  basic special values of Shintani's double sine functions*,
  [DOI:10.1017/S0013091504001579](https://doi.org/10.1017/S0013091504001579).
- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
