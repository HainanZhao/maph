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
