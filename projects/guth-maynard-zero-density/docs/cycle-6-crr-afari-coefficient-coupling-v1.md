# Cycle 6 CRR coefficient--Farey coupling reduction v1

## Claim boundary

`PROVED`: conditional on the frozen CRR-v2 `Base(v)` predicate and the
checked Guth--Maynard raw-`R` fourth-moment lemma, the actual-Farey averaged
bundle has the energy-restricted upper scale

```text
A_v(W) << H^(o(1)) L H^(1/2) E(W)^(1/2) = v^(26+o(1)).
```

`PROVED`: conditional on the v2 `RationalMass(v)` predicate, the same
actual-Farey union carries a fourth moment at least a constant times
`v^(20-6 delta(v))`.  Thus the existing global fourth-moment/energy route is
critical at central exponent `26`; it cannot by itself give a fixed-power
version of `AFARI`.

`PROVED`: the Base coefficient vector yields a phase-sensitive Rayleigh
lower bound on the same `W`.  This produces the explicit coefficient-coupled
target `CFARI_eta` below.  A fixed saving in that target implies `AFARI` and
therefore CRR-U.

`CONJECTURED`: neither `AFARI_eta`, `CFARI_eta`, nor the local fourth-moment
saving is proved or disproved here.  The scalar calibration function used to
show sharpness is not asserted to equal `|R_W|^2` for any separated set `W`,
and it has no coefficient vector.  This note proves no CRR-U theorem,
compatible witness, cubic estimate, density gain, short-interval result,
method-saturation theorem, or L-function result.

The result is a precise reduction/no-go only for the currently available
scalar moment/Cauchy route.  It retains the actual reduced Farey labels and
one common `(b,W)` throughout the coefficient step.

## Frozen objects

For an integer `v>=8`, keep the frozen critical scales

```text
H=v^12,  L=v^10,  Q=v^4,  R=v^8,  V=v^7,
delta(v)=1/sqrt(log v).
```

Let `F_Q` be the actual reduced CRR net

```text
F_Q={(r,s): Q<=r,s<2Q, gcd(r,s)=1, 3/4<=r/s<=5/4}.
```

For `a=r/s` define the true bounded-jitter interval

```text
I_a={a exp(theta/H): |theta|<=3},
U_v=union_(a in F_Q) I_a.
```

`PROVED`: the v2 geometry makes the `I_a` disjoint.  The v1 coprime count,
the elementary hyperbolic-sine lower bound, and the v2 `8/H` containment give

```text
(1/50) Q^2/H <= |U_v| <= 16 Q^2/H,
or equivalently (1/50)v^-4 <= |U_v| <= 16v^-4.          (1)
```

Write

```text
R_W(u)=sum_(t in W) u^(it),
Mcal_v(W)=sum_(a in F_Q) integral_(-3)^3 |R_W(a exp(theta/H))|^2 dtheta.
```

The cross-Gram matrix and the labeled plateau rays are those of Cycle 5:

```text
M_W(t,n)=w(n/L)n^(it),
P_theta(t,t)=exp(i theta t/H),
C_theta=M_W^*P_theta M_W,
K_(r,s)={k>0:6L/5<=rk,sk<=9L/5}.
```

`PROVED`: the exact labeled identity is

```text
C_theta(sk,rk)=R_W((r/s) exp(theta/H)).                 (2)
```

and the multiplicities obey

```text
L/(20Q) <= #K_(r,s) <= 2L/Q.                            (3)
```

Consequently the v2 averaged actual-Farey bundle satisfies

```text
(L/(20Q)) Mcal_v(W) <= A_v(W) <= (2L/Q) Mcal_v(W).       (4)
```

This is not a relabeling of a generic logarithmic packet: every summand in
`Mcal_v` carries its original reduced pair `(r,s)`.

## `PROVED`: energy-restricted actual-Farey upper bound

The change of variables `u=a exp(theta/H)` gives the exact identity

```text
Mcal_v(W)=H integral_(U_v) |R_W(u)|^2 du/u.              (5)
```

Since `U_v` lies in `[1/2,3/2]`, Cauchy--Schwarz and (1) yield

```text
Mcal_v(W)
 <= 2H |U_v|^(1/2) (integral_(1/2)^(3/2)|R_W(u)|^4 du)^(1/2)
 <= 8 Q H^(1/2) (integral_(1/2)^(3/2)|R_W(u)|^4 du)^(1/2).    (6)
```

`PROVED`, from Guth--Maynard Lemma `RL4` (pinned source lines 1267--1305):
for a `H^(1/100)`-separated `W` in an interval of length `H`,

```text
integral_(1/2)^(3/2)|R_W(u)|^4du <= H^(o(1)) E(W).        (7)
```

The frozen Base predicate checks exactly those separation and interval
hypotheses and has `E(W)<=v^(20+delta(v))`.  Combining (3), (4), (6), and
(7) gives

```text
A_v(W) << H^(o(1)) L H^(1/2) E(W)^(1/2)
       <= v^(26+o(1)).                                  (8)
```

`PROVED`: the explicit Base-slack contribution before the source's
published subpower factor is `26+(1/2)delta(v)`.  This is bookkeeping, not
an effective fixed-exponent improvement, because Lemma `RL4` is stated with
a subpower loss.

## `PROVED`: RationalMass forces local fourth-moment saturation

Cycle 5 v2 proves, conditional on `RationalMass(v)`,

```text
A_v(W) >= (15/8)v^(26-3delta(v)).                        (9)
```

Using the upper ray weight in (4), then (5) and `u>=1/2`, gives

```text
Mcal_v(W) >= (15/16)v^(20-3delta(v)),
integral_(U_v)|R_W(u)|^2du >= (15/32)v^(8-3delta(v)).     (10)
```

Applying Cauchy--Schwarz inside `U_v` and the upper measure bound in (1)
therefore gives

```text
integral_(U_v)|R_W(u)|^4du
 >= (225/16384)v^(20-6delta(v)).                         (11)
```

`PROVED`: (7) and (11) meet at central exponent `20`.  Thus a proof based
only on the global fourth-moment/energy upper bound, the actual-Farey window
measure, and Cauchy--Schwarz has no fixed power to spare.

The first clean missing analytic statement is consequently the following.

```text
F4F_eta: for some fixed eta>0 and all sufficiently large v,
every Base(v)-admissible W obeys
  integral_(U_v)|R_W(u)|^4du <= v^(20-eta).
```

`CONJECTURED`: `F4F_eta` is not established here.  `PROVED`, conditional on
`F4F_eta`: (6) and (4) imply `A_v(W)<=v^(26-eta/3)` for all sufficiently
large `v` after absorbing fixed constants and subpower factors.  Equation
(11) then contradicts `RationalMass(v)`.  The numerical `eta/3` is only a
safe fixed-loss conversion; no optimization is claimed.

## `PROVED`: scalar envelope sharpness on the true Farey union

Let

```text
f_star(u)=v^10 |U_v|^(-1/2) 1_(U_v)(u).
```

`PROVED`: this scalar function has

```text
integral_(U_v) f_star(u)^2du=v^20,
integral_(U_v) f_star(u)du=v^10|U_v|^(1/2) asymp v^8,
H integral_(U_v)f_star(u)du/u asymp v^20.                (12)
```

The constants in (1) make every `asymp` in (12) two-sided with fixed
explicit constants.  Combining the last display with the ray scale
`L/Q=v^6` gives the bundle scale `v^26`.

`PROVED`: `f_star` saturates the scalar Cauchy exponent in (6) on the
actual Farey union itself.  `OBSERVED`: it is not known whether a separated
Fourier sum `|R_W|^2`, much less one coming from a Base coefficient vector,
can approximate this scalar profile.  Therefore this calibration is not an
AFARI counterexample.  It proves only that scalar support/measure/fourth-
moment data cannot supply the desired fixed saving.

## `PROVED`: the common-coefficient phase bridge

Now retain one Base-admissible pair `(b,W)` and put

```text
D_v(t)=(M_Wb)_t,
a_t=D_v(t)/|D_v(t)|,
G_W=M_WM_W^*.
```

The Base pointwise threshold makes every `a_t` defined.  With the standard
Hermitian inner product,

```text
sum_(t in W) conjugate(a_t)D_v(t)=sum_(t in W)|D_v(t)|
                              >= v^(15-2delta(v)).       (13)
```

Since `||b||_2^2<=L`, Cauchy--Schwarz gives the phase-sensitive consequence

```text
a^*G_Wa=||M_W^*a||_2^2 >= v^(20-4delta(v)).              (14)
```

This is stronger information than merely naming a large eigenvalue: it
retains the phase vector produced by the same `b` that witnesses Base.

For clarity, define the actual-Farey PSD kernel on that same row set by

```text
(K_F)_(t,t')=
  sum_((r,s) in F_Q) integral_(-3)^3
    ((r/s)exp(theta/H))^(i(t-t')) dtheta.
```

`PROVED`: `K_F` is a sum of rank-one positive semidefinite kernels and

```text
1^*K_F1=Mcal_v(W).                                      (15)
```

The ray-weighted kernel has the same labels and satisfies the Loewner
comparison encoded in (3)--(4).

## A precise coefficient-coupled next gate

For fixed `eta>0`, define

```text
CFARI_eta:
  (a^*G_Wa)(1^*K_F1) <= v^(40-eta)
```

for every sufficiently large `v`, every Base-admissible common pair `(b,W)`,
and its phase vector `a` from (13).

`CONJECTURED`: `CFARI_eta` is not proved or disproved.  It is a mixed
two-kernel anti-alignment statement: the large singular direction generated
by the actual coefficient vector must not coexist with an unweighted
actual-Farey concentration direction on the same `W`.

`PROVED`, conditional on `CFARI_eta`: (14) yields

```text
Mcal_v(W)<=v^(20-eta+4delta(v)),
A_v(W)<=2v^(26-eta+4delta(v)).                           (16)
```

For all sufficiently large `v`, fixed constants and `4delta(v)` are absorbed
to give `AFARI_(eta/2)`.  Cycle 5 v2 then gives CRR-U.

Conversely, Base plus RationalMass gives from (10) and (14)

```text
(a^*G_Wa)(1^*K_F1) >= (15/16)v^(40-7delta(v)),           (17)
```

which contradicts every fixed-power `CFARI_eta` at large `v`.  This verifies
that `CFARI_eta` has the sharp central exponent `40` and is a true
coefficient-coupled replacement for the discarded scalar route.

## Scope and next gate

`PROVED`: the old raw-`RL2` bound, the new energy/`RL4` bound, and the scalar
envelope all stop at central bundle exponent `26`.  A successful proof must
use a fact not present in those scalar inequalities: either Fourier
realizability of `|R_W|^2` on the actual reduced Farey union, or the
coefficient-phase interaction in `CFARI_eta`.

`CONJECTURED`: a possible next route is to prove a restricted mixed-kernel
inequality for `G_W` and `K_F`, respecting that `a` is the phase of `M_Wb`;
replacing `a` by an arbitrary vector would not be a coefficient-coupled
claim.  An actual asymptotic Base-plus-RationalMass family refutes `F4F_eta`
and `CFARI_eta` whenever it satisfies the stated hypotheses.

## Replay

```sh
python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --write
python3 proof/build_cycle_6_crr_afari_coefficient_coupling_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_afari_coefficient_coupling_v1.py
```
