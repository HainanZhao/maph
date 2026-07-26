# Revised paper outline: dark-event tomography

Date: 2026-07-26

## Working title

**Dark-event interferometry: gauge limits and complete off-diagonal
tomography of a four-mode Fourier device**

Alternatives:

- **Signed-probe tomography from multiphoton dark events**
- **From suppressed counts to complete local tomography in a four-mode
  interferometer**

## Paper-level message

Exact dark events are usually treated as scalar witnesses of device
quality.  With a calibrated signed probe, their count probabilities
instead become linear interferometric measurements of a small unitary
error.  Number-state inputs face an exact input-phase gauge: in a
four-mode Fourier device, three of the twelve nominally off-diagonal
error coordinates are unobservable, and the optimal rank is nine.  A
phase-coherent four-photon cat input removes that gauge.  Two calibrated
probe quadratures and twelve dark-output count differentials then give
an exact, moderately conditioned, full-rank \(12\times12\) local
tomography scheme.

The paper should separate three claims carefully:

1. the signed-probe formula is a general local measurement theorem;
2. the Fock-state rank-nine ceiling is an exact gauge no-go theorem;
3. the rank-twelve result is a concrete \(F_4\), four-photon
   construction, not yet a general optimal-design theorem for all
   \(F_m\).

## Abstract skeleton

Multiphoton suppression provides sensitive null tests for linear
optical devices, but an unprobed dark-event probability is quadratic in
a small error and cannot determine its sign.  We show that applying
positive and negative calibrated output probes converts dark-event
counts into linear interferometric observables.  We then identify a
previously hidden limitation: for every number-state input, an
\((m-1)\)-dimensional family of nominally off-diagonal errors in an
\(m\)-mode Fourier interferometer is exactly indistinguishable from
input phases.  An exhaustive exact four-photon calculation proves that
the resulting rank-nine ceiling at \(m=4\) is attainable.  To remove the
gauge, we use the known phase-twisted all-bunched cat states, which
populate exactly one Fourier charge sector.  For \(F_4\), one
four-photon cat input, two
signed probe quadratures, and twelve selected dark-output
differentials produce an exact full-rank Jacobian with determinant
\(-177147/256\).  We describe how the construction diagnoses
output-equivalent internal errors and delimit the effects of diagonal
phases, loss, distinguishability, and state-preparation uncertainty.

## 1. Introduction

### Motivation

- Suppressed multiphoton outcomes are already used as device-quality
  witnesses.
- A zero count by itself is not a coordinate-resolved diagnostic.
- At an exact zero, the unprobed probability has no linear term, so
  amplitude derivatives cannot simply be called measurable.
- A calibrated probe supplies a known reference amplitude, analogous to
  a local oscillator, while retaining photon counting as the only
  measurement.

### Questions

1. Which infinitesimal unitary-error combinations are observable from
   dark-event count probabilities?
2. What is the minimum information supplied by number-state inputs?
3. Which additional input resource removes the remaining phase gauge?
4. Can a complete exact design be exhibited with experimentally
   interpretable probes?

### Contributions

- general signed-probe differential theorem;
- general number-state gauge obstruction;
- exact four-photon rank-nine saturation;
- a new tomographic use of the known \(F_m,n\) cat-sector identity;
- exact \(F_4\) rank-twelve certificate;
- output-equivalent propagation rule for internal errors.

## 2. Setup and parameter target

Use

\[
F_m(k,j)=m^{-1/2}\omega^{kj},
\qquad \omega=e^{2\pi i/m}.
\]

For \(m=4\), parameterize the off-diagonal error generator by

\[
\theta=(x_{01},y_{01},x_{02},y_{02},x_{03},y_{03},
        x_{12},y_{12},x_{13},y_{13},x_{23},y_{23}),
\]

with

\[
X_{pq}=|p\rangle\langle q|+|q\rangle\langle p|,
\qquad
Y_{pq}=-i|p\rangle\langle q|+i|q\rangle\langle p|.
\]

The unknown device is locally

\[
U(\theta)=e^{iG(\theta)}F_4,\qquad
G(\theta)=\sum_\mu\theta_\mu G_\mu.
\]

### Scope warning: output-diagonal coordinates

The twelve-coordinate target intentionally excludes the three
traceless diagonal generators of \(SU(4)\).  An output-diagonal
generator multiplies each unprobed output Fock amplitude by an
outcome-dependent phase and is invisible to output number
probabilities.  At an exact dark event its first amplitude derivative
also vanishes, so it is absent from the leading infinitesimal
signed-probe formula below.

Output-diagonal errors may enter at higher order when they precede a
finite noncommuting probe, but they are **not identified by the
infinitesimal dark-event scheme in this paper**.  No claim of full
\(SU(4)\) tomography is made; “complete” always means complete within
the twelve specified off-diagonal coordinates.

## 3. General signed-probe theorem

Let \(e=(\psi,s)\) be an ideal dark transition and define its complex
amplitude-gradient vector

\[
v_{e,\mu}
=i\langle s|\widehat G_\mu\,\widehat U_0|\psi\rangle.
\]

Append a known signed probe

\[
U_\pm(\theta,\epsilon)
=e^{\pm i\epsilon H}e^{iG(\theta)}U_0,
\qquad H=\sum_\mu h_\mu G_\mu.
\]

### Theorem 1: observable probability differential

\[
\Delta P_{e,h}
:=P_e(+\epsilon h)-P_e(-\epsilon h)
=4\epsilon\,
\operatorname{Re}\!\left[
(v_e\cdot h)^*(v_e\cdot\theta)
\right]
+O(\epsilon\|\theta\|^2+\epsilon^2\|\theta\|+\epsilon^3).
\]

For experimental use, subtract the zero-error probe calibration,

\[
\Delta P_{e,h}^{\rm cal}(\theta)
=\Delta P_{e,h}(\theta)-\Delta P_{e,h}(0),
\]

which removes the probe-only odd bias.

### Consequences

- The observable is a signed count-probability difference, not an
  assumed measurement of a complex amplitude.
- Without the probe, \(P_e(\theta)=|v_e\cdot\theta|^2+O(\|\theta\|^3)\);
  the sign and linear coordinate information are lost.
- All probes applied to one dark event generate rows in
  \(\operatorname{span}_{\mathbb R}\{\operatorname{Re}v_e,
  \operatorname{Im}v_e\}\).  One event supplies at most two real
  coordinates.
- Two phase quadratures are the natural way to expose both components
  of a complex leakage amplitude, although global probe-setting
  minimality depends on the collection of outcomes.

Proof: expand the dark amplitude to first order in the unknown and
probe generators, square it, and antisymmetrize in \(\epsilon\).

## 4. Fock-input gauge obstruction and rank-nine optimum

### Theorem 2: transported input-phase gauge

For any real traceless diagonal

\[
D=\operatorname{diag}(d_0,\ldots,d_{m-1}),
\]

put

\[
K_D=F_mDF_m^\dagger.
\]

The diagonal of \(K_D\) is zero, so \(K_D\) lies in the off-diagonal
generator space.  Nevertheless, for every number-state input
\(|r\rangle\),

\[
e^{iK_D}F_m|r\rangle
=F_me^{iD}|r\rangle
=e^{i\sum_jd_jr_j}F_m|r\rangle.
\]

The error is a global phase.  It remains invisible after any arbitrary
calibrated output unitary \(V\), because \(V\) multiplies both sides.
Thus number-state experiments cannot observe this
\((m-1)\)-dimensional right-diagonal gauge.

For \(F_4\), an explicit null basis inside the twelve-coordinate target
is

\[
\begin{aligned}
K_A&=X_{01}+X_{03}+X_{12}+X_{23},\\
K_B&=Y_{01}-Y_{03}+Y_{12}+Y_{23},\\
K_C&=X_{02}+X_{13}.
\end{aligned}
\]

Therefore the Fock-input rank is at most \(12-3=9\).

### Exact saturation

- Enumerate all four-photon input/output occupations.
- There are 184 dark transitions with two independent amplitude
  quadratures.
- Their aggregate exact rational rank is nine, with precisely the null
  span above.
- Five rank-two dark events attain rank nine, meeting the lower bound
  \(\lceil9/2\rceil=5\).
- A single input \((1,1,1,1)\) and five selected dark outputs also attain
  rank nine.

An exact normalized certificate uses

\[
\begin{array}{c|c}
(0013)&X_{03},Y_{03}\\
(0022)&X_{02},Y_{02}\\
(0031)&X_{12},Y_{12}\\
(0112)&X_{23},Y_{23}\\
(0220)&Y_{02}
\end{array}
\]

for nine scalar differentials.  The minor in columns
\((x_{01},y_{01},x_{02},y_{02},x_{03},y_{03},x_{12},y_{12},y_{13})\)
has determinant \(81/8\).  The exact physical \(9\times12\) matrix
should appear in the main text or an immediately adjacent appendix.

The main text should show the null theorem and a compact five-event
certificate.  Put exhaustive enumeration, canonicalization, and all
independent rows in the supplement.

Interpretation: the usual removal of output phases does not remove the
independent input-phase gauge transported through the Fourier device.
The local number-probability model is a double-coset problem.

## 5. General phase-twisted Fourier-cat dark sectors

Define, for \(n\geq1\),

\[
|\Psi_\ell^{(m,n)}\rangle
=\frac1{\sqrt m}\sum_{j=0}^{m-1}
\omega^{-\ell j}|ne_j\rangle.
\]

For output occupation \(s\) with total \(n\), let

\[
Q(s)=\sum_{k=0}^{m-1}k s_k\pmod m.
\]

### Known cyclic-sector identity

\[
\mathcal A_{\Psi_\ell^{(m,n)},s}(F_m)
=
\sqrt{\frac{n!}{\prod_ks_k!}}\,
m^{(1-n)/2}\,
\mathbf1_{\{Q(s)=\ell\}}.
\]

Proof: a component \(|ne_j\rangle\) contributes

\[
\sqrt{\frac{n!}{\prod_ks_k!}}\,
m^{-n/2}\omega^{jQ(s)};
\]

the cat coefficients produce the root-of-unity sum
\(m^{-1/2}\sum_j\omega^{j(Q-\ell)}\).

### Interpretation and novelty boundary

- Every output outside one modular sector is exactly dark.
- The input carries a phase reference across all modes and lifts the
  continuous right-diagonal gauge locally, conditional on independently
  calibrated preparation phases.
- The selection rule itself is the standard cyclic mechanism in a
  coherent all-bunched representation.  Cite Vourdas and Dunningham,
  Phys. Rev. A 71, 013809 (2005), Eqs. (18)--(20), as a direct
  antecedent, and Dittel et al. for the general symmetry formulation.
  Do not claim it as a new suppression law.
- The new use is as a structured dark-state resource for local
  tomography.

## 6. Exact \(F_4\) cat-state rank-twelve certificate

Use

\[
|\Psi_{\rm cat}\rangle
=\frac12(
|4000\rangle+|0400\rangle+|0040\rangle+|0004\rangle).
\]

It has 25 exactly dark outputs satisfying \(Q(s)\ne0\pmod4\).

Use two calibrated probes,

\[
H_X=X_{01}-X_{02},\qquad
H_Y=Y_{01}-Y_{02}.
\]

They are the two quadratures coupling mode zero to the antisymmetric
supermode \((|1\rangle-|2\rangle)/\sqrt2\).  The four programmed device
settings are \(+\epsilon H_X,-\epsilon H_X,+\epsilon H_Y,-\epsilon H_Y\).

### Exact normalization

For a component \(|4_j\rangle\) and output \(s\), define

\[
D_s=2^4\sqrt{4!\prod_ks_k!}.
\]

If \(M_{s,\mu}^{(j)}\in\mathbb Z[i]\) is the common-denominator
generator moment, then

\[
v_{s,\mu}
=\frac{i}{2D_s}\sum_{j=0}^3M_{s,\mu}^{(j)}.
\]

This includes both Fock normalization and the factor \(1/2\) in the cat
state.

### \(X\)-block

In column order
\((x_{01},x_{02},x_{03},x_{12},x_{13},x_{23})\), use \(H_X\) and
outputs

\[
(0022),(0112),(0310),(1021),(1030),(1102).
\]

Define the physical Jacobian as

\[
(J_X)_{s,\mu}
=\left.
\partial_{\theta_\mu}
\lim_{\epsilon\to0}
\frac{\Delta P_{s,H_X}}{\epsilon}
\right|_{\theta=0}.
\]

It is therefore a leading infinitesimal contrast Jacobian, not an exact
finite-\(\epsilon\) response.  Its matrix is

\[
J_X=
\begin{pmatrix}
0&-\frac32&0&0&-\frac32&0\\
\frac34&0&0&\frac34&0&\frac32\\
\frac94&0&0&\frac34&0&0\\
\frac34&0&\frac34&0&0&\frac32\\
0&-4&0&0&0&0\\
\frac34&0&\frac32&\frac34&0&0
\end{pmatrix},
\qquad
\det J_X=-\frac{243}{8}.
\]

### \(Y\)-block

In column order
\((y_{01},y_{02},y_{03},y_{12},y_{13},y_{23})\), use \(H_Y\) and
outputs

\[
(0022),(0112),(0220),(0310),(1021),(1102).
\]

\[
J_Y=
\begin{pmatrix}
0&-\frac32&0&0&-\frac32&0\\
\frac34&0&0&\frac34&0&\frac32\\
0&-\frac32&0&0&\frac32&0\\
\frac94&0&0&\frac34&0&0\\
\frac34&0&-\frac34&0&0&\frac32\\
\frac34&0&-\frac32&\frac34&0&0
\end{pmatrix},
\qquad
\det J_Y=\frac{729}{32}.
\]

The six omitted \(Y\) columns in the \(H_X\) rows and the six omitted
\(X\) columns in the \(H_Y\) rows are all exactly zero; the verification
asserts them entry by entry.

Thus

\[
\det\operatorname{diag}(J_X,J_Y)
=-\frac{177147}{256}\ne0.
\]

The twelve scalar differentials meet the dimension lower bound for
regular local identification by scalar probability differentials.
All twelve counts are obtained in four programmed settings because
multiple output occupations are recorded simultaneously.  Four settings
are sufficient; setting-count minimality is not claimed.

### Conditioning

- raw physical Jacobian: \(\kappa\simeq7.05\);
- independently row-normalized geometry: \(\kappa\simeq4.86\);
- ideal background-free Poisson weighting: \(\kappa\simeq4.79\);
- probe-only leading count coefficients lie between \(3/16\) and \(1\).

Present these as preliminary local conditioning, not as a globally
optimal design.

## 7. Propagation of internal circuit errors

Let the ideal circuit factor as

\[
U_0=U_LU_{L-1}\cdots U_1.
\]

If a small generator \(H_\ell\) is inserted after layer \(\ell\), write

\[
W_\ell=U_LU_{L-1}\cdots U_{\ell+1}.
\]

Then

\[
U_L\cdots U_{\ell+1}e^{i\delta H_\ell}
U_\ell\cdots U_1
=e^{i\delta\,W_\ell H_\ell W_\ell^\dagger}U_0
+O(\delta^2).
\]

Thus the tomography estimates the off-diagonal coordinates of the
output-equivalent generator

\[
G_{\rm eff}
=\sum_\ell\delta_\ell
W_\ell H_\ell W_\ell^\dagger
\]

to first order.

### What this enables

- map a calibrated component-error model to predicted dark-count
  differentials;
- estimate aggregate coherent crosstalk in the device output frame;
- compare reconstructed coordinates across circuit reconfigurations;
- design probes that maximize sensitivity to specified internal
  components after adjoint propagation.

### What it does not enable automatically

- Multiple layers producing the same output-equivalent generator cannot
  be localized from one circuit configuration.
- Output-diagonal projections are outside the twelve-coordinate target
  and absent from the infinitesimal dark-event Jacobian.
- Separating layer errors requires additional circuit configurations,
  independently addressable controls, or prior sparsity/calibration
  assumptions.

## 8. Statistical model and experimental protocol

### Protocol

1. Prepare the phase-stable four-mode cat state.
2. Implement the nominal \(F_4\).
3. Apply \(+\epsilon H_X\) and \(-\epsilon H_X\); record the six selected
   number-resolved outputs.
4. Repeat for \(+\epsilon H_Y\) and \(-\epsilon H_Y\).
5. Subtract the calibrated zero-error differential.
6. Solve the exact linear system initially, then use a likelihood model
   for finite data.

### Required statistical additions for submission

- multinomial rather than independent-count covariance;
- unequal shot allocation between probe settings;
- finite-\(\epsilon\) bias and a two- or three-angle extrapolation;
- background/dark-count floor;
- propagated uncertainty in the programmed probe generators;
- condition number and Fisher information after all nuisance parameters.

## 9. Limitations and assumption audit

1. **Cat-state preparation is the main experimental cost.** A
   phase-stable four-mode four-photon cat is substantially harder than
   \(|1,1,1,1\rangle\).  The rank-nine Fock scheme is the nearer-term
   experiment.
2. **Output-diagonal errors are not estimated.** They are outside the
   declared twelve-coordinate target and vanish from the leading
   infinitesimal dark-event response.
3. **The analysis is local.** At finite errors, generator
   noncommutativity, probe ordering, and multiple solutions matter.
4. **Darkness assumes ideal indistinguishability.** Partial
   distinguishability, loss, detector noise, and cat dephasing create
   probability floors and can bias the signed differential.
5. **State-preparation and measurement errors can imitate device
   errors.** A complete experiment needs independent SPAM calibration
   or a joint identifiable model.
6. **The cat-sector theorem is not a new suppression law.** Its role is
   to supply phase-referenced dark outputs.
7. **Two-probe global minimality is not proved.** Exact construction
   shows two combined probes suffice.  Finite searches found rank at
   most eleven for one generic probe, but this is not yet a no-go
   theorem.
8. **Internal-layer localization is underdetermined in one
   configuration.** Only the summed output-equivalent generator is
   reconstructed.

## 10. Discussion

- Dark outcomes can be promoted from pass/fail witnesses to
  coordinate-resolved interferometric sensors.
- Identifiability depends on input coherence, not only on the number of
  measured outputs.
- The Fock no-go theorem gives a clean operational meaning to the
  transported right-phase gauge.
- The cat construction reaches the full off-diagonal target using the
  dimension-minimal twelve scalar differentials for regular local
  identification.
- Natural next questions are robust design under realistic noise,
  lower-cost coherent input states, and \(F_m\) probe constructions with
  scalable conditioning.

## Main-text figures and tables

1. **Signed-probe schematic:** unknown error followed by
   \(+\epsilon/-\epsilon\) probes; dark amplitude becomes a count
   differential.
2. **Gauge diagram:** twelve off-diagonal coordinates, three transported
   input phases, nine-dimensional Fock quotient, and cat-state gauge
   lifting.
3. **Fourier charge sectors:** the phase-twisted cat populates one
   modular sector and leaves the rest dark.
4. **Rank-twelve design:** two \(6\times6\) response blocks or a sparse
   Jacobian heatmap.
5. **Conditioning/noise plot:** singular values and predicted estimator
   uncertainty versus probe angle and background floor.

## Self-contained appendices

- exact proof of the signed-probe remainder statement;
- all Gaussian-integer generator moments;
- exhaustive four-photon Fock rank census;
- the five-event rank-nine certificate;
- exact rational row reduction and determinants;
- finite-probe simulations and Fisher-information diagnostics;
- partial distinguishability, loss, and SPAM model;
- internal-error adjoint dictionaries for a chosen circuit
  decomposition;
- reproduction instructions.

## Reproduction

```text
PYTHONDONTWRITEBYTECODE=1 \
python3 scripts/search_su4_dark_tomography.py
```

The script uses Gaussian-integer pairs, integers, and
`fractions.Fraction` for all zero, rank, normalization, and determinant
certificates.  The detailed theorem record is
`docs/agent-su4-tomography.md`.
