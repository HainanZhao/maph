# Cycle 2 — Stream C explicit-formula adversarial audit v3

Claim boundary: `PROVED` that the official licensed-source access gap identified
in audit v2 is closed. V1 and v2 remain preserved. This correction does not
declare G0 PASS.

`PROVED`: the frozen MIT DSpace SWORD archive is a direct official source for
the two checked lecture-note PDFs. Its internal entries equal the separately
frozen official PDFs byte-for-byte; the checker also pins exact theorem and
proof anchors under `mutool version 1.23.10`.

`PROVED`: the relevant official item metadata identifies the course and author,
is non-withdrawn, and records CC BY-NC-SA 3.0. V2’s CC 4.0/author-byte-license
inference is withdrawn. No claim is made that a separately hosted author copy
is byte-identical to, or inherits the license of, the official archive member.

`PROVED`: v2’s distribution caveat no longer applies to the official route:
the official PDFs themselves, rather than an asserted correspondence with
author-hosted copies, are the source units now checked. The formula’s source
authority, range/convention anchors, remainder, and multiplicity proof are
therefore directly supported by the official licensed files.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/check_cycle_2_stream_c_explicit_formula_sources_v4.py
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_c_explicit_formula_v2_v3.py --check \
  projects/guth-maynard-zero-density/artifacts/cycle-2-stream-c-explicit-formula-v2-adversarial-audit-v3.json
```
