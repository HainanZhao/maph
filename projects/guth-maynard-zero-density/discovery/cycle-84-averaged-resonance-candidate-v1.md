# Cycle 84 discovery candidate: averaged `(k,d)` resonance

## Status

`CONJECTURED`: discovery-only candidate.

## Candidate

For a dyadic block `k~K`, sum the Cycle-82 projector bound before taking a
maximum.  At central radius this asks for

```text
I(K)=#{(k,d): k~K,d~D, ||k c0 exp(2pi d/D)||<=1/Q}.
```

A Fejer majorant of bandwidth `Q` gives

```text
I(K)<<KD/Q+Q^(-1)sum_(j<=Q)|B_j|,
B_j=sum_(k~K,d~D)e(jk c0 exp(2pi d/D)).             (1)
```

Sum first in `k`.  Smooth Poisson projection localizes
`j c0 exp(2pi d/D)` to an integer at scale `1/K`.  This function is monotone,
has derivative `asymp j/D`, and crosses `O(j)` integers.  Each crossing
contains at most `1+D/(jK)` integer `d`, suggesting

```text
|B_j|<<D+jK.                                       (2)
```

For a projector annulus of radius `L/Q`, use Fejer bandwidth `Q/L`; (1)--(2)
then predict

```text
I_L(K)<<KD L/Q+D+KQ/L.                             (3)
```

After multiplying by the outer projector factor `Q` and fixed Schwartz
decay in `L`, the three Fourier-`L1` exponents are

```text
xi+3/5,  14/15,  xi+2/3.
```

The last dominates on the active range and closes strictly for
`xi<31/25-2/3=43/75`, adding width `2/25` beyond Cycle 83.

## Falsifiers

1. Smooth `k`-projection has a sign or normalization incompatible with (2).
2. The number of real integer crossings grows faster than `O(j)` on the
   frozen support.
3. Discretization near crossings costs more than one `d` per crossing plus
   total interval length.
4. The annular `L`-sum introduces a power loss.
5. A rational-anchor diagonal exceeds the explicit `KQ` crossing term.

