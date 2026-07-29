# Cycle 005 — benchmark and phase decision

Date: 2026-07-29

Three independent paths were run on the frozen UNSW
\(N=1024,\gamma_j=j^{-2}\) prefixes at dimensions 2, 4, 8, and 16:

1. direct reduced `Fraction` sum-product;
2. direct scaled-integer sum-product; and
3. independent modular sums followed by bounded balanced CRT.

All paths returned the same exact fractions at every dimension.  Local
timings and CRT prime counts are frozen in
`certificates/cycle-005-benchmark.json` and tagged `NUMERICAL`; they are
not extrapolated to the \(N=2^{20},d=100\) reference scale and do not
measure NTT fast CBC.

## Decision

**CONTINUE_WITH_FAST_MODULAR_ENGINEERING.**

The five-cycle gate has established:

- a visible certification gap in the audited maintained tools;
- a correct integer representation and proved signed bounds;
- a reproducible, fully audited NTT-prime family;
- exact modular merit reconstruction; and
- exact per-branch CBC certification on a small oracle case.

What remains unproved is now sharply isolated: fast convolution,
streaming residue storage, certified shadow separation, and measured
scaling.  The next implementation gate should be a compiled modular
direct evaluator followed by a single-prime radix-two NTT prototype.
No production runtime or tie-rate claim is promoted yet.

Tag: exact agreements `VERIFIED`; timing observations `NUMERICAL`.
