# Workstream B certified-table production freeze

Frozen: 2026-07-29T06:42:00Z

## Contribution

Workstream B supplies the merit tables missing from the public
generating-vector distributions.  It does not imply that the producers
published incorrect numbers; the frozen site-and-literature perimeter
contains no attached numbers to classify.

Proposal Deliverable 2 is replaced by:

> Certified reference-merit tables for distributed generating vectors:
> complete producer-weight coverage over the frozen public grid, a
> small standard cross-weight grid, SHA manifests, per-entry
> certificates, and independent one-command replay.

## Fidelity grid

Two public UNSW families are frozen:

- fixed `lattice-29102-N.3600` vectors for
  \(N=2^{10},2^{11},\ldots,2^{20}\);
- extensible `lattice-39102-1024-1048576.3600`, evaluated over the same
  modulus ladder.

For both, report every prefix dimension \(1,\ldots,3600\) under the
producer-documented product weights \(\gamma_j=j^{-2}\).  The frozen
quantity is the squared shift-averaged worst-case error in the
Bernoulli-\(B_2\), beta-zero convention.

## Usability grid

At \(N=2^{10},2^{15},2^{20}\) and dimensions \(16,64,256\), report both
families under:

- \(\gamma_j=j^{-1}\), a slow-decay stress profile;
- \(\gamma_j=j^{-2}\), reusing the fidelity grid;
- \(\gamma_j=j^{-3}\), a faster-decay comparison profile.

This grid is frozen before merit production.  No profile may be added
or removed after seeing results.

## Artifact contract

The top-level SHA-256 manifest authenticates sources, normalization,
weights, budget, chunks, and verifier.  Prime-major chunks permit
streaming evaluation.  Each logical entry records:

- source and generator-prefix hashes;
- \(N,d\), normalization, and weight profile;
- an exact reduced rational or sufficient CRT residues;
- the proved signed reconstruction bound;
- the ordered verified primes and two overflow-check primes;
- deterministic reconstruction status and claim boundary.

The verifier must replay one selected entry without processing unrelated
cells.  The existing 16-prefix table is the format prototype, not the
final production schema.

At the worst cell an entry carries 3,738 work residues, or 29,904
bytes, plus two universal overflow residues and metadata.  Charging the
worst count to all fidelity entries gives a conservative 2.368 GB
decimal residue upper bound.  The release is expected to be roughly
2–3 GB before compression, with chunk-selective downloads.

## Precompute gate

The budget uses the corrected rational-weight bound.  A conservative
work-prime count is
\[
 \left\lceil
 \frac{\text{proved reconstruction bits}}{61}
 \right\rceil,
\]
because every admitted work prime in the frozen family is greater than
\(2^{61}\).  The actual ordered schedule and cumulative product must
still be generated and verified before compute.

The worst frozen cell,
\(N=2^{20},d=3600,\gamma_j=j^{-2}\), already needs 228,015 proved
reconstruction bits and a conservative 3,738 work-prime budget.  The
standard \(j^{-3}\) stress cell at the same full dimension would be even
larger, which is why alternate weights are confined to the small grid.

The compiled prime-major streaming pilot at
\(N=1024,d=256,\gamma_j=j^{-2}\) has now passed its prospectively
frozen throughput, oracle-agreement, overflow, and replay gates.  Its
2.482743 ns/update median projects the complete incremental count to
1.578 node-days, below the seven-node-day ceiling.  The full exact
throughput branch is therefore authorized; the exact/Arb tier fallback
is inactive.

The production count assumes incremental within-column running-product
reuse: all prefixes are emitted during one dimension-ordered pass for
each prime. Per-entry restart from dimension one is forbidden. The
prospective node-day and replay-overhead decision thresholds, and the
mechanical exact/Arb tier fallback, are frozen in
`docs/workstream-b-streaming-pilot-preregistration.md`.

This does not yet launch production.  The remaining blockers are
source provenance/license review and vendoring, generation and
verification of the full deterministic prime schedule, and the
production chunk/selected-entry replay implementation.  The pilot
outcome and its preserved failed first transcript are documented in
`docs/workstream-b-streaming-pilot-report.md`.

The complete machine-readable freeze is
`data/workstream-b-production-freeze.json`; exact budgets are in
`certificates/workstream-b-production-budget.json`.
