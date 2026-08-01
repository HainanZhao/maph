# Cycle 6 CRR row-deletion actual-log inverse reduction v1

## Claim boundary

`PROVED`: this note reduces the missing all-row leverage and phase-leakage
conditions to two explicit statistics of the *actual* logarithmic Gram matrix

```text
M_W(t,n)=w(n/L)n^(it),
G_W=M_W M_W^*.
```

It gives an exact row-deletion lower bound for the top eigenvector, an exact
Gram-projection upper bound for the phase leakage, and an exact accounting of
what `RationalMass(v)` supplies row-by-row through the actual Farey kernel.
The reduction keeps one common `W`, the capped coefficient
`b^ph=phase(M_W^*u)`, the frozen reduced Farey labels, and the bounded jitter.

`CONJECTURED`: no theorem here shows that `RationalMass(v)` forces the new
row-deletion coverage or the phase-leakage inequality. In particular, this
note does not prove an actual CRR witness, AFARI, FARI, CFARI, CRR-U, a cubic
estimate, a density gain, a short-interval theorem, a saturation theorem, or
an L-function result. The last section records a sharp target for any
restricted-Farey inverse theorem rather than claiming it has been proved.

## Frozen actual matrix and diagonal mass

The pinned Guth--Maynard source defines a nonnegative smooth `w`, supported
on `[1,2]` and equal to one on `[6/5,9/5]` (source lines 425--426), and then
defines the matrix `M_W(t,n)=w(n/L)n^(it)` (lines 484--487). Thus for every
actual `W`,

```text
G_W(t,s)=sum_(L<n<2L) w(n/L)^2 n^(i(t-s)),
G_W(t,t)=S_L:=sum_(L<n<2L)w(n/L)^2.                    (1)
```

`PROVED`: at frozen `v>=8`,

```text
L/2 <= S_L <= L.                                      (2)
```

Indeed, every integer in `[6L/5,9L/5]` contributes one to `S_L`; their count
is at least `3L/5-1>=L/2`, while the support has fewer than `L` integer
points and `0<=w<=1`. This is an actual arithmetic fact about the fixed
matrix, not a surrogate Gram model.

## `PROVED`: deletion leverage controls every top-eigenvector coordinate

Let `lambda=lambda_max(G_W)`, fix a unit top eigenvector `u`, and fix a row
`t`. Delete that row and column, and write

```text
lambda_(minus t)=lambda_max(G_(W minus {t})),
d_t=lambda-lambda_(minus t),
beta_t=||G_(W minus {t},t)||_2.
```

Set `d_t^2/(d_t^2+beta_t^2)=0` only in the degenerate `d_t=beta_t=0` case.
Then

```text
|u_t|^2 >= d_t^2/(d_t^2+beta_t^2).                    (3)
```

To prove this, let `P_t` remove the `t` coordinate. The eigenvector equation
gives the exact block identity

```text
(lambda I-G_(W minus {t})) P_t u = u_t P_t G_W e_t.
```

The least singular value on the left is `d_t`, so

```text
d_t sqrt(1-|u_t|^2) <= beta_t |u_t|,
```

which proves (3). The normalized deletion coverage

```text
DelCov(W)=|W| min_(t in W) d_t^2/(d_t^2+beta_t^2)       (4)
```

therefore obeys

```text
mu_top(W):=|W| min_t |u_t|^2 >= DelCov(W).              (5)
```

For the actual log matrix, `beta_t` is the explicit off-row correlation
quantity

```text
beta_t^2=sum_(s in W, s!=t) |sum_(L<n<2L)
                              w(n/L)^2 n^(i(t-s))|^2
         =(G_W^2)_(t,t)-S_L^2.                         (6)
```

Thus (4) says precisely what must be controlled: deleting every individual
time must lower the top logarithmic-Gram eigenvalue by enough relative to
that row's aggregate off-block log correlation. It is not enough that the
rows merely have equal norms or nonzero pairwise correlations.

The bound is sharp. `PROVED`: for every rank-one Gram matrix `G=a a^*`, one
has

```text
d_t=|a_t|^2,
beta_t^2=|a_t|^2(lambda-|a_t|^2),
d_t^2/(d_t^2+beta_t^2)=|a_t|^2/lambda=|u_t|^2.          (7)
```

So no generally stronger lower bound can be inferred from just `d_t` and
`beta_t`.

## `PROVED`: a Gram-projection certificate for phase leakage

Use the capped top phase construction from the preceding phase-flatness
reduction:

```text
x=M_W^*u/sqrt(lambda),
b^ph_n=x_n/|x_n| (zero if x_n=0),
c=||x||_1,
q=b^ph-cx,
r=M_Wq,
eta_ph=||q||_2^2/c^2=(||b^ph||_2^2-c^2)/c^2.
```

`PROVED`: for every row,

```text
|r_t|^2 <= (S_L-lambda|u_t|^2)||q||_2^2.               (8)
```

This is Cauchy--Schwarz after projecting the row vector `M_W^*e_t`
orthogonally away from `x`; the squared norm of that projection is exactly
`S_L-lambda|u_t|^2`. Consequently the relative all-row leakage from the
previous note obeys

```text
chi_ph^2 <= eta_ph max_t (S_L/(lambda|u_t|^2)-1)
           <= eta_ph (|W|S_L/(lambda mu_top)-1).        (9)
```

Combining (5) and (9) yields the completely actual-log sufficient test

```text
DelCov(W)>0,
eta_ph (|W|S_L/(lambda DelCov(W))-1) <= kappa^2
       ==> chi_ph<=kappa.                              (10)
```

The second implication uses no separately optimized coefficient: `eta_ph`
comes from the same `b^ph`, and every term in (10) comes from that same
actual `M_W` and `W`. If `x` has full support,

```text
eta_ph=(1-rho)/rho;
```

in general `eta_ph<=(1-rho)/rho`.

The estimate can be sharp: the exact two-row phase-cancellation model from
the preceding reduction has `eta_ph=243/169`, `S_L=206/243`, `lambda=1`,
`mu_top=1`, and equality in (9), with `chi_ph=1`.

## `PROVED`: combined actual-log conditional gate

Let `|W|=R=v^8` and retain the full CRR separation/cardinality/energy
conditions and `RationalMass(v)` on this same set. Suppose for fixed
nonnegative `ell,r,s`, fixed `gamma>0`, and fixed `0<=kappa<1` that

```text
lambda >= v^(12-ell delta(v)),
rho >= v^(-r delta(v)),
DelCov(W) >= v^(-2s delta(v)),
eta_ph (R*S_L/(lambda DelCov(W))-1) <= kappa^2,
ell+r+2s <= 2-gamma.                                  (11)
```

`PROVED`, conditional on (11): equations (5) and (10) supply the
`mu_top` and `chi_ph` premises of the prior phase-flatness theorem. Therefore
the one capped coefficient `b^ph` satisfies

```text
min_(t in W)|(M_W b^ph)_t| >= v^(7-delta(v))
```

for all sufficiently large `v`. The original exponent budget is unchanged:
`ell+r+2s<2`. The same `W` remains subject to the actual Farey identity

```text
C_theta(sk,rk)=R_W((r/s)exp(theta/H));
```

no generic alias model or replacement of `W` is introduced.

This identifies a usable arithmetic inverse target: prove the deletion
coverage and the projected phase-leakage condition on the actual
RationalMass class, or construct a full actual counterexample to either.

## `PROVED`: why diagonal Cauchy alone is not the missing theorem

The projection certificate (10) is deliberately stronger than the exact
`chi_ph` condition. At a central spectral scale, assume additionally

```text
lambda <= v^(12+a delta(v))
```

for a fixed `a>=0`. Since `DelCov(W)<=mu_top(W)<=1`, (2) gives

```text
R*S_L/(lambda DelCov(W))-1
 >= (1/2)v^(6-a delta(v))-1.                           (12)
```

Hence this particular diagonal/projection certificate can verify a fixed
`chi_ph<=kappa<1` only when

```text
eta_ph <= kappa^2 / ((1/2)v^(6-a delta(v))-1).          (13)
```

That is `v^(-6+o(1))` phase-rounding defect. A lower bound on `rho` of the
form used by the leading-eigenvector gate does not imply (13). Thus
`PROVED`: at central `lambda`, diagonal mass plus Cauchy--Schwarz cannot by
itself be the desired phase-leakage theorem; a successful route must exploit
additional phase-sensitive log/Farey structure. This is a scoped limitation
of the displayed certificate, not a no-go for actual `chi_ph` or a CRR
witness.

## `PROVED`: RationalMass has only average Farey deletion coverage so far

Let the actual Farey kernel from the averaged-jitter reduction be

```text
(K_F)_(t,s)=sum_(a in F_Q) integral_(-3)^3
              (a exp(theta/H))^(i(t-s)) dtheta,
Mcal_v(W)=1^*K_F1.
```

Deleting a row gives the exact Farey influence

```text
Delta_F(t)=Mcal_v(W)-Mcal_v(W minus {t})
          =(K_F)_(t,t)+2 Re sum_(s!=t)(K_F)_(t,s),
sum_t Delta_F(t)=2 Mcal_v(W)-tr(K_F),
tr(K_F)=6|W||F_Q|.                                    (14)
```

`PROVED`, conditional on frozen `RationalMass(v)`: the prior averaged-jitter
reduction supplies

```text
Mcal_v(W)>=(75/2)H v^(8-3delta(v)).                    (15)
```

Since `|F_Q|<=Q^2=v^8`, (14)--(15) imply only the **average** lower bound

```text
(1/R) sum_t Delta_F(t) >= 75v^(12-3delta(v))-6v^8.     (16)
```

It does not lower-bound the least `Delta_F(t)`, and it says nothing directly
about the distinct actual log-Gram deletion statistic in (4). This gap is
genuine at the level of scalar PSD-kernel data: for the abstract kernel
`J_(R-1) direct_sum [1]`, every diagonal is one and
`Mcal=(R-1)^2+1`, but the last deletion influence is only one while the mean
influence is asymptotic to `2R`. This abstract kernel is not claimed to be
`K_F`; it shows only that a total mass like (15) cannot logically force
uniform row coverage without a new restricted-Farey statement.

The sharp missing assertion can therefore be stated as follows.

```text
RFDI_(s,kappa)(v): every actual W satisfying the frozen RationalMass,
separation, cardinality, and energy predicates has

DelCov(W)>=v^(-2s delta(v))
and eta_ph(R*S_L/(lambda DelCov(W))-1)<=kappa^2.
```

`CONJECTURED`: no proof of `RFDI` is supplied. `PROVED`, conditional on
`RFDI` together with the spectral and `rho` rows in (11): the actual capped
phase construction closes the Base value condition at the same exponent
budget. Thus any genuine restricted-Farey inverse theorem must transfer
more than total Farey mass: it must control every row's spectral deletion
deficit relative to (6), and its phase-rounding projection.

## Replay

```sh
python3 proof/build_cycle_6_crr_row_deletion_inverse_v1.py --write
python3 proof/build_cycle_6_crr_row_deletion_inverse_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_row_deletion_inverse_v1.py
```
