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
