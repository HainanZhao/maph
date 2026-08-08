# Goal: explain wavelength selection behind nonlocal Fisher--KPP fronts

**Author:** Hainan Zhao  
**Scope:** the one-dimensional top-hat nonlocal Fisher--KPP equation

\[
u_t=D u_{xx}+u(1-K*u),\qquad
K(x)=\tfrac12\mathbf1_{[-1,1]}(x),\qquad D>0.
\]

This is a user-owned goal file. Do not edit, rename, or delete it without a
new explicit instruction from the user.

## Objective and claim boundary

Develop a rigorous, bounded theory that explains one visible old phenomenon:
why a front can leave approximately regularly spaced population humps behind
it in a nonlocal competition model. The target is a mathematically controlled
selection mechanism—such as a harmonic cascade, a spike-spacing map, or a
different invariant object—not an attractive simulation alone.

The campaign does **not** claim a biological forecast, a proof of the full
large-time P1/P2 program, a universal critical diffusivity, or a solution for
arbitrary kernels. It begins with the top-hat kernel on the line; periodic
problems are permitted only as explicitly derived auxiliary models.

## Starting evidence

- **RECOGNIZED:** Needham, Billingham, Ladas, and Meyer formulate P1/P2
  large-time uniform/periodic-behind-the-front scenarios for this model in
  *European Journal of Applied Mathematics* 36 (2025), DOI
  `10.1017/S0956792524000688`. Their proposed scenarios are not assumed
  proved here.
- **CONJECTURED:** the project’s Cycle 1 derivation says that a nonconstant
  finite Fourier support on the \(2\pi\)-periodic auxiliary problem is not an
  exact invariant nonlinear state space: its highest active mode generates a
  higher harmonic. The local exact audit is
  `proof/verify_fourier_support_barrier.py`; novelty and an independent proof
  audit remain open.

The barrier is a constraint on one proof architecture. It is not evidence for
or against P1/P2, and it does not rule out controlled infinite-dimensional
reductions.

## Workstreams

### Gate 1 — Controlled harmonic cascade

Seek a function space, normal form, or quantitative tail estimate in which
the Fourier cascade can be propagated without treating a finite truncation as
exact. The key invariant is a rigorously defined relation between the leading
unstable wavelength and the generated harmonic tail.

**Acceptance:** prove a theorem with explicit hypotheses, norm, time or
parameter range, and error bound that controls the cascade sufficiently to
derive a checkable wavelength-selection consequence or a rigorously bounded
failure of selection.

**Kill/escalate:** a counterexample to the proposed bound, or an unavoidable
resonance that destroys its invariant estimate, closes this mechanism. Record
the false step and exact example in the failure ledger, then proceed only with
a materially different state space or invariant.

### Gate 2 — Spike-spacing or front-to-pattern map

Derive a reduced map or geometric construction whose variables have a stated
approximation relation to solutions behind a front. It must explain how an
existing hump affects the location or stability of a subsequent hump.

**Acceptance:** prove the reduction for a defined asymptotic regime and show
that its spacing law is stable under a quantified perturbation of the full
equation. A theorem may establish a no-selection, multi-spacing, or
nonuniqueness result; it need not confirm a single preferred wavelength.

**Kill/escalate:** if the required front/hump decomposition cannot be made
uniform or two solutions with the same reduced state diverge at leading order,
record that obstruction and abandon this reduced state rather than repairing
it with unproved closure.

### Gate 3 — Falsification and structural alternatives

For each candidate explanation, construct its smallest direct verifier:
exact Fourier identities, comparison/energy inequalities, or a certified
finite-domain counterexample where applicable. In parallel, assess whether a
Lyapunov, monotonicity, or comparison principle supplies a more suitable
infinite-dimensional invariant than Fourier support.

**Acceptance:** either independently validate the hypotheses needed by Gate
1 or 2, or prove a no-go statement that identifies the exact lost property.

**Kill/escalate:** numerical agreement alone does not advance a candidate.
If no exact or certified verifier exists, retain the route as exploratory and
do not promote a selection claim.

## Verification and reproducibility

- Use only the repository labels `PROVED`, `CERTIFIED_NUMERICAL`,
  `RECOGNIZED`, `OBSERVED`, and `CONJECTURED` for material claims.
- A `PROVED` result requires a self-contained argument or a published theorem
  with hypotheses checked exactly in this run. A `CERTIFIED_NUMERICAL` result
  requires a rigorous enclosure and recorded margin. Simulations and visual
  patterns are `OBSERVED` unless independently certified.
- Pin kernel normalization, Fourier convention, domain, boundary condition,
  parameter regime, and all numerical discretizations before relying on a
  calculation. Keep conjectural exploration in `discovery/` and exact or
  certified work in `proof/`.
- Every promoted computation needs version-pinned, hash-recorded, one-command
  replay and, where the mechanism permits, an independent route. Preserve
  counterexamples and failed mechanisms by naming the false inference rather
  than silently changing the ansatz.
- Read primary literature and check hypotheses before any novelty claim.

## Public explanation and demo gate

An animation may illustrate the theorem only after a gate supplies a stated
mathematical relation between the animated quantity and the PDE. It must show
the regime and assumptions, distinguish exact consequence from simulation,
and label parameter sweeps as `OBSERVED`. It may explain ecological-style
pattern formation but must not be presented as a calibrated bacterial,
financial, or election model without a separate validated modelling bridge.

## Stop conditions and terminal outcomes

A workstream closes when it has either met its acceptance condition or reached
its stated proof-grade countermechanism. Failure of one workstream does not
end the project.

This campaign is complete only when at least one of the following is obtained:

1. a `PROVED` controlled selection or nonselection theorem for the specified
   top-hat model and regime;
2. a `PROVED` structural no-go theorem that rules out a concrete broad class
   of explanations and identifies the required new ingredient; or
3. a `CERTIFIED_NUMERICAL` countermechanism with rigorous error bounds,
   together with a precise theorem-level boundary on what it refutes.

An unbounded computation, a visually persuasive animation, a finite Fourier
truncation, a polished manuscript, or an observed periodic pattern does not
complete the goal. Any final result must state exactly what remains open about
P1/P2 and the full nonlocal Fisher--KPP equation.
