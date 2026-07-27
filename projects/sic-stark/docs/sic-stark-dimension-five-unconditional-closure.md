# Dimension five: unconditional closure of the Stark-value step

Date: 27 July 2026

## Result

Let
\[
K=\mathbb Q(\sqrt3),\qquad \beta=2+\sqrt3,
\qquad \mathfrak m=(5)\infty_2,
\]
where
\(\infty_1(\sqrt3)=+\sqrt3\) and
\(\infty_2(\sqrt3)=-\sqrt3\), and let \(I\) be the principal class of
\(\operatorname{Cl}_{\mathfrak m}(K)\cong C_8\).  Put
\[
X=\exp Z'_{\mathfrak m}(0,I).
\]
The convention-matched Kronecker-limit calculation gives
\[
X=x^2,
\]
where \(x\) is the positive three-double-sine value used by the
dimension-five ghost.

Let \(U>1\) be the root near \(3.890861713943079\) of
\[
\begin{aligned}
P(T)={}&T^8-(8+5\sqrt3)T^7+(53+30\sqrt3)T^6\\
&-(156+90\sqrt3)T^5+(225+130\sqrt3)T^4\\
&-(156+90\sqrt3)T^3+(53+30\sqrt3)T^2\\
&-(8+5\sqrt3)T+1.
\end{aligned}
\]
Then
\[
\boxed{X=U.}
\]
The proof is unconditional.  It does not assume the rank-one Stark
conjecture and does not treat PARI's `bnrstark` output as a proof.

## 1. Why Shintani's 1978 theorem applies

Write \(H\) for the one-infinite-place ray field of modulus
\((5)\infty_2\).  Exact PARI computations give
\[
[H:K]=8,\qquad \operatorname{sig}(H)=(8,4).
\]
The unique octic subfield of \(H/\mathbb Q\) is
\[
M\simeq \mathbb Q(\zeta_{60})^+.
\]
Thus \(M/\mathbb Q\) is abelian, \(H/M\) is quadratic, and, because
\(H/\mathbb Q\) is not Galois, \(M\) is the maximal absolutely abelian
subfield of \(H\).  The signature shows that exactly one real place of
\(K\) splits in \(H\).

These are precisely the field-theoretic hypotheses of Shintani's
Theorem 2 in *On certain ray class invariants of real quadratic
fields*.  PARI orders the roots of \(y^2-4y+1\) increasingly, so the
labeled modulus is entered as `[5,[1,0]]`.

For the remaining hypotheses, Shintani's full narrow ray group is
\[
\operatorname{Cl}_{(5)\infty_1\infty_2}(K)\cong C_8\times C_2.
\]
Let \(\mu\) be the class with residue \(1\bmod5\) and signs
\((-,+)\) at \((\infty_1,\infty_2)\), and let \(\nu\) be the class
with residue \(-1\bmod5\) and signs \((+,+)\).  Then
\[
G=\langle\mu\rangle
\]
is the kernel of the map which forgets \(\infty_1\), and
\[
\operatorname{Cl}_{(5)\infty_1\infty_2}(K)/G
\simeq\operatorname{Cl}_{(5)\infty_2}(K)\simeq C_8.
\]

Every unit is \(\pm\beta^n\), and \(\beta\) has order \(3\) modulo
\(5\).  Hence no totally positive unit is congruent to \(-1\bmod5\),
which is condition (0-3).  There is no norm-\(-1\) unit, since
\(a^2-3b^2=-1\) is impossible modulo \(3\); this implies condition
(0-6).

Units congruent to \(-1\bmod5\) are \(-\beta^{3k}\), which are
negative at \(\infty_2\).  Thus the image of \(\nu\) is the nonidentity
residue/sign class
\[
R=g^4\in\operatorname{Cl}_{(5)\infty_2}(K).
\]
In particular, \(\nu\notin G\).

Finally, this specialization gives exactly the zeta difference used
here.  If \(A\) is the image of a full-narrow class \(c\), then its
inverse image is \(\{c,c\mu\}\), while that of \(RA\) is
\(\{c\nu,c\mu\nu\}\).  Hence
\[
\begin{aligned}
\log X_{(5)}(c,G)
&=\bigl(\zeta'_{\rm full}(0,c)-\zeta'_{\rm full}(0,c\nu)\bigr)\\
&\quad+\bigl(\zeta'_{\rm full}(0,c\mu)
             -\zeta'_{\rm full}(0,c\mu\nu)\bigr)\\
&=\zeta'_{\mathfrak m}(0,A)-\zeta'_{\mathfrak m}(0,RA)
=Z'_{\mathfrak m}(0,A).
\end{aligned}
\]
Thus Shintani's theorem applies to the particular \(X\) in the result,
not merely to an unspecified ray invariant.

The normal closure \(N\) of \(H/\mathbb Q\) is the full two-infinite-place
ray field.  It is also the degree-sixteen ray field over
\(\mathbb Q(\sqrt{-5})\) of conductor
\[
\mathfrak c=
\begin{pmatrix}15&0\\0&3\end{pmatrix}
\]
in PARI's integral basis.  Its ray group is \(C_8\times C_2\).
The quadratic-subfield enumeration contains a unique copy of
\(\mathbb Q(\sqrt{-5})\), so the displayed absolute isomorphism
identifies the required imaginary quadratic subfield rather than merely
an abstract degree-sixteen field.  This is the imaginary-quadratic
field used in Shintani's proof.

Consequently, a positive integral power of every Shintani invariant is
an algebraic unit in \(H\), with the predicted Artin action, and its
conjugates over the other real place of \(K\) have modulus one.

## 2. An explicit safe power

Shintani's proof is constructive.  For a nontrivial imaginary-quadratic
modulus \(\mathfrak d\), his invariant has the form
\[
Z_{\mathfrak d}=\lvert\varphi_{\mathfrak d}\rvert^{1/(6f_{\mathfrak d})}.
\]
Replacing the absolute value by
\(\varphi_{\mathfrak d}\overline{\varphi_{\mathfrak d}}\) and clearing
the distribution exponent \(1/n(S)\) requires a multiple of
\[
12f_{\mathfrak d}n(S).
\]
At the trivial modulus the \(W\)-distribution exponent remains, so the
required exponent is \(12h_kn(S)\).

This denominator clearing is sufficient, not merely necessary:
Shintani's Proposition 4 writes \(Y_{(5)}(c,G)\) as a product of ratios
of the imaginary-quadratic \(W\)-invariants with integral
multiplicities.  For nontrivial \(\mathfrak d\), raising to a multiple
of \(12f_{\mathfrak d}n(S)\) removes both the absolute-value square root
and the distribution denominator; for the trivial divisor the analogous
multiple is \(12h_kn(S)\).  No further rational exponent occurs in that
product.

For the eight divisors of \(\mathfrak c\), the exact clearing exponents
are
\[
384,\ 288,\ 288,\ 144,\ 240,\ 360,\ 360,\ 180.
\]
Their least common multiple is
\[
m=5760.
\]
The real modulus \((5)\) is prime and has no proper divisor satisfying
Shintani's condition (0-3): \(\beta\) has order \(3\) modulo \(5\), so
no totally positive unit is congruent to \(-1\pmod5\), whereas the
trivial modulus fails the condition.  Thus
\(Y_{\mathfrak f}=X_{\mathfrak f}\); no additional induction exponent
is needed.  Hence
\[
X_A^{5760}\in\mathcal O_H^\times
\]
for every ray class \(A\), with
\[
(X_A^{5760})^{\operatorname{Art}(B)}
=X_{AB}^{5760}.
\]

The exact denominator calculation is reproduced by
`scripts/dimension_five_shintani_audit.gp`.

## 3. Exact candidate field and Artin labeling

The absolute candidate polynomial is
\[
\begin{aligned}
p(T)={}&T^{16}-16T^{15}+95T^{14}-260T^{13}+355T^{12}
-348T^{11}\\
&+388T^{10}-300T^9+195T^8-300T^7+388T^6-348T^5\\
&+355T^4-260T^3+95T^2-16T+1.
\end{aligned}
\]
The relative candidate field and the ray field are isomorphic over the
labeled field \(K\), not merely as abstract degree-sixteen fields.
Writing both by `rnfequation`, `nfisisom` returns eight absolute maps,
and an exact substitution check shows that all eight send the candidate
copy of the root of \(y^2-4y+1\) to the ray-field copy.  The root \(U\)
is a unit of norm one.  An exact Buchmann certificate gives
`bnfcertify=1` for this degree-sixteen field.

Let \(g\) denote the raw cyclic basis in the PARI characteristic-lift
audit.  The four displayed characteristics have \(g\)-coordinates
\[
0,\ 6,\ 7,\ 5.
\]
Let \(\mathfrak q\) be the prime above \(3\).  It generates the ray
group and satisfies \(\mathfrak q=g^5\).  Consequently the same four
classes have \(\mathfrak q\)-generator coordinates
\[
0,\ 6,\ 3,\ 1,
\]
since \(5^{-1}=5\bmod8\).  This is the basis used for the Frobenius
orbit below and is the normalized basis stored in the bridge
certificate.  PARI's `bnrL1` call may choose a different local cyclic
basis (the unit transcript reports \(\mathfrak q\)-log \(7\) there);
the script immediately reindexes its output by the ideal
\(\mathfrak q\), so that implementation basis does not enter the
statement.  Modulo \(\mathfrak q\), one has
\(\sqrt3=0\), and the relative polynomial becomes
\[
T^8+T^7+2T^6+2T^2+T+1\in\mathbb F_3[T],
\]
which is irreducible.  Arithmetic Frobenius is therefore \(T\mapsto
T^3\).  Reducing the eight exact automorphisms of the candidate field
modulo this polynomial identifies the Frobenius automorphism uniquely.
Its orbit on \(U\) has logarithms
\[
\begin{split}
(&1.358630653392208,\ 1.712104426904253,\
-0.490802028554627,\ 1.461797117256000,\\
&-1.358630653392208,\ -1.712104426904253,\
0.490802028554627,\ -1.461797117256000).
\end{split}
\]
This agrees, in the same ray-generator order, with the four
Kronecker-limit values and their reciprocals.  The agreement of the
labeling is exact; the decimals merely display the orbit.  More
precisely, a rational interval of width \(10^{-80}\) isolates \(U\).
Exact rational interval evaluation of the eight Frobenius polynomials
puts their successive images in the disjoint windows
\[
\begin{gathered}
(3.890,3.891),\ (5.540,5.541),\ (0.612,0.613),\
(4.313,4.314),\\
(0.257,0.258),\ (0.180,0.181),\ (1.633,1.634),\
(0.231,0.232).
\end{gathered}
\]
Thus the archimedean labels are Galois-equivariant, rather than a
numerical multiset match.

Under the other embedding of \(K\), all candidate conjugates have
modulus one.  An exact Sturm calculation proves this: after substituting
\[
T=2\frac{Y^2-1}{Y^2+1}
\]
in the quartic trace polynomial, `nfpolsturm` returns root counts
\([8,0]\).  Thus all four trace roots at the nonsplit embedding lie in
\((-2,2)\).

These checks are reproduced by
`scripts/dimension_five_unit_lattice_audit.gp`.

## 4. Certified analytic enclosures

The four positive double-sine generators correspond to raw PARI
\(g\)-coordinates \(0,6,7,5\), hence to the normalized bridge
coordinates \(0,6,3,1\) in the \(\mathfrak q\)-generator basis.
Their squares, together with reciprocals, give all eight class values.

Arb interval integration of the regularized Shintani double-sine
integral gives the following enclosures.  In every row, the interval for
the logarithmic difference contains zero:

| characteristic | candidate square |
|---|---:|
| \((0,1)\) | \(3.8908617139430792553\ldots\) |
| \((0,2)\) | \(1.6336259093078891930\ldots\) |
| \((2,4)\) | \(4.3137048000133846360\ldots\) |
| \((3,3)\) | \(5.5406090243168685538\ldots\) |

The largest certified error in
\[
\log(X_A)-\log(U_A)
\]
is less than
\[
2.23\times10^{-9}.
\]
After raising to the Shintani power,
\[
\delta:=5760(2.23\times10^{-9})<1.29\times10^{-5}.
\]

The certificate uses interval Simpson quadrature with an Arb enclosure
of the fourth derivative on every panel.  The interval near zero is
handled by the even Taylor expansion of the regularized integrand; its
positive \(\sinh\)-series gives the checked rational majorant \(4t^2\)
on \(0\le t\le10^{-4}\).  Every reduced argument and its complement
lies in \((1/100,5)\); for \(v\ge36\), the two exponential
denominators exceed \(3/4\), giving the explicit tail bound
\(e^{-36}/9\).  All endpoints, widths, tolerances, and acceptance
comparisons are exact rationals or Arb balls.  Candidate roots are
selected through four disjoint rational isolating intervals,
independently of library ordering.

Run:

```text
PYTHONPATH=/tmp/sic_flint python3 \
  scripts/certify_dimension_five_double_sine.py \
  --digits 40 --tolerance 1e-8
```

The tested interval package was `python-flint==0.9.0`.

## 5. Height rigidity

Set
\[
\eta=\frac{X^{5760}}{U^{5760}}\in H^\times.
\]
At each of the eight real embeddings, the certified calculations and
the exact Artin labeling give
\[
\bigl|\log|\sigma(\eta)|\bigr|<\delta.
\]
At the four complex pairs, both numerator and denominator have modulus
one, so the corresponding logarithms vanish.  Therefore
\[
h(\eta)<\delta<1.29\times10^{-5}.
\]

If \(3\le d=[\mathbb Q(\eta):\mathbb Q]\le16\) and \(\eta\) is not a
root of unity, Voutier's explicit bound gives
\[
h(\eta)>
\frac1{4d}\left(\frac{\log\log d}{\log d}\right)^3.
\]
The minimum for \(3\le d\le16\) is attained at \(d=3\) and is
\[
5.2279533222\ldots\times10^{-5},
\]
which is strictly larger than the certified upper bound.  Degree two
is easier: a non-torsion quadratic unit has height at least
\(\tfrac12\log((1+\sqrt5)/2)\).  A rational unit is \(\pm1\).

It follows that \(\eta\) is a root of unity.  Because \(H\) has a real
embedding, its only roots of unity are \(\pm1\); because \(X\) and \(U\)
are positive at the prescribed embedding, \(\eta=1\).  Hence
\[
X^{5760}=U^{5760},
\]
and positivity finally gives \(X=U\).

## 6. Consequence for the project

The former conditional input
\[
\exp Z'_{(5)\infty_2}(0,I)=U
\]
is now replaced by an unconditional theorem using:

1. Kopp's proved Kronecker-limit formula;
2. Shintani's proved 1978 weak algebraicity theorem in its applicable
   quadratic-over-abelian case;
3. exact ray-field, conductor, unit, Sturm, and Frobenius
   certificates; and
4. a rigorous Arb enclosure followed by Voutier height rigidity.

The dimension-five finite TCC certificate is separate.  This note
closes the analytic Stark-value piece that had remained conditional.

## References

- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, J. Math. Soc. Japan **30** (1978), 139--167.
- G. S. Kopp, *Indefinite zeta functions*, Res. Math. Sci. **8**
  (2021), article 17.
- G. S. Kopp, *The Shintani--Faddeev modular cocycle*,
  arXiv:2411.06763.
- P. Voutier, *An effective lower bound for the height of algebraic
  numbers*, Acta Arith. **74** (1996), 81--95.
