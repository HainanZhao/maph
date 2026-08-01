# Cycle 2 — Stream B hostile Route A/Route B reconciliation

Claim boundary: `OBSERVED` is the status of this reconciliation. It compares
the frozen Route A v2 and Route B v1 reports against the Cycle-2
preregistration and Stream A ledger. It neither changes those reports nor
converts their source audits into a new zero-density proof.

## Outcome

`OBSERVED`: no contradictory checked formula, source hash, range, detector
identity, multiplicity conversion, or Montgomery structural term was found.
The canonical status is nevertheless only **Stream B narrow PASS**. It is not
a G0 PASS: Stream C remains outside this comparison.

`OBSERVED`: three open coverage mismatches prevent the reports from counting
as independent two-route verification of the entire Stream-B application:

- Route A v2 does not explicitly enumerate the three Theorem 1.1 structural
  terms; Route B does.
- Route A v2 records MVT structural terms but not the strict positive
  residual needed in the (L>T^\alpha) branch; Route B does.
- Route A v2 records the two-sided shell conversion but not the full
  Type-I/Type-II exponent comparison and dyadic reassembly; Route B does.

These are evidence-coverage failures, not evidence of a false published
formula. The corresponding falsifiers are retained in the machine record.

## Reconciled evidence

`PROVED` within each frozen route: both pin the same GM, MP, Montgomery, HSW,
and Bui--Heath-Brown inputs where they overlap. This reconciliation also
checks the preregistered GM source tar hash in addition to the extracted TeX
hash used by both routes.

`OBSERVED`: detector inclusion, local multiplicity, two-sided height
conversion, smoothing/extraction, coefficients, both (k) regimes, and
Montgomery's theorem agree at the level their source reports state. Route B
adds a direct eta-series argument excluding real non-trivial zeros; Route A's
two-sided inequality is compatible with this stronger detail.

`CONTAINED`: Route A's unqualified word “PASS” and Route B's “NARROW PASS”
are a label-scope mismatch. The preregistration requires Stream C before G0
PASS, so the only safe canonical label is `STREAM_B_NARROW_PASS`; G0 remains
`OBSERVED`.

`CONTAINED`: Route A's detector-comparison wording calls a beta cutoff part of
the exact detector identity. The beta restriction belongs to the counted
(R_{II}(\sigma,T)) class, while the Type-I detector itself is beta-free.
The complement inclusion remains valid; the reconciliation records the more
precise wording without changing Route A.

`OBSERVED` historical reproducibility defect: Route A v2 embeds
`replay.wall_time_ns`, so rerunning its successful replay changes the raw
artifact bytes. Its `mathematical_and_source_audit_sha256` is stable and is
therefore the Route-A comparison identity here. The raw Route-A hash is kept
only as a seal-time provenance observation; timing-only byte drift is not a
mathematical mismatch. The reconciliation certificate itself embeds no timing
and is byte-stable.

## Next action

`OBSERVED`: if independent two-route agreement is required, a versioned
Route A continuation must add exact rows for the three structural terms, the
strict residual, and the final reassembly. The frozen Route A v2 and Route B
v1 artifacts must remain unchanged.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/reconcile_cycle2_stream_b_routes_v1.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-reconciliation-v1.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_b_route_reconciliation_v1.py
```

The canonical mapping table, input hashes, and all mismatch/falsifier rows
are stored in
[cycle-2-stream-b-route-reconciliation-v1.json](../artifacts/cycle-2-stream-b-route-reconciliation-v1.json).
