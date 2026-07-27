# SIC--Stark research program

## Objective

Determine whether the Shintani--Faddeev construction can be converted into
an unconditional existence theorem for Weyl--Heisenberg covariant symmetric
informationally complete measurements (SICs), first for an infinite family of
dimensions and ultimately in every finite dimension.

This document is a research ledger, not a claim that Zauner's conjecture has
been solved.

The current canonical-family reductions are recorded in
`docs/sic-stark-sprint1.md` and the numbered cycle ledgers.  Cycles
15--18 give the current endpoint: TCC is rank one for one shifted Zak
matrix, equivalently one positive exterior-square scalar or one
parity-Hermitian fourth-moment saturation.

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
- In the canonical family \(Q_d=\langle1,1-d,1\rangle\), TCC is
  equivalent to rank one of an explicitly shifted finite RM Zak matrix.
- The complete rank-one system is equivalent to the single positive
  scalar

  \[
  \Delta_2(K)
  =\frac12\left[
  (\operatorname{Tr}K^\dagger K)^2
  -\operatorname{Tr}((K^\dagger K)^2)
  \right].
  \]

- Parity-Hermiticity rewrites the normalized ghost target as

  \[
  \operatorname{Tr}(PG)^4
  =(\operatorname{Tr}(PG)^2)^2.
  \]

- An exact full-rank parity-Hermitian countermodel shows that the
  Bos--Waldron equation \(\operatorname{Tr}G^4=1\) cannot be transferred
  from its ordinary-Hermitian unit-torus locus without an additional
  theorem.

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
- No known four-point Shintani--Faddeev identity evaluates the positive
  fourth moment above.

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

The preliminary reconstruction and reduction stages are complete.
Cycle 19 found a common factor in the first four-point experiment.  In
dimension four, all ghost minors follow from the single special value

\[
x+x^{-1}=\sqrt{3+\sqrt5},
\]

where

\[
x=\sqrt2\,
\frac{
S_2(\beta/4\mid\beta,1)S_2(1/4\mid\beta,1)}
{S_2((\beta+1)/4\mid\beta,1)},
\qquad
\beta=\frac{3+\sqrt5}{2}.
\]

Cycles 20--21 locate this quarter-period quotient at a ray-class
arithmetic boundary.  The modulus-four one-real-place ray group has
order two, matching the relative degree of the Stark invariant \(x^2\).
The cocycle value \(x\) is its square root and has relative degree four.
The separate modular phase modulus \(8\) is not the ray conductor.
Cycle 22 identifies the ray field explicitly as
\(K(\sqrt\phi)\), with relative discriminant \((4)\) and ramification
at the second real place, and rewrites the target Stark unit as
\(\phi+\sqrt\phi\).
Cycle 23 replaces direct double-sine evaluation by the quadratic
Artin factorization \(\zeta_L/\zeta_K\).  It proves \(D_L=400\) and
\(h_L=1\), and reduces the desired logarithm to the unit index of
\(\langle\sqrt\phi,\phi+\sqrt\phi\rangle\) and one normalization audit.
Cycle 24 closes both checks and proves dimension-four TCC exactly,
conditional only on the published principal-ghost formula and the
proved Shintani--Kopp Kronecker-limit theorem.
Ordinary double-sine shift and reflection identities have therefore
reached their natural boundary.  The immediate target is now the finite
class-field identification proving that this
invariant is the positive \(>1\) root of

\[
X^8-2X^6-2X^4-2X^2+1.
\]

This would make the bounded dimension-four theorem unconditional.  If
the calculation itself requires unproved Stark algebraicity, the honest
endpoint is instead a conditional dimension-four theorem with one
explicit arithmetic hypothesis.

The general remaining problem is the following precise analytic theorem.

For the canonical Shintani--Faddeev RM ghost \(G_d\), prove

\[
\boxed{
\operatorname{Tr}(P G_d)^4
=\bigl(\operatorname{Tr}(P G_d)^2\bigr)^2.
}
\]

Equivalent acceptable forms are:

1. vanishing of the exterior square of the shifted RM Zak matrix;
2. factorization of its sheared partial-Fourier entries;
3. a four-point cocycle or boundary-integral identity evaluating the
   displayed trace;
4. a non-circular positive-metric theorem implying rank one.

Any proposed proof must retain the exceptional zero characteristic,
work in even dimensions and when \(3\mid d\), and reject the exact
countermodels in cycles 8, 9, 14, and 18.

## Reproducibility

Run the current baseline with:

```bash
python3 -m unittest tests.test_sic -v
python3 scripts/verify_sic_fiducials.py --dimension 2
python3 scripts/verify_sic_fiducials.py --dimension 3 --show-residuals
```
