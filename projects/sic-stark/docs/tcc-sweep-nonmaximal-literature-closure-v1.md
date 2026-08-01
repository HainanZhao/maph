# Nonmaximal-order literature closure audit

**Status:** `PROVED` source-scope result
**Date:** 2026-08-01 UTC
**Claim boundary:** This audits what the checked primary AFK/Kopp sources
actually provide. It does not prove that future work cannot establish a
flat-monoid Engine-A analogue.

## Result

**PROVED (checked primary-source statements):** the present AFK/Kopp
theory does not contain the AFK-specific radical-annihilation or
label-preserving group-reduction theorem required by the semisimple descent
criterion.

The sources identify three independent missing ingredients:

1. Kopp, arXiv:2411.06763, introduction around p. 7 / source lines
   321--323, says the relevant field conjecture is not known to follow
   from existing Stark refinements, citing discrepancies in Euler factors
   for nonmaximal orders and RM pairs not in any primitive ray-class-group
   image.
2. The same source Section 3.2 defines the flat imprimitive monoid and
   proves only the injection of the primitive ray class group into it; it
   does not state a character transform or a radical-annihilation result.
3. AFK arXiv:2501.03970v2, source lines 5630--5635, explicitly says that
   nonmaximal-order ray-class partial-zeta theory is insufficiently
   developed for the analogue of the cited Stark-field theorem.

These statements are consistent with—and independently support—the
algebraic failures recorded in
`tcc-sweep-flat-monoid-fourier-obstruction-v1.md` and
`tcc-sweep-flat-monoid-zeta-obstruction-v1.md`.

## Consequence

The next step cannot be a finite support scan under the original plan. It
requires a new theorem proving, for the actual AFK flat monoid, all of:

```text
radical annihilation -> spectral/character coefficient formula
                     -> exact quadratic-support predicate
                     -> Tate-compatible zeta/regulator closure.
```

No existing source checked in this audit supplies any arrow of that chain
for general nonmaximal AFK strata. Thus the plan's
`TERMINAL_SCOPE_MISMATCH_CONTAINED` status remains the only justified
full-family status.

Source pins: AFK source SHA-256
`bc742b19594b5842d1edc343d9b48616273e8225c76910f7d758722cf6761519`;
Kopp source SHA-256
`87d273e270259af93ea27189001bebc4d540f5d28f0f173a799b1257faaac746`.
