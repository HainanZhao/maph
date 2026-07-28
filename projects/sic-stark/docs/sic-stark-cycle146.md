# SIC--Stark research cycle 146': exact S--S evaluation audit

Date: 2026-07-28

## Source statement

The relevant result is not an unnamed general “state-integral
factorization.” It is the unnumbered theorem immediately preceding
equation (58) of Sarkissian--Spiridonov, together with their published
two-gamma degeneration, equation (66).

The main theorem assumes

\[
 \Re a_j>0,\qquad \Re\omega_1,\Re\omega_2>0,\qquad
 \sum a_j=\omega_1+\omega_2,\qquad
 \sum n_j=r-1.
\]

The paragraph after equation (58) states that the auxiliary chamber
restrictions used in its proof are lifted by analytic continuation.
Section 4 then takes the explicit limits (60)--(65) and obtains (66).

## Dimension-six specialization

\[
 (p,k,r,s)=(-115,24,5,24),\qquad
 pr+ks=1,
\]

\[
 \omega_1=24\beta_6-5=\beta_6^3,\qquad
 \omega_2=1,\qquad Q=\omega_1+\omega_2,
\]

\[
 g=Q,\qquad l=0,\qquad N\in\mathbb Z.
\]

The phase coefficient is

\[
 p-k(1-s)=437.
\]

Equation (66) becomes

\[
\begin{aligned}
&\int_{-i\infty}^{i\infty}
 \sum_{m=0}^{23}
 e^{\pi i m\,437(2N-4)/24}
 e^{\pi i\alpha(2y-Q)/(24\omega_1)}
 \Gamma_M(y,m)\Gamma_M(Q-y,-m)
 \frac{dy}{i\sqrt{\omega_1}}
\\
&\qquad =
24\,\Gamma_M(-\alpha,4-N)
     \Gamma_M(\alpha,N)
     \Gamma_M(Q,0).
\end{aligned}
\]

The fixed scalar is finite and nonzero: positivity excludes \(Q\)
from the pole lattice, and the possible zero equation
\(-115+24n=1\) has no integral solution.

The identity therefore applies as a meromorphic identity. The source
does not separately assert that the original vertical contour is
unpinched at \(g=Q\); that is retained for Cycle 148'.

## Explicit double-sine form

Let

\[
 \Delta(24,-115,m)=
 \{(\gamma,\delta):0\le\gamma,\delta<24,\;
 -115\gamma-\delta\equiv-115m\pmod {24}\},
\]

\[
 z_{\gamma,\delta}(\mu,m)
 =\frac{\mu+\omega_1\delta+\gamma}{24}.
\]

With

\[
 S_2^{\rm here}(z\mid\omega_1,1)
 =\gamma^{(2)}(z;\omega_1,1),
\]

S--S equations (15) and (29) give

\[
 \Gamma_M(\mu,m)
 =C_m(\mu)
  \prod_{\Delta(24,-115,m)}
  S_2^{\rm here}(z_{\gamma,\delta}(\mu,m)\mid\omega_1,1),
\]

where

\[
 C_m(\mu)=Z(m)\exp\left(
 -\frac{\pi i}{48}B_{2,2}(\mu)
 +\frac{\pi i}{2}\sum_{\Delta}B_{2,2}(z_{\gamma,\delta})
 \right).
\]

This gives the requested boundary evaluation entirely in the paper's
reciprocal-Kopp double-sine convention.

## Decisive relation-basis verdict

Reflection would pair

\[
 \Gamma_M(\alpha,N)
\quad\text{with}\quad
 \Gamma_M(Q-\alpha,4-N),
\]

not with the displayed \(\Gamma_M(-\alpha,4-N)\).
The unique continuous shift from \(-\alpha\) to \(Q-\alpha\) is
\(\omega_1+\omega_2\), but equations (38)--(39) change the discrete
label by \(r-1=4\), not by zero modulo \(24\). Hence no cancellation
occurs in the canonical reflection/shift basis.

The residue

\[
 \Gamma_M(-\alpha,4-N)\Gamma_M(\alpha,N)
\]

is genuinely oriented and irreducible by the standard norm relations.
Nevertheless, equation (66) is a new **integral-transform identity**,
not a new finite multiplicative relation among the AFK samples.
Therefore

\[
\boxed{\text{S--S (66) alone does not imply the TCC equation.}}
\]

Conservation of obstruction holds. The remaining operation is the
helical periodization and its arithmetic boundary specialization.

## Source

G. Sarkissian and V. P. Spiridonov, *General modular quantum
dilogarithm and beta integrals*, equations (57), (58), and (66),
<https://arxiv.org/abs/1910.11747>.
