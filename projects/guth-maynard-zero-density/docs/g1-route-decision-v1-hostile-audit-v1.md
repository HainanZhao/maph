# G1 route-decision v1 hostile audit v1

## Outcome

`OBSERVED`: the sealed v1 route-decision package replays normally and rejects
both `-O` and `-OO`, but it fails route-predicate completeness. It is
contained and must not be promoted as the G1 decision authority.

## Defects

The frozen G1 rule requires distinct evidence: a trace feature absent from the
cubic terms for P2A; a consistent energy/affine obstruction for P2B; a named
decomposition or branch loss after propagation of local candidates for P2C;
and separate labeled evidence for a combination. The v1 script instead makes
any retained row select P2A, then combines that proxy with fixed booleans for
P2B, P2C, and a combination. Its current zero-retained result happens to be
`NO_SELECTION`, but the executable does not faithfully encode the affirmative
branches of the frozen rule.

The v1 decision artifact also omits the adjudicator path and SHA-256. Frozen
input hashes do not bind the executable that produced the decision.

## Required correction

A v2 no-selection-only adjudicator must require zero retained rows and fail
closed if that premise changes; it must never infer an affirmative route from
a row count. Any affirmative route needs a separately sealed labeled-evidence
artifact for every frozen predicate. The v2 artifact must record and replay
the adjudicator identity, and its tests must cover normal mode, `-O`, `-OO`,
input tampering, and a retained-row counterfactual.

## Replay

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_g1_route_decision_v1_hostile.py \
  --check artifacts/g1-route-decision-v1-hostile-audit-v1.json
python3 -m unittest tests/test_g1_route_decision_v1_hostile_audit.py -v
```
