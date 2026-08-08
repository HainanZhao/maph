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

## Next action

Derive a front-formation law for the detuning \(\lambda-1\), using the Cycle 2
inequality as a mandatory consistency condition, while independently auditing
the commensurability and kernel-blind no-go arguments for promotion.  The local
Turing branch is `RECOGNIZED` as existing literature, not a new bridge.  A demo
may only follow a genuine theorem or a clearly labelled numerical observation.
