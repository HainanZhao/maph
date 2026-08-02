# Cycle 165 preregistration: typed seed-predicate factorization

Freeze three distinct schemas: `TransportRow63=(alpha,beta,h0,j0,L_pkt,q,a,...)`,
`UpperAtom87=(c0,d,q,a_(d,q),z_(d,q),...)`, and `WebLeaf164` with every wrap,
valuation, coefficient, tail, orientation, and phase label. Build a
provenance DAG only from sealed constructors, recording each exact formula,
branch condition, normalization, and retained/discarded field.

Test `TransportRow63 -> UpperAtom87 -> WebLeaf164` by an exact commutative
phase identity. If it composes, test whether the Cycle-67 seed predicate and
packet requirements are constant on actual source fibers. If beta remains
free, construct two admissible same-complete-label representatives with
opposite seed predicates. If no sealed path composes, issue a finite cut
certificate naming the first missing contract. This last outcome is scoped to
the sealed interfaces, not a field-wide no-ancestry theorem.

## Living amendment log

This remains the single preregistration for Cycle 165. Amendments below are
dated by the repository history and retain superseded choices inline; do not
create further Cycle-165 preregistration files.

### A. Direct-detector correction

The typed trace may show that Cycle 63 has no inherited Fourier atom. In that
case, use source points `(h,ell,w)`, `0<=w<=1`,
`x_(h,ell)=h alpha_ell (mod 1)`, with beta an external common anchor. Cycle
66 may only inform later analytic estimates; it cannot provide source
ancestry or beta retention.

Fejer is retained solely as a forward cross-check. The inverse-localization
kernel is the compact periodized bump

```text
psi_X(t)=sum_(k in Z) psi(X(t+k)),
```

where fixed nonnegative even `psi` equals one on `[-2C,2C]`, is supported in
`[-A,A]`, and `A>2C`. It has compact correlation support `2A/X` and Fourier
coefficient `X^(-1) psi_hat(n/X)`. Freeze `epsilon,J` with
`epsilon(2J-1)>4/5` by a fixed margin and
`|psi_hat(xi)|<=C_J(1+|xi|)^(-J)`; prove that truncating at
`|n|<=X^(1+epsilon)` costs `o(X^(7/25))`.

### B. Local cross-energy and grid protocol

Define `D_(X,ell)(beta)=sum_h w_(h,ell)psi_X(beta-x_(h,ell))` and
`E_cross=int D_X^2-sum_ell int D_(X,ell)^2`. Prove the exact positive
physical-space identity

```text
E_cross=2 sum_(ell<ell') int D_(X,ell)D_(X,ell') >=0.
```

With the integer lift `j` retained relative to the fixed beta strip (not
silently identified with `floor(h alpha_ell)` across the circular cut), a
Cycle-63 critical strip must force `E_cross >> X^(7/25+o(1))`; retain the
absolute beta label. Set
`M=floor(X/(16A))`, `w=1/M`, and use exactly four half-open circular grids
with shifts `0,w/4,w/2,3w/4`. Route each compactly supported pair to the
first grid in which it shares a cell; then select a grid by the fixed
pigeonhole rule. Every row has one home cell in each grid.

### C. Mass-sensitive graph gate

For the selected grid set

```text
nu_(I,ell)=sum_(rows in I,ell)w_r,
B_I=sum_ell nu_(I,ell),
Q_I=B_I^2-sum_ell nu_(I,ell)^2.
```

Compact energy `X^(7/25-o(1))` must yield cross-pair mass
`sum_I Q_I>=X^(32/25-o(1))`. Use a fixed dyadic partition of `B_I`, retain
the largest-`Q_I` level, and freeze `U=X^(1/50)`, `rho=1/10`. Split selected
cross-fibre pairs into heavy-involved and light-light terms, where
`(I,ell)` is heavy when its row multiplicity exceeds `U`.

- Heavy-involved mass at least `rho` is a labelled massed repeated-
  anchor-fibre bank, not a packet conclusion.
- Otherwise select lexicographically first `(h,j,source-row-id)` on every
  light occupied pair. Its support graph must satisfy
  `Q_light<=2U^2 W`, hence
  `W>=X^(31/25-o(1))` and `C4>=X^(32/25-o(1))`.

Every C4 retains its four original labels and exports two relations with the
same oriented anchor difference `delta_(I,I')`; degenerate/circle-lift cases
are quarantined. The advance condition is a proof-grade heavy bank or a
nondegenerate two-anchor C4 bank. Neither is a Cycle-67 packet without the
separate depth test.

### D. Four-anchor determinant compiler

For two curve labels sharing four distinct light home cells, use one cell as
base and form the three integer difference vectors `d`, `d'`, and `k` from
the retained `(h,j)` labels. The common anchors give

```text
d_i alpha_ell-d'_i alpha_ell'-k_i=O(X^-1),  i=2,3,4.
```

Since `H^2/X=X^(-3/25)`, dotting against `d cross d'` forces the exact
integer identity `det[d|-d'|k]=0` for sufficiently large `X`. The light graph
must supply `K_(4,2)>=X^(34/25-o(1))` by convexity from
`W>=X^(31/25-o(1))` over at most `Delta^2` label pairs.

Split the resulting bank without discarding multiplicity:

- if `d cross d'!=0`, use a fixed nonzero minor and Cramer's rule to retain a
  simultaneous rational-approximation plane for `(alpha_ell,alpha_ell')`;
- if `d cross d'=0`, reduce to the exact proportional-vector resonance
  `|r alpha_ell-s alpha_ell'-t|<<X^-1` with its four anchor labels.

Repeated planes or resonances are structured output. A dispersed bank with no
anchor-localized recurrence is the registered falsifier for this compiler.

For a rank-two Cramer target `A=N/D`, reduce by `g=gcd(N,D)` to `a/q`. The
registered packet calculation is

```text
|q alpha_ell-a| << H/(gX),
K=g/H,              qK=D/H<=H.
```

Thus `g>=X^(17/25-o(1))` yields a seeded Cycle-67 packet of depth at least
`X^(6/25-o(1))`; low-content planes remain a separately labelled structural
bank. This is a conditional compiler calculation, not yet a bound on the
number or mass of either branch.

### E. Beta-anchored fibre-product determinant compiler

The global compact-detector integral in B--D does **not** retain the original
Cycle-63 beta anchor: a high-energy four-anchor witness can occur at a
different beta. It is consequently an unseeded structural diagnostic only;
it must not be handed to Cycle 67. This correction does not alter the exact
detector identities, but supersedes D as a seeded-packet route.

For the direct anchored route, freeze one putative critical census at its
actual `(beta,C)` and set

```text
H_ell={h in [H,2H] : there is j with |j+beta-h alpha_ell|<=C/X},
t_ell=|H_ell|,        T=sum_ell t_ell.
```

The `j` label is retained with every member of `H_ell`. If
`T>=X^(16/25-o(1))`, then `t_ell<=H+O(1)` gives

```text
S=sum_(ell<ell') t_ell t_ell'
 = (T^2-sum t_ell^2)/2 >> X^(32/25-o(1)).
```

For each labelled pair `(ell,ell')`, an anchor is an ordered element
`(h,h') in H_ell x H_ell'`; write `P_(ell,ell')=t_ell t_ell'`. Convexity
over at most `Delta^2` labelled pairs must give the retained, multiplicity
labelled bank

```text
K=sum_(ell<ell') binom(P_(ell,ell'),4)
  >> S^4/Delta^6 >> X^(38/25-o(1)).
```

For each four distinct anchors of one label pair, take the first anchor as
base and form `d,d',k` exactly as in D, using the four original `h,j` pairs.
The common *fixed beta* now gives the three relations with error `O_C(X^-1)`.
Thus the determinant is exact for large X, and every high-content Cramer
branch contains its base original strip hit: it is eligible to call Cycle 67.

Choose the first nonzero minor `D` in a frozen lexicographic order. With
`N=k_i d'_j-k_jd'_i` and `N'=d_jk_i-d_ik_j`, freeze
`g=gcd(N,D)`, `g'=gcd(N',D)`, and reduce both rational targets. A safety
constant fixed before the calculation (using `C_*=max(1,C)`) defines high content as
`g>=c H X^(6/25)` (respectively `g'>=c H X^(6/25)`), so that integer packet
depth `K_pkt=floor(c' g/H)` (respectively `K'_pkt`) satisfies both the
Cycle-67 approximation inequality and `qK_pkt<=H`. Constants, the enlarged
strip, and the sufficiently-large-X cutoff must be explicit in the proof
artifact.

Assign every labelled four-anchor witness, without deduplication, to exactly
one terminal bank in this order:

1. rank one (`d cross d'=0`), including zero-coordinate cases, with its
   exact proportional resonance retained;
2. rank two and high `g`, giving a seeded packet for `ell`;
3. rank two, low `g`, and high `g'`, giving a seeded packet for `ell'`;
4. rank two with both contents low, retaining its labelled rational plane.

The four classes are exhaustive and disjoint, so one retains at least a
quarter of the labelled `K` mass. Repeated packets, planes, resonances, and
anchors remain counted with their original labels. This is an inverse
classification only; it asserts neither a bound on the terminal banks nor a
density or interval gain.
