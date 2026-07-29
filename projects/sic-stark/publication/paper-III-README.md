# Paper III reproducibility package

This package accompanies:

> *Dimension-Six Twisted Convolution as Arithmetic Boundary Fusion of a
> Two-Base Lens-Space Beta Integral*

## Scope

This is a research note, not a closed proof. The verified content is
the two-base reformulation, the dimension-five/dimension-six
dichotomy, the meromorphic Sarkissian--Spiridonov specialization, the
endpoint exclusion, and the finite multiplier ledger. The unconditional
formal Twisted Convolution Conjecture is already proved in dimensions
four, five, seven, and eight in the companion papers (Paper I and
Paper II). Dimension six remains conditional on the fusion-continuity
conjecture stated in the note; an earlier draft's componentwise
boundary estimate and its claimed implication to the formal shifts
were retired after a normalization audit found the map from additive
spectral coefficients to the three ray-class logarithms undefined.

## Required software

- Python 3.12 or compatible;
- NumPy, mpmath, SymPy;
- PARI/GP 2.15.4 or compatible;
- python-flint 0.9.0 for the rigorous Arb enclosures.

## Principal commands

```bash
python3 -m unittest discover -s tests -k DimensionSix
bash scripts/generate_dimension_six_amendment_certificates.sh
```

The cycle-by-cycle state and every negative-result gate are recorded
in `docs/dimension-six-state-notes-v3.md`.

Every archived file is covered by `ARCHIVE_CONTENTS.sha256`.

The manuscripts and documentation use CC BY 4.0; executable code uses
the MIT license. See `LICENSE` and `LICENSE-CODE`.
