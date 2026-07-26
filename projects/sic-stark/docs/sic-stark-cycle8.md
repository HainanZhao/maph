# SIC--Stark research cycle 8: the full Galois residual packet

Date: 2026-07-26

## Outcome

Cycle 8 followed the only potentially useful reformulation left by
cycle 7: instead of treating one primitive TCC coefficient as a field
trace, put all of its ray-class conjugates into a residual packet,
decompose that packet by characters, and seek a low-degree algebraic
relation forcing every character component to vanish.

The dimension-four calculation is decisive:

\[
\boxed{\text{The ray-unit quotient acts regularly on the residual
packet, so every character occurs and none is forced to vanish.}}
\]

The packet does satisfy nontrivial algebraic relations. There are no
relations of total degree at most four; the first occurs in degree five,
and a short independent relation occurs in degree six. Neither forces
zero.

More strongly, there is an explicit specialization to totally positive
algebraic units in

\[
L=\mathbb Q(\sqrt2,\sqrt3)
\]

for which:

- the four special-value parameters form one faithful
  \(C_2\times C_2\) Galois orbit;
- inverse pairing holds exactly;
- the four residuals form the corresponding regular Galois orbit;
- every character resolvent is nonzero.

This is not a counterexample to TCC: the units are not claimed to be
Shintani--Faddeev RM values. It is a logical countermodel proving that
algebraic-unit status, ray-class Galois covariance, inversion, character
orthogonality, and the first packet relations are jointly insufficient.
Any successful proof must use a property special to the actual analytic
RM values.

## 1. The dimension-four packet

Cycle 7 computed

\[
H=
(\mathcal O_4/4\mathcal O_4)^\times/
\langle\beta_4\rangle
\cong C_2\times C_2.
\]

The \(H\)-orbit of the primitive Zauner direction consists of

\[
\boldsymbol p_0=(0,3),\quad
\boldsymbol p_1=(0,1),\quad
\boldsymbol p_2=(1,1),\quad
\boldsymbol p_3=(2,3).
\]

In this ordering, the four group elements act by

\[
\begin{aligned}
&(0,1,2,3),\\
&(1,0,3,2),\\
&(2,3,0,1),\\
&(3,2,1,0).
\end{aligned}
\]

This is the regular permutation representation of \(C_2\times C_2\).
It contains all four characters, each with multiplicity one. Therefore
representation theory alone supplies no missing isotypical component
whose absence could imply TCC.

## 2. A formal Galois unit orbit

There are six Zauner orbits of characteristics in \(d=4\). Normalize the
two self-inverse orbits to \(1\), and write the remaining four values as

\[
\left(x^{-1},x,y,y^{-1}\right).
\]

Here \(x\) and \(y\) are invertible indeterminates. The four elements of
\(H\) act faithfully by

\[
\begin{aligned}
h_0(x,y)&=(x,y),\\
h_1(x,y)&=(x^{-1},y^{-1}),\\
h_2(x,y)&=(y^{-1},x^{-1}),\\
h_3(x,y)&=(y,x).
\end{aligned}
\]

This realizes the same regular permutation on
\((x^{-1},x,y,y^{-1})\). Thus the Laurent field

\[
\mathbb Q(x,y)
\]

already carries a faithful finite Galois action over its invariant
subfield. The construction incorporates inversion rather than adding it
afterward.

## 3. Exact Laurent residuals

Remove the harmless Gaussian-unit factors from the four actual TCC
residuals by defining

\[
\begin{aligned}
R_{\boldsymbol p_0}&=(1-i)A,\\
R_{\boldsymbol p_1}&=(1-i)B,\\
R_{\boldsymbol p_2}&=(1+i)C,\\
R_{\boldsymbol p_3}&=(1+i)D.
\end{aligned}
\]

Direct exact evaluation of the sixteen-term sums gives

\[
\begin{aligned}
A={}&x^{-1}y^{-1}+x^{-1}-x^{-1}y
      +y^{-1}-1-y-x+x^2,
\\[3pt]
B={}&x^{-2}-x^{-1}-y^{-1}-1+y
      -xy^{-1}+x+xy,
\\[3pt]
C={}&-x^{-1}-x^{-1}y+y^{-2}-y^{-1}-1
      +y+x+xy,
\\[3pt]
D={}&x^{-1}y^{-1}+x^{-1}+y^{-1}-1-y+y^2
      -xy^{-1}-x.
\end{aligned}
\]

Every displayed expression has eight Laurent terms.

The action is exactly equivariant:

\[
h_j(A,B,C,D)
=
(A,B,C,D)^{\pi_j},
\]

where \(\pi_j\) is the corresponding regular permutation above. The
Gaussian normalization is precisely what incorporates the cyclotomic
phase adjustment identified in cycle 7.

## 4. Character resolvents

Use the Walsh character basis

\[
\begin{aligned}
T&=A+B+C+D,\\
U&=A-B+C-D,\\
V&=A+B-C-D,\\
W&=A-B-C+D.
\end{aligned}
\]

Their character sign rows are

\[
\begin{array}{c|rrrr}
 &h_0&h_1&h_2&h_3\\ \hline
T&1&1&1&1\\
U&1&-1&1&-1\\
V&1&1&-1&-1\\
W&1&-1&-1&1
\end{array}
\]

so these are exactly the four character resolvents. The trivial
resolvent \(T\) is the trace component; \(U,V,W\) are the three
nontrivial isotypical components.

Every character occurs. Orthogonality diagonalizes the packet but gives
no reason for any of \(T,U,V,W\) to be zero.

## 5. Exact search for low-degree relations

Treat \(A,B,C,D\) as Laurent polynomials in \(x,y\). Expand every
ordinary polynomial monomial in \(A,B,C,D\) of bounded total degree and
compute exact sparse rank over \(\mathbb Q\).

The relation nullities through degree five are

\[
(0,0,0,0,1).
\]

Thus:

\[
\boxed{\text{There is no nonzero polynomial relation of degree
\(\leq4\).}}
\]

The unique relation through degree five is, in character coordinates,

\[
\begin{aligned}
0={}&T^2U^3+16T^3U-16TUV^2-T^2UV^2-T^2UW^2\\
   &\quad-UV^4+2TV^3W.
\end{aligned}
\]

A particularly short independent degree-six relation is

\[
\boxed{
\left(V^3-TUW\right)^2=16T^3U^2.
}
\]

These relations describe the two-parameter image of the residual map.
They do not isolate its zero point.

For example, the rational specialization \(x=2,y=1\) gives

\[
(A,B,C,D)
=
\left(\frac32,\frac34,3,-3\right)
\]

and hence

\[
(T,U,V,W)
=
\left(\frac94,\frac{27}4,\frac94,-\frac{21}4\right).
\]

All four character components are nonzero while both displayed
relations hold.

## 6. An algebraic-unit Galois countermodel

The rational specialization does not itself realize a nontrivial
Galois action, because rational numbers cannot be sent to their distinct
inverses. This objection can be removed exactly.

Work in

\[
L=\mathbb Q(\sqrt2,\sqrt3)
\]

and take

\[
\begin{aligned}
x&=(3+2\sqrt2)(5+2\sqrt6),\\
y&=(3+2\sqrt2)(5-2\sqrt6).
\end{aligned}
\]

Both factors have norm \(1\) up to their quadratic conjugates:

\[
(3+2\sqrt2)(3-2\sqrt2)=1,
\qquad
(5+2\sqrt6)(5-2\sqrt6)=1.
\]

Moreover,

\[
3-2\sqrt2>0,\qquad5-2\sqrt6>0,
\]

as follows by squaring \(3>2\sqrt2\) and \(5>2\sqrt6\). Therefore all
four conjugates

\[
x^{-1},x,y,y^{-1}
\]

are totally positive algebraic units.

In the basis \(1,\sqrt2,\sqrt3,\sqrt6\), they are

\[
\begin{aligned}
x^{-1}&=(15,-10,8,-6),\\
x&=(15,10,8,6),\\
y&=(15,10,-8,-6),\\
y^{-1}&=(15,-10,-8,6).
\end{aligned}
\]

Let \(h_1\) change the sign of \(\sqrt2\), \(h_3\) change the sign of
\(\sqrt3\), and \(h_2=h_1h_3\). Their action on these units is exactly
the regular permutation required above.

Evaluating the residual packet gives

\[
\begin{aligned}
A&=(800,536,480,360),\\
B&=(800,-536,480,-360),\\
C&=(800,-536,-480,360),\\
D&=(800,536,-480,-360).
\end{aligned}
\]

These four residuals are themselves one faithful Galois orbit and are
all nonzero.

The character resolvents are even simpler:

\[
\begin{aligned}
T&=3200,\\
U&=1440\sqrt6,\\
V&=1920\sqrt3,\\
W&=2144\sqrt2.
\end{aligned}
\]

Every character projection is nonzero. Character orthogonality works
perfectly—it separates the four quadratic subfields—but supplies no
vanishing.

## 7. Logical consequence

The algebraic specialization satisfies all properties tested by the
proposed route:

1. the inputs are totally positive algebraic units;
2. inverse pairs multiply to \(1\);
3. a faithful abelian Galois group permutes them by the ray-unit action;
4. the residual packet is Galois equivariant;
5. its Walsh sums are the character resolvents;
6. the first exact algebraic packet relations hold.

Yet the packet is nonzero. Therefore none of those properties, alone or
together, proves TCC.

What is missing cannot be another generic fact about abelian Galois
orbits of units. It must distinguish the actual Shintani--Faddeev values
from arbitrary units with the same reciprocity pattern.

## 8. Decision and next direction

\[
\boxed{\text{Close the generic Galois-packet/algebraic-relation route.}}
\]

The next research cycle should return to the analytic origin of the
values, but with a narrower target than the pentagon/localization route
closed in cycle 6:

> Find an exact distribution, norm-compatibility, or difference equation
> satisfied by the complete finite array of Shintani--Faddeev RM values
> that fails in the algebraic-unit countermodel above.

Such a property would be genuinely new information. Before attempting a
proof, it should be evaluated on the explicit countermodel as a
specificity gate: if the countermodel also satisfies it, the property
cannot force TCC.

## Executable checks

The implementation provides:

- `canonical_dimension_four_residual_laurent_packet()`;
- `canonical_dimension_four_packet_permutations()`;
- `canonical_dimension_four_laurent_action()`;
- `canonical_dimension_four_character_resolvents()`;
- `canonical_dimension_four_relation_nullities()`;
- `canonical_dimension_four_packet_relation_residuals()`;
- `canonical_dimension_four_algebraic_unit_packet_record()`;
- exact arithmetic in \(\mathbb Q(\sqrt2,\sqrt3)\).

The test suite verifies the regular action, all four character
eigenrelations, absence of relations through degree four, both displayed
relations, the rational nonzero specialization, the algebraic-unit
Galois orbit, and the four nonzero character resolvents.

## Primary-source boundary

The source papers establish why this is the correct logical boundary:

- Kopp, [arXiv:2411.06763](https://arxiv.org/abs/2411.06763), relates
  Shintani--Faddeev RM values to square roots of Stark invariants while
  leaving the complete unsquared Shimura-reciprocity law as future work.
- Appleby--Flammia--Kopp,
  [arXiv:2501.03970](https://arxiv.org/abs/2501.03970), separately assumes
  the Stark conjectural input and the Twisted Convolution Conjecture.
  Its conditional structure is consistent with the present result:
  generic Stark-unit Galois behavior does not supply the missing
  convolution identity.
