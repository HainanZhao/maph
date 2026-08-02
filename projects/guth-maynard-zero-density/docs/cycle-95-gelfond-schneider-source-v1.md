# Cycle 95 source ledger: Gelfond--Schneider

## Checked theorem

Karatarakis--Wiedijk, *A formalization of the Gelfond--Schneider theorem*,
arXiv:2603.24823, Theorem 1 (displayed in Section 3; formal theorem at lines
290--297 of the rendered source): if algebraic `alpha,beta` satisfy
`alpha!=0,1` and `beta` is irrational, every chosen value of `alpha^beta` is
transcendental.

Primary/formalized source:
<https://arxiv.org/abs/2603.24823>

## Registered specialization

Take `alpha=-1` and `beta=-2i/D`, with positive integer `D`. Both are
algebraic, `alpha!=0,1`, and `beta` is nonrational. Using the logarithm value
`Log(-1)=i*pi`, one value is

```text
(-1)^(-2i/D)=exp((-2i/D)(i*pi))=exp(2pi/D).
```

Hence `g_D=exp(2pi/D)` is transcendental. This is qualitative only; the
source supplies no lower bound for a nonzero integer polynomial evaluated at
`g_D` uniform in growing `D`.

