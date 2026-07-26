# Equal-price routing algorithm

## Exact reduction to subset resource allocation

Assume every pool has common initial price \(p=b_i/a_i\) and common fee
factor \(\gamma\).  For an active subset \(S\), let

\[
A_S=\sum_{i\in S}a_i,\qquad q(S)=\sum_{i\in S}q_i.
\]

The unique gross-output-maximizing split is

\[
x_i=\frac{a_i}{A_S}Q,\quad i\in S,
\]

and its net output is

\[
V(S)=
\Phi(A_S)-q(S),\qquad
\Phi(A)=\frac{p\gamma QA}{A+\gamma Q}.
\tag{1}
\]

Therefore, when all \(a_i\) are positive integers, it is enough to compute

\[
C(A)=
\min\left\{
\sum_{i\in S}q_i:
\sum_{i\in S}a_i=A
\right\}
\]

with the standard subset-sum dynamic program and choose the reachable
\(A>0\) maximizing \(\Phi(A)-C(A)\).

**Proposition.**  The algorithm returns a globally optimal gas-aware route
in \(O(m\sum_i a_i)\) time and \(O(\sum_i a_i)\) value-table memory, apart
from reconstruction storage.

**Proof.**  Equation (1) shows that all subsets with the same aggregate
reserve \(A\) have the same gross output.  Among them, only the one with
minimum fixed cost can be optimal.  The dynamic program computes that
minimum for every attainable \(A\); maximizing over its complete list of
states is therefore equivalent to maximizing over all subsets.  The stated
complexity is the usual reverse-update subset-sum complexity. \(\square\)

This is pseudo-polynomial, not polynomial in the binary input length.  That
boundary is consistent with the candidate weak-NP-hardness reduction.

## Reserve discretization

For arbitrary real reserves, choose a quantum \(\delta>0\) and replace

\[
a_i\quad\text{by}\quad
\widetilde a_i=\delta\lfloor a_i/\delta\rfloor.
\]

Optimize the discretized problem while keeping each subset's true gas cost.
For every subset \(S\),

\[
0\leq A_S-\widetilde A_S<m\delta.
\]

Moreover,

\[
\Phi'(A)=
\frac{p\gamma^2Q^2}{(A+\gamma Q)^2}
\leq p.
\]

The derivative at zero is \(p\), independently of \(\gamma\), so the
uniform safe bound is

\[
0\leq\Phi(A_S)-\Phi(\widetilde A_S)<pm\delta.
\tag{2}
\]

If \(\widehat S\) maximizes the discretized objective and \(S^\star\)
maximizes the true objective, then

\[
V(\widehat S)
\geq \widetilde V(\widehat S)
\geq \widetilde V(S^\star)
>V(S^\star)-pm\delta.
\tag{3}
\]

Thus flooring gives an additive \(pm\delta\) guarantee.

## Important correction found during derivation

The first implementation draft described the derivative bound as
\(p\gamma\).  That is false: because \(p=b_i/a_i\) is the reserve price
before the fee, the derivative of (1) at \(A=0\) is \(p\), independently of
\(\gamma\).  The code and tests must use the safe \(pm\delta\) guarantee.

## Practical limitation

The DP is compelling only when reserves have moderate effective dynamic
range after scaling.  Raw on-chain reserve integers can be enormous, making
the exact pseudo-polynomial table useless without discretization.  The next
benchmark must compare certified loss versus state count and must not call
the method scalable merely because it avoids \(2^m\) enumeration.
