# Cycle 113 — B5-025 Euler-deletion transport batch

For a target modulus `m' = m q` with `q` coprime to `m`, suppose the
exact ray-class map identifies target and source labels.  If
`q = product p_i^{e_i}`, only the distinct prime ideals occur in the
imprimitive Euler product:

\[
 L_{m'}(s,\chi)=\prod_i(1-\chi(\mathfrak p_i)N\mathfrak p_i^{-s})
 L_m(s,\chi).
\]

For the odd character part, rank-one vanishing at zero removes the
derivative of the finite Euler product.  Character inversion then
gives

\[
 X_{m'}(A)=\prod_{J\subseteq\{1,\ldots,r\}}
 X_m\!\left(A\prod_{j\in J}\mathfrak p_j^{-1}\right)^{(-1)^{|J|}}.
\]

The source entries are positive at the fixed split real embedding, so
this product/quotient has the required positive orientation.  This is
the multi-prime form of Cycle 108; a repeated exponent `e_i>1` still
contributes the prime only once, because Euler deletion removes the
local factor once.

The proof applies in Cycle 112 only after the sealed RQ-000190 source
certificate integrity check and fresh exact target gates.  It does not
cover targets where the added ideal shares a prime with the source
modulus or where the fixed generator labels are not preserved.
