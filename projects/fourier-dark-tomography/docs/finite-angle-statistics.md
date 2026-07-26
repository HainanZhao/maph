# Finite-angle and statistical layer for the F4 cat protocol

Date: 2026-07-26

This note supplies the finite-probe-angle layer for the exact rank-twelve
certificate in `docs/agent-su4-tomography.md`.  It separates statements that
follow from the ideal unitary/count model from hardware-dependent design
choices.

The calculations are reproduced with

```text
python3 scripts/analyze_cat_finite_statistics.py
python3 -m unittest tests.test_cat_finite_statistics
```

The script uses only the Python standard library and the repository's
occupation-vector enumerator.

## 1. Exact finite-angle probabilities

Let

\[
 |\Psi_{\rm cat}\rangle={1\over2}\sum_{j=0}^3|4e_j\rangle,\qquad
 U_{\sigma,h}(\theta,\epsilon)
 =e^{i\sigma\epsilon h}e^{iH(\theta)}F_4 ,
 \quad \sigma\in\{+1,-1\}.
\]

For any output occupation \(s\) with \(\sum_ks_k=4\), the normalized
amplitude and probability are

\[
 A_s(U)={1\over2}
 \sqrt{{4!\over\prod_ks_k!}}\sum_{j=0}^3\prod_{k=0}^3U_{kj}^{s_k},
 \qquad p_s(U)=|A_s(U)|^2. \tag{1}
\]

Equation (1) is used directly at finite angle; no truncated probability
model is used.  Its directional derivative in a matrix direction \(\dot U\)
is obtained by differentiating the degree-four polynomial.  At
\(\theta=0\),

\[
 \dot U_\mu=e^{i\sigma\epsilon h}\,iG_\mu F_4,\qquad
 \partial_\mu p_s=2\operatorname{Re}(A_s^*\dot A_{s,\mu}). \tag{2}
\]

For the two probes

\[
 h_X=X_{01}-X_{02},\qquad h_Y=Y_{01}-Y_{02},
\]

one has \(h^3=2h\), hence the probe exponential is evaluated in the
closed form

\[
 e^{i\epsilon h}
 =I+{i\sin(\sqrt2\epsilon)\over\sqrt2}h
{\cos(\sqrt2\epsilon)-1\over2}h^2. \tag{3}
\]

The unknown error exponential is evaluated by a scaling-and-squaring
matrix series.  Automated checks verify probability normalization both at
\(\theta=0\) and at a nonzero twelve-coordinate error, and compare (2)
against symmetric finite differences through the full exponential.

## 2. Central-contrast theorem and a rigorous bias bound

This statement is not specific to \(F_4\).  Work in a fixed \(n\)-photon
sector.  Put \(|\phi\rangle=\widehat U_0|\psi\rangle\), assume the selected
event is dark, \(\langle s|\phi\rangle=0\), and define

\[
\begin{split}
 a(t)&=\langle s|e^{it\widehat h}|\phi\rangle,\\
 b_\mu(t)&=\langle s|e^{it\widehat h}i\widehat G_\mu|\phi\rangle,\\
 g_\mu(t)&=\left.\partial_{\theta_\mu}p_s(t,\theta)\right|_{\theta=0}
 =2\operatorname{Re}\{a(t)^*b_\mu(t)\}.
\end{split}
\]

For the calibrated central contrast

\[
 C_s(\theta,\epsilon)
 ={p_s(+\epsilon,\theta)-p_s(-\epsilon,\theta)\over4\epsilon}
 -C_s(0,\epsilon), \tag{4}
\]

the subtraction removes the generally nonzero probe-only baseline.  If

\[
 a_r=\langle s|(i\widehat h)^r|\phi\rangle,\qquad
 b_{r\mu}=\langle s|(i\widehat h)^r i\widehat G_\mu|\phi\rangle,
\]

then direct Taylor expansion gives

\[
\begin{split}
\left.\partial_{\theta_\mu}C_s\right|_0
={}&\operatorname{Re}(a_1^*b_{0\mu})\\
&+\epsilon^2\operatorname{Re}\left\{
{a_1^*b_{2\mu}\over2}
+{a_2^*b_{1\mu}\over2}
+{a_3^*b_{0\mu}\over6}\right\}
+O(\epsilon^4). \tag{5}
\end{split}
\]

The leading term is
\(\operatorname{Re}[(\ell_sh)^*(\ell_sG_\mu)]\), as used in the
rank certificate.  Thus the finite-angle Jacobian differs from its limiting
Jacobian at order \(\epsilon^2\), not order \(\epsilon\).

There is also a simple global bound.  Let

\[
 M=\|\widehat h\|\le n\|h\|,\qquad
 L_\mu=\|\widehat G_\mu\|\le n\|G_\mu\|.
\]

Since

\[
 |g_\mu'''(t)|\le
 2\sum_{k=0}^3{3\choose k}M^kM^{3-k}L_\mu
 =16M^3L_\mu,
\]

the central-difference remainder theorem implies

\[
\boxed{
\left|
\left.\partial_{\theta_\mu}C_s\right|_0
-\operatorname{Re}(a_1^*b_{0\mu})
\right|
\le {4\over3}\epsilon^2M^3L_\mu .
} \tag{6}
\]

This bound is rigorous but intentionally conservative.  If the explicit
second-order term in (5) is retained, the remaining error is at most
\((4/15)\epsilon^4M^5L_\mu\), by the analogous fifth-derivative bound.
For the present probes \(\|h_X\|=\|h_Y\|=\sqrt2\), while every coordinate
generator has norm one.

For the exact selected design, the computed relative Frobenius error of the
Jacobian of \([p(+\epsilon)-p(-\epsilon)]/\epsilon\) is

| \(\epsilon\) | relative Jacobian bias | \(\kappa_2(J_\epsilon)\) |
|---:|---:|---:|
| 0.005 | \(1.94\,10^{-4}\) | 7.045 |
| 0.010 | \(7.74\,10^{-4}\) | 7.043 |
| 0.020 | \(3.09\,10^{-3}\) | 7.033 |
| 0.050 | \(1.92\,10^{-2}\) | 6.968 |
| 0.100 | \(7.46\,10^{-2}\) | 6.759 |
| 0.150 | \(1.60\,10^{-1}\) | 6.513 |
| 0.200 | \(2.68\,10^{-1}\) | 6.475 |

Successive halving tests reproduce the factor-four decrease predicted by
(5).  The good condition number at larger angle does not cancel the growing
model bias.

The baseline in (4) must not be silently dropped.  It is even in
\(\epsilon\) for the six selected \(h_X\) outcomes, but for the selected
\(h_Y\) outcomes the largest signed baseline is

\[
 p_s(+\epsilon,0)-p_s(-\epsilon,0)
 ={9\over8}\epsilon^3+O(\epsilon^5). \tag{7}
\]

Calibration subtraction therefore removes an \(O(\epsilon^2)\) offset in
the divided contrast.  Finite calibration data add their own covariance.

## 3. Count models and Fisher information

Two likelihoods are implemented because “background” has no unique
mathematical meaning.

### Selected independent Poisson channels

For setting \(a\), selected outcome \(s\), and \(N_a\) input trials, take

\[
 Y_{as}\sim{\rm Pois}\{N_a[p_{as}(\theta)+b_s]\}.
\]

The information is

\[
 I_{\mu\nu}^{\rm P}
 =\sum_{a,s}N_a\,
 {(\partial_\mu p_{as})(\partial_\nu p_{as})
  \over p_{as}+b_s}. \tag{8}
\]

The script reports information per total trial for equal allocation among
the four settings.  Only the six certified outcomes in each setting are
used.

At a displaced dark event,
\(p_{as}=c_{as}\epsilon^2+O(\epsilon^3)\) and
\(\partial_\mu p_{as}=d_{as,\mu}\epsilon+O(\epsilon^2)\).  Consequently:

- with \(b_s=0\), the leading Fisher information has a finite nonzero limit
  as \(\epsilon\to0\);
- with \(b_s>0\), its leading scale is
  \(\epsilon^2/(c_{as}\epsilon^2+b_s)\), so too small a displacement loses
  information to the background floor.

For the twelve selected channels, the exact leading coefficients
\(c_{as}\) range from \(3/16\) to \(1\).  The square root of the information
condition number (equivalently, the condition number of a whitened
sensitivity matrix) is:

| \(\epsilon\) | \(b=0\) | \(b=10^{-6}\) | \(b=10^{-4}\) |
|---:|---:|---:|---:|
| 0.005 | 4.786 | 4.781 | 6.529 |
| 0.010 | 4.787 | 4.785 | 5.653 |
| 0.020 | 4.793 | 4.792 | 4.838 |
| 0.050 | 4.831 | 4.831 | 4.829 |
| 0.100 | 4.981 | 4.981 | 4.982 |
| 0.150 | 5.281 | 5.281 | 5.282 |
| 0.200 | 5.842 | 5.842 | 5.843 |

The near equality at moderate angle means the probe signal has risen above
these particular floors.  It is not evidence that real backgrounds are
negligible.

### Selected multinomial channels

For each setting, resolve the six selected outcomes and pool all other
outcomes into a seventh category.  A normalized uniform contamination model
is

\[
 q_{as}=(1-\beta)p_{as}+{\beta\over35},\qquad
 q_{a,\rm other}=1-\sum_{s\in S_a}q_{as}. \tag{9}
\]

The per-trial information is the standard
\(\sum_c(\partial q_c)(\partial q_c)^\mathsf T/q_c\), including the pooled
category.  This model accounts for multinomial anticorrelation and does not
obtain extra tomography information by resolving all bright outcomes.  At
\(\beta=10^{-3}\), the whitened condition is 5.760, 4.842, 4.792, and 4.835
at \(\epsilon=0.005,0.01,0.02,0.05\), respectively.

For a direct contrast estimator made from independent empirical
frequencies,

\[
 \widehat C_s={\widehat p_s^+-\widehat p_s^-\over4\epsilon},
\]

the single-outcome variance before baseline-calibration uncertainty is

\[
 {\rm Var}(\widehat C_s)
 ={1\over16\epsilon^2}\left[
 {p_s^+(1-p_s^+)\over N_+}
 +{p_s^-(1-p_s^-)\over N_-}\right]. \tag{10}
\]

Different outcomes in one setting have the usual negative multinomial
covariances.  A likelihood fit to the full selected-category data uses
these correlations automatically and is preferable to treating twelve
contrasts as independent.

## 4. What the angle tradeoff does and does not establish

Within the ideal model, \(\epsilon\) must balance:

1. central-contrast/model bias, which begins at \(O(\epsilon^2)\);
2. a fixed background floor, whose penalty grows when
   \(c\epsilon^2\ll b\);
3. calibration uncertainty in the probe angle, generator, and baseline;
4. available counts and the radius over which the local error model is
   accurate.

For the illustrative floors above, \(\epsilon\) around \(0.02\)--\(0.05\)
radians is a reasonable *simulation regime*: the relative finite-angle
Jacobian bias is about \(0.3\%\)--\(1.9\%\), and a \(10^{-4}\) per-channel
Poisson floor no longer severely degrades conditioning.  This is not a
hardware recommendation.  A device-specific choice requires measured
backgrounds, a target systematic-error budget, loss and visibility, and an
explicit shot allocation.

A Cramér--Rao statement can safely be made only conditionally: under a
specified likelihood and for locally unbiased estimators,
\({\rm Cov}(\widehat\theta)\succeq I^{-1}\).  Multiplying the per-total-shot
matrices in the script by a chosen trial number gives that model's bound.
It does not include source-generation rate, detector dead time, drifting
calibrations, or estimator bias, and therefore is not a cost forecast.

## 5. Identifiability caveats from imperfect resources

The rank-twelve theorem assumes a calibrated coherent input and calibrated
signed probes.  Several failures are structurally important.

### Cat-state phase is the missing reference

Let the four cat components acquire unknown phases \(\alpha_j\).  Infinitesimally
these are produced by an input diagonal phase \(D\), since
\(|4e_j\rangle\) acquires phase \(4d_j\).  But

\[
 F_4e^{iD}=e^{iF_4DF_4^\dagger}F_4. \tag{11}
\]

Therefore the three relative cat-phase errors are exactly confounded with
the three coherent device directions that were invisible to Fock inputs.
If these phases are included as unconstrained nuisance parameters, the
augmented model cannot separately identify all twelve device coordinates
from this experiment alone.  An independent phase calibration or additional
reference state is necessary.

Partial dephasing of the cat is not merely lower visibility: in the fully
incoherent limit the input again has the number-state input-phase gauge, and
the full-rank mechanism disappears.

### Probe calibration

- A probe-angle scale error changes the finite-angle Jacobian and, at
  leading order, scales its associated contrast block.
- A common generator offset present in both nominal signs can be locally
  indistinguishable from part of the unknown device error.
- Imperfect sign reversal leaves even-order terms in the contrast.
- Probe-only baseline subtraction corrects a stable offset but does not
  correct an incorrect sensitivity matrix.

Bright-output calibration data or separate probe characterization can add
constraints, but identifiability must then be checked on the *augmented*
Jacobian containing device, state, and probe parameters.

### Beyond the coherent lossless model

Loss, distinguishability, source contamination, detector crosstalk, and
drift change the likelihood, not just its variance.  A background floor
alone cannot represent them.  The exact finite-angle code is a suitable
ideal-model reference against which those nuisance models can be added, but
the present analysis makes no hardware sample-complexity or cost claim.

## 6. Conclusions for the paper

The defensible finite-angle result is stronger than an asymptotic rank
statement:

- the exact probability law and its exact local derivative can be evaluated
  at any programmed angle;
- the central-contrast Jacobian has an explicit \(O(\epsilon^2)\) expansion
  and a rigorous norm bound;
- the certified rank remains well conditioned across a useful small-angle
  regime in the ideal model;
- a background floor creates a transparent displacement-versus-bias
  tradeoff;
- unknown cat phases recreate precisely the three-dimensional gauge that
  the coherent resource was introduced to remove.

The last point should be stated as prominently as the rank-twelve
certificate.  It identifies the experimental resource requirement and
prevents “full tomography” from being overclaimed under uncalibrated state
preparation.
