# Cycle 157 preregistration: coefficient-weighted selection-mask cone inverse

Date frozen: 2026-08-02 UTC.

## Objective

Work with the actual Cycle-144/145 coefficient type rather than a scalar
collision surrogate. On each frozen anchor/tail/tensor-frequency/orientation
block, form the Hermitian real-projection selection kernel

```text
H_ell(a,a') = (K_ell(a,a') + conjugate(K_ell(a',a)))/2,
K_ell(a,a') = chi(a,a'-a,ell),
```

together with the actual coefficient vector `c_a(ell)`. The relevant
functional is the retained real coefficient correlation, normalized at the
Cycle-150 one-witness scale; it is not an unweighted matrix metric.

## Target dichotomy

For fixed `kappa>0`, prove one of the following with all constants independent
of the asymptotic parameter.

1. **Positive transport.** On the retained mass, the Hermitian mask has a
   labelled positive-Gram representation

   ```text
   H_ell = sum_(j<=J_kappa) lambda_j u_(j,ell)u_(j,ell)^* + E_ell,
   lambda_j>=0, sum_j lambda_j<=C_kappa,
   ```

   with a frozen normalization on the `u_j`, with every anchor/tail/tensor
   frequency/orientation label retained, and with the aggregate actual
   coefficient-weighted one-witness correlation of `E` at most `kappa/8`.
   This is only a possible bridge toward coefficient-positive transport; its
   compatibility with Cycle 152 must still be proved.

2. **Coefficient-complexity inverse.** A labelled block carries normalized
   correlation at least `c_kappa>0` and supplies an explicit dual sign,
   rectangle, or negative-spectral witness separating its Hermitian mask from
   every such bounded positive-Gram cone. The witness retains the anchor
   block, coefficient vector, frequency range, tail labels, and its numerical
   `c_kappa`.

The dual separation must be in the actual coefficient-weighted correlation
geometry. A statement merely that an unweighted rank exceeds `J_kappa`, or
that a raw oriented mask is not Hermitian, is not an output.

## Registered failure

If the actual mask cannot be put into a finite block family without an
`X^(o(1))` complexity loss, preserve the growing block parameter and an exact
additive labelled decomposition as the Cycle-155 coefficient-complexity
inverse. Do not present the loss as a fixed cone rank.

## Boundary and companion checkpoint

This is a discovery-stage structural theorem search. It does not prove a
finite escape partition, a selected-autocorrelation bound, a complete moment,
density, or prime-interval result.

The persistent companion `/root/guth_maynard_session_mentor` was reactivated
under its stable identity and recommended this theorem on 2026-08-02 UTC.
The primary adopts it because Cycle 150's finite taxonomy is only relative to
the smooth endpoint model, while Cycle 144 leaves the actual coefficient
pushforward open.
