# Cycle 009 — three-representation decision-layer preregistration

Frozen at: **2026-07-29T04:24:47Z**

This checkpoint precedes the \(N=2^{16},d=50\) data run. No decision
statistics have been sampled.

## Frozen target

- \(N=65{,}536\), \(d=50\), \(\gamma_j=1/j^2\).
- First component fixed to 1.
- Candidate sign symmetry quotiented.
- Candidates ordered as \(5^a\bmod N\),
  \(0\le a<2^{14}\).
- Deterministic tournament in ascending \(a\); exact ties choose the
  smaller exponent.

## Three representations

1. **Ground truth:** compiled prime-major scaled-product residues and
   the valuation-stratified NTT.
2. **Decisions:** a double-double midpoint with a rigorous outward
   radius derived from error-free transforms/FMA.
3. **Escalation:** overlapping double-double balls go to 128-bit Arb;
   overlapping Arb balls go to balanced exact CRT reconstruction of the
   candidate difference.

A comparison is ball-separated only when the upper bound of one
candidate is strictly below the lower bound of the other. Arb precision
may increase but never decrease.

## Frozen rate

There are 16,384 sign-quotiented candidates and a fixed tournament of
16,383 comparisons in each of stages 2 through 50: 802,767 comparisons
in total.

\[
r_{\rm CRT}=
{\#\{\text{comparisons escalated to exact CRT}\}\over802{,}767}.
\]

The preregistered acceptance predicate is
\(r_{\rm CRT}<0.001\). Therefore at most 802 exact-CRT escalations pass.
Post-quotient exact equalities count in the numerator and are also
reported separately. Double-double-to-Arb and Arb-to-CRT rates are
reported independently.

If the gate fails, the project halts the certified-optimal-search claim
at this scale. It may still certify the final vector's merit exactly,
but it must publish the observed escalation rate and use the weaker
claim.

## CRT budget

At the final stage the proved candidate-difference bound needs 2,162
modulus-product bits and 35 scheduled primes. The final merit needs
2,176 bits and 36 primes. The schedule is frozen at 40 primes, covering
the final reconstruction plus the mandatory two-prime overflow replay.

## Engineering order

The first \(2^{16}\) correctness transcript uses the plain
`__int128` reduction kernel. Montgomery multiplication and lazy
reduction are scheduled immediately after that transcript is banked.
They are promoted only if every residue, reconstructed decision, and
winner is bit-identical. The suggested 3–5× improvement remains
`PROJECTED`, not a gate or reported result.

Artifacts:

- `certificates/cycle-009-prime-schedule-40.json`
- `certificates/cycle-009-preregistration.json`

Status: `PREREGISTERED`; target run not started.

## Reference preflight after freeze

The pinned `python-flint==0.9.0` / FLINT 3.6.0 reference layer now
exercises all three outcomes without sampling the target run:

- an ordinary comparison separates in the rigorous double-double
  reference ball;
- a constructed near-overlap reaches and separates in Arb at 128 bits;
- a forced sign tie reaches the exact reference layer.

The double-double reference carries an exact rational audit radius
around its error-free-transform center. That is suitable for validating
the future compiled radius but is intentionally too expensive for the
\(2^{16}\) run. The compiled NTT shadow/radius implementation therefore
remains a blocking correctness gate.

Artifact: `certificates/cycle-009-shadow-decision-preflight.json`.

## Arb-first amendment

Amended at **2026-07-29T04:36:30Z**, before the target run:

- the production shadow is compiled Arb at 106 bits;
- overlapping Arb balls escalate directly to exact CRT;
- double-double is disabled in the primary run;
- the mandatory histogram remains
  `DD-resolved / Arb-resolved / exact`, with the primary DD bin fixed
  to zero;
- Arb wall time and fraction of total time are recorded.

Double-double is authorized only if the banked Arb profile shows a
material bottleneck. It must use published rigorous double-word
constants and replay the identical tournament under both shadows. The
complete per-comparison branch trace—not merely the final vector—must
be bit-identical before promotion.

Artifact: `certificates/cycle-009-preregistration-v2-arb106.json`.
