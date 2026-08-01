# Cycle 2: G0 analytic-hypothesis preregistration

Date frozen: 2026-08-01 UTC, before the Cycle-2 source retrievals and analytic
application audits.

## Claim boundary

Cycle 2 audits the hypotheses and transfers hidden behind the exact exponent
algebra completed in Cycle 1. It seeks no new zero-density theorem, no improved
short-interval exponent, and no numerical candidate. A published conclusion
is not independently re-proved merely by matching its displayed exponents.

## Frozen source and branch scope

- Guth--Maynard source: arXiv `2405.20552v2`, frozen tar SHA-256
  `9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`.
- Zero-density range: `7/10 <= sigma <= 4/5`, with the outer Ingham and
  Huxley branches kept separate.
- Zero count: multiplicity counted, `|Im rho| <= T`.
- Uniform short intervals: `x^(17/30+epsilon) <= y <= x^0.99`.
- Almost-all short intervals: `X^(2/15+epsilon) <= y <= X^0.99`.
- Logarithmic factors and `T^o(1)` losses must remain visible until an
  asymptotic absorption step is justified; no finite-`T` power upgrade is
  allowed.

## Stream A: zero-detection and Type-II input

Freeze Maynard--Pratt, *Half-isolated zeros and zero-density estimates*,
arXiv `2206.11729` / IMRN 2024, as the first source to inspect. Record the
retrieved version, file hash, theorem/page locator, and exact hypotheses of
Lemma 24. The audit must answer, without inference from Guth--Maynard alone:

1. whether its detector coefficients and Type-I/Type-II definition are the
   same objects used in Guth--Maynard Section 13.1;
2. the exact `sigma`, `T`, zero-height, and multiplicity conventions;
3. the log factor and uniformity of the Type-II count;
4. every change of notation or harmless constant-factor conversion.

The mean-value input must likewise be pinned to one reachable theorem or
derived exactly from a pinned mean-square/large-sieve statement. Merely
calling it “usual” fails this stream.

## Stream B: Theorem 1.1 application hypotheses

Audit all of the following source-level transfers for both integer-`k`
regimes from Cycle 1:

1. construction of the beta-dependent smooth function and Fourier inversion;
2. uniform Fourier decay/truncation and the local zero count used to extract a
   1-separated set;
3. the coefficient bound for the original detector;
4. coefficient growth after taking the `k`th power and the normalization cost;
5. decomposition of support from `[N^k,(2N)^k]` into admissible dyadic blocks;
6. transfer of the large-value threshold after normalization/decomposition;
7. translation of the height interval to Theorem 1.1's `[0,T]` convention;
8. all `log T`, divisor-function, dyadic-choice, and `o(1)` losses.

Each row must be `PROVED` only when it is an exact identity or follows from a
published theorem whose displayed hypotheses are checked in this run;
otherwise it remains `OBSERVED` and blocks full G0.

## Stream C: complete short-interval replay

Freeze one reachable primary source for each external input:

- the truncated explicit formula used by Guth--Maynard Section 13.2;
- one near-one density theorem, choosing a single branch rather than retaining
  the source's Jutila/Montgomery disjunction;
- the Vinogradov--Korobov zero-free region in the exact form used;
- the zero correlation/counting estimate used in the almost-all second moment.

Two independent routes must reproduce, with all secondary ranges and error
terms, the uniform boundary `17/30` and the almost-all boundary `2/15`.
Agreement only on `1-1/b` and `1-2/b` is insufficient. Each route must label
the truncation choice, zero-free cutoff, density supremum, epsilon margin,
upper range, and exceptional-set/error conversion.

## Pass, failure, and resource rules

G0 analytic PASS requires:

1. every node marked as unread or indirect in
   `g0-theorem-dependency-graph-v1` is either checked or explicitly removed
   from the promoted dependency path;
2. both downstream routes agree on every labeled boundary and secondary
   condition;
3. the source hashes, locators, conventions, and transformations reconcile;
4. one command replays all exact implication checks in under 60 seconds per
   route and 256 MiB per route.

A genuine mismatch opens a versioned correction branch. Inaccessible sources
remain `OBSERVED`; a reachable published restatement may substitute only when
its exact status and loss of primary-source authority are recorded. Failed
rows are retained. No P1 search or P6 generalization begins before this gate.

## Falsifiers

- the Maynard--Pratt lemma does not cover the detector or range quoted by
  Guth--Maynard;
- normalization of powered detector coefficients incurs a non-`T^o(1)` loss;
- the dyadic support or threshold transfer leaves an uncovered branch;
- a downstream external theorem has a range incompatible with the chosen
  truncation;
- the full explicit-formula replay requires a strict theta larger than the
  published endpoint after epsilon bookkeeping.
