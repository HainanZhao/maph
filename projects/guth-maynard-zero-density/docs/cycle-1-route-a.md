# Cycle 1, Route A: exact baseline implication replay

## Claim boundary

`PROVED` in this document means only that the displayed rational identities
follow exactly from the published estimates and proof conditions quoted below.
The replay does **not** reprove Guth--Maynard's zero-density theorem,
Ingham's estimate, the zero-free region, Theorem 1.1's analytic large-values
bound, or any analytic error term.  In particular, it does not establish a
new zero-density, large-values, or short-interval result.

## Frozen source and applicable statements

The source inspected for this route is Larry Guth and James Maynard, *New
large value estimates for Dirichlet polynomials*, arXiv:2405.20552v2,
`LargevaluesDirichlet17.tex`, downloaded on 2026-08-01.  Its local source
tarball was obtained from `https://export.arxiv.org/e-print/2405.20552v2`;
the rendered PDF SHA-256 is
`915392cf7d0ecd108479814a9a1481e23423ef63415776471cec3975ae482cae`.
The downloaded source tarball SHA-256 is
`9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`,
and `LargevaluesDirichlet17.tex` inside it SHA-256 is
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.

- `PROVED` (source, introduction equations (1.2), Theorem 1.2, and the
  paragraph immediately following it): Ingham gives
  
  \[
  N(\sigma,T)\le T^{[3/(2-\sigma)](1-\sigma)+o(1)},
  \]
  while Guth--Maynard Theorem 1.2 gives
  
  \[
  N(\sigma,T)\le T^{[15/(3+5\sigma)](1-\sigma)+o(1)}.
  \]
  The paper combines Ingham for \(\sigma\le7/10\) with its theorem to state
  the coefficient \(30/13\).
- `PROVED` (source, Theorem 1.1 and equation (1.1)): if \(|b_n|\le1\) and
  the \(t_r\) are 1-separated in the theorem's stated range, then the new
  bound has terms
  \(N^2V^{-2}\), \(N^{18/5}V^{-4}\), and \(TN^{12/5}V^{-4}\), all times
  \(T^{o(1)}\).  The classical comparator has terms
  \(N^2V^{-2}\) and \(T\min(NV^{-2},N^4V^{-6})\), again times
  \(T^{o(1)}\).  Route A evaluates only their powers at the frozen cell; it
  does not recheck the theorem hypotheses for a particular polynomial.
- `PROVED` (source, Proposition 11.1, label `prp:energybound`, and the final
  Remark of §13.1, source line 2398): the energy bound is
  \[
  E(W)\lessapprox |W|L^{4-4\sigma}
   +|W|^{21/8}U^{1/4}L^{1-2\sigma}
   +|W|^3L^{1-2\sigma}
  \]
  when \(U^{3/4}\le L\le U\).  The Remark states the bottleneck pattern
  \(\sigma=7/10\), \(N=T^{5/13}\), \(L=N^2=T^{10/13}\),
  \(U=T^{12/13}\), and \(|W|\approx U^{2/3}\) with
  \(E(W)\approx|W|^{5/2}\approx|W|^4/U\).  Route A treats the approximate
  pattern as a frozen exponent substitution only; it does not promote it to
  an extremizer theorem.
- `PROVED` (source, Section 13.2, proof of Corollary 1.3): for the uniform
  result it sets
  \(T=(x/y)\exp(2(\log x)^{1/4})\) and requires
  \(T<x^{13/30-\epsilon/2}\).  The conclusion is
  \(y\ge x^{17/30+\epsilon}\).
- `PROVED` (source, proof of Corollary 1.4): for the almost-all result it
  sets \(\delta=X^{-13/15+\epsilon/2}\) and
  \(T=\delta^{-1}\exp(4(\log X)^{1/4})\), using
  \(T\lessapprox X^{13/15-\epsilon/3}\).  The conclusion is
  \(y\ge X^{2/15+\epsilon}\).

The source's `o(1)`, logarithmic, zero-free-region, and epsilon losses are
analytic hypotheses of these deductions.  The exact replay retains their
strict-inequality endpoint convention rather than treating endpoint equality
as a theorem.

## Exact derivation

Put

\[
A_I(\sigma)=\frac{3}{2-\sigma},\qquad
A_{GM}(\sigma)=\frac{15}{3+5\sigma}.
\]

Using rational arithmetic only,

\[
A_I(\sigma)-A_{GM}(\sigma)
=\frac{30(\sigma-7/10)}{(2-\sigma)(3+5\sigma)}.
\]

Thus at \(\sigma_*=7/10\), both coefficients are

\[
A_I(\sigma_*)=A_{GM}(\sigma_*)=\frac{30}{13}=:b.
\]

### Critical large-values cell

The source identifies the critical situation \(V=N^{3/4}\) and
\(N=T^{4/5}\).  Thus \(V=T^{3/5}\).  `PROVED`: exact substitution into
every displayed term of Theorem 1.1 gives

\[
\begin{array}{c|ccc|c}
 & N^2V^{-2} & N^{18/5}V^{-4} & TN^{12/5}V^{-4} & \max\\
 \text{power of }T & 2/5 & 12/25 & 13/25 & 13/25.
\end{array}
\]

For classical equation (1.1), the two terms inside its minimum both have
power \(3/5\):

\[
\begin{array}{c|ccc|c}
 & N^2V^{-2} & TNV^{-2} & TN^4V^{-6} & \max\bigl(N^2V^{-2},\,T\min(\cdot,\cdot)\bigr)\\
 \text{power of }T & 2/5 & 3/5 & 3/5 & 3/5.
\end{array}
\]

The exact exponent gain is therefore
\(3/5-13/25=2/25\).  The common \(T^{o(1)}\) factor means this is a
comparison of fixed leading powers, not a claimed uniform numerical margin
at finite \(T\).

### Zero-density bottleneck cell

The final Remark of §13.1 identifies a distinct cell in the proof of the
zero-density result.  Freeze precisely its exponent pattern:

\[
\sigma=\frac7{10},\quad N=T^{5/13},\quad L=N^2=T^{10/13},\quad
U=T^{12/13},\quad L=U^{5/6},\quad V=L^\sigma=U^{7/12},\quad
|W|=U^{2/3}.
\]

The hypothesis \(U^{3/4}\le L\le U\) of Proposition 11.1 holds exactly,
since \(3/4\le5/6\le1\).  `PROVED`: substitution into every Theorem 1.1
term, now with time parameter \(U\), gives

\[
\begin{array}{c|ccc|c}
 & L^2V^{-2} & L^{18/5}V^{-4} & UL^{12/5}V^{-4} & \max\\
 \text{power of }U & 1/2 & 2/3 & 2/3 & 2/3.
\end{array}
\]

`PROVED`: substitution into all three Proposition 11.1 energy terms gives

\[
\begin{array}{c|ccc}
 & |W|L^{4-4\sigma} & |W|^{21/8}U^{1/4}L^{1-2\sigma} & |W|^3L^{1-2\sigma}\\
 \text{power of }U & 5/3 & 5/3 & 5/3.
\end{array}
\]

The frozen energy scale itself ties these values:
\[
|W|^{5/2}=U^{5/3}=|W|^4/U.
\]
This is an exact check of the Remark's stated exponent arithmetic, **not** a
proof that a random or constructed set realizes each comparison sharply.

Finally, there are \(T/U=T^{1/13}\) subintervals, and a local
\(U^{2/3}=T^{8/13}\) large-value count maps to
\[
T^{1/13}T^{8/13}=T^{9/13}
=T^{(30/13)(1-7/10)}.
\]
Thus the local tie cell matches the global density exponent exactly at
\(\sigma=7/10\), but it alone does not prove a no-go theorem.

`PROVED`: for the uniform proof condition, the power of \(x\) in
\(T\asymp x/y\) is \(1-\theta\), and the density condition is
\(1-\theta<1/b\), up to the paper's explicitly retained epsilon/subexponential
losses.  Consequently the rational endpoint is

\[
\theta_{\rm uniform}=1-\frac1b
=1-\frac{13}{30}=\frac{17}{30}.
\]

`PROVED`: in the almost-all proof the corresponding density condition is
\(T<X^{2/b-\epsilon}\).  The source chooses
\(\delta=X^{-2/b+\epsilon/2}\), and its Cauchy--Schwarz reduction requires
the target interval length to begin at the scale \(\delta X\).  Hence its
rational endpoint is

\[
\theta_{\rm almost-all}=1-\frac2b
=1-\frac{13}{15}=\frac2{15}.
\]

These are distinct conclusions: the first is a uniform PNT asymptotic; the
second holds for almost all integer starting points in \([X,2X]\).  Neither
asserts a prime-existence result.

## Replay

From the repository root:

```sh
python3 projects/guth-maynard-zero-density/proof/replay_baseline_route_a.py
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -v
```

The first command writes
`artifacts/baseline-route-a-v3.json`; the v1 and v2 certificates remain
preserved and v3 records its supersession.  The script's mathematical state is
solely `fractions.Fraction`; wall time is recorded with integer nanoseconds.
