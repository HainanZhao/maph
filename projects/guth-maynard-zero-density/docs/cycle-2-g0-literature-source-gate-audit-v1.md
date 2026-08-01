# Cycle 2 — G0 literature/source-hypothesis gate audit v1

Claim boundary: `PROVED` only for the bounded literature and source-hypothesis
gate. This is not a proof of the cited analytic theorems and does not declare
G0 PASS.

`PROVED`: the eight selected source gates pass: MP Lemma 24 with the GM Type
transfer; Montgomery’s discrete mean-value theorem; GM’s detector, smoothing,
separation, powered-polynomial, and MVT transfers; Ingham through Huxley’s
published restatement; Huxley’s near-one estimate; Ford plus Platt--Trudgian;
HSW plus Bui--Heath-Brown; and the official Kedlaya formula/proof chain.
Exact locators, ranges, height conventions, multiplicity conventions, and
source hashes are frozen in the artifact.

`PROVED`: no unread or disjunctive source remains on this selected path.
The original Ingham article is not directly used: Huxley (1.8) is the selected
published restatement. Jutila is unused because Huxley (1.9) is the single
near-one branch. Davenport and Montgomery’s *Topics* are replaced by official
Kedlaya and Ford-plus-Platt, respectively.

`PROVED`: MP Lemma 24 itself does not state a multiplicity convention, so the
gate uses the independently pinned Stream-B multiplicity/two-sided conversion
rather than inferring one from MP. HSW+Bui supplies the separate
multiplicity-inclusive local-count convention.

`OBSERVED`: the older Stream-C source ledger contains stale Huxley title
metadata, although its frozen file hash and p. 173/(1.9) locator identify the
correct article. This record-maintenance issue does not put an unread or
disjunctive source on the selected path.

Recommendation: `PROVED` **PASS** for this source-hypothesis gate only.
Resource/performance evidence and global G0 status are deliberately not
evaluated.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g0_literature_source_gates_v1.py --check
```
