# Cycle 093 — quartic completion protocol

## Authorized objective

Complete the five legacy incomplete quartic kernels before presenting
the H taxonomy as complete.  This is a computational-completion task,
not a presumption that any kernel is Engine-C eligible or that any
packet identity follows.

## Frozen targets and methods

1. RQ-005298, packet 4: rerun the existing exact
   `screen_engine_c_geometry.gp` route under PARI/GP 2.15.4 with a
   wall-time cap of **10,800 seconds** and the existing 4 GB GP stack.
   It previously reached the order-16 normal-closure subgroup stage
   after about 960 seconds and was voluntarily deferred, rather than
   failing.
2. RQ-002397 packet 2; RQ-004593 packet 1; RQ-007451 packet 1; and
   RQ-007475 packet 2: do **not** re-run the same PARI/GP 2.15.4 call
   merely for more time.  Each has a recorded reproducible
   `bnrclassfield` segmentation fault.  The next route is a pinned
   newer PARI build or a separately scripted exact class-field
   construction, recorded as a new method and run first on a successful
   and a failing control.  The initially pinned source is the official
   PARI commit `04f8bd714658395434e6ae9becbc9e7d5d1a10e8`; its target
   runs receive a 12 GB GP stack ceiling (the host had 14 GiB available
   when frozen).

## Gates

- Preserve every prior failed/deferred transcript and never overwrite
  the v1 H taxonomy.
- A new tool version is a method substitution, not a replay: record its
  source/version/hash and pass the two controls before target verdicts.
- A positive geometric result requires the existing exact predicates
  (normal-closure degree/group, base identification, and linear
  reinduction condition) plus an independent exact replay before it
  changes the H taxonomy.
- A cap expiry records `INCOMPLETE_NO_CENSUS_VERDICT`; it is not a
  mathematical failure.  A segmentation fault is a tool failure, not a
  mathematical verdict.
