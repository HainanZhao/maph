# Cycle 143: sparse-path layering is norm-self-dual

Fix an exceptional difference `d`, put

```text
kappa_d=NS(r_d-g^d),       L=S/N,                 (1)
```

and decompose its edge graph into the `O(log N)` paths from Cycle 142.
Layer those paths by position.  Every layer is a set of distinct height-`N`
rational labels, separated by `>>N^(-2)`.

For arbitrary complex weights, the separated-label large sieve on a layer
gives

```text
sum_(|ell|<=L)|sum_(a in layer)
  w_a e(ell kappa_d x_a)|^2
 <<(L+N^2/|kappa_d|) sum_(a in layer)|w_a|^2.      (2)
```

Cauchy across `Lambda=O(log N)` layers yields

```text
M2 << Lambda (L+N^2/|kappa_d|) sum_a|w_a|^2.      (3)
```

Since `Lambda=X^(o(1))`, (3) has exactly the Cycle-136 power threshold

```text
|kappa_d| >> N^2/L=N^3/S.                         (4)
```

Thus path decomposition neither loses nor gains a fixed power.  It is
norm-self-dual within the arbitrary-weight architecture.

This scope is sharp.  If `L|kappa_d|` is sufficiently small and all weights
have one sign, the phases remain coherent and

```text
M2 asy L |E_d|^2.                                 (5)
```

The actual operator is signed, so (5) is not a saturator for its full
coefficient vector.  In the exceptional window, expand

```text
sum_a w_a e(ell kappa_d x_a)
 =sum_(m>=0) (2pi i ell kappa_d)^m/m!
             M_m(d),
M_m(d)=sum_a w_a x_a^m.                           (6)
```

The first missing lock is `M_0(d)=sum_a w_a`, followed by the higher signed
moments.  Any strict improvement must use this actual coefficient hierarchy
or an equivalent cross-component invariant; path geometry and arbitrary
weights alone cannot provide it.

No bound for the actual signed moments, paired norm, endpoint, complete
moment, density, or prime-interval theorem is proved.
