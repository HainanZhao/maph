# Dominant-embedding gauge

## Lemma

Let \(\bar\eta\in\bar U_K^-\) be a Roblot quartic weak solution and
fix the distinguished real place \(w\). Write

\[
\ell_j=\log|\eta^{\gamma^j}|_w,\qquad 0\le j<4.
\]

Since \(\gamma^2\) is complex conjugation in \(K/K^+\),

\[
(\ell_0,\ell_1,\ell_2,\ell_3)=(a,b,-a,-b).
\]

If \(|a|\ne|b|\), exactly one member of the trivial-unit orbit has
maximal logarithm at \(w\). Selecting it defines a representative
\(\eta_{\mathrm{dom}}\) independently of the initial generator of the
free \(\mathbf Z[i]\)-module. Call this the dominant-embedding gauge.

## Proof

The four logarithms are \(a,b,-a,-b\). When \(|a|\ne|b|\), their
maximum is positive and occurs exactly once. Replacing the initial
weak solution by a conjugate cyclically permutes the four entries;
replacing it by its inverse negates them, which is the same
permutation by two places because
\(\bar\eta^{\gamma^2}=\bar\eta^{-1}\). Hence the selected orbit member
is unchanged.

## Character covariance

If the original deterministic representative is shifted by
\(\gamma^j\), the coefficient changes by \(i^{-j}\). Therefore, if
\(q\) is defined by

\[
L'(0,\chi)/c_\chi(\eta)=i^q,
\]

then the dominant-gauge label is

\[
q_{\mathrm{dom}}=q+j\pmod4,
\]

where \(j\) is the index of the maximum logarithm. Reversing the
oriented generator conjugates both \(L'\) and \(c\), so
\(q_{\mathrm{dom}}\mapsto-q_{\mathrm{dom}}\); this is the expected
character covariance.

## Controls

All five controls satisfy \(|a|\ne|b|\). Their dominant-gauge labels
are:

\[
\begin{array}{c|ccccc}
\text{case}&\mathrm{RQ\!-\!000129}&\mathrm{RQ\!-\!001280}&
\mathrm{RQ\!-\!001569}&\mathrm{RQ\!-\!001894}&
\mathrm{RQ\!-\!007519}\\ \hline
q_{\mathrm{dom}}&0&1&1&3&3.
\end{array}
\]

This repairs the gauge defect in the response variable. It does not
repair the frozen feature family, which is independently ill-defined.
