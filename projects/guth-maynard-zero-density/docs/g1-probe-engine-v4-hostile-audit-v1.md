# Hostile audit of the G1 v4 promotion boundary

`OBSERVED`: the pinned v4 operational boundary is ready for its two fresh,
unverified production executions. The audit checks the exact engine,
adjudicator, manifest, and command-document identities; rejects optimized
execution; confirms there is no v4 resume path; and verifies that one output
cannot promote itself.

The separate standard-library adjudicator requires distinct A/B fresh paths,
complete screen/structural/validation accounting, driver-chain and resource
checks, and byte-identical timing-independent observations before it may emit
an `EMPIRICALLY_RECONCILED` discovery artifact. This remains a replay-based
finite observation, not an independent mathematical proof.

```sh
python3 projects/guth-maynard-zero-density/proof/audit_g1_probe_engine_v4_hostile_v1.py --check
```
