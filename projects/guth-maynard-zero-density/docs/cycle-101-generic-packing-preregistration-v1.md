# Cycle 101 preregistration: aggregate generic critical fibers

## Claim boundary

This cycle may prove a compact-rational packing lemma and sum the Cycle-100
generic fiber over Cycle-99 injective strong labels. It may not bound
cross-valuation webs, weak rows, simple-root rows, the full alias moment, or
any density/interval exponent.

## Frozen family

- The family has `J` distinct reduced positive labels `N_j/R_j`.
- A fixed `L>=0` satisfies `exp(-L)<=N_j/R_j<=exp(L)`.
- Put `K_L=exp(L)` and `z_j=min(N_j,R_j)`.
- Labels arise from distinct signed `w_j` with `1<=|w_j|<=2M`, hence
  `J<=4M`.
- Let `T_M=max_(1<=n<=2M) tau(n)`.

## Preregistered gates

1. Prove that `z_j<=Y` implies both numerator and denominator are at most
   `K_L Y`; hence there are at most `K_L^2Y^2` such labels.
2. After ordering `z_1<=...<=z_J`, prove

```text
z_j>=sqrt(j)/K_L,
sum_j 1/z_j<=2K_L sqrt(J).
```

3. Insert Cycle 100's
   `F_generic(j)<=2Q tau(|w_j|)/z_j` and prove

```text
sum_j F_generic(j)<=4K_L Q T_M sqrt(J)
                         <=8K_L Q T_M sqrt(M).
```

4. Record `T_M=M^o(1)` and the actual exponent
   `Q M^(1/2+o(1))`; at `Q=X^(1/3)`, `M<=X^(3/5+o(1))`, this is
   `X^(19/30+o(1))`.

## Falsifiers

- A distinct compact label family violating the quadratic height count halts
  the packing lemma.
- Reusing one rational label for two distinct strong `w` values halts the
  Cycle-99 insertion.
- No exceptional cross-valuation row may be charged to the generic sum.
