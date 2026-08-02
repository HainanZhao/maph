# Cycle 57 preregistration: Hilbert-valued support collapse

## Question

Push the Cycle-56 coordinate-centred tensor through the integer-frequency map
`(q,p_1,...,p_s) -> q^m p_1...p_s`. Determine whether collisions increase
the Hilbert-valued coefficient square norm by only a fixed `s`-dependent
factor, uniformly for every `m>=2`.

## Frozen conventions

- `P=I-J/M` is the orthogonal projection off the constant prime vector.
- A tuple `tau=(q,p_1,...,p_s)` has coefficient vector
  `c_tau=(P e_q) tensor (P e_p1) tensor ... tensor (P e_ps)`.
- Its frequency label is `n_tau=q^m p_1...p_s`.
- The collapsed coefficient is `a_n=sum_(tau:n_tau=n)c_tau`.
- Use the Cycle-39 fiber bound
  `D_s=(1+floor(s/2))s!`, uniformly for `m>=2`.
- Evaluate `s=3,4`; record raw and normalized coefficient energies.

## Outcomes

- `CONSTANT_COST`: `sum_n ||a_n||^2 <= D_s sum_tau||c_tau||^2`, so
  support collapse loses no power of `M` or `X`.
- `POWER_LOSS`: the frozen fiber estimate is insufficient for the
  Hilbert-valued coefficients.

No large-value estimate, `3/50` saving, `AMPR_s`, density gain, or interval
gain follows from the first outcome.
