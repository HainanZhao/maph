# Cycle 18 archival-compatibility correction

Cycle 18 v2 correctly replayed the repaired mathematics, but it froze
corrected text at three paths that were already immutable inputs of historical
Cycle 7/13 artifacts.  Leaving those edits in place would make the older
records fail their own hash checks inside the new release archive.

Version 3 restores every historical frozen input byte-for-byte.  The repaired
argument now lives in the manuscript, the dedicated
`character_duality_correction_proof.md`, and the new coordinate verifier.
Version 3 depends only on those new sources plus the unchanged finite rank,
frontier, and core verifiers.  No mathematical field changes relative to v2.
