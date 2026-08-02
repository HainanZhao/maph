# Cycle 118 preregistration: derivative-resolved simple-root profiler

Date frozen: 2026-08-02 UTC.

## Frozen grid

- `D in {24,36,48}`, `Q=round(D^(5/9))`, `K=round(D^(16/15))`;
- `1<=B,C<=Q`, `-D<=a,b<=D`, excluding zero and equal-sign restrictions;
- choose the nearest positive integer `A` to `B exp(2pi a/D)+C exp(2pi b/D)`;
- retain rows with residual `<=1/K`;
- classify with Cycle 115's local thresholds and record `J0=A-B-C`,
  `J1=Ba+Cb`, signs, gcds, and derivative dyadic bin.

Use 80-decimal mpmath and record its version. This is discovery only. A
simple row without a dominant jet/mode signature falsifies the first
structure guess but does not kill the root-covering engine.
