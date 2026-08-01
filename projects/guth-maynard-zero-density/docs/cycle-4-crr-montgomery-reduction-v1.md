# Cycle 4 CRR-to-Montgomery reduction v1

## Claim boundary

`CONJECTURED`: for each fixed `sigma>1/2`, Montgomery's large-value
conjecture gives the stated `N^(2-2*sigma)` cardinality bound for every
one-separated large-value set of a length-`N` Dirichlet polynomial with
coefficient sup norm at most one.  It is not used here as a theorem.

`PROVED`, conditional on the explicitly stated conjectural premise: an
unbounded sequence of CRR Base witnesses contradicts that premise at
`sigma_*=13/20`; in fact it contradicts it at every fixed
`3/5<sigma<7/10`.  The proof is exact exponent algebra plus the Base
definition.  It neither proves CRR-U nor rules out a CRR witness, because its
only analytic large-value input is conjectural.

`PROVED`, conditional on a separately stated uniform three-term
large-value upper bound: fixed power savings in both tied `v^8` terms imply
CRR-U.  A power saving in only one tied term supplies no exponent contradiction
within that three-term architecture.  This last sentence is not a universal
no-go theorem for every possible one-term argument.

This reduction does not use RationalMass or PositiveCubic; it proves no zero
density estimate, short-interval theorem, method saturation theorem, or new
L-function result.  It authorizes no computation or route selection.

## Frozen inputs and translation to the conjecture

The frozen CRR-v2 Base data are

```text
H=v^12,  L=v^10,  delta(v)=1/sqrt(log v),
|W| >= v^(8-delta(v)),
|D_v(t)| >= v^(7-delta(v))  (t in W),
W subset [0,H],  W is H^(1/100)-separated,
D_v(t)=sum_(n>=1) w(n/L)b_n n^(it),  |b_n|<=1.
```

Because `0<=w<=1` and `supp(w) subset [1,2]`, write
`c_n=w(n/L)b_n`.  Then `|c_n|<=1` and `c_n=0` outside `L<=n<=2L`.  Removing
the possible single lower-endpoint term gives
`D_v^+(t)=sum_(L<n<=2L)c_n n^(it)` and
`|D_v^+(t)|>=|D_v(t)|-1`.  The fixed positive threshold margins below absorb
that one coefficient for sufficiently large `v`.  Thus no unverified
endpoint convention is needed.  Since `H>=1`, the `H^(1/100)` separation
implies 1-separation.  A Base witness therefore meets every other
non-conjectural hypothesis of the following frozen source formulation.

Guth--Maynard, *New large value estimates for Dirichlet polynomials*,
Conjecture `cnjctr:Montgomery` (the pinned source TeX, lines 205--210), state:

```text
Let sigma>1/2 and D(t)=sum_(N<n<=2N)b_n exp(i t log n), |b_n|<=1.
If W subset [0,T] is 1-separated and |D(t)|>N^sigma on W, then
|W| <= C(sigma) T^o(1) N^(2-2 sigma).
```

For the exact conditional argument, `T^o(1)` is used only through its standard
fixed-epsilon consequence: for fixed `sigma>1/2` and `epsilon>0`, there are
constants `C(sigma,epsilon)` and `X_0(sigma,epsilon)` such that the displayed
bound is at most

```text
C(sigma,epsilon) T^epsilon N^(2-2 sigma)
```

for all admissible inputs with `max(T,N)>=X_0`.  This epsilon formulation is
also `CONJECTURED`; it is the sole non-algebraic premise of every implication
below.

## Fixed rational anchor: sigma*=13/20

Freeze

```text
sigma_*=13/20,    epsilon_*=1/24.
```

The CRR pointwise threshold and the conjectural threshold have exponents

```text
7-delta(v)  and  10*sigma_*=13/2.
```

Their gap is `1/2-delta(v)`.  If `delta(v)<1/4` and `v^(1/4)>2`, then
`|D_v(t)|>2L^sigma_*`, so the endpoint-trimmed source polynomial still has
`|D_v^+(t)|>L^sigma_*`.

At these scales the conjectural epsilon bound gives

```text
|W| <= C(13/20,1/24) H^(1/24)L^(2-2*(13/20))
     = C(13/20,1/24) v^(1/2)v^7
     = C(13/20,1/24) v^(15/2).
```

The Base lower bound is `v^(8-delta(v))`.  If additionally
`v^(1/4)>C(13/20,1/24)`, then

```text
v^(8-delta(v)) > v^(31/4) > C(13/20,1/24)v^(15/2),
```

a contradiction.  Such `v` occur beyond a finite threshold because
`delta(v)->0` and the conjectural constant is fixed.  Therefore an unbounded
Base witness sequence contradicts the `sigma_*=13/20` epsilon consequence of
Montgomery's conjecture.

## Full fixed-sigma interval

Let `sigma` be any fixed real number with

```text
3/5 < sigma < 7/10.
```

Set

```text
p=7-10*sigma > 0,
g=8-20*(1-sigma)=20*sigma-12 > 0,
epsilon=g/48 > 0.
```

If `delta(v)<p/2` and `v^(p/2)>2`, then
`|D_v(t)|>2L^sigma`, so the endpoint-trimmed polynomial has
`|D_v^+(t)|>L^sigma`.  The conjectural upper bound has total `v` exponent

```text
20*(1-sigma)+12*epsilon
= 8-g+g/4
= 8-3g/4.
```

If also `delta(v)<g/2` and `v^(g/4)>C(sigma,epsilon)`, then the Base lower
bound has exponent larger than `8-g/2`, which exceeds `8-3g/4` by `g/4`.
It therefore contradicts the conjectural upper bound.  This establishes the
conditional reduction at every fixed `sigma` in the open interval.  The
rational anchor `13/20` lies in that interval and has `p=1/2`, `g=1`.

The endpoints are deliberately excluded: the pointwise threshold margin
vanishes at `sigma=7/10`, while the cardinality-exponent gap vanishes at
`sigma=3/5`.

## Joint-saving bridge and the one-saving limitation

Consider the following separate `CONJECTURED` uniform local upper bound at
the CRR scales, for fixed `kappa_2,kappa_3>0`:

```text
|W| <= C(epsilon) v^epsilon
       (v^6 + v^(8-kappa_2) + v^(8-kappa_3))
```

for every `epsilon>0`, every sufficiently large `v`, and every Base-type
large-value configuration to which the bound is meant to apply.  Let
`kappa=min(2,kappa_2,kappa_3)>0` and take `epsilon=kappa/4`.  The right-hand
side is at most `3C(kappa/4)v^(8-3*kappa/4)`.  If
`delta(v)<kappa/2` and `v^(kappa/4)>3C(kappa/4)`, it is strictly smaller than
the Base lower bound `v^(8-delta(v))`.  Thus the algebraic implication is
`PROVED` conditional on this uniform upper bound: such joint savings imply
CRR-U.

If only one of the tied terms is saved, the architecture instead has the
shape

```text
v^o(1) (v^6 + v^(8-kappa_2) + v^8).
```

Its leading exponent remains eight.  The Base lower exponent is
`8-delta(v)`, so exponent comparison alone has no fixed positive gap and
cannot give a contradiction.  This is a limitation of this displayed
three-term comparison, not a claim that a different argument cannot use a
one-term improvement.

## Falsifier and research implication

An actual unbounded Base witness sequence would falsify the fixed-epsilon
form of Montgomery's conjecture throughout `3/5<sigma<7/10`; a finite
witness does neither.  Conversely, this conditional reduction is not a proof
of CRR-U.  The program retains both directions: seek a genuine Base-family
construction, or seek simultaneous savings in the two tied large-value
mechanisms.  Paper-stage hostile review remains deferred; this document has
only received source, algebra, replay, and consistency checks.

## Replay

```sh
python3 proof/build_cycle_4_crr_montgomery_reduction_v1.py --write
python3 proof/build_cycle_4_crr_montgomery_reduction_v1.py --check
python3 -m unittest tests/test_cycle_4_crr_montgomery_reduction_v1.py
```
