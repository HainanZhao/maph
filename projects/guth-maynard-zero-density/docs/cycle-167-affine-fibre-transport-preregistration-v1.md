# Cycle 167 preregistration: affine-fibre beta transport

## Question and claim boundary

Starting from one `PROVED` Cycle-166 massed, beta-anchored exponential-shift
or seeded-packet state, decide whether its *actual affine anchor fibre* can
produce a beta-preserving cross-label transport edge.  The only permitted
outputs are an exact transport lemma with retained labels, or an exact
labelled obstruction in residue, transformed range, or depth balance.  No
E7/E9 skeleton, census, density, or prime-interval result is preregistered.

The shift approximation `qE_u≈a` is not itself a Cycle-67 local packet
approximation `q alpha_(ell+u)≈a`.  Thus a transported hit becomes a
Cycle-67 seed only after it is joined to an independently retained local
packet at its target label, or after a closed transport loop supplies an
equivalent local relation.  This block proves neither join automatically.

The input parent count is not a count of distinct anchors.  The first task is
therefore deconvolution, not a density assertion: a primitive four-anchor
parent count must be converted to an explicitly retained parameter set before
any divisibility argument is made.

## Frozen state, conventions, and thresholds

Use the Cycle-166 canonical rank-one state and write its retained anchors as

```text
h=h_0+r n,        h'=h'_0+s n,        n in N,
```

with the least canonical parameter zero and primitive common direction.  For
a shift packet retain coprime positive `a,q`, its depth `K`, and

```text
|q E_u-a| <= C_1/(K X).                              (1)
```

Let the original Cycle-67 row range be `I=[H,2H]` and freeze the exact
eligible set

```text
N_elig = {n in N: a divides h_0+r n,
                    h_0+r n in I,
                    q(h_0+r n)/a in I}.             (2)
```

The divisibility condition is not relaxed: it is soluble precisely when
`gcd(a,r)|h_0`, and then it is one residue class modulo
`a/gcd(a,r)`.  The transformed range in (2) is retained rather than replaced
by an asymptotic comparability statement.  Freeze the dimensionless balance

```text
B_tr = H/(aK).                                       (3)
```

as an explicit state coordinate.  The proof must derive the allowed constant
from the enlarged Cycle-67 strip budget; it may not infer it from `qK<=H`.

## Gates

1. **Exact deconvolution.**  For a canonical parameter set `N`, relate the
   number `P(N)` of primitive four-subsets to `|N|` by the exact inequality
   `P(N)<=binom(|N|,4)`.  Keep the map from every parent witness to its
   `n`-quadruple and base/orientation labels.  A statement only about the
   parent exponent is insufficient.
2. **Eligibility classifier.**  Solve the congruence and intersect its
   progression with both intervals in (2).  Either retain all eligible
   labelled anchors, or record the first failed condition: insoluble gcd
   residue, empty transformed range, or explicitly too-small eligible fibre.
3. **Reduced rational cross-label transport.**  Restrict this gate to the
   reduced rational approximant ansatz using the frozen multiplier `q/a`.
   For each eligible anchor define

   ```text
   h^+=q h/a,        j^+=j+h-h^+.
   ```

   Prove the exact identity and its strip error with the original beta.  A
   transport output must retain `(beta,ell,u,a,q,K,h,j,h^+,j^+)`, prove both
   rows lie in the frozen range, and meet the derived `B_tr` budget. It is an
   edge to the target strip, not a Cycle-67 progression until a separate
   target-local packet/loop interface is supplied.
4. **Obstruction alternative.**  If Gate 3 cannot be met, bank the first
   exact labelled residue/range/balance obstruction.  It must exhibit a
   legal affine fibre and state why no claimed transport row is available;
   it is not silently discarded as low density.

## Advance condition and falsifier

Advance if the block proves a beta-preserving transport lemma with its exact
eligible-fibre interface, or proves that the three listed arithmetic
conditions are exhaustive within this affine multiplicative architecture.

The registered falsifier is a legal massed Cycle-166 state whose primitive
four-parent multiplicity arises from an affine fibre avoiding (2), whose
transformed range is empty, or whose `B_tr` cannot fit the enlarged strip
budget, with no second loop changing that condition.  Preserve it as a
labelled obstruction; do not turn it into a global impossibility claim.
