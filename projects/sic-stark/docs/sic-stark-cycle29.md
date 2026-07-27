# SIC--Stark research cycle 29: no all-quadratic higher canonical packet

Date: 2026-07-27

## Outcome

The dimension-eight backup route has been audited at the level of the
actual AFK characteristic packet.  It does not avoid the quartic
characters of the nonmaximal-order ray group:

\[
 \operatorname{Cl}_{(8)\infty_2}(\mathcal O_3)
 \cong C_4\times C_2\times C_2.
\]

More strongly, the \(48\) full-denominator characteristics form sixteen
Zauner orbits, and those orbits map bijectively to all sixteen ray
classes.  Hence the complete primitive table uses the entire ray group.

This calculation led to a family-level result:

\[
\boxed{
\text{For every canonical dimension }d\ge5,\text{ the principal Kopp
packet contains a nonquadratic character.}
}
\]

Dimension four is the unique canonical dimension whose full principal
packet can be entirely quadratic.  Therefore searching higher canonical
dimensions for another “free” quadratic proof cannot succeed.

## 1. The decisive dimension-eight characteristic

Let

\[
 \mathcal O_3=\mathbb Z[\theta],
 \qquad
 \theta^2=3\theta+9,
 \qquad
 \beta=\theta+2.
\]

For the AFK characteristic

\[
 q=(0,1),\qquad r=(0,1/8),
\]

Kopp's real-multiplication parameter is

\[
 w=r_2\beta-r_1=\frac{\beta}{8}.
\]

Since \(\beta\) is a unit of \(\mathcal O_3\), the denominator ideal of
\(w\) is exactly

\[
 (8)\subset\mathcal O_3.
\]

Moreover \(8w=\beta\) is a unit, so the associated ray class is the
identity class.  The canonical stabilizer is

\[
 B=L_8^3
 =
 \begin{pmatrix}
 329&-48\\
 48&-7
 \end{pmatrix},
\]

and

\[
 B\binom0{1/8}-\binom0{1/8}
 =
 \binom{-6}{-1}.
\]

Neither \(L_8\) nor \(L_8^2\) fixes the characteristic modulo
\(\mathbb Z^2\).  Thus this is a genuine primitive length-three orbit.

Write the ray group as

\[
 G=C_4\times C_2\times\langle R\rangle,
\]

where \(R\) is Kopp's nontrivial sign class.  A character is labeled
\(\chi_{a,b,c}\), with \(a\bmod4\), \(b,c\bmod2\), and

\[
 \chi_{a,b,c}(R)=(-1)^c.
\]

The identity-class difference \(1-R\) has support \(c=1\).  Its eight
characters have orders

\[
 \underbrace{2,2,2,2}_{a\text{ even}},
 \qquad
 \underbrace{4,4,4,4}_{a\text{ odd}}.
\]

All coefficients are nonzero.  Therefore the single overlap at
\(q=(0,1)\) already contains the four quartic character components.

These components form only two complex-conjugate pairs:

\[
\{\chi_{1,0,1},\chi_{3,0,1}\},
\qquad
\{\chi_{1,1,1},\chi_{3,1,1}\}.
\]

Both pairs have the same square,

\[
 \chi_{1,b,1}^2=\chi_{2,0,0}.
\]

Thus the nonquadratic analytic problem consists of two cyclic-quartic
quotients sharing a quadratic subfield, rather than four unrelated
extensions.

## 2. The complete primitive characteristic table

For \(q=(a,b)\), one has

\[
 8(r_2\beta-r_1)
 =b\beta-a
 =(2b-a)+b\theta.
\]

Its norm is

\[
 N(b\beta-a)=a^2-7ab+b^2.
\]

It is coprime to \(8\) exactly when this norm is odd.  Exactly \(48\) of
the \(64\) characteristics satisfy that condition.

The Zauner action is

\[
 (a,b)\longmapsto(7a-b,a)\pmod8.
\]

Exact enumeration proves:

- every primitive characteristic has orbit length three;
- there are \(48/3=16\) primitive orbits;
- the ray class is constant on each orbit;
- all sixteen ray classes occur; and
- every ray class occurs on exactly three characteristics.

Thus

\[
\boxed{
\{\text{primitive Zauner orbits}\}
\;\longleftrightarrow\;
\operatorname{Cl}_{(8)\infty_2}(\mathcal O_3)
}
\]

is a bijection.  There is no smaller AFK primitive subpacket in which the
quartic characters disappear.

## 3. A family theorem for canonical orders

For the canonical dimension \(d\), put

\[
 \mathcal O_d=\mathbb Z[\beta_d],
 \qquad
 \beta_d^2-(d-1)\beta_d+1=0.
\]

For every \(d\ge5\),

\[
 \mathcal O_d^\times=\langle-1,\beta_d\rangle.
\]

Here is a short proof.  If a unit \(u=a+b\beta_d\) satisfies
\(1<u<\beta_d\), then

\[
 u-u' =b\sqrt{(d+1)(d-3)}
\]

If \(N(u)=1\), monotonicity of \(v-v^{-1}\) gives
\[
 |b|\sqrt D=|u-u^{-1}|<\beta_d-\beta_d^{-1}=\sqrt D.
\]
Thus there is no smaller norm-\(+1\) unit with \(b\ne0\); equality at
the endpoint gives \(\beta_d\).  If
\(N(u)=-1\), monotonicity of \(v+v^{-1}\) gives
\[
 |b|\sqrt D=u+u^{-1}
 <\beta_d+\beta_d^{-1}=d-1,
\]
which forces \(|b|=1\).  A smaller norm-\(-1\) unit would require

\[
 t^2=(d-1)^2-8.
\]

Factoring

\[
 (d-1-t)(d-1+t)=8
\]

shows that the only solution in the canonical range is \(d=4\).  Thus
\(\beta_d\) is the fundamental positive unit for \(d\ge5\).

Modulo \(d\), its defining equation becomes

\[
 \beta_d^2+\beta_d+1=0,
\]

so \(\beta_d\) has exact order three.  The local kernel of the
one-place order-ray group over the order class group is therefore

\[
 G_d^{\mathrm{loc}}
 =
 \frac{
   (\mathcal O_d/d\mathcal O_d)^\times
   \times\{\text{sign at }\infty_2\}
 }{
   \operatorname{im}\mathcal O_d^\times
 }.
\]

The scalar subgroup \((\mathbb Z/d\mathbb Z)^\times\) embeds in
\(G_d^{\mathrm{loc}}\) without changing element orders: a scalar cannot
equal either \(\beta_d\) or \(\beta_d^2\) modulo \(d\).

The exponent of \((\mathbb Z/d\mathbb Z)^\times\) is at most two exactly
for

\[
 d\in\{1,2,3,4,6,8,12,24\}.
\]

Consequently a scalar element already gives an element of order greater
than two for every \(d\ge5\) except

\[
 d=6,8,12,24.
\]

For these four cases, explicit residue/sign witnesses in the basis
\((1,\beta_d)\) are

\[
\begin{array}{c|c|c}
d&\text{witness}&\text{order in }G_d^{\mathrm{loc}}\\ \hline
6&((1,3),\text{negative})&6\\
8&((1,2),\text{positive})&4\\
12&((1,3),\text{positive})&6\\
24&((1,3),\text{positive})&12.
\end{array}
\]

Hence

\[
 \exp G_d^{\mathrm{loc}}>2
 \qquad(d\ge5).
\]

Kopp's sign class is nontrivial: units congruent to \(-1\pmod d\) are
\(-\beta_d^{3k}\), and all are negative at the labeled second real
embedding.  Since finite characters separate points, the Fourier support
of \(1-R\) contains a character of order greater than two whenever the
ray group has exponent greater than two.  This proves the claimed family
obstruction.

## 4. Additional nonmaximal-order boundary

Dimension eight has another difficulty beyond its quartic characters.
Kopp's unconditional limit formula applies to ray class partial zeta
functions of arbitrary orders.  However, his algebraicity theorem with
power \(n=1\) is stated in the fundamental-discriminant case.  Removing
that hypothesis is Conjecture 1.4 in the cited paper.

Kopp explicitly identifies two obstructions in the nonmaximal case:

1. discrepancies between Galois-theoretic and ray-class-theoretic Euler
   factors; and
2. failure of some real-multiplication pairs to arise from primitive
   classes under the order-ray correspondence.

The present calculation removes the second concern for the primitive
dimension-eight table: its sixteen orbits do arise and exhaust the ray
classes.  It does not remove the Euler-factor/algebraicity problem.

Therefore dimension eight would require both:

- quartic Stark-value control; and
- an explicit nonmaximal-order Euler-factor comparison.

It is not simpler than the single remaining maximal-order identity in
dimension six.

## Recommendation

Do not continue searching the canonical family for an all-quadratic
higher dimension; the family theorem rules that out.

The best research strategy is now:

1. retain dimension six as the primary analytic target, because it is
   maximal-order and has only one unresolved complex character identity;
2. retain dimension eight as the first nonmaximal-order/quartic test
   case; and
3. generalize the proof architecture by character type—quadratic,
   quartic, then order six—rather than by increasing dimension.

The quartic decomposition is now isolated into two conjugate pairs.
Roblot's Theorem 6.1 applies to cyclic quartic extensions satisfying its
signature and ramification hypotheses and produces a unit whose
logarithmic character resolvents equal the corresponding \(L'\)-values;
it is unique up to conjugation and inversion.  The next actionable
dimension-eight step is therefore to construct these two quotient fields
inside the maximal-order ray field and verify hypotheses (A1)--(A3).

Even if that succeeds, one must still compare their Galois-theoretic
\(L\)-functions with Kopp's nonmaximal-order ray-class \(L\)-functions.
Kopp explicitly flags this Euler-factor discrepancy in Conjecture 1.4.
That comparison was the smallest unresolved dimension-eight bridge at
the end of this cycle.  It is resolved in
`docs/sic-stark-cycle30.md`: the order ray group is isomorphic to the
maximal-order ray group of modulus \(24\), and the quartic characters
have full conductor \(24\), so the prime-three Euler factor is trivial.
Cycle 30 also verifies Roblot's unit-index hypotheses exactly.  Its
remaining obstruction is the oriented complex phase, since Roblot's
quartic theorem proves equality only up to absolute values.

## Reproducibility

- `scripts/analyze_dimension_eight_order_ray.py`
- `scripts/generate_dimension_eight_ray_table.py`
- `scripts/analyze_canonical_order_character_obstruction.py`

## Primary sources

- G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, arXiv:2411.06763, especially Sections 3.1--3.4
  and Theorem 1.3/Conjecture 1.4.
- G. Kopp and J. C. Lagarias, *Ray class groups and ray class fields for
  orders of number fields*, Essential Number Theory 4 (2025), 1--65.
- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422; arXiv:1112.2820.
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, arXiv:2501.03970.
