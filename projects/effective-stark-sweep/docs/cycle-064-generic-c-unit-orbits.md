# Cycle 064 — generic Engine-C unit-orbit isolation

**Claim tag:** `ENCLOSED_UNIQUE_INTEGRAL_ANTI_UNIT_ORBIT`

The exact cyclic action on
\(\mathcal O_E^\times/\mu(E)\), its rank-two anti-unit lattice, and
the Arb logarithmic inversion are now generic.

The regression anchor caught a factor-of-two implementation hazard.
The banked \(e/2\) factor converts class-log coordinates.  When the
input is already the primitive quartic Fourier sum \(L'(0,\psi)\),
anti-unit symmetry duplicates the two independent logarithms, so the
direct two-coordinate inversion factor is \(e/4\).  With that
distinction made explicit, the Paper-II anchor reproduces its banked
orbit
\[
\{(-2,0),(0,-2),(0,2),(2,0)\}.
\]

Both new imaginary-base routes independently isolate
\[
\{(-1,-1),(-1,1),(1,-1),(1,1)\}.
\]
The exhaustive dihedral transforms cover the Artin
generator/inverse and complex-embedding choices; all matches comprise
one exact \(C_4\)-orbit and no second integral orbit.

Artifact: `artifacts/engine-c-unit-orbits-v1.json`.

