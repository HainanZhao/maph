# Cycle 083: results v1.5 main-paper integration

Recorded: 2026-07-31 UTC.

## Outcome

Version 1.5 is staged as a checksum-verified, unpublished Zenodo draft
at reserved DOI `10.5281/zenodo.21713178`.

The RQ-000013 certified addendum is now a worked subsection of the
main paper. Its exact replay passes with the existing `PROVED` claim:
\(E_\chi=2\), \(I_\chi=2\), and
\(X_{[0]}=u^2,\ X_{[1]}=u^{-2}\). The `bnrL1` point comparison remains
`OBSERVED` and quarantined.

The standalone addendum PDF and TeX file were removed from the v1.5
top-level draft inventory. They remain byte-preserved inside the
nested immutable v1.4 companion.

## Preview correction

The main upload is named
`effective-stark-results-00-main-paper.pdf`. It sorts first in the
five-file inventory. Zenodo's authenticated draft record identifies
that same file as the IIIF thumbnail/default-preview source.

## Verification

- main and supplement: three-pass deterministic builds in two clean
  directories, byte-identical, zero warnings;
- main paper: 19 pages, merged section visually inspected;
- v18 companion: two builds byte-identical, extracted replay passed;
- metadata: all 12 requested fields match the draft;
- files: five of five remote byte counts and MD5 checksums match local
  files; local SHA-256 hashes are frozen;
- publication action: not taken.

Publication remains an irreversible human-approval gate.
