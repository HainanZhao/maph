# Gated roadmap

## Phase 0 — exact ground truth

Status: complete, including the bounded flagship-source audit.

- Freeze one named kernel convention.
- Implement exact and independent-oracle evaluation.
- Implement deterministic certificate replay.
- Freeze one public audit target.
- Audit the first proposed NTT prime.
- Correct denominator, symmetry, and scale assumptions.

Gate: all tests pass and no claim exceeds `docs/claim-ledger.md`.

## Phase 1 — certified engine

Status: direct compiled baseline and single-prime power-of-two mapping
complete; multi-prime compiled engine open.

1. ~~Derive a signed integer bound for candidate-score differences.~~
2. ~~Freeze an individually verified prototype NTT-prime schedule.~~
3. ~~Implement direct modular scaled-product evaluation.~~
4. ~~Reconstruct exact fractions and crosscheck tractable cases.~~
5. Add Arb only through a pinned dependency and adversarial enclosure
   tests.
6. ~~Implement a compiled direct modular evaluator.~~
7. ~~Validate a single-prime radix-two NTT and the composite-\(2^m\)
   valuation mapping.~~
8. Implement the Cycle-009 three-representation ladder and validate its
   balls on \(N\le2^{12}\).
9. ~~Compile and validate the single-prime stratified NTT through
   \(N=2^{12}\).~~ Run it prime-major across the 40-prime
   schedule, and reconstruct candidate differences at
   \(N=2^{16},d=50\).
10. Bank the plain-reduction correctness transcript, then introduce
    Montgomery/lazy reduction and demand bit-identical replay.
11. Add checkpoint/replay manifests before reference-scale search.

Kill gate: if CRT/NTT results differ from exact ground truth once, halt
optimization and isolate the representation error.

## Phase 2 — certified evaluator conformance and reference anchors

Status: the frozen distribution sites and six-paper primary-literature
perimeter contain no merit attached to the frozen vectors. The
classification branch is closed for that perimeter. The engine is the
primary artifact; a preregistered, structurally diverse oracle set is
the principal software-conformance data product; the exhaustive grid is
supplementary archival data and supplies Workstream C comparison
anchors. The grid, weights, artifact contract, exact precompute budget,
source policy, full prime schedule, and chunk replay are closed.
Fidelity production is active under the versioned VPS monitor. Its
first +25% drift pause is preserved; the human-authorized v2 alarm is
+75%, while the seven-node-day budget and all certification gates
remain unchanged.

1. ~~Freeze a source-specific discrepancy protocol and quarantine any
   prematurely exposed values.~~
2. ~~Survey the frozen set for merit-column presence and observed
   precision.~~
3. ~~Remove CBC selection from the classification bound.~~
4. ~~Implement exact lexical \(T_{\rm format}\).~~
5. ~~Implement and prove the reference radix-two transform component
   for the explicit model class \(\mathcal M\), with sensitivity
   variants.~~
6. ~~Freeze and inspect a bounded six-paper primary-literature
   perimeter.~~
7. Compose kernel construction, state updates, convolution products,
   normalization, and accumulation into the complete
   \(T_{\rm eval}(\mathcal M)\), when a merit-bearing target requires
   it.
8. Freeze
   \(B_{\rm alg}(\mathcal M)=T_{\rm eval}(\mathcal M)+T_{\rm format}\)
   only for merit-bearing targets.
9. Only after step 8, preregister and fetch a new unseen merit value.
10. ~~Freeze FFTW plan trees and direct LatNet replays as numerical
   model validation outside the certification chain.~~
11. ~~Freeze the fidelity/usability grid, weights, artifact contract,
    and per-cell conservative prime budgets.~~
12. ~~Archive and classify source terms, freeze keyed-vector mode for
    `UNCLEAR` sources, remove FFTW from the release graph, and choose
    artifact licenses.~~
    Full input files are fetched transiently and hash-pinned for runs,
    but are not redistributed.
13. ~~Generate and independently verify the full 3,740-prime production
    schedule with complete N−1 certificates and byte-identical
    regeneration.~~
14. ~~Implement the prime-major streaming evaluator and pass the frozen
    \(N=1024,d=256,\gamma_j=j^{-2}\) pilot.~~
15. ~~Recompute the full-grid wall-time projection from the pilot and
    apply the prospectively frozen go/no-go predicate.~~
16. ~~Implement hash-chained chunks, forced-kill resumability,
    selected-entry replay below the 1% payload ceiling, universal
    overflow checks, and complete run manifests.~~
17. Produce chunked tables in increasing \(N\), with the frozen
    throughput-drift monitor and post-run audit.
18. Freeze and extract the engine conformance/oracle set independently
    of observed merit values; publish the full fidelity grid as
    supplementary data.

Gate: every supplied entry has a replayable certificate and upstream
hash. The 54.9-trillion combined incremental count has a passing local
projection; source/license, full-schedule, chunk-replay, and fidelity
pre-run gates are closed. The active v2 fidelity run must seal and pass
100 selected replays plus three frozen oracle checks before Cycle 018
computation begins.

## Phase 3 — number-theoretic constructions

1. Run the preregistered Cycle 009 Arb-106 decision experiment and bank
   its escalation count/depth histogram before making any certified-CBC
   construction claim.
2. Exact two-dimensional Zaremba indices and continued-fraction
   controls.
3. Certified enumeration bounds in dimension three.
4. Totally-real unit candidates only after the embedding-to-rule map
   is explicit and executable.
5. Compare every new construction against the same certified merit
   convention and weights.

Gate: no asymptotic statement is presented as a competitive finite-\(N\)
constant.

## Phase 4 — application pilot

Select one preintegrated payoff or UQ integrand only after documenting:

- the exact transformation;
- monotonicity/smoothing hypotheses;
- the relevant function-space membership;
- a norm bound or an explicit empirical label;
- randomized-shift protocol and confidence assumptions.

Gate: the report separately labels rule merit, RKHS inequality,
integrand norm, statistical interval, discretization/model error, and
empirical comparisons.

## Production-phase completion audit

`scripts/audit_production_phase_completion.py --require-complete` is
the terminal Cycles 013–019 gate.  It requires 14 independent items:
the closed G1–G3 certificates; sealed fidelity/usability audits; the
298-case oracle; authenticated four-asset release package; repository
tag; published DOI response; finalized supply-side prose; sealed
Cycle-009 histogram; post-release optimization register; and the
recorded human Workstream-D disposition.  Missing evidence is
`PENDING`, never promoted by absence.
