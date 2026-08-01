# MIT DSpace SWORD official-bitstream audit v1

**Claim boundary — OBSERVED.** This is an independent audit of the frozen
official MIT DSpace SWORD ZIP, its course-level metadata, and two extracted
official PDFs. It proves no new explicit-formula result and does not assert
that the official PDFs are byte-identical, content-identical, or derived from
the author-hosted copies.

Run the deterministic offline check:

```sh
python3 proof/audit_mit_sword_official_bitstream_v1.py --check
```

The audit records the DSpace chain:

- item `ef0f95e2-2e6c-4817-bf11-5e6285783f29`, handle `1721.1/101679`;
- SWORD bundle `b4f16d16-1dc5-4da2-90bf-44165e4a568d`; and
- SWORD bitstream `7292f134-d4a7-4063-bd7e-2084259b8fa9`, whose frozen ZIP
  has SHA-256 `d559229963960da2087918a95af6efd7ad8999a4ba63942a12aef63c5eceac57`.

It verifies Python ZIP CRC integrity, 304 entries, and exact byte agreement
between the ZIP members
`.../errorbounds.pdf` and `.../von_mangoldt.pdf` (underscore) and their
separately frozen official PDFs. It records the official 4- and 6-page counts
and text-extraction anchors: the former states Theorem 1 with its truncated
formula/remainder, while the latter contains the residue proof and explicitly
states multiplicity counting.

Course-level rights metadata is recorded as MIT's Attribution-NonCommercial-
ShareAlike 3.0 Unported field. This is an observed metadata field, not legal
advice. Optional current REST comparison is available with `--live-api`; it is
not part of the deterministic offline artifact.
