# Certified Quasi-Monte Carlo

This project builds an independently replayable exact/enclosure
evaluation path for figures of merit of rank-1 lattice rules.  Its
primary artifact is the evaluator and verifier; a curated conformance
oracle makes implementations falsifiable, while exhaustive certified
tables are supplementary archival data and comparison anchors.

The first target is intentionally narrower than the full proposal:

> Certify the squared shift-averaged worst-case error of a rank-1 lattice
> rule in the product-weight, unanchored Sobolev `B2` convention, and make
> every normalization and denominator visible in the certificate.

For modulus \(N\), generating vector \(z\), and nonnegative rational
product weights \(\gamma_j\), the frozen quantity is
\[
 e^2(z,N)=-1+\frac1N\sum_{k=0}^{N-1}
 \prod_{j=1}^d\left(1+\gamma_j
 B_2\!\left(\left\{\frac{kz_j}{N}\right\}\right)\right),
\qquad
 B_2(x)=x^2-x+\frac16.
\]

This is a pure rational. It is not silently identified with conventions
using \(2\pi^2B_2\), and it is not an error bound for a particular
integrand without a separately justified function-space norm.

## Current status

Phase 0 and implementation Cycles 001–008 are complete:

- exact `Fraction` evaluation of the frozen merit;
- an independent \(O(N^2d)\) RKHS double-sum oracle;
- deterministic JSON certificates with exact replay and tamper detection;
- a small exhaustive exact-CBC oracle for future fast-code validation;
- explicit quotienting of the forced candidate symmetry \(z\sim -z\);
- a corrected denominator formula for rational weights;
- exact verification of the proposal's first 62-bit NTT prime, its
  factorization, 2-adic capacity, and primitive root;
- a frozen first audit target: the 16-component prefix of the official
  UNSW fixed lattice with \(N=1024\) and \(\gamma_j=1/j^2\).
- a source-level audit of frozen LatNet Builder and QMCPy snapshots;
- an exact scaled-integer representation with signed reconstruction and
  CBC-difference bounds;
- a deterministic 16-prime, fully factored NTT schedule;
- direct modular evaluation with balanced CRT reconstruction;
- a small CRT-CBC certificate proving every winning branch; and
- an exact three-way benchmark on the frozen UNSW prefixes;
- a compiled `__int128` direct modular baseline;
- a validated single-prime radix-two NTT; and
- an exact valuation-stratified fast-CBC score mapping for
  \(U(2^m)\);
- a timestamped external-discrepancy gate; and
- an Arb-first \(N=2^{16},d=50\) decision experiment backed by a
  verified 40-prime schedule;
- a version-pinned FFTW plan transcript through length \(2^{18}\); and
- an executable Arb forward-error enclosure for LatNet's direct
  symmetric `CU:P2` product-weight evaluator, with a bit-identical
  compiled-LatNet midpoint transcript; and
- exact-polynomial/Arb certification of every selected component in
  three synthetic fast-CBC searches through \(N=64\).

Across the inspected, hash-frozen LatNet Builder and QMCPy snapshots and
the named public-distribution perimeter, no independently replayable
exact or enclosed lattice-merit path was supplied.  A merit produced
within that frozen toolchain therefore cannot be falsified from its
supplied artifacts alone.  This bounded toolchain finding—not the
rational absence of exhaustive published merit columns—is the project's
central motivation.

The release consequently leads with the evaluator, verifier, and a
preregistered few-hundred-entry conformance/oracle set.  The full
79,200-entry fidelity grid remains authorized and running because its
marginal cost is accepted, it has archival value, and Workstream C
requires certified CBC-side comparison anchors; it is presented as
supplementary data.  A preregistered six-paper sweep found no numerical
merit attached to the frozen vectors, so no producer-error bound is
needed for that perimeter. Future merit-bearing tables use
\(B_{\rm alg}(\mathcal M)=T_{\rm eval}(\mathcal M)+T_{\rm format}\);
CBC selection is outside that comparison.  The FFTW/LatNet replays are
numerical model validation, not part of the trusted base.

The full supply grid and weights are frozen.  A compiled prime-major
streaming pilot passed its frozen oracle, overflow, replay, and
throughput gates: 2.483 ns/update projects the confirmed
54.9-trillion-update workload to 1.58 node-days on the recorded
four-core node.  This authorizes the full exact throughput branch;
Cycle 013 has since closed the licensing/dependency gate: UNSW vectors
use keyed, non-embedded mode and the release graph contains no FFTW.
Cycle 014 has banked the full independently verified 3,740-prime
schedule. Cycle 015 closed the chunk-replay gate with hash-chained
chunks, three byte-identical forced-kill resumes, and 10/10
selected-entry replays. The Cycles 016–017 fidelity grid is now frozen
and running. Its first attempt correctly paused under the original
25% VPS drift alarm and is preserved; a human-authorized,
versioned +75% alarm retains the seven-node-day hard budget and all
certification predicates. Cycle 009 remains explicitly deferred to the
Workstream C entry gate.  Its compiled plain-`__int128` scorer now
matches the independent Python NTT through \(N=2^{12}\), its integrated
Arb/CRT/checkpoint preflight is banked, and the resumable target driver
mechanically refuses to start without the published-DOI certificate.

## Layout

- `src/exact_error.py`: exact kernel and merit evaluator.
- `src/certificate.py`: certificate generation and strict replay.
- `src/cbc.py`: small exact CBC oracle.
- `src/ntt_prime.py`: deterministic 64-bit prime/root audit.
- `src/scaled_integer.py`: integer representation and proved bounds.
- `src/crt.py`: bounded balanced reconstruction.
- `src/modular_error.py`: direct modular merit and CRT-CBC prototype.
- `src/ntt.py`: validated radix-two transform and correlation.
- `src/power2_fastcbc.py`: composite-\(2^m\) valuation mapping.
- `src/producer_error.py`: direct-producer binary64/Arb error replay.
- `src/format_bound.py`: exact decimal lexical-grid and half-cell bound.
- `src/radix2_model.py`: reference binary64 FFT and rational transform
  envelope.
- `native/direct_modular.c`: compiled direct modular baseline.
- `native/streaming_pilot.c`: prime-major incremental exact-table
  throughput pilot.
- `native/cycle009_ntt.c`: compiled plain-`__int128`
  valuation-stratified exact candidate scorer.
- `tools/numerical-crosscheck/`: release-excluded FFTW/LatNet
  `NUMERICAL` cross-check harnesses.
- `scripts/certify_rule.py`: certify a user-supplied rule.
- `scripts/verify_certificate.py`: replay a core certificate.
- `scripts/verify_engine_oracle.py`: authenticate the compact oracle or
  rebuild it byte-identically from both supplementary datasets.
- `scripts/audit_production_phase_completion.py`: require explicit,
  self-hashed evidence for every Cycles 013–019 deliverable and report
  missing evidence as pending rather than inferred success.
- `scripts/audit_phase0_target.py`: certify the frozen official prefix.
- `scripts/audit_workstream_b_reference_table.py`: certify every
  dimension of the frozen vector-only prefix.
- `scripts/audit_workstream_b_production_budget.py`: exact full-grid
  reconstruction and operation-count preflight.
- `scripts/audit_workstream_b_streaming_pilot.py`: prospective
  correctness/replay/throughput gate.
- `scripts/run_exact_cbc_oracle.py`: generate a small exact CBC rule.
- `data/phase0-targets.json`: frozen upstream target and checksum.
- `docs/project-charter.md`: full workstreams and standing orders.
- `docs/phase0-preregistration.md`: scope, gates, and stop conditions.
- `docs/mathematics.md`: normalization and denominator proofs.
- `docs/literature-audit.md`: primary-source state-of-practice audit.
- `docs/claim-ledger.md`: current verified/open/retired claims.
- `docs/status-2026-07-29.md`: initial results and next-cycle handoff.
- `docs/cycle-001-...` through `cycle-008-...`: gated cycle records.
- `docs/cycle-009-decision-layer-preregistration.md`: next-rung freeze.
- `certificates/cycle-009-compiled-ntt-gate.json`: compiled scorer
  replay against direct and independent Python mappings.
- `docs/workstream-b-discrepancy-preregistration.md`: external audit
  classification gate.
- `docs/workstream-b-cycle010-forward-error-report.md`: producer-bound
  experiments and their Cycle-011 trusted-base correction.
- `docs/workstream-b-cycle011-model-class-preregistration.md`:
  selection-free model-class bound and table-schema disposition.
- `docs/workstream-b-cycle011-model-class-report.md`: survey outcome,
  exact formatting component, and reference-transform gate.
- `docs/workstream-b-radix2-model-bound.md`: reference transform proof.
- `docs/workstream-b-literature-perimeter-preregistration.md` and
  `docs/workstream-b-literature-sweep-report.md`: bounded paper sweep.
- `docs/workstream-b-production-freeze.md`: grid, weights, artifact
  contract, and compute gate.
- `docs/workstream-b-streaming-pilot-report.md`: preserved failed run,
  corrected transcript, and mechanical production decision.
- `docs/licensing.md`: code/data licenses and third-party vector policy.
- `docs/cycle-013-licensing-and-dependencies.md`: G1 transcript.
- `docs/cycle-014-full-prime-schedule.md`: complete N−1 certificate
  schedule and independent replay.
- `docs/cycle-015-chunked-replay.md`: G3 forced-kill and selected-entry
  replay transcript.
- `docs/cycles-016-017-production.md`: fidelity freeze, preserved
  throughput pause, and versioned VPS disposition.
- `docs/paper-supply-side-draft.md`: engine-first methods-paper prose
  with result fields mechanically left pending until their gates close.
- `docs/post-release-optimization-register.md`: closed optimization
  queue and its bit-identical promotion predicates.
- `docs/roadmap.md`: gated workstreams.

## Quick start

Run from this directory:

```bash
python3 -m unittest discover -s tests -v

python3 scripts/certify_rule.py \
  --modulus 8 \
  --generator 1,3 \
  --weights 1,1/2 \
  --output certificates/example-n8-d2.json

python3 scripts/verify_certificate.py \
  certificates/example-n8-d2.json

python3 scripts/verify_certificate.py \
  certificates/workstream-b-unsw-prefix-reference-table.json \
  --dimension 7

python3 scripts/audit_phase0_target.py \
  --dimension 8 \
  --output certificates/unsw-j2-n1024-d8.json

python3 scripts/run_exact_cbc_oracle.py --modulus 31 --dimension 5
python3 scripts/audit_reference_ntt_prime.py
python3 scripts/build_prime_schedule.py --count 16
python3 scripts/run_crt_cbc.py
make -C native
python3 scripts/audit_ntt_power2.py

python3 -m venv .venv
.venv/bin/pip install -r requirements-arb.txt
.venv/bin/python -m unittest tests.test_shadow_decision -v
```

## Claim discipline

1. A certified rule merit is not a certified integration result until the
   integrand's norm in the stated space is bounded.
2. Exact evaluation of one vector is not exact certification of a CBC
   search path.
3. A floating-point winner is not certified optimal unless every branch is
   separated by enclosures or exactly tie-broken.
4. Public availability is not evidence that a table was generated in
   unverified arithmetic; implementation precision is audited, not assumed.
5. Scale estimates remain `PROJECTED` until measured on the implemented
   representation.
