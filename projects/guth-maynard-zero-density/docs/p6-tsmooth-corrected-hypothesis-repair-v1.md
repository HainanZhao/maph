# P6 F08: corrected-hypothesis T-smooth repair v1

## Outcome and claim boundary

`PROVED`: under the explicit amended hypothesis

\[
q\text{ is }T\text{-smooth}\quad\Longleftrightarrow\quad
T\geq1\text{ and every prime }p\mid q\text{ obeys }p\leq T,
\]

the needed divisor chain exists, including prime powers and equality at the
right endpoints. This is a theorem about the amended hypothesis, not a
definition supplied to Chen--Gupta--Li v2. The complete pinned TeX uses
`$T$-smooth` at TeX 182, 2266, 2346, and 2350 but does not define it.

`PROVED_CONDITIONAL`: with the existing primitive large-value input, the
qT-uniform detector transport and its stated external/multiplicity inputs,
the cited comparison envelopes, and the primitive-to-all transfer, the
amended smooth branch yields

\[
 \sum_{\chi\bmod q}N(\sigma,T,\chi)
 \ll_\epsilon(qT)^{(30/13)(1-\sigma)+\epsilon}.
\]

This does not validate or amend the CGL preprint, close P6, repair unrelated
`q_1`-sensitive rows, prove an unconditional density estimate, or start a
hostile audit. The historical F08 source gap remains recorded upstream.

## The divisor chain

Put \(Q=qT\), \(X=Q^v\), and \(0<v<5/6\). If
\(q^{5/6}<X\), take the one-element chain \(d_0=q\). Otherwise take the
largest divisor \(d_0\mid q\) with \(d_0^{5/6}<X\). If \(d_j<q\), choose
a prime whose exponent in \(d_j\) is below its exponent in \(q\), and set
\(d_{j+1}=d_jp\). Then \(d_{j+1}\mid q\) and

\[
d_j<d_{j+1}\leq T d_j.
\]

For the first step, maximality gives \(d_1^{5/6}\geq X\), hence
\(X\leq(d_0T)^{5/6}\). At every later step,
\(d_{j+1}^{5/6}\leq(d_jT)^{5/6}\), so the closed intervals
\([d_j^{5/6},(d_jT)^{5/6}]\) overlap. They cover
\([X,Q^{5/6}]\) and end at \((qT)^{5/6}\).

This handles `p=T` without a lost endpoint. Repeated choice of the same
prime handles prime powers. When \(1\leq T<2\), smoothness forces \(q=1\);
when \(T=1\), necessarily \(q=1\) and \(Q=1\), a compact degenerate case
rather than an asymptotic divisor-chain case.

## The essential correction to the source sketch

Later chain divisors can satisfy \(d^{5/6}>Q^v\). Therefore it is not valid
to call each later interval “Case 2” verbatim. Instead, on the interval

\[
d^{5/6}\leq N^k\leq(dT)^{5/6},
\]

the actual middle subdivision has \(T_0=N^{6k/5}/d\in[1,T]\). Its source
large-value input yields, conditionally,

\[
 |W|\ll Q^{1+o(1)}(N^k)^{(12-20\sigma)/5}.
\]

With the fixed \(v=5/(3+5\sigma)\), \(N^k\geq Q^v\), and the negative
exponent,

\[
 Q(N^k)^{(12-20\sigma)/5}
 \leq Q^{1+v(12-20\sigma)/5}
 = Q^{3v(1-\sigma)}
 = Q^{15(1-\sigma)/(3+5\sigma)}.
\]

The optimal term is also absorbed because \(N^k\leq Q^{5/6}\) and
\(5/3\leq3v\). Thus the chain really does close the amended smooth
large-value branch, conditional on its analytic input, without a false
case-label assertion.

## Dependencies that remain conditional

- `S03_MULTIPLICITY_NOT_STATED` remains open.
- `S06_EXTERNAL_INPUTS` remains open, including the exact cited
  Ingham/Huxley/fourth-moment hypotheses.
- The qT detector-tail lemma remains conditional on its recorded growth,
  fourth-moment, and low-height inputs.
- The primitive-to-all lemma applies only after a uniform monotone primitive
  envelope is available. It does not justify arbitrary intermediate
  expressions involving a source-selected `q_1`.

## Replay and identities

From the project directory:

```sh
python3 proof/p6_tsmooth_corrected_hypothesis_repair_v1.py --check
python3 -m unittest tests/test_p6_tsmooth_corrected_hypothesis_repair_v1.py -v
```

- Script SHA-256: `3f3feca3273a6ae88c05c8273d04bf3f9883c9d53328a3684657b839465c69a7`
- Artifact SHA-256: `5097609783b4e076b268255445e94caeb08bc23f93ad2540703c43e1401ca8af`
- Test SHA-256: `51622527a9023332656738636a53d351781e74e718636dda0215b0136e0be3ed`

The replay uses CPython 3.12.3 on Linux, enforces a 60-second wall cap and a
one-GiB RSS cap, and records the resource convention in the artifact. The
recorded local replay took under one second and used about 20 MiB peak RSS.
