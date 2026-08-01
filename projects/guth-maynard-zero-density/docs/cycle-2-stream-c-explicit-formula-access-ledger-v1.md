# Cycle 2 Stream C: truncated explicit-formula source closure (v1)

## Claim boundary

`OBSERVED`: this is a source-access and convention audit. It proves the
elementary conversion from the stated truncated formula to GM's looser
display, conditional on the cited formula and the separately pinned local
zero count. It does not re-prove either published explicit formula or either
short-interval corollary. `PLAN.md` is not changed.

## Source access and locators

`OBSERVED`: H. Iwaniec, *Lectures on the Riemann Zeta Function*, University
Lecture Series 62 (AMS, 2014), DOI `10.1090/ulect/062`, is independently
identified by the official AMS catalogue as the 119-page 2014 volume whose
Chapter 10 is *The asymptotic formula for \(\psi(x)\)*. The relevant locator is
Theorem 10.1, pp. 37--38. A reachable copy is watermarked as an individual
AMS purchase and prohibits duplication. It has **not** been copied, extracted,
or stored in this repository.

`OBSERVED`: the formula attributed to that theorem is independently matched
in C. Y. Yıldırım, *The distribution of primes: conjectures vs. hitherto
provables*, *Further Progress in Analysis* (World Scientific, 2009), pp.
75--107, equation (18), p. 82. Its web-hosted PDF provenance is not established
as publisher-authorised, so it too is not frozen locally and is corroboration
only.

`PROVED` (statement recorded from the view-only primary locator): for
\(z\ge2\), \(T\ge2\), writing \(\psi^{\flat}(z)\) with half weight at a
prime-power endpoint and \(\{z\}\) for the distance to the nearest *other*
prime power,

\[
\psi^{\flat}(z)=z-\sum_{|\gamma|<T}\frac{z^\rho}{\rho}
-\log(2\pi)-\frac12\log(1-z^{-2})+R(z,T),
\]

\[
R(z,T)\ll \frac zT(\log zT)^2+
\min\!\left(\log z,\frac{z\log z}{\{z\}T}\right),
\]

with an absolute implied constant. This is a short mathematical statement of
the theorem, not a copied source extract.

`OBSERVED`: Cully--Hugill--Johnston (CHJ), *On the error term in the explicit
formula of Riemann--von Mangoldt II*, arXiv:2402.04272v3, is locally frozen and
records \(\psi(x)=x-\sum_{|\gamma|\le T}x^\rho/\rho+E(x,T)\). Its quoted
every-\(T\) predecessor applies only for \(T<(x^\alpha-2)/2\),
\(\alpha\le1/2\); its main theorem supplies only *some* \(T^*\in[T,2T]\).
It therefore does not replace Iwaniec for GM's fixed truncations, especially
the almost-all branch. Its displayed zero sum does not state multiplicity.

## Endpoint, half-weight, and error transfer

Let \(u=\lceil x\rceil-1\) and \(v=\lfloor x+y\rfloor\). For the frozen
short-interval range, eventually \(u,v\asymp x\), \(2\le u<v\le2x\), and

\[
\sum_{n\in[x,x+y]}\Lambda(n)=\psi(v)-\psi(u),\qquad v-u=y+O(1).
\]

`PROVED`: because \(u,v\) are integers,
\(\psi(m)-\psi^{\flat}(m)=\Lambda(m)/2=O(\log x)\). Also every distinct
prime power is an integer, so \(\{u\},\{v\}\ge1\). For \(2\le T\le x\),
the two endpoint remainders and elementary terms obey

\[
\frac{x}{T}(\log(xT))^2+\log x
\ll \frac{x(\log x)^3}{T}.
\]

Indeed \(\log(xT)\ll\log x\) and \(x/T\ge1\). Thus endpoint rounding,
half-weighting, and the two explicit-formula remainders cost at most
\(O(x(\log x)^3/T)\).

## Height convention and multiplicity reconciliation

GM §13.2 prints \(|\rho|\le T\), whereas Iwaniec and CHJ display ordinate
truncation. This is not silently identified.

`PROVED` (conditional only on the local count immediately below): since
\(0<\Re\rho<1\), membership can differ only for zeros with
\(T-1/T<|\gamma|\le T\). Each such zero contributes

\[
\left|\frac{v^\rho-u^\rho}{\rho}\right|\ll\frac{x}{T}
\]

because \(u,v\asymp x\) and \(|\rho|\asymp T\). A
multiplicity-inclusive \(O(\log T)\) count in that unit strip changes the
interval zero sum by \(O(x\log T/T)\), absorbed by GM's displayed error. If
GM intended \(|\Im\rho|\le T\), the correction is vacuous.

`PROVED` (published source combination): Hasanalizade--Shen--Wong's explicit
Riemann--von Mangoldt bound gives \(N(t+1)-N(t-1)=O(\log(2t))\) for
\(t\ge3\), by subtracting its two explicit estimates. Bui--Heath-Brown
explicitly defines \(N(T)\) as counting zeros with multiplicity. CHJ uses the
same Riemann--von Mangoldt zero-sum notation but does not repeat that
convention; the source-notation alignment is `OBSERVED`, not a new
independent multiplicity proof for CHJ. Conjugation pairs positive and
negative strips with their multiplicities.

## Result for GM §13.2

`PROVED` (from the recorded input and exact conversions): in the asymptotic
ranges used by GM, the weaker but sufficient form is

\[
\sum_{n\in[x,x+y]}\Lambda(n)
=y-\sum_{|\rho|\le T}\frac{(x+y)^\rho-x^\rho}{\rho}
+O\!\left(\frac{x(\log x)^3}{T}\right),
\qquad 2\le T\le x,
\]

where zeros are interpreted with multiplicity after the pinned
Riemann--von Mangoldt convention. The strict/non-strict truncation issue is
kept inside the boundary-strip error, not changed by notation.

## Replay

```sh
python3 proof/check_cycle_2_stream_c_explicit_formula_sources.py
```

The check verifies frozen local sources, their anchors, and access
containment. It cannot reproduce the restricted Iwaniec text.
