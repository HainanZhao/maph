# Cycles 072--074 preregistration: quartic weak/Stark phase note

Frozen: 2026-07-31 UTC, before drafting the standalone B1 manuscript.

## Objective

Write a short, local-only note containing exactly two principal
theorems.

1. In a cyclic-quartic case satisfying Roblot's hypotheses (A1)--(A3)
   for which the rank-one Stark conjecture is already proved, the weak
   solution \(\eta\) satisfies
   \[
   \frac{L'_{K/k,S}(0,\chi)}{c_\chi(\eta)}
   =\chi(h)^{-1}\in\mu_4
   \]
   for a signed Galois action \(h\in\{\pm\gamma^j:0\leq j<4\}\).
2. Under the same Roblot hypotheses, quartic phase quantization is
   equivalent to the full rank-one Stark conjecture.

No submission, posting, email, or other circulation is authorized.
The note may not be submitted before the B3 counterexample screen
exists as its data section. All outbound communication is human-only.

## Frozen conventions

- \(G=\langle\gamma\rangle\simeq C_4\), \(\tau=\gamma^2\), and
  \(\chi(\gamma)=i\).
- \(S\supseteq S(K/k)\) contains a distinguished real place \(v\)
  splitting completely in \(K/k\), and \(w\mid v\) is fixed.
- Right Galois actions and the Fourier coefficient are
  \[
  c_\psi(u)=\frac12\sum_{g\in G}\psi(g)\log|u^g|_w.
  \]
- Roblot's (A1) supplies a real embedding of \(K\). The note must prove,
  rather than assume, that this forces \(\mu(K)=\{\pm1\}\), so the
  Stark denominator is \(e=2\).
- A signed action \(h=s\gamma^j\), \(s\in\{\pm1\}\), acts on a unit by
  \(u^h=(u^{\gamma^j})^s\) and on the coefficient by
  \(\chi(h)=s\chi(\gamma)^j\).

## Mandatory reverse-implication steps

The implication from quantization to Stark must display all three
steps separately.

1. **Even-component vanishing.** For the trivial and quadratic
   characters, both \(c_\nu(\eta)\) and
   \(L'_{K/k,S}(0,\nu)\) vanish.
2. **Conjugate-pair determination.** The chosen \(\chi\)-identity and
   complex conjugation give the \(\bar\chi\)-identity; Fourier inversion
   then gives the complete logarithmic Stark identity.
3. **Abelian condition.** If \(\epsilon=\pm\eta^{\gamma^j}\), then the
   plus sign is inherited from \(K(\sqrt\eta)/k\). For the minus sign,
   \(K(\sqrt{-\eta^{\gamma^j}})\) is contained in the compositum of the
   abelian extensions \(K(\sqrt\eta)/k\) and \(K(i)/k\), so it is
   abelian over \(k\).

## Primary-source map

- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--417,
  DOI `10.2140/pjm.2013.266.391`.
- assumptions (A1)--(A3): journal pp. 392--393;
- index-solution determinant identity: Proposition 4.1;
- comparison of solutions: Corollary 4.5;
- quartic existence, uniqueness up to \(\pm G\), absolute-value
  identity, even-component vanishing, and abelian square-root
  extension: Theorem 6.1 and its proof, journal pp. 404--405.

## Epistemic and failure rules

- The two theorem statements may be tagged `PROVED` only after each
  cited hypothesis and every propagation step above appears explicitly.
- The five-control phase comparison remains `OBSERVED` against
  certified \(L'\)-balls; it is not a proof route.
- Any failure of the root-of-unity rider, signed-action covariance,
  even-character vanishing, conjugate identity, Fourier inversion, or
  abelian-extension inheritance halts B1 and narrows the theorem.
- A disagreement with the published v1.4 correction record is a
  containment event and halts the note.

## Deliverables and replay gate

- `paper/quartic-stark-phase-note.tex` and compiled PDF;
- a version-pinned source-and-proof audit in `proof/`;
- a cycle checkpoint and manifest entries;
- a regression test checking the rider, three propagation steps,
  theorem tags, citations, and no-circulation boundary.
