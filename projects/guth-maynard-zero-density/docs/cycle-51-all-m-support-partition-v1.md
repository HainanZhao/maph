# Cycle 51: every harmonic order has a finite prime-kernel polynomial

## Claim boundary

`PROVED`: for every fixed `s` and every `m>=2`, the distinct-support
correlation of `K(t)^sK(mt)` is an explicit symmetric polynomial in

```text
K(h),K(2h),...,K((s+m)h).                            (1)
```

This extends Cycle 50 through all small harmonic orders. There is no longer
a finite collision exception in the support-kernel architecture.

`OBSERVED`: no bound for these kernel polynomials is proved. Hence no
`DK_s`, `AMPR_s`, `LCAM_s`, density, or interval gain is promoted.

## 1. Exact exponent-partition criterion

A distinct integer label in `K(t)^sK(mt)` has total prime degree `s+m`.
It occurs exactly when one prime can be designated as `q` and have `m`
copies removed, leaving total degree `s`. In terms of its decreasing positive
prime-exponent partition `lambda`, this is equivalent to

```text
lambda partitions s+m,      lambda_1>=m.             (2)
```

Thus the support polynomial is

```text
S_(s,m)(z)=sum_(lambda partitions s+m, lambda_1>=m) m_lambda(z),  (3)
```

where `m_lambda` is the monomial symmetric function. Criterion (2) handles
multiple possible choices of the high-exponent prime automatically and
counts each distinct integer label once.

## 2. Explicit power-sum conversion

For `lambda=(lambda_1,...,lambda_l)`, first sum over ordered distinct prime
indices. Möbius inversion on the lattice of set partitions gives

```text
sum_(i_1,...,i_l distinct) product_j z_(i_j)^lambda_j
 =sum_(pi partition [l])
   product_(B in pi)[(-1)^(|B|-1)(|B|-1)! P_(sum_(j in B)lambda_j)]. (4)
```

Divide (4) by the factorial of the multiplicity of each repeated part of
`lambda`. Equations (3)--(4) are an executable exact formula for
`S_(s,m)` in the power sums `P_r=K(rh)`.

The registered cases `(3,2),(3,3),(4,2),(4,3),(4,4)` were expanded and
checked against direct monomial evaluation on four exact rational alphabets.
These checks diagnose the implementation; equations (2)--(4) are the proof.

## 3. Reconciliation with the stable range

If `m>s`, total degree `s+m<2m`, so (2) has exactly one part at least `m`.
Removing `m` from that part recovers an arbitrary partition of `s`, and

```text
S_(s,m)(h)=K(mh)H_s(h),                              (5)
```

exactly as in Cycle 50. Symbolic polynomial dictionaries agree for
`(s,m)=(3,4),(4,5),(4,7)`.

## 4. Analytic gate

`CONJECTURED` all-harmonic difference-kernel theorem (`ADK_s`): after the
Cycle 39 dyadic selection in harmonic energy and value size, the aggregate
off-diagonal built from `S_(s,m)(t-u)` is diagonal-scale on every hollow
separated row set.

For large `m`, use the simple product (5) and Cycle 48 on structured row
differences. For the finitely many small `m`, use the explicit polynomials
(3)--(4); no separate ambient-length mean value is needed.

## Gate effect

Cycle 50's `PLUS_SMALL_M_OPEN` qualifier is closed algebraically. The live
gate is `ALL_HARMONIC_FACTORED_DIFFERENCE_KERNEL_ADK4_OPEN`.
