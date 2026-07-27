# SIC--Stark research cycle 25: the dimension-six stratification gate

Date: 2026-07-27

## Outcome

Dimension six now has an unconditional lower-stratum evaluation and an
exact 225-minor theorem conditional only on the primitive order-six packet.
It is not yet a fully unconditional sequel to dimensions four and five.  It
exposes two new structures:

1. composite level splits the overlap table into primitive and
   lower-conductor strata; and
2. the one-infinite-place ray field has cyclic group \(C_6\), whose Kopp
   difference contains both quadratic and genuinely order-six characters.

Numerically,

\[
 \max |\text{two-minor}|<9.8\cdot10^{-11},
 \qquad
 \max |K^2-K|<2.5\cdot10^{-10}.
\]

The finite calculation is now also exact: after certified Artin labeling,
one and only one of the eight lower-root embeddings makes all 225 minors
zero in a degree-48 coefficient compositum.  The primitive reciprocal lift
is the degree-six ray-unit polynomial over \(K\), and its absolute field is
exactly the degree-twelve ray field.  The lower-conductor unit generates the
unique quadratic component, while the three primitive traces generate the
cubic component.  Its value is proved unconditionally from Kopp's theorem
and the analytic class-number formula.

The unconditional analytic method used for \(d=5\), however, stops here.
Shintani's 1978 quadratic-over-the-maximal-absolutely-abelian-subfield
hypothesis fails, and the prime over \(3\) is wildly ramified, so Roblot's
cyclic-sextic theorem does not apply either.

Thus \(d=6\) is not a dead end.  Its sole central obstruction is now a
genuine wild cyclic-sextic Stark algebraicity problem: prove that the three
primitive double-sine values are the certified Artin-labeled algebraic
conjugates.  It is no longer a finite-matrix problem.

## 1. Canonical data

Put

\[
 K=\mathbb Q(\sqrt{21}),\qquad
 \beta=\frac{5+\sqrt{21}}2,\qquad
 Q=\langle1,-5,1\rangle,
 \qquad
 L=\begin{pmatrix}5&-1\\1&0\end{pmatrix}.
\]

Then

\[
 B=L^3=\begin{pmatrix}115&-24\\24&-5\end{pmatrix},
 \qquad B\equiv I\pmod6.
\]

PARI/GP 2.15.4 gives, with the second real place selected,

\[
\operatorname{Cl}_{(6)}(K)\cong C_3,\qquad
\operatorname{Cl}_{(6)\infty_2}(K)\cong C_6,\qquad
\operatorname{Cl}_{(6)\infty_1\infty_2}(K)\cong C_6\times C_2.
\]

The base field has discriminant \(21\), class number one, and certified
fundamental unit \(\beta\).

Let \(g\) generate the one-place group \(C_6\).  The sign class is

\[
 R=g^3.
\]

Indeed the forgetful map to the finite group \(C_3\) has a unique
order-two kernel.  Directly, \(\beta^3\equiv1\pmod6\), and every unit
congruent to \(-1\) modulo \(6\) is negative at the second real place, so
Kopp's residue/sign class is nontrivial.

## 2. Mixed character support

For

\[
 \chi_k(g)=e^{2\pi i k/6},
\]

the coefficient of the Kopp difference \(1-R\) is

\[
 1-\chi_k(R)=1-(-1)^k.
\]

Hence the support is

\[
 k=1,3,5,
\]

with respective character orders

\[
 6,\ 2,\ 6.
\]

This is neither the pure quadratic packet of \(d=4\) nor the pure
order-eight packet of \(d=5\).  The quadratic class-number method evaluates
the \(k=3\) component, but it cannot determine the \(k=1,5\) components.

## 3. The four-parameter overlap table

Numerical evaluation of the published principal three-double-sine formula
gives four positive parameters

\[
\begin{aligned}
x&=2.212885291117\ldots,\\
y&=1.539222338547\ldots,\\
z&=0.359428195362\ldots,\\
w&=0.335713131342\ldots.
\end{aligned}
\]

All thirty-six overlaps reduce numerically to

\[
T_6=
\begin{pmatrix}
\sqrt7&-x&y&-1&y^{-1}&-x^{-1}\\
-x^{-1}&-y^{-2}&-z&-w&-y^{-2}&-x\\
y^{-1}&-w&y^{-3}&-z&y&y^2\\
-1&-z&-w&-1&w^{-1}&-z^{-1}\\
y&-y^{-2}&y^{-1}&z^{-1}&y^3&w^{-1}\\
-x&-x^{-1}&y^2&-w^{-1}&z^{-1}&-y^2
\end{pmatrix}.
\]

The maximum residual in this four-parameter description is
\(1.1\cdot10^{-9}\), at ordinary double precision.

The important new feature is that \(y\) alone accounts for every singular
stratum through

\[
 y^{\pm1},\quad y^{\pm2},\quad y^{\pm3}.
\]

The remaining three reciprocal pairs are primitive modulus-six values.
Thus the apparent six-variable table is really a four-variable table.

## 4. Exact ray-field decomposition

The lower component satisfies the algebraic target

\[
 y^2+y^{-2}=\beta-2.
\]

Writing \(Y=y^2\), its relative polynomial is

\[
 Y^2-(\beta-2)Y+1,
\]

and its absolute polynomial is

\[
 Y^4-Y^3-3Y^2-Y+1.
\]

This field is exactly the unique quartic subfield of the one-place ray
field.

For a primitive value \(u\), put \(V=u^2+u^{-2}\).  The three values
associated to \(x,z,w\) are the three roots of

\[
\begin{aligned}
F(V)={}&V^3+(2-5\beta)V^2\\
&+(35\beta-11)V+(13-78\beta).
\end{aligned}
\]

This is the exact finite Stark polynomial returned by PARI.  Its absolute
field is the unique sextic subfield of the ray field.

The reciprocal lift

\[
 P(U)=U^3F(U+U^{-1})
\]

is

\[
\begin{aligned}
P(U)={}&U^6+(2-5\beta)U^5+(35\beta-8)U^4\\
&+(17-88\beta)U^3+(35\beta-8)U^2\\
&+(2-5\beta)U+1.
\end{aligned}
\]

Its absolute polynomial is

\[
\begin{aligned}
\mathcal P(U)={}&U^{12}-3U^{11}-6U^{10}+16U^9+3U^8\\
&+27U^6+3U^4+16U^3-6U^2-3U+1.
\end{aligned}
\]

Exact `nfisisom` calculations prove that this is the one-infinite-place
ray field.  They also prove that the compositum of the quartic lower
component and the sextic trace component is the same field.

This realizes the group decomposition

\[
 C_6\cong C_2\times C_3
\]

inside the actual overlap packet.

## 5. Artin order is stronger than the polynomial

The primitive squares occur in ray order as

\[
\begin{array}{c|cccccc}
\text{ray log}&0&1&2&3&4&5\\ \hline
\text{value}&x^2&z^{-2}&w^{-2}&x^{-2}&z^2&w^2.
\end{array}
\]

The order-three norm gives the compatibility relation

\[
 x^2z^2w^{-2}=y^4,
\qquad\text{equivalently}\qquad
 \frac{xz}{w}=y^2
\]

for the positive branches.

This relation still does not determine the Artin orientation.  Among all
\(3!\,2^3\) permutations and reciprocal choices for \(x,z,w\), together
with the two choices \(y\leftrightarrow y^{-1}\), only the intended packet
and its simultaneous reciprocal make the minors vanish numerically.

There is a false reversed assignment satisfying the same norm relation
whose maximum minor is approximately

\[
 6.29\cdot10^{-2}.
\]

Therefore polynomial membership, reciprocal pairing, and component norms
remain insufficient.  A Frobenius orientation or an equivalent cubic
resolvent sign is indispensable.

## 6. Unconditional lower-stratum theorem

Let

\[
 E=K\left(\sqrt{\beta-1}\right)
\]

be the quadratic component and take

\[
 Y=\frac{\beta-2+\sqrt{\beta-1}}2>1.
\]

Then \(Y+Y^{-1}=\beta-2\).  The characteristic producing the positive
overlap \(y=\nu_{(0,2)}\) is

\[
 \boldsymbol r=(0,1/3).
\]

It has exact Kopp data

\[
 \mathfrak m=(3),\quad
 \mathfrak A=I,\quad
 \mathfrak b=\mathcal O_K,\quad
 \alpha=3,\quad
 B=L^3=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}.
\]

Indeed \(3(r_2\beta-r_1)=\beta\) is a unit, so the ray class is the
identity, and

\[
 B\boldsymbol r-\boldsymbol r=(-8,-2)^{\mathsf T}.
\]

Neither \(L\) nor \(L^2\) fixes the characteristic modulo
\(\mathbb Z^2\), so \(B\) is its positive stabilizer generator.  The
full signed modulus-three group is \(C_2\times C_2\), while the
one-place group is \(C_2\).  The relevant fiber therefore has order two
and Kopp's exponent is

\[
 n=\frac2{|\varphi^{-1}(I)|}=1.
\]

The finite ray group modulo \(3\) is trivial.  The one-place ray group
has order two, and its conductor is the unique prime above \(3\), together
with \(\infty_2\).  Thus its nontrivial character is exactly the quadratic
character of \(E/K\); presenting it with the modulus
\((3)\infty_2\) introduces no extra character or Euler factor.

Kopp's sign class is nontrivial.  Every unit is
\(\pm\beta^m\), and \(\beta^3\equiv1\pmod3\).  The units congruent to
\(-1\) modulo \(3\) are \(-\beta^{3k}\), all negative at
\(\infty_2\).  Hence no unit realizes the residue/sign pair defining the
sign class.  Since the ray group has order two, that class is its
nonidentity element.  Consequently

\[
 Z_{(3)\infty_2}(s,I)
 =\zeta(s,I)-\zeta(s,R)=L(s,\chi_E).
\]

The convention-sensitive multiplier is also exact.  For \(B\),

\[
 s(115,24)=-\frac{53}{144},\qquad \Psi(B)=6,
\]

and substitution of \(\boldsymbol r=(0,1/3)\) in Kopp's theta
character gives exponent

\[
 \frac{383}{3}\equiv\frac23\pmod1.
\]

Therefore

\[
 \psi^2(B)=-1,\qquad
 \chi_{\boldsymbol r}(B)=e^{4\pi i/3},
\qquad
 (\psi^{-2}\chi_{\boldsymbol r}^{-1})(B)
 =-e^{2\pi i/3}.
\]

AFK's phase at \((0,2)\) is \(e^{-\pi i/6}\), whose square is the same
multiplier.  With

\[
 S_2^{\mathrm{here}}(z\mid\omega_1,\omega_2)
 =\frac{\Gamma_2(z\mid\omega_1,\omega_2)}
 {\Gamma_2(\omega_1+\omega_2-z\mid\omega_1,\omega_2)}
 =\operatorname{Sin}_{2,\mathrm{Kopp}}(z;\omega_1,\omega_2)^{-1},
\]

AFK's principal three-factor formula gives

\[
\begin{aligned}
y
&=S_2^{\mathrm{here}}(1+\beta/3\mid\beta,1)
  S_2^{\mathrm{here}}(1/3\mid\beta,1)
  S_2^{\mathrm{here}}(2(\beta+1)/3\mid\beta,1)\\
&=\sqrt3\,
 \frac{
 S_2^{\mathrm{here}}(\beta/3\mid\beta,1)
 S_2^{\mathrm{here}}(1/3\mid\beta,1)}
 {S_2^{\mathrm{here}}((\beta+1)/3\mid\beta,1)}.
\end{aligned}
\]

Here the first equality includes the AFK sign, which is \(+1\), and the
second uses quasiperiodicity and reflection in the stated reciprocal
convention.

Exact PARI certification gives

\[
 D_E=-1323,\qquad h_E=1,\qquad
 R_E=\log\beta\,\log Y.
\]

More explicitly, \(\mathcal O_E=\mathbb Z[Y]\), and PARI's certified
fundamental units are \(Y\) and \(Y+1\).  Since

\[
 \beta=\frac{(Y+1)^2}{Y},
\]

their logarithmic determinant gives
\(R_E=\log\beta\,\log Y\).  The analytic class-number formula at zero is

\[
 \zeta_F(s)=-\frac{h_FR_F}{w_F}
 s^{r_1(F)+r_2(F)-1}
 +O\!\left(s^{r_1(F)+r_2(F)}\right).
\]

Since \(h_K=h_E=1\), \(w_K=w_E=2\), and the signatures are
\((2,0)\) and \((2,1)\), respectively,

\[
 \frac{\zeta_E(s)}{\zeta_K(s)}
 =\frac{R_E}{R_K}s+O(s^2)
 =\log Y\,s+O(s^2).
\]

Consequently

\[
 L'(0,\chi_2)=\log Y
\]

for the nontrivial quadratic character of \(E/K\).  Kopp's theorem and
the AFK phase relation now prove, without a Stark conjecture,

\[
 y^2=Y
\]

exactly.  This closes the lower-conductor part, but not the primitive
order-six packet.

There is also a direct historical verification.  Shintani's published
\(\mathbb Q(\sqrt{21})\), modulus-three example evaluates

\[
\begin{aligned}
 &\operatorname{Sin}_{2,\mathrm{Kopp}}
   (1/3;\beta,1)\,
  \operatorname{Sin}_{2,\mathrm{Kopp}}
   (1+\beta/3;\beta,1)\\
 &\qquad{}\times
  \operatorname{Sin}_{2,\mathrm{Kopp}}
   (2(\beta+1)/3;\beta,1)
 =
 \left[
 \frac{
 (1+\sqrt{21})/2-\sqrt{(3+\sqrt{21})/2}
 }2
 \right]^{1/2}.
\end{aligned}
\]

The right-hand side is \(Y^{-1/2}=y^{-1}\).  Since the convention used
here is reciprocal to Shintani's/Kopp's double sine, the published formula
gives \(y=\sqrt Y\) immediately.  This independently confirms both the
double-sine convention and the class-number calculation above.

## 7. Exact finite rank theorem

The primitive overlaps themselves, with their AFK signs included, have
the degree-twelve polynomial

\[
\begin{aligned}
\mathcal Q(X)={}&X^{12}+3X^{11}-6X^{10}-16X^9+3X^8+27X^6\\
&+3X^4-16X^3-6X^2+3X+1.
\end{aligned}
\]

Let \(x\) be its root in

\[
 2.21288528901718<x<2.21288528901719.
\]

Exact `nfgaloisconj` substitution, with rational interval evaluation
fixing the labels, gives

\[
\begin{array}{c|cccccc}
\text{conjugate index}&1&2&3&4&5&6\\ \hline
\text{signed value}&x&-w^{-1}&-w&x^{-1}&-z^{-1}&-z.
\end{array}
\]

This explains why adjoining independent square roots was unnecessary:
the convention-correct AFK signs are already encoded in one degree-twelve
field.

Put

\[
 F=\mathbb Q(\zeta_{12},\sqrt7).
\]

The polynomial \(\mathcal Q\) has two degree-six factors over \(F\).
The canonical factor is selected exactly by requiring its \(X^5\)
coefficient to be

\[
 \beta-1=\frac{3+\sqrt{21}}2,
\qquad
 \sqrt{21}=(\zeta_{12}+\zeta_{12}^{-1})\sqrt7.
\]

The compositum of this factor with \(F\) has absolute degree \(48\).
Inside it the lower-overlap polynomial

\[
 h(V)=V^8-V^6-3V^4-V^2+1
\]

splits completely.  Under the canonical embedding

\[
 \zeta_{12}=e^{\pi i/6},\qquad \sqrt7>0,\qquad x>0,
\]

its compatible root is

\[
 y=1.539222338420433\ldots>0.
\]

Substituting each of the eight exact roots of \(h\) into the structured
table and reconstructing the Weyl matrix gives the following numbers of
nonzero \(2\)-minors:

\[
 201,\ 224,\ 225,\ 225,\ 225,\ 225,\ 225,\ \boxed{0}.
\]

Thus the canonical root is not selected by a floating-point tolerance:
it is the unique root for which every one of the
\(\binom62^2=225\) exact number-field remainders is zero.

Let

\[
 K_{r,c}=\frac1{6\sqrt7}
 \sum_{\substack{0\le a,b<6\\r\equiv c+a\pmod6}}
 T_{a,b}\tau_6^{ab}\omega_6^{bc}.
\]

The preceding reduction proves all \(2\)-minors of \(K\) vanish.
Moreover the diagonal Fourier sum gives

\[
 \operatorname{Tr}K=\frac{T_{0,0}}{\sqrt7}=1.
\]

Hence \(K\) has rank exactly one and

\[
 K^2=(\operatorname{Tr}K)K=K.
\]

This finite theorem is unconditional as algebra.  Its remaining analytic
hypothesis is now sharply isolated: the three primitive modulus-six
double-sine values must equal the displayed Artin-labeled roots.  The
lower value \(y\) is no longer part of that hypothesis, by Section 6.

## 8. Why the dimension-five algebraicity proof does not transfer

The degree-twelve ray field has signature \((6,3)\).  Exact enumeration of
all its subfields shows:

- its only absolutely abelian nontrivial subfield is \(K\);
- its quartic subfield has nonabelian normal closure \(D_4\);
- its cubic subfields have normal closure \(S_3\); and
- its sextic trace field is nonabelian over \(\mathbb Q\).

Thus the maximal absolutely abelian subfield is \(K\), and the ray field
has degree six, not two, over it.  Shintani's 1978 condition (0-9) fails.

Roblot's cyclic-sextic result is also unavailable.  Although the ray field
has certified class number one, the cubic component has ramification index
three above \(3\).  The prime above \(3\) is therefore wildly ramified,
contrary to an explicit hypothesis of Roblot's theorem.  Moreover that
theorem gives only a weak equality up to Fourier absolute values, which
would not by itself determine the Artin orientation needed by the minors.

## 9. Research questions

The calculation leaves three precise questions.

1. **Orientation relation.** Which explicit Frobenius or cubic-resolvent
   invariant distinguishes
   \((x,z,w)\) from the false norm-compatible reversal?
2. **Compression.** Can the 225-minor field reduction be replaced by a
   small human-readable ideal or a few fan minors?
3. **Analytic theorem.** Is there an algebraicity theorem covering this
   wildly ramified cyclic-sextic Stark packet, or should the general
   program move to the next dimension satisfying Shintani's condition
   (0-9)?

## 10. Higher-dimensional screen

A maximal-order proxy for \(4\le d\le20\) gives a useful complexity
warning.  For the next maximal canonical orders the one-place ray groups
already have orders

\[
\begin{array}{c|c|c|c}
d&D&\operatorname{Cl}_{(d)\infty_2}(K)&|\,\cdot\,|\\ \hline
9&60&C_{12}\times C_3&36\\
10&77&C_{24}&24\\
13&140&C_{24}\times C_4&96\\
14&165&C_{12}\times C_6&72\\
16&221&C_{16}\times C_4\times C_2&128
\end{array}
\]

Their absolute ray-field degree proxies are twice these orders.  Thus
the next maximal-order dimensions are substantially larger than \(d=6\);
moving monotonically in \(d\) does not evade the analytic obstruction.

The interesting exceptions are nonmaximal canonical orders:

\[
\begin{array}{c|c|c|c}
d&D&f_{\mathcal O}^2&
\text{maximal-order one-place proxy}\\ \hline
7&32&4&C_6\\
8&45&9&C_2\times C_2\\
12&117&9&C_2^3
\end{array}
\]

The exponent-two proxies at \(d=8\) and \(d=12\) are potentially
attractive because every character would be quadratic.  They are not yet
the canonical AFK ray groups, however: `bnrinit` computes the maximal
order, whereas these tuples use orders of conductors \(3\).  An
order-aware ray-class-monoid calculation is required before claiming a
free quadratic generalization.

## Recommendation

The two recommended dimension-six deliverables are now complete:

1. \(y^2=Y\) is unconditional, with the full Kopp/AFK normalization
   audited; and
2. all 225 minors vanish exactly, conditional only on the three
   Artin-labeled primitive modulus-six values.

Do not yet draft a dimension-six paper.  The central next task is the
primitive analytic bridge.  It should be attacked in two ways:

1. search for a wild-prime correction or direct double-sine distribution
   argument that covers the order-six character pair; and
2. compute the correct nonmaximal-order ray monoid for \(d=8\), testing
   whether its promising exponent-two maximal-order proxy survives.

The first route could complete dimension six.  The second is the best
chance of obtaining another unconditional dimension without first
solving the wild cyclic-sextic Stark problem.

## Reproducibility

- `scripts/explore_dimension_six.py`
- `scripts/dimension_six_ray_recon.gp`
- `scripts/dimension_six_field_recon.gp`
- `scripts/dimension_six_roblot_recon.gp`
- `scripts/analyze_dimension_six_character.py`
- `scripts/dimension_six_lower_stratum.gp`
- `scripts/dimension_six_embedding_certificate.gp`
- `scripts/verify_dimension_six_conjugates.gp`
- `scripts/screen_higher_dimensions.gp`

## Primary sources

- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, J. Math. Soc. Japan 30 (1978), 139--167.
- T. Shintani, *On a Kronecker limit formula for real quadratic fields*,
  J. Fac. Sci. Univ. Tokyo Sect. IA Math. 24 (1977), 167--199.
- H. Tanaka, *Special values of multiple sine functions*, Kyushu J.
  Math. 62 (2008), 123--137.
- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422; arXiv:1112.2820.
- G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, arXiv:2411.06763.
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, arXiv:2501.03970.
