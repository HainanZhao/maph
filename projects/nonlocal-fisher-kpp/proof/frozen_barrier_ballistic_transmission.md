# Frozen-barrier ballistic transmission theorem

## Claim boundary

`PROVED`: the
linearized Fisher--KPP leading edge behind a fixed competition barrier is
controlled on its critical ballistic ray by a drift-two survival factor, not
by the zero-energy scattering length.

The theorem below concerns a frozen linear potential. It does not prove that
the nonlinear top-hat trace freezes during hump formation, that an incoming
seed has a universal shape, or that the nonlinear PDE selects a wavelength.

`RECOGNIZED`: Simon's Theorem 1.1 in *A Feynman--Kac Formula for Unbounded
Semigroups* (1999, arXiv `math-ph/9907022`) gives the Brownian-bridge kernel
formula used in (8), with the harmless factor-two time rescaling between its
generator $\tfrac12\partial_{xx}$ and the present $\partial_{xx}$. The
bounded nonnegative potential here satisfies its hypotheses. The ballistic
ratio limit (5) was not found in the bounded literature search and is derived
below; no priority claim is made.

## Theorem candidate

Let $C:\mathbb R\to[0,\infty)$ be bounded and continuous. Assume that for
some $A,\gamma>0$,

\[
C(x)\le A e^{-\gamma x}\qquad (x\ge0).
\tag{1}
\]

Let $q$ solve

\[
q_t=q_{xx}+(1-C(x))q,qquad q(0,x)=q_0(x),
\tag{2}
\]

where $q_0$ is bounded, continuous, nonnegative, integrable, and has finite
exponential moment

\[
\int_{\mathbb R}e^yq_0(y)\,dy<\infty.
\]

Define

\[
H_C(y)=\mathbb E_y\exp\left{-\int_0^\infty C(Y_r)\,dr\right},
\qquad
Y_r=y+2r+\sqrt2 W_r.
\tag{3}
\]

Then $0<H_C\le1$, $H_C(+\infty)=1$, and $H_C$ is the bounded positive
solution of

\[
H_C''+2H_C'-C H_C=0.
\tag{4}
\]

For every fixed $s\in\mathbb R$,

\[
\lim_{t\to\infty}\sqrt{4\pi t}\,e^s q(t,2t+s)
=\int_{\mathbb R}e^yH_C(y)q_0(y)\,dy.
\tag{5}
\]

Moreover, with $\phi_C=e^xH_C$,

\[
\phi_C''+(1-C)\phi_C=2\phi_C
\tag{6}
\]

and, whenever the integrals and boundary terms are justified,

\[
e^{-2t}\int_{\mathbb R}\phi_C(x)q(t,x)\,dx
=\int_{\mathbb R}\phi_C(x)q_0(x)\,dx.
\tag{7}
\]

Thus the right side of (5) is also an exact generalized exponential moment.

## Route A: Brownian-bridge proof

Write $p_C(t;y,x)$ for the heat kernel of $\partial_{xx}-C$. The
Feynman--Kac bridge formula gives

\[
\frac{p_C(t;y,x)}{p_0(t;y,x)}
=\mathbb E_{y\to x}^{\,t}
 \exp\left{-\int_0^t C(B_r)\,dr\right}.
\tag{8}
\]

Take $x=2t+s$. On every fixed time interval $[0,T]$, the bridge has the
representation in law

\[
B_r=y+\frac r t(2t+s-y)
 +\sqrt2\left(W_r-\frac r tW_t\right),
\tag{9}
\]

and converges uniformly in distribution to $Y_r=y+2r+\sqrt2W_r$.
Consequently the expectation in (8), truncated at $T$, converges to the
corresponding drift-two expectation.

It remains to remove the truncation. Fix $y$ and choose $R_0\ge|y|$; also
fix $s$. For
$t\ge2(|s|+R_0+1)$, the mean of the bridge at time $r$ is

\[
\mu_{t,r}=y+\left(2+\frac{s-y}{t}\right)r
\ge -R_0+\frac32r.
\]

Its variance is $2r(1-r/t)\le2r$. If
$r\ge4R_0+1$, then $\mu_{t,r}-r/2\ge3r/4$, and the elementary Gaussian
tail bound gives

\[
\mathbb P(B_r\le r/2)\le e^{-9r/64}.
\]

On the complementary event, (1) gives
$C(B_r)\le A e^{-\gamma r/2}$. Hence, uniformly in
$y\in[-R_0,R_0]$ and all sufficiently large $t$,

\[
\mathbb E_{y\to2t+s}^{\,t}C(B_r)
\le \|C\|_\infty e^{-9r/64}+Ae^{-\gamma r/2}.
\]

The same estimate, with an improved mean, holds for the drift-two process
$Y_r$. Integrating this bound proves

\[
\lim_{T\to\infty}\sup_{t\ge2T}
\mathbb E_{y\to 2t+s}^{\,t}
 \int_T^t C(B_r)\,dr=0.
\tag{10}
\]

Using $|e^{-a}-e^{-b}|\le|a-b|$ for $a,b\ge0$, (8)--(10) yield

\[
\frac{p_C(t;y,2t+s)}{p_0(t;y,2t+s)}\longrightarrow H_C(y).
\tag{11}
\]

The free kernel satisfies the exact identity

\[
\sqrt{4\pi t}\,e^{s+t}p_0(t;y,2t+s)
=\exp\left{y-\frac{(s-y)^2}{4t}\right}.
\tag{12}
\]

Since the bridge factor lies in $[0,1]$, the integrand obtained after using
(12) is bounded by $e^yq_0(y)$. The assumed exponential moment therefore
gives dominated convergence in the Feynman--Kac representation of (2) and
proves (5). The drift-two process tends to $+\infty$ almost surely, and the same
tail bound makes the integral in (3) finite. Starting farther to the right
makes its expected occupation of every fixed left half-line tend to zero,
while (1) controls the right tail, so $H_C(+\infty)=1$. The
infinite-horizon Feynman--Kac formula and the Markov property give (4);
standard one-dimensional elliptic regularity makes the equation classical
under the stated continuity assumption. If two bounded solutions of (4)
have the same limit at $+\infty$, their difference $g$ obeys, for every
$T>0$,

\[
g(y)=\mathbb E_y\left[
 e^{-\int_0^T C(Y_r)\,dr}g(Y_T)
\right].
\]

Since $Y_T\to+\infty$ almost surely and $g$ is bounded, dominated convergence
gives $g=0$. This proves uniqueness.

## Route B: generalized-moment audit

Equation (4) and $\phi_C=e^xH_C$ give (6) by direct differentiation. For a
smooth rapidly decaying solution, differentiate the left side of (7),
integrate the $q_{xx}$ term twice by parts, and use (6):

\[
\frac d{dt}\int\phi_Cq
=\int\bigl(\phi_C''+(1-C)\phi_C\bigr)q
=2\int\phi_Cq.
\]

This proves (7) independently of the bridge limit and fixes the spectral
parameter sampled by the critical ray.

## Exact step benchmark

For $C(x)=3\mathbf1_{(-\infty,0)}(x)$, equation (4) has the explicit bounded
solution

\[
H_C(x)=
\begin{cases}
\frac23e^x,&x<0,\\[2mm]
1-\frac13e^{-2x},&x\ge0.
\end{cases}
\tag{13}
\]

Both $H_C$ and $H_C'$ match at zero. The ballistic transmission at the
interface is $H_C(0)=2/3$. By contrast, the left-normalized zero-energy
solution of $\psi''=C\psi$ is

\[
\psi(x)=
\begin{cases}
e^{\sqrt3x},&x<0,\\
1+\sqrt3x,&x\ge0,
\end{cases}
\]

whose extrapolated zero is $-1/\sqrt3$. These are different spectral
observables; the zero-energy intercept cannot substitute for the ballistic
transmission factor.

## Remaining proof obligations

1. Prove or falsify a controlled replacement of the evolving trace $K*u$ by
   the frozen profile $C_L$ over one formation event.
