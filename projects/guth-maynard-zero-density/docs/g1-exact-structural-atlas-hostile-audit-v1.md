# Hostile audit of the G1 exact structural atlas v1

## Outcome and boundary

`PROVED`, conditional on the source formulas already frozen by G1: an
independent exact-rational implementation recomputes all 7,744 local rows,
704 diagonal energy rows, all 560 transfer rows, every recorded residual and
tie label, both transfer branches, and both mandatory anchors. It also
directly verifies the frozen source and preregistration-document hashes.

`OBSERVED`: containment—the mathematical row data is correct, but the package
does not yet meet the repository's runtime and convention-provenance rules.
The preregistration builder uses bare `assert` statements; consequently its
replay exits zero under `python3 -O`. The exact atlas hashes the resulting
artifact but does not itself run a direct source/document verification.
Further, it redefines the grid functions instead of deriving them from
`conventions/g1_atlas_v1.py`.

This audit proves no new large-values, zero-density, short-interval,
extremizer, or saturation theorem. It is not a G1 route selection.

## Containment

The sealed v1 artifact remains unchanged, and its current finite rational
rows are retained as exactly recomputed. The defect blocks only a claim that
v1 is a fully AGENTS.md-compliant final authority. A versioned successor must
use explicit failures in the preregistration builder, verify the cited source,
document, and runtime pins directly before atlas construction, and import the
frozen grid conventions rather than duplicate them.

`OBSERVED`: after this historical audit was frozen, the convention module was
runtime-hardened and received a new byte identity. Its historical `--check`
therefore halts at the intentionally frozen old convention hash. The separate
v2 authority and v2 hostile re-audit preserve this v1 finding while checking
the explicit old-to-new semantic correction; this document and artifact are
not rewritten to make the old audit appear current.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_exact_structural_atlas_hostile_v1.py --check
python3 -m unittest projects/guth-maynard-zero-density/tests/test_g1_exact_structural_atlas_hostile_audit_v1.py -v
```

The first command deliberately reports `REMEDIATION_REQUIRED`: successful
replay means the bounded defect has been preserved and the exact current data
still agrees, not that the defect has been silently repaired.
