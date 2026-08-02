# Cycle 36: first-harmonic entropy is the determinant collapse

## Claim boundary

`PROVED`: the minimum phase entropy compatible with a given first Fourier
coefficient has the same leading constant and exponent as the sharp
common-projection determinant collapse. Its small-excess branch reproduces
the `X^(2/5)` second-harmonic/popular-kernel scale already present in Cycle
19. Thus raw first-harmonic entropy is not an independent saving mechanism;
only entropy excess above the information projection can add arithmetic
content.

`OBSERVED`: no upper or lower bound for that excess on actual prime rows is
proved. No prime-kernel count, zero-density gain, or interval improvement is
claimed.

## 1. Exact information projection

Let `u` be uniform measure on the circle. After rotation, prescribe the first
moment `int cos(theta)dmu=r` and `int sin(theta)dmu=0`. The entropy-minimizing
measure is the von Mises projection

```text
dnu_r/du=exp(kappa cos(theta))/I_0(kappa),
I_1(kappa)/I_0(kappa)=r.                               (1)
```

For a finite equal-arc histogram, the identical statement holds with the
finite exponential family and partition function replacing the Bessel
functions. If `qstar` is that projection and `q` has the same first moment,
then

```text
log(qstar_j/u_j)=kappa c_j-log Z.
```

The constraint makes the affine term have the same expectation under `q`
and `qstar`, giving the exact Pythagorean identity

```text
D(q||u)=D(qstar||u)+D(q||qstar).                       (2)
```

Write

```text
J(r)=D(qstar||u),             E(q)=D(q||qstar)>=0.      (3)
```

The first term is completely determined by the already known kernel value;
`E(q)` is the new higher-harmonic statistic.

## 2. Leading constant

The exact Bessel series give

```text
I_1(kappa)/I_0(kappa)
 =kappa/2-kappa^3/16+kappa^5/96+O(kappa^7),
kappa(r)=2r+r^3+(5/6)r^5+O(r^7),
J(r)=kappa(r)r-log I_0(kappa(r))
    =r^2+r^4/4+(5/36)r^6+O(r^8).                      (4)
```

Put `r^2=rho=X^(-3/5)` and `k=X^(21/25)`. Then

```text
kJ(sqrt(rho))=k rho+o(1)=X^(6/25+o(1)),                (5)
```

because `k rho^2=X^(-9/25)`.

The sharp equal-projection Gram determinant upper bound from Cycle 20 is

```text
det_max=k rho [k(1-rho)/(k-1)]^(k-1).
```

Since `rho->0`, `k rho->infinity`, and `k rho^2->0`,

```text
-log det_max
 =-log(k rho)-(k-1)log(1-rho)
   -(k-1)log(k/(k-1))
 =k rho-log(k rho)-1+o(k rho)
 =(1+o(1))k rho.                                      (6)
```

`PROVED`: (5) and (6) agree not only at exponent `6/25` but at leading
constant one. The Cycle 35 match is therefore an equivalence at first
harmonic, not a second source of saving.

## 3. The excess dichotomy

Pinsker applied to (3) gives

```text
||q-qstar||_1<=sqrt(2E(q)).                            (7)
```

Thus small excess rigidly places the phase histogram near its von Mises
model. To preserve a second harmonic of order `r^2`, the quantitative
condition is `E(q)=o(r^4)`, which makes the right side of (7) `o(r^2)`.
The model has

```text
int exp(2i theta)dnu_r=I_2(kappa(r))/I_0(kappa(r))
                      =r^2/2+O(r^4).                  (8)
```

At the prime scale, multiplying by `M=X^(1+o(1))` makes (8) an unnormalized
second-harmonic kernel of size

```text
M r^2=X^(2/5+o(1)),                                   (9)
```

exactly the popular-edge correlation scale forced in Cycle 19. Therefore
the minimum-entropy branch loops back to the already sharp synchronization
graph rather than producing the missing `4/25`.

The only genuinely new E7 statistic is

```text
E_total(C)=sum_(t in C)E(q_t).                         (10)
```

There are now two valid research branches:

1. **excess at least comparable to `r^4`:** convert (10), or a scale
   decomposition of it, into higher Fourier mass and then into a multiscale
   prime-kernel or detector-surgery estimate;
2. **quadratically tiny excess `o(r^4)`:** use quantitative von Mises
   rigidity jointly across separated rows, not merely the single-row second
   harmonic in (8).

No universal Hilbert-space argument can distinguish these branches; the
next lemma must use the common actual prime phases across rows.

## Gate effect

`PROVED` scoped saturation: first-harmonic information projection plus the
sharp common-component determinant contains no power saving beyond Cycles
19--23. E7 remains alive only through excess entropy or joint von Mises
rigidity. E9's sifted-curvature route remains independent.
