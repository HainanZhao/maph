# SIC--Stark research cycle 123: the coefficient-polarized blocks

Date: 2026-07-28

For \(d=6\), the general modular gamma dictionary is

\[
 \mu_b=1+b(4\beta-1),\qquad
 h_{a,b}=b-4a-1\pmod {24}.
\]

At fixed \(b\), the six discrete arguments form

\[
 W_r=\operatorname{span}\{|r+4\ell\rangle:\ell\in\mathbf Z/6\},
 \qquad r=b-1\pmod4.
\]

On \(W_r\), the operators \(P^4\) and \(U\), after removing the scalar
\(\zeta_{24}^r\), are the standard level-six shift and clock. Thus the
AFK samples themselves already select six-dimensional Heisenberg
representations. They use four coefficient polarizations
\(W_0,\ldots,W_3\), not initially the \((2)\)-ideal polarization found
in cycle 120.

The exact ledger is
`scripts/dimension_six_level24_blocks.py`.
