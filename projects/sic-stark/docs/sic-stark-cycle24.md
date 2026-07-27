# SIC--Stark research cycle 24: completed dimension-four theorem

Date: 2026-07-27

## Outcome

The two finite checks from cycle 23 close.  Put

\[
\phi=\frac{1+\sqrt5}{2},\qquad \beta=\phi^2,\qquad
u=\phi+\sqrt\phi.
\]

Then the Shintani--Kopp limit formula gives

\[
\boxed{
\left(
\sqrt2\,
\frac{S_2(\beta/4\mid\beta,1)S_2(1/4\mid\beta,1)}
{S_2((\beta+1)/4\mid\beta,1)}
\right)^2=u.
}
\]

The positive branch satisfies

\[
x=\sqrt u,\qquad x+x^{-1}=\sqrt{3+\sqrt5}.
\]

Cycle 19 therefore makes all 36 dimension-four ghost minors vanish.

## 1. Fundamental units

Write \(t=\sqrt\phi\).  Then

\[
L=\mathbb Q(t),\qquad t^4-t^2-1=0,\qquad
\mathcal O_L=\mathbb Z[t].
\]

The units \(t\) and \(u=t^2+t\) are fundamental.  Indeed, a proper
overlattice of their logarithmic lattice would have a nontrivial unit
in its centered fundamental parallelogram.  The two real conjugate
absolute values of such a representative are less than

\[
\exp\left(\frac14\log\phi+\frac12\log u\right)<2,
\]

and its complex absolute value is less than
\(\exp(\frac14\log\phi)<6/5\).

For \(\alpha=a+bt+ct^2+dt^3\), adding and subtracting its values at
\(t,-t,i/t,-i/t\) puts \(a,b,c,d\) in a finite integer box.  Exact
reduction by \(t^4=t^2+1\) and
\(N_{L/\mathbb Q}(\alpha)=\pm1\) leaves only \(\alpha=\pm1\) in the
centered cell.  Hence

\[
\mathcal O_L^\times=\{\pm t^m u^n:m,n\in\mathbb Z\},
\qquad R_L=\log\phi\,\log u.
\]

## 2. Relative \(L\)-derivative

Cycles 22--23 give

\[
h_K=h_L=1,\quad w_K=w_L=2,\quad R_K=\log\phi.
\]

For the quadratic character of \(L/K\),

\[
L(s,\chi)=\frac{\zeta_L(s)}{\zeta_K(s)}.
\]

The analytic class-number formula at zero now gives

\[
\boxed{L'(0,\chi)=\log u.}
\]

## 3. Normalization

The primitive quarter characteristic has denominator ideal \((4)\).
Exact residue enumeration gives ray-group orders

\[
|\operatorname{Cl}_{(4)\infty_2}(K)|=2,\qquad
|\operatorname{Cl}_{(4)\infty_1\infty_2}(K)|=4.
\]

The quotient map has fibers of order two, so Kopp's exponent is

\[
n=\frac2{|\text{fiber}|}=1.
\]

The generalized zeta derivative is the difference of the two
one-infinite-place partial zetas:

\[
Z'(0,A_0)
=\zeta'(0,A_0)-\zeta'(0,A_1)
=L'(0,\chi).
\]

Kopp's normalized positive cocycle occurs squared.  Consequently

\[
x^2=\exp Z'(0,A_0)=\exp L'(0,\chi)=u.
\]

## 4. Dimension-four TCC

Since \(u+u^{-1}=1+\sqrt5\),

\[
(x+x^{-1})^2=u+u^{-1}+2=3+\sqrt5.
\]

Positivity gives \(x+x^{-1}=\sqrt{3+\sqrt5}\).  Every ghost minor
belongs to the ideal

\[
(x^2-\sqrt{3+\sqrt5}\,x+1)
\]

by cycle 19, so all minors vanish.  The shifted ghost matrix has rank
one and TCC holds.

## Theorem

Assuming the published principal-ghost formula and the proved
Shintani--Kopp Kronecker-limit theorem with their stated conventions,
the canonical dimension-four ghost is a rank-one projector and
satisfies TCC exactly.  No Stark conjecture is assumed.

## Sources

- G. Kopp, *The Shintani--Faddeev modular cocycle*,
  [Theorem 1.1](https://arxiv.org/abs/2411.06763).
- T. Shintani, *On a Kronecker limit formula for real quadratic
  fields*, J. Fac. Sci. Univ. Tokyo 24 (1977), 167--199.
- S. Flammia et al., [`Zauner.jl`](https://github.com/sflammia/Zauner.jl).
