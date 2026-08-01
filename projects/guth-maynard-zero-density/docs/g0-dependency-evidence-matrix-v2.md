# G0 dependency/evidence matrix v2

**Claim boundary — OBSERVED.** This deterministic inventory cross-references
all current Cycle-1/Cycle-2 JSON artifacts with the inherited G0 dependency
graph. It reports prior tags and evidence coverage; it neither rechecks the
underlying theorems nor declares G0 PASS.

Run:

```sh
python3 proof/audit_g0_dependency_evidence_v2.py --check
```

The matrix contains every inherited v1 graph node plus the local-pair-kernel,
source-manifest, and full-G0 nodes. Every row gives the required independent
route evidence, present route evidence, source/hypothesis evidence, open gaps,
and the validity boundary of the reported tag.

The audit includes every JSON object directly under `artifacts/` at build time,
apart from its own output (excluded only to avoid a self-referential hash
cycle). Source-manifest v2 is explicitly included.

The builder runs its coverage check without rewriting the manifest. If a new
direct source appears or its metadata has no reviewed row, the matrix records
`STALE_OR_INCOMPLETE` and adds a correction-required gap rather than silently
changing the frozen manifest.

Two G0 blockers remain explicit:

- Route A v3 does not independently pin the archival explicit-formula source
  closure; Route A v4 is required before a two-route Stream-C/G0 closure.
- Per-route evidence for the preregistered 60-second / 256-MiB G0 resource
  condition is not yet recorded for every current Stream-B and Stream-C route.

The matrix also enumerates all `wall_time_ns` occurrences. Earlier mathematical
artifacts with embedded timing have mutable raw bytes; the documented Stream-B
Route-A v2 and Stream-C Route-A v2 defects are contained only by canonical
semantic identities and later corrections. The isolated Route-A v3 performance
artifact is intentionally non-mathematical. For every timing-bearing artifact,
the inventory records a canonical content hash with `wall_time_ns` removed,
not a misleading raw-byte identity.

`OBSERVED` containment gap: the preserved Stream-C two-route reconciliation v1
records the raw hash of the timed Route-A v1 artifact. Replaying Route A v1 can
therefore stale that reconciliation certificate without changing its
mathematical content. The matrix retains this as a required versioned,
timing-free reconciliation correction; it does not modify the historical v1
record.
