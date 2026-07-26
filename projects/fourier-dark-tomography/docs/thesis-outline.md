# Proposed thesis outline

Date: 2026-07-26

## Scope assumption

This outline targets a master's thesis in mathematical or theoretical
physics.  At undergraduate level it is more than sufficient if the core
proofs survive review.  At PhD level it is one prospective chapter, not
a complete dissertation.

## Working title

**The reciprocity closure of suppression laws in four-mode Fourier
interferometers**

## Proposed central claim

Dark transitions in Fourier multiports should not be divided only into
“symmetry predicted” and “accidental.”  Elementary suppression laws
must first be closed under exact histogram-preserving reciprocity.  The
current hierarchy is:

1. cyclic selection-rule zeros;
2. reciprocity images of cyclic zeros, including the former T1 family;
3. lower-dimensional zeros obtained by collapse to two effective support
   types;
4. residual arithmetic roots not captured by this closure.

The thesis develops exact certificates for this hierarchy, proves a
phase-histogram reciprocity theorem and a closed amplitude formula, and
tests how far their closure explains finite four-mode data.

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

Which zeros are predicted directly by cyclic symmetry, which become
cyclic after histogram reciprocity, which reduce to a two-type
transition, and which remain unexplained?

Current answer: the reciprocity theorem places the former multitype T1
pilot in the cyclic closure.  The exact orbit census through \(N=9\)
reduces 72 nominal residual families at \(N=9\) to 40 closure
components.

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

The coefficient proof uses nested Krawtchouk duality.  The reciprocity
theorem further identifies this zero line as a transport of a standard
cyclic-symmetry zero.

### RQ4 — physical distinction

Do different cancellation mechanisms respond differently to structured
phase errors or partial distinguishability?

Current answer: yes for calibrated output-mode unitary mixers.  Direct
cyclic, reciprocity-cyclic, and isolated-root examples have different
directional leakage exponents.  Every odd T1 member is exactly protected
along the \(Y_{13}\) axis.  Realistic partial-distinguishability and loss
floors remain open.

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

### 5. Krawtchouk reciprocity closure

- sectorwise histogram reciprocity;
- extension across the \(4\times4\) complex-Hadamard family;
- cyclic closure of the former T1 family;
- reciprocity-orbit census;
- boundary failure of the naive \(F_8\) analogue.

### 6. Reflection-plane arithmetic

- generating-function representation;
- Theorems T1 and T2;
- interpretation of sector pairing;
- two-parameter reflection family;
- attack on Conjecture T3.

### 7. Larger devices and physical consequences

- lifting \(F_d\) zeros to \(F_m\) for \(d\mid m\);
- examples in \(F_8,F_{12},F_{16}\);
- exact tangent formulas for appended two-mode mixers;
- directional quadratic/quartic/exact leakage fingerprints;
- the all-odd \(Y_{13}\) protected-axis theorem;
- realistic distinguishability and loss analysis.

### 8. Conclusions and open problems

- what the hierarchy explains;
- what remains genuinely unclassified;
- relation to integral Krawtchouk zeros;
- possible experimental tests.

## Success levels

### Minimum defensible thesis

- independent literature audit;
- fully checked proofs of the cyclotomic criterion, T1/T2, T4, and P1;
- reproducible exact code;
- correct separation of the pilot families;
- honest discussion of novelty and limitations.

### Strong master's thesis

Minimum thesis plus one of:

- proof of Conjecture T3;
- a classification of the new sectorwise reciprocity and the fraction
  of residual events it explains;
- a theorem quantifying the fraction explained by the mechanism
  hierarchy in a growing regime;
- a mechanism-dependent robustness theorem.

The present package meets the last criterion and partially meets the
reciprocity-classification criterion.  This assessment still depends on
independent proof review and novelty confirmation.

### Paper threshold

Literature novelty must be confirmed.  The most credible package is the
sectorwise histogram reciprocity, its cyclic-closure consequence, the
exact directional leakage theorem, and either realistic-noise analysis
or a proof of Conjecture T3.

### Stretch goal

A complete necessary-and-sufficient classification for all \(F_4\)
occupations.  This is not promised because even embedded two-mode cases
touch difficult questions about integral zeros of Krawtchouk
polynomials.

## Four immediate research sprints

### Sprint A — novelty and correctness

1. **Done at open-literature level:** compare the 2018 detailed
   symmetry paper, the 2026 symmetric \(SU(N)\) paper, and later work on
   non-periodic Fourier inputs.
2. **Done:** identify T1's arithmetic core as a known central
   Krawtchouk/parity mechanism.
3. **Next:** confirm the absence of the T3 completeness theorem through
   MathSciNet or Zentralblatt access before making a novelty claim.

### Sprint B — multitype classification

1. **Partly done:** implement and apply the support-type filter;
   strengthen it to a formal reducibility definition.
2. **Done:** reclassify residual families through \(N=11\).
3. **Done for \(N=11\):** reduce 16 representatives to four reflection
   classes and classify their natural affine lines exactly.
4. **Done:** prove the hidden histogram identity directly and generalize
   it to an infinite sectorwise reciprocity theorem.
5. **Done through \(N=9\):** quotient the residual census by this
   reciprocity.
6. **Next:** extend the quotient with precomputed \(N=11\) families and
   find repeated affine factors at smaller particle numbers.

### Sprint C — Conjecture T3

1. **Done:** express \(C_{a,b}\) as an explicit central-binomial
   convolution and derive its Bessel generating function.
2. **Done:** derive a three-term recurrence and an exact formula on
   \(b=2a-1\).
3. **Done:** certify every \(b>0\) for \(a\leq1000\), using modular
   recurrence plus a rigorous positive-tail bound.
4. **Done in a non-sharp form:** prove \(C_{a,b}>0\) for
   \(a\geq3,\ b\geq4a-3\), with the two smaller cases handled
   separately.
5. **Next:** control the remaining linearly wide strip uniformly in
   \(a\), especially the oscillatory region below and just above
   \(b=2a\).
6. **Challenged:** the stronger irreducibility pattern is exactly
   certified through \(a=59\), but elementary Eisenstein and one-edge
   Newton-polygon routes show no traction.  Keep T3e secondary unless a
   new valuation structure appears.

### Sprint D — physical discriminator

1. **Done:** choose phase-programmable, unitary two-mode output mixers.
2. **Done:** derive exact leading leakage coefficients for direct
   cyclic, reciprocity-cyclic, and isolated-root examples.
3. **Done:** prove an exact \(Y_{13}\) null axis for every odd T1
   member.
4. **Next:** add partial distinguishability, mode-dependent loss, and
   reconstructed-unitary uncertainty to test experimental resolvability.

## Current verdict

The project has advanced from a thesis proposal to a coherent thesis
core.  It is not yet a submission-ready paper.  The strongest package
is now the phase-histogram reciprocity theorem, its reclassification of
the T1 line as transported cyclic suppression, and the
mechanism-sensitive leakage fingerprint with an exact protected axis.
The reflection-plane completeness conjecture remains a valuable
arithmetic chapter but is no longer the only route to success.  The
decisive next issues are reciprocity-orbit coverage, realistic noise
floors, and independent database-level novelty confirmation.
