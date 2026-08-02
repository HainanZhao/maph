# Cycle 111 correction: the anchor is in the stationary value, not the point

## Correct derivation

`PROVED`. The crossed Cycle-81 columns contribute, in the `k` variable,

```text
Phi_k(k)=c*Delta*log(k*c0)-m*k,       c=D/(2pi).
```

Since `log(k*c0)=log k+log c0`, the anchor term is constant under
`k`-differentiation. Therefore

```text
Phi_k'(k)=c*Delta/k-m,
k*=c*Delta/m,
Phi_k''(k*)=-m^2/(c*Delta).                       (1)
```

The stationary value is nevertheless

```text
Phi_k(k*)=c*Delta[log(c*c0*Delta/m)-1],            (2)
```

exactly the value used in Cycle 94. Thus the combined entropy phase and its
central relation `m=c0(n-n')` remain unchanged.

## Versioned correction and affected scope

The sealed Cycle-108 display

```text
k*=c*c0*Delta/m
```

is incorrect and is superseded by (1). The Cycle-108 Hessian amplitude
`sqrt(c*Delta)/m`, its product Jacobian, and the `ell^(-3/2)` scale law are
unchanged. The corrected point is still invariant under simultaneous scale
dilation, so Cycle 107's homogeneity is also unchanged. Cycle 109 already
uses the corrected curvature and stationary point, and Cycle 110 uses only
the unchanged coefficient Jacobian product.

Any cutoff value or mixed-symbol norm inherited specifically from the old
Cycle-108 location is not licensed and must be rederived from (1). This is
now the first task of the exact normalization ledger.

## Claim boundary

This is a location-only correction with a contained cutoff-interface audit.
It does not yet prove a uniform outer-prefactor or anchor envelope, a complete
moment, a density gain, or an interval gain.
