# Cycle 106 discovery candidate: exact scale saturation is not a seed

`CONJECTURED` before proof sealing.

For a perfect-power core, Cycle 104 gives

```text
K=(d*R2/y)*(N/R)^(u/d).
```

Substituting `N=n0^d`, `R=r0^d`, and `R2=r0^d/x` should collapse this to

```text
K=d*n0^u*r0^v/(x*y),  v=d-u.
```

If `K=A0/S0` is reduced and the critical tolerance is below `1/S0`, the
surviving scales should be exactly the multiples of `S0`. Integer `K` is
therefore a genuine unsigned all-scale saturator.

This structure is still beta-free. Holding it fixed while changing the
original strip shift `beta` can turn one candidate row from an exact seed to
a definite miss. The correct E16 interface is therefore: inspect and verify a
retained payload, or use signed phase cancellation; powered-ray geometry by
itself cannot manufacture the Cycle-67 seed.
