# Cycle 18 sealing correction

Cycle 18 v1 included `peak_rss_kib` freshly measured by the polynomial-core
verifier.  That field is a benchmark, not mathematical evidence, and made
byte-for-byte `--check` replay depend on process history.  No proof, rank,
determinant, convention, or gate outcome is affected.

Version 2 preserves v1, removes the volatile memory measurement from the
canonical payload, and freezes this correction together with the v1 artifact
and builder.
