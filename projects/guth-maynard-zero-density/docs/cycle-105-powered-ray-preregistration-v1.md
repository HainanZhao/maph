# Cycle 105 preregistration: perfect-power ray compiler

Date frozen: 2026-08-02 UTC.

## Boundary

This cycle compiles Cycle-104 rational aliases into powered rational rays. It
may prove an exact base-ray representation, root-error transfer, and height
packing. It does not assert that sparse exponents form a full progression or
that a powered ray is already a realized original packet seed.

## Frozen gates

1. From `N=n0^d`, `R=r0^d`, `w=h*d`, prove
   `N/R=(n0/r0)^d` with reduced base and exact mode/base anchor `h`.
2. From `|(n0/r0)^d-exp(h*d*x)|<=delta`, prove the mean-value root bound
   `|n0/r0-exp(h*x)|<=delta/(d*min(n0/r0,exp(h*x))^(d-1))`.
3. Under `|h*d*x|<=L` and `delta<=exp(-L)/2`, derive a frozen lower envelope
   for the denominator in gate 2.
4. Prove that a nonunit base of height `Z` has at most
   `floor(log(H)/log(Z))` admissible positive powers under height `H`, also
   respecting `d<=2M/|h|`.
5. A repeated `(h,n0/r0)` must output its exact exponent set, arithmetic mode
   multiples, geometric labels, and unchanged stationary/anchor payloads.
   Do not fill missing exponents.
6. Singleton bases remain a packing branch. No hostile audit is authorized.

## Replay

```sh
python3 proof/build_cycle_105_powered_ray_compiler_v1.py --check
python3 -m unittest tests/test_cycle_105_powered_ray_compiler_v1.py
```
