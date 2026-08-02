# Cycle 165: beta-anchored fibre-product determinant inverse

## Claim boundary

`PROVED`: conditional on a fixed-beta Cycle-63 strip census of size
`T`, the labelled fibre products contain a four-anchor determinant bank.  At
the critical size `T>=X^(16/25-o(1))`, its multiplicity is
`>>X^(38/25-o(1))`. Every witness is routed, without deduplication, into a
rank-one resonance, a seeded high-content packet for one of its two labels,
or a labelled rank-two low-content rational plane.

This is an inverse classification for a putative critical census. It does not
bound the census or any terminal bank, and proves no transport, density, or
prime-interval gain.

## Anchored count

Fix `beta`, a positive strip constant `C`, write `C_*=max(1,C)`, and retain
the same strip rows after this harmless enlargement. Their integer labels are

```text
H_ell={h in [H,2H] : |j(h,ell)+beta-h alpha_ell|<=C/X},
t_ell=|H_ell|,  T=sum_ell t_ell.
```

For `X>2C`, the integer label is unique. Let `H0` be the integer diameter of
the h-range, so `t_ell<=H0+1`. The number of ordered two-label anchors is

```text
S=sum_(ell<ell') t_ell t_ell'
 =(T^2-sum_ell t_ell^2)/2 >=(T^2-(H0+1)T)/2.        (1)
```

For a label pair put `P_(ell,ell')=t_ell t_ell'`. There are at most
`binom(Delta,2)` nonzero label pairs. Discrete convexity gives the exact
minimum of `sum binom(P,4)` by balancing the integral `P` values. Thus, as
soon as `S/binom(Delta,2)` tends to infinity,

```text
K4=sum_(ell<ell') binom(P_(ell,ell'),4)
   >> S^4/Delta^6.                                  (2)
```

At `H=X^(11/25+o(1))`, `Delta=X^(15/25+o(1))`, and
`T>=X^(16/25-o(1))`, (1) gives `S>>X^(32/25-o(1))`; hence (2) gives
`K4>>X^(38/25-o(1))`. Every counted anchor retains `(beta,ell,h,j)`.

## Exact determinant

Choose four distinct ordered anchors for a fixed pair `(ell,ell')`, use the
first as base, and for `i=2,3,4` put

```text
d_i =h_i-h_1,       d'_i=h'_i-h'_1,
k_i =(j_i-j_1)-(j'_i-j'_1).
```

Subtracting the two strip equations at the fixed beta gives

```text
|d_i alpha_ell-d'_i alpha_ell'-k_i| <= 4C/X.        (3)
```

The components of `d cross d'` have magnitude at most `2H0^2`. Therefore

```text
| (d cross d') dot k | <= 24 C_* H0^2/X.            (4)
```

The left side of (4) is integral. Under the explicit cutoff
`24 C_* H0^2<X`, it is zero, equivalently

```text
det[d|-d'|k]=0.                                      (5)
```

## Rank/content routing

If `d cross d'=0`, write `d=r v`, `d'=s v` with `v` primitive (using a
nonzero vector among `d,d'`). Applying the same integer forcing to the minor
with `k` gives `k=t v` for an integer `t`, and (3) yields the labelled
resonance

```text
|r alpha_ell-s alpha_ell'-t| <=4C_*/X.               (6)
```

This includes `r=0` or `s=0`; it is structural output, not a packet.

Otherwise choose the first nonzero minor in the order `(1,2),(1,3),(2,3)`:

```text
D=d_i d'_j-d_j d'_i,
N=k_i d'_j-k_j d'_i,       N'=d_j k_i-d_i k_j.
```

From (3), both `|D alpha_ell-N|` and `|D alpha_ell'-N'|` are at most
`8 C_* H0/X`. Reduce the two fractions separately, with
`g=gcd(N,D)`, `g'=gcd(N',D)`, and denominators `q=|D|/g`, `q'=|D|/g'`.
The corresponding signed reduced numerators are
`a=sign(D)N/g`, `a'=sign(D)N'/g'`.
For the first label, set

```text
K_pkt=floor(g/(16 C_* H0)).                          (7)
```

Then `|q alpha_ell-a|<=1/(K_pkt X)` and `q K_pkt<=H0` whenever
`K_pkt>=1`; the same statement holds for the primed data. In particular, if
`g>=32 C_* H0 L`, then `K_pkt>=L`, and analogously for `g'`. Taking
`L=ceil(X^(6/25))` supplies the exact Cycle-67 depth interface. The base
anchor is already a genuine fixed-beta strip seed, so—and only so—the
corresponding high-content branch may invoke Cycle 67.

Partition each labelled four-anchor witness in priority order into rank one;
rank two with `g>=32 C_* H0 L`; rank two with low `g` and
`g'>=32 C_* H0 L`; or rank two with both contents low. The partition is
disjoint and exhaustive. Consequently one bank contains at least a quarter
of the labelled `K4` witnesses, with all original labels and multiplicities
preserved.

## Contained detector route

The compact detector's global beta integral remains an exact, useful
unseeded diagnostic. Its selected four-anchor witness need not occur at the
original beta, so it must not be used as a Cycle-67 seed compiler.
