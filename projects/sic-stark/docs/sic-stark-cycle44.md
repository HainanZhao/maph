# SIC--Stark research cycle 44: the exact theorem boundary in dimension six

Date: 2026-07-27

## Outcome

The remaining dimension-six statement has been reduced to, and identified
with, one currently unproved real-quadratic Shintani--Stark special case.
There is no remaining finite matrix calculation, sign choice, square,
reciprocal, Artin label, or regulator-index ambiguity.

Let

\[
 K=\mathbb Q(\sqrt{21}),\qquad
 \beta=\frac{5+\sqrt{21}}2,
\]

and let \(C\) be the identity class for the one-real-place modulus \(6\).
If

\[
 D_0=\zeta'(0,C)-\zeta'(0,\bar C),
\]

then the proved Kronecker-limit specialization gives

\[
 \exp(D_0/2)=x_{\rm an},
\]

where \(x_{\rm an}>1\) is the convention-matched three-double-sine
product.  The finite class-field and unit certificates isolate
\(x_{\rm alg}\in(2.212885,2.212886)\), the unique root in that interval
of

\[
\begin{aligned}
Q(X)={}&X^{12}+3X^{11}-6X^{10}-16X^9+3X^8+27X^6\\
&+3X^4-16X^3-6X^2+3X+1.
\end{aligned}
\]

Thus the missing theorem is exactly

\[
\boxed{x_{\rm an}=x_{\rm alg}.}
\]

Equivalently, it is the identity-class scalar instance
\(D_0=r_0\) of the complex rank-one abelian Stark conjecture for the
primitive order-six character.

## Exact conductor obstruction

The proper divisor moduli do not contain the missing character.  Exact
PARI/GP computation, certified with `bnfcertify`, gives the one-place ray
groups

\[
\begin{array}{c|cccc}
\text{finite modulus}&1&2&3&6\\ \hline
\text{ray group}&1&1&C_2&C_6.
\end{array}
\]

For a generator \(g\) of \(C_6\), reduction to conductor three has kernel
\(\langle g^2\rangle\simeq C_3\).  If
\(\chi_k(g)=\zeta_6^k\), then \(\chi_k\) descends exactly when

\[
 \chi_k(g^2)=1,
\]

which among the odd characters holds only for \(k=3\).  Consequently:

- \(\chi_3\) is the already-proved quadratic lower stratum;
- \(\chi_1,\chi_5\) are primitive at level six and disappear under
  conductor lowering;
- modulus two supplies no second quotient because its ray group is
  trivial.

This proves character-theoretically that divisor-conductor formulas
cannot recover the required primitive component.

## Exact distribution obstruction

The same obstruction is visible directly in the double-sine products.
The four lifts of the conductor-three orbit are

\[
\begin{aligned}
\mathcal O_1&=((0,1),(1,0),(5,5)),\\
\mathcal O_2&=((0,4),(4,0),(2,2)),\\
\mathcal O_3&=((3,1),(4,3),(5,2)),\\
\mathcal O_4&=((3,4),(1,3),(2,5)).
\end{aligned}
\]

Double-sine duplication gives only

\[
 P_3=P_{6,1}P_{6,2}P_{6,3}P_{6,4}.
\]

In logarithmic coordinates this is one rank-one equation in four
unknowns.  Its nullspace has dimension three and contains directions
that change the selected coordinate \(\log P_{6,1}\).  Therefore the
known algebraic conductor-three evaluation cannot isolate the TCC lift.

## Applicability audit of unconditional theorems

The standard unconditional theorem families stop strictly short of the
boxed identity:

1. Shintani's explicit \(\mathbb Q(\sqrt{21})\) calculation evaluates the
   conductor-three product.  It is precisely the \(C_2\) quotient above,
   not the primitive conductor-six lift.
2. Stark's rational-character theorem sees
   \(L(s,\chi_1)L(s,\chi_5)\).  Since both factors vanish simply, its
   leading coefficient is
   \(|L'_S(0,\chi_1)|^2\); it determines the modulus, not the real part
   or phase.
3. Relative-quadratic and higher-rank Stark results similarly produce a
   regulator determinant after inducing from the quadratic top layer.
   They do not separate the primitive Fourier eigenvalue.
4. The proved Brumer--Stark theorem concerns CM extensions.  The
   dimension-six ray field has mixed signature \((6,3)\).
5. Totally-odd strong-Stark results do not apply to a character that is
   odd at exactly one of the two real places.
6. Recent effective Shintani formulas express the relevant Hecke
   \(L\)-function in finite Shintani-zeta or cyclic-dilogarithm terms,
   but do not prove algebraicity of this value.

The literature itself marks this boundary: current work on Shintani
invariants states that their class-field algebraicity over real quadratic
fields remains unproved.

## Honest theorem statement

The dimension-six result is therefore:

> All finite algebra, ray-class labels, regulator indices, analytic
> normalizations, and orientation signs are unconditional.  The complete
> dimension-six TCC bridge follows from the single explicit
> Shintani--Stark identity \(x_{\rm an}=x_{\rm alg}\).

Calling the full dimension-six result unconditional would amount to
claiming a new proof of this open special case.  No such proof has been
obtained here.

## Reproducibility

- `scripts/dimension_six_conductor_obstruction.gp`
- `scripts/dimension_six_lift_relation.py`
- `scripts/dimension_six_scalar_closure.py`
- `scripts/certify_dimension_six_orientation.py`
- `scripts/dimension_six_roblot_index.gp`

## Primary sources

- T. Shintani, *On a Kronecker limit formula for real quadratic fields*,
  J. Fac. Sci. Univ. Tokyo 24 (1977), 167--199.
- N. Kurokawa and M. Wakayama, *Algebraicity and transcendency of basic
  special values of Shintani's double sine functions*, Proc. Edinburgh
  Math. Soc. 49 (2006), 361--366.
- S. Yamamoto, *Factorization of Shintani's ray class invariant for
  totally real fields*, RIMS Kôkyûroku Bessatsu B19 (2010), 249--254.
- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422.
- M.-H. Tomé, *Arithmetic of Hecke L-functions of quadratic extensions
  of totally real fields*, J. Number Theory 268 (2025), 482--514.
- B. Yalkinoglu, *Shintani's invariant via cyclic quantum dilogarithm*,
  arXiv:2508.18320.
