# Unconditional closure of the canonical dimension-eight packet

## Theorem

For the canonical dimension-eight admissible tuple of order conductor
three and form discriminant \(45\), both \(0\) and \(1\) are formal TCC
shifts.

This does not yet assert the result for the separate maximal-order
discriminant-five tuple.

## 1. Linear reinduction

The two quartic Artin representations over
\(\mathbf Q(\sqrt5)\) are also induced from quartic ray characters over
\(\mathbf Q(\sqrt{-6})\) (and independently over
\(\mathbf Q(\sqrt{-30})\)).  Exact character comparison on the
degree-sixteen normal closures proves equality of the complete Artin
\(L\)-functions, with no scalar twist.

The two convenient character fields over
\(M=\mathbf Q(\sqrt{-6})\) are

\[
\begin{aligned}
E_0:\;&X^8-4X^6-12X^5+18X^4+48X^3-16X^2-168X+166,\\
E_1:\;&X^8-4X^7+8X^5+28X^4+96X^3+144X^2+96X+24.
\end{aligned}
\]

They are cyclic quartic over \(M\), have signature \((0,4)\), and have
two roots of unity.  Their exact ray characters are printed by
`dimension_eight_linear_cm_reinduction.gp`.  Equality of induced
characters is checked on every element of the order-sixteen Galois
group, so equality of all local Artin factors is formal.  The first 500
Dirichlet coefficients are additionally compared exactly as an
implementation audit.

## 2. The proved imaginary-quadratic theorem

Stark's rank-one theorem is proved for every abelian extension of an
imaginary quadratic base.  Applied to \(E_b/M\), it supplies a global
unit \(\varepsilon_b\) such that

\[
 \zeta'_S(0,g)
 =-\frac1{e_b}\log|g(\varepsilon_b)|,
 \qquad e_b=|\mu(E_b)|=2.
\]

Consequently, for the convention-matched quartic character,

\[
 L'_S(0,\chi_b)
 =-\frac12\sum_{g\in C_4}
   \chi_b(g)\log|g(\varepsilon_b)|.
\tag{1}
\]

Equation (1) is the missing discreteness statement.  It gives an
oriented complex logarithmic resolvent of an actual unit, rather than
only Roblot's equality of absolute values.

## 3. Integral coordinate isolation

Let \(u_{b,1},u_{b,2},u_{b,3}\) be PARI's certified fundamental units.
For compatible generators of \(\operatorname{Gal}(E_b/M)\), the exact
unit actions are

\[
\begin{aligned}
A_0&=\begin{pmatrix}-1&0&0\\0&0&1\\0&-1&0\end{pmatrix},&
A_1&=\begin{pmatrix}-1&0&0\\0&0&-1\\0&1&0\end{pmatrix}.
\end{aligned}
\]

Thus the quartic anti-unit component is the integral lattice spanned by
\(u_{b,2},u_{b,3}\).  The exact order/maximal-order character dictionary
is

\[
 (a,b,c)\longmapsto[a-2b,b,c-a].
\]

Hence the characters labeled \([1,0,0]\) and \([1,1,0]\) in the paper
come from \((1,0,1)\) and \((3,1,1)\), respectively.  With conjugate
Fourier coefficients, rigorous Arb evaluation of Kopp's eight
independent partial-zeta differences gives

\[
\begin{aligned}
L'_0&=8.281565738\ldots+5.457798022\ldots i,\\
L'_1&=-2.968853827\ldots+6.247666148\ldots i
\end{aligned}
\]

with radii below \(10^{-8}\).

At every upper-half-plane embedding, inversion of the certified
two-dimensional unit-log matrix puts the quartic component of the unit
in one of the four balls

\[
(0,2),\quad(-2,0),\quad(0,-2),\quad(2,0),
\]

each of radius below \(5\cdot10^{-9}\).  Since (1) guarantees that the
coordinates are integral, the unique possibilities are exact.  The
Stark-unit component is therefore the \(C_4\)-orbit of

\[
 u_{b,3}^{\,2}.
\tag{2}
\]

The first fundamental-unit coordinate is irrelevant to the quartic
Fourier projection and need not be determined.

## 4. Exact bridge back to the real units

Let \(\eta_0,\eta_1\) be the real-quadratic units used in the original
Roblot computation.  Embed the corresponding real and
imaginary-quadratic character fields in their common degree-sixteen
normal closure \(N_b\).  The closures have signature \((0,8)\).

Complex conjugations are detected exactly as involutions whose fixed
fields have a real place.  For every real embedding \(\rho\) of
\(\eta_b\), exact arithmetic in \(N_b\) gives, for a compatible CM
embedding \(\iota\),

\[
 \rho(\eta_b)^{\pm1}
 =
 \iota(u_{b,3}^{\,2})\,
 \overline{\iota(u_{b,3}^{\,2})}.
\tag{3}
\]

All such identities, including reciprocal choices, are enumerated by
`dimension_eight_cm_real_unit_bridge.gp`.  Equation (3), together with
the Arb orientation balls, proves the formerly conditional identities

\[
\begin{aligned}
L'_S(0,[1,0,0])&=R_0,\\
L'_S(0,[1,1,0])&=R_1.
\end{aligned}
\tag{4}
\]

No equality of logarithms is inferred from numerical agreement alone:
Stark's theorem supplies the integral unit lattice, Arb selects its
unique coordinates, and (3) is an exact algebraic identity.

## 5. Finite conclusion

Consequently the two oriented identities formerly labeled as the
dimension-eight closure targets are unconditional.  Together with the
existing lower-stratum and 784-minor certificates, this proves both
formal shifts for the canonical conductor-three tuple.

The exact finite script independently verifies, for each shift,

\[
\operatorname{Tr}\Pi=1,\qquad
\Pi^2=\Pi,\qquad
784\text{ rank-two minors vanish}.
\]

The result does **not** yet assert the complete formal TCC for every
dimension-eight admissible tuple.  Dimension-eight admissibility has
\(j=2\), so forms of conductor dividing \(f_2=3\) include the
maximal-order discriminant-five case as well as the canonical
discriminant-forty-five case treated here.

## Reproduction

```bash
gp -q scripts/dimension_eight_linear_cm_reinduction.gp
gp -q scripts/dimension_eight_cm_unit_lattice.gp
PYTHONPATH=/path/to/python-flint:scripts \
  python3 scripts/certify_dimension_eight_cm_orientation.py
gp -q scripts/dimension_eight_cm_real_unit_bridge.gp
gp -q scripts/dimension_eight_exact_tcc.gp
```
