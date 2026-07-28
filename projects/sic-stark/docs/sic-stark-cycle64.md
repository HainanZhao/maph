# SIC--Stark research cycle 64: signed Zauner reduction in dimension six

## Outcome

The apparent failure of Zauner invariance in the regularized rational
tables is completely explained by the even-dimensional Weyl wrap sign.
If an integral label

\[
 (a,b)=(a_0+6m,b_0+6n)
\]

is reduced to \((a_0,b_0)\in(\mathbf Z/6\mathbf Z)^2\), then

\[
 D_{a,b}=(-1)^{a_0n+b_0m}D_{a_0,b_0}.
\]

For

\[
 L^{-1}=\begin{pmatrix}0&1\\-1&5\end{pmatrix},
\]

this gives a signed action

\[
 (a,b)\longmapsto (b,-a+5b)\pmod6
\]

with precisely the signs observed in the boundary packet.  Once these
signs are retained, the covariance error decreases rapidly along the
modular geodesic.

## Exact orbit reduction

The signed Zauner action has fourteen label orbits, including zero.
Thus it reduces the nonzero TCC coefficients from \(35\) to \(13\).
The cocycle inverse law is also visible numerically as

\[
 \nu_p\nu_{-p}=\varepsilon(p),
\]

where \(\varepsilon(p)\) is the same even-dimensional wrap sign.
However, this relation is multiplicative, not Hermitian conjugation.
The ghost matrix is not known to be Hermitian, so it does **not** by
itself identify the defect equations at \(p\) and \(-p\).  The safe
linear reduction therefore remains

\[
 \boxed{13\text{ nonzero representatives}.}
\]

This distinction avoids importing an orthogonal-projector hypothesis
into a theorem whose natural conclusion is a rank-one idempotent.

## Numerical covariance check

For the first four corrected rational-boundary tables, the maximum signed
covariance defects are

\[
 1.43\cdot10^{-1},\quad
 6.41\cdot10^{-3},\quad
 2.80\cdot10^{-4},\quad
 1.22\cdot10^{-5}.
\]

The corresponding unsigned comparison has persistent order-one errors
because it compares entries whose Weyl representatives differ by a wrap
sign.

## Consequence for the proof

It is enough to prove convergence to zero for thirteen representative Weyl
coefficients of \(K_k^2-K_k\).  Every remaining coefficient follows by
signed Zauner covariance.  The inverse relation may permit a later
nonlinear reduction, but it is not used here.

The exact audit is:

```bash
python3 scripts/dimension_six_defect_limit.py
```
