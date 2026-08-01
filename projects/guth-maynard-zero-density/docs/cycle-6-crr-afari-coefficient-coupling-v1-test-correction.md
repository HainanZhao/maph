# Cycle 6 CRR coefficient--Farey coupling v1 test correction

## Correction boundary

`OBSERVED`: the immutable v1 artifact and its builder replay correctly.  Its
first test file, however, expected the literal substring `does not prove` in
the claim boundary.  The sealed boundary instead correctly says `proves
neither`.  This is a test-wording defect only.

`PROVED`: no mathematical statement, source anchor, convention, artifact
field, coefficient-phase identity, actual-Farey label, or replay payload is
changed by this correction.  The v1 artifact remains immutable and its
builder `--check` continues to pass.

`OBSERVED`: the affected v1 test is retained unchanged as historical evidence
of the failed lightweight check.  This new version replaces only the faulty
literal expectation with `proves neither`, reruns the exact arithmetic and
artifact checks, and records the result in a new correction artifact.

## Exact cause and effect

The v1 claim boundary reads:

```text
It proves neither F4F_eta, AFARI_eta, CFARI_eta, CRR-U, ...
```

The original test required:

```text
assertIn("does not prove", data["claim_boundary"])
```

`PROVED`: these phrases are semantically consistent, but the string test is
false.  Replacing the assertion with `assertIn("proves neither", ...)` tests
the actual sealed boundary without changing it.

## Replay

```sh
python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --check
python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py --write
python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py --check
python3 -m unittest tests/test_cycle_6_crr_afari_coefficient_coupling_v1_test_correction.py
```
