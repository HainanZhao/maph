# Cycle 006 — compiled direct modular baseline

Date: 2026-07-29

A C11 command-line evaluator now computes the frozen scaled merit
numerator modulo one 62-bit prime. Multiplication and signed kernel
intermediates use GCC/Clang `__int128`; inputs remain explicit integer
generators and rational weight numerators/denominators.

The compiled evaluator agrees residue-for-residue with the Python
modular oracle on:

- the frozen UNSW dimensions 2, 4, 8, and 16;
- the first two audited 62-bit primes; and
- 20 additional deterministic random test cases in the regression
  suite.

The benchmark includes a synthetic \(N=2^{20},d=16\) direct evaluation.
It is an \(O(Nd)\) final-merit baseline, not an all-candidate CBC
benchmark. Exact residue equality is `VERIFIED_IMPLEMENTATION`; local
timings are `NUMERICAL`.

Minimum local subprocess timings over five runs were 1.04 ms at
\(N=2^{10}\), 4.77 ms at \(N=2^{14}\), 67.4 ms at \(N=2^{18}\), and
270 ms at \(N=2^{20}\), all at \(d=16\). Process-launch overhead is
included.

Artifact: `certificates/cycle-006-native-baseline.json`.

Decision: **PASS**.
