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
   complete 16-characteristic overlap audit, the exact \(4\times4\)
   Laurent matrix, and all 36 exact minor quotients, encoded as rational
   vectors in the coefficient basis printed in the JSON file.
2. `python3 scripts/verify_referee_certificate.py`
   independently reloads that JSON and verifies every polynomial
   identity using `fractions.Fraction` arithmetic.
3. `gp -q scripts/referee_pari_audit.gp`
   independently checks the quartic field, integral basis, class group,
   regulator, fundamental units, and ray groups.
4. `python3 -m unittest discover -s tests -v`
   runs the exact regression suite.
5. `python3 scripts/explore_dimension_four_double_sine.py`
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
  differ between source versions.  Replacing it by Kopp's convention
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

## Dimension-five continuation

The separate research note
[`sic-stark-dimension-five.md`](sic-stark-dimension-five.md) records the
next-dimensional calculation. Its artifacts are also checksummed:

- `dimension-five-finite.json` contains the exact 100-minor Laurent system;
- `dimension-five-pari.txt` contains the ray and Stark-polynomial audit;
- `dimension-five-exact-minors.txt` records exact vanishing of all 100
  minors in the correctly labeled Stark-conjugate factor;
- `dimension-five-numerical.txt` independently checks the original
  double-sine values;
- `dimension-five-bridge.json` audits all 25 characteristics, including
  Kopp-positive lifts, ray-class logs, cocycle signs, and all 24
  Kopp/AFK multiplier comparisons;
- `dimension-five-root-isolation.txt` gives rational Sturm intervals for
  all 16 real roots of the absolute packet polynomial;
- `dimension-five-embedding-certificate.txt` certifies the interval-root
  to `nfgaloisconj` labels and uniquely selects factor four by the positive
  \(\sqrt5,\sqrt6\) subfield embeddings;
- `dimension-five-character-support.json` proves that the Kopp difference
  is supported on four order-eight characters and has zero coefficient at
  the unique quadratic character.
- `dimension-five-local-isolation.txt` proves that four fan minors have an
  invertible Jacobian at the certified packet, so the rank-one point is
  reduced and locally isolated.
- `dimension-five-shintani.txt` gives the exact Shintani specialization,
  sign classes, imaginary-ray conductor, and safe exponent \(5760\);
- `dimension-five-unit-lattice.txt` certifies the labeled \(K\)-isomorphism,
  unit data, nonsplit modulus-one conjugates, Frobenius action, and exact
  rational interval propagation of all eight real orbit labels;
- `dimension-five-double-sine-intervals.txt` is the Arb enclosure used in
  the Voutier height-rigidity step.

The dimension-five theorem has now been rewritten unconditionally.  The
supporting research note
[`sic-stark-dimension-five-unconditional-closure.md`](sic-stark-dimension-five-unconditional-closure.md)
records the proof of its former Stark-value input by specializing Shintani's
1978 theorem and applying certified height rigidity.  The rewritten
manuscript is
[`../paper/sic-stark-dimensions-four-five.tex`](../paper/sic-stark-dimensions-four-five.tex),
with compiled
[`../paper/sic-stark-dimensions-four-five.pdf`](../paper/sic-stark-dimensions-four-five.pdf).
