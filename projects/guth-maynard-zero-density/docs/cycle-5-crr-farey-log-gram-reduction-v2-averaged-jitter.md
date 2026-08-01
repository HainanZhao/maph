# Cycle 5 CRR actual-Farey/log-Gram reduction v2: averaged jitter

## Claim boundary

`PROVED`, conditional on the frozen CRR-v2 `RationalMass(v)` predicate: the
actual-Farey cross-Gram statistic averaged over its bounded logarithmic jitter
obeys

```text
A_v(W) >= (15/8) v^(26-3 delta(v)).
```

`PROVED`, conditional on the frozen `Base(v)` separation/cardinality bounds
and the published raw-`R` (L^2) lemma: the same statistic has only the
global estimate

```text
A_v(W) << v^(26+delta(v)) = v^(26+o(1)).
```

Thus `PROVED`: after the Base coefficient vector is discarded except for
`|W|`, the raw global (L^2) route reaches the critical exponent `26` on
both sides.  This is a scoped saturation statement for that *uncoupled
global-(L^2) step*, not a saturation theorem for the Guth--Maynard method.

`CONJECTURED`: a fixed-power upper bound for this averaged statistic, called
`AFARI_eta` below, may hold on Base-admissible sets.  This note does not
prove or disprove `AFARI_eta`, v1 `FARI_eta`, CRR-U, a compatible witness, a
cubic estimate, a zero-density improvement, a short-interval improvement, or
an L-function extension.  In particular, the `v^(26+o(1))` upper estimate is
not presented as a proof of FARI.

The separate v1 supremum-over-jitter reduction is preserved verbatim.  V2
adds an averaged-jitter route; it does not alter a v1 statement or artifact.

## Frozen setup and the averaged statistic

Use the v1/v2 frozen scales, for integer `v>=8`,

```text
H=v^12,  L=v^10,  Q=v^4,  Q=M^2,  H=Q^3,
delta(v)=1/sqrt(log v).
```

Let `F_Q` be the reduced fractions `a=r/s` with

```text
Q<=r,s<2Q,  gcd(r,s)=1,  3/4<=r/s<=5/4,
```

and set

```text
J_a=[a-1/(100H),a+1/(100H)],
J_a^+=[a-101/(100H),a+101/(100H)].
```

As in v1, define the same measurement matrix and its row-modulated
cross-Gram matrix:

```text
M_W(t,n)=w(n/L)n^(it),
P_theta(t,t)=exp(i theta t/H),
C_theta=M_W^* P_theta M_W.
```

For `a=r/s`, retain the actual multiplicative ray

```text
K_(r,s)={k in Z_{>0}: 6L/5<=rk,sk<=9L/5}.
```

The v1 labeled identity remains exact:

```text
C_theta(sk,rk)=R_W((r/s) exp(theta/H)).                 (1)
```

Define the nonnegative averaged actual-Farey bundle

```text
A_v(W)=sum_((r,s) in F_Q) integral_(-3)^3
          sum_(k in K_(r,s)) |C_theta(sk,rk)|^2 dtheta. (2)
```

`PROVED`: (1) uses the same rows `W`, same Dirichlet weight, same reduced
Farey labels, and same matrix as the v1 bundle.  The map
`(r,s,k)->(sk,rk)` remains injective, so no labeled matrix entry is silently
duplicated.

## `PROVED` averaged lower bound from actual Farey cells

Let `S=union_(a in F_Q)J_a` and write the frozen smoothing as

```text
F_W(u)=integral H psi1(H(u-u')) psi2(u') |R_W(u')|^2 du'.
```

Under `RationalMass(v)`, the set

```text
E={u in S:F_W(u)>=v^(12-2delta)}
```

has measure at least `v^(-4-delta)`.  Hence, with `I=integral_S F_W(u)du`,

```text
I >= v^(8-3delta).                                      (3)
```

`PROVED`: distinct reduced centers in `F_Q` differ by at least `1/(4Q^2)`.
Since the diameter of `J_a^+` is `202/(100H)` and `H=Q^3`, the expanded
cells are disjoint for the frozen `Q>=4096`.  Since
`0<=psi1,psi2<=1` and `supp(psi1) subset [-1,1]`, Fubini gives

```text
I <= H integral |R_W(u')|^2
       measure({u in S:|u-u'|<=1/H}) du'
  <= (2/100) sum_(a in F_Q) integral_(J_a^+) |R_W(u')|^2 du'.  (4)
```

The final incidence factor is `2/100`, not the measure of an arbitrary
overlap: every length-`2/H` window meets at most one original Farey cell once
the expanded cells are disjoint.  Combining (3)--(4),

```text
sum_a integral_(J_a^+) |R_W(u)|^2 du >= 50 v^(8-3delta). (5)
```

`PROVED`: each expanded cell lies in

```text
{a exp(theta/H): |theta|<=3}.                            (6)
```

For the upper endpoint use `exp(x)>=1+x`; for the lower use
`exp(-x)<=1/(1+x)`.  At the worst center `a=3/4`, the exact required
inequality is

```text
(101/75)/H <= 3/(H+3),
```

which holds at `H>=8^12`.  On every `J_a^+`, `u<=4/3`, and the substitution
`u=a exp(theta/H)` therefore yields

```text
integral_(J_a^+) |R_W(u)|^2 du
 <= (4/(3H)) integral_(-3)^3 |R_W(a exp(theta/H))|^2 dtheta.
```

Thus (5) implies

```text
sum_a integral_(-3)^3 |R_W(a exp(theta/H))|^2 dtheta
 >= (75/2) H v^(8-3delta).                              (7)
```

Finally, the v1 ray calculation gives

`#K_(r,s)>=L/(20Q)=v^6/20` for every reduced pair.  Apply (1), (2), and
(7):

```text
A_v(W) >= (L/(20Q)) (75H/2) v^(8-3delta)
        = (15/8) v^(26-3delta).                         (ALB)
```

This proof keeps the actual rational labels and averages the true bounded
jitter.  It does not select a favorable jitter separately for each cell.

## `PROVED` raw-`R` (L^2) upper scale

The frozen source is `LargevaluesDirichlet17.tex`, Lemma `RL2` (lines
1242--1243 in the pinned copy): if `W` is `T^epsilon`-separated in an
interval of length `T`, then

```text
integral_(x asymp 1) |R_W(x)|^2 dx <<_epsilon |W|.       (RL2)
```

`PROVED`: the CRR-v2 Base predicate makes `W` `H^(1/100)`-separated and
contained in `[0,H]`, so `RL2` applies with `T=H` and `epsilon=1/100`.
For `|theta|<=3`, the elementary bound `exp(x)-1<=2x` for `0<=x<=1/2`
places

```text
{a exp(theta/H): |theta|<=3} subset [a-8/H,a+8/H].       (8)
```

These theta-neighborhoods are pairwise disjoint because their diameter is
`16/H<1/(4Q^2)`.  They lie in `[1/2,3/2]`.  Changing variables in each
disjoint interval gives

```text
sum_a integral_(-3)^3 |R_W(a exp(theta/H))|^2 dtheta
 = H sum_a integral_(a exp([-3,3]/H)) |R_W(u)|^2 du/u
 <= 2H integral_(1/2)^(3/2) |R_W(u)|^2 du
 << H |W|.                                               (9)
```

`PROVED`: every ray also has the elementary upper count
`#K_(r,s)<=9L/(5Q)<=2L/Q`.  Equations (1), (2), and (9) give

```text
A_v(W) << (L/Q) H |W|.
```

Under Base cardinality `|W|<=v^(8+delta)`, this is

```text
A_v(W) << v^(12+6+8+delta)=v^(26+delta)=v^(26+o(1)).     (AUB)
```

## The exact scope of the saturation statement

`PROVED`: `(ALB)` and `(AUB)` meet at central exponent `26`; their only
displayed exponent separation is `4 delta(v)=o(1)`.  Therefore a fixed
power saving for `A_v(W)` cannot be obtained *from the raw global `RL2`
estimate and Base cardinality alone*.  A route to such a saving must use
information discarded in (9): Base/coefficient coupling, or a stronger
arithmetic/restricted-(L^2) input on these Farey rays.

This is deliberately not a universal impossibility claim.  It does not say
that v1 FARI, the averaged target below, or another analytic argument cannot
have a fixed power gain.  It isolates exactly why the uncoupled global-(L^2)
step cannot supply one.

For precision, define the new target `AFARI_eta` for fixed `eta>0`:

```text
For all sufficiently large v, every H^(1/100)-separated W subset [0,H]
with a Base(v) coefficient vector satisfies A_v(W)<=v^(26-eta).
```

`CONJECTURED`: no proof or disproof of `AFARI_eta` is supplied.  `PROVED`,
conditional on `AFARI_eta`: for sufficiently large `v` with
`3delta(v)<eta`, `(ALB)` contradicts `AFARI_eta`; therefore `AFARI_eta`
implies CRR-U.  This conditional gate makes no assertion about whether the
needed coefficient-coupled or arithmetic gain is true.

## Falsifiers and replay

The lower reduction would be refuted by failure of expanded-cell disjointness,
the smoothing-incidence estimate, the theta-cover/Jacobian calculation, the
ray lower count, or the labeled identity (1).  The raw upper route would be
refuted by failure of the `RL2` hypotheses, theta-neighborhood disjointness,
or the ray upper count.  An asymptotic Base-plus-RationalMass family attaining
the lower scale refutes every `AFARI_eta` that covers it.

```sh
python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v2.py --write
python3 proof/build_cycle_5_crr_farey_log_gram_reduction_v2.py --check
python3 -m unittest tests/test_cycle_5_crr_farey_log_gram_reduction_v2.py
```
