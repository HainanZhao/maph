# P7-3 common ideal cubic v2 correction

`OBSERVED`: the immutable P7-3 v1 artifact has two presentation/replay
defects. Its finite \(\mathbb Z/2\) Parseval test stored `34.0`, not integer
`34`, because Python evaluates `(-1)**negative_integer` as a float. Its
single-character norm-fibre string wrote `1_(a,f)=1`, which is ambiguous.

`PROVED`: an integer-only replay gives the exact coloured energy and Parseval
count \(34\), with uncoloured time-multiset energy \(62\), and the corrected
fibre inequality is

\[
 \left|\sum_{N\mathfrak a=n}c(\mathfrak a)\chi(\mathfrak a)\right|^2
 \leq a_{\mathbb Q(i)}(n)\sum_{N\mathfrak a=n}|c(\mathfrak a)|^2
 \mathbf1_{(\mathfrak a,\mathfrak f_\chi)=1}.
\]

This is a versioned correction, not an edit of v1. It changes neither the
Gram/coloured-energy identities, the scoped non-verbatim-import conclusion,
nor the fact that a family-uniform coloured primitive cubic estimate remains
open. No hostile audit is initiated.

Replay:

```sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_common_ideal_cubic_v2_correction.py --check
python3 -m unittest tests/test_p7_common_ideal_cubic_v2_correction.py -v
```
