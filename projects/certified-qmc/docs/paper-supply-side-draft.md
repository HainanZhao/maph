# Methods-paper supply-side draft

Status: pre-results prose; production result fields remain `PENDING`

## Motivation: making merit computations falsifiable

Rank-1 lattice-rule repositories distribute generating vectors because
the vector—not a merit under one particular convention and weight
profile—is the reusable object.  Our initial interpretation treated the
absence of exhaustive numerical merit tables as the certification gap.
The bounded source audit showed why that framing was weak: the absence
is rational.

The stronger finding sits one layer lower.  Across the named,
hash-frozen LatNet Builder and QMCPy revisions and the frozen
public-distribution perimeter, we found no independently replayable
exact or enclosed evaluation path.  A merit produced within that
toolchain cannot be falsified from its supplied artifacts alone.  This
is not a universal negative about private, historical, or uninspected
software.  It is a durable statement about a named perimeter whose
sources and hashes are published with the audit.

The principal contribution is therefore an evaluator and independent
replay contract.  A 298-case, value-blind conformance oracle is the
main data artifact.  The exhaustive 79,200-entry fidelity grid is
supplementary archival data and supplies the certified CBC-side anchors
needed for later certified-versus-certified construction comparisons.

## Audit perimeter

The perimeter consists of the hash-frozen UNSW and Magic Point Shop
distribution surfaces, the frozen QMCPy repository snapshot, and the
six primary papers named in the prospective literature sweep.  The
sites distribute vector components without a numerical merit column.
Four of the six papers report merit-like numerical quantities, but none
attaches such a value to a frozen `lattice-29102` or
`lattice-39102` vector.  The conclusion is explicitly “within the
frozen sites-plus-six-paper perimeter,” never “nowhere in the
literature.”

The inspected LatNet Builder path represents lattice merits in
binary64, uses FFTW in its fast product path, and selects an argmin by a
floating-point comparison.  The inspected QMCPy revision supplies no
exact/enclosed lattice-merit evaluator or certified CBC path.  Frozen
FFTW and LatNet replays validate the realism of our model class but are
tagged `NUMERICAL` and excluded from the proof chain.

## Exact evaluation and certificate architecture

For the product-weight Bernoulli-\(B_2\) convention,

\[
e^2(z,N)=-1+\frac1N\sum_{k=0}^{N-1}
\prod_{j=1}^d\left(1+\gamma_j
B_2(\{kz_j/N\})\right),
\]

rational weights make the merit rational.  The implementation exposes
the normalization and represents every factor over its exact
denominator \(6\,\operatorname{den}(\gamma_j)N^2\).  The corrected CRT
budget includes the weight-denominator term
\(\sum_j\log_2\operatorname{den}(\gamma_j)\), which contributes
\(2\log_2(d!)\) for \(\gamma_j=j^{-2}\).

The production evaluator streams one prime at a time through a
dimension-incremental running product.  Each emitted chunk is
authenticated independently; an append-only manifest hashes the
previous line; bounded balanced CRT reconstructs the unique signed
integer; and two universal overflow primes check the reconstruction
without participating in it.  A selected-entry verifier authenticates
only the chunks needed for one merit and reports the exact reduced
rational.  The release dependency graph contains no FFTW.

Primality is certified rather than merely tested.  The deterministic
schedule contains 3,738 work primes and two overflow primes of the form
\(c2^{32}+1\).  Each carries a complete-factorization \(N-1\)
certificate, root checks, and 2-adic valuation.  A separate verifier
with no shared arithmetic helpers checks all 3,740 certificates, and
two generator reruns reproduce the schedule byte-for-byte.

## Gated engineering history

The first streaming pilot failed before authorization because a native
constant-factor error made the measured update count inconsistent with
the preregistered incremental model.  The failed transcript was
preserved.  The corrected implementation was versioned and
re-preregistered without changing an acceptance threshold.  It passed
25/25 independent modular oracle checks, both overflow checks, and all
checkpoint replays.  Its four-core VPS median was 2.483 ns/update,
projecting the confirmed 54.9-trillion-update fidelity workload to
1.58 node-days with 3.70% replay overhead.

The first production attempt then correctly paused under a
prospectively frozen +25% throughput-drift alarm.  Same-host diagnostics
showed VPS scheduling variance rather than an arithmetic failure.  A
human-authorized, versioned +75% monitor retained the seven-node-day
hard budget and every correctness predicate.  The partial first run is
preserved and no value from it is promoted.  The plain-`__int128`
kernel, compiler flags, and build path remain frozen throughout
production.

Production outcome:

<!-- BEGIN GENERATED PRODUCTION OUTCOME -->

- fidelity manifest: `PENDING`;
- 100-entry selected replay: `PENDING`;
- three independent oracle checks: `PENDING`;
- usability grid and \(j^{-2}\) hash reuse: `PENDING`;
- 298-case engine oracle extraction: `PENDING`;
- DOI: `PENDING`.

<!-- END GENERATED PRODUCTION OUTCOME -->

No result sentence may replace these markers until the corresponding
self-hashed certificate exists and replays.

## Artifact hierarchy and claim boundary

The release hierarchy is:

1. exact evaluator and independent verifier;
2. 298-case conformance/oracle set selected before value extraction;
3. supplementary exhaustive fidelity and usability tables.

The oracle spans complete tractable prefixes, low/intermediate/extreme
moduli and dimensions, both source families, all three weight profiles,
and adversarial decision cases including exact symmetry, zero and tiny
weights, and denominator stress.  It is a software-conformance suite,
not a representative sample of lattice quality.

Every certified number is a rule merit in the declared RKHS
convention.  It is not an error bound for an arbitrary integrand
without a separately proved function-space norm, and it is not a
certified price or risk estimate.  The application pilot will keep
rule merit, RKHS inequality, integrand membership/norm, smoothing
hypotheses, randomized-shift interval, and model error as distinct
claims.

Cycle-009 decision-layer outcome:

<!-- BEGIN GENERATED CYCLE009 OUTCOME -->

- escalation histogram: `PENDING`;
- exact-CRT acceptance predicate: `PENDING`;
- exact final-vector merit: `PENDING`.

<!-- END GENERATED CYCLE009 OUTCOME -->

## Methodological correction

The initial proposal inferred a substantive gap from an absence before
asking why the evidence was absent.  The absence was rational.
Applying the same prospective claim discipline used for arithmetic
gates moved the contribution from “publish missing numbers” to
“provide the replayable path by which any such number can be
challenged.”  The correction is itself part of the method: explain an
absence before turning it into a novelty claim; certify what one builds;
envelope what one does not control; and keep external black boxes out
of the trusted base.
