# Width-three Ising twist-response demo

This standalone page explores an all-sector width-three Ising strip engine.
For `G_(n,3)` there is one handle site per longitudinal slab, and the virtual
carrier is the 256 even masks on nine frontier sites. It is not part of, nor
used by, any paper or proof archive.

The core is applied as a structured operator:

1. sparse XOR parity transitions for transverse edges;
2. the longitudinal connector diagonal;
3. the transported cochain-gauge sign diagonals;
4. the local four-state quadratic Gauss transform.

It does not store a generic dense matrix for every handle. The browser
provides dense materialization of one representative core solely as a
benchmark control.

## Claim boundary

- `OBSERVED`: the TypeScript engine matches the committed finite-field fixture
  checksums for `n=2..7`, both primes `1,000,000,007` and `1,000,000,009`,
  and isotropic, anisotropic, and deterministic nonuniform weights. The
  fixtures are in `fixtures/reference.json`.
- `OBSERVED`: browser runtimes and memory measurements depend on the local
  machine. Exported benchmark JSON records what was actually measured.

The demo does not claim an efficient algorithm when transverse width grows,
a thermodynamic limit, or an exact solution of the three-dimensional Ising
model. WebGPU is not implemented in this first version.

## Verification

From the repository root:

```bash
cd demos
npm ci
npm test
BASE_PATH=/maph/ npm run build
```

Regression checks are self-contained within `demos/`; this page has no paper
or proof-archive replay obligation.
