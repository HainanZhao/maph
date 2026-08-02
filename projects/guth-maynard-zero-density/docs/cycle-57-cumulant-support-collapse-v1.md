# Cycle 57: the edge cumulant survives support collapse at constant cost

## Claim boundary

`PROVED`: the Cycle-56 coordinate-centred tensor is a Hilbert-valued
Dirichlet polynomial on the actual integer labels `q^m p_1...p_s`. After
collapsing equal labels, its coefficient square norm increases by at most

```text
D_s=(1+floor(s/2))s!,
```

uniformly for every `m>=2`. Thus support collapse loses no power of `M` or
`X`; `D_3=12` and `D_4=72`.

This proves a coefficient-norm bridge, not a restriction estimate. It does
not supply `3/50`, prove `AMPR_s`, or improve density or prime intervals.

## Hilbert-valued frequency representation

Let `P=I-J/M` project the prime-coordinate space off its constant vector.
For an ordered tuple `tau=(q,p_1,...,p_s)`, set

```text
c_tau=(P e_q) tensor (P e_p1) tensor ... tensor (P e_ps),
n_tau=q^m p_1...p_s.
```

Then the raw coordinate-centred tensor equals

```text
sum_tau n_tau^(-ih)c_tau.
```

Grouping equal integer frequencies gives fixed Hilbert coefficients

```text
a_n=sum_(tau:n_tau=n)c_tau.
```

This resolves the apparent dependence of `p^(-ih)-k(h)` on `h`: the
dependence is entirely in `n^(-ih)`, while `P e_p` is a fixed vector
coefficient.

## Exact norm ledger

Every projected basis vector has

```text
||P e_p||^2=1-1/M.
```

There are `M^(s+1)` ordered tuples, hence before collapse

```text
sum_tau||c_tau||^2=(M-1)^(s+1).
```

Cycle 39 proves that every fiber of `tau -> n_tau` has size at most `D_s`,
uniformly in `m>=2`. Cauchy--Schwarz on each fiber gives

```text
||a_n||^2 <= |fiber(n)| sum_(tau in fiber(n))||c_tau||^2.
```

Summing over `n` yields

```text
sum_n||a_n||^2 <= D_s(M-1)^(s+1)=M^(s+1+o(1)).
```

With Cycle-56's normalized prime measure, divide by `M^(s+1)`; the energy is
at most `D_s(1-1/M)^(s+1)`. The exponent cost remains zero.

## Strategic consequence

The ordered-coordinate caveat in Cycle 56 is closed at coefficient-energy
level. E12 can now be stated directly as a Hilbert-valued sparse restriction
problem on the same prime-monomial support as `AMPR_s`, without paying an
ambient support length or a collision power.

`CONJECTURED` next dichotomy: on the popular-edge set after three ordinary
contractions, either the Hilbert-valued cumulant restriction estimate saves
`3/50`, or its failure forces simultaneous approximate multiplicativity of
`k` at scales `1,m`, which enters Cycle 52/E13.

## Gate effect

E12 advances to `HILBERT_EDGE_CUMULANT_RESTRICTION_3_50_OPEN`.
