# TCC flat-monoid sweep — handoff summary

**Status:** TERMINAL_UNIVERSAL_ORDINARY_CHARACTER_ROUTE_REFUTED
**Date:** 2026-08-01 UTC
**Authoritative plan:** `plans/tcc-flat-monoid-engine-a-successor.md`
**Recorded commit:** `c89e5e9` (`research: record flat-monoid Engine A scope counterexample`)

## Bottom line

**CERTIFIED_NUMERICAL:** the proposed universal extension of Engine A from
maximal-order ray *groups* to AFK's non-coprime flat order-ray *monoids* is
false. The original 2-elementary stratum sweep is therefore terminally
contained: do not resume its eligibility scan, bridge automation, or minor
certificates on the ordinary-character route.

This is a scope result, not a TCC counterexample and not a correction to a
published TCC theorem. Dimensions 4/5 use conductor-one/maximal-order ray
groups; dimensions 7/8 use their explicit conductor-lowering and labelled
ray-class calculations. No earlier certificate or theorem table was found to
rely on the universal flat-monoid factorization ruled out here. A later prose
audit should still flag any sentence claiming that Engine A applies to every
AFK order-monoid stratum.

## Certified obstruction

For the admissible AFK pilot

    d = 12, K = Q(sqrt(13)), O = O_3, Q = <1,-11,1>,

the finite flat monoid has 50 elements and its rational monoid algebra has
Jacobson-radical dimensions

    dim J = 19, dim J^2 = 2, J^3 = 0.

**PROVED_FINITE_LABEL_MAP:** the 144 characteristics split into 50 stabilizer
orbits which map bijectively to the flat-monoid classes. The first frozen
radical vector is `e_3 - e_0`, with `e_3` labelled by characteristic `(4,10)`.

**CERTIFIED_NUMERICAL:** the AFK differenced partial-zeta derivative is zero
on `e_0` and has rigorous enclosure

    Z'_(12 infinity_2)(0,e_3)
      in [-4.348280582567914, -4.348280577050716].

The interval excludes zero. By the **PROVED** semisimple-descent criterion,
the functional does not factor through ordinary monoid characters. This
refutes the universal ordinary-character/ray-group Engine-A descent.

## What is and is not authorized

- **Closed:** reusing maximal-order character Fourier, quadratic-support,
  Tate, or deleted-prime-cover mechanisms as a universal AFK flat-monoid
  closure.
- **Not claimed:** a TCC counterexample, impossibility of every nonsemisimple
  method, or invalidity of Papers I/II.
- **Only possible successor:** preregister a genuinely radical-sensitive,
  label-preserving spectral theory and prove its Stark/Tate-compatible
  closure before any new TCC sweep.

## Fast evidence map

| Purpose | Controlling artifact |
|---|---|
| Research status, gates, and recovery | `plans/tcc-flat-monoid-engine-a-successor.md` |
| Exact AFK monoid-type/scope correction | `docs/tcc-sweep-engine-a-interface-scope-audit-v3.md` |
| Character expansion iff radical annihilation | `docs/tcc-sweep-semisimple-descent-criterion-v1.md` |
| P1 finite algebra and labels | `docs/tcc-flat-monoid-p1-overlap-result-v1.md`; `docs/tcc-flat-monoid-p1-overlap-labels-v1.md` |
| P2 certified counterexample | `docs/tcc-flat-monoid-p2-radical-counterexample-v2.md`; `artifacts/tcc-flat-monoid-p2-radical-counterexample-v2.json` |
| Original sweep containment | `plans/tcc-2-elementary-stratum-sweep.md` |

## Replay

Run from the repository root:

    python3 projects/sic-stark/discovery/build_tcc_flat_monoid_p1_overlap_adapter.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p1_overlap_adapter.py
    python3 projects/sic-stark/discovery/build_tcc_flat_monoid_p1_overlap_labels.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p1_overlap_labels.py
    projects/sic-stark/.venv/bin/python -u projects/sic-stark/proof/certify_tcc_flat_monoid_p2_radical_counterexample.py
    python3 projects/sic-stark/proof/verify_tcc_flat_monoid_p2_radical_counterexample.py

Expected terminal enclosure is the interval displayed above. A failure, a
changed label, or an interval meeting zero contains the result and requires a
versioned correction; it does not authorize re-opening the original sweep.
