# Cycle 6 CRR actual-log/Farey RFDI outlier surgery v1

## Claim boundary

`PROVED`: this note gives a conditional obstruction to the **set-only** RFDI
target stated in the row-deletion reduction.  Starting from an actual
logarithmic/Farey core with a fixed isolated top eigenvalue and a fixed
RationalMass surplus, one may add one actual late-time row.  The resulting
single common set retains the frozen separation, cardinality, energy, and
RationalMass predicates, while its actual-log row-deletion coverage is too
small for every fixed RFDI exponent `s` at sufficiently large `v`.

`CONJECTURED`: the required surplus core is not constructed here.  Thus this
does **not** refute RFDI, produce an actual CRR witness, prove that a
RationalMass core with the stated spectral gap exists, or address the capped
coefficient's pointwise Base value condition or PositiveCubic.  It also does
not prove AFARI/FARI/CFARI, a cubic estimate, a density gain, a short-interval
theorem, a saturation theorem, or an L-function result.

The precise consequence is narrower and useful: a proof of the set-only
RFDI assertion cannot be based solely on scalar conditions that survive this
one-row surgery.  It must use genuinely all-row information, rule out the
isolated-core configuration, or use the non-hereditary pointwise/coefficient
part of Base.  This is not an abstract PSD countermodel: every matrix and
Farey quantity below is the frozen actual logarithmic one and the construction
uses one common `W`.

## Frozen setup and conditional core

Write

```text
H=v^12,  L=v^10,  R=v^8,  Q=v^4,
delta(v)=1/sqrt(log v),
M_A(t,n)=w(n/L)n^(it),  G_A=M_A M_A^*.
```

The source-fixed weight has `0<=w<=1`, support in `[1,2]`, and the plateau
used in the preceding actual-log reductions.  Therefore the squared norm of
each row is the same number

```text
S_L=sum_(L<n<2L) w(n/L)^2 <= L.                         (1)
```

Fix `0<g<=1`, `epsilon>0`, and nonnegative fixed `ell,s`.  The conditional
input is a core `A` of exactly `R-1` real times satisfying all of the
following.

```text
(i)   A subset [0,H/4] is H^(1/100)-separated;
(ii)  E(A) lies in [v^(20-delta), v^(20+delta)-(4R-3)];
(iii) lambda_1(G_A)=Lambda,
      lambda_2(G_A)<=(1-g)Lambda,
      Lambda>=v^(12-ell*delta),
      S_L+sqrt(Lambda*S_L)<=g*Lambda/2;                (2)
(iv)  on a rational set E of measure at least v^(-4-delta),
      F_A(u)>=(1+epsilon)T_v,
      T_v=v^(12-2delta).                               (3)
```

Here `F_A` is the *same* frozen smoothing of the actual rational exponential
sum `R_A(u)=sum_(t in A)u^(it)`:

```text
F_A(u)=H integral psi1(H(u-u')) psi2(u') |R_A(u')|^2 du'. (4)
```

Condition (3) is a fixed multiplicative strengthening of the frozen
RationalMass threshold.  The margin is needed only to make its preservation
under a new row completely elementary.  Condition (2)'s final inequality is
automatic for sufficiently large `v` from its preceding lower bound on
`Lambda`, with fixed `g,ell`, because `S_L/Lambda` is at most
`v^(-2+ell*delta(v))`.

The energy margin in (ii) is equally explicit.  It prevents a claim that an
upper endpoint happens to survive a positive one-row change; it is not hidden
in an asymptotic `o(1)`.

## `PROVED`: one actual late row preserves the scalar/Farey predicates

Put

```text
I=[3H/4,H].
```

For every `tau in I`, the set `W=A union {tau}` is still
`H^(1/100)`-separated: its new distance from `A` is at least `H/2`.  The three
classes of ordered pair sums are

```text
A+A subset [0,H/2],
tau+A=A+tau subset [3H/4,5H/4],
{2tau} subset [3H/2,2H].                               (5)
```

Their mutual gaps exceed one.  Since the original rows are separated by more
than one, the frozen ordered tolerance-one additive energy decomposes exactly:

```text
E(W)=E(A)+4|A|+1=E(A)+4R-3.                             (6)
```

Consequently (ii) gives the full frozen energy band for `W`, and
`|W|=R` gives its frozen cardinality band.

The RationalMass predicate also survives.  For positive `u`,
`R_W(u)=R_A(u)+u^(i tau)` and `|u^(i tau)|=1`.  The pinned normalized bump
formulas give `0<=psi1,psi2<=1`; with their support and positivity,

```text
J(u):=H integral psi1(H(u-u'))psi2(u')du' <= 2.          (7)
```

Cauchy--Schwarz in (4) gives the pointwise actual-smoothing inequality

```text
F_W(u) >= F_A(u)-2 sqrt(2 F_A(u)).                       (8)
```

If

```text
T_v >= max(2, 8(1+epsilon)/epsilon^2),                  (9)
```

then the function `x-2sqrt(2x)` is increasing on the relevant range and
(3), (8) imply `F_W(u)>=T_v` throughout the same rational set `E`.  Thus
the exact frozen RationalMass predicate holds for `W`; no rational cell or
favourable jitter is selected after the outlier is chosen.

For clarity, the actual-Farey structure is retained as well.  Its kernel is

```text
(K_F)_(t,s)=sum_(a in F_Q) integral_(-3)^3
              (a exp(theta/H))^(i(t-s)) dtheta,          (10)
```

which is the Gram kernel of
`Phi_t(a,theta)=(a exp(theta/H))^(it)`.  Hence

```text
Mcal(W)=1^*K_F1=||sum_(t in W)Phi_t||_2^2,
(K_F)_(t,t)=6|F_Q|<=6Q^2=6v^8,
|Mcal(W)-Mcal(A)-6|F_Q||<=2sqrt(6|F_Q|Mcal(A)).          (11)
```

The actual label identity remains exactly

```text
C_theta(sk,rk)=R_W((r/s)exp(theta/H)).                  (12)
```

Thus the construction neither switches to an alias kernel nor uses a
different row set for the Farey statistic.  In particular, once (8)--(9)
have supplied RationalMass for `W`, the prior actual-Farey lower reduction
applies to this same `W` unchanged.

## `PROVED`: elementary selection of a spectrally weak actual row

Let `u_A` be a unit top eigenvector of `G_A`.  For a prospective outlier
`tau`, put `b(tau)=G_(A,tau)` and

```text
f(tau)=u_A^* b(tau).
```

With `x=M_A^*u_A/sqrt(Lambda)`, direct expansion of the actual rows gives

```text
f(tau)=sqrt(Lambda) D_c(tau),
D_c(tau)=sum_(L<n<2L) c_n n^(-i tau),
c_n=conjugate(x_n)w(n/L),  sum_n |c_n|^2<=1.             (13)
```

This is where the selection is tied to the actual logarithmic matrix rather
than a surrogate spectral block.  An elementary integral calculation gives
the required row without invoking a large-values theorem.  On `I`, for
`n!=m`,

```text
|integral_I exp(-i tau log(n/m))dtau| <= 2/|log(n/m)|,
1/|log(n/m)| <= 2L/|n-m|.                               (14)
```

Using `2ab<=a^2+b^2` and the harmonic sum bound,

```text
sum_(n!=m) |c_n||c_m|/|n-m|
 <= 2(1+log L) sum_n|c_n|^2,
```

one obtains

```text
(1/|I|) integral_I |D_c(tau)|^2dtau
 <= C_v:=1+32L(1+log L)/H.                              (15)
```

Choose `tau in I` with `|D_c(tau)|^2<=C_v`.  For `v>=64`, the elementary
bound `log v<=sqrt(v)` gives `C_v<=2`.  This choice is made from the core
matrix only, before the target top eigenvector of `W` is considered; it has no
post-hoc phase or Farey alignment.

## `PROVED`: the selected outlier defeats row-deletion coverage

Use the orthogonal decomposition of the enlarged Gram matrix along `u_A`:

```text
G_W = [ Lambda   f^* ]
      [   f       B  ].                                  (16)
```

The lower-right block comprises the core orthogonal complement and the new
row.  By (1), (2), and `||G_(A,tau)||_2<=sqrt(Lambda*S_L)`,

```text
||B|| <= lambda_2(G_A)+S_L+sqrt(Lambda*S_L)
       <= Lambda-gLambda/2.                              (17)
```

Let `u_W=(a,y)` be any unit top eigenvector of `G_W`.  Principal-submatrix
interlacing gives `lambda_1(G_W)>=Lambda`.  The second block eigenvector
equation and (17) therefore give

```text
||y|| <= |f(tau)|/(gLambda/2),
|(u_W)_tau|^2 <= 4C_v/(g^2 Lambda).                      (18)
```

The preceding actual row-deletion lemma says

```text
DelCov(W)<=mu_top(W)<=R |(u_W)_tau|^2
                         <=4R C_v/(g^2 Lambda).          (19)
```

In the central lower-eigenvalue regime of (2), for `v>=64`,

```text
DelCov(W)<=8g^(-2)v^(-4+ell delta(v)).                   (20)
```

For every fixed `g,ell,s`, the right side of (20) is below
`v^(-2s delta(v))` once `v` is sufficiently large.  In particular this
holds for every proposed phase-flatness budget
`ell+r+2s<2` (the unused `r` does not repair a failed deletion bound).
Therefore the chosen actual `W` violates the deletion-coverage half of
`RFDI_(s,kappa)` for every fixed `kappa`; no analysis of the separate
phase-leakage half is needed.

## What this does, and does not, settle

`PROVED`, conditional on a core satisfying (2)--(3): the actual frozen
separation, cardinality, energy, RationalMass, matrix lower-eigenvalue scale,
and Farey labels coexist with `DelCov(W)<v^(-2s delta(v))`.  Any attempt to
deduce the set-only RFDI assertion from scalar conditions stable under this
extension is therefore blocked.

`CONJECTURED`: no such core is exhibited.  In particular, the theorem does
not establish that the **full** Base predicate (which contains a common
capped coefficient and its all-row value lower bound) survives the surgery.
That distinction is intentional: the RFDI target in the prior reduction was
introduced as a RationalMass/separation/cardinality/energy inverse statement.
The obstruction says that this target needs a new all-row or coefficient
mechanism, not that the broader CRR program is impossible.

The claim would be refuted by an error in the actual expansion (13), the
integral or harmonic estimates in (14)--(15), the pair-sum separation in (5),
the smoothing bound (8), or the block estimate (17)--(19).  A construction
showing that no core can simultaneously meet (2)--(3) would not refute this
conditional theorem; it would instead identify a promising new structural
incompatibility route.

## Replay

```sh
python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py --write
python3 proof/build_cycle_6_crr_rfdi_outlier_surgery_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_rfdi_outlier_surgery_v1.py
```
