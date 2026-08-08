# Cycle 2 — commensurate-window detuning

## Claim boundary first

`CONJECTURED` under the repository promotion policy, pending an independent
proof audit and a primary-literature overlap check: a positive periodic steady
state cannot have a period that divides the top-hat averaging-window length.
More quantitatively, a bounded positive pattern of fixed logarithmic contrast
must remain a distance of order at least $D$ from such a commensurate period.

This restricts possible wake wavelengths. It does not prove which wavelength
a front selects, that a periodic wake forms, or P1/P2.

## Question → question the questioning → brainstorm

**Question.** Can the infinite harmonic cascade be controlled near the first
periodic instability strongly enough to obtain a wavelength consequence?

**Question the questioning.** Needham--Billingham--Ladas--Meyer already analyze
the Turing instability, local periodic branches, and the change from a
most-unstable-mode mechanism to small-$D$ hump formation. Re-deriving a local
Lyapunov--Schmidt branch would be a consistency check, not the missing bridge
from a propagating front to its wake.

**Brainstorm.** The routes considered were an analytic Wiener-space center
manifold, an exact cumulative-mass delay equation, a small-$D$ atomic spike
map, and the resonance created when the averaging window contains an integer
number of periods. The last route was selected because it yields an exact
identity and a direct falsifier without assuming finite Fourier closure.

## Exclusion map from Cycle 1

| Former mechanism | Outcome or falsifier | State/invariant delta |
| --- | --- | --- |
| Finite Fourier invariant space | Highest mode $N$ generates $2N$ | Replace finite support by a full periodic profile and an exact window integral |
| Local weakly nonlinear branch | `RECOGNIZED`: already treated in the primary top-hat Fisher--KPP paper | Ask what exact geometry constrains its wavelength |
| Atomic spike equilibrium | Arbitrary isolated spike spacings survive at formal $D=0$ | Require positive diffusion and a finite-$D$ identity |
| Commensurate-window detuning | Selected | Track the residual window length $r=2-m\lambda$ |

## Decision specification

- **Input state:** a positive $C^2$, $\lambda$-periodic stationary solution
  of the radius-one top-hat equation.
- **Invariant/map:** decompose the length-two averaging window into $m$
  complete periods and one oriented residual interval of length
  $r=2-m\lambda$.
- **Smallest direct verifier:** exact integration for a periodic step function,
  followed independently by vanishing nonzero Fourier multipliers at $r=0$.
- **Advance condition:** obtain a rigorous inequality that forces zero contrast
  at $r=0$ and quantifies the detuning required for nonzero contrast.
- **Resource stop:** elementary identities plus exact rational replay; no PDE
  simulation is authorized for this decision.
- **Falsifier:** a positive nonconstant $C^2$ stationary solution with
  $2=m\lambda$, or a profile violating the displayed detuning inequality.

## Proposed theorem

Let

\[
K(x)=\tfrac12\mathbf 1_{[-1,1]}(x),\qquad
D u''+u(1-K*u)=0,
\]

and let $u>0$ be a $C^2$, $\lambda$-periodic solution. Write

\[
\bar u=\frac1\lambda\int_0^\lambda u(x)\,dx,\qquad
S^2=\frac1\lambda\int_0^\lambda |(\log u)'|^2\,dx,\qquad
M=\max u.
\]

For any integer $m\ge1$ with $r=2-m\lambda$ and $|r|\le\lambda$,

\[
\bar u-1=D S^2,
\tag{1}
\]

\[
D S^2\le \frac{|r|}{2}\operatorname{osc}u.
\tag{2}
\]

If $u$ is nonconstant,

\[
S\le \frac{|r|M\lambda}{2\sqrt2D},\qquad
\operatorname{osc}(\log u)
\le \frac{|r|M\lambda^2}{4D}.
\tag{3}
\]

Consequently,

\[
|2-m\lambda|
\ge \frac{4D\,\operatorname{osc}(\log u)}{M\lambda^2}.
\tag{4}
\]

In particular, if $2=m\lambda$, then $u\equiv1$. For the resonance nearest
the small-diffusion first tongue in this project's normalization, $m=2$ and
$\lambda=1$. Thus a nonconstant positive steady wake cannot have exact
wavelength one, and a bounded wake of fixed logarithmic contrast must be
detuned from one by at least order $D$.

## Route A — residual-window proof

For a periodic function, a length-two integral is $m$ complete periods plus
an oriented residual interval of length $r$. Hence, for every $x$,

\[
(K*u)(x)-\bar u
=\frac12\int_{I_x}^{\mathrm{oriented}}(u(y)-\bar u)\,dy.
\]

The residual interval has unsigned length $|r|$, so

\[
\|K*u-\bar u\|_\infty
\le \frac{|r|}{2}\operatorname{osc}u.
\tag{5}
\]

Divide the stationary equation by $u$, average over one period, and use

\[
\frac{u''}{u}=(\log u)''+|(\log u)'|^2,\qquad
\overline{K*u}=\bar u.
\]

This gives (1). At a maximum point $x_M$, $u''(x_M)\le0$, so the
stationary equation gives $(K*u)(x_M)\le1$. Since (1) gives $\bar u\ge1$,
inequality (5) gives (2).

The maximum and minimum of a periodic function can be joined along an arc of
length at most $\lambda/2$. Cauchy--Schwarz and the mean-value theorem for
the exponential give

\[
\operatorname{osc}(\log u)\le\frac{\lambda}{\sqrt2}S,\qquad
\operatorname{osc}u\le M\operatorname{osc}(\log u).
\]

Substitution in (2), followed by division by $S>0$, proves (3); its second
inequality rearranges to (4). When $r=0$, (2) gives $S=0$, so $u$ is
constant, and (1) fixes the constant as one.

## Route B — Fourier audit at exact commensurability

If $\lambda=2/m$, the $j$-th nonzero Fourier wavenumber is
$q_j=2\pi j/\lambda=\pi mj$. The top-hat multiplier is

\[
\widehat K(q_j)=\frac{\sin q_j}{q_j}=0.
\]

Thus $K*u=\bar u$ exactly. The steady equation becomes
$D u''+(1-\bar u)u=0$. Integrating over a period and using positivity gives
$\bar u=1$, after which periodicity forces $u''=0$ and $u\equiv1$.
This route independently checks the normalization and exact-resonance
conclusion, but not the quantitative bound (4).

## Literature boundary

`RECOGNIZED`: Needham, Billingham, Ladas, and Meyer describe the periodic
solution tongues and show their first small-$D$ boundary approaching the
commensurate wavelength in their radius-$1/2$ normalization. Their paper
also identifies front-driven hump formation as the mechanism replacing the
most-unstable linear wavelength at very small $D$. The exact no-pattern
identity at the tongue endpoint is consistent with that geometry (Section 4,
DOI `10.1017/S0956792524000688`). Hamel and Ryzhik prove kernel-independent
leading spreading at first order under general nonlocal Fisher--KPP
hypotheses (Theorem 1.5, DOI `10.1088/0951-7715/27/11/2735`), consistent with
the kernel-blind derivative used below.

`UNASSESSED`: the quantitative contrast--detuning estimate (4) has not yet
received a theorem-level literature audit. No novelty claim is made.

## Gate consequence

`CONJECTURED`: exact kernel-scale spacing is not the selected finite-$D$
wavelength; it is a singular boundary that annihilates all nonconstant
top-hat Fourier response. A successful small-$D$ front-to-pattern theory
must compute detuning from this boundary, not simply assert that the spacing
equals the interaction radius.

The next bridge is a front-formation law for $\lambda-1$, with (4) as a
mandatory consistency inequality.

## Kernel-blind leading-edge no-go

The detuning theorem extends verbatim to

\[
K_R(x)=\frac1{2R}\mathbf 1_{[-R,R]}(x),\qquad R>0.
\]

With $r=2R-m\lambda$, the corresponding bound is

\[
|2R-m\lambda|
\ge \frac{4RD\,\operatorname{osc}(\log u)}{M\lambda^2},
\tag{6}
\]

and exact commensurability $2R=m\lambda$ again forces $u\equiv1$.

`CONJECTURED` under the same promotion boundary: no rule that uses only the
linearization at the unpopulated state can universally select a positive
periodic wake across the top-hat-radius family.

Indeed, the Fréchet derivative at $u=0$ is

\[
D\mathcal N_R(0)h=D h_{xx}+h
\]

for every $R$; the radius first appears in the quadratic term
$-u(K_R*u)$. A deterministic rule whose entire input is this leading-edge
operator must therefore return the same candidate period $\Lambda(D)$ for
every $R$. Choosing $R=\Lambda(D)/2$ makes one averaging window exactly one
candidate period. The commensurability result then says that no positive
nonconstant $\Lambda(D)$-periodic stationary wake exists for that model,
contradicting the rule's claimed universality.

This does **not** rule out selection by the linearization at $u=1$, which
contains the multiplier $\widehat K_R$, or by a nonlinear front-memory law.
It rules out the concrete class of explanations that attempts to obtain the
wake period from pulled-front linearization at $u=0$ alone. The required new
input is now explicit: populated-state instability or the nonlinear
competition trace left by earlier humps.

## Front-event map: exact local-state obstruction

### Dependent decision question

Can a hump-formation event be propagated from the position and local shape of
the exponentially small leading edge, without retaining a nonlocal
competition trace?

- **Input state:** a regular level $u(X(t),t)=\theta>0$ and any finite local
  jet—or even the complete local germ—of $u$ at $X(t)$.
- **Transition:** the instantaneous level velocity.
- **Smallest verifier:** two positive initial profiles identical near the
  level point but differing by one compact $C^2$ bump inside its top-hat
  window.
- **Advance condition:** an exact closed velocity functional of the proposed
  local state.
- **Falsifier:** equal proposed states with unequal level velocities.
- **Stop criterion:** one exact counterexample kills only local-event closure;
  it does not rule out an asymptotic map carrying a competition-memory state.

For $W=\log u$, the PDE gives the exact identity

\[
W_t=D(W_{xx}+W_x^2)+1-K*u.
\tag{7}
\]

At a regular level $W(X(t),t)=\log\theta$,

\[
X'(t)=-\frac{D(W_{xx}+W_x^2)+1-(K*u)(X(t),t)}{W_x}.
\tag{8}
\]

`CONJECTURED` under the repository promotion policy, with a complete
elementary counterexample now recorded: no exact event law depending only on
the local germ at $X$ can reproduce (8) for all positive smooth data.

Take $X=0$ and

\[
u_0(x)=2-\frac{x}{1+x^2}.
\]

Then $u_0>0$, $u_0(0)=2$, $u_0'(0)=-1$, and $u_0''(0)=0$. Let

\[
h(x)=\begin{cases}
((x-\tfrac14)(\tfrac34-x))^3,&x\in[\tfrac14,\tfrac34],\\
0,&\text{otherwise},
\end{cases}
\qquad u_\varepsilon=u_0+\varepsilon h.
\]

The bump is $C^2$, is zero on a neighborhood of zero, and satisfies

\[
\int h(x)\,dx=\frac1{17920}.
\]

Thus $u_0$ and $u_\varepsilon$ have identical local germs at the level point,
but

\[
(K*u_\varepsilon)(0)-(K*u_0)(0)
=\frac{\varepsilon}{35840}.
\]

Their vector fields at zero differ by $-\varepsilon/17920$, and because
their common spatial derivative is $-1$, their level velocities also differ
by

\[
X_\varepsilon'(0)-X_0'(0)=-\frac{\varepsilon}{17920}.
\tag{9}
\]

For sufficiently small $\varepsilon>0$, both profiles remain positive and
the level near zero remains regular. This is the Gate-2 kill condition for a
position/local-shape-only map.

Equation (8) also identifies the smallest missing instantaneous observable:

\[
C(X,t)=(K*u)(X,t).
\]

But this scalar is not dynamically closed. Direct differentiation gives

\[
C_t=D C_{xx}+K*\bigl[u(1-C)\bigr],
\tag{10}
\]

so propagating $C(X,t)$ requires spatial competition information, not merely
its current value. The surviving route is therefore an **asymptotic**
front-memory closure with a controlled window profile or boundary layer;
an exact Markov map on hump positions and local edge shape is killed.

## Surviving asymptotic state: the scaled window profile

`RECOGNIZED`: in the radius-$1/2$ normalization, Needham et al. derive a
small-diffusion steady boundary-layer equation when
$\lambda=\tfrac12+\sqrt D\,L$. Translating their spatial and diffusivity
normalization to this project's radius-one kernel gives

\[
\lambda=1+\sqrt D\,L,\qquad
u(x)=D^{-1/2}v(x/\sqrt D)+o(D^{-1/2}),
\]

and the candidate even profile equation

\[
v''+v\left(
1-M+\frac12\int_{\xi-L}^{\xi+L}v(s)\,ds
\right)=0,
\qquad
M=\int_{\mathbb R}v(s)\,ds.
\tag{11}
\]

The existence and uniqueness of a positive decaying solution of (11) for
each $L>0$ are only `OBSERVED` numerically in the cited paper after
normalization; they are not assumed here.

### Conditional mass theorem

`CONJECTURED` under the repository promotion policy, with a self-contained
calculation: every positive, even, integrable $C^2$ solution of (11) with
$v'(\pm\infty)=0$ satisfies

\[
Q_L=2M(M-1),\qquad
Q_L=\iint_{|x-y|\le L}v(x)v(y)\,dx\,dy,
\tag{12}
\]

and therefore

\[
1<M<2.
\tag{13}
\]

To prove (12), integrate (11) over the line. The $v''$ term vanishes,
the constant term contributes $(1-M)M$, and Tonelli's theorem identifies
the remaining term with $Q_L/2$. Positivity gives $Q_L>0$, hence $M>1$.
Because $v$ is positive on the line and $L<\infty$, the complementary
double integral over $|x-y|>L$ is strictly positive, so $Q_L<M^2$.
Substitution into (12) gives $M<2$.

If $v(\xi)\sim A e^{-\sigma\xi}$ as $\xi\to+\infty$, the moving-window
integral vanishes in the limit and (11) gives

\[
\sigma^2=M-1,\qquad 0<\sigma<1.
\tag{14}
\]

Thus the minimal asymptotic memory can be parameterized by a full window
profile, while its total mass and tail exponent are constrained by (12)--(14).
This does not yet determine $L$; it supplies exact acceptance tests for a
front-matching law.

### Literature discrepancy firewall

`RECOGNIZED`: Equation (5.97) of the primary source writes the tail as
$e^{-\sigma_\infty\xi}$, while its displayed Equation (5.98), in the
radius-$1/2$ variables, states $\sigma_\infty=4\int_0^\infty v-1$.
Direct substitution into its own far-field differential equation instead
gives

\[
\sigma_\infty^2=4\int_0^\infty v-1.
\]

Unless a convention is missing from the display, the square root is absent.
This discrepancy affects the reported tail rate, not the derivation of
Equation (11) or the exact identities (12)--(14). No correction or novelty
claim is promoted until the journal version and author conventions receive
an independent audit.

## Exact critical-ray identity: a controlled front-matching target

Let $X(t)=X_0+2\sqrt D\,(t-t_0)$ and retain $W=\log u$ and
$C=K*u$. Combining (7) with the chain rule gives the exact identity

\[
\frac d{dt}W(X(t),t)
=D W_{xx}
 +D\left(W_x+D^{-1/2}\right)^2-C
\quad\text{at }(X(t),t).
\tag{15}
\]

Equivalently, for $t_1>t_0$,

\[
W(X(t_1),t_1)-W(X(t_0),t_0)
=-\int_{t_0}^{t_1}C(X(t),t)\,dt
 +\mathcal E_{t_0,t_1},
\tag{16}
\]

where

\[
\mathcal E_{t_0,t_1}
=\int_{t_0}^{t_1}
\left[D W_{xx}
 +D\left(W_x+D^{-1/2}\right)^2\right](X(t),t)\,dt.
\tag{17}
\]

`CONJECTURED` as a route, not as a concluded estimate: if the leading edge
can be shown to retain critical slope $W_x=-D^{-1/2}+o(D^{-1/2})$, its
integrated curvature is controlled, and the competition trace converges in
the edge scale to the one-sided cumulative profile generated by $v_L$, then
(16) becomes a scalar phase-delay law. Matching that delay between
consecutive formation events is the first mechanism in this cycle capable of
determining $L=(\lambda-1)/\sqrt D$ while retaining the required nonlinear
memory.

The acceptance conditions are now quantitative:

1. bound $\mathcal E_{t_0,t_1}$ uniformly on the inter-event interval;
2. prove a trace approximation for $C(X(t),t)$ in terms of $v_L$;
3. define formation events by a fixed regular log-density level and show the
   resulting $L$ is level-independent at leading order;
4. verify that the resulting $L$ obeys (6) and the mass/tail constraints
   (12)--(14).

A surviving $O(1)$ curvature defect, a noncritical edge slope, or leading
dependence on the chosen event level falsifies this phase-delay closure.

## Failure ledger

- **False first-replay step:** for $r<0$, the deleted residual tail was
  initially placed before the endpoint of the length-two window. The correct
  decomposition subtracts the interval from $x+2$ to $x+m\lambda$. The
  exact replay rejected the error before promotion; Route A uses the corrected
  oriented-interval identity.
- **False generalized-replay pass:** the first radius-parametric edit indented
  the identity check outside the offset loop and inside only the negative-
  residual branch, producing a misleading 48-check pass. Coverage inspection
  caught it; the corrected replay exercises 2,448 exact rational cases across
  three radii, both residual signs, exact resonance, and every frozen offset.
