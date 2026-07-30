# Sealed-constructor preregistration

Frozen: 2026-07-30 UTC, before running the constructor and before
opening any analytic \(L'\)-record in this block.

## Selection

Run the genuine (A1)--(A3) screen on all five frozen controls. If at
least one passes, select the passing row with smallest absolute field
class number, then smallest finite norm, then lexicographically smallest
case id.

The expected selection under the already public census invariants is
RQ-000129, but the selection rule, not that expectation, is binding.

## Independence wall

The constructor may read:

- the original relative ray-class polynomial or its frozen absolute
  polynomial;
- exact class groups and unit groups;
- automorphisms, subfields, local prime decompositions, and unit-lattice
  coordinates computed directly from that polynomial;
- Roblot's published construction.

It may not read:

- any analytic \(L'\)-value;
- any Engine-C unit orbit or Fourier-inverted comparison vector;
- the certified packet polynomial;
- `artifacts/control-phase-audit-v1.json`.

The constructor output is sealed in version control before the
comparison phase begins.

## Deterministic conventions

1. Use the first order-four automorphism returned by
   `nfgaloisconj`, with \(\chi(\gamma)=i\).
2. Work modulo the torsion subgroup \(\{\pm1\}\).
3. Use the first column of the integral kernel basis returned by
   `matkerint(1+\gamma^2)` when it and its \(\gamma\)-translate form a
   unimodular basis of the minus-unit lattice.
4. Use the least real root of the absolute field polynomial as the
   distinguished embedding.
5. For trivial minus class group, take the Fitting generator \(f=1\).
6. Construct
   \[
   \bar\eta=f(\gamma+1)^{e+t_S}\bar\theta
   \]
   exactly as in Roblot's proof of Theorem 6.1.
7. Seal both the exact algebraic unit and
   \[
   c(\eta)=\frac12\sum_{r=0}^3 i^r
   \log|\gamma^r\eta|
   \]
   before opening \(L'\).

## Gate

Continue to phase-formula fitting only if:

- at least one row genuinely passes (A1)--(A3);
- the chosen row's minus-unit lattice is cyclic over
  \(\mathbf Z[i]\);
- the exact Roblot unit can be constructed without crossing the
  independence wall;
- after opening \(L'\), the magnitudes agree at certified precision.

The phase comparison itself is a measurement, not a theorem.

