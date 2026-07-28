# SIC--Stark research cycle 49: AFK-to-double-sine convention translation

## Result

The canonical principal-overlap evaluator has been aligned with the AFK
phase formula and the authors' implementation.

For \(r=-p-q\pmod 7\), the normalized principal overlap is

\[
\widetilde\nu_{p,q}
=(-1)^{7(p+q)+pq+\min(7,p+q)}
\prod_{\rm cyc}
S_2^{\rm rec}\!\left(
1+\frac{q\beta-p}{7}\,\middle|\,\beta,1
\right),
\]

where \(\beta=3+2\sqrt2\), the product is over
\((p,q,r)\mapsto(q,r,p)\), and

\[
S_2^{\rm rec}
=\operatorname{Sin}_{2,\mathrm{Kopp}}^{-1}.
\]

This is exactly the convention implemented in the authors'
`Zauner.jl` principal-ghost routine at commit
`dcff219c986208ce900e2ddaaed8eae2bae6756f`.

The sign in this real formula is the result after multiplying the raw
Shintani--Faddeev value by

\[
\phi_p=\zeta_{56}^{7-32Q(p)}.
\]

It must not be confused with the phase of the raw cocycle itself.

## Scope

This translation closes the executable convention dictionary.  For a
publication proof, the three \(S\)-factors should still be obtained
line-by-line from a word for \(A=L^3\); citing software alone is not a
substitute for that derivation.

## Sources

- AFK Definitions 1.30 and 1.32 and Theorem 5.6,
  <https://arxiv.org/abs/2501.03970>.
- Kopp's double-sine and samech conventions,
  <https://arxiv.org/abs/2411.06763>.
- Authors' implementation,
  <https://github.com/sflammia/Zauner.jl>.

