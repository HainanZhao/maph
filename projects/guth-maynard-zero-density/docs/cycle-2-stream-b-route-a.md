# Cycle 2, Stream B, Route A: §13.1 application-hypothesis audit

## Outcome and claim boundary

`OBSERVED`: the audit closes the internal coefficient, support, threshold, and
interval transfers needed to apply Theorem 1.1 to the powered detector, in
both integer-\(k\) regimes.  It retains two blockers: the primary source for
the local zero-in-unit-strip estimate and the precise mean-value theorem used
on the \(q>\alpha\) branch.  Therefore Stream B is **not** an analytic G0
pass.

`PROVED` rows below are either direct identities/elementary inequalities
spelled out here or applications of a displayed Guth--Maynard statement whose
hypotheses were checked in the frozen source.  This audit does not reprove
Theorem 1.2, the zero detector, the local zero count, or the mean-value
theorem.

The source is Guth--Maynard, arXiv:2405.20552v2,
`LargevaluesDirichlet17.tex`, SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`;
the parent tarball SHA-256 is
`9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`.
The primary source defines \(A\lessapprox B\) to allow \(T^\epsilon\) for
every fixed \(\epsilon>0\), and interprets \(o(1)\) as \(T\to\infty\)
(TeX lines 288--290).  Every such loss remains visible below.

## What closes

### Smoothing and extraction

For a Type-I zero \(\rho=\beta+i\gamma\), the source chooses a smooth
\(\psi\) agreeing with \(e^{u(\sigma-\beta)}\) on the detector support.
The identity

\[
n^{-\beta-i\gamma}=n^{-\sigma-i\gamma}\psi(\log n)
\]

is exact there, giving the source's Fourier inversion formula.  Uniformity in
\(\beta\) is valid: putting \(a=\beta-\sigma\ge0\),

\[
\sup_{a\ge0} a^j e^{-au}=(j/u)^j e^{-j}\quad(j\ge1).
\]

After multiplying by a cutoff at scale \(\log N\), Leibniz gives the stated
\(\|\psi^{(j)}\|_\infty\ll_j(\log N)^{-j}\).  Repeated integration by
parts gives a rapidly decreasing Fourier tail.  The retained bounds are
\(\|\widehat\psi\|_1=O(\log N)\) and, for any fixed \(\epsilon>0\), an
\(O(T^{-100})\) tail after truncating \(|\xi|\le T^\epsilon\) with enough
integrations by parts.  Thus the original \(1/(3\log T)\) Type-I threshold
becomes only \(T^{-o(1)}\), never a fixed constant.

`OBSERVED` blocker: Guth--Maynard state an \(O(\log T)\) zero count in each
unit horizontal strip but provide no locator.  Conditional on that statement,
a maximal 1-separated extraction costs at most \(T^\epsilon\log T\): the
selected Fourier shifts can move a zero by \(O(T^\epsilon)\).  This is
\(T^{o(1)}\), but its primary theorem, multiplicity convention, and
uniformity have not yet been checked.

The shifted values lie in
\([T-O(T^\epsilon),2T+O(T^\epsilon)]\), not literally the unexpanded
`[T,2T]` printed after the truncation.  This is harmless after translation:
\(t=t_0+u\) changes a coefficient \(a_n\) to \(a_n n^{it_0}\), preserving
its magnitude, and places the set in \([0,H]\) with \(H\le2T\) for large
\(T\).  Theorem 1.1 may therefore use \(H\), with only the recorded
constant-factor/\(T^{o(1)}\) change.

### Detector normalization and powering

For \(n\asymp N\), the original detector coefficient is a truncated Möbius
divisor sum times \(e^{-n/T^{1/2}}\).  If \(N<T^{1/100}\), all divisors of
such \(n\) lie below the cutoff and \(\sum_{d\mid n}\mu(d)=0\), as the
source states.  Otherwise,

\[
|\widetilde b_n|\le\tau(n)=T^{o(1)},
\]

because \((N/n)^\sigma\le1\).  The elementary fixed-order divisor bound
is sufficient here; no exact finite-\(T\) coefficient-one assertion is
made before normalization.

Both \(k\) regimes are uniformly bounded.  In the small-\(n\) branch,
\(k=\lceil l(\sigma)/n\rceil\le77\); in the large-\(n\) branch, \(k=2\).
Thus a coefficient of \(\widetilde D^k\) is bounded by a fixed-order divisor
function times fixed powers of \(T^{o(1)}\), hence is itself \(T^{o(1)}\).
Dividing by this norm produces coefficients bounded by one and changes the
large-value threshold only to

\[
V=L^\sigma T^{-o(1)},\qquad L=N^k.
\]

The support is \([L,2^kL]\).  It has \(O(k)\) dyadic blocks.  Triangle
inequality and pigeonhole choose one fixed block over a subset of the large
value set, at a further \(O(k)=T^{o(1)}\) loss.  Since its length parameter
\(M\) satisfies \(M/L\le2^k\), the threshold is equivalently
\(M^\sigma T^{-o(1)}\).  This supplies every displayed Theorem 1.1
hypothesis after the conditional separated-set extraction.

### The two \(k\) regimes and remaining mean-value blocker

The small regime has \(l\le q<u\) exactly.  The large regime has
\(q>l\) exactly and \(q\le1+o(1)\).  Because
\(u(\sigma)\ge15/14\) for \(7/10\le\sigma\le4/5\), this yields
\(q\le u(\sigma)+o(1)\) (indeed an eventual strict inequality), not an
unqualified finite-\(T\) bound.

`OBSERVED` blocker: the source calls the complementary input the “usual Mean
Value Theorem” without a theorem locator.  The normalized block has the
expected bounded-coefficient, 1-separated, single-support preparation, but
the exact mean-value statement and uniform losses remain unpinned.  This
blocks the \(q>\alpha\) branch of a full analytic reconstruction.

## Falsifiers retained

- A multiplicity-inclusive local zero count with loss \(T^c\), \(c>0\),
  would defeat separated extraction.
- Unbounded \(k\), or powered coefficients larger than \(T^{o(1)}\), would
  defeat the normalization/dyadic transfer.
- A pinned mean-value theorem with incompatible coefficient, support, or
  spacing hypotheses would invalidate the complementary branch.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_b_route_a.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_b_route_a.py -v
```

The first command checks the frozen TeX hash and required §13.1 declarations,
then writes `artifacts/cycle-2-stream-b-route-a-v1.json` with a canonical audit
hash, script hash, tool version, and integer-nanosecond timing.
