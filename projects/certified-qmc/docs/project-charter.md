# Project charter: Certified Quasi-Monte Carlo

Date: 2026-07-29

## Final program disposition

**CANCELLED_BY_USER at `2026-07-29T12:07:54Z`.** This charter is
retained as historical scope, not an active program. The exhaustive
tables, usability grid, conformance-oracle release, packaging,
application pilot, QMC paper, and scale-CBC gates are retired. The
small exact evaluator remains an internal utility; the campaign's
preregistration/failure/quarantine/pivot record remains a methods-paper
case study. Only the totally-real unit-lattice question is parked as a
small, independent side question at dimensions 16–64, without an
industrial certification engine.

## Mission

Build the independently replayable exact/enclosure evaluation path that
the audited rank-1 lattice-rule toolchain lacks.  Use a compact,
structurally diverse oracle suite to make implementations falsifiable;
retain exhaustive certified merits as supplementary archival data and
as the CBC-side anchors for number-theoretic comparisons.  Demonstrate
the result on one application without conflating a certified rule merit
with a certified application output.

## Motivation and artifact hierarchy

The frozen source-and-literature audit found something more important
than an absent merit column.  Across the hash-frozen LatNet Builder and
QMCPy revisions and the named public distribution perimeter, no
independently replayable exact or enclosed evaluation path was supplied.
Consequently, a merit produced within that frozen toolchain cannot be
falsified from its supplied artifacts alone.  This is a bounded claim
about the named, hash-frozen perimeter, not a universal claim about
every private or historical QMC implementation.

The absence of exhaustive published merit tables is rational: vectors
are the reusable object, and consumers can evaluate the merit under
their own convention and weights.  The certification gap therefore
sits one layer down, in the evaluator and its replay contract.  Release
and paper emphasis follows that finding:

1. the exact/enclosure engine and independent verifier are primary;
2. a few-hundred-entry conformance/oracle suite is the principal data
   artifact for software testing;
3. the 79,200-entry fidelity grid is supplementary archival data.

The exhaustive grid was initially authorized, then cancelled when its
consumer case failed review. It is not required for the surviving C2
side question: small CBC anchors at dimensions 16–64 can be evaluated
directly with exact rational arithmetic.

## Workstream A — certification engine

### A0. Convention registry

Every input declares:

- function space and kernel;
- smoothness parameter;
- kernel scaling;
- weight semantics and exact representation;
- deterministic or shift-averaged quantity.

The first registered convention is the rational `B2` product merit.
Polynomial-in-\(\pi^2\) and Arb modes are separate future conventions,
not flags that alter the meaning of existing certificates.

### A1. Exact evaluation

The direct exact engine is the ground truth. The production path may
use scaled integers, CRT, and NTTs, but its output must replay against
the direct engine on every tractable case. Certificates bind inputs,
convention, exact result, denominator proof, summand digest, and
provenance.

### A2. Enclosures

Nonrational merits will return balls with:

- library/version and precision;
- complete input normalization;
- outward-rounded interval;
- acceptance predicate;
- replay transcript.

No Arb interface is implemented in Phase 0.

### A3. Certified CBC

The intended architecture retains three representations:

1. exact scaled products in modular residue form;
2. an Arb shadow score with error enclosures;
3. exact reconstruction for unresolved comparisons.

Before implementation, the project must prove the signed integer bound
used to choose CRT primes and identify all cheap exact symmetries. The
small exact CBC oracle defines the branch-level ground truth.

Cycle 009 uses compiled Arb at 106 bits as its first production shadow.
Double-double is not a correctness dependency. It may be introduced
only after profiling shows Arb is material, using published
double-word constants and a dual-shadow replay whose complete
comparison/branch trace is bit-identical to the banked Arb transcript.
The run is explicitly deferred from Workstream B and becomes the entry
gate for any Workstream C claim that a new rule was selected by
certified CBC.  Its escalation histogram is not silently abandoned.

### A4. Scale

The reference \(N=2^{20},d=100\) target remains aspirational. Memory,
butterfly, and wall-time budgets will be rewritten from measurements of
the implemented representation. The proposal's denominator-only bit
count and tie-rate assumptions are not used as performance guarantees.
Every rational-weight bit budget includes
\(\sum_j\log_2\operatorname{den}(\gamma_j)\); for
\(\gamma_j=j^{-2}\) this is \(2\log_2(d!)\).

## Workstream B — evaluator conformance and certified anchors

The frozen public sites and six-paper primary-literature perimeter
publish no numerical merit attached to the frozen vectors.  Workstream
B therefore validates the engine against exact ground truth and
supplies a compact, diverse conformance set.  Each source is frozen by
URL and SHA-256.

The fidelity grid covers the fixed `lattice-29102` and extensible
`lattice-39102` families for \(N=2^{10},\ldots,2^{20}\), every prefix
dimension through 3,600, and the documented construction weights
\(\gamma_j=j^{-2}\). A small usability grid additionally freezes
\(\gamma_j=j^{-1},j^{-2},j^{-3}\) at
\(N=2^{10},2^{15},2^{20}\) and dimensions 16, 64, and 256.

Every table is a versioned data product: exact rationals or sufficient
CRT residues, proved reconstruction bounds, ordered verified primes,
two overflow-check primes, per-entry provenance, chunk hashes, a
top-level SHA manifest, and one-command independent entry replay.

The curated oracle set spans the \(N\) ladder, representative and
extreme prefix dimensions, all three frozen weight profiles,
full-prefix construction tests at tractable scale, and deliberately
difficult decision-layer cases such as exact symmetries, zero/tiny
weights, and large rational denominators.  Its selection is frozen
before values are extracted.  It is a software-conformance suite, not
a statistical sample of lattice-rule quality.

The corrected weight-denominator budget is computed before production.
No full-grid run begins until the source/license freeze, deterministic
prime schedule, and compiled prime-major streaming pilot pass.

For a published pair \((z,y)\), CBC selection optimality is irrelevant:
Workstream B evaluates the published \(z\).  Its error envelope is
\(B_{\rm alg}(\mathcal M)=T_{\rm eval}(\mathcal M)+T_{\rm format}\),
where \(\mathcal M\) is an explicit class of plausible producer
evaluators and the formatting term is exact from the observed decimal
grid. Historical binaries and the project's FFTW reproduction remain
outside the trusted base.

Before acquiring or comparing any published merit value, the
timestamped protocol in
`docs/workstream-b-discrepancy-preregistration.md` and its Cycle-011
amendment must replay. Without the required bound it is
`UNCLASSIFIED_EXTERNAL`.
This classification protocol is banked but optional for the frozen
perimeter. A newly discovered merit-bearing source requires a prospective
perimeter amendment and all gates above. Any discrepancy follows:

1. local exact replay;
2. independent implementation replay;
3. upstream version/provenance check;
4. private maintainer contact;
5. public correction only after confirmation.

Public recommendation is not labeled “production use” without usage
evidence.

## Workstream C — number-theoretic constructions

Status: parked as a small independent side question, not an active
workstream. If resumed later, it uses direct `Fraction` evaluation and
the existing regulator machinery; it does not depend on the cancelled
production engine or tables.

- exact Zaremba/dual indices in dimension two;
- continued-fraction constants with explicit finite-\(N\) statements;
- certified dimension-three enumeration;
- candidates from totally real units only after an explicit embedding
  from number-field data to a finite rule;
- certified head-to-head comparison in one frozen merit convention.

The unit-lattice thread is the research bet, not a presumed improvement
over CBC.

## Workstream D — application pilot

Status: cancelled.

Select one preintegrated pricing or UQ workload. The final report keeps
separate:

- lattice-rule merit;
- RKHS inequality;
- proof or estimate of the integrand norm;
- preprocessing/smoothing hypotheses and error;
- randomized-shift statistical interval;
- model and discretization error;
- empirical comparison to MC/Sobol baselines.

There will be no “certified price” language unless every listed factor
is certified.

## Deliverables

1. Retained internal exact evaluator.
2. Retained process record for the cross-project methods paper.
3. Optional future C2 note only if the small direct benchmark produces
   a mathematical result.

## Standing orders

- Preregister experiments and target hashes.
- `VERIFIED`, `ENCLOSED`, `NUMERICAL`, and `PROJECTED` are distinct.
- Test every analytic reduction with an independently structured oracle.
- Stop on unexplained discrepancies.
- Record negative results and retirement criteria at the entry points.
- Do not optimize a bridge that has not first been made executable.
