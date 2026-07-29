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
9. Compile the stratified NTT, run it prime-major across the 40-prime
   schedule, and reconstruct candidate differences at
   \(N=2^{16},d=50\).
10. Bank the plain-reduction correctness transcript, then introduce
    Montgomery/lazy reduction and demand bit-identical replay.
11. Add checkpoint/replay manifests before reference-scale search.

Kill gate: if CRT/NTT results differ from exact ground truth once, halt
optimization and isolate the representation error.

## Phase 2 — certified table supply

Status: the frozen distribution sites and six-paper primary-literature
perimeter contain no merit attached to the frozen vectors. The
classification branch is closed for that perimeter. The grid, weights,
artifact contract, and exact precompute budget are frozen. The compiled
streaming pilot authorizes the full exact throughput branch; production
compute remains gated on sources, the full prime schedule, and chunk
replay.

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
12. Vendor all fixed and extensible upstream files with
    license/provenance review and SHA freezes.
13. ~~Extend and verify the deterministic prime schedule required by
    the pilot only.~~
14. ~~Implement the prime-major streaming evaluator and pass the frozen
    \(N=1024,d=256,\gamma_j=j^{-2}\) pilot.~~
15. ~~Recompute the full-grid wall-time projection from the pilot and
    apply the prospectively frozen go/no-go predicate.~~
16. Produce chunked tables in increasing \(N\), with independent entry
    replay and two-prime overflow checks.

Gate: every supplied entry has a replayable certificate and upstream
hash. The 54.9-trillion incremental count now has a passing local
projection, but source/license and full-schedule gates still forbid
production launch.

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
