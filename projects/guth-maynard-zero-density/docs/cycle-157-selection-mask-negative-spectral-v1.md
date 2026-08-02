# Cycle 157: raw Gram obstruction and coefficient-weighted negative spectrum

## Claim boundary

`PROVED`: for a fixed nonzero difference, let

```text
K^(d)_ell(a,a')=chi(a,d,ell)1_(a'=a+d),
H^(d)_ell=(K^(d)_ell+K^(d)*_ell)/2.                (1)
```

The raw fixed-difference mask has zero diagonal. If `H_ell` is nonzero, it
cannot be positive semidefinite; if `(H_ell)_(a,b)!=0`, its two-by-two
principal compression has lower eigenvalue `-|H_(a,b)|`, hence
`lambda_min(H_ell)<=-|H_(a,b)|` by interlacing.

Moreover, with the convention in (1),

```text
c_ell^* H^(d)_ell c_ell = Re(c_ell^* K^(d)_ell c_ell). (2)
```

For nonnegative external weights `q_(ell,d)`, if

```text
-sum_(ell,d) q_(ell,d)c_ell^*H_(ell,d)c_ell >= kappa W_h,
```

then spectral splitting `H=H_+-H_-` gives exactly

```text
sum_(ell,d)q_(ell,d)||H_(ell,d),-^(1/2)c_ell||_2^2
>= kappa W_h.                                     (3)
```

All rows retain anchor, tail, orientation, tensor-frequency, fixed-difference,
and external-weight labels.

This does not show that the actual coefficient vector aligns with one
negative eigenspace, that negative energy sits in finitely many blocks, that
the mask admits an approximate Gram transport, or that there is a finite
escape partition, moment, density, or interval theorem.

## Proof

A PSD Hermitian matrix with a zero diagonal has every row and column zero by
the Cauchy--Schwarz inequality for its Gram vectors. Thus a nonzero
zero-diagonal mask is not PSD. The stated two-by-two compression is

```text
[[0,H_ab],[conjugate(H_ab),0]],
```

whose eigenvalues are `+-|H_ab|`; Hermitian interlacing yields the displayed
global negative eigenvalue.

Equation (2) follows by taking the real part of `c^*Kc`. Finally
`c^*Hc=||H_+^(1/2)c||^2-||H_-^(1/2)c||^2`. Multiply by
`q_(ell,d)>=0`, sum, and discard the nonnegative positive-spectral term to
obtain (3).

## Gate effect and decision record

This rules out exact raw-mask Gram transport and converts any actual negative
mask correlation into coefficient-weighted negative spectral energy. The next
task is concentration of that energy in a fixed labelled block family, or a
quantified block-complexity inverse.

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity and recommended banking this scoped lemma inside
Cycle 157 on 2026-08-02 UTC. The primary adopts that recommendation.
