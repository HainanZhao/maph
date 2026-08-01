# Cycle 4 P1R-CRR finite-analogue probe preregistration v3 correction

## Disposition and boundary

`OBSERVED`: v1 is immutable and `CONTAINED_UNEXECUTABLE` because its family
maps, phase counts, proxy, and feasible precision rule were underspecified.
`OBSERVED`: v2 is immutable and unexecuted; it fixed those omissions but did
not state the dimensional cubic compression identity with enough precision to
rule out a wrong `2M`-dimensional diagonal subtraction.  Neither correction is
a research outcome or evidence about CRR compatibility.

V3 retains **exactly** v2's 160 row identifiers/order/seeds, scales, families,
variants, construction maps, phase counts, mutation and proxy rules,
thresholds, quadrature/mode choices, precision policy, 55-minute cap, 1-GiB
cap, and retention semantics.  It changes no scientific threshold or search
parameter.  It proves no continuous CRR statement, saturation theorem, density
estimate, or short-interval result.  Finite rows are `OBSERVED`; numerical
complex diagnostics are `RECOGNIZED`; an all-miss table is not a universal
negative.  Hostile review is deferred to paper stage.

## Explicit cubic rule

For `W` of cardinality `R`, let `U` be the `R x 2M` matrix
`U_(t,m)=exp(2*pi*i*m*t/H)` for nonzero `m` with `|m|<=M`, and let
`D=diag(1-|m|/(M+1))`.  The prescribed zero-diagonal matrix is

```text
B_M = A_R - M I_R,             A_R=U D U^*.
```

Writing `G=U^*U`, cyclicity gives `tr(A_R^k)=tr((D G)^k)` for `k>=1`, but the
subtracted identity has ambient dimension `R`, not `2M`.  Therefore the only
permitted cubic calculation is

```text
tr(B_M^3)=tr((DG)^3)-3M tr((DG)^2)+3M^2 tr(DG)-R M^3.
```

In particular, `tr((DG-M I_(2M))^3)` is prohibited.  This is an exact
algebraic implementation identity for the frozen finite proxy, not a new
analytic statement.

