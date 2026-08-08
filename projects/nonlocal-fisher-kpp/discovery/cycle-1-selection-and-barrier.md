# Cycle 1 — finite-harmonic barrier

## Question → question the questioning → brainstorm

**Question.** Can a finite Fourier system exactly explain the periodic humps
conjectured behind the top-hat Fisher--KPP front?

**Question the questioning.** A finite truncation is not automatically an
invariant state space of a nonlinear PDE.  Test that before treating it as an
explanation.

**Brainstorm.** An entropy/Lyapunov route; finite-mode amplitude closure; a
harmonic-cascade barrier; and a small-diffusion spike-spacing map.  Cycle 1
selects the barrier because it has a smallest exact falsifier.

## Theorem (finite-harmonic closure barrier)

On \(\mathbb T=\mathbb R/(2\pi\mathbb Z)\), every nonconstant
trigonometric polynomial \(v\) leaves its original Fourier support under

\[
Dv_{xx}-K*v-v(K*v).
\]

### Proof

Write \(v=\sum_{|n|\le N}a_ne^{inx}\), with \(N>0\) maximal and
\(a_N\ne0\).  Since \(\pi\) is irrational, \(\sin N\ne0\).  The linear
terms do not create mode \(2N\).  In \(v(K*v)\), the only supported ordered
pair summing to \(2N\) is \((N,N)\).  Its coefficient is

\[
-a_N\frac{\sin N}{N}a_N\ne0,
\]

outside the original support.  Therefore no finite-dimensional nonconstant
Fourier-support space is invariant.

## Status and consequence

`CONJECTURED` for project purposes until an independent proof audit and a
targeted literature check establish whether this elementary barrier is already
standard.  The displayed derivation and
`proof/verify_fourier_support_barrier.py` are a first exact consistency check,
not a sealed research result.  Novelty is `UNASSESSED`.

This does not prove the P1/P2 selection conjectures.  It says an exact theory
must retain an infinite harmonic cascade, find a different invariant object,
or rigorously control an approximation.
