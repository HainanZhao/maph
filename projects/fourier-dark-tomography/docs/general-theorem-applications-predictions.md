# Applications and predictions of the general Fourier-cat theorem

Date: 2026-07-26

## Scope

The theorem concerns a nominal \(m\)-mode Fourier multiport, the coherent
input

\[
|\mathrm{Cat}_{m,m}\rangle
=m^{-1/2}\sum_{j=0}^{m-1}|m e_j\rangle ,
\]

and a small coherent output error \(e^{iH}\), with \(H=H^\dagger\) and
\(H_{aa}=0\).  It locally identifies the \(m(m-1)\) real off-diagonal
coordinates of \(H\).  It does not identify output-diagonal phases, give
global process tomography, or by itself separate state-preparation,
interferometer, and detector errors.

## Main application: calibrated coherent-error sensing

For every cyclic distance \(c=1,\ldots,\lfloor m/2\rfloor\), use the
nominally dark output occupations

\[
s_{p,c}=(m-1)e_p+e_{p+c}.
\]

For a non-antipodal distance, their complex amplitude differentials are

\[
L_{p,c}=(m-1)z_p+z_{p+c},
\qquad z_p=H_{p,p-c}.
\]

Two fixed calibrated probes in phase quadrature convert the real and
imaginary parts of all \(L_{p,c}\) into signed photon-count contrasts.
Inverting the cyclic systems reconstructs every off-diagonal entry of
\(H\).  Operationally, the dark outputs become a bank of null sensors:
they have no ideal carrier at the nominal device, while the probes provide
a calibrated local oscillator that restores the sign and phase information
lost by unprobed probabilities.

This can be used for:

1. commissioning a Fourier or complex-Hadamard photonic processor;
2. monitoring coherent drift and mode crosstalk;
3. reconstructing an output-equivalent error generator and programming a
   first-order correction;
4. checking a component-error model after propagating internal errors to
   the output frame;
5. targeted sensing, by retaining only the cyclic-distance blocks in which
   the hardware is expected to have crosstalk;
6. separating an antisymmetric coherent response from a probe-independent
   incoherent count floor.

## Falsifiable predictions

### 1. Exact modular darkness

At the ideal Fourier device, an output \(s\) is dark unless

\[
Q(s)=\sum_a a s_a=0\pmod m.
\]

Every selected \(s_{p,c}\) has \(Q=c\neq0\) and therefore has exactly zero
ideal probability.

### 2. Linear signed response and quadratic unprobed response

If the unknown error is scaled as \(H=tK\), the unprobed dark probability
begins as \(t^2\), whereas the signed probe contrast begins as \(t\).
Reversing \(K\) therefore reverses the contrast but leaves the leading
unprobed probability unchanged.  This is the observable distinction between
ordinary null leakage and phase-sensitive null tomography.

More explicitly, if \(\ell_s\) is the dark-amplitude functional and \(h\)
is a calibrated probe, then

\[
\frac{P_s(H+\epsilon h)-P_s(H-\epsilon h)}{4\epsilon}
=\operatorname{Re}\!\left[\ell_s(h)^*\ell_s(H)\right]
+O(\epsilon^2,\|H\|^2).
\]

The exact convention-dependent prefactor can be calibrated at the ideal
device; the odd sign reversal is invariant.

### 3. A single-edge crosstalk fingerprint

For a non-antipodal cyclic distance, suppose only \(z_q\) is nonzero.
Then only two amplitude coordinates in that distance block respond:

\[
L_{q,c}=(m-1)z_q,\qquad L_{q-c,c}=z_q.
\]

Thus the normalized signed contrasts have the fixed ratio
\((m-1):1\), while the corresponding unprobed leading probabilities have
ratio \((m-1)^2:1\).  Extra responding events, or a different ratio in the
small-error limit, falsify the isolated-edge model.

### 4. The even-\(m\) antipodal signature

When \(m\) is even and \(c=m/2\), Hermiticity gives

\[
L_{p,c}=m\,\operatorname{Re}z_p
+i(m-2)\,\operatorname{Im}z_p.
\]

Before row normalization, the real- and imaginary-quadrature signed
contrast gains are proportional to \(m^2\) and \((m-2)^2\).  Their predicted
gain ratio is therefore

\[
\frac{G_{\mathrm{imag}}}{G_{\mathrm{real}}}
=\left(\frac{m-2}{m}\right)^2.
\]

It is \(1/4\) at \(m=4\), \(4/9\) at \(m=6\), and tends to one for large
\(m\).  Calibration rescaling removes this anisotropy in the inverse.

### 5. Complete local visibility of off-diagonal coherent errors

For every nonzero off-diagonal Hermitian \(H\), at least one selected signed
contrast is nonzero to first order.  Conversely, an output-diagonal phase
generator produces no first-order signal in this protocol.  A measured
rank deficiency beyond these \(m-1\) excluded diagonal directions indicates
a broken assumption, a miscalibrated probe, or insufficient state coherence.

### 6. Resource law

The construction predicts the following exact algebraic resource counts:

| modes \(m\) | photons \(n\) | dark outcomes | scalar contrasts | normalized Jacobian bound |
|---:|---:|---:|---:|---:|
| 3 | 3 | 3 | 6 | \(3\) |
| 4 | 4 | 6 | 12 | \(2\) |
| 5 | 5 | 10 | 20 | \(5/3\) |
| 6 | 6 | 15 | 30 | \(3/2\) |
| 8 | 8 | 28 | 56 | \(4/3\) |

All outcomes are collected in parallel under four global settings,
\(+\epsilon R,-\epsilon R,+\epsilon T,-\epsilon T\).  “Minimal” here means
the number of selected complex outcomes and scalar first-order contrasts
meets the tangent-dimension lower bound.  It does not mean minimum shots,
minimum optical depth, or globally optimal Fisher information.

### 7. Conditioning improves while rates deteriorate

For \(n=m\), the normalized cyclic inverse has

\[
\kappa\leq\frac{m}{m-2},
\]

which approaches one as \(m\) grows.  However, the common squared amplitude
normalization entering every selected \((m-1,1)\) gradient is

\[
\alpha^2=m^{2-m}.
\]

It equals \(1/3,1/16,1/125,1/1296\) for \(m=3,4,5,6\), respectively.
The actual gradient entries carry additional factors \(m-1\) or \(1\).
With the unnormalized dense real probe the leading probe-only probability
scales as \(\epsilon^2m^{4-m}\); after normalizing that probe by its operator
norm \(m-1\), it scales asymptotically as \(\epsilon^2m^{2-m}\).
Consequently the algebraic problem becomes better conditioned while the raw
signals become rarer and the cat state becomes harder to prepare.  This
predicts that the first useful demonstrations will be at \(m=3\) or \(4\),
not at large \(m\).

### 8. Finite-probe extrapolation

Because a \(+\epsilon/-\epsilon\) difference is odd in the probe angle,
the contrast divided by \(4\epsilon\) has a leading finite-probe bias of
order \(\epsilon^2\) under the analytic ideal model.  Halving \(\epsilon\)
should reduce that systematic bias by approximately a factor of four until
shot noise or background dominates.  A multi-angle fit is therefore both a
bias-control method and a falsification check.

## Internal-error interpretation

If an error \(H_\ell\) occurs inside a layered circuit and \(W_\ell\) is the
ideal circuit after that layer, the reconstructed output-equivalent
generator is

\[
H_{\mathrm{eff}}
=\sum_\ell \delta_\ell W_\ell H_\ell W_\ell^\dagger
\]

to first order.  This predicts how a known component fault changes its
dark-event fingerprint when the surrounding circuit is reconfigured.
One configuration generally cannot localize the faulty layer: different
internal errors may have the same \(H_{\mathrm{eff}}\).  Several known
reconfigurations can turn fault localization into a second linear inverse
problem.

## Strongest near-term experiment

The cleanest test is \(m=n=4\):

- prepare a phase-stable four-mode four-photon cat;
- implement \(F_4\);
- collect six specified dark outcomes in each of four signed-probe settings;
- verify a rank-twelve local Jacobian;
- inject one known two-mode coherent error and test its two-event
  \({3:1}\) signed-contrast fingerprint;
- test the antipodal raw quadrature-gain ratio \(1/4\);
- repeat at several probe angles to verify the \(O(\epsilon^2)\) extrapolation.

Success would demonstrate local reconstruction of all twelve off-diagonal
\(SU(4)\) directions from dimension-minimal dark-event differentials.
Failure would be scientifically useful if it can be assigned to cat
dephasing, partial distinguishability, loss, detector background, or probe
miscalibration by independent controls.
