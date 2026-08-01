# Cycle 3 G1 exact structural atlas v2 correction

## Outcome

`PROVED`, conditional on the directly hash-verified frozen source formulas:
v2 exactly reevaluates the same 7,744 local and 560 transfer rows as v1,
with 704 diagonal-only energy rows and both mandatory anchors intact. This is
not a new large-values, density, short-interval, extremizer, or saturation
theorem; it evaluates no finite complex Dirichlet polynomial.

`OBSERVED`: correction—hostile audit v1 found that the predecessor's
preregistration builder accepted `python3 -O` because it used bare asserts,
and that the atlas duplicated its frozen grids. V1 is preserved unchanged.
V2 rejects optimized mode explicitly, requires CPython 3.12.3 and mpmath
1.2.1, hashes the preregistration artifact and document plus both pinned
Guth--Maynard source members directly, and imports/cross-checks the frozen
grid functions in `conventions/g1_atlas_v1.py`.

`OBSERVED`: the convention module's prior bare `primary_spine` assertions
were hardened to explicit failures without changing any returned grid or
family value. V2 pins that corrected convention-module byte identity and
cross-checks its complete grids, 42-coordinate spine, all families/pairs,
scales, precisions, and RNG constants against the sealed preregistration
artifact. The correction record states the old hash
`3d3cef60c32dff2a2e4cbd3c10b229464d74aadbbaef53ba1fccc7158b78d726` and
the new pinned hash in the v2 artifact; it never overwrites v1.

## Replay

```sh
python3 projects/guth-maynard-zero-density/discovery/run_g1_exact_structural_atlas_v2.py --check
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle_3_g1_exact_structural_atlas_v2.py -v
```

`-O` and any mismatched source, document, convention, artifact, runtime, or
row byte cause failure before the v2 result is accepted.
