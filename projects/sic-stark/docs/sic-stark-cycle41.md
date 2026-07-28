# SIC--Stark research cycle 41: determinant theorems do not give the scalar

Date: 2026-07-27

## Outcome

Three possible "free" closures were tested and ruled out:

1. Roblot P1/P2 uniqueness;
2. Stark's theorem for rational-valued characters; and
3. dihedral weight-one modularity.

Each controls a determinant, product, or rational character orbit.  None
isolates the identity-class number \(D_0\).

## Roblot P1/P2

The exact candidate \(\eta=x_{\mathrm{alg}}^2\) satisfies P1, and in this
class-number-one example the P2 conditions away from \(2\) and \(3\) add
no missing odd-prime obstruction.  Roblot's Proposition 4.1 therefore
proves

\[
 |\Lambda|=|R|,
\]

where

\[
 \Lambda=L'_S(0,\chi_1),\qquad
 R=r_0+\zeta_6r_1+\zeta_6^2r_2.
\]

However, P1/P2 uniqueness compares two *algebraic unit solutions*.  It
does not assert that the analytic \(L\)-value logarithm vector is one of
those solutions; that assertion is precisely the rank-one Stark
conjecture.  Thus uniqueness cannot be used to manufacture existence.

## Rational-character Stark theorem

The primitive rational orbit is \(\{\chi_1,\chi_5\}\).  Its rational
Artin \(L\)-function has leading coefficient

\[
 L'_S(0,\chi_1)L'_S(0,\chi_5)=|\Lambda|^2.
\]

The corresponding regulator determinant is \(|R|^2\).  Hence the
rational-character theorem lands on the same modulus identity already
proved by Roblot.  It does not compute

\[
 \Lambda+\bar\Lambda=2\operatorname{Re}\Lambda,
\]

because Artin formalism is multiplicative in \(L\)-functions, not
additive in their leading terms.

This is the key reason rationality of the character orbit does not make
dimension six another dimension-four quadratic case.

## Dihedral modularity

Inducing the primitive Hecke character toward \(\mathbb Q\) places the
problem in the neighborhood of dihedral weight-one forms.  Theta-series
modularity supplies analytic continuation and a functional equation, but
the required logarithmic unit formula remains a Stark-unit statement.
Current derived-Hecke results concern different adjoint or symmetric-square
Stark units and do not evaluate this mixed-signature ray-class invariant.

## Conclusion

There is no known determinant or modularity theorem that turns
\(|\Lambda|=|R|\) into \(D_0=r_0\).  A proof must use information that is
not invariant under continuous rotation of the primitive component.

## Sources

- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Proposition 4.1 and Section 4,
  <https://arxiv.org/abs/1112.2820>.
- A. Nickel, *The strong Stark conjecture for totally odd characters*,
  for the rational-character theorem background and the scope of modern
  strong-Stark results, <https://arxiv.org/abs/2106.05619>.
- H. Darmon, M. Harris, V. Rotger, and A. Venkatesh,
  *The derived Hecke algebra for dihedral weight one forms*,
  <https://arxiv.org/abs/2207.01304>.

