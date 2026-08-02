# Cycle 21 v2 correction: weighted prime continuum frame

## Correction and affected claims

`OBSERVED` correction: v1 chose uniform measure in
`y=log(p/X)`. Its continuous-frame theorem and its explicitly conditional
perturbation implication remain mathematically valid, but that measure is not
the natural prime limit and so v1 is superseded as the strategic quadrature
gate.

`PROVED`: under the prime number theorem scaling `p=Xe^y`, normalized prime
mass has the reference density

```text
dnu(y)=e^y dy,    0<=y<=log 2,
```

whose total mass is one.

## Corrected continuum theorem

The normalized weighted kernel is

```text
H_nu(h)=integral_0^(log 2)e^(1-ih)y dy
       =(2^(1-ih)-1)/(1-ih).
```

For nonzero `h`, its magnitude is at most `3/|h|`. Hence for ordered,
`Delta`-separated rows,

```text
epsilon_nu<=6H_(k-1)/Delta,
det(H_nu)>=(1-epsilon_nu)^k.
```

If the normalized prime Gram matrix satisfies

```text
eta_C=||H_P-H_nu||_op,
```

then `det(H_P)>=(1-epsilon_nu-eta_C)^k` whenever the bracket is positive.

## Corrected critical gate

After coloring by `ceil((log X)^2)`, the continuum row-sum error remains

```text
epsilon_nu=O(X^(-3/5)/log X)=o(X^(-3/5)).
```

Therefore the corrected sufficient prime input is still

```text
eta_C=o(X^(-3/5)).
```

It would contradict the Cycle-20 determinant collapse at scale
`X^(6/25-o(1))`. The exponent target is unchanged; only the reference
measure and kernel constant are corrected. The prime discrepancy itself
remains `CONJECTURED` and open.
