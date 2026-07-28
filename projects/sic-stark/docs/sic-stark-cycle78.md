# SIC--Stark research cycle 78: rigorous orientation isolation

The exact Artin labels reduce the quartic Fourier transforms to eight
independent Kopp partial-zeta differences.  Arb integration gives

\[
\begin{aligned}
L'_0&=8.281565738\ldots+5.457798022\ldots i,\\
L'_1&=-2.968853827\ldots+6.247666148\ldots i
\end{aligned}
\]

with rigorous radii below \(10^{-8}\).

At every upper-half-plane embedding of \(E_b\), the inverse certified
unit-log matrix sends the appropriate real and imaginary parts to one
of

\[
(0,2),\quad(-2,0),\quad(0,-2),\quad(2,0),
\]

with coordinate radii below \(5\times10^{-9}\).  Since Stark's theorem
already guarantees integral unit coordinates, each ball contains
exactly one possible coordinate vector.  The quartic component of the
CM Stark unit is therefore forced to be the orbit of \(u_{b,3}^2\).

Reproduction:

```bash
PYTHONPATH=/path/to/python-flint:scripts \
  python3 scripts/certify_dimension_eight_cm_orientation.py
```
