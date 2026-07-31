# Cycles 076--080 preregistration: B3 input construction

Frozen: 2026-07-31 UTC, before constructing the quartic
character-kernel list, before any new weak-coefficient evaluation, and
without opening a census \(L'\) target.

## Objective and claim boundary

This block constructs the two missing B3 inputs:

1. a genuine Roblot-eligibility column for every census row supporting
   an order-four ray character; and
2. an Arb-ball evaluator for the weak-unit Fourier coefficient,
   anchored on the five already opened controls.

This block does not run the phase-defect census.  It does not evaluate,
read, rank, or filter a census row using \(L'\), a phase, or a
floating-point field pre-screen.

## Frozen population source and selection

The sole selection source is
`../effective-stark-sweep/artifacts/w1-full-census-v1.json`, whose
recorded source-census SHA-256 is
`9fa0f1880ca0c2d263e0235bd4ed83e8e6001b88bfede0927a7197f46f7d4563`
and whose screen-source SHA-256 is
`4ee9d907c9a3d601c5f0346e8e8f7f2ddec725170e7a061b153cbc69fc9b2683`.

A row is relevant exactly when its frozen `support_orders` contains
`4`.  A preliminary metadata count, made before this amendment, found
1,512 such rows; this count is a cross-check, not a filtering input.

For every relevant row, reconstruct all characters of exact order four
on the frozen one-place ray class group and retain exactly those
nontrivial on the frozen `sign_log`.  Characters are deduplicated only
under \(\chi\sim\chi^{-1}\), since these and only these surjective
characters have the same kernel in a cyclic quotient of order four.
The resulting `(case_id, kernel)` list is frozen before any field or
coefficient result is inspected.

The 881 Engine-C rows and their geometry verdicts are not selection
inputs.

## Exact Roblot gate

For each frozen character kernel:

- reconstruct its primitive ray character and primitive conductor;
- construct the exact cyclic-quartic extension \(K/k\);
- certify the number fields used by the calculation;
- check (A1) from \(k\) being totally real, the exact relative degree,
  the four ray automorphisms, and the exact signature \([4,2]\) of
  \(K\);
- construct the unique totally real quartic intermediate field
  \(K^+\) and check \([K:K^+]=2\) for (A2);
- factor every prime of \(k\) in the finite part of the primitive
  conductor through \(K^+\) and \(K\), and check that no prime above it
  splits in \(K/K^+\) for (A3).

Every attempted kernel remains in the artifact.  Construction errors,
resource caps, certification failures, and failed hypotheses are
recorded as separate noneligible verdicts; none may be silently
dropped.  The per-kernel resource cap is one node-hour.

## Arb evaluator gate

The evaluator takes only:

- an exact defining polynomial;
- an exact algebraic-unit polynomial;
- the exact four-element Galois orbit/order convention; and
- the distinguished embedding rule.

It must isolate the distinguished real root by disjoint Arb balls,
evaluate the four algebraic conjugates with outward rounding, prove
that their absolute-value balls exclude zero, take certified
logarithms, and form
\[
c_\chi(\eta)=
\frac{\ell_1+i\ell_2-\ell_3-i\ell_4}{2}.
\]

The backend is pinned to `python-flint==0.9.0`; the runtime artifact
must record the Python, python-flint, and FLINT versions and the working
precision.  The initial precision is 256 bits and the anchor rerun is
512 bits.

The evaluator passes its anchor only if all five existing exact weak
units produce nested 256/512-bit coefficient balls and each ball
contains the corresponding archived point evaluation.  The archived
points are validation data only; they may not choose a root, Galois
orientation, unit representative, or precision.

## Gates and continuation rule

| Gate | Pass condition | Containment and continuation |
|---|---|---|
| Kernel inventory | all relevant rows replayed; exact characters and inverse-pair kernels agree with frozen metadata checks | preserve discrepant rows and continue independent rows |
| Roblot population | every kernel has an explicit construction or explicit noneligible/tool verdict; eligible rows pass A1--A3 exactly | withhold failed rows from B3 promotion, preserve evidence, continue independent kernels |
| Arb anchor | five controls pass at both precisions with nonzero log arguments and nested balls | do not open census targets; diagnose or replace only the evaluator branch |
| Independence wall | source and runtime access no census target-bearing artifact | quarantine affected output and rerun cleanly |

Issues are highlighted in the block report after the current input
construction goal is cleared, unless they threaten evidence integrity,
authorize an irreversible action, or make all meaningful progress
impossible.

