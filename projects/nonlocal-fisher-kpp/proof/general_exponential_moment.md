# General exponential-moment dissipation

## Claim boundary

`PROVED`: let (D>0), let (K\in L^1(\mathbb R)) be even and nonnegative,
and let (u\ge0) be a classical solution of

\[
u_t=D u_{xx}+u(1-K*u)
\]

for which the weighted integrations below are justified. For every real
(a) with finite weighted mass,

\[
\mathcal E_a(t)=e^{-(1+Da^2)t}\int e^{ax}u(x,t)\,dx
\]

satisfies

\[
\mathcal E_a'(t)
=-\frac{e^{-(1+Da^2)t}}2
\iint K(x-y)(e^{ax}+e^{ay})u(x,t)u(y,t)\,dx\,dy.
\]

Consequently, if (a>0) and a nonzero finite-(a)-moment state repeats after
time (T) translated right by (\lambda), then

\[
\frac{\lambda}{T}
=Da+\frac1a-\frac1{aT}\int_{t_0}^{t_0+T}
\langle K*u\rangle_{a,t}\,dt.
\]

When the interaction integral is positive, this speed is strictly smaller
than (Da+a^{-1}). At (a=D^{-1/2}) it is strictly smaller than the pulled
speed (2\sqrt D).

The claim assumes the needed regularity and weighted integrability. It does
not assert those hypotheses for every kernel or initial datum. It does not
exclude a front with divergent critical moment, and it does not select a wake
wavelength.

## Proof

Put (J_a=\int e^{ax}u\). Twice integrating the diffusion term by parts gives

\[
J_a'=(1+Da^2)J_a-\int e^{ax}u(x)(K*u)(x)\,dx.
\]

Writing the last term as a double integral and exchanging (x,y), evenness
of (K) gives

\[
\int e^{ax}u(x)(K*u)(x)\,dx
=\frac12\iint K(x-y)(e^{ax}+e^{ay})u(x)u(y)\,dx\,dy.
\]

Differentiation of the normalizing exponential proves the dissipation
identity. Nonnegativity of (K,u) proves monotonicity, and positivity of the
displayed double integral proves strictness.

If (u(x,t_0+T)=u(x-\lambda,t_0)), then
(J_a(t_0+T)=e^{a\lambda}J_a(t_0)). Dividing the differential identity for
(J_a) by (J_a), integrating in time, and dividing by (aT) yields the
translation-delay identity. Finally,

\[
\min_{a>0}(Da+a^{-1})=2\sqrt D
\]

at (a=D^{-1/2}).
