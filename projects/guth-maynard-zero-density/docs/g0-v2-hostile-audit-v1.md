# Bounded hostile audit of corrected G0 v2

## Outcome

`OBSERVED`: normal `python3 proof/reconcile_g0_full_v2.py --check` completed
successfully under CPython 3.12.3. `PROVED`: the separately sealed
published-source v5 record identifies the selected MIT DSpace item as a
`Publication` and records the checked official theorem/proof scope.
`OBSERVED`: the six registered resource routes all have sealed, strictly
under-ceiling host measurements.

`OBSERVED CONTAINMENT`: the v2 standalone runtime assertion is not robust
under optimized Python. The hostile probe

```sh
python3 -O proof/reconcile_g0_full_v2.py --check
```

exited zero because CPython removes bare `assert` statements under `-O`.
This does not change the literal normal replay result, but v2 must not be
described as an optimization-robust runtime pin. It is preserved in
[the audit artifact](../artifacts/g0-v2-hostile-audit-v1.json), not silently
repaired in place.

## Scope and replay

The audit checks only the corrected v2 package: its ordinary frozen command,
the source-classification v5 record, exactly six named resource routes and
strict resource semantics, plus the hostile optimization probe. `OBSERVED`:
it is not a G0 decision and proves no new density estimate or short-interval
result.

```sh
python3 proof/audit_g0_v2_hostile_v1.py --check
```

The required operational containment is an explicit non-optimized CPython
3.12.3 preflight before delegating to v2. The later runtime-v2/G0-v3 pair
implements that correction while retaining the v2 record unchanged.
