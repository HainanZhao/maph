# SIC--Stark research cycle 144': honest two-base lens packet

Date: 2026-07-28

## Gate verdict

\[
\boxed{\text{two-base interior packet `ENCLOSED`}}
\]

The retired equal-base \( {}_2\psi_2\) is not used as an interior
function.

## Two different modular pairs

For

\[
 A_6=\begin{pmatrix}115&-24\\24&-5\end{pmatrix},
\]

Sarkissian--Spiridonov equations (5)--(8) define

\[
 q_M=e^{2\pi i\tau},\qquad
 \widetilde q_M=e^{2\pi iA_6\tau}.
\]

Their equation (15) factors the same general modular dilogarithm into
standard Faddeev factors. Those factors use equation (14):

\[
 q_S=e^{2\pi i\rho},\qquad
 \widetilde q_S=e^{-2\pi i/\rho}.
\]

Consequently,

\[
 \widetilde q_S=q_S
 \iff \rho+\rho^{-1}\in\mathbb Z.
\]

At

\[
 \beta_6=\frac{5+\sqrt{21}}2,
\qquad
 \beta_6+\beta_6^{-1}=5,
\]

the standard pair fuses. The lens pair also fuses because
\(A_6\beta_6=\beta_6\). Off the boundary these are different
transformations and must retain separate notation.

For the dimension-six lens specialization

\[
 (p,k,r,s)=(-115,24,5,24),\qquad
 \rho=\frac{\omega_1}{\omega_2}=24\tau-5.
\]

Thus the standard factorization and the general-lens product give two
independent interior realizations of the same analytic continuation.

## Bibasic helical packet

For a finite frequency \((p_a,p_b)\), put

\[
 \alpha_z
 =\frac{4\tau-1}{3}(4p_b-5p_a)+2(4\tau-1)z,
\qquad
 N_z=p_a+2-6z.
\]

The three residue classes \(z\bmod3\) are bilateral orbits under

\[
 (\alpha,N)\longmapsto
 (\alpha+\omega_1-\omega_2,N+6).
\]

Writing

\[
 X=e^{2\pi i(\mu+m)/24},\qquad
 A=\widetilde q_M
 e^{2\pi i(\mu+115m\omega_1)/(24\omega_1)},
\]

the exact functional equations give the kernel-term ratio

\[
 \frac{K(z+3)}{K(z)}
 =
 \frac{1-X_1}{1-A_1}
 \,\frac{1-A_2/\widetilde q_M}{1-X_2/q_M}.
\]

This is the honest bibasic object. Both bases occur independently.

## Formal fusion

At \(\tau=\beta_6\), the RM identities and the descent condition give

\[
 X_1=x,\quad A_1=-qx,\quad
 X_2=wx^{-1},\quad A_2=qw^4x^{-1}.
\]

Since \(w^3=-1\), the bibasic ratio becomes

\[
 -q\,
 \frac{(1-x)(1+w^{-1}x)}
 {(1+qx)(1-qw^{-1}x)}.
\]

This is exactly the term ratio of

\[
 {}_2\psi_2(x,w^2x;-qw^2x,-qx;q,-q).
\]

It proves formal recovery of the retired series at fusion without
using that series in the upper half-plane.

## Arb audit

At the three rationally parametrized \(A_6\)-axis points
\(t=20,10,5\):

- all four bases \(q_M,\widetilde q_M,q_S,\widetilde q_S\) lie strictly
  inside the unit disk;
- the direct two-base definition in equations (5)--(8) agrees with the
  24-factor continuation in equation (15);
- all three bibasic residue-class sums have rigorous geometric tails.

The enclosure counts are

\[
 \text{direct/factorized}=3/3,\qquad
 \text{alias classes}=9/9.
\]

The slowest direct/factorized comparison still contains zero with
coordinate radii below \(4.4\cdot10^{-12}\) at 30 working digits.

## Source and reproducibility

The source is G. Sarkissian and V. P. Spiridonov, *General modular
quantum dilogarithm and beta integrals*, equations (5)--(8), (14), and
(15), <https://arxiv.org/abs/1910.11747>.

```bash
PYTHONPATH=scripts python \
  scripts/dimension_six_two_base_lens.py \
  --digits 30 --tolerance 1e-14

SIC_STARK_RUN_ARB=1 PYTHONPATH=scripts python -m unittest \
  tests.test_dimension_six_two_base_lens -v
```
