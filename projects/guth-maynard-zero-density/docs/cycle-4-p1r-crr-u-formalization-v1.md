# Cycle 4 P1R-CRR-U formalization v1

## Claim boundary

`CONJECTURED`: CRR-U is the assertion that the simultaneous critical
configuration defined below is eventually impossible.  This document does
not prove CRR-U, construct an extremizer, improve a zero-density exponent, or
authorize a computational search.

`PROVED`: exact substitution in the pinned Guth--Maynard upper bounds gives
large-value exponents `[6,8,8]`, energy exponents `[20,20,20]`, and four
`S3` exponents `[36,36,36,36]`.  These compatible upper-bound exponents do
not imply that common actual coefficients and a common set exist.

`OBSERVED`: the rational discussion after the affine proposition and the
critical discussion near the end of the paper are heuristic remarks.  They
do not define rational concentration or derive it from additive energy.

## Exact conventions

The code source of truth is `conventions/crr_formalization_v1.py`.  Let

```text
eta(x)=0                         (x<=0),
eta(x)=exp(-1/x)                 (x>0),
step(x)=eta(x)/(eta(x)+eta(1-x)),
w(u)=step(5(u-1))*step(5(2-u)),
psi1(x)=eta(1-x^2)/eta(1),
psi2(u)=eta(1-4(u-1)^2)/eta(1).
```

Thus `w` is nonnegative, smooth, supported on `[1,2]`, bounded by one,
and equals one on `[6/5,9/5]`.  The two `psi` functions are nonnegative
smooth bumps, with `psi1(0)=psi2(1)=1`, supported respectively on
`[-1,1]` and `[1/2,3/2]`.

Freeze `e(x)=exp(2*pi*i*x)` and

```text
hat(f)(xi)=integral_R f(u) exp(-2*pi*i*xi*u) du.
```

For each integer `v>=3`, put

```text
delta(v)=1/sqrt(log v),  T0=v^13,  H=v^12,  L=v^10,
R0=v^8,  M=v^2,  Q=v^4,  V=v^7,  sigma=7/10.
```

Here `v^delta(v)=exp(sqrt(log v))` is a fixed subpower slack.  `T0` is
bookkeeping for the global density height; every witness below lives on the
local interval of length `H`.

## A CRR witness

A witness at `v` is one common pair `(b,W)` satisfying all three blocks.

### Base(v)

1. `b=(b_n)_(n>=1)` is a complex sequence with `|b_n|<=1`.
2. `D_v(t)=sum_(n>=1) w(n/L)b_n n^(it)`.
3. `W` is a finite subset of `[0,H]`, separated by at least `H^(1/100)`.
4. `v^(8-delta(v)) <= |W| <= v^(8+delta(v))`.
5. `|D_v(t)| >= v^(7-delta(v))` for every `t in W`.
6. With ordered quadruples and multiplicity,

   ```text
   E(W)=#{(t1,t2,t3,t4) in W^4:
          |t1+t2-t3-t4|<=1},
   ```

   and `v^(20-delta(v)) <= E(W) <= v^(20+delta(v))`.

### RationalMass(v)

Define

```text
R_W(u)=sum_{t in W} |u|^(it),
Rtilde_W(u)^2 = integral_R H*psi1(H*(u-u'))
                         *psi2(u')*|R_W(u')|^2 du'.
```

The square root is the nonnegative root.  This is an explicit diagnostic of
the same smoothed-correlation form as Guth--Maynard equation `eq:RtDef`, but
the particular bumps and the lower-bound predicate are new definitions; no
source theorem is claimed to select them.

Let `Q_v` be the union of the intervals

```text
[r/s-1/(100H), r/s+1/(100H)]
```

over coprime positive integers `Q<=r,s<2Q` with
`3/4<=r/s<=5/4`.  Require

```text
measure({u in Q_v: Rtilde_W(u)>=v^(6-delta(v))})
    >=v^(-4-delta(v)).
```

The rational set depends only on frozen pre-result data and `W`; it does not
inspect `S3` or a computed candidate.

### PositiveCubic(v)

Put `h_t(u)=w(u)^2u^(it)` and, for `m in Z^3`,

```text
I_m=L^3 sum_(t1,t2,t3 in W)
      hat(h_(t1-t2))(m1*L)
      hat(h_(t2-t3))(m2*L)
      hat(h_(t3-t1))(m3*L),
S3_signed=sum_(m1*m2*m3 != 0) I_m.
```

The rapid Fourier decay of the fixed smooth `w` makes the displayed `m` sum
convergent for each finite `W`.  Conjugation and the involution
`m -> -m` make `S3_signed` real.  Require

```text
S3_signed >= v^(36-delta(v)).
```

`PROVED`: reality is a symmetry consequence.  `CONJECTURED`: a positive
lower bound of this order can occur together with the preceding blocks.
The published estimates provide upper bounds and do not establish this
condition.

## Classification branch and falsifier

CRR-U is the universal-incompatibility statement

```text
there exists v0 such that no CRR witness exists at any integer v>=v0.
```

Equivalently, any sequence of witness integers `v_j -> infinity` falsifies
CRR-U and is a candidate compatibility mechanism.  A finite witness neither
proves nor refutes CRR-U.

`PROVED`: the displayed Guth--Maynard upper bounds are exponent-compatible
with every block above.  Therefore exponent substitution, the moment bounds,
the energy upper bound, the affine upper bound, and the four-term `S3` upper
bound cannot by themselves prove CRR-U.

## Authorized work and proof obligations

The first branch is analytic and universal.  No discovery computation is
authorized by this version: row cap `0`, no RNG seed, no candidate rows, no
post-result selection, and no numerical certification margin.  A later
finite probe requires a new preregistration that freezes its families,
ranges, seed, cap, failed-row rule, and rigorous retention margin.

CRR-U promotion requires two independent proof routes or a documented reason
why the mechanism admits only one, plus exact closure of:

1. the Base pointwise large-value and separation hypotheses;
2. both sides of the energy band;
3. the explicit rational-mass measure bound;
4. convergence, reality, sign, and size of the signed cubic trace;
5. all uniformity in `v` and every subpower loss.

The immediate analytic alternatives are: derive a quantitative conflict
between random-scale energy and the explicit rational mass, or derive a
conflict between rational mass and positive signed cubic size.  Failure of
both approaches is retained; it is not evidence of compatibility.
