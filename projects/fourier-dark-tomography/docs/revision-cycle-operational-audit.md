# Operational-audit revision cycle

Date: 26 July 2026

## Trigger

The arbitrary-mode theorem solved the original \(F_4\)-generality problem,
but a hostile operational review identified six remaining weaknesses:

1. an artificially narrow comparator set;
2. conflation of dimension saturation with sample efficiency;
3. phase-only rather than full coefficient-SPAM analysis;
4. identifiability without an explicit estimator;
5. overemphasis on outcome-bin minimality;
6. an unidentified reproducibility package.

## Literature correction

The manuscript now compares against:

- standard-laser and intensity-only transfer-matrix reconstruction;
- one-/two-photon reconstruction;
- mode-mismatch-corrected procedures;
- PhaseLift reconstruction;
- loss- and phase-instability-aware multimode characterization;
- recent single-photon, loss- and indistinguishability-aware tomography.

The dark-event construction is no longer positioned as a replacement for
these methods. Its proposed niche is a fixed-setting residual diagnostic at
a known Fourier operating point, especially when the device is already
being exercised with multiphoton inputs and number-resolved detection.

## New proposition: complete coefficient-SPAM confounding

For

\[
|\Psi_\eta\rangle=\frac1{\sqrt m}
\sum_j(1+\eta_j)|ne_j\rangle,
\]

the first-order leakage in charge sector \(c\) is

\[
\delta A_s=\alpha_s\widehat\eta_c,\qquad
\widehat\eta_c=\frac1m\sum_j\eta_j\omega^{jc}.
\]

This is constant over the selected outcomes \(s_{p,c}\). The device block

\[
i\alpha[(n-1)z_p+z_{p+c}]
\]

reproduces it by taking \(z_p\) constant. The antipodal block reproduces
both quadratures through gains \(n\) and \(n-2\). Therefore unknown cat
amplitudes, not only phases, are exactly confounded with device errors on
the selected data.

For real relative amplitude errors the nuisance image has rank \(m-1\);
the same is true for relative phase errors. Their combined image has rank
\(m-1\) for odd \(m\) and \(m\) for even \(m\). At \(m=4\), the two
individual ranks are three and their union has rank four. An exact
Gaussian-integer regression test certifies the \(m=4\) statement.

## New statistical scaling theorem

Normalize both dense probes by \(m-1\), giving spectral norm at most one.
For the background-free selected-Poisson model, define

\[
C_c=\sum_{k=0}^{m-1}
|n-1+e^{2\pi i ck/m}|^{-2}.
\]

The A-optimal allocation is explicit. If \(A_R,A_T\) are the inverse-Gram
trace coefficients, then

\[
w_R=\frac{\sqrt{A_R}}{\sqrt{A_R}+\sqrt{A_T}},\qquad
w_T=1-w_R,
\]

and

\[
\min\operatorname{Tr}\operatorname{Cov}(\hat\theta)
=\frac{(\sqrt{A_R}+\sqrt{A_T})^2}{4N\alpha^2}.
\]

At \(n=m\):

\[
\overline{\operatorname{Var}}=\Theta(m^{m-4}/N).
\]

The weakest reference probability is
\(\Theta(\epsilon^2m^{2-m})\), so obtaining a constant expected number of
counts in every sign bin needs

\[
N=\Omega(\epsilon^{-2}m^{m-2}).
\]

With fixed additive background \(b\) dominating the selected bins:

\[
\overline{\operatorname{Var}}
=\Theta\!\left(\frac{b\,m^{2m-6}}{N\epsilon^2}\right).
\]

This establishes that dimension saturation is algebraic, not statistical
scalability.

## Explicit estimator and Monte Carlo

The revised paper uses calibrated weighted local least squares,

\[
\hat\theta=(J_\epsilon^T\Sigma^{-1}J_\epsilon)^{-1}
J_\epsilon^T\Sigma^{-1}\hat r.
\]

For the sparse \(F_4\) design with
\(\epsilon=0.05\), \(N=2\times10^6\), background \(10^{-5}\), and all
twelve coordinates nonzero with norm \(0.002\):

- A-optimal \(H_X\)-pair allocation for signed contrasts: \(0.516351\);
- predicted RMS vector error: \(0.00290022\);
- empirical RMS over 5000 repetitions: \(0.00290334\);
- bias norm: \(4.93\times10^{-5}\);
- nominal 95% ellipsoid coverage: \(0.9544\).

This validates the estimator under its stated ideal count model only.
A deterministic scan over 128 simultaneous-error directions gives worst
relative linear-inversion bias \(0.9\%\), \(3.4\%\), and \(9.1\%\) at
coordinate-vector radii \(10^{-3}\), \(3\times10^{-3}\), and \(10^{-2}\).
This is an empirical \(F_4\) radius diagnostic, not a uniform theorem.

## Revised claim boundary

The strongest experimental resource statement is now four programmed
settings independent of \(m\). Outcome minimality is retained only as a
mathematical consequence of the two-row event bound. The paper explicitly
states that bins are collected in parallel and that overcomplete designs
may be statistically superior.

## Statistical-consistency review

A subsequent audit found that the reported \(H_X\)-pair allocation optimized
the Fisher information of the separate raw sign counts, while the declared
estimator first compresses those counts into signed contrasts. Re-optimizing
the actual contrast covariance gives

\[
w_X=0.5163513,\qquad
\sqrt{\operatorname{Tr}\operatorname{Cov}}=0.002900218
\]

at \(\epsilon=0.05\), \(N=2\times10^6\), and \(b=10^{-5}\). A 5000-run
simulation gives vector RMSE \(0.00290334\) and 95.44% nominal-ellipsoid
coverage. The implementation and a numerical regression test now certify
these values.

The statistical model now makes four further assumptions explicit:

- probe-only baselines are pre-calibrated and treated as exact; finite
  baseline shots would add covariance and acquisition cost;
- background scaling assumes
  \(b_{\boldsymbol s}=\Theta(b)\) uniformly over selected bins;
- the appendix derives the signed-contrast information
  \(4w_hN\alpha^2B_h^TB_h\), inverse-trace allocation, and both asymptotic
  regimes;
- the Monte Carlo uses selected-channel Poissonization. At the displayed
  \(F_4\) operating point the six selected bins contain at most 0.0062
  probability per setting, so omitted multinomial covariance is a
  sub-percent correction.

A reproducible vector figure now scans total trial count and the local
linearity radius. It confirms \(N^{-1/2}\) finite-shot scaling and displays
the growth of local-inversion bias. The comparison table now describes
conventional methods as full-matrix and not neighborhood-restricted rather
than simply “global,” and the abstract specifies unit spectral norm.
