# SIC--Stark research cycle 66: the missing characteristic half-power

## Outcome

The generic nonsingular residue formula in cycle 63 was still too
compressed.  It retained only the cyclic-dilogarithm term

\[
 -\frac1n\log D_\zeta(w),
\]

which is valid when \(w\) is held fixed during the radial limit.  For a
level-six characteristic,

\[
 w=e(r_2\tau-r_1)
\]

moves with \(\tau\).  After residue-class factorization, its \(j\)-th
factor is

\[
 (z_jQ^{\alpha_j};Q)_\infty,\qquad
 \alpha_j=\frac{r_2+j}{n}.
\]

Euler--Maclaurin therefore contributes the indispensable constant

\[
 \left(\frac12-\alpha_j\right)\log(1-z_j)
\]

for every nonsingular residue.  The complete nonsingular boundary
constant is

\[
 \boxed{
 \sum_{j=0}^{n-1}
 \left(\frac12-\frac{r_2+j}{n}\right)
 \log(1-w_0\zeta^j).
 }
\]

At a singular residue this formula is replaced by the \(q\)-gamma term
already derived in cycle 63.

## Why the omission was initially hidden

At the symmetric test \(1/4\mapsto19/4\), the omitted factors cancel
between numerator and denominator.  Thus that test validated the
curvature phase but could not distinguish the two nonsingular formulas.

The first small point on the actual period-three geodesic,

\[
 \frac5{23}\longmapsto\frac{23}{5},
\]

does distinguish them.  For characteristic \((0,1)/6\) and radial
parameter \(t=0.4\):

\[
\begin{array}{c|c}
\text{boundary formula}&
|\text{direct product}/\text{formula}-1|\\ \hline
\text{complete half-power}&5.56\cdot10^{-3}\\
\text{cyclic term alone}&>2\cdot10^{-2}.
\end{array}
\]

The complete error continues to zero with \(t\), as required.

## Consequence

This correction changes the observed geodesic convergence from
\(O(n^{-1})\) to \(O(n^{-2})\), matching the continued-fraction distance
to the RM fixed point.  It also reduces the fourth-step matrix
idempotency defect from \(4.34\cdot10^{-4}\) to
\(1.94\cdot10^{-6}\).

The corrected formula is now used by
`scripts/dimension_six_qgamma_boundary.py`.
