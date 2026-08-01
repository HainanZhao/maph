# Cycle 129 — census Zenodo publication

Recorded: 2026-08-01 UTC.

## Outcome

Version 1.0 of the corrected census paper is public at
<https://doi.org/10.5281/zenodo.21729947>. The concept DOI is
`10.5281/zenodo.21729946`.

No mathematical claim changed at publication. The deleted-prime cover
criterion remains `PROVED`; its 1,560-row exact census corollary remains
`PROVED`; the proposed four-support nondegeneracy claim remains
`REFUTED`. The H boundary remains 2,699 complete statuses plus five
incomplete historical quartic constructions, with twelve of 232
Engine-B member transports proved.

## Gate results

- The first two clean PDF builds, made without a frozen build epoch,
  differed in metadata bytes. This failed attempt is preserved in the
  release-candidate artifact. With `SOURCE_DATE_EPOCH=1785542400`, two
  independent two-pass builds were byte-identical, eight pages, and
  free of warning, overfull, undefined-reference, and error matches.
- All 174 tests passed in 33.40 seconds with peak RSS 75,244 KiB.
- Two independent companion builds were byte-identical. A fresh
  extraction verified all 1,609 manifest files and replayed the theorem,
  referee-boundary, and manuscript audits successfully.
- The authenticated draft contained exactly the three preregistered
  files. Remote byte counts and MD5 hashes matched the local SHA-256
  freeze before publication.
- After publication, every file was downloaded without authentication
  and compared byte-for-byte with its local source.
- The DOI resolves with HTTP 200 to record 21729947. The public record
  page names `effective-stark-census-00-main-paper.pdf` in its citation
  PDF metadata, open preview title, and preview iframe; it is the public
  default preview.

## Public inventory

1. `effective-stark-census-00-main-paper.pdf` — 314,917 bytes — SHA-256
   `6aa6a529249567eceb4589a2f925643fc0d1a272066344d7e1710b82e9fdd0fd`.
2. `effective-stark-census-00-main-paper.tex` — 27,302 bytes — SHA-256
   `ca2d2cbcaf3f92952b32885ba9d9d3486d11f4ae85dce3c785d3ef0291ffcf0d`.
3. `effective-stark-census-companion-v1.tar.gz` — 1,524,266 bytes —
   SHA-256
   `4d2f598c444b3a6cbf969bcb945fc5a89334229531d13738eebf989495be2ec3`.

The API response and credential were not copied into repository files.
`ZENODO_TOKEN` was used only in an `Authorization: Bearer` header.
