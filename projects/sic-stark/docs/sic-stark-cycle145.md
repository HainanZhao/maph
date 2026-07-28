# SIC--Stark research cycle 145': dimensions five and four calibration

Date: 2026-07-28

## Decisive branch verdict

\[
\boxed{\text{branch (a): dimension five lands on the closed locus}}
\]

For

\[
 \beta_5=2+\sqrt3,\qquad
 A_5=\begin{pmatrix}56&-15\\15&-4\end{pmatrix},
\]

the two fusion conditions are

\[
 A_5\beta_5=\beta_5,\qquad
 \beta_5+\beta_5^{-1}=4.
\]

Thus both the general-lens pair and the standard modular-double pair
fuse at the arithmetic boundary.

The exact parameters are

\[
 (p,k,r,s)=(-56,15,4,15),\qquad
 \omega_1=15\tau-4.
\]

For finite frequency \((p_a,p_b)\), the two bibasic classes are

\[
 \alpha_z
 =\frac{3\tau-1}{2}(3p_b-4p_a+10)
  +\frac52(3\tau-1)z,
\qquad
 N_z=p_a-1-5z.
\]

At fusion their term ratio becomes

\[
 q\,
 \frac{(1-x)(1-w^{-1}x)}
 {(1-qx)(1-qw^{-1}x)}.
\]

Equivalently the fused bilateral packet is

\[
 {}_2\psi_2(x,w^{-1}x;qx,qw^{-1}x;q,q).
\]

The transcript bit is
\[
 k_{\rm lens}=15,\qquad
 \text{alias parity period}=2,\qquad
 \text{fusion sign bit}=0.
\]

The argument is \(+q\). In dimension six the corresponding argument is
\(-q\). This proves the summability dichotomy at the level of the exact
fusion ratio: the already proved dimension lies on the positive
closed locus, while dimension six is its sign-reflected neighbor.

## Arb results

At the same three lens-axis parameters \(t=20,10,5\):

\[
 \text{direct/factorized continuations}=3/3,
\qquad
 \text{bibasic alias classes}=6/6.
\]

The independent boundary calculation gives

\[
 x_5^2=3.8908617139430792553376439596\ldots,
\]

and the double-sine ball contains the isolated algebraic root. Hence
the two-base mechanism is calibrated against a proved, unconditional
packet rather than only against itself.

## Dimension-four even-wrap control

For dimension four,

\[
 A_4=\begin{pmatrix}21&-8\\8&-3\end{pmatrix},
\qquad
 \beta_4+\beta_4^{-1}=3.
\]

The direct/factorized comparisons pass at three interior points, as
does the single bibasic alias class. The modulus ledger is:

\[
 \boxed{k_{\rm lens}=8,\qquad k_{\rm phase}=2k=16.}
\]

Level \(24\) is the dimension-six lens modulus and is not the
dimension-four even-wrap level.

Exact fusion-exponent reduction also gives
\[
 -q\frac{(1-x)(1-ix)}{(1+qx)(1+iqx)}.
\]
Thus the pre-registered dimension-four prediction is confirmed: its
bilateral argument is \(-q\).

## Reproduction

```bash
PYTHONPATH=scripts python \
  scripts/dimension_five_two_base_calibration.py

PYTHONPATH=scripts python \
  scripts/dimension_four_two_base_calibration.py
```
