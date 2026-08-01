# Cycle 1 — Route B exact baseline audit

Claim boundary: this route independently checks the rational exponent algebra
which turns the cited zero-density inputs into the frozen global coefficient
and short-interval thresholds. It does not re-prove Ingham's, Huxley's, or
Guth--Maynard's analytic estimates, and it does not independently prove an
explicit-formula or mean-square estimate.

## Outcome

`PROVED` conditional on the source inputs below: the exact three-case
comparison gives the uniform coefficient
\[
b=\frac{30}{13},
\]
with its critical equality at \(\sigma=7/10\). The source's uniform
sufficient criterion converts this to \(\theta=1-1/b=17/30\).

`REPLAYED`: the source's almost-all reduction uses the distinct criterion
\(T<X^{2/b-\epsilon}\), together with \(y\geq\delta X\) and
\(\delta=X^{-2/b+\epsilon/2}\). Its exponent conversion is exactly
\(\theta=1-2/b=2/15\). This route has checked that arithmetic, but has **not**
independently derived the mean-square/explicit-formula criterion. Thus
`2/15` must remain labelled a source replay in the G0 record until a separate
route reconstructs that analytic argument.

No new zero-density estimate, no short-interval improvement, and no
saturation theorem is claimed.

`PROVED` conditional on Theorem 1.1 and the classical large-values inequality
(1.1): at the critical cell \(N=T^{4/5}\), \(V=N^{3/4}=T^{3/5}\), the three
new-bound term exponents are \(10/25,12/25,13/25\), so their maximum is
\(13/25\). The classical first term is \(10/25\); its two alternatives inside
the minimum both have exponent \(15/25=3/5\). Therefore the critical-cell
gain is exactly \(3/5-13/25=2/25\). The equality of the two classical
min-branches is explicitly certified, so this does not hide a branch choice.

## Frozen source inputs and checked hypotheses

The source inspected in this run was the arXiv source archive
`2405.20552v2`, downloaded from
`https://export.arxiv.org/e-print/2405.20552v2`.

- Tarball SHA-256:
  `9d34ac093abcb8129f68ff86eaad65f09a09d832fe637ff84d50a69496046bdc`.
- TeX member `LargevaluesDirichlet17.tex` SHA-256:
  `36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.
- Lines 96–160 give the counting convention, Ingham and Huxley inputs,
  Theorem 1.2, and the two stated corollaries. Lines 2307–2402 give the
  published `7/10` and `8/10` zero-density case boundaries. Lines 2407–2471
  give the stated explicit-formula criteria used here.
- Lines 64–91 state Theorem 1.1 and the classical comparison inequality
  (1.1), including their coefficient, spacing, interval, and large-value
  hypotheses.

The fixed convention is
\[
N(\sigma,T)=\#\{\rho:\zeta(\rho)=0,\ \Re\rho\geq\sigma,
|\Im\rho|\leq T\},
\]
with multiplicity. Write a density input as
\(N(\sigma,T)\leq T^{A(\sigma)(1-\sigma)+o(1)}\).

The checked source inputs are
\[
A_I(\sigma)=\frac3{2-\sigma},\qquad
A_G(\sigma)=\frac{15}{3+5\sigma},\qquad
A_H(\sigma)=\frac3{3\sigma-1}.
\]
The frozen audit domain is \([1/2,1]\). The proof partition is `Ingham` on
\([1/2,7/10]\), `Guth--Maynard` on
\([7/10,4/5]\), and `Huxley` on \([4/5,1]\). Denominators are strictly
positive on their respective intervals.

For the critical large-values check, the frozen hypotheses are \(|b_n|\leq1\),
one-separated \(t_r\in[0,T]\), and
\(\left|\sum_{n=N}^{2N}b_nn^{it_r}\right|\geq V\) for every \(r\). The
certificate evaluates **every** term:
\[
\begin{array}{c|ccc}
&N^2V^{-2}&N^{18/5}V^{-4}&TN^{12/5}V^{-4}\\
\hline
\text{Theorem 1.1 T-exponent}&10/25&12/25&13/25
\end{array}
\]
while the classical terms \(N^2V^{-2}\), \(TNV^{-2}\), and
\(TN^4V^{-6}\) have exponents \(10/25,15/25,15/25\). Exact positive
differences order the first row, and the classical minimum branches tie.

## Exact case analysis

The crossover is certified by clearing positive denominators:
\[
A_I-A_G=\frac{30\sigma-21}{(2-\sigma)(3+5\sigma)}.
\]
It has the sole root \(\sigma=7/10\), and both coefficients there equal
\(30/13\).

For \(b=30/13\), the positive-denominator numerators for the three proof
cases are
\[
\begin{aligned}
b-A_I&=\frac{21-30\sigma}{13(2-\sigma)},\\
b-A_G&=\frac{150\sigma-105}{13(3+5\sigma)},\\
b-A_H&=\frac{90\sigma-69}{13(3\sigma-1)}.
\end{aligned}
\]
Their signs establish \(A(\sigma)\leq30/13\) in every case. This is a
polynomial sign certificate, not numerical sampling.

## Replay

The certificate is [cycle-1-route-b-baseline.json](../artifacts/cycle-1-route-b-baseline.json).
It uses only Python's standard library:

```sh
python3 projects/guth-maynard-zero-density/proof/replay_baseline_route_b.py --check projects/guth-maynard-zero-density/artifacts/cycle-1-route-b-baseline.json
```

The project-local test command is:

```sh
python3 -m unittest discover -s projects/guth-maynard-zero-density/tests -p 'test_*.py'
```

The artifact pins the replay script SHA-256. Regenerate it after an authorized
script change; any resulting change is a new versioned certificate, not a
silent replacement of a certified record.
