# All-spin-structure Walsh marginals from the canonical TT

## Claim boundary

`PROVED`: Given the exact all-spin-structure TT from Cycle 7, all four
single-handle Walsh marginals at every handle, under arbitrary product-form
weights on the spin structures, can be evaluated with `O(g p d_w^2)` ring
operations, where `p=4` and `d_w=2^(w^2-1)`.  This is an operation on the
complete pre-Arf family, not an alternative way to evaluate only the final
physical partition function.

`CERTIFIED_NUMERICAL`: Exact reconstructions and marginal contractions for
`G_(6,3)` and `G_(7,3)` agree with explicit enumeration of all `4^g` sectors
over both `GF(1000000007)` and `GF(1000000009)`.

No thermodynamic-limit or critical-point consequence is claimed.

## The operation

Write one four-state physical index per canonical handle,

```
s_i=(lambda_(a_i),lambda_(b_i)) in F_2^2,
F(s_1,...,s_g)=ell^T A_1(s_1)...A_g(s_g)r,
```

and let `omega_i:F_2^2 -> R` be arbitrary product-form weights.  For every
handle `i` and Walsh character `c in F_2^2`, define

```
M_i(c)=sum_s (-1)^(c dot s_i) F(s_1,...,s_g)
       product_(j != i) omega_j(s_j).                         (1)
```

Thus the output contains `4g` linear statistics of the full sector tensor.
Taking `omega_j=1` gives the ordinary single-handle Walsh projections;
choosing other weights conditions or biases all other handles without
enumerating them.

## Exact algorithm and proof

Put

```
B_i=sum_(s in F_2^2) omega_i(s) A_i(s).
```

Compute left and right environments

```
L_0=ell^T,             L_(i+1)=L_i B_i,
R_g=r,                 R_i=B_i R_(i+1).
```

Then output

```
M_i(c)=sum_(s in F_2^2) (-1)^(c dot s) L_i A_i(s) R_(i+1).    (2)
```

`PROVED`: Expanding the matrix products in (2) selects one local state at
every site.  Sites other than `i` contribute exactly `omega_j(s_j)`, while
site `i` contributes the declared Walsh sign.  Each tuple `s` appears once,
so (2) equals (1) coefficientwise over the underlying ring.

For bond at most `d`, forming all `B_i`, both environment sweeps, and all
outputs uses `O(g p d^2)` dense ring operations.  Storing the cores costs
`O(g p d^2)` and the environments `O(gd)`.  In contrast, an explicit
sector-list method must inspect `p^g=4^g` values of `F` before applying the
same weights; if each value is obtained by a Pfaffian, its cost is
`O(4^g * Pfaffian-cost)`.  The comparison is specifically for the `4g`
all-family observables (1), not for computing one Arf-weighted partition
function, where ordinary transfer already has separator dependence.

## Exact validation

`proof/verify_lane_b_all_q_marginals.py` constructs the finite-field tensor
from the independently implemented character transfer, transports it to the
corrected canonical basis, computes an exact rank-factorization TT, evaluates
(2), and compares against the literal `4^g` sum (1).  The tested TT pair-rank
profiles are:

| graph | genus | sectors | exact pair ranks |
|---|---:|---:|---|
| `G_(6,3)` | 5 | 1024 | `4,16,16,4` |
| `G_(7,3)` | 6 | 4096 | `4,16,64,16,4` |

The table is reproduced over both declared primes.  The replay freezes the
edge-label hash, canonical coordinate transform, product-weight rule, and all
`4g` output residues.

