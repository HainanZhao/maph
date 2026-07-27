# SIC--Stark referee package

This directory accompanies
[`sic-stark-paper-draft.md`](sic-stark-paper-draft.md).

The review manuscript is available as
[`../paper/sic-stark-dimension-four.tex`](../paper/sic-stark-dimension-four.tex)
and the compiled
[`../paper/sic-stark-dimension-four.pdf`](../paper/sic-stark-dimension-four.pdf).

## Verification layers

1. `python3 scripts/generate_referee_certificates.py`
   emits the deterministic project certificate. Version 2 contains the
   exact \(4\times4\) Laurent matrix and all 36 exact minor quotients,
   encoded as rational vectors in the coefficient basis printed in the
   JSON file.
2. `gp -q scripts/referee_pari_audit.gp`
   independently checks the quartic field, integral basis, class group,
   regulator, fundamental units, and ray groups.
3. `python3 -m unittest discover -s tests -v`
   runs the exact regression suite.
4. `python3 scripts/explore_dimension_four_double_sine.py`
   performs an independent numerical branch audit.

Generated review artifacts belong in `certificates/`:

- `dimension-four-certificate.json`
- `pari-audit.txt`
- `test-suite.txt`
- `double-sine-audit.txt`

## Exact scope of the package

- The finite certificate proves a rank-one implication for the one
  explicitly defined matrix in the manuscript.
- It does not certify both formal TCC shifts.
- The manuscript uses the reciprocal of Kopp's `Sin_2`; this is now a
  definition, not an implicit convention.
- The exceptional zero characteristic and its normalization to
  \(a_0=1\) are explicit.
- The ray-group order and class-number computations are certified.
- The ray-class, characteristic, stabilizer, multiplier, sign, and
  cocycle conversion needed to specialize Kopp's Theorem 1.1 have not
  been proved. The manuscript labels this as equation `(KL)` and does
  not use it as an unconditional premise.

Accordingly, the unconditional theorem in the revised manuscript is
the finite reduction `(SV) => rank K=1`, not the full dimension-four
Twisted Convolution Conjecture.
