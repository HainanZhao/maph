# P6 detector-tail v2 epistemic-status correction

`OBSERVED`: the immutable v1 detector-tail artifact used the noncanonical tag
`PROVED_CONDITIONAL`. Repository policy permits `PROVED` with its hypotheses
stated explicitly, but not that compound tag. The analytic statement and all
open obligations are unchanged.

The continuing status is therefore:

- `PROVED`: the Mellin-tail, spacing, height-transport, residue, and compact-
  range deductions follow from the inputs explicitly recorded in v1;
- `CONJECTURED`/external premises for this project: `L_POLY_A`,
  `FOURTH_MOMENT_H`, and `LOW_HEIGHT_MULTIPLICITY_COUNT` until their exact
  primary hypotheses are checked;
- `OBSERVED`: this is an amended detector route, not validation of the CGL-v2
  text as written.

Consequently Z03 is reduced to those named external inputs; S06, S03, F08,
and the remaining conductor-sensitive obligations stay open. No zero-density
or short-interval theorem is promoted, and paper-stage hostile audit remains
deferred.

Replay:

```sh
python3 proof/p6_detector_qt_tail_v2_status_correction.py --check
python3 -m unittest tests.test_p6_detector_qt_tail_v2_status_correction -v
```
