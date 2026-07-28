# Dimension-five result

## Summary

Dimension five does not repeat the one-variable factorization seen in
dimension four. It produces a larger but highly structured ray-class packet.
The packet is nevertheless now proved unconditionally.  The result combines:

- Kopp's proved Kronecker-limit formula for the four positive cocycle values;
- Shintani's 1978 algebraicity theorem with the explicit safe power \(5760\);
- exact \(K\)-compatible ray-field and Frobenius labeling;
- rigorous Arb integration and Voutier height rigidity; and
- exact vanishing of all one hundred \(2\)-minors of the reconstructed
  dimension-five ghost matrix.

Consequently, both formal shifts \(0\) and \(1\) hold for every
dimension-five admissible tuple.  This proves the complete
dimension-five Twisted Convolution Conjecture.  It does not prove a
dimension-five SIC or the conjecture in arbitrary dimensions.

Set

\[
K=\mathbb Q(\sqrt3),\qquad
\beta=2+\sqrt3,\qquad
Q=\langle1,-4,1\rangle,\qquad
L=\begin{pmatrix}4&-1\\1&0\end{pmatrix}.
\]

Then

\[
B=L^3=\begin{pmatrix}56&-15\\15&-4\end{pmatrix},\qquad
B\binom0{1/5}-\binom0{1/5}=\binom{-3}{-1}.
\]

Thus the natural Kopp data are modulus \(5\mathcal O_K\), identity ray
class, characteristic \((0,1/5)^T\), and positive stabilizer \(B\).

## The overlap packet

For nonzero characteristics, the principal three-double-sine formula,
the certified ray log, and its explicit sign give

\[
T_5=
\begin{pmatrix}
\sqrt6&x&y&y^{-1}&x^{-1}\\
x^{-1}&-z^{-1}&w^{-1}&-z^{-1}&x\\
y^{-1}&w^{-1}&w^{-1}&y&-z\\
y&-z^{-1}&y^{-1}&w&w\\
x&x^{-1}&-z&w&-z
\end{pmatrix}.
\]

The entry \(T_{0,0}=\sqrt6\) is an artificial reconstruction entry:
after division by \(\sqrt6\), it makes the identity Weyl coefficient
equal to one. It is not AFK's auxiliary zero-characteristic cocycle
value.

Numerically,

\[
\begin{aligned}
x&=1.972526734280932, &
y&=1.278133760244910,\\
z&=2.076946027188073, &
w&=2.353849830511481.
\end{aligned}
\]

The Weyl reconstruction of this table has trace one and is numerically
idempotent to approximately \(10^{-10}\). All one hundred two-by-two minors
vanish to the same accuracy.

The exact formal calculation is substantially larger than in dimension
four. Before imposing special-value relations:

- all 100 minors are nonzero Laurent polynomials;
- they involve 41 Laurent monomials in \(x,y,z,w\);
- their linear span over \(\mathbb Q(\zeta_5,\sqrt6)\) has dimension 24.

Consequently there is no dimension-five analogue in which the calculation
visibly collapses to one quadratic relation in one double-sine value.

## Ray-class explanation of the four variables

PARI/GP gives

\[
\operatorname{Cl}_{(5)}(K)\cong C_4,\qquad
\operatorname{Cl}_{(5)\infty_2}(K)\cong C_8,\qquad
\operatorname{Cl}_{(5)\infty_1\infty_2}(K)\cong C_8\times C_2.
\]

The order-two sign class is the fourth power in \(C_8\). For each
\((p,q)\), choose the Kopp-positive lift by replacing \(p\) with the
congruent integer \(\widetilde p\) satisfying
\(q(2-\sqrt3)-\widetilde p>0\). Exact `bnrisprincipal` calculations give
the complete ray-class log table in PARI's raw cyclic basis \(g\):

\[
\begin{array}{c|ccccc}
p\backslash q&0&1&2&3&4\\ \hline
0&-&0&6&2&4\\
1&4&3&1&3&0\\
2&2&1&1&6&7\\
3&6&3&2&5&5\\
4&0&4&7&5&7.
\end{array}
\]

The prime \(\mathfrak q\) above \(3\) satisfies
\(\mathfrak q=g^5\).  The bridge and Frobenius certificates normalize
to \(\mathfrak q\) itself; multiplication by \(5\) converts the table
to that basis.  Thus the four positive characteristics have normalized
coordinates \(0,6,3,1\).

In particular:

| pair | ray classes |
|---|---|
| \(x,x^{-1}\) | \(0,4\) |
| \(w^{-1},w\) | \(1,5\) |
| \(y^{-1},y\) | \(2,6\) |
| \(z^{-1},z\) | \(3,7\) |

Thus reciprocal values differ by the sign class, and the four independent
positive values represent the four cosets of \(C_8/\langle R\rangle\).
This is exactly the structure hidden by the single reciprocal pair in
dimension four.

### The quadratic shortcut is impossible

This conclusion can be sharpened at the character level. Write
\(\operatorname{Cl}_{(5)\infty_2}(K)=\langle g\rangle=C_8\) and
\(R=g^4\). For \(\chi_k(g)=e^{2\pi i k/8}\), the Kopp difference
\[
\zeta(s,A)-\zeta(s,RA)
\]
has Fourier coefficient proportional to
\[
1-\chi_k(R)=1-(-1)^k.
\]
It is therefore supported precisely on \(k=1,3,5,7\), all four of which
have order eight. The unique quadratic character is \(k=4\), and its
coefficient is zero. Thus the needed invariant does not factor through the
quadratic subfield; it annihilates the quadratic character. The
dimension-four analytic class-number shortcut cannot recur in dimension
five.

## Stark polynomial

Let \(u\) denote the square of a positive double-sine value. The four values
\(x^2,y^2,z^2,w^2\), together with their inverses, numerically satisfy

\[
\begin{aligned}
P(U)={}&U^8-(8+5\sqrt3)U^7+(53+30\sqrt3)U^6\\
&-(156+90\sqrt3)U^5+(225+130\sqrt3)U^4\\
&-(156+90\sqrt3)U^3+(53+30\sqrt3)U^2\\
&-(8+5\sqrt3)U+1.
\end{aligned}
\]

This exact polynomial was previously published as the conjectural Stark-unit
polynomial for this example: Kopp gives it in *Indefinite zeta functions*,
§7, equation (7.21), and again in *A Kronecker limit formula for indefinite
zeta functions*, Example 1.17, equation (3.12). Writing
\(V=U+U^{-1}\), it is the exact quadratic lift

\[
P(U)=U^4F(U+U^{-1})
\]

of

\[
\begin{aligned}
F(V)={}&V^4-(8+5\sqrt3)V^3+(49+30\sqrt3)V^2\\
&-(132+75\sqrt3)V+(121+70\sqrt3),
\end{aligned}
\]

and \(F\) is reproduced by PARI's `bnrstark` calculation.  The proof does
not treat that recognition as evidence of algebraicity.  Instead,
Shintani's theorem makes the \(5760\)-th powers algebraic units, and the
certified height argument identifies the analytic values with these roots.
The Artin ordering is

\[
x^2+x^{-2},\quad w^2+w^{-2},\quad
y^2+y^{-2},\quad z^2+z^{-2},
\]

in ray-class order modulo the sign class.

The relative field defined by
\(P\) and the class field produced independently by `bnrclassfield` both
have degree eight over \(K\). After conversion to absolute
degree-sixteen polynomials, PARI's `nfisisom` finds eight isomorphisms;
exact substitution proves that all eight fix the labeled copy of \(K\).
Reduction modulo the prime above \(3\), followed by rational interval
propagation through the exact Frobenius polynomials, certifies all eight
Artin labels.

## Exact finite rank certificate

Let

\[
\begin{aligned}
\mathcal Q(X)={}&X^{32}-16X^{30}+95X^{28}-260X^{26}+355X^{24}
-348X^{22}\\
&+388X^{20}-300X^{18}+195X^{16}-300X^{14}
+388X^{12}\\
&-348X^{10}+355X^8-260X^6+95X^4-16X^2+1.
\end{aligned}
\]

This is the absolute norm of \(P(X^2)\). Its root field has sixteen
automorphisms over \(K\). Exact root isolation, rational interval
evaluation of every `nfgaloisconj` polynomial, and exact subfield-sign
tests label the positive conjugates as

\[
w=\sigma_2(\alpha),\quad y=\sigma_5(\alpha),\quad
x=\sigma_{10}(\alpha),\quad z=\sigma_{16}(\alpha),
\]

with the reciprocal values supplied by
\(\sigma_8,\sigma_4,\sigma_6,\sigma_{12}\), respectively.

Over the Weyl coefficient field
\(\mathbb Q(\zeta_5,\sqrt6)\), \(\mathcal Q\) has four degree-eight
factors. The embedding with positive \(\sqrt5\) and positive \(\sqrt6\)
selects the fourth factor uniquely. Substituting the
eight labeled conjugates into the exact overlap table and reconstructing the
Weyl matrix gives:

\[
\boxed{\text{all 100 two-by-two minors vanish exactly}.}
\]

For comparison, the other three factors leave \(70,100,100\) nonzero
minors. Thus the vanishing is sensitive to the precise embedding and
Artin labeling; it is not a consequence of the polynomial alone.

## Kopp multiplier

For \(\boldsymbol r=(0,1/5)^T\), Kopp's defining theta-character formula
gives

\[
\chi_{\boldsymbol r}(B)=e^{2\pi i/5}.
\]

The Dedekind sum is \(s(-4,15)=-19/90\), so the Rademacher invariant is
three and

\[
\psi^2(B)=i.
\]

Therefore

\[
(\psi^{-2}\chi_{\boldsymbol r}^{-1})(B)
=-i\,e^{-2\pi i/5},
\]

which agrees with the square of the AFK phase at \((0,1)\). As in dimension
four, the full-ray fiber has order two, so Kopp's exponent is \(n=1\).

The comparison has also been carried out for all 24 nonzero
characteristics. If \(Q(p,q)=p^2-4pq+q^2\), substitution of every positive
lift into Kopp's theta-character formula gives

\[
\arg\chi_{\boldsymbol r}(B)=\frac{Q(p,q)}5\pmod1.
\]

Since \(\psi^{-2}(B)=-i\), the Kopp multiplier has exponent

\[
-\frac14-\frac{Q(p,q)}5\pmod1,
\]

which is exactly the exponent of the square of the AFK phase. The complete
JSON certificate records the lift, ray class, three double-sine arguments,
cocycle sign, and both multiplier exponents for every characteristic.

## Certified real-root selection

Sturm calculations isolate the eight positive roots of \(\mathcal Q\) in

\[
\begin{gathered}
(0.424835,0.424836),\ (0.481476,0.481477),\
(0.506963,0.506964),\ (0.782390,0.782391),\\
(1.278133,1.278134),\ (1.972526,1.972527),\
(2.076946,2.076947),\ (2.353849,2.353850).
\end{gathered}
\]

Every interval contains exactly one root, and the corresponding negative
intervals contain the other eight real roots. A narrower rational interval
for \(w\), propagated through the rational `nfgaloisconj` polynomials,
certifies that all eight conjugate indices land in the displayed intervals.
Exact `nfisincl` identities then prove that factor four is the unique
factor with the two required positive subfield embeddings.

## Unconditional closure

Let \(H\) be the ray field of modulus \((5)\infty_2\).  Its unique
octic subfield is \(\mathbb Q(\zeta_{60})^+\), and \(H\) is quadratic
over that maximal absolutely abelian subfield.  Exactly one real place
of \(K\) splits.  These facts put the example inside Shintani's proved
1978 theorem.

In the full narrow ray group, take
\[
\mu=[11-5\beta],\qquad \nu=[4],\qquad G=\langle\mu\rangle .
\]
Exact ray arithmetic gives
\[
\mu\mapsto0,\qquad \nu\mapsto4
\]
after forgetting \(\infty_1\).  The unit calculation proves Shintani's
conditions (0-3) and (0-6), and summing the two full-narrow fibers gives
exactly Kopp's one-place difference \(Z'_{(5)\infty_2}(0,A)\).

Shintani's imaginary-quadratic reduction uses
\(\mathbb Q(\sqrt{-5})\) with conductor
\[
\begin{pmatrix}15&0\\0&3\end{pmatrix}.
\]
This field is not selected from a subfield list: conjugation acts on
the \(C_8\times C_2\) ray generators by \((5,0)\) and \((4,1)\), and
the class field of its fixed subgroup
\(\{(a,b):a+b\equiv0\pmod2\}\) is exactly
\(\mathbb Q(\sqrt3,\sqrt{-5})\).
Clearing every absolute-value and distribution denominator over its
eight divisors gives
\[
384,\ 288,\ 288,\ 144,\ 240,\ 360,\ 360,\ 180,
\]
with least common multiple \(5760\).  Hence every required analytic
value raised to the \(5760\)-th power is a correctly Artin-labeled unit.

Rigorous double-sine integration gives maximum logarithmic error
\[
4.4\times10^{-11}.
\]
After raising to the Shintani power and accounting for eight real and
four complex pairs in degree sixteen, the height of the quotient of
the analytic and algebraic candidates is less than
\[
1.27\times10^{-7}.
\]
Voutier's lower bound for a non-torsion algebraic number of degree at
most \(16\) is at least
\[
5.22795\times10^{-5}.
\]
The quotient is therefore a root of unity; positivity makes it \(1\).
This proves the entire Artin-labeled packet.  Combining it with the exact
minor certificate proves the complete dimension-five TCC.

## Reproducible artifacts

- `scripts/analyze_dimension_five_finite.py`
- `certificates/dimension-five-finite.json`
- `scripts/explore_dimension_five.py`
- `certificates/dimension-five-numerical.txt`
- `scripts/dimension_five_pari_audit.gp`
- `certificates/dimension-five-pari.txt`
- `scripts/verify_dimension_five_conjugates.gp`
- `certificates/dimension-five-exact-minors.txt`
- `scripts/generate_dimension_five_bridge.py`
- `certificates/dimension-five-bridge.json`
- `scripts/dimension_five_root_isolation.gp`
- `certificates/dimension-five-root-isolation.txt`
- `scripts/dimension_five_embedding_certificate.gp`
- `certificates/dimension-five-embedding-certificate.txt`
- `scripts/dimension_five_local_isolation.gp`
- `certificates/dimension-five-local-isolation.txt`
- `docs/sic-stark-dimension-five-unconditional-audit.md`
- `docs/sic-stark-dimension-five-unconditional-closure.md`
- `scripts/analyze_dimension_five_character.py`
- `certificates/dimension-five-character-support.json`
- `scripts/dimension_five_shintani_audit.gp`
- `certificates/dimension-five-shintani.txt`
- `scripts/dimension_five_unit_lattice_audit.gp`
- `certificates/dimension-five-unit-lattice.txt`
- `scripts/certify_dimension_five_double_sine.py`
- `certificates/dimension-five-double-sine-intervals.txt`
- `paper/sic-stark-dimensions-four-five.tex`
- `paper/sic-stark-dimensions-four-five.pdf`
