# Cycle 073 — B1 standalone theorem note

## Outcome

Track B1 is complete as a local-only four-page note:
`paper/quartic-stark-phase-note.tex` and its deterministic PDF.

`PROVED`: Roblot's real-place hypothesis (A1) gives an embedding
\(K\hookrightarrow\mathbb R\), hence
\(\mu(K)=\{\pm1\}\) and the Stark denominator is \(2\).

`PROVED`: in a certified cyclic-quartic Stark case,
\[
\frac{L'(0,\chi)}{c_\chi(\eta)}
=\chi(h)^{-1}\in\mu_4
\]
for the explicitly pinned left signed action
\(h\mathbin{\cdot}u=u^{h^{-1}}\).

`PROVED`: under Roblot's (A1)--(A3), the quartic orbit condition is
equivalent to the full rank-one Stark conjecture. The reverse
implication now displays:

1. even-component vanishing on the analytic and unit sides;
2. conjugate-pair determination followed by exact \(C_4\) Fourier
   inversion;
3. inheritance of the abelian square-root condition, including the
   \(-1\) representative through the abelian compositum with \(k(i)\).

`OBSERVED`: the five-control comparison remains only the
two-orientation numerical statement against certified \(L'\)-balls.
It is not a proof route and supplies no data section here.

## Contained convention correction

The first clarification note did not distinguish right exponentiation
from the left group-ring action. Exact reindexing gives
\[
c_\chi(u^a)=\chi(a)^{-1}c_\chi(u)
\]
for right exponentiation and
\[
c_\chi(a\mathbin{\cdot}u)=\chi(a)c_\chi(u)
\]
for \(a\mathbin{\cdot}u=u^{a^{-1}}\).

`CONTAINED_NOTATIONAL_CORRECTION`: inversion permutes the signed group,
so the \(\mu_4\)-membership theorem and existential
\(\chi(h)^{-1}\) formula are unchanged. The corrected source is
`docs/roblot-phase-clarification-correction-v2.md`.

## Replay and build

The proof audit checks all eight signed \(C_4\) actions, the signed
character image, exact Fourier orthogonality, even-character
cancellation, all required manuscript steps, citations, and the
no-circulation boundary:

```bash
python3 proof/audit_b1_note.py
```

The first independent PDF pair differed only in the pdfTeX trailer ID;
that failure is preserved in `artifacts/b1-note-audit-v1.json`. After
pinning the trailer ID and suppressing volatile PDF metadata, two
independent triple-pass builds were byte-identical:

- PDF SHA-256:
  `bed234c430e72946f30a4695a601e23eaa34e18ad8441cc838ffb6e0f53c02bc`;
- bytes: 212,995;
- warnings: zero;
- all four rendered pages visually checked.

## Boundary and next gate

The note is not authorized for submission, posting, or circulation
before B3 exists as its data section. Every outbound communication is
human-only.

B2 remains the next phase-theory item and must reconstruct exact Artin
transport before reading any analytic target. B3 remains independent
of B2 labels but cannot execute until its genuine population and Arb
weak-coefficient gates are banked.
