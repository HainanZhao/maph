# Cocycle covariance audit

The supplied-tuple multiplier is

\[
M(A,\boldsymbol r)
=-\Psi(A)/12-t_A(\boldsymbol r)\pmod{\mathbf Z}.
\]

For the frozen level stabilizers, \(A\boldsymbol r\equiv\boldsymbol r\)
modulo \(\mathbf Z^2\). Direct substitution in the quadratic
theta-character expression gives

\[
\Psi(A^{-1})=-\Psi(A),\qquad
t_{A^{-1}}(\boldsymbol r)=-t_A(\boldsymbol r)\pmod{\mathbf Z},
\]

and hence

\[
M(A^{-1},\boldsymbol r)=-M(A,\boldsymbol r).
\]

The exact replay checks this for the dimension-four characteristic and
all 24 dimension-five lifted characteristics. Thus reversing the
oriented generator conjugates the cocycle multiplier, exactly as it
conjugates \(L'(0,\chi)\).

Weak-unit gauge covariance is separate. Conjugating a Roblot weak
solution changes its coefficient by a fourth root of unity, while the
cocycle tuple is unchanged. The dominant-embedding gauge removes that
freedom on all five controls, as proved in
`docs/dominant-embedding-gauge-v1.md`. A future character-level bridge
must compare against that canonical representative or prove an
equivalent intrinsic normalization.
