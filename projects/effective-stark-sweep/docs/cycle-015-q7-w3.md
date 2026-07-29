# Cycle 015 — W3 exact packet and Arb closure

The exact candidate packet is the reciprocal degree-six polynomial
printed in `data/q7-p7-case-v1.json`. Its absolute polynomial is
irreducible, defines the one-place ray field over the labeled base,
has signature \((6,3)\), class number one, six disjoint Sturm windows,
and split-prime Frobenius generators at 19 and 31.

For the class represented by \((3)^r\), choose
\[
 \lambda_r=(7-2\sqrt7)/3^r,\qquad \epsilon=8+3\sqrt7.
\]
In coordinates for \(\mathfrak p_7/(3)^r\), the cone lattice generated
by \(\lambda_r,\lambda_r\epsilon\) has matrix
\(\left(\begin{smallmatrix}1&2\\-2&5\end{smallmatrix}\right)\), hence
determinant nine. Exact enumeration gives nine points in the half-open
parallelotope for every ray class. Yamamoto's factorization and
place-change relation reduce the one-place difference to twice the
logarithm of this real-place double-sine product.

The 27 independent double-sine values (the other 27 follow from exact
complement symmetry) were enclosed using Arb and interval
fourth-derivative Simpson bounds. No PARI \(L\)-value enters this
certificate. All six analytic log balls contain the logs of the six
Sturm-isolated algebraic roots.

- For quotient degree \(3\le d\le24\), Voutier gives lower bound
  \(5.2279\times10^{-5}\).
- For \(d=1\), the quotient is rational and positivity eliminates
  \(-1\).
- For \(d=2\), a non-torsion quotient has height at least
  \(\tfrac12\log\phi\), while positivity again orients the torsion
  case.

The powered height upper bound is \(9.191\times10^{-9}\), so the
certified Voutier margin is \(>5688\), against the preregistered
requirement \(100\). Therefore the explicit packet identity is
`VERIFIED`. The earlier high-precision `bnrL1` transcript remains
`NUMERICAL` and is not part of this proof.
