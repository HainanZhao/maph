# Cycle 7 CRR energy-only restricted-log-Farey fourth-moment sharpness v1

## Claim boundary

`PROVED`: in the precisely defined **energy-only restricted-log-Farey
fourth-moment architecture** below, the central exponent is exactly `20`.
The checked global Guth--Maynard `RL4` upper gives `v^(20+o(1))`, while the
sealed actual reduced-Farey phase-lattice construction gives a lower bound
`(1/30)v^20` in the same logarithmic functional along every sufficiently
large even scale. Thus no fixed-power energy-only fourth-moment saving is
possible in this architecture.

`CONJECTURED`: this does not settle the full Base/common-coefficient
Guth--Maynard problem. The lower phase lattice is not proved to possess one
capped coefficient vector satisfying Base's all-row pointwise condition; it
is also not proved to satisfy RationalMass or PositiveCubic. Therefore this
note proves neither `F4F_eta` on the Base class, AFARI, CFARI, CRR-U, a
compatible witness, a cubic estimate, a density gain, a short-interval result,
a full-method saturation theorem, nor an L-function result.

The theorem is deliberately sharper than a scalar-profile calibration: its
lower bound is an equal-weight actual row set with the frozen separation,
cardinality, energy band, an actual coprime Farey label, and true bounded
logarithmic jitter. It is deliberately weaker than a Base counterexample:
the common coefficient and pointwise requirements are excluded from the
architecture by definition.

## The energy-only restricted-log-Farey architecture

For integer `v>=8`, set

```text
H=v^12,  L=v^10,  Q=v^4,  R=v^8,
delta(v)=1/sqrt(log v).
```

Use the genuine reduced Farey shell and true jitter windows

```text
F_Q={(r,s): Q<=r,s<2Q, gcd(r,s)=1, 3/4<=r/s<=5/4},
I_(r,s)={(r/s)exp(theta/H): -3<=theta<=3},
U_v=disjoint union_((r,s) in F_Q) I_(r,s).              (1)
```

The pinned actual-Farey geometry gives `U_v subset [1/2,3/2]` at the frozen
scales. For a finite real set `W`, write

```text
R_W(u)=sum_(t in W)u^(it),
J_v(W)=integral_(log U_v)|sum_(t in W)exp(i t x)|^4dx
      =integral_(U_v)|R_W(u)|^4du/u.                    (2)
```

Let `EO_v` be the class of row sets satisfying exactly

```text
W subset [0,H],
W is H^(1/100)-separated,
v^(8-delta(v))<=|W|<=v^(8+delta(v)),
v^(20-delta(v))<=E(W)<=v^(20+delta(v)),                 (3)
```

where

```text
E(W)=#{(t1,t2,t3,t4) in W^4: |t1+t2-t3-t4|<=1}.          (4)
```

There is no `b`, no pointwise `D_v(t)` condition, no `RationalMass`, and no
`PositiveCubic` in `EO_v`. In particular this is an intentionally restricted
set/energy architecture, not a redefinition of full Base.

For a fixed `eta>0`, its putative saving statement is

```text
EO-F4F_eta: J_v(W)<=v^(20-eta)
for all sufficiently large v and all W in EO_v.          (5)
```

## `PROVED`: checked global upper at central exponent 20

The Guth--Maynard raw-`R` Lemma `RL4` is source-checked in the pinned
coefficient--Farey reduction. Its hypotheses are exactly met by (3): `W` is
`H^(1/100)`-separated in an interval of length `H`. It gives

```text
integral_(1/2)^(3/2)|R_W(u)|^4du <= H^(o(1))E(W).         (6)
```

Because `u` lies between `1/2` and `3/2` on the genuine union,

```text
J_v(W)<=2 integral_(U_v)|R_W(u)|^4du
        <=2H^(o(1))E(W)
        <=v^(20+o(1))                                   (7)
```

uniformly for `W in EO_v`. This is the global upper in the architecture; it
uses no coefficient and no rational-mass antecedent.

## `PROVED`: actual phase-lattice lower at the same exponent

The sealed signed-projection/extremizer construction applies on every
sufficiently large even `v`. With `Q=v^4`, it takes the genuine reduced label

```text
r_Q=Q+1,  s_Q=5Q/4+1,
alpha_Q=r_Q/s_Q,
P_Q=2 pi/log(s_Q/r_Q),                                  (8)
```

and produces an integer set `A` such that

```text
W_v={P_Q a:a in A}                                      (9)
```

belongs to `EO_v`. Its additive-energy construction is needed here: it gives
the full two-sided band in (3), not just a large local Fourier value. Since
`alpha_Q^(iP_Qa)=1` for every `a in A`, the actual label and a true subinterval
of its `|theta|<=3` cell give

```text
integral_(U_v)|R_(W_v)(u)|^4du >= (1/20)v^20.            (10)
```

This is an actual reduced-Farey/jitter statement, not an abstract PSD kernel
or a non-realizable scalar profile. Converting (10) to the *same* logarithmic
functional (2) uses `1/u>=2/3` on `U_v`:

```text
J_v(W_v)>=(2/3)(1/20)v^20=(1/30)v^20.                   (11)
```

## `PROVED`: sharpness theorem and exact scope

Let

```text
S_v=sup_{W in EO_v} J_v(W).
```

Equations (7) and (11) give the formal central-exponent theorem

```text
limsup_(v->infinity, v even) log(S_v)/log(v)=20.         (12)
```

In particular, `EO-F4F_eta` in (5) is false for every fixed `eta>0`: its
purported universal inequality contradicts (11) along the unbounded even
subsequence. This is a `PROVED` saturation/no-go theorem for exactly the
architecture (1)--(4).

It is not a no-go theorem for full Base. The excluded common-coefficient
question is concrete: on the very phase lattice in (9), the sealed
phase-lattice Base reduction leaves open whether a single capped coefficient
can simultaneously have adequate sampled norm and all-row efficiency. The
phase lattice's energy and local Farey concentration alone do not decide
that question. Thus any advance beyond (12) must use information absent from
`EO_v`, such as the common Base coefficient/pointwise constraint, a nonlinear
pair-sum realizability restriction beyond energy, RationalMass/PositiveCubic
coupling, or a new all-row actual log-Farey inverse theorem.

## Falsifiers and replay

The theorem would be refuted by a failure of either pinned predecessor: the
exact `RL4` applicability in (6), or the phase-lattice `EO_v` membership and
actual-cell lower bound (10). It would also fail if the change of variables
in (2) or the elementary factor `2/3`--`2` on `U_v` were wrong. A proof that
the phase lattice is Base-inadmissible would be a new result about the open
coefficient gate; it would not alter this energy-only theorem.

```sh
python3 proof/build_cycle_7_crr_energy_only_f4f_sharpness_v1.py --write
python3 proof/build_cycle_7_crr_energy_only_f4f_sharpness_v1.py --check
python3 -m unittest tests/test_cycle_7_crr_energy_only_f4f_sharpness_v1.py
```
