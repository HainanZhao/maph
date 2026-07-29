# Cycle 002 — signed scaled-integer bounds

Date: 2026-07-29

For \(\gamma_j=a_j/b_j\) in lowest terms, define

\[
C_j=6b_jN^2,\qquad
F_j(r)=6b_jN^2+a_j(6r^2-6rN+N^2).
\]

Then the frozen kernel factor is exactly \(F_j/C_j\), and

\[
e_s^2={E_s\over D_s},\quad
E_s=\sum_{k=0}^{N-1}\prod_{j=1}^sF_j(kz_j)-N\prod_{j=1}^sC_j,
\quad
D_s=N\prod_{j=1}^sC_j.
\]

This representation uses integers throughout; reducing \(E_s/D_s\)
recovers the Phase-0 fraction oracle.

For nonnegative weights,
\(|F_j|\le M_j=N^2(6b_j+a_j)\), hence

\[
|E_s|\le N\left(\prod_jM_j+\prod_jC_j\right).
\]

At a CBC branch, the constant term cancels.  The exact range of the
fixed \(B_2\) numerator is \(3N^2/2\) for even \(N\), and
\(3(N^2-1)/2\) for odd \(N\).  Therefore

\[
|E(u)-E(v)|\le
N\,a_s\,\operatorname{span}_{B_2}(N)\prod_{j<s}M_j.
\]

A balanced CRT reconstruction is unique once the modulus product is
strictly larger than twice the relevant bound.  Exhaustive small
regressions verify the exact span, the fraction identity, candidate
differences, and both inequalities.

Decision: **CONTINUE**.  The reconstruction target and its bit budget
are now proved rather than projected.

Tag: `VERIFIED`.
