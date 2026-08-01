# Cycle 5 CRR actual-Farey/log-Gram reduction v1

## Claim boundary

`PROVED`: this note gives an exact reduction from the frozen CRR
`RationalMass(v)` predicate to a large **actual Farey--log Gram-bundle**
statistic, and gives the simultaneous coefficient-matrix spectral lower bound
forced by `Base(v)`.  The reduction uses the reduced fractions in the frozen
CRR net, their `H^(-1)` neighborhoods, and multiplicative rays in the same
Dirichlet measurement matrix that carries the Base coefficient vector.

`CONJECTURED`: the resulting Farey restricted inverse inequality (FARI),
defined below, has a fixed power saving.  This note does not prove FARI,
CRR-U, a compatible witness, a positive cubic lower bound, a density gain, a
short-interval theorem, a saturation theorem, or an L-function result.  It
does not reuse the generic logarithmic-alias argument: every node below is an
ordinary reduced rational `r/s` in the frozen CRR net.

The point is to expose an exact arithmetic/coefficient-coupled target.  A
proof of FARI would prove incompatibility; an asymptotic compatible family
must instead realize the displayed bundle lower bound on one common `W`.

## Frozen setup

Use the CRR-v2 conventions, for integer `v>=8`:

```text
H=v^12,   L=v^10,   M=v^2,   Q=v^4=M^2,
R=v^8=Q^2,   V=v^7,   delta=1/sqrt(log v).
```

Let

```text
F_W(u)=Rtilde_W(u)^2
      = integral H psi1(H(u-u')) psi2(u') |R_W(u')|^2 du',
R_W(u)=sum_(t in W) u^(it)       (u>0).
```

The frozen rational cells are

```text
J_(r,s)=[r/s-1/(100H), r/s+1/(100H)]
```

for coprime `Q<=r,s<2Q`, `3/4<=r/s<=5/4`.  Write this reduced set as
`F_Q`.  `RationalMass(v)` asserts, for

```text
E={u in union_(r,s in F_Q) J_(r,s): F_W(u)>=v^(12-2delta)},
```

that `|E|>=v^(-4-delta)`.

The bound `0<=psi1,psi2<=1` used below follows directly from the explicit
CRR-v2 definitions: `eta` is increasing on the positive half-line and each
argument of `eta` is at most one.  Also `supp(psi1) subset [-1,1]`.

## Actual Farey geometry at the critical scale

`PROVED`: distinct members of `F_Q` are separated by at least `1/(4Q^2)`,
because the numerator of the difference of two distinct reduced fractions is
a nonzero integer and both denominators are less than `2Q`.  Since

```text
2/(100H) < 1/(4Q^2),       H=Q^3,
```

the frozen cells are disjoint.  Their total possible measure has the exact
critical scale

```text
#F_Q * H^(-1) = Q^(2+o(1))/H = Q^(-1+o(1))=v^(-4+o(1)).
```

This is the same scale as the CRR `RationalMass` lower measure, so the actual
net is neither replaced by nor inferred from a generic alias packet.

For completeness, it already contains `>>Q^2` cells by an elementary finite
count.  Put `I=[Q,Q+floor(Q/4)) cap Z`.  Every coprime pair in `I^2` lies in
`F_Q`.  If `X=|I|`, the union bound over a prime dividing both entries gives

```text
#non-coprime pairs
 <= X^2 sum_p p^(-2) + 2X sum_(p<=2Q) p^(-1) + pi(2Q)
 <= 3X^2/4 + 2X(1+log(2Q)) + 2Q.
```

Here `sum_(n>=2)n^(-2)<=3/4`, and `sum_(n<=x)n^(-1)<=1+log x`.
For `Q>=4096`, `X>=Q/5` and the last two terms are at most `X^2/8`:
at the endpoint this follows from `log(8192)=13 log 2<91/10`, and the
remaining normalized bound increases with `Q`.  Hence

```text
#F_Q >= Q^2/200       (Q>=4096).
```

This count is only a scale check; the stronger activation conclusion below
comes from `RationalMass`, not from this lower count.

## The jittered actual-Farey lift

`PROVED`, conditional only on `RationalMass(v)`: let `A` be the set of cells
that meet `E`.  Disjointness and the cell diameter give

```text
#A >= H|E|/(2/100) >= 50 v^(8-delta).                 (1)
```

For each `(r,s) in A`, choose `u in E cap J_(r,s)`.  Positivity, boundedness,
and the support of the two frozen bumps yield

```text
F_W(u) <= H integral_(|u-u'|<=H^(-1)) |R_W(u')|^2 du'
       <= 2 sup_(|u-u'|<=H^(-1)) |R_W(u')|^2.
```

Thus some `x_(r,s)` satisfies

```text
|R_W(x_(r,s))| >= 2^(-1/2) v^(6-delta),
|x_(r,s)-r/s| <= 101/(100H).
```

Writing `x_(r,s)=(r/s) exp(theta_(r,s)/H)`, the lower endpoint
`r/s>=3/4` gives

```text
|theta_(r,s)| <= 2*(101/75) < 3.                       (2)
```

The factor two uses `|log(1+y)|<=2|y|` for the present tiny relative shift.
So `RationalMass` forces a dense set of *jittered actual Farey nodes*, not
unrelated logarithmic aliases.  The bounded jitter is essential: the frozen
positive smoothing does not justify silently replacing `x_(r,s)` by the
center `r/s`.

## Lift to multiplicative rays of the Dirichlet matrix

Let the source measurement matrix use the same rows `W` and the same weight
as Base:

```text
M_W(t,n)=w(n/L)n^(it).
```

For each real `theta`, put

```text
P_theta(t,t)=exp(i theta t/H),
C_theta=M_W^* P_theta M_W.
```

`P_theta` is unitary.  For `(r,s) in F_Q`, let

```text
K_(r,s)={k in Z_{>0}: 6L/5 <= rk,sk <= 9L/5}.
```

`PROVED`: every such ray has

```text
#K_(r,s) >= L/(20Q)=v^6/20.                            (3)
```

Indeed, with `a=min(r,s)` and `b=max(r,s)<=5a/4`, the permissible real
`k`-interval has width at least

```text
9L/(5b)-6L/(5a) >= 3L/(25Q).
```

Subtracting one for an integer endpoint still leaves `L/(20Q)` because
`L/Q=v^6>=64`.  On this interval the frozen weight is exactly one.  Therefore
the labeled, exact identity is

```text
C_theta(sk,rk) = sum_(t in W) (r/s)^(it) exp(i theta t/H)
                = R_W((r/s) exp(theta/H)).             (4)
```

The map `(r,s,k)->(sk,rk)` is injective: the ratio recovers the reduced pair,
then the common multiplier.  Thus no matrix entry is counted twice.

Define the nonnegative actual-Farey/log-Gram bundle

```text
B_v(W)=sum_((r,s) in F_Q) sup_(|theta|<=3)
          sum_(k in K_(r,s)) |C_theta(sk,rk)|^2.
```

Combining (1)--(4) gives the central result:

```text
B_v(W) >= (5/4) v^(26-3delta).                          (FLG)
```

The exponents are `8-delta` activated cells, `12-2delta` raw squared
amplitude, and `6` ray multiplicity.  This is a rigorous necessary condition
for `RationalMass(v)`; it uses no energy estimate, generic spacing argument,
or cubic sign claim.

## The common coefficient coupling

`PROVED`, conditional on `Base(v)`: for the same matrix and the same Base
coefficient vector `b`,

```text
||M_W b||_2^2 >= |W| v^(14-2delta) >= v^(22-3delta).
```

Only `L-1` nonzero coefficient positions occur in the support interior of
`w`, so `||b||_2^2<=L`.  Consequently

```text
lambda_max(M_W M_W^*) >= v^(12-3delta).                 (SPEC)
```

`(FLG)` and `(SPEC)` are imposed on the same `M_W`, rather than on separately
chosen point sets or separately optimized coefficients.  This is the promised
coefficient-coupled inverse formulation.  It does not itself compare the two
lower bounds strongly enough to prove a contradiction.

## A precise conditional incompatibility gate

For a fixed `eta>0`, define `FARI_eta` to be the following statement.

```text
For all sufficiently large v, every H^(1/100)-separated W subset [0,H]
which has a Base(v) coefficient vector satisfies

    B_v(W) <= v^(26-eta).
```

`CONJECTURED`: no proof or disproof of `FARI_eta` is supplied here.  It is an
actual Farey-log restricted inverse inequality; it is deliberately stronger
than any statement based only on real spacing, ordinary additive energy, and
positive smoothing.

`PROVED`, conditional on `FARI_eta` for any fixed `eta>0`: CRR-U follows.
For sufficiently large `v`, `3delta(v)<eta`, so `(FLG)` contradicts FARI.
The conclusion is stronger than needed because it already excludes a common
Base-plus-RationalMass pair, before invoking `PositiveCubic(v)`.  It still
does **not** prove FARI or CRR-U unconditionally.

An asymptotic compatible construction must confront `(FLG)` and `(SPEC)`.  A
finite equal-weight phase-rounding miss does not test this requirement as a
spectral construction, and it is not used as negative evidence here.

## Relation to the source rational model

The source's rational example after Proposition `propsumaff` uses a factor
`s=d e` with factors of the affine scale and the transformation

```text
(d*(r/(d e))+m2)/m3 = (r+e*m2)/(e*m3).
```

`PROVED`: at the frozen scales `M=v^2` and `Q=M^2`, if
`d,e,m2,m3 asymp M` and `r asymp Q`, then the displayed numerator and
denominator are both `asymp Q`.  Thus the source rational mechanism is
dimensionally compatible with the actual critical Farey scale.  This is only
an arithmetic scale identity.  It does not say that a positive-density
reduced subset is closed in the exact shell `[Q,2Q]`, that coprimality is
preserved, or that the CRR smoothing centers at unjittered rationals.

Those are precisely the nontrivial arithmetic features retained in FARI.

## What would refute or advance this reduction

The exact reduction would fail if a Farey-cell disjointness calculation, the
positive-smoothing selector argument, the plateau-ray count, or the labeled
cross-Gram identity failed.  The replay checks each finite algebraic
ingredient.

An explicit asymptotic Base-plus-RationalMass family would refute every
`FARI_eta` that applies to it.  Conversely, a fixed-power upper bound for
this exact bundle on Base-admissible `W` would prove `CRR-U` through the
conditional reduction above.  Neither direction is settled in this note.

## Replay

```sh
python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py --write
python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v1.py --check
python3 -m unittest tests/test_cycle_5_crr_farey_log_gram_reduction_v1.py
```
