# Research projects

This repository contains independent mathematical research programs.  Each
project is self-contained: run its commands from that project's directory.

## Projects

- [`projects/erdos-700/`](projects/erdos-700/): exact and computational
  work on Erdős Problem 700, concerning
  \(\min_{1<k\le n/2}\gcd(n,\binom nk)\).
- [`projects/fourier-dark-tomography/`](projects/fourier-dark-tomography/):
  multiphoton dark events, Fourier-cat coherent-error identification, exact
  rank certificates, finite-angle statistics, and the Physical Review A
  manuscript.

The projects share only the repository history and top-level ignore rules.
Their source packages, scripts, tests, documentation, and data or paper
artifacts live inside their own directories.

## Verification

```bash
cd projects/erdos-700
python3 -m unittest discover -s tests -v

cd ../fourier-dark-tomography
python3 -m unittest discover -s tests -v
```
