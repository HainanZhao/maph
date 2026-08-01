# Cycle 7 signed F4F projection/extremizer v1 test correction

## Correction boundary

`OBSERVED`: the immutable signed-projection/extremizer v1 artifact and its
builder replay correctly.  One v1 unit test nevertheless fails because it
expects the unformatted literal

```text
F4F_eta fails on this energy/spaced/cardinality class
```

whereas the sealed document correctly typesets the same statement as

```text
of `F4F_eta` fails on this energy/spaced/cardinality class.
```

This is a literal-string harness defect only.

`PROVED`: no mathematical statement, source anchor, convention, reduced
Farey label, jitter interval, artifact field, projection identity,
phase-lattice construction, or replay payload is changed by this correction.
The v1 artifact remains immutable and its builder `--check` continues to
pass.

`OBSERVED`: the original failing test is retained unchanged.  This correction
records its exact failure and supplies a new test checking the actual sealed
formatted phrase.  The corrected test also reruns the immutable v1 builder.

## Exact cause and effect

The v1 document's conclusion is intentionally precise: it says that the
*conclusion of* `F4F_eta` fails on the larger energy/spaced/cardinality class,
while explicitly saying that it neither refutes `F4F_eta` on the actual Base
class nor proves the target.
The original exact-string assertion omitted both the words `of` and Markdown
backticks.  It therefore cannot match the sealed source.

`PROVED`: replacing only this test expectation with the exact source phrase
checks the intended boundary and changes no result.  The correction has no
effect on F4F, AFARI, CFARI, CRR-U, density, prime intervals, or L-functions.

## Replay

```sh
python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --check
python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py --write
python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py --check
python3 -m unittest tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1_test_correction.py
```
