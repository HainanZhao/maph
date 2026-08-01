# Cycle 4 P1R v4 hostile audit — PASS

Claim boundary: `OBSERVED` read-only verification of v4 replay integrity and source attribution. No P1R theorem is proved; CRR discovery/search remains prohibited.

V4 corrects the v3 source-attribution defect. The audit independently checks GM `thrm:LargeValues`, its exact three-term formula and listed hypotheses, the formal substitution `(N,T,V)=(v^10,v^12,v^7)`, and the resulting exponent vector `[6,8,8]`. The calculation is only upper-bound bookkeeping.

The audit also verifies static and guarded-runtime absence of live `PLAN.md` reads, the immutable snapshot and preserved v1--v3 hostile-failure chain, unexecuted FS status, CRR prohibition, source/range records, CLI replay, `-O`/`-OO` failure, overwrite refusal, and in-project self/source tamper rejection.

The v4 regression test is not a builder input because `--check` is the self-contained historical artifact replay. Its exact test byte is independently hash-pinned and executed by this audit.

Replay:

```text
python3 proof/audit_cycle_4_p1r_preregistration_v4_hostile.py --check artifacts/cycle-4-p1r-preregistration-v4-hostile-audit-v1.json
```
