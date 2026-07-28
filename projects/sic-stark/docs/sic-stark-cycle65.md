# SIC--Stark research cycle 65: the scale of the dimension-six defect

## Outcome

The corrected rational-boundary matrices exhibit second-order convergence
in the denominator of the modular approximant.  Let \(n_k\) be the
denominator and set

\[
 \epsilon_k=\|K_k^2-K_k\|_{\max}.
\]

For the first four reliable steps:

\[
\begin{array}{c|c|c}
n_k&\epsilon_k&n_k^2\epsilon_k\\ \hline
527&2.1832\cdot10^{-2}&6063\\
2525&1.0167\cdot10^{-3}&6483\\
12098&4.4422\cdot10^{-5}&6500\\
57965&1.9380\cdot10^{-6}&6511
\end{array}
\]

The covariance, reciprocity, primitive-entry, matrix-idempotency, and
Weyl-coefficient errors all decrease on these steps.  The stable values
of \(n_k^2\epsilon_k\) identify

\[
 \epsilon_k=O(n_k^{-2})
\]

as the correct target estimate.  This matches the quadratic
continued-fraction distance to the RM fixed point.

This is a numerical diagnosis, not yet a bound.  It rules out the need
for exponential estimates and suggests that the TCC defect is an
ordinary analytic function with a simple zero at that fixed point.

## Precision boundary

Direct double-precision cyclic products become unreliable around the
fifth step, whose denominator is already \(277727\).  Later
numerics should use either:

1. exact cyclotomic product rearrangements;
2. high-precision block products; or
3. the analytic first correction rather than direct summation.

The proof should not depend on pushing floating-point denominators
further.
