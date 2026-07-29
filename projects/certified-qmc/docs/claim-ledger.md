# Claim ledger

Date: 2026-07-29

## VERIFIED

- The frozen `B2` product merit is rational for rational weights.
- Its reduced denominator divides
  \(N\prod_j(6\,\mathrm{den}(\gamma_j)N^2)\).
- The implementation's single sum matches an independent RKHS double
  sum on the regression set.
- Core certificates replay deterministically and detect mutation.
- The exact CBC oracle chooses a true per-stage minimum on its tested
  small cases.
- The merit has the exact candidate symmetry \(z\sim N-z\).
- For integral normalized weights, \(N=2^{20},d=100\), the stated
  master denominator has bit length 4,279.
- `4611685941117976577` is prime,
  \(p-1=2^{33}\cdot311\cdot1726273\), and 3 is a primitive root.
- The frozen UNSW upstream file had 57,600 bytes, 3,600 lines, and the
  recorded SHA-256 when downloaded on the freeze date.
- At the audited LatNet Builder commit, lattice merits are represented
  by `double`, fast products use double FFTW, and argmin selection uses
  an ordinary floating-point comparison.
- At the audited QMCPy commit, no exact/enclosed lattice-merit evaluator
  or certified CBC path was discovered.
- Across the named, hash-frozen LatNet Builder/QMCPy revisions and
  public-distribution perimeter, no independently replayable exact or
  enclosed evaluation path was supplied.  A merit produced within that
  frozen path is therefore not falsifiable from the supplied artifacts
  alone.  This claim is perimeter-bounded, not universal.
- The scaled merit and CBC candidate-difference numerators satisfy the
  signed bounds recorded in Cycle 002.
- The deterministic first 16 `c*2^32+1` primes, their complete
  factorizations, and primitive roots replay exactly.
- Direct modular sums plus bounded balanced CRT reproduce the rational
  oracle.
- The frozen \(N=31,d=5\) CRT-CBC certificate proves every
  candidate-minus-winner difference nonnegative and matches the
  rational CBC oracle.
- All three exact evaluation paths agree on frozen UNSW prefixes at
  dimensions 2, 4, 8, and 16.
- The compiled `__int128` evaluator matches the Python modular oracle
  on the frozen prefixes and deterministic random regressions.
- The radix-two NTT matches quadratic cyclic convolution over the first
  audited 62-bit prime.
- The valuation strata partition every nonzero residue modulo \(2^m\).
- The stratified NTT mapping reproduces every direct modular candidate
  score on the frozen \(N=1024\), dimension-9 stage and small
  regressions. This is internal implementation agreement, not agreement
  with a published merit value.
- The deterministically extended 40-prime schedule replays completely
  and covers the \(N=2^{16},d=50\) final bound plus two overflow primes.
- The reference double-double audit balls contain their exact rational
  operation and score oracles on the regression set.
- With python-flint 0.9.0 / FLINT 3.6.0 pinned, the reference ladder
  exercises double-double separation, Arb-128 separation after a
  near-overlap, and exact fallback on a forced tie.
- The pinned FFTW 3.3.10 `FFTW_ESTIMATE` plan trees and `fftw_flops`
  counts replay identically for forward and inverse radix-two lengths
  through \(2^{18}\).  This is verified plan metadata, not by itself a
  transform-error proof.
- A compiled LatNet direct evaluator at the audited source/submodule
  commits produces binary64 words identical to the enclosed midpoint
  replay on all three frozen synthetic cases at 17 displayed digits.
- The frozen UNSW collection schema has exactly two columns—dimension
  and generating-vector component—and no published merit column.
  The current Workstream B target therefore needs certified reference
  merits, not \(B_{\rm alg}\).
- Finite decimal merit lexemes and their formatting half-cells are
  computed exactly under the declared round-to-nearest lexical model.
- For the declared reference radix-two model, the rational transform
  factor \(((1+\eta)^L-1)\|x\|_1\) encloses the Arb-replayed reference
  DFT errors on the frozen validation suite.  This is a transform
  component, not yet a complete evaluator bound.
- Every dimension \(1,\ldots,16\) of the frozen UNSW prefix has a
  replayable exact reference-merit certificate.  This does not certify
  the unvendored remainder of the 3,600-component source.
- The frozen six-paper primary-literature perimeter was inspected after
  preregistration. Four papers print numerical merits or FOMs, but none
  attaches one to a frozen `lattice-29102` or `lattice-39102` vector.
- The frozen full production grid has exact precompute budgets. Its
  worst fidelity cell
  \(N=2^{20},d=3600,\gamma_j=j^{-2}\) needs 228,015 proved
  reconstruction bits and a conservative 3,738 work-prime budget.
- The current reference-table verifier independently replays a selected
  dimension with one command.
- The corrected compiled prime-major streaming pilot matches the
  independent Python modular oracle on all 25 selected residues, writes
  every prefix for 151 work and two universal overflow primes, and
  replays all five checkpoint digests.
- The pilot's first failed transcript is retained. It exposed and then
  isolated a native constant-factor error before authorization; the v2
  preregistration changed no acceptance threshold.
- The Cycle-013 release graph and clean-room build contain no FFTW
  reference or linked object. The direct evaluator links only the C
  runtime; the frozen OpenMP streaming kernel links only the compiler
  OpenMP runtime and C runtime.
- Archived terms snapshots classify the UNSW lattice page and Magic
  Point Shop as `UNCLEAR`, and frozen QMCPy as `REDISTRIBUTABLE` under
  Apache-2.0. Production therefore uses keyed merits without embedded
  vectors and requires no licensing escalation.
- The full ordered production schedule contains 3,738 work primes and
  two universal overflow primes. An independent code path verifies all
  3,740 complete-factorization Lucas/Pocklington N−1 certificates,
  primitive roots, and 2-adic valuations; two generator reruns are
  byte-identical to the banked schedule.
- The chunked production driver resumes after literal `SIGKILL` at
  three preregistered boundaries to byte-identical sealed trees. Ten
  selected entries replay exactly, pass both universal overflow primes,
  match independent Python oracles, and touch at most 0.8529% of pilot
  payload.

## ENCLOSED

- The frozen direct, symmetric, unilevel LatNet `CU:P2`
  product-weight evaluation graph has an executable binary64
  forward-error ball.  Independent Arb sum-product targets are
  contained on the preregistered adversarial cases.
- For the frozen synthetic fast-CBC searches at \(N=16,32,64\), every
  selected component is a certified mathematical minimizer under
  exact polynomial comparison plus Arb separation.  Three stages have
  exact polynomial ties.  This does not supply a general FFTW error
  bound.

## PREREGISTERED

- No Workstream B external merit comparison may begin without the
  timestamped model-class discrepancy gate.  Selection optimality is
  excluded; future bounds are
  \(T_{\rm eval}(\mathcal M)+T_{\rm format}\).
- Workstream B production uses the frozen fidelity/usability grid and
  artifact contract. Source licensing, the full prime schedule, and
  chunk replay/run hygiene are closed gates.  The versioned v2 fidelity
  run is active; no production result is promoted until its sealed
  post-run audit passes.
- The engine conformance/oracle set is selected structurally before
  merit extraction.  It spans modulus scale, prefix dimension, all
  three frozen weight profiles, full tractable prefixes, and
  adversarial exact-decision cases.  It is not a representative sample
  of rule quality.

## EXPLICITLY DEFERRED GATES

- The \(N=2^{16},d=50\) Cycle 009 run remains preregistered with
  compiled Arb-106 first and exact CRT for unresolved comparisons. It is
  deferred to the Workstream C entry gate. It accepts only an exact-CRT
  escalation count below 803 over 802,767 fixed comparisons and must
  report the escalation-depth histogram before any certified-CBC
  construction claim.

## NUMERICAL

- Binary64 agrees with conversion of the exact result within the
  preregistered tolerance on 100 frozen pseudorandom small cases.
- Direct Python evaluator timings in the Cycle-005 benchmark.
- Compiled direct-baseline timings in Cycle 006 and direct-versus-NTT
  score timings in Cycle 008.
- The streaming pilot measured 2.482743 aggregate wall ns/update on
  four visible cores, projecting the confirmed 54.901-trillion-update
  workload to 1.577618 node-days with 3.7001% replay overhead.  This is
  a local measurement, not a portable performance guarantee.
- The first Cycles 016–017 production attempt correctly paused after
  5.013504 billion updates at 3.653537 aggregate ns/update, above its
  prospectively frozen +25% VPS drift alarm. Same-host
  single-process diagnostics remained below that ceiling. The partial
  hash-chained run is preserved and no partial merit is promoted.
- The human-authorized v2 monitor uses a versioned +75% VPS drift
  alarm (4.344801 ns/update), whose boundary projects 2.704 node-days.
  The seven-node-day hard budget and all certification gates are
  unchanged. The v2 fidelity computation is in progress; no production
  table is yet promoted.
- The pinned FFTW plans, compiled LatNet midpoint matches, and synthetic
  fast-CBC transcripts validate that the proposed model class is
  realistic.  They are outside the Workstream B certification chain.

This is a regression fact, not an enclosure.

## PROJECTED

- A compiled multi-prime NTT is expected to be necessary for
  production-scale exact CBC.
- A three-representation CBC may make most decisions by fast shadow
  arithmetic and reserve exact CRT reconstruction for overlaps.
- The reference scale may fit in commodity-node memory.

No tie-rate projection is promoted.  The Workstream B runtime
projection is promoted only to `NUMERICAL` under the recorded pilot
hardware and implementation.

## OPEN

- Whether A1/A3 is novel beyond the two maintained source snapshots
  audited in Cycle 001.
- Whether the official full table reproduces under the exact stated
  convention.
- Compiled multi-prime valuation-stratified NTT scoring.
- A production-cost compiled double-double radius propagated through
  the valuation-stratified score kernel.
- Certified floating/Arb separation for CBC comparisons.
- Exact CRT reconstruction of compiled fast-CBC score differences.
- Nonrational merit enclosures.
- Optional appendix completion of the full
  \(T_{\rm eval}(\mathcal M)\) composition across kernel
  construction, state updates, convolution, normalization, and
  accumulation. It is off the critical path for the closed frozen
  perimeter, but remains a gate for any future merit-bearing table.
- Selection of a new, unseen merit-bearing Workstream B target after
  its \(B_{\rm alg}(\mathcal M)\) passes. Previously exposed repository
  examples are protocol contaminated and remain unclassified.
- Certified Zaremba enumeration.
- Competitive totally-real unit constructions.
- Any application-level error statement.

## RETIRED OR CORRECTED

- `6^d N^(2d+1)` as the universal rational-weight denominator:
  corrected by the weight-denominator product.
- The 4,743-bit reference denominator as an exact consequence of that
  formula: corrected to 4,279 bits for integral normalized weights.
- The raw unquotiented `<0.1%` exact-tie expectation: retired. Cycle
  009 replaces it with a sign-quotiented exact-CRT escalation-rate
  predicate.
- “Five further verified 62-bit siblings”: not inherited without an
  explicit list and individual certificates.
- “Under an hour” and “minutes, trivially parallel”: retained only as
  proposal aspirations pending implementation benchmarks.
- “Industry consumes these exact tables”: narrowed to a public-table
  audit target until usage evidence is documented.
- A plan-specific FFTW proof as a Workstream B blocker: retired.  The
  historical producer is generally unrecoverable; FFTW reproduction is
  numerical model validation, not trusted evidence.
- CBC selection error inside Workstream B \(B_{\rm alg}\): removed.
  Workstream B evaluates the published merit of the published vector;
  selection certification belongs to A3/C.
- “Public-table audit” as the flagship Workstream B deliverable:
  replaced by certified reference-table supply after the frozen
  sites-plus-literature perimeter produced zero attached merit values.
- “Missing published merits” as the project's primary gap: retired.
  Their absence is rational because vectors are reusable across merit
  conventions and weights.  The audited gap is the absence of an
  independently replayable certified evaluation path in the frozen
  toolchain.  The engine is primary, the curated oracle set is the
  principal data artifact, and the exhaustive grid is supplementary.
- The exact/Arb production tier split is retained as a designed
  contingency but retired from the active plan because the frozen
  streaming throughput gate passed.
