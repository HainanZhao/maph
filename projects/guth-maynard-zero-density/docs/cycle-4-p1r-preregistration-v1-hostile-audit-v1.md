# Cycle 4 P1R preregistration v1 hostile audit v1

`OBSERVED`: P1R preregistration v1 is contained with
`FAIL_REPLAY_LIFECYCLE_SOURCE_AND_STATUS`.

The literal documented replay command does not match the parser. The v1
artifact also pins mutable live `PLAN.md`; future gate updates mandated by
repository policy would invalidate an otherwise historic sealed record. Its
four-term (S_3) scale balance is algebraically correct but cites the
two-term Refined (S_3) proposition rather than the later four-term
(S_3)-Bound proposition and omits that result's (N\ge T^{3/4}) gate.
Finally, P1R-FS is marked `PROVED` while explicitly unexecuted.

The current PLAN authorizes P1R-FS execution now that a preregistration exists.
P1R-CRR search remains forbidden until its separate formalization fields are
sealed. Neither conclusion is a mathematical obstruction or compatibility
result.

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_cycle_4_p1r_preregistration_v1_hostile.py \
  --check artifacts/cycle-4-p1r-preregistration-v1-hostile-audit-v1.json
python3 -m unittest tests/test_cycle_4_p1r_preregistration_v1_hostile_audit.py -v
```
