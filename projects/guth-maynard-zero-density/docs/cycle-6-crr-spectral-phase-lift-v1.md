# Cycle 6 CRR capped spectral phase lift v1

## Claim boundary

`PROVED`: this note gives an exact finite-dimensional reduction of the
coefficient-capped, all-row `Base(v)` value problem to a phase-lifted
max--min problem.  It also gives a sufficient certificate for the genuine
leading-eigenvector/phase-rounded coefficient construction.  The matrix is
the actual CRR matrix

```text
M_W(t,n)=w(n/L)n^(it),
```

on the actual smooth-weight support and uses one fixed `W` throughout.

`CONJECTURED`: no asymptotic `W` satisfying the spectral gate, the energy
band, and `RationalMass(v)` is constructed here.  The note does not prove or
disprove AFARI, FARI, CRR-U, a positive cubic estimate, a density gain, or a
short-interval theorem.  It replaces neither actual Farey labels nor the
averaged-jitter statistic of the preceding reduction.

The purpose is narrower: distinguish a capped *all-row* construction from
the much weaker fact that `M_W M_W^*` has one large eigenvalue.  This is the
leading-eigenvector/minimum-value mechanism that the earlier equal-weight
phase-rounding finite probe did not implement.

## The capped all-row value is an exact phase-lift program

Fix a finite `W`, write `I_L={n in Z:L<n<2L}`, and put `N=|I_L|=L-1`.
For `b in C^{I_L}` define `D_b=M_W b`.  The coefficient constraint is the
polydisc `|b_n|<=1`, exactly as in `Base(v)`.  Define

```text
Gamma(W)=max_(|b_n|<=1) min_(t in W) |D_b(t)|.
```

For a row-phase vector `z in T^W` (`|z_t|=1`) and a probability vector
`p in Delta(W)`, set

```text
Phi_W(z,p)=sum_(n in I_L) |(M_W^*(p z))_n|.
```

Here `(p z)_t=p_t z_t`.  Then the exact identity is

```text
Gamma(W)=max_(z in T^W) min_(p in Delta(W)) Phi_W(z,p).       (PL)
```

This retains the same `W` in every row, and the actual `n^(it)` labels in
every matrix entry.  It is not a proxy based on an additive finite group.

### Proof of (PL)

For fixed `z`, let

```text
h_t(b)=Re(conjugate(z_t)(M_W b)_t).
```

The finite-dimensional compact convex set
`C_z={ (h_t(b))_(t in W): |b_n|<=1 }` has the elementary separation
identity

```text
max_(c in C_z) min_t c_t = min_(p in Delta(W)) max_(c in C_z) sum_t p_t c_t.
```

Indeed, one inequality is immediate.  For the reverse, if `C_z` misses the
orthant `a*1+R_{>=0}^W`, a separating functional can be chosen nonnegative;
after normalizing its coordinates it is a member of `Delta(W)`, and it gives
the reverse inequality for `a`.  Letting `a` approach the right side proves
the identity.  For fixed `p`, coordinatewise maximization over the polydisc
gives

```text
max_(|b_n|<=1) Re((M_W^*(p z))^* b)=sum_n |(M_W^*(p z))_n|.
```

Finally, for any `b` choose `z_t=D_b(t)/|D_b(t)|` when the row is nonzero;
then `h_t(b)=|D_b(t)|`.  Conversely `h_t(b)<=|D_b(t)|`.  Maximizing over the
compact phase torus yields (PL).

Thus a valid all-row construction is equivalent to finding a row-phase
vector whose *worst* probability weighting has `Phi_W(z,p)>=V`.  Uniform
row weights alone are not a minimum-value certificate: the inner minimizer
in (PL) is part of the exact problem.

## A checked leading-eigenvector certificate

Let `lambda=lambda_max(M_W M_W^*)`, choose a unit top left eigenvector `u`,
and put

```text
x=M_W^*u/sqrt(lambda),
b^ph_n=x_n/|x_n|  (with 0 when x_n=0).
```

Then `|b^ph_n|<=1`.  Define the two dimensionless losses

```text
rho=||x||_1^2/N,
phi=sqrt(|W|) min_(t in W)|(M_W b^ph)_t| / ||M_W b^ph||_2.
```

Both lie in `[0,1]`.  Since `x` is a top right singular vector,

```text
||M_W b^ph||_2^2 >= lambda |<x,b^ph>|^2 = lambda N rho.
```

Consequently

```text
Gamma(W)^2 >= lambda N rho phi^2 / |W|.                 (LEG)
```

This is a true coefficient-capped and all-row certificate, not merely an
aggregate spectral lower bound.  It separates precisely what the top
eigenvalue misses:

- `rho` is the coefficient-cap (right-eigenvector delocalization) loss;
- `phi` is the row-minimum/flatness loss.

For a central-cardinality set `|W|=R=v^8`, suppose, for fixed nonnegative
constants `ell,r,s,gamma`, that

```text
lambda >= v^(12-ell*delta),
rho >= v^(-r*delta),
phi >= v^(-s*delta),
ell+r+2s <= 2-gamma,
delta=1/sqrt(log v).
```

`PROVED`: for all sufficiently large `v`, (LEG) gives
`Gamma(W)>=v^(7-delta)`.  The exact support factor is `N=L-1`; the strict
`gamma` absorbs `(L-1)/L` and all fixed constants because
`v^(gamma*delta)=exp(gamma*sqrt(log v))` tends to infinity.  This is an
asymptotic sufficient gate, not an assertion that its hypotheses occur.

The boundary `ell+r+2s=2` is only a limitation of this certificate: when it
is not met, no conclusion about the existence of other capped coefficients
is licensed.

## Relation to actual Farey--log data

The preceding actual-Farey reduction supplies, from `RationalMass(v)`, a
large statistic made from the same `M_W`:

```text
C_theta(sk,rk)=R_W((r/s) exp(theta/H)).
```

The phase lift does not replace those reduced `r/s`, their rays, or the
bounded jitter.  It makes the remaining Base/coefficient condition a
`W`-dependent exact program.  A compatible asymptotic route must therefore
produce one `W` which simultaneously has the energy/rational properties and
passes either the exact phase program (PL) or the sufficient leading gate
(LEG).  A structural AFARI route could instead upper-bound (PL) on an
actual-Farey/rational class of `W`.

## Falsifiers and next gate

The phase-lift claim would be refuted by an orientation error in the
polydisc support function, failure of the finite separation argument, or a
counterexample to (LEG).  The replay checks the symbolic scale arithmetic;
the accompanying bounded actual-log experiment is deliberately separate and
its output is only `OBSERVED`/`RECOGNIZED`.

The next mathematical gate is an inverse theorem or a construction showing
that a `RationalMass`-relevant actual-Farey set can keep both `rho` and
`phi` above the strict `ell+r+2s<2` threshold.  A numerical leading-vector
run that omits the adversarial `p` in (PL) is diagnostic only, never a
minimum-value proof.

## Replay

```sh
python3 proof/build_cycle_6_crr_spectral_phase_lift_v1.py --write
python3 proof/build_cycle_6_crr_spectral_phase_lift_v1.py --check
python3 -m unittest tests/test_cycle_6_crr_spectral_phase_lift_v1.py
```
