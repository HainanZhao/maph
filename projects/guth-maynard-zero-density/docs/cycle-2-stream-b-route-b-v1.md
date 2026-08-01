# Cycle 2 — Stream B Route B analytic application audit

Claim boundary: `PROVED` here means a source-pinned audit of the application
of the named published results. It does not reprove MP Lemmas 23–24, their
twisted-fourth-moment input, Montgomery's theorem, GM Theorem 1.1, or GM
Theorem 1.2. It claims no new density theorem. Stream C's external
truncated-explicit-formula node is outside this audit, so this is not a G0
promotion.

## Narrow outcome

`PROVED`: this independent Route B closes the Stream B application nodes that
Route A had left unpinned: MP's Type-II input, a multiplicity-inclusive
unit-strip conversion, the two-sided-height convention, and the discrete
mean-value input. The resulting status is a narrow Stream B PASS only.

The frozen hashes, all labels, and exact rational checks are in
[cycle-2-stream-b-route-b-v1.json](../artifacts/cycle-2-stream-b-route-b-v1.json).

## Complement, multiplicity, and heights

`PROVED`: GM's Type I detector is exactly MP's: both use the same truncated
Möbius divisor sum, (e^{-n/T^{1/2}}), (nsim N), dyadic range
([T^{1/100},T^{1/2}(\log T)^2]), and threshold ((3\log T)^{-1}).
GM defines its Type II class as the complement of that Type I class. MP Lemma
23 says that every positive-height zero is MP Type I or MP Type II (or both).
Therefore every GM-complement zero is MP Type II, and MP Lemma 24 gives

\[
R_{II}(\sigma,T)\ll T^{2(1-\sigma)}(\log T)^{O(1)}.
\]

`PROVED`: MP expressly takes cluster zeros without multiplicity. The frozen
Hasanalizade--Shen--Wong Riemann--von Mangoldt bound and Bui--Heath-Brown's
explicit multiplicity convention give (O(\log(T+2))) multiplicity in a
unit strip, by subtracting the RvM bounds at (u+1) and (u-1). Hence
changing MP's distinct count to the frozen multiplicity count costs only a
logarithm.

`PROVED`: (zeta(s)<0) on (0<s<1): the alternating eta series is positive
and (eta(s)=(1-2^{1-s})\zeta(s)). Thus there is no real non-trivial zero,
and conjugation converts the positive-height count exactly to the two-sided
count by a factor two. The log loss and factor two are both (T^{o(1)}) at
the audited exponent level.

## Type-I preparation

`PROVED`: GM's smooth (psi) has
(psi(\log n)=n^{\sigma-\beta}) on detector support. Its displayed Fourier
identity moves a Type-I value from (gamma) by (2\pi\xi), and rapid decay
permits (|\xi|\le T^\epsilon) after a (T^{-100}) tail. A maximal
1-separated subset then loses at most (O(T^\epsilon\log T)) source zeros
per chosen value using the pinned multiplicity-inclusive unit-strip bound.
After the (O(\log T)) choice of detector length, this produces the required
1-separated large-value set with only (T^{o(1)}) loss. Endpoint padding and
translation give an interval of length (O(T)) and preserve all moduli.

`PROVED`: once (N>T^{1/100}),
(|\widetilde b_n|\le\tau(n)=T^{o(1)}). Both permitted choices of (k) are
bounded. For small (n=\log N/\log T),
(k=\lceil\ell(\sigma)/n\rceil\le77), with

\[
\ell(\sigma)=\frac{10}{6+10\sigma},\qquad
\ell(\sigma)\le kn\le\frac{15}{6+10\sigma}.
\]

For large (n), (k=2); then (kn>\ell(\sigma)) and
(kn\le1+o(1)<15/(6+10\sigma)+o(1)), retaining the endpoint gap
(15/14-1=1/14). Fixed-order divisor bounds normalize every coefficient of
(widetilde D^k) to modulus at most one at a (T^{o(1)}) threshold loss.

`PROVED`: its support is contained in ([L,2^kL]), (L=N^k). Pigeonholing
over (O(k)) dyadic blocks chooses one common block of length (M\asymp_kL)
and preserves the threshold (V=M^\sigma T^{-o(1)}).

## The two applications

`PROVED`: on (L\le T^\alpha), GM Theorem 1.1 gives the three structural
terms

\[
L^{2-2\sigma},\qquad L^{18/5-4\sigma},\qquad TL^{12/5-4\sigma}.
\]

The upper, middle, and lower bounds on (L), respectively, make their
exponents exactly (A(\sigma)=15(1-\sigma)/(3+5\sigma)).

`PROVED`: Montgomery's Theorem 1 / formula (7), visually inspected at
printed p. 335 (frozen PDF p. 348), applies to arbitrary complex
coefficients at separated ordinates. Complex conjugation changes GM's
(m^{it}) to the printed (m^{-it}) with no modulus change. Padded endpoints
give (delta\ge1), so the theorem gives

\[
R\ll T^{o(1)}\bigl(M^{2-2\sigma}+TM^{1-2\sigma}\bigr).
\]

In the (L>T^\alpha) branch, the first term is at most (T^{A(\sigma)});
the second has strictly smaller exponent because

\[
A(\sigma)-[1+(1-2\sigma)\alpha]
=\frac{250(\sigma-3/4)^2+3/8}
 {2(3+5\sigma)(9-10\sigma)}>0.
\]

`PROVED`: adding the MP-Type-II and Type-I bounds on positive dyadic shells,
then using the two-sided conversion above, recovers GM's published exponent
on (7/10\le\sigma\le4/5) within this source route. This is an audit result,
not a replacement proof.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_b_route_b.py --check projects/guth-maynard-zero-density/artifacts/cycle-2-stream-b-route-b-v1.json
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_b_route_b.py
```
