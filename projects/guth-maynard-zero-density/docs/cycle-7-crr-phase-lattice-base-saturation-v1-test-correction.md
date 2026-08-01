# Cycle 7 phase-lattice Base-saturation v1 test correction

## Correction boundary

`OBSERVED`: the immutable phase-lattice Base-saturation v1 artifact and its
builder replay correctly.  One v1 unit test expects the literal phrase

```text
Exact rational aliases offer only constant factors
```

but the sealed document correctly says

```text
exact aliases can therefore provide at most constant factors
```

This is a literal-string harness defect only.

`PROVED`: no mathematical statement, source anchor, convention, actual
reduced-Farey label, alias quotient, capped efficiency identity, artifact
field, or replay payload is changed by this correction.  The v1 artifact
remains immutable and its builder `--check` continues to pass.

`OBSERVED`: the original failing test is retained unchanged.  This correction
records the expected failure and supplies a new focused test that checks the
actual sealed phrase and reruns the immutable v1 builder.

## Exact cause and effect

The two phrases have the same intended content, but an exact substring test
does not permit paraphrase.  `PROVED`: checking the actual sealed phrase
repairs only the test harness.  It changes no conclusion about Base
compatibility, alias class size, the distinct-phase quotient, F4F, AFARI,
CFARI, CRR-U, density, prime intervals, or L-functions.

## Replay

```sh
python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1.py --check
python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py --write
python3 proof/build_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py --check
python3 -m unittest tests/test_cycle_7_crr_phase_lattice_base_saturation_v1_test_correction.py
```
