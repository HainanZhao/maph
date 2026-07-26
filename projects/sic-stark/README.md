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
precision. Research cycles 2--5 additionally:

- proves from the source's conjugation involution that rank-one shifts
  \(0\) and \(1\) occur together;
- reduces the \(L_d^3\) Jacobi cocycle to three copies of the universal
  \(S\)-kernel;
- proves the Shintani--Faddeev values and canonical phase kernel are
  invariant under Zauner action, giving an exact threefold reduction of the
  TCC equations;
- identifies the zero-output equation as an automatic consequence of the
  cocycle inverse law;
- rewrites every remaining equation as a distinguished finite symplectic
  Fourier coefficient;
- expands the first primitive quotient into three \(S\)-kernel ratios and
  explicit finite q-Pochhammer corrections;
- gives an exact countermodel proving that covariance, reciprocal pairing,
  and cyclic telescoping alone cannot imply TCC;
- proves that the known continuous, cyclic, and general modular pentagon
  identities do not directly specialize to the primitive TCC transform:
  their contour, deformation parameter, or discrete modulus is
  incompatible;
- isolates a new real-multiplication localization theorem as the narrow
  remaining quantum-dilogarithmic route.

See [`docs/sic-stark-sprint1.md`](docs/sic-stark-sprint1.md) and
[`docs/sic-stark-cycle2.md`](docs/sic-stark-cycle2.md), followed by
[`docs/sic-stark-cycle3.md`](docs/sic-stark-cycle3.md) and
[`docs/sic-stark-cycle4.md`](docs/sic-stark-cycle4.md), then
[`docs/sic-stark-cycle5.md`](docs/sic-stark-cycle5.md), for the claim ledger.

## Verification

The code uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/analyze_sic_canonical_family.py --stop 20
python3 scripts/verify_sic_fiducials.py --dimension 4 --show-residuals
```
