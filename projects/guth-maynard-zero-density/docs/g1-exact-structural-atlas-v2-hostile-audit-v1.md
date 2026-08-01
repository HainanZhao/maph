# Hostile re-audit of the corrected G1 exact structural atlas v2

`PROVED`, conditional on the directly pinned source formulas: a second,
independent exact-rational route recomputes all 7,744 local rows, 704
diagonal-energy rows, and 560 transfer rows in v2, including residuals, ties,
branches, and anchors.

`OBSERVED`: the v2 normal replay passes and `-O` fails closed. The re-audit
also verifies v2's direct source/document/runtime pins and the explicit old to
new convention-runtime correction, whose current module outputs match every
frozen grid, spine, constant, and family record. V1 and its hostile finding
remain preserved. This is not a G1 decision or a new analytic theorem.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_v2_hostile_v1.py --check
```
