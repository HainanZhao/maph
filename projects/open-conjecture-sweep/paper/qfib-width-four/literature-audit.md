# Literature and novelty audit: width-four q-Fibonomial unimodality

Audit date: 2026-08-06 UTC.

- `PROVED` (source-checked): Bergeron--Ceballos--K\"ustner, Theorem 2.4,
  proves that q-Fibonomials are polynomials with nonnegative integer
  coefficients through a weighted path--domino model. Their Conjecture 2.5
  asserts unimodality for all parameters. Primary source:
  <https://doi.org/10.3842/SIGMA.2020.076>.
- `PROVED` (source-checked): Connelly--Ito--Martinez--Shevchenko--Yang,
  Theorem 1.2, proves only widths `n <= 3`. Section 5 says all parameters
  remain open and explains that Conjecture 5.4 does not directly apply to
  `n >= 4`. Primary source: <https://arxiv.org/abs/2605.12822>, version 1,
  2026-05-12.
- `PROVED` (source-checked historical attribution): Sagan--Savage gives the
  earlier unweighted Lucas-sequence/Fibonomial combinatorial model used as a
  precursor to the q-weighted model. Primary record:
  <https://doi.org/10.1515/integ.2010.052>.
- `OBSERVED` (bounded search, not a universal negative): searches for
  `"width four" q-Fibonomial unimodality`,
  `"m+4" "q-Fibonomial" unimodality`,
  `site:arxiv.org q-Fibonomial unimodality n=4`, and
  `"q-Fibonomial" unimodal n=4` located no later width-four proof as of the
  audit date. Accordingly, the paper states the search boundary and makes no
  exhaustive priority claim.

Claim boundary: the manuscript proves only
`[m+4 choose 4]_F` for every integer `m >= 1`. It does not claim the full
two-parameter conjecture, widths at least five, log-concavity, or a
combinatorial chain decomposition.
