# Cycle 2 — Stream C explicit-formula access ledger v4 official-source correction

Claim boundary: `PROVED` that an official MIT DSpace SWORD archive directly
contains the two inspected course PDFs and that the official course item records
CC BY-NC-SA 3.0. This source correction does not establish G0 PASS. V1–V3 are
preserved.

`PROVED`: bitstream UUID `7292f134-d4a7-4063-bd7e-2084259b8fa9`, downloaded
from the DSpace core-bitstream endpoint, is frozen as
`artifacts/sources/mit-ocw-18-785-2007-sword-official.zip`. Its SHA-256 is
`d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57` and its
size is 5,334,292 bytes. The archive members
`18-785-spring-2007/contents/lecture-notes/errorbounds.pdf` and
`18-785-spring-2007/contents/lecture-notes/von_mangoldt.pdf` match the frozen
extracted official PDFs byte-for-byte.

`PROVED`: the frozen DSpace item metadata for handle `1721.1/101679` identifies
“18.785 Analytic Number Theory, Spring 2007,” author Kiran Kedlaya, is not
withdrawn, and records “Usage Restrictions:
Attribution-NonCommercial-ShareAlike 3.0 Unported.” The applicable statement
here is therefore course-specific CC BY-NC-SA 3.0—not CC 4.0, and not a license
assertion about separately hosted author-copy bytes.

`PROVED`: the official formula member contains the all-\(T\) formula, its
half-weight convention, the truncated zero range, and the stated remainder;
the official proof member contains the multiplicity convention and conclusion.
The deterministic checker pins both PDF and archive bytes, both internal
members, the item metadata, all literal `mutool` anchors, and `mutool version
1.23.10`. The reprocessed PDFs extract the displayed inequality glyph
differently; the checker pins the literal output for each PDF separately.

This supersedes v3’s now-obsolete distribution caveat, because the official
licensed source bytes are available and checked directly. It also withdraws
v2’s CC 4.0/author-byte-license overclaim. It does **not** assert byte identity
between author-hosted copies and these official PDFs, because that assertion is
unneeded.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py
```
