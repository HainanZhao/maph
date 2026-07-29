# Cycle 008 — composite-\(2^m\) fast-CBC mapping

Date: 2026-07-29

For \(m\ge3\),

\[
U(2^m)=\langle-1\rangle\times\langle5\rangle
       \cong C_2\times C_{2^{m-2}}.
\]

The Bernoulli kernel and the running product satisfy
\(F(k)=F(-k)\) and \(P(k)=P(-k)\), so candidate signs are quotiented.
However, nonunit indices cannot be placed in the full unit cycle.
Every nonzero \(k\) is first written \(k=2^v q\), with
\(q\in U(2^{m-v})\). On that stratum multiplication by candidate
\(5^a\) is a cyclic shift modulo \(2^{m-v-2}\). Thus the candidate
score is:

- the \(k=0\) contribution;
- candidate-independent contributions for residual unit moduli 2 and
  4; and
- one plus-shift NTT correlation for each larger valuation stratum.

The strata partition every nonzero residue exactly. In an **internal
consistency check**, all 256 modular candidate scores for the frozen
UNSW \(N=1024\), dimension-9 generator prefix agree between direct
modular enumeration and the stratified evaluator over the same prime.
No published Kuo merit value was compared in this cycle.

Local Python measurements show the expected scaling separation, but
they remain `NUMERICAL`. The artifact
`certificates/cycle-008-power2-fastcbc.json` records exact score digests
and timings.

| \(N\) | Direct enumeration | Stratified NTT | Minimum ratio |
|---:|---:|---:|---:|
| 256 | 6.17 ms | 1.87 ms | 3.30× |
| 1,024 | 93.3 ms | 7.50 ms | 12.4× |
| 4,096 | 1.60 s | 35.2 ms | 45.5× |

Decision: **MAPPING VERIFIED; proceed to compiled multi-prime NTT**.
