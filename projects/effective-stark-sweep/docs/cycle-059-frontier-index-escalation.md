# Cycle 059 — FRONTIER odd-index escalation

**State:** `VERIFIED_EXACT_INVENTORY`; mathematical interpretation
remains `CONJECTURAL/DISCOVERY_CANDIDATE`.

The exact post-routing ledger covers all 1,818 FRONTIER rows.  It
exposes a semantic defect in the historical obstruction name:
`INDEX_GT_2` was emitted by

```text
shintani_index != 2 OR exactly_one_real_place_splitting fails
```

and therefore never meant that every recorded index was literally
greater than two.  Among its 1,100 rows the exact index distribution
is:

| index | 1 | 2 | 3 | 4 | 5 | 6 | 8 | 9 | 10 | 12 | 14 | 16 | 18 | 20 | 24 |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| rows | 271 | 13 | 75 | 342 | 6 | 230 | 68 | 7 | 37 | 32 | 5 | 4 | 7 | 2 | 1 |

Predicate separation gives:

- index not two, splitting predicate passes: 985;
- index not two, splitting predicate fails: 102;
- index two, splitting predicate fails: 13.

The escalation trigger fires on 88 odd indices above two:
`3:75`, `5:6`, `9:7`.  They occupy 38 real quadratic fields.  In 81
of the 88 rows the exactly-one-real-place splitting predicate passes,
so these are not artifacts of the historical disjunction.  Exact
fresh reruns of one case at each value reproduce:

- RQ-000294: index 3 (splitting predicate fails);
- RQ-002147: index 5 (splitting predicate passes);
- RQ-003093: index 9 (splitting predicate passes).

Their support-order patterns are concentrated at orders divisible by
three: 53 rows have `(2,6)`, 19 have `(4,12)`, seven have
`(2,6,18)`, with nine remaining rows in other patterns.  This
association is an exact census statistic, not yet a structural
theorem.

No prior proof tag is invalidated: every affected case was already
FRONTIER.  The consequence is a new W4 question—explain the occurrence
of odd maximal-abelian indices and their concentration in
3-primary support—while W4 itself remains closed behind the bulk and
transport gates.

Primary artifacts:

- `artifacts/frontier-index-inventory-v1.json`;
- `artifacts/frontier-odd-index-spotcheck-v1.json`.

