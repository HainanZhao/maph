# Cycle 7 CRR signed F4F projection and phase-lattice extremizer v1

## Claim boundary

`PROVED`: after taking logarithmic coordinates, the exact signed
pair-sum/Farey kernel for the local fourth moment is a positive-semidefinite
Fourier projection.  On unrestricted `L^2` pair-sum profiles its normalized
operator norm is exactly one, and this remains true after imposing any finite
number of homogeneous continuous linear Mellin/Fourier diagnostics.  Thus
ambient positivity, energy as an `L^2` size, and finitely many such linear
diagnostics cannot by themselves produce a fixed signed spectral saving.

`PROVED`: on every sufficiently large even scale there is an equal-weight,
actual-Farey phase-lattice set `W` with the frozen cardinality, separation,
and full CRR energy band, but whose fourth moment on one genuine reduced
Farey jitter cell is at least a fixed multiple of `v^20`.  This is a sharp
scoped no-go for any F4F proof that uses only those set/energy conditions.

`PROVED`: a near-maximal one-cell Mellin value forces the row set close to a
single phase lattice.  The construction realizes the exact endpoint of this
inverse statement.

`CONJECTURED`: the construction is *not* shown to arise from a common
coefficient vector satisfying the full `Base(v)` pointwise predicate, nor is
it shown to satisfy `RationalMass(v)` or `PositiveCubic(v)`.  Hence it neither
refutes `F4F_eta` on the actual Base class nor proves F4F, AFARI, CFARI,
CRR-U, a density gain, a short-interval theorem, a full-method saturation
theorem, or an L-function result.  Its precise conclusion is that a
successful signed route must exploit nonlinear self-convolution realizability
and/or the common Base coefficient constraint, rather than energy and a
finite-dimensional spectral test alone.

## `PROVED`: exact signed pair-sum projection

Put

```text
E_v=log(U_v)
    = union_((r,s) in F_Q) [log(r/s)-3/H, log(r/s)+3/H].
```

The Cycle 5 disjointness makes this equality a disjoint union.  The change of
variables `u=exp(x)` turns `du/u` into `dx`.  For an arbitrary finite real
row set `W`, define its positive atomic row and pair-sum measures by

```text
lambda_W=sum_(t in W) delta_t,
nu_W=lambda_W*lambda_W
    =sum_(t,t' in W) delta_(t+t').
```

Their Fourier transform is exactly

```text
nu_hat_W(x)=integral exp(i s x)dnu_W(s)
           =(sum_(t in W) exp(i t x))^2
           =R_W(exp(x))^2.                               (1)
```

Consequently the signed expansion from the preceding F4F reduction admits
the positive form

```text
I4_log(W)=integral_(E_v)|nu_hat_W(x)|^2 dx
         = integral_(E_v)|R_W(exp(x))|^4 dx
         = <nu_W,K_v nu_W>,                              (2)

K_v(s,s')=integral_(E_v)exp(i(s-s')x)dx
          =J_H(s-s')S_Q(s-s').                           (3)
```

Here `J_H` and `S_Q` are the exact bounded-jitter and reduced-label Mellin
sums from Cycle 7 F4F v1.  Thus (3) retains every coprime ordered `(r,s)` and
the true interval `|theta|<=3`; it is not a generic alias kernel.  The
apparently signed Farey expansion is positive semidefinite because (2) is a
sum of squared Fourier amplitudes.

Use the unitary Fourier transform

```text
(Ff)(x)=(2 pi)^(-1/2) integral_R f(s) exp(-i s x) ds
```

on unrestricted `L^2(R)`, and define

```text
P_(E_v)=F^(-1) M_(1_(E_v)) F.
```

It is an orthogonal projection, with distribution kernel

```text
P_(E_v)(s,s')=(2 pi)^(-1)K_v(s,s').                      (4)
```

Therefore

```text
0<=P_(E_v)<=I,  ||P_(E_v)||_(L^2->L^2)=1.               (5)
```

The norm is exactly one, not merely at most one, because `E_v` has positive
measure and `F^(-1)L^2(E_v)` is a nonzero (indeed infinite-dimensional)
eigenspace of eigenvalue one.

This ambient statement has a useful finite-diagnostic strengthening.  If
`ell_1,...,ell_m` are any fixed finite collection of homogeneous continuous
linear functionals on `L^2(R)`, then

```text
F^(-1)L^2(E_v) intersect ker(ell_1) intersect ... intersect ker(ell_m)
```

is still infinite-dimensional.  Every nonzero `f` in this intersection
satisfies `P_(E_v)f=f`.  Thus no inequality of the form

```text
<P_(E_v)f,f> <= (1-c)||f||_2^2,   c>0,                  (6)
```

can follow on unrestricted profiles from their `L^2` size plus finitely many
such homogeneous linear Mellin/Fourier moments.  This is a finite-rank
no-go, not an assertion about arbitrary prescribed nonhomogeneous data.

The atomic measure `nu_W` in (2) is not an `L^2` function, so (5)--(6) do
not themselves prove an extremizer in the nonlinear row-set class.  That
additional restriction is exactly

```text
nu=lambda*lambda,  lambda=sum_(t in W)delta_t,
with equal positive atomic row weights and one common W.                 (7)
```

The following construction proves that even this nonlinear restriction does
not let cardinality, separation, and the tolerance-one energy band alone
force a saving.

## `PROVED`: an actual reduced-Farey phase-lattice extremizer

Restrict to even integers `v` tending to infinity.  Then `Q=v^4` is divisible
by four.  Define one actual reduced label

```text
r_Q=Q+1,
s_Q=5Q/4+1,
alpha_Q=r_Q/s_Q,
P_Q=2 pi/log(s_Q/r_Q).                                  (8)
```

For `Q>=4`, `Q<=r_Q,s_Q<2Q`,

```text
gcd(r_Q,s_Q)=gcd(Q+1,Q/4)=1,
4/5 < alpha_Q <= 5/6.
```

Hence `(r_Q,s_Q)` is one of the *actual* labels in `F_Q`.  The elementary
inequalities `pi>3`, `pi<22/7`, `log(1+x)<=x`, and
`log(1+x)>=x/(1+x)` give the convenient absolute bounds

```text
24 < P_Q < 38.                                          (9)
```

Set

```text
N=floor(H/P_Q),  X={0,1,...,N},  n=|X|=N+1,
M=2R=2Q^2,
D=ceil(H^(1/100)/P_Q).                                  (10)
```

For sufficiently large `Q`, `n>H/38`, `n>=2M`, and
`D<=H^(1/100)`.  Choose a uniformly random `M`-element subset `B` of `X`.
Let

```text
E_add(B)=#{(b1,b2,b3,b4) in B^4:b1+b2=b3+b4},
C_D(B)=#{ {b,b'} subset B: 0<|b-b'|<D }.
```

The elementary random-subset bounds are

```text
E[E_add(B)] <= M+24M^2+16M^4/n <= 2^14 Q^5,             (11)
E[C_D(B)] <= 2 D M^2/n <= 304 Q^(103/100).              (12)
```

For (11), tuples using fewer than four distinct values contribute at most
`M+24M^2`: after choosing a repeated pair of positions and two values, the
additive equation fixes the remaining entry.  For four distinct values,
choose the first three entries; the fourth is fixed.  The inclusion
probabilities are bounded by `(2M/n)^2` and `(2M/n)^4`, respectively.  For
(12), there are at most `nD` close unordered pairs and each has inclusion
probability at most `2M^2/n^2`.

Markov's inequality, applied with factor four to both nonnegative variables,
therefore gives one `B` with

```text
E_add(B)<=2^16 Q^5,
C_D(B)<=1216 Q^(103/100)<Q^2=R                         (13)
```

for all sufficiently large `Q`.  Greedily delete one endpoint of each close
pair.  This deletes at most `C_D(B)` points and leaves a `D`-separated subset
of size at least `R`.  Taking any `R` of its points gives `A`.  Additive
energy does not increase under deletion, so

```text
E_add(A)<=2^16Q^5.                                      (14)
```

Conversely `A+A` has at most `2N+1<=H` elements.  Cauchy--Schwarz gives

```text
E_add(A)>=|A|^4/|A+A|>=R^4/H=Q^5.                       (15)
```

Finally put

```text
W_Q={P_Q a:a in A}.                                     (16)
```

It is a single common real row set in `[0,H]`, has `|W_Q|=R`, and is
`H^(1/100)`-separated.  Since `P_Q>24`, a difference of two pair sums of
`W_Q` has absolute value at most one precisely when the associated integer
pair sums agree.  Thus its frozen tolerance-one energy is exactly

```text
E(W_Q)=E_add(A).
```

Equations (14)--(15) imply, after the usual eventual absorption of the fixed
constant `2^16`,

```text
v^(20-delta(v)) <= E(W_Q) <= v^(20+delta(v)).           (17)
```

The phase synchronization is exact at the genuine Farey label `alpha_Q`:

```text
alpha_Q^(i P_Q a)=1  for every integer a.               (18)
```

For `|theta|<=1/10`, every `t=P_Q a` in `W_Q` obeys

```text
Re((alpha_Q exp(theta/H))^(it))
 =cos(t theta/H) >= cos(1/10) >=9/10.
```

The subinterval `|theta|<=1/10` belongs to the true jitter cell of
`alpha_Q`.  Since `alpha_Q exp(theta/H)>=(3/4)(9/10)` there, changing
variables back to `u` proves

```text
integral_(U_v)|R_(W_Q)(u)|^4 du
 >= (1/20) R^4/H
 = (1/20) Q^5
 = (1/20) v^20.                                        (19)
```

This is an actual-label, actual-jitter, equal-weight, signed-kernel
extremizer.  In particular, for every fixed positive `eta`, the conclusion
of `F4F_eta` fails on this energy/spaced/cardinality class along an unbounded
even sequence.  It does **not** fail on the full Base class unless one also
supplies a common coefficient vector meeting Base's pointwise condition.

## `PROVED`: one-cell inverse structure and the remaining gate

The extremizer is not accidental.  Let `alpha>0`, `alpha!=1`, and suppose
that a finite row set has the near-maximal one-cell value

```text
|R_W(alpha)| >= (1-epsilon)|W|,  0<=epsilon<=1.         (20)
```

Choose the phase `z` of `R_W(alpha)`.  Then exactly

```text
sum_(t in W)|alpha^(it)-z|^2
 =2|W|-2|R_W(alpha)| <=2epsilon|W|.                     (21)
```

If `dist_(2pi)(t log(alpha)-arg(z))>lambda`, where
`0<lambda<=pi`, its summand in (21) is at least
`4lambda^2/pi^2`.  Hence

```text
# {t in W: dist_(2pi)(t log(alpha)-arg(z))>lambda}
 <= pi^2 epsilon |W|/(2lambda^2).                       (22)
```

Thus near-maximal Mellin coherence forces all but a controlled exceptional
set into one coset of the phase lattice of period `2pi/|log(alpha)|`.  The
sets in (16) are the zero-error endpoint `epsilon=0` at `alpha_Q`.

`CONJECTURED`: Base's common coefficient condition, the rational-mass
predicate, or the positive cubic predicate may exclude the phase-lattice
profiles in (22) at the scale required by (19).  Nothing sealed so far proves
that exclusion.  The remaining signed F4F problem is therefore a genuinely
nonlinear inverse question about profiles of the form (7), coupled to one
coefficient vector `b`; it is not an ambient PSD or finite-rank spectral
question.

## Consequence and falsifiers

`PROVED`: the local fourth-moment path has a sharper boundary.  The absolute
Wiener route is impossible by the preceding F4F artifact; this note shows
that merely retaining signs and appealing to generic PSD/spectral contraction
is also insufficient.  Any advance must use an additional property that
excludes (16) or controls the nonlinear pair-sum image (7) together with
Base's common coefficients.

This note would be refuted by an error in the exact logarithmic Fourier
identity, the projection normalization, the random-subset bounds, the
reduction of tolerance-one energy to exact additive energy, or the actual
Farey-label/jitter calculation.  A proof that the full Base predicate excludes
the phase-lattice inverse pattern (22) would be a substantive next result.

## Replay

```sh
python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --write
python3 proof/build_cycle_7_crr_f4f_signed_projection_extremizer_v1.py --check
python3 -m unittest tests/test_cycle_7_crr_f4f_signed_projection_extremizer_v1.py
```
