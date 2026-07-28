# SIC--Stark research cycle 120: two ideal-norm descents

Date: 2026-07-28

## Outcome

The index-504 construction is not isolated.  The native general-modular
level \(24=d(d-2)\) has the same structure.

At level \(24\), take the invariant lattice

\[
 2\mathcal O_K,\qquad B_{24}=2I,\qquad\det B_{24}=4=\frac{24}{6}.
\]

The column Weyl operators satisfy

\[
 X_{24}Y_{24}=\zeta_{24}^4Y_{24}X_{24}
=\omega_6Y_{24}X_{24}.
\]

Their sixth powers generate a subgroup of order \(4\), so its trivial
joint eigenspace has dimension \(24/4=6\).

Together with cycle 119, this gives two exact ideal-norm descents:

\[
\begin{array}{c|c|c|c}
N&\text{ideal}&N_{K/\mathbf Q}(\text{ideal})&\text{block dimension}\\
\hline
24&(2)&4=N/6&6\\
504&(2\sqrt{21})&84=N/6&6.
\end{array}
\]

Both ideals are preserved by multiplication by \(\beta\), so both blocks
carry the exact Zauner action.

## General lesson

This suggests a reusable higher-dimensional mechanism:

> Find an \(L_d\)-invariant ideal lattice of index \(N/d\) inside a
> natural modular or inter-level Heisenberg lattice of level \(N\).
> Its trivial sixth-power analogue should produce the \(d\)-dimensional
> Weyl block.

The dimension-six certificates are in
`scripts/dimension_six_heisenberg_descent.py`.
