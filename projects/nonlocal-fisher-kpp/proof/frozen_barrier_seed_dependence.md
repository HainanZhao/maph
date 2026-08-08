# Frozen-barrier seed-dependence obstruction

## Claim boundary

`PROVED`, conditional only on the sealed frozen-barrier theorem
`cycle-2-b002-frozen-ballistic-transmission-v1`: a fixed competition profile
does not determine the critical front phase for arbitrary admissible incoming
seeds. The additional scalar required by the frozen linear problem is

\[
J_C(q_0)=\int_{\mathbb R}e^yH_C(y)q_0(y)\,dy.
\tag{1}
\]

This does not rule out a theorem showing that the nonlinear Fisher--KPP flow
creates a universal incoming seed. It says that such universality is a
necessary hypothesis, not something supplied by the previous hump profile.

## Uniform critical-window corollary

Under the hypotheses of the sealed theorem, its ray limit remains uniform for

\[
|s|\le A\log t
\tag{2}
\]

for every fixed $A>0$:

\[
q(t,2t+s)=\frac{e^{-s}}{\sqrt{4\pi t}}
\bigl(J_C(q_0)+o(1)\bigr).
\tag{3}
\]

Indeed, the bridge slope is
$2+(s-y)/t=2+o(1)$ uniformly in (2), so the finite-window bridge convergence
and the exponential tail estimate in the sealed proof are unchanged. The
free-kernel correction satisfies

\[
\frac{(s-y)^2}{4t}\longrightarrow0
\]

uniformly for $s$ in (2) and each fixed $y$. The integrand is still dominated
by $e^yq_0(y)$, so dominated convergence gives (3).

For a fixed level $\theta>0$, define

\[
s_\theta(t;q_0)
=\log J_C(q_0)-\log\theta-\frac12\log(4\pi t).
\tag{4}
\]

Then (3) gives

\[
q\bigl(t,2t+s_\theta(t;q_0)\bigr)=\theta(1+o(1)).
\tag{5}
\]

Thus two seeds with $J_C(q_0^{(1)})\ne J_C(q_0^{(2)})$ have critical phase
separation

\[
s_\theta(t;q_0^{(1)})-s_\theta(t;q_0^{(2)})
=\log\frac{J_C(q_0^{(1)})}{J_C(q_0^{(2)})}.
\tag{6}
\]

## Exact step-barrier witness

Take $C(x)=3\mathbf1_{(-\infty,0)}(x)$. The sealed step calculation gives

\[
e^xH_C(x)=\frac23e^{2x},\qquad x<0.
\tag{7}
\]

Let $b\ge0$ be any nonzero continuous bump supported in $[0,1]$, and set

\[
q_a(x)=b(x-a),\qquad a\le-1.
\]

All $q_a$ have the same total mass and shape. Their supports lie to the left
of the barrier, and changing variables in (1) gives

\[
J_C(q_a)=\frac23e^{2a}\int_0^1e^{2r}b(r)\,dr.
\tag{8}
\]

In particular, the equal-mass seeds $q_{-2}$ and $q_{-3}$ satisfy

\[
\log\frac{J_C(q_{-2})}{J_C(q_{-3})}=2.
\tag{9}
\]

They therefore produce asymptotic critical-level locations separated by
exactly two inner length units, despite seeing the identical frozen barrier.

## Gate consequence

An exact or asymptotically accurate front-to-spacing map whose state contains
the previous hump/competition profile but omits the incoming critical moment
cannot be universal over admissible seeds. The smallest surviving frozen
linear state is the pair

\[
(C, J_C(q_0)).
\]

For the nonlinear top-hat equation, the next decisive question is whether
the flow makes $J_{C_L}(q_0)$ a universal function of the established hump
profile. A leading dependence on the original tail or earlier humps kills a
one-step spacing map and requires a longer memory state.

