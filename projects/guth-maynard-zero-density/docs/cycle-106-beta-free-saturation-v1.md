# Cycle 106: beta-free powered-ray saturation boundary

## Exact rational scale orbit

`PROVED`. In the Cycle-104 rational class, write

```text
N=n0^d, R=r0^d, d=u+v,
R=x*R2, N=y*N2.
```

The single-radical formula simplifies completely:

```text
K=(d*R2/y)*(N/R)^(u/d)
 =d*n0^u*r0^v/(x*y)=A0/S0,                        (1)
```

where `A0/S0` is reduced. The equality uses `R2=r0^d/x` and `v=d-u`.

## Tight critical-value hits

`PROVED`. Suppose `0<=epsilon<1/S0`. For an integer scale `lambda`, the
distance from `lambda*K` to the integers is either zero or at least `1/S0`.
Consequently

```text
|A-lambda*K|<=epsilon for some integer A
 iff S0 divides lambda.                            (2)
```

The hit set is therefore exactly

```text
S0,2S0,...,floor(Lambda/S0)S0,                    (3)
```

with cardinality `floor(Lambda/S0)`. All coefficient scales survive iff
`S0=1`. This is sharp: the nontrivial cross core

```text
(u,v,d,x,y,n0,r0)=(2,1,3,2,1,3,2)
```

has reduced label `27/8` and `K=27`, so every scale is an exact
critical-value hit.

## Why this is not yet a packet seed

`PROVED`, scoped non-implication. The powered-ray datum is beta-free, while a
Cycle-67 seed is an original row satisfying

```text
|j0+beta-h0*alpha|<=C0/X.                          (4)
```

Hold `alpha,h0,j0` and every powered-ray coordinate fixed. The choice

```text
beta_seed=h0*alpha-j0
```

makes (4) exact. Replacing it by `beta_seed+1/2` gives residual `1/2`, which
misses whenever `C0/X<1/2`. Thus no compiler inspecting only beta-free
powered-ray data can certify a genuine seed.

This is not a no-go for payload-aware E16: if a retained stationary payload
itself verifies (4), Cycle 67 applies and propagates the seed. The missing
lock is precisely beta/payload coupling. Signed cancellation among the exact
scale progression (3) is also still available.

## Boundary

The theorem proves a sharp unsigned all-scale saturator and a scoped seed
non-implication. It does not close payload-aware realization, signed phase
cancellation, singleton/large-degree aggregation, weak/simple-root rows, the
complete moment, density, or interval targets.
