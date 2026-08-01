# Cycle 10 E1 frame detector and E2 two-step centring v1

## Claim boundary

`PROVED`: a weighted detector dictionary has an exact PSD mixed-kernel trace
inequality, with its full colour loss visible. Pure colouring by a subpower
number of otherwise unrelated scalar detectors produces no fixed-power gain
over pigeonholing.

`PROVED`: for a Hermitian Gram matrix with constant diagonal, deleting exact
two-step returns gives an identity and spectral alternative. At the frozen
CRR Base scale, a large sampled eigenvalue forces either one large local
return row or a large coherent off-diagonal two-step operator.

`PROVED`: the raw length-four nonbacktracking trace is not nonnegative for
general real symmetric weights. The preregistered search found an order-four
integer countermodel with value `-128`.

This note proves no saving for either term in the two-step alternative, no
new large-value or zero-density estimate, no shorter prime interval, no
Base/CRR incompatibility, and no L-function extension. It corrects the
research objects E1 and E2; it does not terminate their parent mechanisms.

## 1. Source overlap and the corrected novelty boundary

The pinned Guth--Maynard source has SHA-256
`36d64e4ec02f0cee8baccd6ee1dbf5ea73f0dfde55827e00ad2566a142ffa428`.

`PROVED` by direct inspection of TeX lines 2309--2330: the classical detector
already uses `O(log T)` dyadic lengths, chooses a length carrying the largest
Type-I subfamily, removes the real-part dependence by Fourier translation,
and arrives at one coefficient vector on one separated set. Treating those
dyadic lengths as colours instead changes only logarithmic factors.

`PROVED` by direct inspection of TeX lines 497--587: the source already uses
the Gram matrix `M_W M_W^*`, arbitrary trace powers as a benchmark, and the
centred cubic spectral statistic

```text
tr(G^3)-tr(G)^3/m^2.
```

Consequently E1 must exploit structure among detectors beyond their number,
and E2 must delete row-local or alias returns beyond scalar centring.

## 2. `PROVED`: the E1 frame trace lemma

Let `M` be an `m x n` complex matrix, let `b^(1),...,b^(K)` be vectors in
`C^n`, and let `omega_j>0` with `sum_j omega_j=1`. Put

```text
B=sum_j omega_j b^(j)b^(j)*,
K_B=M B M*,
q_t=(K_B)_(t,t)=sum_j omega_j |(M b^(j))_t|^2.
```

Then `B` and `K_B` are positive semidefinite. For every integer `r>=1` and
every row set `S` on which `q_t>=V^2`,

```text
|S| V^(2r) <= sum_t q_t^r <= tr(K_B^r).                 (1)
```

To prove the second inequality, write the spectral decomposition
`K_B=U diag(lambda_a) U*`. For each row `t`, Jensen's inequality gives

```text
q_t^r=(sum_a |U_(t,a)|^2 lambda_a)^r
     <=sum_a |U_(t,a)|^2 lambda_a^r.
```

Summing over `t` gives `sum_t q_t^r<=sum_a lambda_a^r=tr(K_B^r)`. The first
inequality in (1) is the pointwise threshold summed over `S`.

If every `t in S` merely has one colour `j(t)` satisfying
`|(M b^(j(t)))_t|>=V`, uniform weights give only `q_t>=V^2/K`. Hence (1)
becomes

```text
|S| V^(2r) <= K^r tr(K_B^r).                            (2)
```

The complete colour cost is therefore `K^r`. It is subpower when both `K`
and the useful moment order are bounded or sublogarithmic in the appropriate
sense, but (2) contains no saving by itself.

### Pure-colouring barrier

`PROVED`: suppose the only information is a partition
`S=S_1 union ... union S_K`, with one unrelated scalar detector large on each
`S_j`, and suppose the available scalar theorem gives `|S_j|<=F` uniformly.
Then summation gives `|S|<=K F`, while the largest-colour argument gives the
same inequality. If `K=T^o(1)`, this changes no power exponent. The model with
all detectors equal shows that no universal improvement follows from the
dictionary cardinality alone.

Thus the E1 input still missing is precise: a zero-detection construction
must provide frame geometry that makes the mixed trace in (2) smaller than
the sum of unrelated scalar traces by more than its explicit colour loss.
This may come from disjoint prime blocks, low coherence, or a factorization
identity, but none is proved here.

## 3. `PROVED`: exact E2 return deletion

Let `G` be an `m x m` Hermitian matrix with constant diagonal `d`. Write

```text
A=G-dI,
r_i=sum_(j != i)|A_(i,j)|^2,
R=diag(r_1,...,r_m),
C_2=A^2-R.
```

Since `A` is Hermitian and has zero diagonal,
`(A^2)_(i,i)=r_i`, so `C_2` has zero diagonal. Moreover,

```text
||C_2||_F^2
 =sum_(i != k)|(A^2)_(i,k)|^2
 =||A^2||_F^2-sum_i r_i^2
 =tr(A^4)-sum_i r_i^2.                                  (3)
```

This is the desired exact deletion of two-step returns. It is stronger
local information than subtracting only a scalar spectral mean.

For the spectral consequence, `A^2=R+C_2` and therefore

```text
||A||_op^2=||A^2||_op
 <=max_i r_i+||C_2||_op
 <=max_i r_i+||C_2||_F.
```

Since `lambda_max(G)<=d+||A||_op`,

```text
lambda_max(G)
 <=d+sqrt(max_i r_i+||C_2||_op)
 <=d+sqrt(max_i r_i+||C_2||_F).                         (4)
```

Equation (4), rather than a raw nonbacktracking trace, is the first one-sided
E2 engine.

## 4. `PROVED`: the raw `NB4` sign obstruction

Expanding `tr(A^4)` as closed length-four walks and excluding immediate
returns by inclusion--exclusion gives

```text
NB4(A)=tr(A^4)-2 sum_i r_i^2+sum_(i != j)|A_(i,j)|^4.   (5)
```

The two subtracted events are `i_2=i_0` and `i_3=i_1`; their intersection is
the oriented edge traversed four times, giving the last term. Although (5)
is real for Hermitian `A`, it need not be nonnegative.

The preregistered lexicographic exact search checked all `125` order-three
matrices first and then stopped at the fifth order-four matrix. It found

```text
A = [[ 0,-2,-2,-2],
     [-2, 0,-2,-2],
     [-2,-2, 0, 2],
     [-2,-2, 2, 0]],
NB4(A)=-128.
```

Thus raw `NB4` cannot replace the positive trace statistic in a universal
one-sided spectral argument. This contains only that formulation. The
positive square `||C_2||_F^2` in (3), even dilations, and alias-conditional
centring remain live E2 designs.

## 5. `PROVED`: critical Base translation

For the frozen actual Dirichlet sampling matrix, the diagonal of `G=M_WM_W*`
is `d=sum_n w(n/L)^2<=L+1=v^(10+o(1))`. The sealed phase-lattice Base bridge
shows that Base compatibility requires

```text
lambda_max(G)>=v^(12-3 delta(v)).                       (6)
```

For all sufficiently large `v`, (6) and `d<=v^(10+o(1))` imply

```text
||A||_op>=lambda_max(G)-d
          >=(1/2)v^(12-3 delta(v)).
```

Combining with (4) gives the necessary alternative

```text
max_i r_i >= (1/8)v^(24-6 delta(v))                    (7a)
or
||C_2||_op >= (1/8)v^(24-6 delta(v)).                  (7b)
```

The constant `1/8` follows because the sum in (4) is at least
`(1/4)v^(24-6delta)` and one of its two nonnegative terms is at least half.

This is not an equivalence with improvement and not an exhaustive theorem
about all methods. It is an exact necessary dichotomy within the frozen Base
sampling architecture. The old scalar lock `lambda*Xi` is now refined on its
spectral side: a Base-compatible family must generate either a local return
spike (7a) or coherent off-diagonal two-step mass (7b).

## 6. Research consequence

`CONJECTURED`: the E1+E2 hybrid should apply (3)--(4) to a frame kernel
`K_B=M B M*`, after separating its nonconstant diagonal. The hoped-for
mechanism is that source-derived detector diversity lowers both the maximal
row return and the coherent two-step excess, while (2) records the exact
colour price.

The next falsifiable questions are:

1. Can a source-derived prime-block dictionary make the normalized frame
   operator low-coherence without reducing the row threshold by a power?
2. Does RationalMass force (7a), (7b), or both on actual phase-lattice sets?
3. Can the large local-return branch be converted, through the existing
   row-deletion identity, into a smaller subfamily on which (7b) dominates?
4. Does alias-conditional centring remove the phase-lattice contribution to
   `C_2`, or does the sealed extremizer saturate it?

No route is selected by this cycle alone.

## Replay

```sh
python3 proof/build_cycle_10_e1_frame_e2_two_step_v1.py --write
python3 proof/build_cycle_10_e1_frame_e2_two_step_v1.py --check
python3 -m unittest tests/test_cycle_10_e1_frame_e2_two_step_v1.py
```
