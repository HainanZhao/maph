# Cycle 82: smooth projection closes a second Fourier band

## Claim boundary

`PROVED`: the smooth `q`-sum is a rapidly decaying projector onto phases
within `1/Q` of an integer.  Combining it directly with the Cycle-80 phase
occupancy bound gives

```text
|S_k|<=X^(37/45+o(1)).                              (1)
```

Hence every dyadic block `xi<94/225` is strictly below the raw Fourier
target.  This adds the band `163/450<=xi<94/225`, of width `1/18`, beyond
Cycle 80.  Equality at `xi=94/225` ties and is not promoted.

No estimate for `94/225<=xi<=83/75`, packet closure, density gain, or
interval gain is proved.

## Smooth projector

With the Cycle-81 convention

```text
hat V(y)=int V(t)e(-yt)dt,
```

Poisson summation gives the exact identity

```text
Theta_Q(x):=sum_q V(q/Q)e(qx)
           =Q sum_(m in Z) hat V(Q(m-x)).           (2)
```

Because `V` is fixed and smooth with compact support, `hat V` is Schwartz.
For every fixed `A>2`, summing the nearest integer and the remaining tails
in (2) yields

```text
|Theta_Q(x)|<<_(A,V) Q(1+Q||x||)^(-A).             (3)
```

## Occupancy summation

Let

```text
x_d=kc0 exp(2pi d/D) mod 1
```

and let `A_k` be the maximum number of these phases in a circular interval
of length `1/Q`.  Partition the circle into half-open intervals at this
scale, ordered by circular distance from zero.  Each interval contains at
most `A_k` phases, while (3) contributes at most
`Q(1+j)^(-A)` on the `j`-th pair of intervals.  Therefore

```text
|S_k|<=sum_d |Theta_Q(x_d)|
     <<Q A_k sum_(j>=0)(1+j)^(-A)
     <<Q A_k.                                      (4)
```

No Cauchy--Schwarz loss is needed.  Cycle 80 proves
`A_k<=X^(22/45+o(1))`, while `Q=X^(1/3+o(1))`; (4) proves (1), since

```text
1/3+22/45=37/45.                                   (5)
```

## Fourier ledger

A dyadic block containing `X^(xi+o(1))` frequencies has exponent

```text
xi+37/45.
```

It is strictly less than `31/25` exactly when

```text
xi<31/25-37/45=94/225.                             (6)
```

The gain over Cycle 80 is

```text
94/225-163/450=1/18.                               (7)
```

## Strategic implication

The generic maximum-occupancy input has now been fully harvested.  Further
progress should exploit that the projector is centered specifically at the
integer lattice, rather than at the worst circular interval.  The next
object is therefore the fixed-center resonant count

```text
R_k=#{d~D: ||kc0 exp(2pi d/D)||<=1/Q},             (8)
```

together with weighted annular variants.  A bound better than the uniform
`22/45` occupancy exponent on any high-frequency range immediately extends
the cutoff through (4).

## Gate effect

E14/E14D advance jointly to
`SMOOTH_PROJECTOR_BAND_CLOSED_FIXED_CENTER_RESONANCE_OPEN`.

