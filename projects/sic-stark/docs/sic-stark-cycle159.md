# SIC--Stark research cycle 159: trilogy publication handoff

Date: 2026-07-29

## Program decision

The Certified-QMC production program was cancelled by explicit user
direction. Its production process, packaging, prime-schedule,
licensing, and paper work must not resume. The small exact evaluator
and the process record remain archived; the partial production dataset
is evidence only and is not a releasable table set.

The active order is now:

1. ship SIC--Stark Papers I and II;
2. run the dimension-16 PARI/Shintani check;
3. execute the effective-Stark harvest;
4. run the two dimension-six diagnostics and finish Paper III;
5. write the methods paper.

The unit-lattice C2 question is parked as an independent, small side
question. It has no dependency on the cancelled QMC engine.

## Dimension-seven publication gate

Cycle 158 independently replayed the dimension-seven conductor-two
closure. All eight dedicated tests passed, covering Shintani index
two, both formal shifts, trace one, idempotency, and all \(441\) exact
minors per shift. The relevant order has one wide class.

Verdict: **PROVED; Paper II Theorem 1 does not require rescoping.**

## Local publication work completed

- Paper I now explicitly cites the dimension-seven/eight companion
  manuscript instead of carrying the obsolete composite-dimension
  pointer.
- Each paper has its own Zenodo metadata and citation file.
- Each paper has a deterministic, standalone arXiv source archive.
- Both arXiv archives compile twice from clean extraction.
- Both reproducibility archives build byte-identically, verify their
  root checksum manifests, and pass their archive-local test suites:
  80 tests for Paper I and 11 tests for Paper II.
- The Kopp correspondence draft now leads with the four unconditional
  dimensions and retains the isolated dimension-six analytic question
  as the follow-up.

Artifact hashes:

```text
a9731fbeaf108f08b77fe7a23f2d0fb127df1078f3fc9200e79edf4d97f1593f  dist/sic-stark-paper-I.tar.gz
8f5f91205b52a0fad5468f23f1258ad8f0c260c6ca21de4132d6956bedb6ef84  dist/sic-stark-paper-II.tar.gz
0493c6c1bb3c8c01daf9ec8a864ec0a6bf2ba3bedf1dd30b844b0ddec6847316  dist/sic-stark-paper-I-arxiv.tar.gz
df24b350711907be0767463a39c011e91d6f6e092291f8ffed1c8f591914a642  dist/sic-stark-paper-II-arxiv.tar.gz
```

The machine-readable gate is
`certificates/trilogy-publication-local-gate-cycle159.json`.

## External boundary

No Zenodo access token or arXiv author session is present in the
workspace. Therefore no DOI has been reserved, no arXiv submission has
been made, and no correspondence has been sent. These are
author-account actions and remain explicitly **PENDING**, not silently
treated as complete.

`publication/EXTERNAL-SUBMISSION.md` gives the exact handoff order:
reserve the two archive DOIs, insert them and rebuild, upload the final
reproducibility bytes, submit the two arXiv bundles, then replace the
four link placeholders in the Kopp letter and send after author review.

## Crash recovery

Resume from this record and the current Git commit. Do not restart QMC.
For the trilogy, rerun:

```bash
cd projects/sic-stark
bash tests/test_arxiv_submissions.sh
bash tests/test_companion_archives.sh
```

If both pass, the only unfinished trilogy operations are the
author-account actions described above.
