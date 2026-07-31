# Census-paper preregistration amendment v4: height calibration

Frozen: 2026-07-31 UTC, after the exact RQ-000245 proper-image anchor
passed and before any corpus-wide packet polynomial was synthesized.

## Claim boundary

This calibration is a resource-planning pass, not a proof of a packet
identity.  It may extract the exact Engine-A unit data and evaluate
high-precision logarithms, but it must not construct a packet
polynomial.  Its height outputs are tagged `OBSERVED`.  The subsequent
polynomial run remains subject to exact coefficient-size gates.

## Frozen population and inputs

Run over all 1,560 Q rows in stable RQ order.  Use only:

- `artifacts/w1-full-census-v1.json`, SHA-256
  `b656a587bea705e8efe817e2870a0ea86cbf2c10fa37c7d9aa03d3868dfa76f1`;
- `artifacts/engine-a-euler-degeneracy-v1.json`, SHA-256
  `f4ead3438d3b305fa42e73e1d979530a04104ce8d642db0b1c9ac85929bac033`;
- `data/engine-a-uniform-theorem-v1.json`, SHA-256
  `54469ec4ff4871bbf30e51f8f9f69037329f893e329009940d84b51026f4e0df`;
- `scripts/census_packet_conventions.gp`, SHA-256
  `805f53e896335824b762aad2125f3aa9c854fe8f207657e853720d2fdc3fadc6`.

No analytic packet target or previously synthesized Q-row polynomial
may be opened.

## Frozen predictor

For each nonvanishing supported quadratic character, compute the exact
rational Engine-A multiplier

\[
 c_\chi=E_\chi(h_L/h_K)(w_K/w_L)(2/I_\chi)
\]

and the convention-oriented relative unit \(u_\chi\).  At 100 decimal
digits evaluate

\[
 H=\frac{2}{|G|}\sum_\chi |c_\chi\log|u_\chi||.
\]

Let \(d\) be the exact cardinality of the effective Artin sign image;
set \(d=1\) when every Euler product vanishes.  Record

\[
 B=\left\lceil\frac1{\log 10}
 \max_{0\le j\le d}
 \left(\log {d\choose j}+\min(j,d-j)H\right)\right\rceil .
\]

`B` is a conservative planning predictor for decimal coefficient
digits, not a certified enclosure.  Record the full distribution of
`H`, `B`, common exponent denominators, effective-character counts, and
Artin-image sizes, together with the maximizing case ids.

## Cap rule frozen before measurement

Let \(B_{\max}\) be the largest observed `B`.  The corpus polynomial
digit cap is the smallest power of two at least
\(\max(256,2B_{\max})\).  If that rule exceeds 1,048,576 decimal digits,
do not authorize the corpus polynomial run.  Otherwise freeze the
resulting integer in a new amendment before synthesis.

During synthesis, exceeding the frozen digit cap, 2 GiB peak resident
memory, or 300 seconds for one row is a recorded resource failure.  It
does not authorize a method substitution or dropping the row.
