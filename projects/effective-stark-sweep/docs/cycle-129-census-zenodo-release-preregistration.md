# Cycle 129 — census Zenodo release preregistration

Recorded: 2026-08-01 UTC, before creating a Zenodo deposition.

## Authorized objective

Publish version 1.0 of the corrected census paper and its deterministic
replay package under the standing Zenodo authorization in root
`AGENTS.md`. This is a new Zenodo concept record, not a new version of
the results paper.

## Frozen public inventory

The deposit root will contain exactly these three files, in lexical
order:

1. `effective-stark-census-00-main-paper.pdf`;
2. `effective-stark-census-00-main-paper.tex`;
3. `effective-stark-census-companion-v1.tar.gz`.

The first file must be the public default preview. No standalone
addendum or competing PDF is authorized at the deposit root.

## Frozen metadata

- upload/publication type: publication / article;
- version: 1.0;
- publication date: 2026-08-01;
- creator: Zhao, Hainan; Independent Researcher;
- access/license/language: open / CC BY 4.0 / English;
- title: *A Certified Canonical Census of One-Place Stark Invariants
  over Real Quadratic Fields: Exact Quadratic Value Orbits and the
  Higher-Order Frontier*;
- related work: the published results-paper DOI
  `10.5281/zenodo.21713178` is referenced, not treated as the census
  archive DOI.

The description must lead with the corrected selected-modulus boundary,
state the exact T/Q/H counts, identify the deleted-prime cover theorem,
state the 2,699-complete plus five-incomplete H boundary, and disclose
that only twelve of 232 Engine-B noncanonical transports are proved.

## Required gates

1. Reserve the DOI before editing any release-facing source.
2. Insert the reserved DOI into the paper, metadata, archive README,
   and replay verifier.
3. Build the paper twice and require byte identity, eight pages, and no
   warning/overfull/undefined/error matches.
4. Build the companion twice independently and require byte identity.
5. Extract the archive into a fresh directory and run its verifier,
   including manuscript, referee-boundary, and deleted-prime theorem
   audits.
6. Run the full live project suite and preserve wall time and peak RSS.
7. Upload metadata, then exactly the three frozen files.
8. Verify the authenticated draft inventory, remote byte counts and MD5
   checksums, local SHA-256 checksums, and main-paper preview source.
9. Publish once, then verify public metadata, downloads, checksums,
   ordered inventory, and default preview.

Any mismatch stops publication. A request timeout must be resolved by
inspecting deposition state before retrying.

## Credential boundary

`ZENODO_TOKEN` may be loaded only from the established interactive zsh
startup and used only in an `Authorization: Bearer` header. Its value
must never appear in a URL, file, transcript, or command output.
