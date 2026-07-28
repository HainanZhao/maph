# SIC--Stark research cycle 93: theorem-coverage audit for dimension six

Date: 2026-07-28

## Question

Can an existing cyclic-sextic Brumer--Stark theorem or Tangedal's
double-sine theorem supply the remaining oriented modulus-six identity?

## Cyclic-sextic Brumer--Stark

No.  Greither--Roblot--Tangedal work with an abelian extension \(E/F\)
in which \(F\) is totally real and \(E\) is totally complex; after the
opening definitions their main results impose the stronger CM
hypothesis.  Their real-quadratic cyclic-degree-six theorem is a theorem
in that setting.

The dimension-six one-place ray field instead has

\[
 \operatorname{sig}(H)=(6,3).
\]

It is neither totally complex nor CM.  Thus the phrase “\(F\) real
quadratic and \(E/F\) cyclic of degree six” is not sufficient: the
signature hypothesis excludes the field needed here.

## Tangedal's double-sine paper

The published abstract makes two logically different claims:

1. every *existent* real-quadratic Stark unit has a canonical expression
   in Tangedal's double-sine invariants; and
2. existence is proved in certain special cases.

The first statement is conditional on the Stark unit.  It cannot be used
to prove that the dimension-six analytic value is algebraic.

The exact \(\mathbf Q(\sqrt{21})\) algebraic evaluation visible in the
subsequent literature is Shintani's modulus-three identity

\[
\begin{aligned}
 &S_2(1/3\mid 1,\beta)
 S_2(1+\beta/3\mid 1,\beta)
 S_2((2+2\beta)/3\mid 1,\beta)\\
 &\qquad =
 \left(
  \frac{(1+\sqrt{21})/2-\sqrt{(3+\sqrt{21})/2}}{2}
 \right)^{1/2},
 \qquad \beta=\frac{5+\sqrt{21}}2.
\end{aligned}
\]

That is precisely the lower modulus-three stratum already used
unconditionally in this project.  The unresolved primitive character has
conductor \((6)\infty_2\), so the modulus-three formula does not identify
its selected level-six lift.

## Conclusion

Neither source closes the remaining bridge.  The theorem-coverage failure
is exact:

\[
\boxed{
\text{CM cyclic-sextic Brumer--Stark does not cover signature }(6,3);
\quad
\text{the known }\sqrt{21}\text{ formula is level }3,\text{ not }6.
}
\]

## Primary sources

- C. Greither, X.-F. Roblot, and B. A. Tangedal,
  *The Brumer--Stark conjecture in some families of extensions of
  specified degree*,
  <https://math.univ-lyon1.fr/~roblot/resources/bsfam.pdf>.
- B. A. Tangedal,
  *Continued fractions, special values of the double sine function, and
  Stark units over real quadratic fields*,
  <https://doi.org/10.1016/j.jnt.2006.09.011>.
- H. Tanaka, *Special values of multiple sine functions*,
  <https://www.jstage.jst.go.jp/article/kyushujm/62/1/62_1_123/_pdf>.

