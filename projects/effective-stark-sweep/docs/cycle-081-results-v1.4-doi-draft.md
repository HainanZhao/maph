# Cycle 081 — results v1.4 DOI-bearing Zenodo draft

Recorded: 31 July 2026 UTC.

## Outcome

`DOI_RESERVED_UNPUBLISHED`: an authenticated read-only check found
published v1.3 and no existing successor draft. One new-version action
created Zenodo draft 21712478 and reserved DOI
`10.5281/zenodo.21712478`. The draft remains unsubmitted.

The reserved DOI was inserted into the main paper, supplement,
RQ-000013 addendum, and release metadata. Independent three-pass builds
of all three PDFs were byte-identical and warning-free. The DOI-bearing
companion v17 was built twice byte-identically; its SHA-256 is
`e2a945edaddcec32e3aad10e67f8b960af0bc304b07ba5503ab7be62384b9506`.
Extracted replay passed through the nested v16/v15/v14/v13 chain.

The exact source-delta audit proves that relative to published v1.3:

- the main source changes only the Tangedal--Young page range and
  archive DOI;
- the supplement changes only the archive DOI;
- the new addendum supplies the `PROVED` RQ-000013 row.

No theorem, packet, polynomial, magnitude certificate, or Artin
convention changed from the pre-DOI freeze.

## Draft upload verification

Metadata and exactly seven top-level files were uploaded to the
unsubmitted draft. Every remote MD5 and byte count matches the local
file, and all local SHA-256 values are frozen in
`artifacts/zenodo-results-v1.4-draft-upload-verification-v1.json`.
All 12 requested metadata fields match the remote draft.

The inherited draft copy of companion v13 was removed only after v17
was uploaded; published v1.3 and the local v13 archive remain
untouched.

## Publication gate

Publication is irreversible and has not been requested. The next action
is permitted only after the user sees the final metadata, seven-file
inventory, and verified checksums and explicitly approves publication
of DOI `10.5281/zenodo.21712478` immediately before the publish call.
