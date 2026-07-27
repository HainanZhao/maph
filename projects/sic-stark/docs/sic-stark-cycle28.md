# SIC--Stark research cycle 28: the period-one cone does not lower

Date: 2026-07-27

## Outcome

The direct Shintani--Yamamoto cone route has now been specialized exactly
to the primitive dimension-six characteristic.  It proves two useful
facts:

1. the period-one cone formula is exactly the convention-matched
   three-double-sine Kopp/AFK value; and
2. conductor lowering from modulus \(6\) to modulus \(3\) determines only
   the product of four modulus-six lift orbits.

Thus this route verifies the analytic normalization but does **not** prove
the remaining primitive algebraicity identity.  The unresolved statement
remains

\[
 L_S'(0,\chi_1)
 =
 r_0+\zeta_6r_1+\zeta_6^2r_2.
\]

This is a genuine rank-one Stark--Shintani identity for the mixed-signature
order-six character, not a disguised consequence of the already-proved
quadratic component.

## 1. Period-one cone data

Put

\[
 K=\mathbb Q(\sqrt{21}),\qquad
 \beta=\frac{5+\sqrt{21}}2.
\]

Then

\[
 \beta=5-\frac1\beta,
\]

so its minus continued fraction is

\[
 \beta=[\![5]\!].
\]

The least totally positive unit congruent to \(1\) modulo \(6\) is
\(\beta^3\).  Consequently Yamamoto's cone decomposition for the identity
ray class has three factors.

For a modulus \(n\), write the rational cone coordinates as
\((x_k,y_k)\), with \(0<x_k\leq1\) and \(0\leq y_k<1\).  In residue
coordinates

\[
 (a_k,b_k)=(nx_k,ny_k)\pmod n,
\]

where \(x_k=1\) is represented by \(a_k=0\), Yamamoto's recurrence becomes

\[
 (a_{k+1},b_{k+1})
 =
 (5a_k+b_k,-a_k)\pmod n.
\]

At modulus \(6\), the identity-class initial point is \((0,1)\), and the
exact orbit is

\[
 (0,1)\longmapsto(1,0)\longmapsto(5,5)\longmapsto(0,1).
\]

Therefore

\[
 (x_k,y_k)
 =
 \left(1,\frac16\right),\
 \left(\frac16,0\right),\
 \left(\frac56,\frac56\right),
\]

and the three cone arguments \(z_k=x_k\beta+y_k\) are

\[
 \beta+\frac16,\qquad
 \frac{\beta}{6},\qquad
 \frac{5(\beta+1)}6.
\]

## 2. Exact comparison with the Kopp/AFK product

Let \(S(\beta,z)\) denote the double sine in the
Yamamoto--Shintani--Kopp convention.  Its two quasiperiodicity formulas
give, for \(0<a<1\),

\[
\begin{aligned}
 S(\beta,a)
 &=2\sin(\pi a)\,S(\beta,\beta+a),\\
 S(\beta,a\beta)
 &=2\sin(\pi a)\,S(\beta,1+a\beta).
\end{aligned}
\]

Dividing cancels the elementary sine factor:

\[
\boxed{
S(\beta,\beta+a)S(\beta,a\beta)
=
S(\beta,a)S(\beta,1+a\beta).
}
\]

Taking \(a=1/6\) transforms the first two cone factors and proves

\[
\begin{aligned}
 &S\left(\beta,\beta+\frac16\right)
 S\left(\beta,\frac{\beta}{6}\right)
 S\left(\beta,\frac{5(\beta+1)}6\right)\\
 &\qquad=
 S\left(\beta,\frac16\right)
 S\left(\beta,1+\frac{\beta}{6}\right)
 S\left(\beta,\frac{5(\beta+1)}6\right).
\end{aligned}
\]

The right-hand side is exactly the three-factor primitive
Kopp/AFK cocycle value, in Kopp's convention.  Passing to the reciprocal
paper convention inverts both sides.

This is a useful convention certificate: the direct cone formula and the
cocycle specialization agree term for term.  It is not an independent
algebraicity evaluation.

## 3. Exact conductor-lowering relation

At modulus \(3\), the same recurrence gives

\[
 (0,1)\longmapsto(1,0)\longmapsto(2,2)\longmapsto(0,1),
\]

or

\[
 \left(1,\frac13\right),\
 \left(\frac13,0\right),\
 \left(\frac23,\frac23\right).
\]

Reduction modulo \(3\) sends the selected modulus-six orbit to this
modulus-three orbit.  It is tempting, but incorrect, to conclude that the
known modulus-three evaluation determines the selected lift.

The precise relation follows from double-sine duplication:

\[
\boxed{
S(\beta,z)
=
\prod_{e,f\in\{0,1\}}
S\left(\beta,\frac{z+e\beta+f}{2}\right).
}
\]

To see that there is no normalization factor, write the double sine as a
difference of Barnes double-zeta derivatives.  Splitting the two lattice
indices into their parity classes gives the displayed product, while the
possible \(\log2\) term cancels because

\[
\zeta_2(0,\beta,\beta+1-z)
=
\zeta_2(0,\beta,z).
\]

The four lifts of the first modulus-three point are

\[
 (0,1),\quad(0,4),\quad(3,1),\quad(3,4)\pmod6.
\]

They generate four distinct length-three cycles:

\[
\begin{aligned}
\mathcal O_1&=((0,1),(1,0),(5,5)),\\
\mathcal O_2&=((0,4),(4,0),(2,2)),\\
\mathcal O_3&=((3,1),(4,3),(5,2)),\\
\mathcal O_4&=((3,4),(1,3),(2,5)).
\end{aligned}
\]

The twelve duplication factors group into these four orbits.  Hence, if
\(P_3\) is the known lower-conductor product and \(P_{6,j}\) denotes the
product for \(\mathcal O_j\), then

\[
\boxed{
P_3=P_{6,1}P_{6,2}P_{6,3}P_{6,4}.
}
\]

The TCC requires \(P_{6,1}\).  The algebraic value of \(P_3\) supplies one
product relation among four lift invariants and cannot isolate
\(P_{6,1}\).

The ray-character calculation says the same thing more economically.
The modulus-three one-place group is \(C_2\), while the modulus-six
one-place group is \(C_6\).  Conductor lowering sees the quotient \(C_2\)
and therefore the quadratic character \(\chi_3\).  The pair
\(\chi_1,\chi_5\) is nontrivial on the cubic kernel and has conductor
\(6\); it disappears from the lowered data.

## 4. Comparison with the algebraic resolvent

The exact algebraic candidate \(\varepsilon=x^2\) has arithmetic-Frobenius
logarithms

\[
 r_j=\log|\sigma^j(\varepsilon)|.
\]

The quadratic relation obtained by conductor lowering is

\[
 L_S'(0,\chi_3)=r_0-r_1+r_2=2\log Y,
\]

which is already unconditional.

The primitive component is

\[
 \Lambda_1=L_S'(0,\chi_1)
\]

and the candidate algebraic resolvent is

\[
 \mathcal R_1(\varepsilon)
 =r_0+\zeta_6r_1+\zeta_6^2r_2.
\]

They agree numerically to more than \(100\) decimal digits, but the
period-one cone and duplication formulas yield no equation separating
\(\Lambda_1\) from its primitive companions.  Numerical agreement is not
a proof of

\[
\Lambda_1=\mathcal R_1(\varepsilon).
\]

## 5. Theorem-level escape routes checked

Three existing theorem families do not close this case:

1. Shintani's 1978 weak algebraicity theorem requires the ray field to be
   quadratic over its maximal absolutely abelian subfield.  Here that
   subfield is \(K\), while the relevant ray field has degree \(6\) over
   \(K\).
2. Roblot's cyclic-sextic theorem assumes no prime above \(3\) is wildly
   ramified.  The cubic component here has ramification index \(3\) above
   \(3\).  In addition, Roblot's conclusion is a weak result up to
   absolute values and does not by itself determine the oriented complex
   character value.
3. The proved Brumer--Stark theorem for abelian CM extensions does not
   apply: this is a mixed-signature ray field of signature \((6,3)\), not
   a CM extension.

Thus no located published theorem converts the remaining double-sine
value into the Artin-labeled unit.

## 6. Recommendation

The dimension-six project has reached a clean theorem boundary, not a
finite-computation ambiguity.  Continuing to apply standard reflection,
shift, multiplication, or conductor-distribution identities will only
produce norms and products invariant under the missing primitive
orientation.

The two honest routes are now:

1. prove a new explicit modulus-six Shintani evaluation for
   \(\mathbb Q(\sqrt{21})\), strong enough to establish the complex
   order-six regulator identity; or
2. treat the dimension-six finite theorem as conditional on that single
   identity and move the unconditional search to a dimension whose
   relevant character packet is entirely quadratic.

For the broader SIC program, route 2 is the better next experiment.
For completing dimension six specifically, route 1 is unavoidable and is
essentially a small explicit case of the rank-one Stark--Shintani
algebraicity problem.

## Reproducibility

- `scripts/dimension_six_shintani_cycle.py`
- `scripts/dimension_six_primitive_fourier_audit.gp`
- `scripts/dimension_six_artin_orientation.gp`
- `scripts/analyze_dimension_six_orientation_obstruction.py`

## Primary sources

- S. Yamamoto, *On Kronecker limit formulas for real quadratic fields*,
  J. Number Theory 128 (2008), 426--450; arXiv:math/0602615.
- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, J. Math. Soc. Japan 30 (1978), 139--167.
- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422; arXiv:1112.2820.
- S. Dasgupta and M. Kakde, *On the Brumer--Stark conjecture*,
  Ann. of Math. 197 (2023), 289--388; arXiv:2010.00657.
- G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, arXiv:2411.06763.
