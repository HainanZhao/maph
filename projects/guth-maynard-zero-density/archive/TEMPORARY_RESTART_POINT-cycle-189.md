# Temporary restart point — Cycle 189

This is the compact handoff after the five-cycle closeout (C185--C189). It
does not replace immutable artifacts.

## Valid results

- `PROVED`: C183 supplies one populated, coefficient-retaining primitive-ray
  box at `X^(21/25-o(1))` conditional on a critical light census.
- `PROVED`: C184's LCM identity is redundant. Its nonrational deformation is
  valid only after the `z^j-1` phase correction and remains subcritical.
- `PROVED`: C185's original curvature is withdrawn; its shifted-numerator
  identity and mass-only AP-free obstruction survive under correction.
- `PROVED`: C186 gives local actual-curve convexity/grid exclusion.
- `PROVED`: C187 shows local spacing plus current weighted data cannot force a
  critical saving.
- `PROVED`: C188 makes corrected nonrational root towers subcritical in the
  light regime.

## Open bridge

`CONJECTURED`: a global actual-exponential distribution theorem across
separated labels and varying denominator windows must bound the C183 box,
force seeded recurrence, or construct a critical nonrational saturator.
Further local classifiers are not authorized as a restart target.

## Required correction replays

```sh
source ../../tools/dev-env.sh
research rebuild
research check
python3 proof/build_cycle_183_intercept_cleared_ray_box_v1.py --check
python3 proof/build_cycle_184_phase_shift_correction_v1.py --check
python3 proof/build_cycle_185_three_label_curvature_convention_correction_v1.py --check
python3 proof/build_cycle_186_actual_curve_convexity_v1.py --check
python3 proof/build_cycle_187_separated_packing_v1.py --check
python3 proof/build_cycle_188_nonrational_root_tower_v1.py --check
```

Read this file, `PLAN.md`, and the cited C183--C188 artifacts before a new
cycle. Do not use uncorrected C184/C185 displays.

