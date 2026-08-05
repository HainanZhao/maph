# C78 certification reinstatement after C79 endpoint proof

## Corrected status — PROVED

C78 v1's arbitrary-qubit compatible three-qubit pair-support theorem is now
certified. C78 correction v1 withdrew the `PROVED` label because its only
\(Q=I/2\) endpoint authority was Song--Chen Proposition 3, then available
only as an arXiv preprint. C79 independently proves exactly that endpoint and
is sealed as `cycle-79-b079-compatible-endpoint-foundation-v1`.

For the same compatible \(\rho_{ABC}\) and weights \(a,b,c\), C79 proves the
unnormalized-I inequality \(L_0\preceq R_0\). Positive homogeneity gives
\(L_0/2\preceq R_0/2\), precisely C78's \(H_{1/2}\preceq T_{1/2}\).
Thus Song--Chen is no longer an authority in the C78 proof chain.

Together with the already frozen pure endpoint, common local-unitary
diagonalization, affine \(Q_q=(1-t)I/2+tP_0\) decomposition, and common
ordered target spectrum, this reinstates the C78 conclusion:

\[
a\rho_{AB}\otimes Q_C+b\rho_{AC}\otimes Q_B+cQ_A\otimes\rho_{BC}
\preceq
aP_{00,AB}\otimes Q_C+bP_{00,AC}\otimes Q_B+cQ_A\otimes P_{00,BC}.
\]

It holds for every three-qubit density matrix, probability weights on
\(AB,AC,BC\), and qubit density matrix \(Q\). The \(AC\) term is in ambient
\(ABC\) order.

## Boundary and remaining work

This is a scoped case of the compatible-marginal spin-alignment conjecture.
It does not cover incompatible pair triples, other subset supports, more
parties, or higher local dimension. It is not a novelty certification:
Song--Chen Proposition 3 overlaps the endpoint, while the arbitrary-\(Q\)
interpolation needs the renewed paper-stage literature and hostile audit.

The two older C78 artifacts remain immutable historical records. This
reinstatement supersedes the certification withdrawal, not their bytes.
