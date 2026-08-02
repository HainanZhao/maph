# Cycle 146: the collision mask must retain its negative halo

## Claim boundary

`PROVED`: the Cycle-87 pair detector is a zero-mode-free high-pass kernel; if
the dyadic moment cutoff is additionally chosen nonnegative, it is also a
Gram kernel.  A nonnegative incidence replacement necessarily inserts a
positive zero mode.  A deterministic arithmetic partition can nevertheless
retain the actual signed coefficients: one cell inherits at least the
average real signed contribution, with the exact cell entropy charged.

No arithmetic-cell estimate, paired norm, endpoint, complete moment, density
gain, or interval gain is proved.

## Exact high-pass kernel

Poisson summation gives the two identical forms

```text
Psi_K(t)=sum_(k in Z) U(k/K)e(kt)
        =K sum_(m in Z) hat U(K(m-t)).             (1)
```

The frozen frequency cutoff is supported away from zero, hence

```text
int_(R/Z) Psi_K(t)dt=U(0)=0.                      (2)
```

Cycle 87 froze a smooth dyadic cutoff but did not require its sign.  Under
the additional standard choice that the moment cutoff is nonnegative, its
pair quadratic form is

```text
sum_(i,j)c_j conjugate(c_i)Psi_K(z_j-z_i)
 =sum_k U(k/K)|sum_j c_j e(kz_j)|^2 >=0.          (3)
```

Thus `Psi_K` is a Gram kernel whose feature vector is
`(sqrt(U(k/K))e(kz))_k`.  The absent `k=0` coordinate is exactly the absent
continuous volume term.

Even though (3) is positive as a quadratic form, the pointwise kernel is not
a positive collision indicator.  Its real part has mean zero, so

```text
int (Re Psi_K)_+ = int (Re Psi_K)_-.              (4)
```

The negative halo is therefore not an error term; it balances the positive
collision core.

## Why positive incidence restores the barrier

If a nonnegative majorant is at least one on a circle interval of width `w`,
its mean is at least `w`.  On the natural collision width `w~1/K`, the
scaled kernel `K` times that majorant has constant mean per atom pair.  This
is precisely the zero-mode/volume contribution that obstructed the unsigned
route.  No nonzero nonnegative kernel can simultaneously retain (2).

## Signed arithmetic-cell inverse

Partition all oriented pairs deterministically into `P` arithmetic cells,
before taking absolute values.  For a cell `C`, define

```text
q_C=Re sum_k U(k/K)
       sum_((i,j) in C)c_j conjugate(c_i)e(k(z_j-z_i)). (5)
```

The cells partition the exact quadratic form, so

```text
sum_C q_C=E.                                      (6)
```

If `E>0`, at least one cell satisfies

```text
q_C>=E/P.                                         (7)
```

This is the missing coefficient-preserving interface.  Each pair in the
winning cell can be decorated with its mode difference, rational centers,
next-convergent matrices, orientations, and tails without altering (5).
The Fourier label `k` and correlation product must remain attached.  The
factor `P` is real entropy and must be paid; (7) alone does not show that the
current fine partition is affordable.

## New theorem contract

Construct a hierarchical arithmetic partition in which only the labels
needed for the next estimate are frozen at each stage.  At every split,
retain the real signed contribution and stop before the accumulated cell
entropy consumes the diagonal excess.  A terminal cell must either satisfy a
signed vector-autocorrelation estimate or output a coefficient-faithful
fixed-phase obstruction.

## Gate effect

The gate becomes `SIGNED_HIGH_PASS_CELL_ENTROPY_OPEN`.
