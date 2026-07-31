# Ray-to-form obstruction

Recorded: 2026-07-31 UTC

## Proposed bridge and its type error

The preregistered map asked a character-level input
\((K,\mathfrak m,\chi,\infty_2)\) to produce one form,
characteristic, and positive lift. The source theorems do not provide
such a map.

Kopp's specialization starts with additional class-level data:

\[
(\mathfrak A,\mathfrak b,\alpha,\boldsymbol r,B),
\qquad
\alpha(r_2\beta-r_1)\mathcal O_K
=\mathfrak A\mathfrak b\mathfrak m,
\]

together with positivity at the omitted real place. A quartic character
\(\chi\) is a Fourier functional on all ray classes. It does not select
one \(\mathfrak A\), one auxiliary ideal \(\mathfrak b\), or one
positive representative. In the SIC papers those data are supplied by
the form/ghost construction before the multiplier comparison begins.

Consequently the correct generic character-level object, if one exists,
cannot be the multiplier of a single tuple. It must be a Fourier
resolvent assembled from a compatible family of class-level cocycle
multipliers, with covariance and lift-independence proved.

## RQ-000129 attempt

The frozen data are:

- \(K=\mathbf Q(\sqrt6)\);
- finite modulus with HNF
  \(\left(\begin{smallmatrix}4&0\\0&2\end{smallmatrix}\right)\), norm
  \(8\);
- one-place ray group \(C_4\);
- faithful source character \([1]\);
- sign class \(2\in C_4\).

Unlike the scalar-modulus SIC anchors, this nonscalar ideal does not
canonically provide a rational denominator for a characteristic.
Neither the census row nor the Engine-C proof records a Kopp tuple
\((\mathfrak A,\mathfrak b,\alpha,\boldsymbol r,B)\), because that
tuple is unnecessary for CM descent. Constructing an arbitrary tuple
and selecting the one whose multiplier matches the known quarter turn
would be post-selection and is forbidden.

Therefore RQ-000129 cannot be evaluated by the supplied-tuple bridge
from its frozen ray-character data alone. Its known phase label was not
used in reaching this verdict.

## Corrected theorem target

A viable next theorem would have two stages:

1. class level: construct a cocycle multiplier
   \(\mu(\mathfrak A)\) independent of the admissible Kopp
   representatives;
2. character level: prove that a Fourier resolvent of the
   \(\mu(\mathfrak A)\) gives the weak-Stark phase modulo \(\mu_4\).

This is substantially different from—and more meaningful than—the
original three-feature congruence.
