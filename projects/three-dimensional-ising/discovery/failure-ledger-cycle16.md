# Cycle 16 failure ledger

- False step: the first sealer draft mistyped the already pinned sealing
  scaffold digest.
- Detection: the pre-write `freeze_inputs` check rejected it; no artifact was
  created.
- Containment: the digest was replaced by direct SHA-256 output.  The
  tensor-network translation and all mathematical sources were unaffected.
