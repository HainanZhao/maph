# SIC--Stark research cycle 26: the orientation wall and the \(d=8\) order

Date: 2026-07-27

## Outcome

Two proposed escape routes from the remaining dimension-six obstruction
have now been tested.

1. Kopp's conductor-lowering identity supplies product and norm relations,
   but it does not isolate the two oriented primitive order-six character
   components.  Rational class-number and Dedekind-zeta data are invariant
   under reversal of the Artin generator, while the SIC minors are not.
2. The promising maximal-order proxy for dimension eight does not survive
   passage to the actual quadratic order of discriminant \(45\).  Its
   one-place ray group is
   \[
     C_4\times C_2\times C_2,
   \]
   and Kopp's difference contains four quartic as well as four quadratic
   characters.

Thus neither route gives another immediate unconditional theorem.  The
dimension-six problem is nevertheless sharply localized: it needs one
genuinely oriented order-six analytic input.  The finite Artin orientation
itself is now explicit and certified below.  Dimension eight is a secondary
quartic-character project, not a free analogue of dimension four.

## 1. What distribution relations do and do not determine

Kopp's conductor-lowering/level-raising theorem has the schematic form

\[
 \operatorname{shin}^{\boldsymbol r}_{BAB^{-1}}(B\alpha)
 =
 \prod_{\substack{\boldsymbol s\in\mathbb Q^2/\mathbb Z^2\\
                   B\boldsymbol s-\boldsymbol r\in\mathbb Z^2}}
 \operatorname{shin}^{\boldsymbol s}_{A}(\alpha).
\]

For the dimension-six fundamental unit \(\beta\), whose quadratic-number
conductor is already \(1\), this identity relates products of level-six
values to lower-level values.  It explains the norm relation already found
in cycle 25, but it does not choose an individual primitive value from its
Artin orbit.

This limitation is now formal.  Write the one-place ray group as

\[
  G=C_6=\langle g\rangle,\qquad R=g^3.
\]

The Kopp difference \(1-R\) has Fourier support

\[
 \chi_1,\quad\chi_3,\quad\chi_5,
\]

of respective orders \(6,2,6\).  Complex conjugation acts by

\[
 \chi_1\longleftrightarrow\chi_5,\qquad \chi_3\longmapsto\chi_3.
\]

Consequently rational character data splits the packet only into

\[
 \{\chi_3\}\quad\text{and}\quad\{\chi_1,\chi_5\}.
\]

It cannot distinguish the two members of the primitive pair.  On ray
classes this ambiguity is precisely

\[
 g\longleftrightarrow g^{-1}.
\]

The unlabeled ray-unit polynomial, reciprocal pairs, every subgroup norm,
and rational sums of the two primitive \(L\)-derivatives are unchanged by
this reversal.  The inversion-odd primitive component changes sign.

This explains the exact finite observation from cycle 25.  The correct
Artin packet and a reversed packet satisfy the same polynomial and norm
constraints, but only the correct packet annihilates all minors; a false
reversal leaves a maximum minor of about \(6.29\cdot10^{-2}\).

The remaining lemma therefore cannot come from another rational
class-number quotient.  It must provide at least one of:

- a non-rational order-six character evaluation;
- an explicit reciprocity law fixing the Frobenius generator;
- a direct, oriented evaluation of one primitive double-sine value; or
- an equivalent cubic-resolvent sign tied to the AFK characteristic.

## 2. The Artin orientation is now explicit

The finite orientation can be fixed without a numerical choice of roots.
The characteristic-to-ray calculation contains the prime

\[
 \mathfrak p=(4\beta+1),\qquad N\mathfrak p=37.
\]

PARI's exact ray discrete logarithm is

\[
 [\mathfrak p]=g
 \quad\text{in}\quad
 \operatorname{Cl}_{(6)\infty_2}(K)=\langle g\rangle\cong C_6.
\]

The canonical signed overlap polynomial over \(K\) is

\[
\begin{aligned}
 P(X)={}&X^6+(\beta-1)X^5+(1-\beta)X^4-(4\beta+1)X^3\\
       &+(1-\beta)X^2+(\beta-1)X+1.
\end{aligned}
\]

Modulo \(\mathfrak p\), one has \(\beta=9\) in \(\mathbb F_{37}\), and
\(P\) remains irreducible.  Arithmetic Frobenius is therefore computed
exactly by

\[
 X\longmapsto X^{37}\pmod{P,\mathfrak p}.
\]

Matching its six powers against the exact `nfgaloisconj` automorphisms gives

\[
\begin{array}{c|cccccc}
j&0&1&2&3&4&5\\ \hline
\operatorname{Frob}_{\mathfrak p}^{\,j}(x)
&x&-z^{-1}&-w^{-1}&x^{-1}&-z&-w.
\end{array}
\]

The corresponding exact automorphism indices are

\[
 [1,5,2,4,6,3].
\]

Thus the earlier reversal ambiguity is no longer present in the algebraic
certificate: it is resolved by the ray generator
\(\mathfrak p=(4\beta+1)\) and arithmetic Frobenius.  What remains is to
prove that Kopp's analytically defined primitive value belongs to this
oriented algebraic orbit.  In particular, the missing result may now be
stated as one concrete equality:

\[
 \operatorname{Art}(\mathfrak p)(x_{\mathrm{an}})
 =-z_{\mathrm{an}}^{-1}
\]

with the Artin/Frobenius convention fixed as above, together with
algebraicity of one member of the packet.  Replacing arithmetic Frobenius
by geometric Frobenius reverses the displayed cycle, so that convention
must be stated in any theorem.

## 3. Independent confirmation from the newest SIC--Stark work

Bengtsson and McConnell's June 2026 preprint gives an independent
stratification of the dimension-six overlaps.  Their dimension-six table
places the singular strata in square roots of modulus-three Stark units,
while the generic \(D\otimes D\) stratum, containing eighteen overlaps,
uses square roots of full modulus-six Stark units.

This matches the exact decomposition in cycle 25:

- the lower value \(y\) is the quadratic modulus-three component and is
  already unconditional;
- the three pairs \(x,z,w\) form the generic full modulus-six packet.

The paper does not close the bridge.  It explicitly presents the
identification of SIC overlaps with Stark units as the difficult unproved
step and computes the units numerically.  It therefore corroborates the
location of our obstruction rather than removing it.

## 4. The actual dimension-eight order

For the canonical dimension-eight form,

\[
 D=(8+1)(8-3)=45.
\]

The relevant order is not the maximal order of
\(K=\mathbb Q(\sqrt5)\).  It is the conductor-three order

\[
 \mathcal O_3=\mathbb Z[\theta],
 \qquad \theta=3\phi,\qquad
 \theta^2=3\theta+9,
\]

where \(\phi=(1+\sqrt5)/2\).  The canonical positive unit is

\[
 \beta=\phi^4=\theta+2.
\]

The coefficient of \(\phi\) in \(\phi^n\) is the Fibonacci number \(F_n\).
Modulo \(3\), \(F_n=0\) exactly when \(4\mid n\).  Hence

\[
 \mathcal O_3^\times=\langle-1,\beta\rangle.
\]

The ring class number formula gives

\[
 h(\mathcal O_3)
 =h(\mathcal O_K)\,
   \frac{3\left(1-\left(\frac5{3}\right)/3\right)}
        {[\mathcal O_K^\times:\mathcal O_3^\times]}
 =1\cdot\frac{3(1+1/3)}4
 =1.
\]

This agrees with the independent PARI calculation
\(\texttt{qfbclassno(45)}=1\).

Because \(3\) and \(8\) are coprime, the ray exact sequence for the order
reduces the calculation to the finite ring

\[
 \mathcal O_3/8\mathcal O_3
 =(\mathbb Z/8\mathbb Z)[\theta]/
   (\theta^2-3\theta-9).
\]

It has \(48\) units.  The image of the global unit group has order \(6\):
\(-1\) has order \(2\), and

\[
 \beta^3\equiv1\pmod8,\qquad \beta\not\equiv1\pmod8.
\]

Exact coset enumeration gives

\[
\begin{array}{c|c|c}
\text{modulus}&\text{ray-group structure}&\text{order}\\ \hline
(8)&C_4\times C_2&8\\
(8)\infty_2&C_4\times C_2\times C_2&16\\
(8)\infty_1\infty_2&C_4\times C_2\times C_2\times C_2&32.
\end{array}
\]

The element-order distributions are, respectively,

\[
\begin{array}{c|ccc}
&1&2&4\\ \hline
(8)&1&3&4\\
(8)\infty_2&1&7&8\\
(8)\infty_1\infty_2&1&15&16.
\end{array}
\]

These distributions certify the displayed invariant factors, rather than
merely the group orders.

## 5. Character support in dimension eight

Kopp's sign class is represented by

\[
 R=(-1\bmod8,\,+\text{ at }\infty_2).
\]

Exact enumeration proves that \(R\) is nontrivial of order two and

\[
 R\notin2G.
\]

It may therefore be chosen as one of the independent \(C_2\) factors in

\[
 G=C_4\times C_2\times C_2.
\]

Of the sixteen characters of \(G\), exactly eight satisfy
\(\chi(R)=-1\) and occur in \(1-R\).  Among those eight,

\[
 \boxed{\text{four are quadratic and four are quartic}.}
\]

This answers the screening question decisively.  The specific character
packet needed in dimension eight does not factor entirely through
quadratic subfields.  The maximal-order proxy \(C_2\times C_2\) had erased
the \(C_4\) factor created by the conductor-three order.

## 6. Literature boundary

No currently identified theorem closes the dimension-six primitive packet.

- Shintani's 1978 theorem does not apply because the relevant ray field is
  degree six, rather than degree at most two, over its maximal absolutely
  abelian subfield.
- Roblot's cyclic-sextic theorem assumes away the wild ramification at the
  prime over \(3\) that occurs here, and in any case supplies only the
  weaker absolute-value Fourier statement.
- The Dasgupta--Kakde Brumer--Stark theorem concerns CM abelian extensions
  and \(p\)-adic Brumer--Stark units, not this mixed-signature
  archimedean ray field.
- Kopp's theorem supplies the exact analytic cocycle formula, but its
  algebraicity is conditional on the relevant Stark statement.

This is a theorem-coverage gap, not evidence against the proposed identity.
The numerical, field-theoretic, and exact-minor evidence all remain
consistent.

## Recommendation

The best next step is not to start a dimension-eight proof.  It is to
finish the one missing oriented primitive lemma in dimension six.

A focused attack should now:

1. write the primitive logarithms in the \(\chi_1,\chi_5\) Fourier basis;
2. use the certified prime
   \(\mathfrak p=(4\beta+1)\) and its Frobenius cycle to translate the AFK
   characteristic order into the algebraic ray field; and
3. prove that this oriented algebraic unit has the same logarithm as
   Kopp's double-sine value.

The finite Frobenius step is complete.  The last equality is the genuinely
new analytic content.  If it cannot be proved with existing theorems, the
honest output is a sharply formulated special-case Stark lemma whose proof
would complete dimension six.

Dimension eight should remain the backup project.  Its quartic characters
are simpler than a large general ray group, but its nonmaximal-order
reciprocity and Euler-factor bookkeeping must be developed first.

## Reproducibility

- `scripts/analyze_dimension_six_orientation_obstruction.py`
- `scripts/dimension_six_artin_orientation.gp`
- `scripts/dimension_six_primitive_fourier_audit.gp`
- `scripts/analyze_dimension_eight_order_ray.py`
- `scripts/analyze_dimension_six_character.py`
- `scripts/dimension_six_lower_stratum.gp`
- `scripts/dimension_six_embedding_certificate.gp`
- `scripts/verify_dimension_six_conjugates.gp`

## Primary sources

- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, J. Math. Soc. Japan 30 (1978), 139--167.
- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422;
  <https://arxiv.org/abs/1112.2820>.
- S. Dasgupta and M. Kakde, *On the Brumer--Stark conjecture*,
  <https://arxiv.org/abs/2103.02516>.
- G. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, <https://arxiv.org/abs/2411.06763>.
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, <https://arxiv.org/abs/2501.03970>.
- I. Bengtsson and G. McConnell, *How Stark units enter SIC overlaps*,
  <https://arxiv.org/abs/2606.23535>.
