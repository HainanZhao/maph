# SIC--Stark research cycle 23: the relative class-number route

Date: 2026-07-27

## Outcome

The remaining Stark evaluation can be attacked through an ordinary
Dedekind-zeta quotient rather than through direct double-sine
manipulation.

Let

\[
K=\mathbb Q(\sqrt5),\qquad
L=K(\sqrt\phi),\qquad
u=\phi+\sqrt\phi.
\]

For the nontrivial quadratic character \(\chi\) of \(L/K\),

\[
\boxed{L(s,\chi)=\frac{\zeta_L(s)}{\zeta_K(s)}.}
\]

The analytic class-number formula at \(s=0\) reduces
\(L'(0,\chi)\) to a class-number and regulator calculation.  The class
number is forced to be one by a very small Minkowski bound.  The
remaining checks are the index of the visible units and the precise
partial-zeta normalization in Kopp's theorem.

> **Cycle-24 completion.** Both checks pass.  The fundamental units are
> \(\sqrt\phi\) and \(\phi+\sqrt\phi\), and Kopp's exponent is \(n=1\).

## 1. Discriminant and class number

Cycle 22 gives

\[
\mathfrak d_{L/K}=(4).
\]

Therefore

\[
|D_L|
=|D_K|^{[L:K]}N_{K/\mathbb Q}(\mathfrak d_{L/K})
=5^2\cdot16
=400.
\]

The signature of \(L\) is \((r_1,r_2)=(2,1)\).  Its degree-four
Minkowski ideal-class bound is

\[
\frac{4!}{4^4}\left(\frac4\pi\right)^{r_2}\sqrt{|D_L|}
=\frac{15}{2\pi}
<2.4.
\]

Thus every ideal class contains an integral ideal of norm \(1\) or
\(2\).  But \(2\) is inert in \(K\) and ramified in \(L/K\), so the
prime above \(2\) in \(L\) has norm \(4\); there is no ideal of norm
\(2\).  Hence

\[
\boxed{h_L=1.}
\]

## 2. Visible regulator

The two explicit independent units are

\[
\sqrt\phi,\qquad u=\phi+\sqrt\phi.
\]

At the two real embeddings of \(L\),

\[
\begin{array}{c|cc}
 & \sigma_1 & \sigma_2\\ \hline
\sqrt\phi & \sqrt\phi & \sqrt\phi\\
u & u & u^{-1}.
\end{array}
\]

At the complex place, \(|u|=1\) and
\(|\sqrt{\phi'}|=\phi^{-1/2}\).
The logarithmic determinant of these visible units is therefore

\[
\boxed{R_{\mathrm{vis}}=\log\phi\,\log u.}
\]

If \(\langle\sqrt\phi,u\rangle\) has index one in the free part of
\(\mathcal O_L^\times\), then

\[
R_L=\log\phi\,\log u.
\]

Since \(h_K=h_L=1\), \(w_K=w_L=2\), and \(R_K=\log\phi\), the
class-number formula gives

\[
\boxed{L'(0,\chi)=\log u.}
\]

This is exactly the logarithm required by the Stark unit, up to the
factor conventions relating the character \(L\)-function, partial
zeta difference, Kopp's exponent \(n\), and the cocycle square.

## 3. Remaining finite checks

Two finite checks now replace the open-ended special-function problem:

1. **Unit index.** Prove that \(\sqrt\phi\) and \(u\) generate the free unit
   group of \(L\).  Equivalently, rule out a smaller relative unit whose
   power is \(u\).
2. **Normalization.** Track the nontrivial ray character through
   \[
   L(s,\chi)=\zeta(s,A_0)-\zeta(s,A_1)
   \]
   and Kopp's Theorem 1.1, including its exponent \(n\) and cocycle
   square, to determine whether the selected invariant is \(u\),
   \(u^{-1}\), or a square.

Positivity and the numerical value \(x>1\) will select \(u\) once those
factors are fixed.

## Claim ledger

Proved exactly:

- \(D_L=400\);
- \(h_L=1\) by Minkowski's bound;
- the visible regulator is \(\log\phi\log u\);
- unit index one would give \(L'(0,\chi)=\log u\).

Closed in cycle 24:

- the unit index;
- the exact partial-zeta/cocycle normalization;
- consequently, the unconditional analytic identity.

## Sources

- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [arXiv:2411.06763](https://arxiv.org/abs/2411.06763).
- S. Yamamoto, *Kronecker limit formula for real quadratic fields and
  Shintani invariant*,
  [RIMS B4](https://www.kurims.kyoto-u.ac.jp/~kenkyubu/bessatsu/open/B4/pdf/B04_004.pdf).
