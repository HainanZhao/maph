# Cycle 8 EO-LF4 Objective-2 audit v1 test correction

## Correction boundary

`OBSERVED`: the immutable EO-LF4 Objective-2 audit artifact and builder replay
correctly.  Its original test expected the lower-case literal

```text
for every fixed epsilon>0
```

but the sealed theorem field correctly begins its sentence with

```text
For every fixed epsilon>0
```

This is a case-only test-harness defect.  `PROVED`: it changes no theorem,
source anchor, actual Farey label, energy class, sharp exponent, objective-2
assessment, exclusion, or Base/full-CRR gate.  The original test remains
immutable and is retained as a contained failed lightweight check.

## Exact effect

The corrected test checks the exact sealed phrase with its initial capital.
It reruns the immutable v1 builder and validates the artifact hash.  No
payload in the original artifact is modified, and the correction makes no
new claim about AFARI, CFARI, CRR-U, density, short intervals, or L-functions.

## Replay

```sh
python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --check
python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py --write
python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py --check
python3 -m unittest tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1_test_correction.py
```
