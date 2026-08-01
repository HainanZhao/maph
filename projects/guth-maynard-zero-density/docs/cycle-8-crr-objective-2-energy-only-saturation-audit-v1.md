# Cycle 8 CRR Objective-2 audit: energy-only actual-log-Farey saturation v1

## Claim boundary

`PROVED`: the sealed records imply a sharp saturation theorem for the
following **restricted Guth--Maynard subarchitecture**, denoted `EO-LF4`:
the raw fourth-moment/approximate-additive-energy step on the actual reduced
logarithmic Farey union, after the coefficient vector, rational-mass
predicate, and cubic trace have all been discarded.  Its sharp central
exponent is `20`, and it has an actual-label equal-weight phase-lattice
extremizing sequence.

This satisfies Objective 2 only in that explicitly scoped sense: Objective 2
asks for a saturation theorem for a *precisely defined* Guth--Maynard
architecture, and `EO-LF4` is a named, literal subarchitecture of the
critical CRR route.  It is **not** a saturation theorem for the full
Guth--Maynard method, the full CRR common-pair witness architecture, or even
the Base-restricted `F4F_eta` target.  No density gain, short-interval
consequence, L-function theorem, AFARI, CFARI, CRR-U, RationalMass, or
PositiveCubic statement follows.

The exact missing link for any stronger reading is the common capped
coefficient/Base bridge on the same phase lattice.  It is recorded below as
an open gate rather than folded into the completed `EO-LF4` theorem.

## The precisely defined architecture

For sufficiently large even integers `v`, write

```text
H=v^12,  L=v^10,  Q=v^4,  R=v^8=Q^2,
delta(v)=1/sqrt(log v).
```

Keep the actual reduced Farey labels

```text
F_Q={(r,s): Q<=r,s<2Q, gcd(r,s)=1, 3/4<=r/s<=5/4}
```

and their genuine logarithmic-jitter union

```text
U_v=union_((r,s) in F_Q)
      {(r/s) exp(theta/H): |theta|<=3}.
```

For a finite real row set `W`, put

```text
R_W(u)=sum_(t in W) u^(it),
E(W)=#{(t1,t2,t3,t4) in W^4:
       |t1+t2-t3-t4|<=1},
I_v(W)=integral_(U_v)|R_W(u)|^4du.
```

The `EO-LF4` admissible class is

```text
E_v={W subset [0,H]:
     |W|=R,
     W is H^(1/100)-separated,
     v^(20-delta(v))<=E(W)<=v^(20+delta(v))}.
```

This retains the actual CRR height, cardinality, separation, energy
normalization, reduced labels, and bounded jitter.  It deliberately omits
the common Dirichlet coefficient `b`, the Base pointwise condition, the
rational-mass condition, and the signed cubic condition.  The sole analytic
upper mechanism allowed in `EO-LF4` is Guth--Maynard Lemma `RL4`, followed by
restriction from a fixed `u asymp 1` interval to `U_v`.

## `PROVED`: sharp EO-LF4 saturation theorem

For every fixed `epsilon>0`, there are `C_epsilon` and `v_epsilon` such that
for every even `v>=v_epsilon` and every `W in E_v`,

```text
I_v(W) <= C_epsilon v^(20+epsilon).                    (1)
```

Indeed, `U_v subset [1/2,3/2]`, and the checked raw-`R` Lemma `RL4` gives

```text
integral_(1/2)^(3/2)|R_W(u)|^4du <= C_eta H^eta E(W)
```

for every fixed `eta>0`.  Choose `eta=epsilon/24`.  Since `H=v^12`, the
source loss is `v^(epsilon/2)`; eventually
`delta(v)<=epsilon/2`, so the energy upper band gives (1).

Conversely, for every sufficiently large even `v`, there exists a set
`W_v in E_v` with

```text
I_v(W_v) >= (1/20)v^20.                                (2)
```

The construction uses the actual reduced label

```text
r_Q=Q+1,  s_Q=5Q/4+1,  alpha_Q=r_Q/s_Q,
P_Q=2 pi/log(s_Q/r_Q).
```

It chooses an `H^(1/100)/P_Q`-separated integer set `A` of size `R` inside
`[0,floor(H/P_Q)]` with additive energy between `Q^5` and `2^16 Q^5`, and
sets `W_v=P_Q A`.  The pointwise identity

```text
alpha_Q^(iP_Q a)=1  (a in A)
```

forces coherent fourth-moment mass on the actual `|theta|<=1/10` subcell of
the label `alpha_Q`, yielding (2).  It is an existential extremizing
sequence, obtained by the sealed random-subset/deletion argument, not a
claim that every `W` in `E_v` is extremal.

Equivalently, if

```text
M_v=sup_{W in E_v} I_v(W),
```

then

```text
limsup_(v->infinity, v even) log(M_v)/log(v)=20.        (3)
```

Thus for every fixed `eta>0`, a uniform bound
`I_v(W)<=v^(20-eta)` for all sufficiently large even `v` and all
`W in E_v` is false.  The sharp inequality is precisely the exponent-20
raw-energy local fourth-moment bound in this actual-log-Farey architecture.

## Why the result is a real saturation statement, but not a full one

The upper and lower sides concern the same class, functional, scales,
actual reduced Farey labels, and asymptotic quantifiers.  This is stronger
than the earlier scalar profile calibration, whose profile was not asserted
to be a Fourier sum.  It is also stronger than the absolute-Wiener no-go,
which only ruled out one way of proving a saving: here an equal-weight atomic
self-convolution realizes the critical lower exponent.

The theorem does **not** establish a sharp exponent `26` for the complete
ray-weighted bundle `A_v(W)`.  The phase-lattice construction concentrates
on one actual Farey cell; it supplies the `v^20` local fourth-moment lower
bound, not the all-cell RationalMass lower bound that would force
`A_v(W)` at scale `v^26`.  Likewise, the conditional matching of a
RationalMass lower and a global upper at exponent `26` is not an extremizer
theorem, because no one common witness has been supplied.

## Exact missing gate for Base or full-CRR promotion

For a phase-lattice row set `W_(P,A)=P A`, let

```text
Gamma_(P,A)=max_(|b_n|<=1) min_(a in A)
              |sum_(L<n<2L) w(n/L)b_n n^(iPa)|,
lambda_(P,A)=||M_(A,P)||_op^2,
Xi_(P,A)=|A| Gamma_(P,A)^2/((L-1)lambda_(P,A)).
```

The sealed alias-quotient reduction proves the exact equivalence

```text
Gamma_(P,A)>=v^(7-delta(v))
 <=> lambda_(P,A) Xi_(P,A)
     >= |A| v^(14-2delta(v))/(L-1).                    (4)
```

For the extremizing row set `|A|=R`.  Neither side of (4) is known for the
set produced by the energy-only construction.  In particular, energy,
cardinality, separation, a local fourth moment, exact rational aliases, and
ambient PSD projection information do not supply a common capped coefficient
vector.

`CONJECTURED` gate `PL-BASE-BRIDGE`: settle (4), in either direction, for
the actual phase-lattice energy extremizers or uniformly for the relevant
phase-lattice class.  A `Gamma` lower bound would be only a Base lift; a
full CRR-compatible extremizer would still have to verify `RationalMass` and
`PositiveCubic` for the same `(b,W)`.  A fixed-power upper bound for the
distinct-phase quotient norm or `Xi` would exclude Base on that lattice but
would not by itself be a full-method saturation theorem.

## Explicit exclusions and falsifiers

This audit does not claim:

- that the phase-lattice sequence is Base-admissible or refutes
  `F4F_eta` on the Base class;
- that it realizes RationalMass, PositiveCubic, AFARI, CFARI, or the
  ray-bundle lower exponent `26`;
- that every analytic route through the Guth--Maynard method is saturated;
- any new zero-density, primes-in-short-intervals, or L-function result.

The scoped theorem would fail if the actual-jitter cell were not contained
in `U_v`, the phase-lattice construction failed a cardinality, separation,
or energy-band condition, the local lower (2) failed, or the checked `RL4`
upper bound did not apply to this row-set class.  The stronger interpretation
would require closing `PL-BASE-BRIDGE`, not changing the scope of this
theorem after the fact.

## Replay

```sh
python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --write
python3 proof/build_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py --check
python3 -m unittest tests/test_cycle_8_crr_objective2_energy_only_saturation_audit_v1.py
```
