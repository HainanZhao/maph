# SIC--Stark research cycle 46: the dimension-seven conductor bridge

## Result

The convention-sensitive absolute-value bridge in dimension seven is now
complete.  For every nonzero characteristic
\((a,b)\in(\mathbb Z/7\mathbb Z)^2\), the two conductor-lowered
characteristics have been assigned:

- an exact maximal-order ray class;
- an exact flat-to-invertible conductor reduction;
- the canonical stabilizer;
- Kopp's exponent \(n\in\{1,2\}\); and
- the corresponding differenced partial-zeta derivative.

The resulting formula reproduces all \(48\) direct principal-cocycle
log-squares.  At the current numerical integration precision,

\[
 \max_{(a,b)\ne(0,0)}
 \left|
 2\log|\nu_{a,b}|-\sum_{j=0}^{1}n_{a,b,j}D_{a,b,j}
 \right|
 <3.5\cdot10^{-9}.
\]

This closes the absolute values and Artin labels.  It does **not** yet close
the roots of unity in the cocycle multipliers, construct exact ray units, or
prove the dimension-seven rank-one minors.

## 1. The reduced maximal-order point

Put

\[
 K=\mathbb Q(\sqrt2),\qquad
 \alpha=2+\sqrt2,\qquad
 \beta=3+2\sqrt2.
\]

The point \(\alpha\) is reduced:

\[
 0<\alpha'=2-\sqrt2<1<\alpha.
\]

The determinant-two matrix

\[
 B=\begin{pmatrix}2&-1\\0&1\end{pmatrix}
\]

satisfies \(B\alpha=2\alpha-1=\beta\).  If

\[
 r=\begin{pmatrix}a/7\\b/7\end{pmatrix},
\]

then the two solutions of \(Bs-r\in\mathbb Z^2\) are

\[
 s_j=
 \begin{pmatrix}
  (a+b+7j)/14\\
  2b/14
 \end{pmatrix},
 \qquad j=0,1.
\]

This is the complete fiber in Kopp's conductor-lowering theorem.

## 2. Inverse \(\Upsilon\) without an ideal-label guess

For the maximal order
\(\mathcal O_K=\mathbb Z[\sqrt2]=\alpha\mathbb Z+\mathbb Z\) and modulus
\(14\mathcal O_K\), Kopp's inverse \(\Upsilon\) construction may be taken
with scalar \(14\) and auxiliary ideal \(\mathcal O_K\).  It therefore sends
\(s_j\) to the flat ray class represented by

\[
\begin{aligned}
 \gamma_{a,b,j}
 &=14(s_{j,2}\alpha-s_{j,1})\\
 &=2b\sqrt2+3b-a-7j.
\end{aligned}
\]

If necessary, an integral multiple of \(14\) is added to \(\gamma\) to
choose the totally positive representative required by the inverse
\(\Upsilon\) statement.  The ray class is unchanged.

For

\[
 \mathfrak d=(14,\gamma),\qquad
 \mathfrak m'=\mathfrak d^{-1}(14),\qquad
 A'=[(\gamma)\mathfrak d^{-1}],
\]

Proposition 6.2 gives

\[
 Z_{14,\infty_2}(s,A)
 =N(\mathfrak d)^{-s}Z_{\mathfrak m',\infty_2}(s,A').
\]

The value at zero on the right is zero, so the derivative is unchanged.
The script nevertheless evaluates the general derivative formula, including
the possible
\(-\log N(\mathfrak d)\,Z_{\mathfrak m',\infty_2}(0,A')\) term, rather
than assuming its disappearance.

## 3. The six exact lowered moduli

Across the \(96\) lifted factors, precisely six HNF moduli occur.  The table
also records their multiplicities and Kopp exponent.

| lowered modulus | factors | one-place ray group | negative-norm unit congruent to \(1\) | \(n\) |
|---|---:|---:|---:|---:|
| \(\begin{psmallmatrix}14&0\\0&14\end{psmallmatrix}\) | 36 | \(C_6\times C_2\) | none | 1 |
| \(\begin{psmallmatrix}7&0\\0&7\end{psmallmatrix}\) | 36 | \(C_6\) | none | 1 |
| \(\begin{psmallmatrix}14&6\\0&2\end{psmallmatrix}\) | 6 | \(C_2\) | none | 1 |
| \(\begin{psmallmatrix}14&8\\0&2\end{psmallmatrix}\) | 6 | \(C_2\) | none | 1 |
| \(\begin{psmallmatrix}7&3\\0&1\end{psmallmatrix}\) | 6 | \(C_2\) | \(-\phi^3\) | 2 |
| \(\begin{psmallmatrix}7&4\\0&1\end{psmallmatrix}\) | 6 | trivial | \(\phi^3\) | 2 |

Here \(\phi=1+\sqrt2\), so

\[
 \phi^3=7+5\sqrt2.
\]

The two exceptional congruences are exact:

\[
\begin{aligned}
 -\phi^3-1
   &=-8-5\sqrt2
     \in\left\langle7,\,3+\sqrt2\right\rangle,\\
 \phi^3-1
   &=6+5\sqrt2
     \in\left\langle7,\,4+\sqrt2\right\rangle.
\end{aligned}
\]

The second modulus has trivial ray group, so its differenced derivative is
zero, but its exponent is still recorded correctly.  The finite search for
the remaining moduli tests both signs through twice the quotient-ring norm;
this is exhaustive because the powers of a residue-class unit repeat within
the finite group.

## 4. Stabilizer and exponent

The determinant-minus-one fundamental stabilizer of \(\alpha\) is

\[
 M=
 \begin{pmatrix}
 3&-2\\
 1&-1
 \end{pmatrix}.
\]

For every one of the \(96\) lifted characteristics, the canonical
determinant-one stabilizer is exactly

\[
 A=M^6=
 \begin{pmatrix}
 239&-140\\
 70&-41
 \end{pmatrix}.
\]

Thus no hidden cocycle power remains: the common stabilizer power is one for
every factor.

Kopp's Theorem 8.2 gives

\[
 \exp\!\left(n_jD_j\right)
 =\operatorname{samech}^{\,s_j}_{A}(\alpha).
\]

Because the samech cocycle is the square of the shin cocycle times a
root-of-unity multiplier,

\[
 2\log\left|
 \operatorname{shin}^{\,s_j}_{A}(\alpha)
 \right|=n_jD_j.
\]

Applying conductor lowering to the shin cocycle therefore yields the
audited identity

\[
 \boxed{
 2\log|\nu_{a,b}|
 =\sum_{j=0}^{1}n_{a,b,j}D_{a,b,j}.
 }
\]

## 5. The PARI leading-term trap

The last numerical discrepancy came from the interpretation of
`bnrL1(...,,6)`.  PARI returns

\[
 [r_\chi,c_\chi],
 \qquad
 L(s,\chi)=c_\chi s^{r_\chi}+O(s^{r_\chi+1}),
\]

not the pair \([L(0,\chi),L'(0,\chi)]\).

Consequently,

\[
 L(0,\chi)=
 \begin{cases}
 c_\chi,&r_\chi=0,\\
 0,&r_\chi\ne0,
 \end{cases}
 \qquad
 L'(0,\chi)=
 \begin{cases}
 c_\chi,&r_\chi=1,\\
 0,&r_\chi\ne1.
 \end{cases}
\]

Treating the leading coefficients of the order-two and order-three
characters as first derivatives produced the former uniform scalar
residual.  Removing those spurious terms closes the packet.

The PARI computation reports version \(2.15.4\), and
`bnfcertify` returns \(1\).

## 6. Reproducibility

- `scripts/explore_dimension_seven_conductor_lowering.gp` prints all
  \(96\) exact lift, ideal, ray-class, sign-class, stabilizer, and exponent
  records.
- `scripts/verify_dimension_seven_conductor_lowering.py` compares their
  predicted log-squares with all \(48\) direct principal-cocycle values and
  fails if the maximum residual exceeds \(10^{-7}\).
- `tests/test_higher_dimension_sieve.py` runs the bridge as an automated
  regression test.

## 7. What to do next

The next step is no longer to search for the ray classes.  It is to recover
the exact phase of each factor:

1. evaluate the theta and eta multipliers in Kopp's samech definition for
   the six lowered strata;
2. combine them with the AFK characteristic phase;
3. produce the complete complex \(48\)-entry overlap table;
4. construct exact representatives of the associated Shintani ray units;
   and
5. test the \(7\times7\) rank-one minors over that exact field.

The absolute-value part now has no unresolved analytic identity.

## Primary sources

- G. S. Kopp, *The Shintani--Faddeev modular cocycle: Stark units from
  \(q\)-Pochhammer ratios*, Theorems 3.14, 4.46, 6.2, and 8.2,
  <https://arxiv.org/abs/2411.06763>.
- D. M. Appleby, S. T. Flammia, and G. S. Kopp,
  *A constructive approach to Zauner's conjecture via the Stark
  conjectures*, especially the principal-candidate and TCC definitions,
  <https://arxiv.org/abs/2501.03970>.
- The PARI Group, *PARI/GP documentation*,
  <https://pari.math.u-bordeaux.fr/dochtml/html-stable/>.
