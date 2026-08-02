# Cycle 172 preregistration: primitive eligible fibre moment no-go

## Question and boundary

Cycle 171 leaves one possible route: a complete primitive source-packet/cross-
edge bank could have an eligibility-weighted divisor moment `M>W`, forcing
seeded deep target mass. This cycle tests whether the *signed abstract local*
Cycle-165/167/170 interface already forces that surplus. It may instead bank
a fully labelled primitive eligible fibre with no surplus and a typed
obstruction. Its frozen negative `alpha` values are outside the actual
positive exponential curve, so it proves no fact about an actual global
census, density, or prime intervals.

## Frozen interface

Require a reduced source packet

```text
(d,b)=1,       |d alpha-b|<=C_S/(K_S X),       d K_S<=H,
```

and a reduced cross edge `qE-a=e` with an affine source fibre whose retained
rows satisfy the Cycle-167 integrality, source/target range, and balance
conditions. Retain its beta seed and all row labels. Put

```text
u=gcd(|d|,a),       v=gcd(q,|d+b|),
g=uv,               G_req=ceil(max(L Lambda,L|qd|/H)).
```

The exact primitive pullback must prove `g=uv` and `gcd(u,v)=1`. The
eligible moment is `M=sum w g/G_req`, with `W=sum w`.

## Proposed no-go family

For every positive integer `m`, freeze

```text
H=10m, K_S=2m, K_E=5m, L=2m,
alpha=-4/5, E=3/2, alpha_plus=-7/10,
d=5, b=-4, q=2, a=3, beta=0,
h_t=15(m+t), j_t=-12(m+t),
h_t_plus=10(m+t), j_t_plus=-7(m+t),
0<=t<=floor(m/3).
```

All errors are zero. The family is intended to satisfy the exact cross-edge
map, both frozen row ranges, divisibility `a|h_t`, `qK_E<=H`, and the
Cycle-167 balance with `Y=1/5`. It has `u=v=g=1`, `G_req=2`, and target
capacity depth `m<L`; hence its full labelled mass is a denominator-capacity
obstruction and `M=W/2` for arbitrary nonnegative row weights.

## Gates and falsifier

1. Prove the primitive pullback and the two-factor Euler divisor expansion,
   retaining every pair label.
2. Verify every family condition exactly, including the cross-edge seed,
   range, balance, source depth, target capacity, and `M=W/2` identity.
3. Conclude only that the listed signed abstract local interface cannot imply
   `M>W` or a positive deep population. It cannot obstruct the actual
   positive-exponential census; the positive-curve primitive-fibre question
   remains a separate next gate.

The falsifier is one failed frozen local condition, a nonprimitive source
relation, `u` or `v` nonunit, or a target that reaches depth `L`. A model not
retaining complete labels is not an admissible no-go result.
