# Cycle 145 preregistration: vector-valued autocorrelation compiler

Date frozen: 2026-08-02 UTC.

For a fixed arithmetic edge class, retain the complete coefficient function
`ell -> C_e(ell)` from Cycle 144.  Regard these functions as vectors in the
finite `ell^2` space instead of replacing them by scalar weights.

Derive the componentwise Taylor expansion of

```text
F(ell)=sum_e C_e(ell)e(ell kappa x_e)
```

and an explicit norm remainder in terms of the vector moments
`M_m(ell)=sum_e C_e(ell)x_e^m`.  Freeze every frequency multiplier `ell^m`;
it may not be hidden in an unweighted moment norm.

Then identify `M_0(d;ell)` for a complete fixed-mode-difference class as the
coefficient autocorrelation.  Record its positive-definite Fourier identity,
and isolate exactly how the arithmetic collision-selection mask destroys or
preserves that identity.  Test fixed-phase local charts as an adverse model,
but do not call them saturators unless the full weighted inverse selects them.

Success is an exact vector-valued moment compiler and a precise next target
for the selected autocorrelation.  No cancellation estimate, paired norm,
complete moment, density gain, or prime-interval consequence is implied.
