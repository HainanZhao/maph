# Research projects

This repository contains independent mathematical research programs. Each
project is self-contained: run its commands from that project's directory.

## Projects

- [`projects/erdos-700/`](projects/erdos-700/): exact and computational
  work on Erdős Problem 700, concerning
  \(\min_{1<k\le n/2}\gcd(n,\binom nk)\).
- [`projects/fourier-dark-tomography/`](projects/fourier-dark-tomography/):
  multiphoton dark events, Fourier-cat coherent-error identification, exact
  rank certificates, finite-angle statistics, and the Physical Review A
  manuscript.
- [`projects/certifiable-grid-optimization/`](projects/certifiable-grid-optimization/):
  certifiable AC optimal power flow, beginning with exact and approximate
  voltage recovery on unicyclic networks.
- [`projects/gas-aware-amm-routing/`](projects/gas-aware-amm-routing/):
  exact and certifiable order routing across parallel constant-product
  automated market makers with fixed execution costs.
- [`projects/sic-stark/`](projects/sic-stark/): a focused investigation of
  Zauner's conjecture through the Shintani--Faddeev/Stark-unit construction,
  with exact Weyl--Heisenberg diagnostics and canonical-family reductions.
- [`projects/certified-qmc/`](projects/certified-qmc/): cancelled research
  campaign retained as an archival process record; only the small exact
  evaluator remains an internal utility, and no production run or release
  is active.

The projects share only the repository history and top-level ignore rules.
Their source packages, scripts, tests, documentation, and data or paper
artifacts live inside their own directories.

## Verification

```bash
cd projects/erdos-700
python3 -m unittest discover -s tests -v

cd ../fourier-dark-tomography
python3 -m unittest discover -s tests -v

cd ../certifiable-grid-optimization
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m unittest discover -s tests -v

cd ../sic-stark
python3 -m unittest discover -s tests -v

cd ../certified-qmc
python3 -m unittest discover -s tests -v
```
