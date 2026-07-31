# Gauge-ambiguity lemma

## Statement

Let \(G=\langle\gamma\rangle\simeq C_4\), let
\(\chi(\gamma)=i\), and put

\[
c_\chi(\eta)=\frac12\sum_{r=0}^3
i^r\log|\eta^{\gamma^r}|.
\]

Then, for every \(j\in\mathbf Z\),

\[
c_\chi(\eta^{\gamma^j})=i^{-j}c_\chi(\eta),
\qquad
c_\chi(\eta^{-\gamma^j})=-i^{-j}c_\chi(\eta).
\]

Consequently the quarter-turn integer in
\[
L'(0,\chi)/c_\chi(\eta)\in\mu_4
\]
is not an invariant of Roblot's weak solution, because his Theorem 6.1
determines that solution only up to the trivial units
\(\{\pm\gamma^j\}\). The invariant assertion is only

\[
\arg L'(0,\chi)-\arg c_\chi(\eta)
\in(\pi/2)\mathbf Z.
\]

## Proof

Write
\(\ell_r=\log|\eta^{\gamma^r}|\), with indices modulo four. Then

\[
\begin{aligned}
c_\chi(\eta^{\gamma^j})
 &=\frac12\sum_{r=0}^3i^r\ell_{r+j}\\
 &=\frac12\sum_{t=0}^3i^{t-j}\ell_t
 =i^{-j}c_\chi(\eta).
\end{aligned}
\]

Inversion changes every \(\ell_r\) to \(-\ell_r\), giving the second
formula. Since \(j\) is arbitrary, all four quarter-turn labels occur
within the same trivial-unit orbit. This proves the claim.

## Consequence for this project

The five labels \(3,0,3,3,0\) recorded in
`artifacts/all-five-phase-gates-v1.json` are valid replay diagnostics
for the frozen deterministic unit basis. They are not arithmetic
response variables that a Dedekind-sum formula may meaningfully fit
without first supplying an additional canonical gauge.

The original empirical fitting plan therefore has an identifiability
defect even after its independence defect is repaired.
