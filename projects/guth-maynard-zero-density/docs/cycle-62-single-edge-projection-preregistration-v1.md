# Cycle 62 preregistration: single-edge projection stress test

## Question

Determine whether the Cycle-61 full coordinate projection can give a
fixed-power saving pointwise on one Fourier edge, and isolate the additional
structure available for genuine phase-aligned edge weights.

## Frozen setup

- For one edge `h`, take the label vector `beta_n=n^(-ih)`.
- Its ordered lift is the pure tensor
  `q^(-imh) product_j p_j^(-ih)`.
- Normalize the raw tensor to squared norm one.
- The full-centered projection uses `P=I-J/M` in every coordinate.
- Compare with the genuine phase-aligned vector
  `beta_n=sum_(t,u)z_t conj(z_u)n^(-i(t-u))`.

## Outcomes

- `POINTWISE_SAVING`: the centered single-edge norm is smaller by a fixed
  power whenever normalized prime kernels are polynomially small.
- `SINGLE_EDGE_SATURATES`: the retained fraction is exactly
  `(1-|k(mh)|^2)(1-|k(h)|^2)^s=1-o(1)` in that regime. Any saving theorem
  must use the multi-edge convolution identity `beta_n=|sum_t z_t n^(-it)|^2`.

The second outcome does not refute a theorem restricted to large
phase-aligned row sets or nonnegative convolution vectors.
