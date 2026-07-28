# SIC--Stark research cycle 86: the six-factor AFK cocycle

The continued-fraction word of
\[
A_t=\begin{pmatrix}377&-144\\144&-55\end{pmatrix}
\]
is
\[
[3,3,3,3,3,3,0].
\]
Thus the generic AFK rank-one evaluator has six double-sine factors.
We transcribed the algorithm from the pinned Zauner.jl revision
`dcff219c986208ce900e2ddaaed8eae2bae6756f`, including the finite
\(q\)-Pochhammer factor, Rademacher phase, and even-dimensional signs.

The resulting 63 nonexceptional values agree with the ray-class
logarithms after the lower-conductor stabilizer power is inserted.
Both reconstructed shifted matrices are numerically idempotent and
rank one to better than \(10^{-9}\).

The convention audit is
`scripts/certify_dimension_eight_maximal_cocycle.py`.
It is deliberately labeled numerical; the exact finite proof is
separate.

