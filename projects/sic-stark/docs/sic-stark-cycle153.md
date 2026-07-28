# SIC--Stark research cycle 153: tilted finite part and small divisors

Date: 2026-07-28

## Tilted finite part

For an interior point \(\tau\), let
\[
 S_\tau=\{y:0<\Re y<\Re Q_\tau\}.
\]
An admissible tilt is a \(C^1\) graph
\[
 C_h=\{c+h(t)+it:t\in\mathbb R\}
\]
which, together with a homotopy to the vertical graph, stays in
\(S_\tau\), with one common integrable majorant for the two-base
kernel. The tilted value is the specialized S--S integral over
\(C_h\), followed by exact helical periodization.

**Tilt independence is proved.** Truncate two graphs at heights
\(\pm T\), join their endpoints, and apply Cauchy's theorem in the
pole-free strip. The joining caps vanish by the common interior
exponential estimate. Taking \(T\to\infty\) gives equality. Local
uniform convergence permits the same operation after periodization.

The remaining hypothesis is now concrete:

> The tilted primitive value extends continuously to \(\beta_6\)
> along the attracting \(A_6\)-axis, commutes there with trace-five
> fusion, and hence has the flow-invariant fused value.

No uniform, Hölder, or two-sided boundary regularity is assumed.

## Component difficulty

Center \(s_{a,b}\equiv4b-5a\pmod6\) in
\(\{-3,-2,-1,0,1,2\}\).

- Six components have \(s_{a,b}=0\). They are purely oscillatory and
  use the Fresnel/Abel value without a strip tilt.
- Thirty have \(s_{a,b}\ne0\). Each grows at one end and decays at the
  other, so the two-base strip is essential.

## Exact arithmetic of the degenerating phase

Set \(\Delta(\tau)=\tau+\tau^{-1}-5\). Then
\[
 \boxed{A_6\tau-\tau
 =-\frac{24\tau}{24\tau-5}\Delta(\tau).}
\]
With
\[
 \gamma(s)=
 \frac{\beta+\beta^{-1}s^2+i\sqrt{21}s}{1+s^2},
\]
we have
\[
 \Delta(\gamma(s))=i\frac{21}{\beta}s+O(s^2),
\]
\[
 \kappa(s):=2\pi|\Im(A_6\gamma(s)-\gamma(s))|
 =2\pi\sqrt{21}(1-\beta^{-6})s+O(s^2).
\]

Moreover \(\beta=[4;\overline{1,3}]\), and
\[
 (n\beta-m)(n\beta^{-1}-m)=m^2-5mn+n^2
\]
gives
\[
 \|n\beta\|\ge\frac1{\sqrt{21}n+\frac12},\qquad
 |1-e^{2\pi in\beta}|
 \ge\frac4{\sqrt{21}n+\frac12}.
\]
The estimate must control the transition range
\(n\asymp1/\kappa(s)\asymp1/s\).

## Numerical rehearsal

Arb evaluates the 24-factor continuation at
\(s=1/2,1/4,1/8,1/16,1/24\). The output balls remain rigorous, but the
unperiodized primitive oriented factor becomes rapidly
ill-conditioned. It is not the finite AFK overlap before helical
projection, so this rehearsal is diagnostic and is not promoted to
boundary convergence. The certificate records every ball, the fusion
defect, its radius, and comparison of its absolute value with the
certified primitive root.

## The three queued gates

- Dimension four: the even-wrap ledger gives argument \(-q\).
- Dimension five: lens level \(15\), sign bit \(0\), argument \(+q\).
- Zero mode: the tilted/Fresnel normalization gives
  \(\nu_{\rm aux}^{\pm1}=-2\sqrt7\pm3\sqrt3\), hence trace
  \(-4\sqrt7\), matching the independent AFK endpoint enclosure.

The last formula is exact: reciprocity gives product \(1\), while the
calibrated trace is \(-4\sqrt7\); solving
\(X^2+4\sqrt7X+1=0\) gives the displayed roots.

The last item is a normalization calibration, not an inference of the
nonzero oriented packet.

Executable audit:
`scripts/dimension_six_tilted_finite_part.py`.
