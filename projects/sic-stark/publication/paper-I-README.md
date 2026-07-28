# Paper I reproducibility package

This package accompanies:

> *Twisted-Convolution Identities in Dimensions Four and Five from
> Shintani Ray Units*

It is logically independent of the dimension-seven and
dimension-eight companion paper.

## Main theorem

For every admissible tuple in dimension four or five, both \(0\) and
\(1\) are formal TCC shifts.  Shift sets agree for the admissible forms
covered by the same discriminant.

## Required software

- Python 3.12 or compatible;
- NumPy;
- PARI/GP 2.15.4 or compatible;
- python-flint 0.9.0 for rigorous Arb enclosures.

## Principal commands

```bash
python3 scripts/generate_referee_certificates.py
python3 scripts/verify_referee_certificate.py
gp -q scripts/referee_pari_audit.gp
python3 -m unittest tests.test_dimension_five_artifacts
python3 -m unittest tests.test_dimension_five_character
```

For the rigorous dimension-five double-sine certificate:

```bash
PYTHONPATH=scripts python3 scripts/certify_dimension_five_double_sine.py
```

Every archived file is covered by `ARCHIVE_CONTENTS.sha256`.

The manuscripts and documentation use CC BY 4.0; executable code uses
the MIT license. See `LICENSE` and `LICENSE-CODE`.
