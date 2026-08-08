# Cycle 15 failure ledger

- False step: the first sealer draft mistyped the sealing-scaffold SHA-256.
- Detection: input freezing failed before the deterministic search and before
  any artifact write.
- Containment: the direct digest replaced the transcription; the timeboxed
  rank-12 outcome was unaffected.

- False step: the first replay comparison compared the search's in-memory
  tuples directly with lists produced by JSON decoding and misclassified the
  representation difference as nondeterminism.
- Detection: the complete deterministic search finished, then the equality
  guard failed although the serialized data were unchanged.
- Containment: replay now compares canonical JSON values.  No search result or
  mathematical field changed, and no artifact had been written.
