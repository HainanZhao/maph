# SIC--Stark research program

## Objective

Determine whether the Shintani--Faddeev construction can be converted into
an unconditional existence theorem for Weyl--Heisenberg covariant symmetric
informationally complete measurements (SICs), first for an infinite family of
dimensions and ultimately in every finite dimension.

This document is a research ledger, not a claim that Zauner's conjecture has
been solved.

The current canonical-family reductions are recorded in
`docs/sic-stark-sprint1.md` and `docs/sic-stark-cycle2.md`.

## Mathematical specification

For an integer \(d\geq2\), a SIC is a set of \(d^2\) unit vectors
\(\{\psi_j\}\subset\mathbb C^d\), considered up to phase, such that

\[
  |\langle\psi_j,\psi_k\rangle|^2=\frac1{d+1}
  \qquad(j\ne k).
\]

Let

\[
  X|j\rangle=|j+1\bmod d\rangle,\qquad
  Z|j\rangle=\omega^j|j\rangle,\qquad
  \omega=e^{2\pi i/d},
\]

and choose displacement operators

\[
  D_{p,q}=\tau^{pq}X^pZ^q,\qquad \tau=-e^{\pi i/d}.
\]

A unit vector \(\psi\) is a Weyl--Heisenberg SIC fiducial exactly when

\[
  |\langle\psi,D_{p,q}\psi\rangle|^2=\frac1{d+1}
\]

for every nonzero \((p,q)\in(\mathbb Z/d\mathbb Z)^2\).  Its displacement
orbit then supplies the \(d^2\) SIC lines.  These equations are the first
executable interface for any candidate produced by the number-theoretic
construction.

## Current external result and bottlenecks

Appleby, Flammia, and Kopp give a proposed construction in every dimension
\(d>3\) from real-multiplication values of the Shintani--Faddeev modular
cocycle.  Their main all-dimensions conclusion is conditional on:

1. the order-one abelian Stark conjecture for real quadratic fields; and
2. a special-value identity for the Shintani--Faddeev modular cocycle.

In their construction the first input controls the required Galois
relationship, while the second proves idempotency of the presumptive
fiducial projector.  Therefore the first project target is not the full
banner conjecture but the special-value/idempotency identity, preferably on
an infinite family where its arithmetic simplifies.

Primary references:

- M. Appleby, S. T. Flammia, and G. S. Kopp, *A Constructive Approach to
  Zauner's Conjecture via the Stark Conjectures*,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970).
- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  q-Pochhammer ratios*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- I. Bengtsson and G. McConnell, *How Stark units enter SIC overlaps*,
  [arXiv:2606.23535](https://arxiv.org/abs/2606.23535).

## Claim ledger

### Proved or directly checkable here

- The nonidentity displacement-overlap equations above are equivalent to
  the equiangularity of a Weyl--Heisenberg orbit.
- The full displacement orbit of any normalized vector has frame operator
  \(dI\).  Tightness alone therefore does not establish the SIC condition.
- `src/sic.py` numerically verifies the standard tetrahedral fiducial in
  \(d=2\) and Hesse fiducial in \(d=3\), with independent checks of the
  equiangular and frame-operator residuals.

### Results imported from cited work

- There is extensive exact and numerical evidence for SICs across many
  dimensions.
- The 2025 ghost-SIC construction is conditional on the two inputs listed
  above.
- The 2026 overlap-unit calculations provide further evidence compatible
  with the modular-cocycle and Stark-unit mechanism.

### Not established

- No unconditional construction in every dimension is known here.
- No new case of the Stark conjecture or special-value identity has yet
  been proved here.
- Floating-point residuals are diagnostics, not exact certificates.

## Work packages

### WP1: Reproduce the construction

1. Pin the precise definitions and theorem numbering from the source
   manuscripts.
2. Reproduce low-dimensional ghost-SIC values independently.
3. Convert each candidate projector or fiducial into the displacement
   equations implemented in `src/sic.py`.
4. Record conventions explicitly; phase and Galois-conjugation mismatches
   are a major source of false failures.

Exit criterion: independent agreement with published exact examples in at
least three dimensions \(d>3\).

### WP2: Isolate the idempotency identity

1. Express the candidate projector in the displacement basis.
2. Reduce \(P^2=P\) to orbit sums of cocycle special values.
3. Quotient these sums by Clifford, Galois, and complex-conjugation
   symmetries.
4. Identify the smallest generating family of identities.

Exit criterion: a finite symbolic specification whose truth implies
idempotency for a stated family of dimensions.

### WP3: Search for an infinite family

Rank dimension families by arithmetic simplicity of
\(\Delta=(d+1)(d-3)\), conductor, ray class group, and Zauner orbit
structure.  Test whether the cocycle identity reduces to known functional
equations of q-Pochhammer ratios, double-sine functions, or the quantum
dilogarithm.

Exit criterion: either a proof for an infinite family or a rigorously
documented obstruction showing why the chosen family does not simplify.

### WP4: Exact and formal certification

Replace floating-point complex values by algebraic-number representations,
interval enclosures, or exact minimal-polynomial certificates.  Keep
discovery code separate from the checker.  A final computational theorem
must ship with a small deterministic verifier and immutable certificate
data.

## Immediate next actions

1. Obtain and archive the exact source version of arXiv:2501.03970 used for
   the reconstruction.
2. Extract the definitions of the ghost projector, the two conditional
   conjectures, and the precise idempotency theorem into a notation table.
3. Select the smallest published \(d>3\) example and reproduce it without
   calling the authors' implementation.
4. Extend `src/sic.py` with exact cyclotomic arithmetic only after the
   required coefficient field and conventions are fixed.

## Reproducibility

Run the current baseline with:

```bash
python3 -m unittest tests.test_sic -v
python3 scripts/verify_sic_fiducials.py --dimension 2
python3 scripts/verify_sic_fiducials.py --dimension 3 --show-residuals
```
