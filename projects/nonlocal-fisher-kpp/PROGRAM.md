# PROGRAM: nonlocal Fisher--KPP pattern selection

## Objective and claim boundary

Study the one-dimensional top-hat nonlocal Fisher--KPP equation

\[
u_t=D u_{xx}+u(1-K*u),\qquad K(x)=\tfrac12\mathbf1_{[-1,1]},
\]

as a route to an explanatory theory of visible biological/ecological pattern
formation.  The external starting point is Needham--Billingham--Ladas--Meyer,
*European Journal of Applied Mathematics* 36 (2025), DOI
10.1017/S0956792524000688.  Its P1/P2 statements propose uniform or periodic
large-time behaviour behind a propagating front; they are not assumed proved.

No biological prediction, selection theorem, or critical-diffusivity claim is
made here.

## Cycle 1: finite-harmonic closure barrier

**Decision question.** Can a nonconstant finite Fourier ansatz on the
\(2\pi\)-periodic domain be an exact invariant nonlinear state space, and thus
support a finite-dimensional exact theory of pattern selection?

For \(v=u-1\), the nonlinear term is \(-v(K*v)\), with multiplier
\(\widehat K(n)=\sin(n)/n\) for every nonzero integer mode \(n\).  A largest
positive support mode \(N\) generates mode \(2N\) with coefficient
\(-\widehat K(N)a_N^2\).

**Advance condition.** Prove the no-go theorem, including cancellation.
**Falsifier.** Exhibit a nonconstant finite support whose vector field stays
inside it.  **Verifier.** Extract the \(2N\) coefficient and audit its unique
contributing pair.  **Stop criterion.** The result is only a barrier to a
finite-mode proof architecture, never a proof of P1/P2.

## Selection exclusion map

| Candidate | Cycle-1 disposition |
| --- | --- |
| Exact 3D bootstrap-percolation threshold | Not selected: the main fixed-dimension sharp-threshold program is already addressed in 2009/2012 work. |
| Generic active matter | Not selected: no smallest exact falsifier. |
| Sandpile exponents | Deferred: high animation value, no near-term exact mechanism. |
| Nonlocal Fisher--KPP | Selected: published P1/P2 target, exact multiplier, falsifiable first gate, and a future population-pattern explanation if theory is earned. |

## Cycle 2: commensurate-window detuning

**Decision question.** What exact finite-diffusion constraint replaces the
false intuition that small-diffusion humps may simply sit at the interaction
radius?

`CONJECTURED`, pending independent proof and overlap audits: if a positive
periodic steady state has period \(\lambda\) and \(2=m\lambda\), the top-hat
window averages exactly \(m\) periods and the state must be \(u\equiv1\).
The live derivation strengthens this to a contrast--detuning inequality of the
form

\[
|2-m\lambda|\ge
\frac{4D\,\operatorname{osc}(\log u)}{(\max u)\lambda^2}.
\]

**Falsifier.** A positive nonconstant commensurate stationary state, or a
violation of the quantitative inequality. **Verifier.** Residual-window
decomposition plus an independent Fourier-multiplier audit. **Claim boundary.**
This restricts admissible steady wavelengths; it does not select the wake or
prove P1/P2.

The same identity for radius \(R\) yields a second `CONJECTURED` structural
boundary: linearization at \(u=0\) is \(D\partial_{xx}+1\) for every \(R\),
whereas exact forbidden wake periods depend on \(R\).  Therefore no universal
wake-selection rule using only pulled-front linearization at \(u=0\) can be
correct across the top-hat-radius family.  Kernel information must enter
through the populated state or nonlinear competition memory.

The exact logarithmic level law further gives a Gate-2 obstruction.  Two
positive profiles can have the same complete local germ at a prospective hump
level but different top-hat window masses, hence different instantaneous level
velocities.  A position/local-shape-only event map is therefore killed; the
minimum instantaneous state must retain the competition trace \(K*u\), whose
own evolution is still spatially nonlocal.

The surviving small-\(D\) state is the scaled window profile \(v\) with
\(\lambda=1+\sqrt D\,L\).  The translated boundary-layer equation is

\[
v''+v\left(1-M+\tfrac12\int_{\xi-L}^{\xi+L}v\right)=0,
\qquad M=\int_{\mathbb R}v.
\]

`CONJECTURED`, conditional on existence: its exact integrated identity is
\(Q_L=2M(M-1)\), forcing \(1<M<2\), and an exponential tail has
\(\sigma^2=M-1\). The 2025 publisher's PDF has now been audited: its
Equation (143) omits the square root required by direct substitution into
Equation (137). This source correction does not select a wavelength.

Along a ray moving at \(2\sqrt D\), the exact completed-square identity is

\[
\frac d{dt}\log u
=D(\log u)_{xx}
+D\bigl((\log u)_x+D^{-1/2}\bigr)^2-K*u.
\]

It isolates the nonlinear competition delay from an explicit slope/curvature
defect and is the current front-matching interface.

`PROVED` for a frozen competition barrier: a zero-energy scattering-length
closure uses the wrong spectral scale. It was falsified after its numerical
fixed point had converged: the pulled front is sampled on a ballistic ray and
therefore probes exponential spatial weight one. For a frozen inner-scale
competition profile \(C\), the correct collective object is instead the
positive solution of

\[
H''+2H'-CH=0,
\]

or equivalently the generalized eigenfunction
\(\phi=e^xH\) satisfying \(\phi''+(1-C)\phi=2\phi\). The exact conserved
quantity for \(q_t=q_{xx}+(1-C)q\) is

\[
e^{-2t}\int \phi q.
\]

The frozen-barrier critical-ray theorem identifies a ballistic transmission
factor as the surviving candidate memory. It also exposes the next
obstruction: the factor acts on the incoming
exponentially small seed, so it is not yet a closed function of the previous
hump alone.

`PROVED` for the full nonlinear equation: the critical exponential moments

\[
\mathcal E_\pm(t)=e^{-2t}\int e^{\pm x/\sqrt D}u(x,t)\,dx
\]

are strictly decreasing, with an explicit positive top-hat pair-interaction
as their dissipation. If a finite-moment state repeats after time $T$ shifted
by $\lambda$, then

\[
\frac{\lambda}{\sqrt D}
=2T-\int_0^T\langle K*u\rangle_{+,t}\,dt,
\qquad \frac\lambda T<2\sqrt D.
\]

Thus an exact localized shedding packet cannot itself repeat at the pulled
speed. The leading tail and deposited wake must be separated, and the tilted
competition integral is the exact phase-delay quantity to control.

## Terminal gate reached

The campaign's permitted structural-no-go outcome is now met by sealed artifact
`cycle-2-b004-critical-exponential-moment-v1`. It rules out the concrete broad
class of nonzero finite-critical-moment states that repeat at or above the
pulled speed, and it identifies the missing ingredient exactly: a separate
critical leading tail together with the tilted competition-delay integral.

This does **not** prove P1/P2, a selected wake wavelength, nonlinear seed
universality, or a thermodynamic/biological prediction. Those remain open
research directions rather than hidden consequences of the terminal theorem.

## Optional continuation beyond the completed gate

Evaluate or bound the exact tilted competition delay over one formation cycle
after separating the nonintegrable critical leading tail from the localized
hump/wake state. Determine whether the incoming generalized moment becomes a
universal function of the established boundary-layer hump; two full nonlinear
histories with the same hump state but different leading delay kill the
one-step map. Any surviving map must also satisfy the mass/tail and detuning
identities. A demo may only follow a genuine theorem or a clearly labelled
numerical observation.
