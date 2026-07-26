# SIC--Stark research

This project investigates the Twisted Convolution Conjecture (TCC) in the
canonical rank-one family

\[
Q_d=\langle1,1-d,1\rangle,\qquad d\ge4,
\]

as a focused route toward Zauner's SIC-existence conjecture. It is a
research ledger and executable reduction, not a claim that the conjecture
has been solved.

## Current result

The canonical arithmetic, Weyl--Heisenberg diagnostics, and finite twisted
convolution are implemented exactly or to controlled floating-point
precision. Research cycle 2 additionally:

- proves from the source's conjugation involution that rank-one shifts
  \(0\) and \(1\) occur together;
- reduces the \(L_d^3\) Jacobi cocycle to three copies of the universal
  \(S\)-kernel;
- proves the canonical phase kernel is invariant under simultaneous Zauner
  action and records the resulting conditional threefold equation reduction.

See [`docs/sic-stark-sprint1.md`](docs/sic-stark-sprint1.md) and
[`docs/sic-stark-cycle2.md`](docs/sic-stark-cycle2.md) for the claim ledger.

## Verification

The code uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/analyze_sic_canonical_family.py --stop 20
python3 scripts/verify_sic_fiducials.py --dimension 4 --show-residuals
```
