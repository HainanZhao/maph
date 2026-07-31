# Cycle 080 — Track A2 wording and bibliography audit

Recorded: 31 July 2026 UTC.

## Outcome

`CONTAINED_BIBLIOGRAPHIC_CORRECTION`: the historical-scope
back-reference, both companion-paper anchor citations, and the
Tate IV.5.4 / Arakawa / Roblot scope discussion were already present
in the published v1.3 source. The Tangedal--Young entry was not
correct: it printed pages 1022--1045, while the publisher record for
DOI `10.1016/j.jnt.2012.04.021` gives volume 133, issue 3, pages
1045--1061.

The staged v1.4 source corrects that one line. An exact comparison
against the manuscript stored in the immutable v1.3 companion proves
that no other source line changed. In particular, no theorem, formula,
case row, polynomial, exponent, height margin, or Artin label changed.

## Verification

- `python3 scripts/audit_results_paper_a2.py`: pass;
- independent three-pass PDF builds: byte-identical;
- LaTeX warnings: zero;
- page count: 18;
- corrected source SHA-256:
  `5fd43c986c70459cfcd6a347511d780d03374527153701a4137cb6fcc85e1b93`;
- corrected PDF SHA-256:
  `9ad56d9ab1e2be123f5ddae709c5d9efa6fefbdad77989d33a48bca90e145d8c`.

Because companion v14 was already locally frozen, it was not silently
rewritten. Companion v15 is the versioned successor that nests v14 and
adds the corrected paper plus this audit. Publication remains gated on
DOI reservation, DOI insertion, a final deterministic rebuild, and
immediate explicit human approval.
