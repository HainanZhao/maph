# Cycle 6 CRR all-row phase-flatness gate v1

## Claim boundary

`PROVED`: this note gives an exact finite-dimensional lower bound for the
all-row flatness factor in the capped leading-eigenvector construction, under
two explicitly defined row statistics. Applied below, those statistics are
computed from the actual CRR matrix

```text
M_W(t,n)=w(n/L)n^(it)
```

on one fixed `W`, with the same coefficient cap and the same actual
Farey/RationalMass context as the preceding reductions. It also gives two
exact abstract matrix countermodels. Together they show that a large top
eigenvalue, right-eigenvector delocalization `rho`, equal row norms, and even
ordinary nonzero Gram connectivity do not by themselves control `phi`.

`CONJECTURED`: no actual Dirichlet set `W` is proved to satisfy the new row
statistics under `RationalMass(v)`, and no inverse theorem deriving them from
the actual Farey kernel is proved. This note does not prove AFARI, FARI,
CFARI, CRR-U, a compatible witness, a cubic estimate, a density gain, a
short-interval theorem, a saturation theorem, or an L-function result.

The abstract countermodels below are not asserted to have the Dirichlet form
of `M_W`, to be separated time sets, or to satisfy any Farey or RationalMass
condition. Their scope is only to rule out a derivation based on the named
matrix summaries alone.

## Exact decomposition of the phase-rounded top mode

Let `M` be any complex `m x N` matrix, let `lambda>0` be a chosen top
singular value squared, and choose unit singular vectors

```text
M M^* u=lambda u,       x=M^*u/sqrt(lambda),       ||u||_2=||x||_2=1.
```

Put

```text
b_n^ph=x_n/|x_n|  (zero when x_n=0),
c=<x,b^ph>=||x||_1=sqrt(N rho),
q=b^ph-c x,
r=Mq,
rho=||x||_1^2/N.
```

`PROVED`: `q` is orthogonal to `x`, and the exact orthogonal decomposition is

```text
M b^ph=c sqrt(lambda) u+r,
||M b^ph||_2^2=lambda c^2+||r||_2^2.                 (1)
```

The first summand is the desired top mode. The second is the precise
phase-rounding leakage that can cancel it at individual rows.

Define the two all-row statistics

```text
mu_top(M,u)=m min_t |u_t|^2,

chi_ph(M,u)=max_t |r_t|/(c sqrt(lambda)|u_t|),
```

where `chi_ph=+infinity` if some `u_t=0`. Thus `mu_top` is the minimum
diagonal entry of the normalized top spectral projector, scaled by its mean;
`chi_ph` is a coordinatewise relative leakage. It is weaker than bounding
`||r||_infinity` against the smallest top coordinate, since it permits larger
residuals on larger `|u_t|` rows.

## `PROVED`: rowwise phase-coherence lemma

If `chi_ph(M,u)<=kappa<1`, then

```text
phi(M,u) >= ((1-kappa)/sqrt(1+kappa^2))*sqrt(mu_top(M,u)),       (2)
```

where

```text
phi(M,u)=sqrt(m) min_t |(M b^ph)_t| / ||M b^ph||_2.
```

Indeed, (1) and the definition of `chi_ph` give, row by row,

```text
|(M b^ph)_t| >= (1-kappa)c sqrt(lambda)|u_t|.
```

They also give `||r||_2<=kappa c sqrt(lambda)`, because the coordinatewise
bound is weighted by the unit vector `u`. The second identity in (1) now
proves (2). This is an all-row result: an averaged leakage estimate would
not rule out a single cancelled row.

The criterion is sharp in the two relevant senses. If `r=0`, then
`phi^2=mu_top` exactly, so minimum top leverage cannot be replaced by global
top-vector participation. If `chi_ph=1`, one row can cancel exactly even
when `mu_top=1`; an example is given below.

## `PROVED`: an actual-log conditional closure gate

Return to the frozen CRR scales

```text
H=v^12, L=v^10, R=v^8, V=v^7, delta(v)=1/sqrt(log v).
```

For a fixed actual set `W` of cardinality `R`, form the actual matrix `M_W`
and calculate `lambda,u,x,b^ph,rho,mu_top,chi_ph` exactly as above. The
coefficient `b^ph` obeys `|b_n^ph|<=1` on the exact smooth support
`L<n<2L`; it is one common coefficient vector for every row of that same
`W`.

Suppose that, for fixed nonnegative `ell,r,s`, fixed `gamma>0`, and fixed
`0<=kappa<1`,

```text
lambda >= v^(12-ell delta),
rho >= v^(-r delta),
mu_top >= v^(-2s delta),
chi_ph <= kappa,
ell+r+2s <= 2-gamma.                                  (3)
```

`PROVED`: for all sufficiently large `v`, the capped coefficient `b^ph`
satisfies

```text
min_(t in W) |(M_W b^ph)_t| >= v^(7-delta(v)).         (4)
```

This follows from the prior leading-eigenvector certificate

```text
Gamma(W)^2 >= lambda*N*rho*phi^2/R,   N=L-1,
```

and (2). The fixed factor in (2) and `(L-1)/L` are absorbed by the strict
`gamma` margin. Thus `mu_top>=v^(-2s delta)` is exactly the row-leverage
replacement for the former `phi>=v^(-s delta)` premise, while `chi_ph` is a
fixed relative no-cancellation margin. The exponent budget remains
unchanged:

```text
ell+r+2s<2.                                            (5)
```

For clarity, define `AF-PLF_(ell,r,s,gamma,kappa)(v)` to be the conjunction
of (3) for the actual `M_W`, the CRR separation/cardinality/energy conditions
on the same `W`, and the frozen `RationalMass(v)` predicate on that same
`W`. `PROVED`, conditional on `AF-PLF`: (4) supplies the capped Base value
condition without changing `W`; the prior actual-Farey identity

```text
C_theta(sk,rk)=R_W((r/s)exp(theta/H))
```

and its reduced labels, rays, bounded jitter, and RationalMass consequence
remain exactly intact. In particular this is not a generic-alias surrogate.

`CONJECTURED`: the missing actual-Farey inverse statement is that its
RationalMass-relevant class forces usable `mu_top` and `chi_ph`. The scalar
Farey mass `1^*K_F 1` does not presently prove either one. The theorem above
only states the precise additional data that would close the existing
coefficient construction.

## `PROVED`: minimum top leverage is indispensable

For `m>=3`, write `n=m-1`, choose `0<tau<(n-1)/n` and `epsilon>0`, and set

```text
K_(tau,epsilon)=(1/(1+epsilon))
 [ J_n+epsilon I_n       tau 1_n ]
 [ tau 1_n^*             1+epsilon ].                 (6)
```

This matrix is positive definite, has every diagonal entry equal to one, and
has every cross-block entry `tau/(1+epsilon)>0`. Its largest eigenvalue is

```text
lambda=(lambda_tau+epsilon)/(1+epsilon),
lambda_tau=(n+1+sqrt((n-1)^2+4n tau^2))/2>n.
```

The corresponding positive unit eigenvector has the form

```text
u=(1/sqrt(1+d^2)) (1/sqrt(n),...,1/sqrt(n),d),
d=2 sqrt(n) tau/(sqrt((n-1)^2+4n tau^2)+n-1).
```

The hypothesis on `tau` makes the final coordinate the minimum, and

```text
d^2 <= n tau^2/(n-1)^2.                                (7)
```

Choose a square factor `M` of `K_(tau,epsilon)` and a right unitary so that
its top right singular vector is the flat vector
`x=(1,...,1)/sqrt(m)`. Then `rho=1`, `b^ph=(1,...,1)`,
`r=0`, and hence

```text
phi^2=mu_top=m d^2/(1+d^2)
     <= m n tau^2/(n-1)^2.                              (8)
```

Meanwhile the global left participation obeys

```text
||u||_1^2/m >= [n/m]/[1+n tau^2/(n-1)^2].               (9)
```

Thus letting first `m` and then `tau^(-1)` grow makes the top eigenvalue
large, `rho=1`, every row norm identical, every Gram entry connected, and
global left participation arbitrarily close to one, while `phi` becomes
arbitrarily small. This is a full-rank abstract countermodel, not merely a
zero-row construction.

For the exact displayed sample `m=101`, `tau=epsilon=1/100`, the replay
certifies

```text
lambda > 10000/101,
phi^2 <= 101/980100,
||u||_1^2/m >= 98010000/98990201,
rho=1, chi_ph=0.
```

So even perfect phase coherence does not replace the needed minimum top-row
leverage.

## `PROVED`: phase leakage is also indispensable

There is a separate two-row, four-column abstract countermodel. Let

```text
x=(10,1,1,1)/sqrt(103),       b^ph=(1,1,1,1),
u=(1,1)/sqrt(2),              z=(1,-1)/sqrt(2),
q=b^ph-<x,b^ph>x=(-27,90,90,90)/103.
```

Then `||q||_2^2=243/103` and `rho=169/412`. With
`y=q/||q||_2`, define

```text
M=u x^*+sqrt(169/243) z y^*.
```

`PROVED`: `M M^*=u u^*+(169/243)z z^*`. Hence the top eigenvalue is one,
the second eigenvalue is `169/243`, both row norms squared are `206/243`,
and `mu_top=1`. But

```text
M b^ph=(13/sqrt(103))(u+z),
```

whose second coordinate is zero. Therefore `phi=0`. Here the relative
leakage is exactly `chi_ph=1`: fixed spectral gap, constant diagonal,
perfect minimum top leverage, and a positive constant `rho` still allow an
exact all-row cancellation.

Consequently a global spectral-gap or averaged residual hypothesis cannot
replace a coordinatewise no-cancellation statistic. The relative
`chi_ph` condition is the least restrictive direct `l_infinity`-type
control used by (2): it compares leakage to each row's own top-mode size,
rather than to the globally smallest one.

## What advances this gate

An actual proof that the CRR RationalMass/Farey class has
`mu_top>=v^(-2s delta)` and `chi_ph<=kappa<1`, with (5), would supply a real
common `(b^ph,W)` construction. An actual sequence of Dirichlet matrices
violating either condition while satisfying the full frozen Farey and
RationalMass requirements would refute that proposed route.

The abstract examples refute only a matrix-summary shortcut; they do not
refute any statement exploiting the actual logarithmic phases, reduced
Farey arithmetic, or coefficient/Farey interaction.

## Replay

```sh
python3 proof/build_cycle_6_crr_phase_flatness_v1.py --write
python3 proof/build_cycle_6_crr_phase_flatness_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_phase_flatness_v1.py
```
