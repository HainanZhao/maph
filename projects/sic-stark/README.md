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
precision. Research cycles 2--7 additionally:

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
- embeds every TCC special value exactly into the general modular gamma
  function and matches the dimension-four beta-integral phase;
- closes the standard pentagon/localization route by proving that every
  desired characteristic sample lies strictly inside the resulting
  two-gamma kernel's pole-free strip;
- computes the exact local ray-unit action on TCC characteristics and
  proves that it moves the output direction together with the summation
  variable;
- shows already in dimension four that the additive TCC phase does not
  descend to a fixed-direction ray-class character, so character
  resolvents decompose the full residual vector rather than force a
  primitive coefficient to vanish.

See [`docs/sic-stark-sprint1.md`](docs/sic-stark-sprint1.md) and
[`docs/sic-stark-cycle2.md`](docs/sic-stark-cycle2.md), followed by
[`docs/sic-stark-cycle3.md`](docs/sic-stark-cycle3.md) and
[`docs/sic-stark-cycle4.md`](docs/sic-stark-cycle4.md), then
[`docs/sic-stark-cycle5.md`](docs/sic-stark-cycle5.md) and
[`docs/sic-stark-cycle6.md`](docs/sic-stark-cycle6.md), and finally
[`docs/sic-stark-cycle7.md`](docs/sic-stark-cycle7.md), for the claim ledger.

## Verification

The code uses only the Python standard library.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/analyze_sic_canonical_family.py --stop 20
python3 scripts/verify_sic_fiducials.py --dimension 4 --show-residuals
```
