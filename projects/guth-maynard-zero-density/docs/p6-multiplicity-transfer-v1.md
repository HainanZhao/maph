# P6 multiplicity transfer v1

## Claim boundary

`PROVED`: the elementary transfer below converts a bound obtained from a
well-spaced set of **distinct** Dirichlet zeros into the corresponding
multiplicity-weighted bound, at the cost of one local zero-count factor.

`CONJECTURED`/external for this project: the required uniform local input

\[
 \sum_{\substack{\rho:\,L(\rho,\chi)=0\\
                  \sigma\leq\Re\rho\leq1\\
                  u\leq\Im\rho<u+1}}
 m(\rho,\chi)\ \leq C\log(q(|u|+3))
 \tag{LC}
\]

for every character and relevant unit strip, with endpoint conventions
matched to the application. Its exact primary theorem and hypotheses remain
part of `S06_EXTERNAL_INPUTS`.

`OBSERVED`: Chen--Gupta--Li v2 defines its zero count as the “number of
zeros” in the rectangle without stating multiplicity, then uses cardinalities
of sets of zeros and cites a unit-height difference bound at TeX lines
2148--2158. This document does not amend that text or infer an unstated
convention.

No Dirichlet zero-density estimate is promoted here.

## Transfer lemma

Fix one character \(\chi\). Let \(Z_\chi\) be a finite multiset of zeros in
the target rectangle and let \(Z_\chi^*\) be its distinct support. Write
\(m(z)\) for the multiplicity of \(z\). Hypothesis (LC), applied to a unit
strip containing \(\Im z\), gives

\[
 m(z)\leq L_\chi,
 \qquad L_\chi:=C\log(q(T+3)).
\]

Therefore

\[
 |Z_\chi|_{\rm mult}
   =\sum_{z\in Z_\chi^*}m(z)
   \leq L_\chi |Z_\chi^*|.
\]

Summing over characters gives

\[
 \sum_\chi |Z_\chi|_{\rm mult}
 \leq L\sum_\chi |Z_\chi^*|,
 \qquad L=C\log(q(T+3)).
 \tag{1}
\]

This proof is label-preserving: multiplicity copies are attached to their
original \((\rho,\chi)\), and no copy is inserted into a well-spaced set.

More generally, suppose a saturated spacing selection at scale \(X\geq1\)
proves

\[
 |Z^*|\leq K(X,L)|W|,
\]

where \(W\) is a well-spaced subset of the distinct support. Combining this
with (1) yields

\[
 |Z|_{\rm mult}\leq L K(X,L)|W|.
\]

For the CGL usage \(X=(qT)^\epsilon\), every fixed power of \(\log(qT)\)
is \((qT)^{o(1)}\). Thus this transfer does not alter a stated density
exponent. It does not prove (LC), the detector, the fourth moment, or any
conductor-uniform constant.

## Gate effect

`PROVED`: `S03_MULTIPLICITY_NOT_STATED` is not an independent exponent or
selection obstruction once (LC) is supplied. It is reduced to the precise
multiplicity-inclusive local-count source obligation in S06.

`OBSERVED`: the remaining P6 obligations include the named external inputs,
the corrected \(T\)-smoothness gate, and conductor-sensitive intermediate
formulae. Paper-stage hostile audit remains deferred.

Replay:

```sh
python3 proof/p6_multiplicity_transfer_v1.py --check
python3 -m unittest tests.test_p6_multiplicity_transfer_v1 -v
```
