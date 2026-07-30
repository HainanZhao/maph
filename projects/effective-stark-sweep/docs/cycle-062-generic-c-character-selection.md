# Cycle 062 — generic Engine-C character selection

**Status:** `VERIFIED_EXACT_CHARACTER_SELECTION`

The generic selector starts from the real primitive ray datum, packet
field, imaginary quadratic base, and absolute character field.  It
does not receive a CM conductor, ray subgroup, or selected CM
character.

For each route it:

1. factors the character field over the imaginary base;
2. chooses a canonical relative factor by the exact conductor-HNF key;
3. reconstructs the conductor and subgroup with `rnfconductor`;
4. enumerates all compatible characters with `bnrchar`;
5. proves the compatible order-four set is an inverse pair;
6. compares 64 exact `lfunan` coefficients with the source character;
7. emits the first exact separating coefficient.

## Results

| object | CM base | compatible pair | selected | separator | \(|S|\) |
|---|---|---|---|---:|---:|
| Paper-II packet 0 | \(\mathbb Q(\sqrt{-6})\) | `[2,3]`, `[6,1]` | `[6,1]` | 5 | 4 |
| RQ-001280 route 1 | \(\mathbb Q(\sqrt{-10})\) | `[3,2]`, `[9,2]` | `[9,2]` | 5 | 3 |
| RQ-001280 route 2 | \(\mathbb Q(\sqrt{-14})\) | `[0,3]`, `[0,1]` | `[0,3]` | 5 | 3 |

In all three cases the source and selected coefficient at \(n=5\) is
\(-i\), while the inverse coefficient is \(+i\).  Full 64-term vectors
agree exactly, not approximately.  The Paper-II selection reproduces
the banked `[6,1]` label without importing it into the algorithm.

Both new routes have two distinct finite conductor primes, so the
natural Stark set has \(|S|=3\) and the banked global-unit clause
applies.

Artifacts:

- `artifacts/engine-c-character-selection-v1.json`, SHA-256
  `ccfb9861183d3113cc6c721afd803502d14fe9dac3896da21cc3d5e641707f6f`;
- transcript SHA-256
  `fd9082528bcc975b80908776360011fa05af30d49b0f0cbc068e2aaff3409c68`.

This certificate selects ray characters only.  It makes no analytic
unit or real-packet claim.
