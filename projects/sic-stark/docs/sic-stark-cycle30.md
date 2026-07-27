# SIC--Stark research cycle 30: the dimension-eight quartic bridge

Date: 2026-07-27

## Outcome

The two quartic character pairs in the canonical dimension-eight packet
have now been reduced to explicit, certified cyclic quartic extensions of
\(K=\mathbb Q(\sqrt5)\).  The nonmaximal-order Euler-factor problem
disappears in this sector, and Roblot's hypotheses and unit-index
conditions can be checked exactly.

For each pair there is an explicit totally positive anti-unit
\(\eta_b\) such that Roblot's unconditional cyclic-quartic theorem gives

\[
 \left|L'_{S}(0,\chi_b)\right|
 =
 \left|
 \frac12\sum_{g\in C_4}\chi_b(g)\log|\eta_b^g|
 \right|,
 \qquad b=0,1.
\]

The complex quantities on the two sides agree numerically to more than
\(90\) decimal places after a suitable exact choice of Galois
orientation.  This is strong evidence for the desired Stark identity,
but it is not yet an unconditional proof of the phase: Roblot's theorem
states equality of absolute values.  This distinction is the surviving
dimension-eight analytic obstruction.

Thus the new conclusion is

\[
\boxed{
\begin{gathered}
\text{the fields, units, indices, ramification, and Euler factors close
unconditionally;}\\
\text{only the oriented complex Stark phase remains.}
\end{gathered}}
\]

## 1. Replacing the order ray group by a maximal-order ray group

Put

\[
 K=\mathbb Q(\phi),\qquad \phi^2-\phi-1=0,
\]

and

\[
 \mathcal O_3=\mathbb Z+3\mathcal O_K
 =\mathbb Z[3\phi].
\]

The canonical dimension-eight modulus is \(8\mathcal O_3\).  In the
basis \(1,\phi\),

\[
 8\mathcal O_3=8\mathbb Z+24\mathbb Z\phi.
\]

Its maximal-order colon is

\[
 (8\mathcal O_3:\mathcal O_K)=24\mathcal O_K.
\]

Indeed, write \(x=8a+24b\phi\in8\mathcal O_3\).  Since

\[
 x\phi=24b+(8a+24b)\phi,
\]

the condition \(x\phi\in8\mathcal O_3\) is equivalent to \(3\mid a\).
This gives \(x\in24\mathcal O_K\), and the converse is immediate.

The exact order computation gives

\[
 \operatorname{Cl}_{(8)\infty_2}(\mathcal O_3)
 \cong C_4\times C_2\times C_2.
\]

PARI gives

\[
 \operatorname{Cl}_{(24)\infty_2}(\mathcal O_K)
 \cong C_4\times C_2\times C_2.
\]

The Kopp--Lagarias change-of-order map is a surjection from the latter
group to the former.  Since both groups have order \(16\), it is an
isomorphism:

\[
\boxed{
 \operatorname{Cl}_{(24)\infty_2}(\mathcal O_K)
 \simeq
 \operatorname{Cl}_{(8)\infty_2}(\mathcal O_3).
}
\]

This removes the conjectural nonmaximal-order algebraicity issue from
the dimension-eight quartic sector: the relevant characters can be
handled as ordinary maximal-order Hecke characters.

## 2. Exact coordinate transport

Use the order-ray generators

\[
 A=[3\phi],\qquad
 B=[1+12\phi],\qquad
 R=[-1,\text{ positive at }\infty_2],
\]

of orders \(4,2,2\), respectively.  Coprime positive lifts to modulus
\(24\) are

\[
 8+3\phi,\qquad 17+12\phi,\qquad 7.
\]

In PARI's coordinates for \(C_4\times C_2\times C_2\), their exact ray
logs are

\[
 A\longmapsto(1,1,0),\qquad
 B\longmapsto(0,1,0),\qquad
 R\longmapsto(2,0,1).
\]

Consequently an order-ray character \(\chi_{a,b,c}\) maps in the dual
coordinates to

\[
 (a-2b,\ b,\ c-a)
 \quad\text{in}\quad
 \mathbb Z/4\times\mathbb Z/2\times\mathbb Z/2.
\]

The four supported quartic characters therefore become

\[
 (1,0,0),\ (3,0,0),\ (1,1,0),\ (3,1,0).
\]

They split into the two conjugate pairs

\[
 \{(1,0,0),(3,0,0)\},
 \qquad
 \{(1,1,0),(3,1,0)\}.
\]

## 3. The two cyclic quartic fields

Let \(F_b/K\) be the quotient field belonging to the \(b\)-th pair.
Relative equations are

\[
\begin{aligned}
 F_0/K:\quad&X^4-6\phi X^2+3,\\
 F_1/K:\quad&X^4+(6-6\phi)X^2+3.
\end{aligned}
\]

Convenient absolute models are

\[
\begin{aligned}
 P_0(X)&=X^8-6X^6-30X^4-18X^2+9,\\
 P_1(X)&=X^8+6X^6-30X^4+18X^2+9.
\end{aligned}
\]

Exact PARI certification gives, for both fields,

\[
 \operatorname{sig}(F_b)=(4,2),\qquad
 h(F_b)=1,\qquad
 \operatorname{bnfcertify}(F_b)=1.
\]

The two fields share the same quadratic subfield over \(K\):

\[
 F_b^+=K(\sqrt3).
\]

It is totally real, has class number one, and is unconditionally
certified by `bnfcertify`.

Both quartic characters have conductor

\[
 (24)\infty_2,
\]

whereas their common quadratic square has conductor

\[
 (12)
\]

with no infinite place.

It follows that the primes above \(2\) and \(3\) ramify already in
\(F_b^+/K\).  In a cyclic group of order four, an inertia group whose
image in the quadratic quotient is nontrivial must be the whole group.
Hence those primes remain ramified in \(F_b/F_b^+\).  This proves
Roblot's condition (A3), and no finite prime in \(S\) is inert in the
top quadratic step:

\[
 t_S=0.
\]

The signatures prove (A1), and the totally real index-two fixed field
proves (A2).

## 4. Exact unit indices

Let \(\tau\) be the order-two automorphism \(X\mapsto-X\) in the models
\(P_b\).  In both fields, if
\(\epsilon_1,\ldots,\epsilon_5\) are the certified PARI fundamental
units, set

\[
 \eta_b=(\epsilon_4\epsilon_5)^2.
\]

Exact reduction modulo \(P_b\) proves

\[
 \eta_b^\tau\eta_b=1.
\]

The norm images of the five fundamental units in the rank-three unit
lattice of \(F_b^+\) have exponent matrices

\[
 N_0=
 \begin{pmatrix}
 2&0&0&0&0\\
 0&0&-2&-1&1\\
 0&2&-2&-1&1
 \end{pmatrix},
\qquad
 N_1=
 \begin{pmatrix}
 2&0&0&0&0\\
 0&2&-2&-1&1\\
 0&0&2&1&-1
 \end{pmatrix}.
\]

The gcd of their \(3\times3\) minors is \(4\).  Therefore

\[
 [\overline U_{F_b^+}:N\overline U_{F_b}]=4=2^2,
\qquad e=2.
\]

The anti-unit lattice \(U^-_{F_b}\) has rank two.  In integral bases
reported by the certificate, the two columns corresponding to
\(\eta_b\) and its generator-conjugate are

\[
 \begin{pmatrix}-2&0\\0&2\end{pmatrix}
 \quad\text{and}\quad
 \begin{pmatrix}-2&0\\0&-2\end{pmatrix},
\]

respectively.  Thus

\[
 [U^-_{F_b}:\mathbb Z[C_4]\bar\eta_b]=4.
\]

Since both class groups are trivial,

\[
 \operatorname{Cl}_{F_b}^-=1.
\]

Roblot's condition (P1) is therefore exactly

\[
 4=2^{e+t_S}|\operatorname{Cl}_{F_b}^-|
   =2^{2+0}\cdot1,
\]

and (P2) is automatic because the quotient has no odd primary part.

## 5. The prime-three Euler factor disappears

The order/maximal-order comparison enlarges the finite modulus from
\(8\) to \(24\), so a possible Euler factor at \(3\) had to be checked.
Both quartic characters are already primitive at \(3\), because their
conductor is the full finite ideal \((24)\).  Their local factor at
\(3\) is therefore \(1\).

Equivalently, PARI's primitive and imprimitive derivatives agree for
all four quartic characters.  At \(100\)-digit working precision the
certificate residual is zero to more than \(110\) digits.  This
numerical calculation audits the exact conductor argument; it is not
being used in place of it.

## 6. What Roblot proves—and what he does not

Roblot's cyclic-quartic theorem unconditionally constructs a solution
of the unit-index conditions and proves

\[
 \left|L'_{S}(0,\chi)\right|
 =
 \frac12
 \left|\sum_{g\in C_4}\chi(g)\log|\eta^g|\right|.
\]

For the units above, oriented logarithmic resolvents numerically give

\[
\begin{aligned}
 8.2815657385270383359
  +5.4577980221739814265\,i
 &=
 L'_S(0,(1,0,0)),\\
 -2.9688538268612984554
  +6.2476661476733697830\,i
 &=
 L'_S(0,(1,1,0)),
\end{aligned}
\]

to more than \(90\) decimal places.

This phase match is not a consequence of the cited theorem.  The paper
itself describes the conclusion as a weak Stark result “up to absolute
values.”  Multiplying or conjugating a candidate anti-unit changes its
complex resolvent by a Gaussian unit and/or complex conjugation while
preserving the proven absolute value.

Therefore the following stronger equalities remain unproved:

\[
 L'_S(0,\chi_b)
 =
 \frac12\sum_g\chi_b(g)\log|\eta_b^g|.
\]

They are now the only quartic analytic gap.  The gap is one of
orientation or phase, not one of class-field identification, unit
existence, regulator index, ramification, or Euler factors.

## 7. Exact unit data

The minimal polynomials of the selected anti-units are

\[
\begin{aligned}
 m_{\eta_0}(T)
 ={}&T^8-4184T^7+922684T^6+881176T^5+861190T^4\\
 &\quad+881176T^3+922684T^2-4184T+1,\\
 m_{\eta_1}(T)
 ={}&T^8-536T^7+9916T^6+2008T^5+14086T^4\\
 &\quad+2008T^3+9916T^2-536T+1.
\end{aligned}
\]

The certificate prints their exact expressions in the power bases of
\(P_0\) and \(P_1\), verifies \(\eta_b^\tau\eta_b=1\), computes the
Galois action on the full unit lattice, and checks the two index-four
determinants.

## Recommendation

Dimension eight is substantially closer than it appeared in cycle 29:
the nonmaximal-order and quartic-unit problems are solved in this
specific packet.  But it is not yet unconditional, because the
oriented phase is exactly the information omitted by Roblot's
absolute-value theorem.

The next useful dimension-eight question is narrowly formulated:

> Can the AFK/Kopp cocycle normalization, together with a direct
> Shintani cone calculation, fix the phase of the two explicit
> logarithmic resolvents?

If yes, the complete analytic packet can be reconstructed from
quadratic class-number formulas and the two units above, after which
the finite \(8\times8\) TCC calculation becomes an exact algebraic
certificate.  If no phase theorem is available, dimension six remains
the better primary target because it has only one unresolved
orientation identity and no nonmaximal-order layer.

## Reproducibility

- `scripts/dimension_eight_quartic_bridge.gp`
- `scripts/analyze_dimension_eight_order_ray.py`
- `scripts/generate_dimension_eight_ray_table.py`

The main certificate uses PARI/GP 2.15.4 and calls `bnfcertify` for the
base, both quartic fields, and their common totally real subfield.

## Primary sources

- X.-F. Roblot, *Index formulae for Stark units and their solutions*,
  Pacific J. Math. 266 (2013), 391--422; arXiv:1112.2820, especially
  Theorem 6.1.
- G. S. Kopp and J. C. Lagarias, *Ray class groups and ray class fields
  for orders of number fields*, Essential Number Theory 4 (2025),
  1--65.
- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, arXiv:2411.06763v3.
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, arXiv:2501.03970v2.
