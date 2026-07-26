# Thesis stage 2: reciprocity closure and physical fingerprints

Date: 2026-07-26

## Executive change

The central thesis idea changed during this research cycle.

The earlier hierarchy treated the self-transition

\[
(0,a,2a,a)\longrightarrow(0,a,2a,a)
\]

as a candidate mechanism beyond cyclic suppression.  That interpretation
is false.  A new sectorwise Krawtchouk reciprocity theorem transports the
whole odd-\(a\) zero line to a standard cyclic-symmetry zero.

The stronger organizing principle is now:

> Apply elementary suppression laws, then close them under exact
> histogram-preserving transformations.  Only the residue outside this
> closure should be called unexplained.

The proposed title is:

> **The reciprocity closure of suppression laws in four-mode Fourier
> interferometers**

## Main proved results of this cycle

### 1. Sectorwise histogram reciprocity

Let \(d,N\geq0\), \(0\leq\alpha,s\leq d\), and
\(0\leq k,p\leq N\).  Define

\[
\mathcal H_{d,N}(\alpha,k;s,p)
=
\operatorname{hist}\bigl(
(\alpha,k,d-\alpha,N-k),
(s,p,d-s,N-p)
\bigr).
\]

Then

\[
\mathcal H(\alpha,k;s,p)
=\mathcal H(\alpha,p;s,k)
=\mathcal H(s,k;\alpha,p)
=\mathcal H(s,p;\alpha,k).
\]

The nontrivial partial exchange follows term by term from binary
Krawtchouk self-duality after the parity change of variables

\[
E=x_0+x_2,\quad T=x_0-x_2,\quad
S=x_1+x_3,\quad D=x_1-x_3.
\]

This is not, in general, a rotation, reflection, arbitrary mode
permutation, phase gauge, or global input/output exchange.

### 2. Robustness across the complex-Hadamard family

The same normalized-amplitude reciprocity holds polynomially for

\[
H(z)=
\begin{pmatrix}
1&1&1&1\\
1&z&-1&-z\\
1&-1&1&-1\\
1&-z&-1&z
\end{pmatrix}
\]

for arbitrary complex \(z\).  For \(|z|=1\), \(H(z)/2\) is unitary.
The theorem is special to the binary two-mode sectors of \(F_4\): the
naive \(F_8\) parity analogue is false.

### 3. Reclassification of the former T1 mechanism

Reciprocity and rotations identify the vanishing behavior of

\[
(0,a,2a,a)\to(0,a,2a,a)
\]

with

\[
(0,0,2a,2a)\to(a,a,a,a).
\]

The latter is caught directly by the cyclic rule exactly when \(a\) is
odd.  Thus T1/T2 is a reciprocity-cyclic family, not an irreducible new
suppression law.  The balance condition for applying reciprocity to the
larger reflection plane is precisely \(b=2a\), structurally explaining
the conjectured zero line.

### 4. Exact closure census

After rotations, reflections, input/output exchange, and reciprocity:

| photons | residual families | closure components | families reaching direct cyclic |
|---:|---:|---:|---:|
| 4 | 3 | 3 | 1 |
| 5 | 8 | 3 | 0 |
| 6 | 10 | 6 | 0 |
| 7 | 0 | 0 | 0 |
| 8 | 33 | 23 | 1 |
| 9 | 72 | 40 | 0 |

Reciprocity both explains some nominal residuals and merges many others,
but a substantial arithmetic residue remains.

### 5. Directional unitary-leakage fingerprints

For appended two-mode mixers, direct cyclic, reciprocity-cyclic, and
isolated-root examples have different directional leakage exponents:

| event class | \(X_{12}\) | \(Y_{12}\) | \(X_{13}\) | \(Y_{13}\) |
|---|---:|---:|---:|---:|
| direct cyclic | exact | exact | exact | exact |
| reciprocity-cyclic, \(a=1\) | quadratic | quadratic | quadratic | exact |
| isolated \(N=11\) | quadratic | quartic | quadratic | quadratic |

For every positive odd \(a\), the T1 event remains exactly dark along
the full \(Y_{13}\) rotation.  This is proved by reflection pairing, not
inferred from finite cases.

## Assumptions rejected

1. Failure of the direct cyclic rule does not imply a non-cyclic
   mechanism.
2. An infinite exact family is not generically more robust than an
   isolated arithmetic root.
3. Reciprocity-equivalent ideal zeros do not have identical laboratory
   leakage fingerprints unless the perturbation is transported too.
4. Extending finite irreducibility evidence is not automatically a
   promising proof strategy: simple Eisenstein and Newton-polygon
   patterns have not appeared.
5. The \(F_4\) reciprocity does not automatically generalize to
   \(F_{2^m}\).

## Status of the reflection-plane conjecture

The Bessel generating function, two exact recurrences, positive cone,
adjacent-diagonal formula, and arithmetic divisibility conditions remain
valid.  The zero conjecture is exactly certified for
\(a\leq1000\) and every positive \(b\).

The stronger polynomial irreducibility pattern is rigorously certified
through \(a=59\), with no counterexample.  However, direct
and shifted Eisenstein tests and simple one-edge Newton-polygon searches
have not exposed a uniform proof mechanism.  T3/T3e should remain an
important arithmetic chapter, but no longer the sole thesis bottleneck.

## Thesis and paper assessment

The project now has enough proved mathematics and reproducible
computation for a strong master's-thesis core:

- a new phase-resolved application of classical Krawtchouk duality;
- an infinite histogram reciprocity theorem;
- a nontrivial suppression-law closure and finite census;
- exact unitary-leakage predictions;
- a concrete four-photon experiment proposal.

A paper should wait for:

1. a broader database/expert novelty audit of sectorwise reciprocity;
2. partial-distinguishability, loss, and calibrated-unitary uncertainty
   in the leakage model;
3. either a more systematic reciprocity-orbit classification or a proof
   of the reflection-plane completeness conjecture.

## Immediate next work

1. Add distinguishability and loss floors to the four-axis experiment.
2. Formalize the closure as an equivalence relation and quotient the
   complete \(F_4\) census at larger particle numbers.
3. Search the remaining closure components for repeated affine
   quasipolynomial factors.
4. Seek a circuit-level explanation of sectorwise reciprocity from the
   Cooley--Tukey factorization of \(F_4\).
5. Continue T3e only when a structural prime or valuation pattern
   appears; do not replace proof strategy with an arbitrary larger
   cutoff.

## Reproduction

```text
python3 -m unittest discover -s tests -v
python3 scripts/analyze_reciprocity_census.py
python3 scripts/analyze_unitary_leakage.py
python3 scripts/certify_reflection_conjecture.py --a-limit 1000
python3 scripts/audit_reflection_irreducibility.py
python3 scripts/analyze_n11_affine.py
```

Detailed proofs and calculations are in:

- [`thesis-stage1.md`](thesis-stage1.md);
- [`agent-n11-direct-proof.md`](agent-n11-direct-proof.md);
- [`agent-unitary-leakage.md`](agent-unitary-leakage.md);
- [`agent-n11-findings.md`](agent-n11-findings.md).
