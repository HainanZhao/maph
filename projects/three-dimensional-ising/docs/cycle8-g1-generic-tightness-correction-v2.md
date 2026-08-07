# Cycle 8 G1 artifact correction v2

## Error

The sealed v1 artifact included measured `wall_seconds` and `peak_rss_kib`
fields returned by its exact replay.  These values are intentionally variable
between runs, so `build_cycle8_g1_generic_tightness.py --check` reproduced all
mathematical assertions but failed byte-for-byte artifact comparison.

## Cause and scope

The builder passed volatile measurement fields directly into the immutable
JSON payload instead of separating runtime metadata from deterministic proof
data.  No rank, edge set, homology relation, determinant residue, coordinate
ordering, or claim boundary differed.

## Correction

Version 2 recursively removes only the keys `wall_seconds` and
`peak_rss_kib` from replay payloads before deterministic rendering.  It
freezes the v1 artifact as the superseded input and leaves every mathematical
source and verifier unchanged.

The v1 artifact remains immutable but is noncanonical.  The v2 artifact is
the authoritative G1 record only after both `--write` and `--check` succeed.
