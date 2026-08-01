# Cycle 2 Stream A: Maynard--Pratt and mean-value audit (v1)

## Claim boundary

`OBSERVED`: this ledger freezes and reads the cited arXiv sources. It does not
re-prove MP Lemma 24, its twisted-fourth-moment input, or the remaining
zero-to-large-value transfers assigned to Stream B. It does not promote G0.

## Frozen sources and locators

| ID | Source / frozen version | Exact locator | Status |
| --- | --- | --- | --- |
| MP | J. Maynard and K. Pratt, *Half-isolated zeros and zero-density estimates*, arXiv:2206.11729v2, 29 May 2023, 39 PDF pages | `HalfIsolatedv2.tex` lines 1017--1022 (Lemma 24), 975--1005 (definition and Lemma 23), and 2132--2166 (proof); PDF pp. 14, 16, and 37 | `OBSERVED` source freeze; hashes in the companion metadata |
| GM | L. Guth and J. Maynard, *New large value estimates for Dirichlet polynomials*, arXiv:2405.20552v2, 52 PDF pages | `LargevaluesDirichlet17.tex` lines 2310--2318 and 2353--2363; PDF pp. 48--49 | `OBSERVED` source freeze; hashes in the companion metadata |
| M | H. L. Montgomery, *Mean and Large Values of Dirichlet Polynomials*, *Inventiones mathematicae* **8** (1969), 334--345 | Theorem 1 (Davenport), formula (7), printed p. 335; GDZ volume PDF p. 348 | `OBSERVED` source freeze; published primary statement inspected in the scan |

All PDF page numbers are pages of the named frozen source PDF, not inferred
journal pagination.

## Maynard--Pratt's exact local setup

`PROVED` (by the displayed definitions in MP): for a non-trivial zero
\(\rho=\beta+i\gamma\) with \(\gamma\in[T,2T]\), MP defines

\[
D_N(s)=\sum_{n\sim N}a(n)n^{-s}e^{-n/T^{1/2}},\qquad
a(n)=\sum_{\substack{d\mid n\\d\le2T^{1/100}}}\mu(d).
\]

It calls \(\rho\) Type I when, for some dyadic
\(N\in[T^{1/100},T^{1/2}(\log T)^2]\),
\(|D_N(\rho)|\ge(3\log T)^{-1}\). It calls \(\rho\) Type II when

\[
\left|\frac1{2\pi i}\int_{(-\beta+1/2)}
 T^{s/2}\Gamma(s)M(\rho+s)\zeta(\rho+s)\,ds\right|\ge\frac13,
\qquad M(s)=\sum_{m\le2T^{1/100}}\mu(m)m^{-s}.
\]

`PROVED` (MP Lemma 23): for sufficiently large \(T\), every non-trivial
zero in the positive-height interval \([T,2T]\) is Type I or Type II, or
both. The Appendix proof first assumes \(\beta\ge1/2+1/\log T\).

`PROVED` (MP Lemma 24, in the range used here): with
\(R_{II}(\sigma,T)\) the number of MP-Type-II zeros having
\(\beta\ge\sigma\) and \(\gamma\in[T,2T]\),

\[
R_{II}(\sigma,T)\ll T^{2(1-\sigma)}(\log T)^{O(1)}.
\]

The printed lemma has no displayed \(\sigma\)-range. Its proof treats
\(\sigma\ge1/2+1/\log T\) and calls the complementary case trivial. It
therefore covers the preregistered range \(7/10\le\sigma\le4/5\), for
sufficiently large \(T\). The proof exposes \((\log T)^{17}\) before
using a twisted fourth moment bounded by \(T(\log T)^{O(1)}\); the final
log power in Lemma 24 is not explicit.

## Exact transfer to GM Section 13.1

| Audit item | Finding | Status |
| --- | --- | --- |
| Detector coefficients | GM sets \(b_n=(\sum_{d\mid n,\ d\le2T^{1/100}}\mu(d))e^{-n/T^{1/2}}\) and \(D(s)=\sum_{n\sim N}b_nn^{-s}\). This is MP's \(D_N\) exactly, with only the renaming \(a(n)e^{-n/T^{1/2}}\mapsto b_n\). | `PROVED` |
| Support convention | MP explicitly writes \(n\sim N\) for \(N<n\le2N\). GM's definition of a length-\(N\) Dirichlet polynomial uses the same condition. | `PROVED` |
| Type-I threshold and length | GM uses the same dyadic range \([T^{1/100},T^{1/2}(\log T)^2]\) and threshold \((3\log T)^{-1}\). | `PROVED` |
| Height and real-part restrictions | Both local definitions use \(\gamma\in[T,2T]\). GM adds \(\beta\ge\sigma\), exactly matching MP's \(R_{II}(\sigma,T)\). | `PROVED` |
| "Type II" terminology | GM defines Type II as the *complement* of GM-Type-I. MP defines an integral-condition Type II; its types may overlap. MP Lemma 23 makes each GM-complement zero MP-Type-II, so MP Lemma 24 bounds it. | `PROVED` |
| Log loss | GM's \((\log T)^{O(1)}\) is exactly MP Lemma 24's granularity. No finite-\(T\) conversion to a power of \(T\) is made. | `PROVED` |
| Multiplicity convention | MP explicitly takes cluster zeros without multiplicity and says multiplicities cost harmless logarithms. Neither its local \(R_{II}\) definition nor GM's theorem/Section 13.1 declares a multiplicity convention. The preregistration fixes multiplicity counted, but a separately frozen local zero-count conversion is not yet audited. | `OBSERVED`; blocks a multiplicity-counted promotion |
| Two-sided heights | MP and GM's reduction are local at positive heights. GM later dyadically passes to \([0,T]\); the \(|\Im\rho|\le T\) conversion is not part of MP Lemma 24. | `OBSERVED`; not promoted here |

`PROVED`: the detector/range falsifier in the preregistration does not occur.
The counting-convention gap is contained rather than silently absorbed.

## Pinned mean-value input for GM's MVT branch

`PROVED` (Montgomery, Theorem 1): let \(T_0,T\) be real with \(T>0\),
let \(T_0<t_1<\cdots<t_R<T_0+T\), set
\(t_0=T_0,t_{R+1}=T_0+T\), and
\(\delta=\min_{0\le r\le R}(t_{r+1}-t_r)\). For arbitrary complex
\(a_n\), Montgomery states

\[
\sum_{r=1}^R\left|\sum_{n\le L}a_nn^{-it_r}\right|^2
\ll\bigl(T+O(L\log L)\bigr)\bigl(\delta^{-1}+\log L\bigr)
\sum_{n\le L}|a_n|^2,
\]

with an absolute implied constant. For GM's 1-separated set in \([T,2T]\),
use the enclosing interval \((T-1,2T+1)\); then \(\delta\ge1\), so the
published statement gives the required discrete large-value estimate with
only logarithmic loss. Montgomery writes \(n^{-it_r}\), whereas GM writes
\(n^{it_r}\); replacing every ordinate by its negative maps GM's set to a
1-separated set in \([-2T,-T]\), an admissible Montgomery interval.

`PROVED` (algebraic consequence, conditional only on the separately audited
coefficient norm): taking \(L\asymp N^k\), dividing by
\(N^{2k\sigma}\), and inserting
\(\sum|c_m|^2\le N^{k+o(1)}\) yields
\(N^{2k-2k\sigma+o(1)}+TN^{k-2k\sigma+o(1)}\), the two structural terms
of GM equation (13.4).

`OBSERVED`: the powered-coefficient bound and log-loss absorption belong to
Stream B. Thus this pins the MVT input but does not certify GM's full MVT
branch.

## Replay

Run from the project root:

```sh
python3 proof/check_cycle_2_stream_a_sources.py
```

It verifies hashes and source-anchor strings, not the cited theorems.
