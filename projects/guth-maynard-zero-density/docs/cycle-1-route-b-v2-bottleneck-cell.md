# Cycle 1 — Route B v2 bottleneck-cell audit

Claim boundary: `PROVED` below means exact rational substitution conditional on
Guth--Maynard Theorem 1.1, Proposition 11.1, and their final Remark in §13.1.
This audit does not prove those analytic inputs, does not reconstruct the
intermediate (S_1,S_2,S_3) estimates, and does not prove that the method
saturates.

## Outcome

`PROVED`: at the source's declared bottleneck cell,
\[
\sigma=\frac7{10},\quad N_{\rm original}=T^{5/13},\quad
L=N_{\rm original}^2=T^{10/13},\quad U=T^{12/13},
\]
we have
\[
L=U^{5/6},\quad V=L^\sigma=U^{7/12},\quad
|W|=U^{2/3}.
\]
Every Theorem 1.1 term has exponent, relative to (U),
\[
\frac12,\ \frac23,\ \frac23.
\]
Thus its latter two terms tie and the local output is exactly
(U^{2/3+o(1)}).

`PROVED`: every term in Proposition 11.1 has exponent (5/3) at this
same cell. Hence all three energy terms tie, precisely matching
\[
E(W)=|W|^{5/2}=|W|^4/U=U^{5/3}.
\]
This is a stronger statement than merely identifying the leading energy term:
at the frozen cell, there is no slack among the three displayed
Proposition 11.1 terms.

`PROVED`: the local count converts exactly to the zero-density target:
\[
U^{2/3}\frac{T}{U}=T^{8/13}T^{1/13}=T^{9/13}
=T^{15(1-7/10)/(3+5(7/10))}.
\]
The multiplicative combination is understood up to the source's (T^{o(1)})
losses and its interval-endpoint bookkeeping.

## Source and hypotheses

The frozen source is `arXiv:2405.20552v2`, whose TeX source member
`LargevaluesDirichlet17.tex` has SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
The source tarball SHA-256 is
`9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`.

- Theorem 1.1, TeX lines 64–79: 
  (L^2V^{-2}+L^{18/5}V^{-4}+UL^{12/5}V^{-4}).
- Proposition 11.1 / (11.1), TeX lines 1785–1804:
  
  \[
  |W|L^{4-4\sigma}+|W|^{21/8}U^{1/4}L^{1-2\sigma}
  +|W|^3L^{1-2\sigma}.
  \]
- Final Remark in §13.1, TeX line 2398: the frozen values of the original
  length, squared length, interval size, (|W|), and (E(W)).

The Proposition 11.1 range is checked exactly:
(U^{3/4}\leq L=U^{5/6}\leq U), and (7/10>1/2). Its coefficient and
one-separation hypotheses are inherited as source assumptions, not generated
by this arithmetic certificate.

## Cleared-linear-form tables

For Theorem 1.1 the three (U)-exponents are respectively
\[
2\left(\frac56\right)-2\left(\frac7{12}\right)=\frac12,
\]
\[
\frac{18}{5}\left(\frac56\right)-4\left(\frac7{12}\right)=\frac23,
\qquad
1+\frac{12}{5}\left(\frac56\right)-4\left(\frac7{12}\right)=\frac23.
\]
After clearing by 12, the values are (6,8,8), so the maximum/tie is
certified without floating-point comparisons.

For Proposition 11.1, after clearing by 12, each of
\[
\frac23+\left(4-4\cdot\frac7{10}\right)\frac56,
\]
\[
\frac{21}{8}\frac23+\frac14+
\left(1-2\cdot\frac7{10}\right)\frac56,
\]
and
\[
3\cdot\frac23+\left(1-2\cdot\frac7{10}\right)\frac56
\]
equals (20/12=5/3). This certifies the three-way tie.

## Replay

The versioned certificate is
[cycle-1-route-b-v2-bottleneck-cell.json](../artifacts/cycle-1-route-b-v2-bottleneck-cell.json).

```sh
python3 projects/guth-maynard-zero-density/proof/replay_bottleneck_cell_route_b_v2.py --check projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-v2-bottleneck-cell.json
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The separate v1 Route-B baseline artifact is intentionally retained and its
validity is regression-tested by the v2 test suite.
