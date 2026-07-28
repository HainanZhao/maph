# SIC--Stark research cycle 45: dimension seven passes the Shintani sieve

Date: 2026-07-28

## Breakthrough

Dimension seven is the unique dimension in the audited range
\(7\leq d\leq20\) that simultaneously satisfies:

1. the canonical order-ray field agrees with a maximal-order ray field
   at the multiplier modulus; and
2. the resulting one-place ray field is quadratic over its maximal
   absolutely abelian subfield.

The second property is Shintani's condition (0-9), the unconditional
algebraicity mechanism used in dimension five.  Thus dimension seven is
not merely the smallest untested case: it has a genuine route around the
open Stark identity that blocks dimension six.

This corrects the initially proposed all-quadratic sieve.  The canonical
family theorem already proves that every \(d\geq5\) has a nonquadratic
character in the principal Kopp packet.  The right question is not
whether all characters are quadratic, but whether an established
algebraicity theorem covers the nonquadratic packet.

## The exact sieve

Let

\[
 \mathcal O_d=\mathbb Z[\beta_d],\qquad
 \beta_d^2-(d-1)\beta_d+1=0,
\]

and write

\[
 (d+1)(d-3)=f_d^2D_K.
\]

The multiplier ideal of \(d\mathcal O_d\) in the maximal order is
\(d f_d\mathcal O_K\).  For the both-infinite maximal ray field \(N\),
put

\[
 A=\operatorname{Gal}(N/K).
\]

Conjugation \(\iota\in\operatorname{Gal}(K/\mathbb Q)\) acts on \(A\).
Since \(A\) is abelian, the commutator subgroup of
\(\operatorname{Gal}(N/\mathbb Q)=A\rtimes\langle\iota\rangle\) is

\[
 C=(\iota-1)A.
\]

Let \(B\) be the kernel obtained by deleting the second infinite place,
so the one-place field is \(H=N^B\).  The maximal absolutely abelian
subfield of \(N\) is \(N^C\), and

\[
 [H:H\cap\mathbb Q^{\rm ab}]
 =\frac{|C|}{|B\cap C|}.
\]

The sieve computes this index exactly from PARI ray generators and
conjugated ideal classes.

\[
\begin{array}{c|c|c|c|c|c}
d&f_d&|\mathrm{Cl}_{d\mathcal O_d,\infty}|&
|\mathrm{Cl}_{df_d,\infty}(\mathcal O_K)|&
\text{same field?}&[H:H\cap\mathbb Q^{\rm ab}]\\ \hline
7&2&12&12&\text{yes}&2\\
8&3&16&16&\text{yes}&4\\
9&1&36&36&\text{yes}&6\\
10&1&24&24&\text{yes}&6\\
11&2&80&80&\text{yes}&4\\
12&3&24&72&\text{no}&12\\
13&1&96&96&\text{yes}&4\\
14&1&72&72&\text{yes}&6\\
15&4&96&96&\text{yes}&12\\
16&1&128&128&\text{yes}&16\\
17&3&192&192&\text{yes}&6\\
18&1&108&108&\text{yes}&18\\
19&8&216&432&\text{no}&12\\
20&1&192&192&\text{yes}&12
\end{array}
\]

Only \(d=7\) has Shintani index two.

## Dimension-seven order and ray field

Put

\[
 K=\mathbb Q(\sqrt2),\qquad
 \phi=1+\sqrt2,\qquad
 \beta=\phi^2=3+2\sqrt2.
\]

Then

\[
 \mathcal O_7=\mathbb Z[\beta]
 =\mathbb Z+2\mathcal O_K,
\qquad
 \operatorname{disc}(\mathcal O_7)=32,
\qquad
 h(\mathcal O_7)=1.
\]

The multiplier ideal of \(7\mathcal O_7\) is
\(14\mathcal O_K\).  Direct residue enumeration gives

\[
 |(\mathcal O_7/7\mathcal O_7)^\times|=36.
\]

The signed image of
\(\mathcal O_7^\times=\langle-1,\beta\rangle\) has order six, hence

\[
 |\mathrm{Cl}_{7\mathcal O_7,\infty_1}(\mathcal O_7)|
 =\frac{36\cdot2}{6}=12.
\]

PARI gives

\[
 \mathrm{Cl}_{(14)\infty_1}(\mathcal O_K)
 \simeq C_6\times C_2,
\]

also of order twelve.  The natural order-to-maximal-order ray map is
surjective, so equality of orders proves it is an isomorphism.

## Shintani condition at modulus fourteen

For

\[
 A=\mathrm{Cl}_{(14)\infty_1\infty_2}(\mathcal O_K)
 \simeq C_6\times C_2\times C_2,
\]

conjugation has matrix

\[
 \begin{pmatrix}
 4&3&0\\
 1&0&0\\
 0&0&1
 \end{pmatrix}.
\]

Consequently

\[
 C=(\iota-1)A
 =\langle(3,1,0)\rangle.
\]

The map deleting \(\infty_2\) has matrix

\[
 \begin{pmatrix}
 1&0&3\\
 0&1&0
 \end{pmatrix},
\]

and kernel

\[
 B=\langle(3,0,1)\rangle.
\]

The two order-two subgroups are distinct, so

\[
 |C|=2,\qquad B\cap C=1,\qquad
 [H:H\cap\mathbb Q^{\rm ab}]=2.
\]

This is exactly Shintani's quadratic-over-absolutely-abelian
hypothesis.

## Conductor lowering does not spoil the result

Because

\[
 \beta=2\phi+1,
\]

the conductor-lowering matrix has determinant two.  A primitive
characteristic \((a,b)\bmod7\) has two maximal-order lifts

\[
 s_j=
 \left(\frac{a-b+7j}{14},\frac{2b}{14}\right),
 \qquad j=0,1,
\]

represented by

\[
 \gamma_j=2b\phi-a+b-7j.
\]

Across all \(48\) primitive characteristics and both lifts, the divisor
and lowered-modulus norm pairs are exactly

\[
 (1,196),\quad(4,49),\quad(7,28),\quad(28,7).
\]

The six distinct lowered ideals have one-place ray groups

\[
 1,\quad C_2,\quad C_2,\quad C_6,\quad C_6\times C_2.
\]

The only nonquadratic proper level is modulus \(7\).  Its both-place
group is \(C_6\times C_2\); its commutator and one-place kernel are the
distinct classes \((3,1)\) and \((3,0)\).  It therefore also has
Shintani index two.  Every conductor-lowered factor is consequently
covered either by a quadratic theorem or by Shintani's condition.

This statement is at the level of fields and conductors.  A provisional
attempt to reuse the dimension-eight ideal-label formula verbatim did
not reproduce the dimension-seven analytic logs.  Thus the
conductor-two \(\Upsilon\)-class translation, including its choice of
reduced representative and cocycle power, must be derived directly from
Kopp's Theorems 3.14 and 4.46.  No provisional formula from that failed
comparison has been retained.

The underlying TCC target is nevertheless numerically sound.  Direct
evaluation of the \(48\) nonexceptional double-sine values gives

\[
\begin{aligned}
|\operatorname{Tr}K-1|&<3.2\cdot10^{-16},\\
\|K^2-K\|_{\max}&<4.8\cdot10^{-10},\\
\max|\text{\(2\times2\) minor of }K|&<2.2\cdot10^{-10}.
\end{aligned}
\]

## What this proves—and what remains

This cycle proves that dimension seven has an unconditional
**algebraicity route**.  It does not yet prove the dimension-seven TCC.
The remaining work is finite and explicit:

1. derive the complete \(48\)-characteristic conductor-lowered
   Kopp/AFK table from the exact \(\Upsilon\) correspondence, including
   phases, signs, cocycle powers, and Artin labels;
2. construct and certify the corresponding ray units using Shintani's
   algebraicity theorem;
3. reconstruct the \(7\times7\) ghost matrix;
4. factor all rank-one minors over the certified unit field; and
5. transport the two formal shifts between all discriminant-\(32\)
   admissible tuples.

Unlike dimension six, this list contains no presently open Stark
identity.

## Reproducibility

- `scripts/screen_higher_dimension_theorem_coverage.gp`
- `scripts/screen_higher_dimension_theorem_coverage.py`
- `scripts/dimension_seven_candidate_audit.gp`
- `scripts/explore_dimension_seven.py`
- `scripts/analyze_canonical_order_character_obstruction.py`
- `tests/test_higher_dimension_sieve.py`

## Primary sources

- T. Shintani, *On certain ray class invariants of real quadratic
  fields*, J. Math. Soc. Japan 30 (1978), 139--167,
  <https://doi.org/10.2969/jmsj/03010139>.
- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, especially the conductor-lowering section,
  <https://arxiv.org/abs/2411.06763>.
