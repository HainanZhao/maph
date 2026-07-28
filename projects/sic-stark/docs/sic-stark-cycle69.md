# SIC--Stark research cycle 69: fixed-point divisibility is equivalent to TCC

## Outcome

The fixed-point divisibility proposal from cycle 68 is not a smaller
analytic lemma.  For the dimension-six stabilizer it is exactly equivalent
to the desired fixed-point identity.

Let

\[
 A=\begin{pmatrix}115&-24\\24&-5\end{pmatrix},
 \qquad
 \beta=\frac{5+\sqrt{21}}2.
\]

Direct calculation gives

\[
\begin{aligned}
 A\tau-\tau
 &=\frac{115\tau-24}{24\tau-5}-\tau\\
 &=-24\,\frac{\tau^2-5\tau+1}{24\tau-5}.
\end{aligned}
\]

The numerator is the minimal polynomial of \(\beta\).  Its discriminant is
\(21\), so its two roots are simple.  Moreover

\[
 24\beta-5=\beta^3
\]

is a unit of norm one.  Hence \(A\tau-\tau\) is a local uniformizer at
\(\beta\):

\[
 (A\tau-\tau)=(\tau-\beta)
\]

as principal ideals in the local holomorphic ring at \(\beta\).

It follows for every holomorphic defect entry \(F(\tau)\) that

\[
 (A\tau-\tau)\mid F(\tau)
 \quad\Longleftrightarrow\quad
 F(\beta)=0.
\]

Taking \(F\) to be an entry of \(K_6(\tau)^2-K_6(\tau)\) proves:

\[
\boxed{\text{fixed-point divisibility}\iff
       K_6(\beta)^2=K_6(\beta).}
\]

Thus the \(O(|A\tau-\tau|)\) behavior observed on rational convergents is
consistent with TCC, but proving that bound would already prove TCC.  It
cannot bypass the remaining constant-term cancellation.

## Consequence for the proof program

Cycle 68's proposed thirteen-equation divisibility program should not be
presented as a weaker substitute for the mixed-signature special-value
identity.  The two viable routes remain:

1. prove the single Artin-labelled primitive Shintani value
   \(x_{\mathrm{an}}=x_{\mathrm{alg}}\); or
2. prove the constant term of the finite cyclic-dilogarithm convolution
   vanishes by an independent pentagon or star--triangle identity.

The first is one explicit rank-one Stark--Shintani case.  The second would
be a direct proof of TCC and must include a genuine parameter match, not
only the observed first-order decay.

## Reproducibility

- `scripts/dimension_six_fixed_point_equivalence.py`

