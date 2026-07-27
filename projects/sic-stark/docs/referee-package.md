# SIC--Stark referee package

This directory accompanies
[`sic-stark-paper-draft.md`](sic-stark-paper-draft.md).

The review manuscript is available as
[`../paper/sic-stark-dimension-four.tex`](../paper/sic-stark-dimension-four.tex)
and the compiled
[`../paper/sic-stark-dimension-four.pdf`](../paper/sic-stark-dimension-four.pdf).

## Verification layers

1. `python3 scripts/generate_referee_certificates.py`
   emits the deterministic project certificate. Version 3 contains the
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
- The finite file certifies the identity-twist matrix.  The manuscript
  proves that this is the \(\lambda=1\) equation and applies the exact
  conjugation rule \(\bar\lambda=1-\lambda\) to obtain \(\lambda=0\).
- The manuscript defines its double sine directly as
  \(\Gamma_2(z)/\Gamma_2(\omega_1+\omega_2-z)\), avoiding names that
  differ between source versions.  Replacing it by the reciprocal
  changes \(x^2=u\) to \(x^2=4/u\).
- The exceptional zero characteristic and its normalization to
  \(a_0=1\) are explicit.
- The ray-group order and class-number computations are certified.
- The Kopp specialization uses modulus \((4)\infty_2\), the identity
  ray class, characteristic \((0,1/4)^T\), stabilizer
  `[[21,-8],[8,-3]]`, exponent \(n=1\), and multiplier \(-i\).
- The PARI transcript contains `L_BNFCERTIFY=1`, making its
  class-group and unit computation unconditional.

Accordingly, the revised manuscript claims the complete
dimension-four Twisted Convolution Conjecture, but no higher-dimensional
case.
