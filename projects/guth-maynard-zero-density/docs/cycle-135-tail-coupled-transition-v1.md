# Cycle 135: tail-only projection is self-dual; the paired edge survives

For one collision put

```text
Y=1/(q|g^a-p/q|),       R=r+tq,
theta=(Y-R)/q.                                      (1)
```

The next-convergent condition is simply

```text
R<Y<R+q,       equivalently 0<theta<1.              (2)
```

As `t` runs through consecutive integers, the intervals in (2) tile:

```text
(r+tq,r+(t+1)q).
```

A complete shear block therefore has only two outer boundaries.  Fourier
projection in `theta` cancels its internal boundaries but leaves exactly the
single logarithmic-center interval already obtained in Cycle 132.  Thus a
tail-only marginal does not reduce the `S/N` transition entropy; it is
self-dual with the Cycle-132 discrepancy problem.

There is, however, an exact phase-coupled object which the marginal discards.
Write

```text
x_a=p_a/q_a,
g^a=x_a+s_a/[q_a(R_a+theta_a q_a)],       s_a=+-1. (3)
```

For an edge `b=a+d`, using `g^b=g^d g^a` in (3) gives

```text
x_b-g^d x_a
 =g^d s_a/[q_a(R_a+theta_a q_a)]
  -s_b/[q_b(R_b+theta_b q_b)].                     (4)
```

This retains the mode difference, both orientations, both next denominators,
and both tail coordinates.

On `q~N`, `R~S`, normalize

```text
Omega_d(a)=NS (x_(a+d)-g^d x_a).                   (5)
```

It has bounded scale on compact support.  Varying either tail through a unit
interval changes (5) on scale `N/S`; hence the natural resolving frequency is

```text
L=S/N,                                             (6)
```

or `S^2` against the unnormalized residual.  The next genuinely new estimate
is the fixed-difference paired-tail norm

```text
sum_(|ell|<=L)
  |sum_(a in E_d) w_a e(ell Omega_d(a))|^2
    << L |E_d| X^epsilon.                          (7)
```

Unlike the marginal projection, (7) preserves the signed residual identity
(4) and can distinguish the shears from Cycle 134.  It is an exact target,
not a proved estimate.

No paired-tail bound, transition concentration, recurrence seed, endpoint,
moment, density, or prime-interval theorem is proved.
