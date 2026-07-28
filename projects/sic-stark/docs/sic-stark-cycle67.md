# SIC--Stark research cycle 67: a simple-zero target for the TCC defect

## Exact geodesic scale

For every rational point \(m_k/n_k\) used in the dimension-six
regularization,

\[
 m_k^2-5m_kn_k+n_k^2=-21.
\]

Writing

\[
 \beta'=\frac{5-\sqrt{21}}2,
\]

gives the exact identity

\[
 \left(\frac{m_k}{n_k}-\beta'\right)
 \left(\frac{m_k}{n_k}-\beta\right)
 =-\frac{21}{n_k^2}.
\]

Thus

\[
 \frac{m_k}{n_k}-\beta'
 \sim\frac{\sqrt{21}}{n_k^2}.
\]

This explains why the corrected defect has the scale \(n_k^{-2}\).

## The derivative packet

Let

\[
 R_k(p)=\sqrt7\,
 \operatorname{Tr}\!\left(D_p^*(K_k^2-K_k)\right).
\]

The normalized arrays

\[
 \frac{R_k(p)}{m_k/n_k-\beta'}
\]

converge numerically to a finite nonzero derivative packet.  The maximum
differences between consecutive normalized packets are

\[
 383.9,\qquad17.90,\qquad0.7935.
\]

At the same time their maximum norms stabilize near \(5161\).
This is strong evidence that every defect coefficient has an ordinary
simple zero at \(\beta'\), rather than a fractional-power or Stokes
singularity.

## Revised analytic target

The narrowest remaining lemma is no longer a global cyclic estimate.
For the thirteen signed Zauner representatives, define the
convention-correct rational-boundary continuation \(R_p(\tau)\).  Prove

\[
 R_p(\tau)
 =
 (\tau-\beta')H_p(\tau)
\]

on a one-sided neighborhood of \(\beta'\), with \(H_p\) bounded there.
Then \(R_p(\beta')=0\), which is exactly the TCC conclusion.

The \(q\)-gamma calculation handles the only possible singular residue.
The remaining work is to control the logarithm branches in the
nonsingular half-power product and show that the constant term of each
of the thirteen defects cancels.

## Pentagon audit

The standard cyclic pentagon identity does not make the finite matrices
idempotent: their defects are small but nonzero.  Its root of unity has
order \(n_k\), whereas TCC uses the level-six Weyl phase (and its
order-twelve even-dimensional lift).  A pentagon argument would
therefore have to operate in the combined \(6n_k\) root system and
extract only its constant term.

This remains a possible proof mechanism, but the observed simple-zero
structure makes direct local factorization the more economical next
attack.

Relevant root-of-unity identities are developed by Ip and Yamazaki,
*Quantum Dilogarithm Identities at Root of Unity*,
<https://arxiv.org/abs/1412.5777>.  Their mutation-period hypotheses do
not directly identify the present level-six convolution.
