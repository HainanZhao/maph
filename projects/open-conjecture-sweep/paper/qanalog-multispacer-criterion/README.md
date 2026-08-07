# Aligned-Center Criteria for Products with Multiple q-Integer Spacers

Author: Hainan Zhao

This working archive contains one combined criterion paper. It proves:

1. the sufficient direction of Connelly--Ito--Martinez--Shevchenko--Yang
   Conjecture 5.4 for every `k>=1` and `r>=2`; and
2. a hybrid sufficient criterion for any finite number of spacer factors,
   with no coprimality requirement.

The hybrid first absorbs disjoint divisibility pairs and then applies a
nonnegative integer allocation matrix to the residual product. It is not a
necessary condition and does not characterize all unimodal products.

## Exact verification

From the repository root:

```sh
python3 proof/qanalog_multispacer_criterion.py
```

From this directory, build the manuscript twice:

```sh
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

The finite computations are regression evidence. The universal results rest
on the recursion, center calculation, allocation induction, and absorption
factorization in the manuscript.
