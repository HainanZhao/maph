# Cycle 14 failure ledger

## Sealer hash transcription

- False step: the first sealer draft transcribed one hexadecimal character of
  the machine preregistration SHA-256 incorrectly (`e` in place of `c`).
- Detection: `freeze_inputs` rejected the preregistration before any artifact
  was written.
- Containment: no sealed record was created, no determinant or mathematical
  field was affected, and the digest was corrected from the file's direct
  SHA-256 output before retrying.
