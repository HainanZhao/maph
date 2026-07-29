# Cycle 018 release and deposition contract

Status: **CANCELLED_BY_USER.** No QMC package, tag, deposition, DOI, or
announcement will be created.

Reviewed: 2026-07-29 UTC

## Artifact order

1. Commit the passed fidelity/usability audits, compact oracle, and
   final release sources.
2. Create and push `certified-qmc-v1.0`.
3. Package the tag plus the three independently licensed data assets.
4. Authenticate the local release manifest and every declared file.
5. Create a Zenodo draft, reserve its DOI, insert that DOI into the
   local release manifest, and upload exactly the declared file set.
6. Verify every returned filename, byte count, and Zenodo MD5 against
   local bytes; verify the complete draft inventory again.
7. Publish only under the explicit `--publish` action.
8. Reverify the complete published inventory and DOI before emitting
   `cycle-018-zenodo-deposition.json` or permitting announcement.

The deposition certificate is necessarily post-tag external evidence.
Cycle 019 results and the finalized paper remain later commits, as
required by the production directive.

## Fail-closed checks

The depositor rejects:

- a bad release-manifest self-hash;
- a missing, changed, duplicate, or undeclared local file;
- anything other than four assets and three ancillary files;
- a release above Zenodo's documented 100-file or 50 GB default
  record limit;
- any remote filename, size, or MD5 mismatch;
- duplicate, missing, or extra remote files;
- a draft whose reserved DOI conflicts with the release manifest;
- any post-publication change in the verified file inventory; or
- a publication response without the reserved DOI and record URL.

The remote MD5 is used only as Zenodo's transport/storage equality
check.  The project release manifest continues to authenticate every
local asset with SHA-256.

## API and license perimeter

The official Zenodo developer documentation, checked on 2026-07-29,
still documents the depositions API, bucket streaming upload, computed
MD5 checksums, and the publish action:
`https://developers.zenodo.org/`.
The official file documentation states a maximum of 100 files and a
default total record volume of 50 GB:
`https://help.zenodo.org/docs/deposit/manage-files/`.

The record is software-primary and therefore uses Apache-2.0 at record
level.  Per-asset metadata and included license files identify source
as Apache-2.0 and the project-authored oracle/tables as CC-BY-4.0.
Upstream generating vectors are not embedded.

The local flow has been exercised with a mocked authenticated API
through upload, draft inventory verification, irreversible publish,
published-inventory verification, DOI confirmation, and self-hashed
certificate creation.  This is a local preflight only; the final
`VERIFIED_EXTERNAL_DEPOSITION_RESPONSE` tag requires the real Zenodo
response.
