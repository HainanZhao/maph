# Cycle 082 — results v1.4 publication

## Outcome

`PUBLISHED_AND_PUBLICLY_VERIFIED`: immediately after explicit human
approval, Zenodo draft 21712478 was published as version 1.4 at DOI
`10.5281/zenodo.21712478`.

The publish response reported `submitted=true`, `state=done`, and seven
files. A fresh read through the public records API then downloaded all
seven files. Every downloaded byte count, MD5 checksum, and SHA-256
checksum matched the frozen local publication candidate exactly.

The postpublication regression replay passed 142/142 Effective-Stark
tests in 22.905 seconds with peak memory 60,304 KiB. The Dedekind
manifest passed, followed by 22/22 tests in 0.007 seconds with peak
memory 16,420 KiB.

## Claim boundary

No mathematical claim changed between the prepublication freeze and
the published record. `PROVED`: the RQ-000013 addendum records the exact
imprimitive Engine-A row with \(E_\chi=I_\chi=2\).
`PROVED`: the Roblot clarification identifies the certified-case
fourth-root ratio as a consequence of uniqueness. `OBSERVED`: the
retained five-case empirical statement is only the two-orientation
comparison against certified \(L'\)-balls; the target-selected raw
orientation remains withdrawn.

The immutable version 1.3 record remains untouched. Any future change
to version 1.4 requires a new Zenodo version.

## Evidence

- publication record:
  `artifacts/zenodo-results-publication-v5.json`;
- prepublication candidate:
  `artifacts/results-paper-v1.4-publication-candidate-v4.json`;
- DOI-bearing archive:
  `dist/effective-stark-results-companion-v17.tar.gz`;
- archive SHA-256:
  `e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506`.
