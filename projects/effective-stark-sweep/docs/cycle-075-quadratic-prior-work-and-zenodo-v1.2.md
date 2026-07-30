# Cycle 075 — quadratic prior work and Zenodo v1.2

Recorded: 2026-07-30T17:06:36Z

## Outcome

The paper now locates all three engine layers against Roblot's
framework without importing a theorem across an invalid base-field
boundary.

1. **Quadratic layer.** Tate, Theorem IV.5.4, is cited for the
   classical proved rank-one conjecture in quadratic extensions.
   Arakawa's 1985 relative-index formula is cited as adjacent
   quadratic-base context. Engine A is positioned as the uniform
   explicit one-place formula through \(I_\chi\), \(E_\chi\), and
   exact per-character exponents, not as a new algebraicity theorem.
2. **Quartic and sextic layer.** The exact five-case audit is
   unchanged: Roblot's Theorem 7.1 applies to four selected sextic
   rows; RQ-002057 fails its no-wild-ramification-above-3 hypothesis.
   The manuscript now explains that Roblot's (A4) is not required by
   Theorems 6.1 and 7.1 for existence, but is used in the earlier
   implication from an assumed Stark unit to property (P2).
3. **Engine C boundary.** The manuscript expressly does not invoke
   Roblot's squareness criteria for
   \(\varepsilon=u^{e/2}\). Those criteria assume a totally real base;
   Engine C works over imaginary quadratic bases and certifies the
   divisibility directly in the unit lattice.

## Verification

- deterministic main-paper build: 17 pages, zero warnings;
- deterministic supplement build: 3 pages, zero warnings;
- full referee audit: PASS;
- companion replay: Engine A/B/C and structural lemmas VERIFIED;
- public main-PDF download matches the local SHA-256;
- Zenodo default preview is `effective-stark-results.pdf`.

## Public record

- version: 1.2;
- DOI: `10.5281/zenodo.21707692`;
- concept DOI: `10.5281/zenodo.21703305`;
- companion: `effective-stark-results-companion-v12.tar.gz`;
- companion SHA-256:
  `04ab5b01021b3b7ba4adb4fbf25c872a9a2507f52bc32da0370275d70b53cfce`;
- full freeze: `artifacts/results-paper-full-freeze-v9.json`.

This version supersedes v1.1 while preserving it as part of the
Zenodo version chain.
