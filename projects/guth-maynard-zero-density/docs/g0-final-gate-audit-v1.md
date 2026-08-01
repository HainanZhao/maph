# Hostile final G0 gate audit v1

**Claim boundary — OBSERVED recommendation.** This fixed-scope audit checks the
evidence required by PLAN §6/WP0 and the Cycle-1/Cycle-2 preregistrations. It
is not the authoritative global reconciliation and does not itself change the
project gate or `PLAN.md`.

Run:

```sh
python3 proof/audit_g0_final_gate_v1.py --check
```

The audit records a `PASS` recommendation, based on:

- 24 exact Cycle-1 labeled comparisons;
- 7 reconciled Stream-B source/application nodes;
- 26 exact Stream-C v5 two-route labels;
- all inherited v1 dependency nodes mapped to bounded evidence;
- source-manifest v3, official DSpace/SWORD source closure, and route-hash
  agreement; and
- all four preregistered route commands meeting the observed strict runtime
  and RSS ceilings.

Route independence is tested at the replay-source level: Route A v5 has no
Route-B replay/artifact dependency, Route B v5 has no Route-A replay/artifact
dependency, and the shared official-source checker has neither route
dependency. The reconciliation occurs only after both sealed route outputs.

`PLAN.md` was consulted to identify WP0 requirements but is deliberately not
hash-frozen. A future authoritative decision must update PLAN without making
this audit stale. The recommendation remains `OBSERVED`; the `PROVED` tags it
reports retain the narrow conditional boundaries of their underlying records.
