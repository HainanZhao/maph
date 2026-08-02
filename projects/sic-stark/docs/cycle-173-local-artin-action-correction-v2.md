# Cycle 173 correction v2: mutable-plan replay input

`cycle-173-local-artin-action-v1` correctly records the first-graded local
Artin-action calculation, but its builder froze `PLAN.md`. The required
post-seal plan update therefore made the builder and frozen-evidence check
report a false drift. No mathematical input, calculation, result, claim
boundary, or gate outcome is changed.

`cycle-173-local-artin-action-v2` supersedes v1 for replay. It freezes the
preregistration, prior immutable artifact, proof script, discovery output, and
sealing scaffold, but not the mutable strategic plan. Its exact replay must
reproduce the same all-power action `[1,2,1,2,1,2]`.
