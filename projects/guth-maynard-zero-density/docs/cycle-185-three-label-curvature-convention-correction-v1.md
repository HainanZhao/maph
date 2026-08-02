# Cycle 185 correction: the shifted positive-exponential slope

## Correction and claim boundary

`PROVED`: the original Cycle 185 identity is false under the project's pinned
phase convention.  The ray slope is

```text
alpha_ell = exp(2*pi*ell/Delta)-1,
```

so an arithmetic-progression label triple satisfies

```text
(1+alpha_(ell-r))*(1+alpha_(ell+r)) = (1+alpha_ell)^2,
```

not `alpha_(ell-r)*alpha_(ell+r)=alpha_ell^2`.  The original unshifted
curvature conclusion, its syzygy as a statement about that `K`, and its depth
exactification are therefore withdrawn.

`PROVED`: setting `B_i=A_i+U_i` repairs the local algebra.  The corrected
integer

```text
K_plus = U_0^2*B_-*B_+ - U_-*U_+*B_0^2
```

has the exact product expansion for `z_i=1+alpha_i`, is divisible by `v^2`,
and retains the same primitive pair-determinant syzygy because the common
intercept factor makes the numerator shift cancel.  The depth bound is the
former bound with a cap for `z_i`, rather than `alpha_i`.

The abstract AP-free mass/capacity/stable-shell obstruction in Cycle 185 does
not use the false identity and remains valid as stated.  This correction
proves no actual-exponential distribution theorem, populated-box bound,
recurrence, density gain, or interval result.

## Exact shifted algebra

Write `z_i=1+alpha_i` and `B_i=U_i*z_i+epsilon_i=A_i+U_i`, with
`U_i=v*u_i`.  At AP labels, `z_-z_+=z_0^2`.  Therefore

```text
K_plus/v^2
 = u_0^2*B_-*B_+ - u_-*u_+*B_0^2
 = u_0*B_+*(u_0*B_- - u_-*B_0)
   -u_-*B_0*(u_+*B_0-u_0*B_+).                            (1)
```

Since `B_i=A_i+v*u_i`, both bracketed determinants in (1) equal their Cycle
183 `A`-numerator counterparts.  Thus no coefficient data is dropped.  The
error expansion is the previous five-term formula with every `alpha_i`
replaced by `z_i`.

## Disposition

The original artifact stays immutable.  This correction is the authority for
all future use of Cycle 185: cite only `K_plus`, retain the non-exponential
status of the AP-free occupancy, and rederive any downstream use from the
corrected record.

