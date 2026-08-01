# Cycle 4 P1R v3 hostile audit — source-attribution correction required

Claim boundary: **OBSERVED** read-only audit of the sealed v3 preregistration. This audit records no P1R obstruction theorem and grants no CRR search authority.

## Outcome

`FAIL_SOURCE_ATTRIBUTION_COMPLETENESS`.

The v3 historical replay is correctly lifecycle-decoupled: static and guarded-runtime checks found no read of live `PLAN.md`; the immutable authorization snapshot is chained to the historic Plan byte; and current operational preflight remains an `OBSERVED`, excluded, non-frozen report. Under simulated `P1R ACTIVE -> COMPLETE` and a later affirmative P2 selection, preflight becomes ineligible while historical replay bytes remain unchanged.

The bounded remaining defect is direct attribution of the large-values scale calculation. The sealed calculation asserts `[6, 8, 8]` from the three large-values monomials, yet v3 records neither `GM-T1.1` nor a `thrm:LargeValues` source fragment. A hash of the complete GM TeX file cannot substitute for an explicit theorem locator, hypotheses, and permitted use.

Required v4 correction: add a `GM-T1.1` ledger row and machine-check the theorem label plus its three-term formula. Preserve the v3 lifecycle architecture and the pinned v1/v2 hostile failures.

Replay:

```text
python3 proof/audit_cycle_4_p1r_preregistration_v3_hostile.py --check artifacts/cycle-4-p1r-preregistration-v3-hostile-audit-v1.json
```
