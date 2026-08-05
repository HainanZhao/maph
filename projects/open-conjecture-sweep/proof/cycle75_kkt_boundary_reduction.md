# C75 exact \(d=4\) extremizer reduction

## Claim boundary

**CONTAINED / NO NOVELTY CLAIM.** A post-work primary-source audit found
Zhang, arXiv:2605.05243v1, Theorem 2, which proves the full
Holevo--Utkin conjecture for all \(d\ge4\). This document is consequently
an unsealed overlapping reconstruction only. Do not cite it as a project
proof, scoped theorem, or paper result; its retained purpose is to document
the eligibility failure and allow comparison with the prior proof.

**PROVED.** This document gives a complete reduction of the \(d=4\) target
to three explicit one-variable families and the two-coordinate endpoint. It
does **not** establish the required global inequalities for those families,
and hence does not prove the Holevo--Utkin conjecture.

Let
\[
 S=\{x\in\mathbb R^4:\sum_i x_i=0,\ \sum_i x_i^2=1\},
 \qquad F_\alpha(x)=\sum_i|x_i|^{2\alpha}.
\]

## Reduction theorem

For \(0<\alpha\leq\tfrac12\),
\[
 F_\alpha(x)\geq2^{1-\alpha}\quad(x\in S),
\]
with equality exactly at permutations and total sign changes of
\((2^{-1/2},-2^{-1/2},0,0)\).

For \(\alpha\in(\tfrac12,1)\cup(1,\infty)\), every global minimizer
(when \(\alpha<1\)) or global maximizer (when \(\alpha>1\)) is, up to
permutation and total sign, either the two-coordinate vector above or one of
the following families with \(r>0\):
\[
 \begin{aligned}
 E_3(r)&=\frac{(1+r,-1,-r,0)}{\sqrt{2(r^2+r+1)}},\\
 E_{13}(r)&=\frac{(2+r,-1,-1,-r)}{\sqrt{2(r^2+2r+3)}},\\
 E_{22}(r)&=\frac{((1+r)/2,(1+r)/2,-1,-r)}
 {\sqrt{(3+2r+3r^2)/2}}.
 \end{aligned}
\]
Their objective functions are respectively
\[
 \begin{aligned}
 f_3(r)&=\frac{(1+r)^{2\alpha}+1+r^{2\alpha}}
 {[2(r^2+r+1)]^\alpha},\\
 f_{13}(r)&=\frac{(2+r)^{2\alpha}+2+r^{2\alpha}}
 {[2(r^2+2r+3)]^\alpha},\\
 f_{22}(r)&=\frac{2((1+r)/2)^{2\alpha}+1+r^{2\alpha}}
 {[(3+2r+3r^2)/2]^\alpha}.
 \end{aligned}
\]
The endpoint has value \(A_\alpha=2^{1-\alpha}\). Thus these four
explicit comparisons are necessary and sufficient for the full \(d=4\)
conjecture (with \(\alpha=1\) the identity \(F_1=1\)).

## Proof

Write the positive nonzero coordinates as \(a_i\), the negative ones as
\(-b_j\), and put \(T=\sum a_i=\sum b_j\). For \(p=2\alpha\leq1\),
subadditivity gives
\[
 F_\alpha=\sum a_i^p+\sum b_j^p\geq2T^p.
\]
Moreover \(1=\sum a_i^2+\sum b_j^2\leq2T^2\), so
\(F_\alpha\geq2^{1-p/2}=2^{1-\alpha}\). The equality conditions in the
two displayed inequalities force one positive and one negative coordinate,
both of magnitude \(2^{-1/2}\). This proves the first assertion, including
the nonsmooth range.

Now let \(p=2\alpha>1\), \(\alpha\ne1\), and take a global extremizer.
Compactness of \(S\) supplies one. On its nonzero support the two constraint
gradients are independent, so Lagrange multipliers give
\[
 h(t):=p\,\operatorname{sgn}(t)|t|^{p-1}-2\lambda t-\mu=0. \tag{1}
\]
If \(\lambda\leq0\), \(h\) is strictly increasing. If \(\lambda>0\),
\[
 h'(t)=p(p-1)|t|^{p-2}-2\lambda\qquad(t\ne0).
\]
For \(p>2\), its signs are \(+,-,+\) on the three intervals cut by
\(-r,r\); for \(1<p<2\), they are \(-,+,-\). (For \(p=2\), \(h\) is
affine.) The middle interval is strictly monotone even when the derivative
is unbounded at zero. Hence (1) has at most three nonzero roots: otherwise
the indicated monotonicity intervals, or Rolle's theorem away from zero,
would force a fourth change. This is the needed root-count lemma.

A support of size two has opposite, equal coordinates and is the endpoint.
A support of size three has signs \((+,-,-)\) after total sign change; write
the negative magnitudes as \(b,rb\). Zero sum and normalization give
\(E_3(r)\). At support four the sign partition is either \(1+3\) or
\(2+2\). Four distinct signed coordinate values would contradict the
root-count lemma. In the \(1+3\) case two of the three equal-sign coordinates
therefore agree, giving \((2+r,-1,-1,-r)\) after scaling. In the \(2+2\)
case a repeated root must occur within one sign class; after total sign change
it gives \(((1+r)/2,(1+r)/2,-1,-r)\). Normalization yields the displayed
families. Direct substitution gives their formulas, independently checked by
the replay below. These cases exhaust all supports and signs.

## Exact parameter anchor: \(\alpha=2\)

**PROVED.** At \(\alpha=2\),
\[
 \max_{x\in S}\sum_i x_i^4=\frac7{12}=B_2,
\]
with equality exactly at permutations and total sign changes of
\((3,-1,-1,-1)/\sqrt{12}\).

Indeed, if \(e_4=x_1x_2x_3x_4\), Newton's identities with
\(\sum_i x_i=0\) and \(\sum_i x_i^2=1\) give
\[
 \sum_i x_i^4=\frac12-4e_4. \tag{2}
\]
When there are two positive and two negative coordinates, \(e_4\ge0\).
Otherwise, after total sign change write the coordinates as
\(a,-b,-c,-d\), where \(a=b+c+d\). AM--GM and normalization give
\[
 abcd\leq a(a/3)^3=\frac{a^4}{27},
 \qquad
 1=a^2+b^2+c^2+d^2\geq\frac43a^2.
\]
Therefore \(abcd\leq1/48\), so always \(e_4\geq-1/48\).
Equation (2) yields the asserted bound. Equality forces
\(b=c=d=a/3\) and \(a^2=3/4\), exactly the stated family.

## Two closed profile strata

**PROVED.** Put
\[
 A_\alpha=2^{1-\alpha},quad
 B_\alpha=4^{-\alpha}(3^\alpha+3^{1-\alpha}),quad
 C_\alpha=\frac{4^\alpha+2}{6^\alpha}.
\]
For every \(r>0\),
\[
 \begin{array}{ll}
 f_3(r),f_{22}(r)\ge A_\alpha,&\tfrac12<\alpha<1,\\
 f_3(r),f_{22}(r)\le\max(A_\alpha,B_\alpha),&\alpha>1.
 \end{array} \tag{3}
\]

Both profiles are invariant under \(r\mapsto1/r\), so take \(0<r\le1\)
and put \(s=2\alpha-1\). Direct logarithmic differentiation gives the
sign of \((\log f_3)'\) as the sign of
\[
 E_s(r)=(1-r)(1+r)^s+(r+2)r^s-(2r+1). \tag{4}
\]
As a function of \(s\), (4) is strictly convex, has
\(E_1=E_3=0\), and
\[
 \left.\partial_sE_s(r)\right|_{s=1}
 =(1-r^2)\log(1+r)+r(r+2)\log r<0. \tag{5}
\]
For (5), use \(\log(1+r)<r\) and
\(-\log r\ge2(1-r)/(1+r)\ge(1-r^2)/(r+2)\).
Convexity now gives \(E_s>0\) for \(0<s<1\), \(E_s<0\) for
\(1<s<3\), and \(E_s>0\) for \(s>3\). Consequently \(f_3\) runs
monotonically from \(A_\alpha\) to \(C_\alpha\), increasing for
\(\tfrac12<\alpha<1\), decreasing for \(1<\alpha<2\), constant for
\(\alpha=2\), and increasing for \(\alpha>2\).

Similarly, the sign of \((\log f_{22})'\) is the sign of
\[
 H_s(r)=2\left(\frac{1+r}{2}\right)^s(1-r)
 +(3+r)r^s-(1+3r). \tag{6}
\]
Here \(H_1=0\) and \(H_s\) is strictly decreasing in \(s\), since both
bases in (6) lie strictly between zero and one. Thus \(f_{22}\) increases
from \(C_\alpha\) when \(\alpha<1\), and decreases from
\(C_\alpha\) when \(\alpha>1\).

It remains only to compare endpoints. After multiplication by \(6^\alpha\),
the assertion \(C_\alpha\ge A_\alpha\) is
\[
 L(\alpha):=4^\alpha+2-2\,3^\alpha\ge0.
\]
It holds on \((\tfrac12,1)\) because \(L(1)=0\) and \(L'<0\) there.
On \([1,2]\), \(L\) is strictly convex with \(L(1)=L(2)=0\), giving
\(C_\alpha\le A_\alpha\). For \(\alpha\ge2\), the sign of
\(B_\alpha-C_\alpha\), after positive clearing of denominators, is that
of
\[
 18^\alpha+3\,2^\alpha-16^\alpha-2\,4^\alpha\ge0.
\]
After division by \(16^\alpha\), move the last two decaying terms to the
right: the left side \((9/8)^\alpha-1\) increases, the right side
\(2/4^\alpha-3/8^\alpha\) decreases, and the inequality holds at
\(\alpha=2\). This proves (3).

The only unresolved profile is \(f_{13}\). Its derivative has extra
interior critical points for part of the parameter range, so (3) must not be
misread as an endpoint argument for that remaining family.

## The \(1+3\) profile below \(\alpha=1\)

**PROVED.** For \(0<\alpha<1\) and every \(r>0\),
\[
 f_{13}(r)\ge A_\alpha. \tag{7}
\]
Put \(Q=r^2+2r+3\) and
\[
 N_\alpha=(r+2)^{2\alpha}+r^{2\alpha}+2,qquad
 g(\alpha)=\log N_\alpha-\log2-\alpha\log Q.
\]
Then (7) is \(g(\alpha)\ge0\). The function \(g\) is convex,
\(g(1)=0\), and
\[
 g'(1)=-\frac{G(r)}{2Q},qquad
 G(r)=2Q\log Q-(r+2)^2\log(r+2)^2-r^2\log r^2. \tag{8}
\]
It is enough to prove \(G(r)>0\).

Let \(r_0=\sqrt2-1\). For \(0<r\le r_0\), write
\(a=r^2\), \(b=(r+2)^2\), and \(S=a+b=2Q-2\). Since
\(Q\le4\), convexity of \(t\log t\) gives
\[
 a\log a+b\log b\le S\log S,
\]
and hence
\[
 G(r)\ge F(Q):=2Q\log Q-(2Q-2)\log(2Q-2).
\]
On \([3,4]\), \(F'(Q)=2\log(Q/(2Q-2))<0\), so
\[
 F(Q)\ge F(4)=\log(1024/729)>0. \tag{9}
\]

For \(r\ge r_0\), set \(H=G'/4\). Direct differentiation gives
\[
 H=(r+1)\log Q-r\log r-(r+2)\log(r+2),
\]
and, with \(t=r(r+2)\),
\[
 H'=k(t):=\log(1+3/t)-\frac4{t+3},qquad
 k'(t)=\frac{t-9}{t(t+3)^2}. \tag{10}
\]
Here \(k(1)=\log4-1>0\), \(k(9)=\log(4/3)-1/3<0\), and
\(k(t)\to0\) from below. Thus \(H\) first increases and then decreases
to zero. At \(r_0\),
\[
 H(r_0)=\sqrt2\log4-2\log(1+\sqrt2)>0.
\]
For example, \(2^{\sqrt2}>2^{7/5}>1+\sqrt2\): raise the last comparison
to the fifth power, use \(\sqrt2<3/2\), and compare
\((1+\sqrt2)^5=41+29\sqrt2<85<128=2^7\).
Hence \(H>0\) on this whole ray, so \(G\) increases there. Together with
(9), this proves \(G>0\). Convexity now gives
\(g(\alpha)\ge g(1)+g'(1)(\alpha-1)>0\) for \(0<\alpha<1\).

## Residual \(\alpha>1\) compression

**PROVED reduction; CONJECTURED baseline.** Let
\[
 p(r)=\frac{((r+2)^2,1,1,r^2)}{2Q},quad
 A=(1/2,1/2,0,0),quad B=(3/4,1/12,1/12,1/12),
\]
and write \(\mathcal C_x(t)=\sum_i(x_i-t)_+\). Direct sorting gives one
strict negative-to-positive crossing of
\(\mathcal C_{p(r)}-\mathcal C_A\), at \(t=1-U\), and one strict
positive-to-negative crossing of
\(\mathcal C_{p(r)}-\mathcal C_B\), where
\[
 U=\frac{(r+2)^2}{2Q},qquad
 t_B=\begin{cases}1/8-r^2/(4Q),&0<r\le1,\\
 1/4-1/Q,&r\ge1.
 \end{cases} \tag{11}
\]
For equal-mass probability vectors and \(\alpha>1\),
\[
\sum_i p_i^\alpha-\sum_i q_i^\alpha
=\alpha(\alpha-1)\int_0^\infty
[\mathcal C_p(t)-\mathcal C_q(t)]t^{\alpha-2}\,dt. \tag{12}
\]

The candidate switch is also **PROVED** to be unique. Indeed,
\[
 \frac{B_\alpha}{A_\alpha}
 =\frac12\left((3/2)^\alpha+3(1/6)^\alpha\right)=:R(\alpha)
\]
is strictly convex, \(R(1)=1\), \(R'(1)=\tfrac12\log3-\log2<0\), and
\(R(2)=7/6>1\). Hence, besides \(1\), it has exactly one root
\(\alpha_*\in(1,2)\) of \(A_\alpha=B_\alpha\).

The one-crossing rule applied to (12) means that the single baseline
\[
 N_{\alpha_*}\le2Q^{\alpha_*}\quad(r>0) \tag{13}
\]
would imply every remaining \(\alpha>1\) comparison: the \(A\) bound
below \(\alpha_*\), and the \(B\) bound above it. Equation (13) is the
remaining C75 proof obligation. It must not be replaced by a numerical check.

## Closure of the crossover baseline

**PROVED.** Equation (13) holds. Let \(a=\alpha_*\), \(p=2a\), and
\(s=p-1\). First,
\[
 \frac54<a<\frac32,qquad \frac32<s<2. \tag{14}
\]
For \(R(a)=\tfrac12((3/2)^a+3(1/6)^a)\), the defining equation is
\(R(a)=1\). The bounds in (14) follow directly from
\[
 (3/2)^{5/4}+3(1/6)^{5/4}<\frac53+\frac{25}{77}<2
\]
and
\[
 (3/2)^{3/2}+3(1/6)^{3/2}>\frac95+\frac15=2.
\]
For the first line, put \(t=(3/2)^{1/4}\), use
\(11/10<t<10/9\) and \(7/5<\sqrt2<3/2\). For the second, use
\(\sqrt{3/2}>6/5\) and \(\sqrt6<5/2\).

With \(x=r+1>1\), (13) is equivalent to
\[
 (x+1)^p+(x-1)^p+2\le2(x^2+2)^a. \tag{15}
\]
Define the normalized ratio
\[
 F(x)=\frac{(x+1)^p+(x-1)^p+2}{(x^2+2)^a}.
\]
Direct differentiation yields
\[
 F'(x)=\frac{pD(x)}{(x^2+2)^{a+1}},qquad
 D(x)=(2-x)(x+1)^s+(x+2)(x-1)^s-2x. \tag{16}
\]
The function \(D\) is strictly convex. Indeed, putting
\(\delta=2-s\in(0,1)\) and \(C=s+1=3-\delta\), differentiation twice
gives
\[
 \frac{D''(x)}s=
 \frac{Cx-2\delta}{(x-1)^\delta}
 -\frac{Cx+2\delta}{(x+1)^\delta}. \tag{17}
\]
Both numerators are positive. Thus (17) is positive precisely when
\[
 \delta\operatorname{artanh}(1/x)>
 \operatorname{artanh}\left(\frac{2\delta}{C x}\right).
\]
Since \(0<2\delta/C<\delta<1\), monotonicity and convexity of
\(\operatorname{artanh}\), with value zero at zero, prove this strictly.

Moreover,
\[
 D(2)=0,qquad D'(2)=4s-1-3^s<0. \tag{18}
\]
For the latter set \(J(s)=3^s-4s+1\). Then
\(J(3/2)=3\sqrt3-5>0\) and
\(J'(s)=3^s\log3-4>0\) for \(s\ge3/2\). Strict convexity, (18), and
\[
 D(x)=2(2-s)x^s-2x+O(x^{s-1})\longrightarrow+\infty
\]
show that \(D>0\) before \(2\), then is negative until one later zero,
and is positive thereafter. Hence \(F\) rises to \(x=2\), falls, and then
rises to \(\lim_{x\to\infty}F(x)=2\). Finally the crossover equation,
multiplied by \(6^a\), says \(3^{2a}+3=2\,6^a\), so \(F(2)=2\).
This proves (15), with equality only at the finite point \(x=2\).

## Full \(d=4\) theorem

**PROVED.** For every \(\alpha>0\), the Holevo--Utkin claimed extremum in
dimension four is correct. On \(S\), the minimum for \(0<\alpha<1\) and
the maximum for \(\alpha>1\) of \(F_\alpha\) is respectively
\[
 \min(A_\alpha,B_\alpha),qquad\max(A_\alpha,B_\alpha).
\]
Here \(A_\alpha) is the active value below the unique switch
\(\alpha_*\), and \(B_\alpha\) above it; at \(\alpha=1\),
\(F_1=1\). The reduction theorem exhausts all extremizers, the first
profile section proves the endpoint and \(E_3,E_{22}\) comparisons, (7)
proves the remaining profile below one, and (11)--(13) plus (15) propagate
the crossover bound across every exponent above one. The equality families
are exactly the two source-proposed families, with both available at the
switch.

## Replay

Run `python3 proof/verify_cycle75_kkt_boundary_reduction.py`. It checks the
zero-sum and unit-norm normalizations, objective formulas at several exact
exponents, and endpoint controls using rational arithmetic. The calculus and
root-count argument above, not finite sampling, proves coverage.
