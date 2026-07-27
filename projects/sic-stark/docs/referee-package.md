# SIC--Stark referee package

This directory accompanies
[`sic-stark-paper-draft.md`](sic-stark-paper-draft.md).

The review manuscript is available as
[`../paper/sic-stark-dimension-four.tex`](../paper/sic-stark-dimension-four.tex)
and the compiled
[`../paper/sic-stark-dimension-four.pdf`](../paper/sic-stark-dimension-four.pdf).

## Verification layers

1. `python3 scripts/generate_referee_certificates.py`
   emits the deterministic project certificate.
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

## Claims requiring human convention review

- the reciprocal double-sine convention between `Zauner.jl` and Kopp;
- the exceptional zero characteristic;
- the identification of the selected ray class and infinite place;
- the normalized cocycle square in Kopp's Theorem 1.1;
- the final projector normalization after the rank-one certificate.

These are listed explicitly in Section 10 of the paper draft.
