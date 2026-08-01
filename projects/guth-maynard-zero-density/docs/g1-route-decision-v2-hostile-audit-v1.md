# G1 route-decision v2 hostile audit v1

`OBSERVED`: v2 passes hostile replay. It binds the adjudicator executable,
replays the sealed zero-retained record, rejects `-O` and `-OO`, rejects an
actual mutated frozen input, and fails closed for retained-row and
validation-row counterfactuals.

The promoted scope remains narrow: G1 closes only as `NO_SELECTION` for the
sealed zero-retained branch. P2A, P2B, P2C, and combinations are not selected
and are not refuted. The package authorizes no P2 theorem search or
replacement screen without a new `PLAN.md`-authorized preregistration.

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/audit_g1_route_decision_v2_hostile.py \
  --check artifacts/g1-route-decision-v2-hostile-audit-v1.json
python3 -m unittest tests/test_g1_route_decision_v2_hostile_audit.py -v
```
