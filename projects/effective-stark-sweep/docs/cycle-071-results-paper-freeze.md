# Cycle 071 — results-paper referee freeze

The submission manuscript is frozen at
`paper/effective-stark-results.tex` and its compiled PDF.  The earlier
Markdown file is a research memorandum, not the submission source.

The parity bonus closed inside its one-cycle budget.  In the genuine
normal closure the two real-place inertia involutions are conjugate;
their quotient lies in the commutator and maps to the one-place sign
class.  Nontrivial differenced support therefore forces even
Shintani index.  This proof is included as the last new result.

The internal referee audit passed:

- seven displayed safe exponents agree with their promoted records;
- eight displayed height margins were recomputed and clear their
  printed integer lower bounds;
- every displayed polynomial, finite constant, and Artin label is
  tied to an exact case record;
- nine certificate hashes replay;
- the introduction says explicitly that “unconditional” is
  case-specific use of proved theorems, not the general real-quadratic
  Stark conjecture;
- the two historical-first statements remain restricted to the
  named, hash-frozen literature perimeter;
- every Engine-C use of Stark 1980 has its abelian imaginary base,
  exact \(e=|\mu(E)|\), and \(|S|\ge3\) global-unit condition audited;
- census populations, FRONTIER counts, and trends do not occur.

The audit caught one non-mathematical but referee-visible defect:
`engine-c-general-e-theory-v2.json` had omitted minus signs in its
specialization strings even though its general formulas and all
sealed tranche records had the correct signs.  Version 3 corrects the
strings.  No case tag or numerical certificate changed.

The primary freeze record is
`artifacts/results-paper-freeze-v2.json`.  Any manuscript edit after
this point requires rebuilding twice, rerunning
`scripts/audit_results_paper.py`, and issuing a new freeze hash.
The PDF was built independently in two temporary directories with
`SOURCE_DATE_EPOCH=1785411036`; the two outputs were byte-identical.

## Supersession

This freeze was superseded on 30 July 2026 by
`artifacts/results-paper-freeze-v3.json` after the external-referee
repair.  Version 2 remains preserved as the pre-repair checkpoint.
The v3 manuscript is fourteen pages, contains the explicit eight-item
theorem inventory, expands all three engine proofs, corrects the
\(\mathbb Q(\sqrt6)\) packet polynomial, and banks the genuine
446-case parity replay.  Its independent builds are byte-identical at
`SOURCE_DATE_EPOCH=1785414600`.

Freeze v3 was in turn superseded by
`artifacts/results-paper-freeze-v4.json`.  Version 4 adds the explicit
fixed-field step in the parity proof, makes index parity the ninth
inventory item, defines \(\infty_2\) as the negative-square-root
embedding (PARI's first real place), displays the closed universal
Engine-A product for \(X_A\), and promotes the banked general-\(e\)
Engine-C normalization/orientation result to a named tenth theorem
inventory item covering \(e=6,8,12\).  Independent builds are
byte-identical at `SOURCE_DATE_EPOCH=1785417387`.

Freeze v4 was superseded by
`artifacts/results-paper-freeze-v5.json` after the journal-facing
editorial pass. Version 5 removes internal verification tags from the
mathematical narrative, moves certificate paths and chronology to an
appendix, shortens the RQ-000458 process caveat, and places a
publisher-compatible AI-use declaration immediately before the
bibliography. No theorem, formula, constant, polynomial, or margin
changed. Independent builds are byte-identical at
`SOURCE_DATE_EPOCH=1785420000`.
