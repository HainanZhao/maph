# Cycle 061 — generic Engine-C W3 contract

**Frozen:** `2026-07-30T06:34:18Z`  
**Claim tag:** `PREREGISTERED_CONTRACT`

## Pilot objects

The new-case gate is the first polynomial-sorted \(e\in\{2,4\}\)
packet field:

```text
x^8 + 10*x^6 + 14*x^4 - 20*x^2 + 4
```

with member occurrences RQ-001280 and RQ-001297 over
\(\mathbb Q(\sqrt{35})\).  The exact linear-reinduction bases are
\(\mathbb Q(\sqrt{-10})\) and \(\mathbb Q(\sqrt{-14})\), and both
character fields have \(e=2\).

The regression anchor is the already proved primitive Engine-C packet
from Paper II.  A generic component is accepted only if its result
agrees with the anchor's banked exact output without importing the
answer as a constant.

## Component gates

### C61 — exact character selection

Input is limited to the real primitive ray datum, the real packet
field, one certified imaginary quadratic base, and the corresponding
absolute character field.  The implementation must:

1. factor the character field over the imaginary base;
2. recover the relative conductor and ray subgroup with
   `rnfconductor`;
3. enumerate every compatible ray character with `bnrchar`;
4. retain the exhaustive inverse pair of order four;
5. compare exact `lfunan` coefficient vectors against the source ray
   character;
6. emit the least coefficient index at which the candidate set is
   injectively labeled.

No numerical character recognition or preselected CM character is
allowed.

### C62 — analytic target and unit orbit

The selected character must pass the exact Stark scope predicates,
including its finite conductor factorization, \(w_k\),
\(e=|\mu(E)|\), and \(|S|\ge3\).  The analytic target is an Arb ball,
never a point.  Scaling uses the banked exact factor \(e/2\).
Logarithmic lattice inversion is performed in
\(\mathcal O_E^\times/\mu(E)\), and promotion requires one isolated
integral orbit.  An unproved or unavailable analytic evaluator is a
named halt, not a float substitution.

### C63 — exact packet bridge

The isolated orbit must be embedded into a common certified normal
closure.  Exact identities must map its positive CM norms to the real
packet roots, with embeddings ordered by the selected exact Artin
action.  Field isomorphism or equality of unlabeled polynomials is
insufficient.

### C64/C65 — anchor and new-case gates

The generic route first replays the anchor.  It then runs independently
on the \(\mathbb Q(\sqrt{35})\) closure.  Both member moduli require
separate ray-class/packet transport.  Promotion requires:

- exact character selection;
- applicable Stark theorem;
- Arb unit-orbit isolation;
- exact Artin-labeled bridge;
- replayable per-member certificate.

Any missing component leaves the case
`BLOCKED_MISSING_GENERIC_W3`; any disagreement is `HALT`.

## Frozen sources

- Cycle-060 boundary:
  `529358b90decf0026a82d87d8db31afa28548897c61428999104fd69ce18c6e6`
- General-\(e\) theorem:
  `1067e3cd00cbbb5a33c55b698353a3554d991090f6c4e4997e8d5ebebdf68233`
- Complete geometry transcript:
  `0ab3c647d9de69d2cc347a6846298eca30ea3f46adc60270de4f6b67d6f66278`
- Exact \(e\)-inventory:
  `a53be7591753b11fecdad2d96dca4479b99bbfaf732982fc1cf17dcf0ac5ef9b`

