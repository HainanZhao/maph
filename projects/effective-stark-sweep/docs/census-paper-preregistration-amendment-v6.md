# Census-paper preregistration amendment v6: independent Arb route

Frozen: 2026-07-31 UTC, after materializing the deterministic 50-row
sample and before computing any independent analytic value for it.

The selected ids and their SHA-256 ranks are fixed in
`data/census-paper-q-arb-sample-v1.json`, SHA-256
`e01a050f8ab40d7c18445ac404cc71a79cc5b727f2420ed5b6993eda4cf221ef`.

## Independent route

For each nonzero quadratic character, independently construct its
primitive quadratic extension \(L/K\).  Do not compute or read the
relative-unit norm kernel, determinant index, selected packet factor,
or packet-polynomial roots.

Use

\[
 L'_K(0,\chi_{\rm prim})
 = \frac{\zeta_L^*(0)}{\zeta_K^*(0)}
 = \frac{h_LR_L/w_L}{h_KR_K/w_K}.
\]

Multiply by the exact imprimitive Euler product.  Compute \(R_K\) and
\(R_L\) from the complete PARI fundamental-unit systems, but evaluate
all algebraic embeddings and logarithmic determinants independently
with python-flint/Arb at 192 bits.  Quartic fields must pass
`bnfcertify`.

The exact-route comparison value for each character is reconstructed
only after the independent ball is frozen, from the corpus powered
trace:

\[
 L'_K(0,\chi)
 = \frac{|G|}{2q}\operatorname{arcosh}(t_{\chi,q}/2).
\]

For each exact Artin sign row, apply the Fourier factor \(2/|G|\) to
both sets of character values.  This checks every distinct packet
class represented in the effective Artin image.

## Acceptance

- Start at 192 bits.
- Add a target-independent radius \(10^{-45}\) to every independent
  character ball.
- The inflated ball must contain the complete exact-trace-derived Arb
  interval.
- Every Artin-class difference ball must contain zero and have radius
  below \(10^{-38}\).
- All-zero rows must have no independent field call and must check
  exactly as packet logarithm zero.

Any failure is preserved under its stable RQ id and leaves the
analytic audit table open.  It does not remove or alter the exact
packet corpus.
