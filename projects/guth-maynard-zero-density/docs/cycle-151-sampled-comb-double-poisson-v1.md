# Cycle 151: halo cancellation needs an lcm resonance and a negative tail lobe

## Claim boundary

`PROVED`: for every smooth halo mode whose denominator remains a fixed power
below `Q`, its correlation with the Cycle-149 divisor comb is supported on
the common frequency lattice `lcm(h,h_b)`.  On that lattice the correlation
has an explicit two-variable tail-transform main term.  Target negative mass
forces both large aggregate gcd capacity and tail parameters in a negative
lobe of this transform.

Boundary denominators and the required halo population are not bounded.  No
full second moment, endpoint, density gain, or interval gain is proved.

## Exact common frequency lattice

Fix the witness denominator `h` and write one halo phase as

```text
c0g^b=r_b/h_b+epsilon_b,
gcd(r_b,h_b)=1,
tau_b=KQ epsilon_b.                               (1)
```

Sample at `k=h ell`.  The rational part is integral precisely when

```text
h_b | h ell.
```

Putting `d_b=gcd(h,h_b)`, this is equivalent to

```text
h_b/d_b | ell,
L_b=lcm(h,h_b)=h h_b/d_b | k.                    (2)
```

For `h_b<=QX^(-delta)`, Cycle 148 makes every nonmultiple of `h_b`
power-negligible.  If `L_b` exceeds the upper support of the `k` block, no
common rational resonance exists and the whole mode is negligible.

## Tail-transform formula

Assume `L_b<=cK` and `|tau_b|<=T` for fixed constants.  Write `k=L_bj`.
After the rational phase disappears, the sampled correlation of this mode is

```text
Gamma_(h,b)
 =Q sum_j U(L_bj/K) sum_n V(n/Q)e(L_bj n epsilon_b)
   +power-negligible error.                       (3)
```

Set `j=(K/L_b)x` and `n=Qy`.  Then

```text
L_b j n epsilon_b=tau_bxy.
```

Smooth two-dimensional Riemann summation gives

```text
Gamma_(h,b)
 =KQ^2/L_b B(tau_b)
  +O_(U,V,T)(KQ^2/L_b)(L_b/K+1/Q),               (4)

B(tau)=int int U(x)V(y)e(tau xy)dxdy.             (5)
```

The same formula follows by Poisson summation in the sampled frequency
variable; (4) records the elementary fixed-chart error explicitly.

## Gcd capacity

The Cycle-149 one-witness negative scale is `KQ^2/h`.  Dividing (4) by that
scale gives the maximum relative capacity of one halo mode:

```text
h/L_b=d_b/h_b=gcd(h,h_b)/h_b.                    (6)
```

Thus a target anti-aligner must satisfy, schematically and with its actual
positive chart weights retained,

```text
sum_b gcd(h,h_b)/h_b >>1.                         (7)
```

Modes with generic small gcd cannot provide enough negative mass unless
they are numerous.  A single-mode canceler requires `h_b` to divide `h` up
to a bounded factor.

## Tail sign

For positive coefficient weights, the sign in (4) is the sign of
`Re B(tau_b)`.  Cycle 147 proves positivity in a fixed neighborhood of
`tau=0`. Therefore every negative halo contribution governed by the
continuum main term must also satisfy, with the discretization margin,

```text
Re B(tau_b)<<-(L_b/K+1/Q).                        (8)
```

The arithmetic and analytic locks are simultaneous: an anti-aligner needs
an admissible lcm, large gcd capacity, and a tail error landing in an actual
negative lobe.

## Remaining boundary

When `h_b` lies within a fixed power of `Q`, the nonmultiple separation
`Q/h_b` is no longer a power.  Formula (4) is not asserted there; those modes
remain the `BOUNDARY_DENOMINATOR` class from Cycle 150.  `PHASE_CHANGE` and
`NONSMOOTH_PAYLOAD` also remain separate.

## Gate effect

The gate becomes `GCD_WEIGHTED_NEGATIVE_TAIL_LOBE_OR_BOUNDARY_OPEN`.
