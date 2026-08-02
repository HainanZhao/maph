# Cycle 42 localized-comb preregistration v1

## Claim boundary

This cycle may retain the exact localized sampling comb from Cycle 41,
derive its Fourier factorization, and compare it with the full-annulus
relaxation. It may supersede `ASAM_s` as an allocation target if the exact
loss exceeds the closure margins. It may not promote the new row-aware
estimate, a kernel count, a density gain, or an interval gain.

## Registered tasks

1. Define the comb `omega_(B,C)(u)=sum_(t in C)|phi_B(t-u)|` for a fixed real
   even reproducing kernel.
2. Record its exact total mass, separated-set overlap bound, and leakage.
3. Expand `integral omega |F|^2` and retain both the coefficient collision
   and the row Fourier sum.
4. Quantify the loss from replacing the comb by `B 1_W` at maximal
   `Delta`-separated occupancy.
5. Compute the diagonal exponent of the localized vector form and compare it
   to the Cycle 39 target.

Hostile audit remains deferred to paper stage.
