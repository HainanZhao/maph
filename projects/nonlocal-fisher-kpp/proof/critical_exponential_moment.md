# Critical exponential-moment dissipation for top-hat Fisher--KPP

## Claim boundary

`PROVED`: the full nonlinear radius-one top-hat Fisher--KPP equation has two
strictly decreasing critically tilted masses. Their dissipation is an exact
positive pair-interaction integral. Consequently, any nonzero exponentially
localized state that repeats after a spatial translation has average
translation speed strictly below $2\sqrt D$, with an exact competition-delay
identity.

This constrains exact repeating hump packets. It does not rule out a front
with a nonintegrable critical tail, a stationary wake behind a separate
leading edge, or the proposed P1/P2 large-time scenarios. It does not by
itself select the wake wavelength.

## Setting

Let

\[
u_t=D u_{xx}+u(1-K*u),\qquad
K(x)=\frac12\mathbf1_{[-1,1]}(x),\qquad D>0,
\tag{1}
\]

and put $a=D^{-1/2}$. Assume $u$ is a nonzero nonnegative classical solution
on $[t_0,t_1]$ and that the integrations below are justified. In particular,
this holds for bounded compactly supported initial data at every positive
time: Hamel--Ryzhik, Theorem 1.2 (2014, DOI
`10.1088/0951-7715/27/11/2735`) supplies the global bounded classical
solution, while $u_t-Du_{xx}\le u$ and the Gaussian heat kernel give both
critical exponential moments and the required boundary decay.

Define

\[
J_\pm(t)=\int_{\mathbb R}e^{\pm ax}u(x,t)\,dx,
\qquad
\mathcal E_\pm(t)=e^{-2t}J_\pm(t).
\tag{2}
\]

## Exact dissipation theorem

For the right tilt,

\[
\mathcal E_+'(t)
=-\frac{e^{-2t}}4
\iint_{|x-y|\le1}
\left(e^{ax}+e^{ay}\right)u(x,t)u(y,t)\,dx\,dy.
\tag{3}
\]

The left-tilted identity is the reflected formula

\[
\mathcal E_-'(t)
=-\frac{e^{-2t}}4
\iint_{|x-y|\le1}
\left(e^{-ax}+e^{-ay}\right)u(x,t)u(y,t)\,dx\,dy.
\tag{4}
\]

Both derivatives are strictly negative for a nonzero solution.

To prove (3), differentiate $J_+$ and integrate the diffusion term twice by
parts. Since $Da^2=1$,

\[
J_+'=2J_+-\int e^{ax}u(x)(K*u)(x)\,dx.
\tag{5}
\]

For the top-hat kernel, symmetry in $x,y$ gives

\[
\begin{aligned}
\int e^{ax}u(x)(K*u)(x)\,dx
&=\frac12\iint_{|x-y|\le1}e^{ax}u(x)u(y)\,dx\,dy\\
&=\frac14\iint_{|x-y|\le1}
  (e^{ax}+e^{ay})u(x)u(y)\,dx\,dy.
\end{aligned}
\tag{6}
\]

Equations (5)--(6) give (3); reflection gives (4). If $u$ is nonzero and
continuous, it is positive on some interval of length less than one, so the
double integral is positive.

## Exact translation-delay corollary

Suppose that for some $T>0$ and $\lambda>0$,

\[
u(x,t_0+T)=u(x-\lambda,t_0).
\tag{7}
\]

Then $J_+(t_0+T)=e^{a\lambda}J_+(t_0)$. Dividing (5) by $J_+$ and integrating
gives

\[
\frac{\lambda}{\sqrt D}
=2T-\int_{t_0}^{t_0+T}\langle K*u\rangle_{+,t}\,dt,
\tag{8}
\]

where

\[
\langle K*u\rangle_{+,t}
=\frac{\int e^{x/\sqrt D}u(x,t)(K*u)(x,t)\,dx}
       {\int e^{x/\sqrt D}u(x,t)\,dx}>0.
\tag{9}
\]

Therefore

\[
\frac\lambda T<2\sqrt D.
\tag{10}
\]

For a left translation, the same statement follows from $\mathcal E_-$.
Equation (8), rather than the bare inequality, is the structural result: the
loss of critical front phase is exactly the time-integrated competition trace
seen under the exponentially tilted population measure.

## Consequence for the selection program

An exact periodic-shedding model that identifies the whole localized state
after one cycle with a translate moving at the pulled speed $2\sqrt D$ is
impossible: (8) has a strictly positive delay. A viable model must separate
the nonintegrable critical leading tail from the localized hump/wake state, or
retain a genuinely nonstationary competition-memory variable. This is
consistent with, but does not prove, a front that advances at pulled speed
while depositing stationary humps behind it.

The next quantitative gate is to evaluate the tilted average (9) during one
formation cycle and determine whether it becomes a universal functional of
the boundary-layer hump and the incoming moment from the frozen-barrier
theorem.

