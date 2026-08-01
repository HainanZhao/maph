# Cycle 4 P1R preregistration v2 hostile audit v1

`OBSERVED`: v2 corrects the documented CLI, frozen snapshot, four-term
(S_3) source/range ledger, and unexecuted FS status. It still fails historic
replay lifecycle separation.

Its `--check` evaluates live `PLAN.md` predicates that require P1R to remain
`ACTIVE` and no P2 route to be selected. Both conditions can change through
legitimate future gates. Simulated P1R completion and a later affirmative P2
selection both make the historic v2 check fail, despite the immutable
authorization snapshot remaining valid.

Historical replay must depend only on frozen snapshot/source bytes. A separate
operational preflight may evaluate the current PLAN, but it must not be part of
artifact-byte reproduction. No P1R mathematical conclusion is affected by
this containment record.

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_cycle_4_p1r_preregistration_v2_hostile.py \
  --check artifacts/cycle-4-p1r-preregistration-v2-hostile-audit-v1.json
python3 -m unittest tests/test_cycle_4_p1r_preregistration_v2_hostile_audit.py -v
```
