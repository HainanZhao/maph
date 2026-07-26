# Submission-ready status: directional response jets

Date: 2026-07-26

## Outcome

The project has been reorganized into a focused Physical Review A theory
submission:

> **Directional response jets of suppressed multiphoton events in a
> four-mode Fourier interferometer**

The main novelty claim is no longer generic “suppressed events diagnose
devices” or Krawtchouk reciprocity by itself. Both have substantial prior
art. The defensible contribution is the coherent, event-level directional
response jet before random-error averaging:

- an event may remain dark for a full one-parameter mixer subgroup;
- a different direction may produce quadratic leakage;
- a tangent-flat direction may begin at quartic order.

The sectorwise reciprocity theorem remains an important structural result,
but it is positioned as an \(F_4\)-specific, phase-resolved refinement and
application of classical symmetric-power/Krawtchouk duality.

## New exact result added during submission preparation

For the four-photon event

\[
\boldsymbol r=\boldsymbol s=(0,1,2,1),
\]

the two quadratures on output modes \(1,3\) obey the all-angle laws

\[
P_{Y_{13}}(\epsilon)=0,\qquad
P_{X_{13}}(\epsilon)=\frac{\sin^2(2\epsilon)}{16}.
\]

The \(Y_{13}\) null extends to every positive odd \(a\) in

\[
(0,a,2a,a)\longrightarrow(0,a,2a,a).
\]

This makes the four-photon case the cleanest proposed experiment: the same
mode pair and angle are used, while only the beam-splitter quadrature changes.

## Applications and falsifiable predictions

### 1. Quadrature-sensitive calibration

The exact \(X_{13}/Y_{13}\) contrast checks the programmed mixer quadrature.
For a small angular misalignment \(\delta\) away from \(Y_{13}\) toward
\(X_{13}\),

\[
P(\epsilon,\delta)
=\frac{\epsilon^2\sin^2\delta}{4}+o(\epsilon^2).
\]

The null is therefore sensitive to coherent axis error. It is not full
unitary tomography and cannot identify a noise source from one count alone.

### 2. Cross-configuration consistency

Sectorwise reciprocal occupation pairs have equal ideal amplitudes throughout
the standard dephased family \(H(z)/2\) for \(|z|=1\). Sweeping \(z\) and
comparing reciprocal configurations gives an overdetermined joint check of
state preparation, the programmed interferometer, indistinguishability, and
detection.

What persists is the reciprocal-pair equality. A Fourier-dark event need not
remain dark for generic \(z\); for \(a=1\), its coefficient is proportional
to \(2(1+z^2)\).

### 3. Protected output subgroups

For

\[
(1,1,1,1)\longrightarrow(3,1,0,0),
\]

arbitrary \(U(2)\) rotations on pairs \(02,12,13,23\) leave the target dark.
This supplies event-specific constraints for changing an analysis basis
without opening that output.

### 4. Exact, quadratic, and quartic benchmarks

For \((0,1,2,1)\to(0,1,2,1)\),

\[
\begin{aligned}
P_{X_{12}}&=\epsilon^2/64+\cdots,\\
P_{Y_{12}}&=25\epsilon^2/64+\cdots,\\
P_{X_{13}}&=\epsilon^2/4+\cdots,\\
P_{Y_{13}}&=0\quad\text{exactly}.
\end{aligned}
\]

For the eleven-photon affine-family root

\[
(0,1,3,7)\longrightarrow(1,3,3,4),
\]

\[
P_{Y_{12}}(\epsilon)=\frac{315}{8192}\epsilon^4+O(\epsilon^5).
\]

This eleven-photon result is a future, high-resource prediction. It is an
isolated integral root on the scanned affine family, not a proof of global
isolation.

## Nuisance-floor and finite-shot calculation

The submission includes the transparent illustrative model

\[
P_{\rm obs}
=\mathcal V P_{\rm ind}+(1-\mathcal V)P_{\rm dist}+B.
\]

This is a run-level mixture with fully distinguishable labelled photons, not
a general partial-distinguishability theory.

At \(\epsilon=0.1\), \(\mathcal V=0.99\), and \(B=0\), the four-photon
quadrature comparison gives

\[
P_{\rm obs}^{X_{13}}=2.91093\times10^{-3},\qquad
P_{\rm obs}^{Y_{13}}=4.74917\times10^{-4}.
\]

A normal-approximation difference-of-proportions estimate gives 14,228
accepted four-photon trials per setting for a nominal \(5\sigma\) contrast.
This is model-dependent, not a scalable sample-complexity theorem.

Post-interferometer attenuation cannot lift a fixed exact amplitude zero when
conditioning on all photons. Internal or path-dependent loss can change
interfering paths; source impurity and detector noise can add a count floor.

## Literature and novelty audit

The manuscript now explicitly accounts for:

- classical symmetric-power reciprocity: Chen--Louck (1998), Chami--Sing--
  Sookoo (2014), and Feinsilver--Kocik (2005);
- Fourier suppression laws and generic disorder leakage: Tichy et al.
  (2010), Dittel et al. (2018);
- device diagnostics based on forbidden events: Crespi et al. (2016) and
  Wang et al. (2023);
- partial distinguishability: Shchesnovich (2015);
- suppression laws beyond permutation symmetry: Bezerra--Shchesnovich
  (2023);
- recent suppressed-output indistinguishability benchmarking: Sanz et al.
  (2026);
- symmetric-group Fourier analysis of many-body amplitudes:
  Dufour--Buchleitner (2026 revision).

No searched source was found that states the exact/quadratic/quartic coherent
directional response classification or the all-odd \(Y_{13}\) protected axis.
The paper uses “to our knowledge” scope and avoids a categorical first-ever
claim.

## Adversarial proof audit

An independent hostile review:

- checked 200 random sectorwise-reciprocity instances with \(d,N\leq10\);
- reproduced every tabled leakage coefficient;
- found no theorem-breaking error in the Krawtchouk/factorial normalization;
- confirmed the all-odd reflection pairing;
- required, and prompted, narrower wording about gauge, \(H(z)\), event-level
  fingerprints, the eleven-photon root, and loss location.

## Submission artifacts

- `paper/manuscript.tex`
- `paper/supplement.tex`
- `paper/references.bib`
- `paper/build/manuscript.pdf`
- `paper/build/supplement.pdf`
- `paper/cover-letter.md`
- `paper/submission-checklist.md`
- `paper/submission-source.tar.gz`

## Verification

```text
python3 -m unittest discover -s tests -v
python3 scripts/analyze_reciprocity_census.py
python3 scripts/analyze_unitary_leakage.py
python3 scripts/analyze_finite_shot_protocol.py
```

Status:

- 54 tests passed;
- exact leakage certificates passed;
- exact finite-angle formula certificate passed;
- main and supplemental PDFs compile without TeX errors, undefined
  citations/references, or overfull boxes.

## Remaining nontechnical confirmations

Before portal submission, the author must confirm affiliation, public email,
funding, conflicts, license, and whether to post the same version on arXiv.
These are personal declarations, not research blockers.
