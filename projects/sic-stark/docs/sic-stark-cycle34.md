# SIC--Stark research cycle 34: the wild sextic satisfies Roblot P1

Date: 2026-07-27

## Outcome

The certified dimension-six unit

\[
 \eta=x^2
\]

satisfies Roblot's global index property (P1) **unconditionally**, even
though the extension is wildly ramified above \(3\).

This bypasses the tame hypothesis in Roblot's sextic existence theorem.
That hypothesis is needed to construct a solution abstractly; Proposition
4.1 applies directly once an explicit P1 unit has been supplied.

Let \(L/K\) be the cyclic sextic ray extension, let
\(\tau=\sigma^3\), and put \(E=L^{\langle\tau\rangle}\).  Exact
certification gives

\[
 \operatorname{sig}(L)=(6,3),\quad
 \operatorname{sig}(E)=(6,0),\quad
 h_L=h_E=1.
\]

The fixed field has polynomial

\[
 t^6+3t^5-12t^4-31t^3+36t^2+63t+7.
\]

The norm image of the eight fundamental units of \(L\) has index

\[
 [U_E:N_{L/E}U_L]=4=2^2,
\]

so \(e=2\).  The anti-unit lattice has rank three, and the three
\(\mathbb Z[C_3]\)-conjugates of \(\eta\) generate a sublattice of
index

\[
 [U_L^-:\mathbb Z[C_3]\eta]=8.
\]

At the top quadratic step, the unique prime above \(2\) is inert, while
the unique prime above \(3\) is ramified.  Hence

\[
 t_S=1,\qquad |\mathrm{Cl}_L^-|=h_L/h_E=1.
\]

Therefore

\[
 \boxed{
 [U_L^-:\mathbb Z[G]\eta]
 =8
 =2^{e+t_S}|\mathrm{Cl}_L^-|.
 }
\]

This is exactly P1.

Roblot's product formula, together with the already-proved quadratic
component, now gives

\[
 \boxed{
 |L'_S(0,\chi_1)|
 =
 \left|
 r_0+\zeta_6r_1+\zeta_6^2r_2
 \right|.
 }
\]

Thus the wild sextic absolute-value identity is unconditional.  Only its
complex argument remains.

## Reproducibility

- `scripts/dimension_six_roblot_index.gp`
- `scripts/dimension_six_primitive_fourier_audit.gp`
- `scripts/dimension_six_artin_orientation.gp`

## Source

X.-F. Roblot, *Index formulae for Stark units and their solutions*,
especially Proposition 4.1 and Section 7.
