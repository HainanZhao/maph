# Proposed thesis outline

Date: 2026-07-26

## Scope assumption

This outline targets a master's thesis in mathematical or theoretical
physics.  At undergraduate level it is more than sufficient if the core
proofs survive review.  At PhD level it is one prospective chapter, not
a complete dissertation.

## Working title

**Beyond cyclic suppression: exact cancellation mechanisms in
many-boson Fourier interference**

## Proposed central claim

Dark transitions in Fourier multiports should not be divided only into
“symmetry predicted” and “accidental.”  They admit a finer hierarchy:

1. cyclic selection-rule zeros;
2. lower-dimensional zeros obtained by collapse to two effective support
   types;
3. nested orthogonal-polynomial cancellations among multiple path
   sectors;
4. any residue not captured by the first three mechanisms.

The thesis develops exact certificates for this hierarchy, proves a
closed amplitude formula for one infinite non-periodic family, and tests
how far the hierarchy explains finite four-mode data.

This claim is intentionally weaker than a complete classification of
all Fourier zeros.  It is also more meaningful than calling every
unpredicted zero “accidental.”

## Research questions

### RQ1 — exact detection

How can a many-boson Fourier amplitude be certified as zero using only
integer arithmetic?

Current answer: phase histograms and cyclotomic divisibility; complete
for the evaluation step at prime-power mode counts.

### RQ2 — mechanism

Which zeros are predicted by cyclic symmetry, which reduce to a
two-type transition, and which require a multi-sector coefficient
identity?

Current answer: complete for the three \(m=N=4\) pilot families; a
finite census exists through \(N=9\).

### RQ3 — infinite families

Can a non-periodic, multitype family be evaluated for all photon
numbers?

Current answer:

\[
(0,a,2a,a)\longrightarrow(0,a,2a,a)
\]

has coefficient

\[
\begin{cases}
0,&a\text{ odd},\\
(-1)^{a/2}\binom{2a}{a}\binom{a}{a/2},&a\text{ even}.
\end{cases}
\]

The proof uses nested Krawtchouk duality.

### RQ4 — physical distinction

Do different cancellation mechanisms respond differently to structured
phase errors or partial distinguishability?

Current answer: open.  Generic robustness is already known in the
literature, so only a mechanism-dependent result would count as a new
contribution.

## Proposed chapters

### 1. Physical background

- Hong--Ou--Mandel interference;
- Fourier multiports and Fock-state transitions;
- permanents and boson sampling;
- why exact zeros are useful for certification.

### 2. Known suppression laws

- Fourier cyclic rule;
- permutation-symmetric framework;
- extended two-mode HOM and central nodal lines;
- precise statement of the residual non-periodic problem;
- literature and novelty audit.

### 3. Exact arithmetic framework

- phase histograms;
- cyclotomic-polynomial criterion;
- prime-power fiber balance;
- dynamic programming and independent validation;
- equivalence operations and canonical representatives.

### 4. Four-mode mechanism hierarchy

- complete \(N=4\) pilot classification;
- embedded two-type families R1 and R2;
- support-type filter;
- exact census for larger photon numbers;
- limitations of the filter.

### 5. Nested Krawtchouk cancellation

- generating-function representation;
- Theorems T1 and T2;
- interpretation of sector pairing;
- two-parameter reflection family;
- attack on Conjecture T3.

### 6. Larger devices and physical consequences

- lifting \(F_d\) zeros to \(F_m\) for \(d\mid m\);
- examples in \(F_8,F_{12},F_{16}\);
- mechanism-sensitive perturbations if a nontrivial result is found.

### 7. Conclusions and open problems

- what the hierarchy explains;
- what remains genuinely unclassified;
- relation to integral Krawtchouk zeros;
- possible experimental tests.

## Success levels

### Minimum defensible thesis

- independent literature audit;
- fully checked proofs of the cyclotomic criterion and T1/T2;
- reproducible exact code;
- correct separation of the pilot families;
- honest discussion of novelty and limitations.

### Strong master's thesis

Minimum thesis plus one of:

- proof of Conjecture T3;
- a second non-equivalent multitype infinite family;
- a theorem quantifying the fraction explained by the mechanism
  hierarchy in a growing regime;
- a mechanism-dependent robustness theorem.

### Paper threshold

Literature novelty must be confirmed, and at least one result must go
beyond a single isolated closed-form family.  The most credible package
is T1/T2, the lifting theorem, and either Conjecture T3 or a second
structural family.

### Stretch goal

A complete necessary-and-sufficient classification for all \(F_4\)
occupations.  This is not promised because even embedded two-mode cases
touch difficult questions about integral zeros of Krawtchouk
polynomials.

## Four immediate research sprints

### Sprint A — novelty and correctness

1. Read the full 2018 detailed symmetry paper and the 2026 symmetric
   \(SU(N)\) paper theorem by theorem.
2. Search citations for later work on non-periodic Fourier inputs.
3. Have the T1/T2 proof reconstructed independently.

### Sprint B — multitype classification

1. Formalize support-type reduction.
2. Reclassify residual families through \(N=11\).
3. Identify common affine or reflection patterns.

### Sprint C — Conjecture T3

1. Express \(C_{a,b}\) as a Hahn/Krawtchouk-type value.
2. derive divisibility and sign constraints;
3. search much larger rectangles with exact recurrence;
4. prove zero exclusion in at least one region, such as \(b<2a\) or
   \(b>2a\).

### Sprint D — physical discriminator

1. Choose a unitary-preserving perturbation of the Fourier network.
2. Compare leading leakage coefficients for cyclic, two-type, and
   nested cancellations.
3. Determine whether the difference is experimentally observable.

## Current verdict

The project has advanced from a thesis proposal to a viable core
chapter.  It is not yet a complete thesis or a submission-ready paper.
The main mathematical result is exact and infinite; the remaining
decisive issue is whether it sits inside an existing theorem and whether
it can be extended to a broader structural statement.
