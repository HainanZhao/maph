# Cycle 8: p199 lifted multiple-choice-cover sample

Fix a completed representative `v` in `I(13,199,1)` and put `q=14*199`.
For coordinate `i` and digit `d in {0,...,13}`, define the lifted speed

\[
 w_{i,d}=v_i+199d
\]

and its bad-time mask

\[
 D_{i,d}=\{a\in\mathbb Z_q:14\min(a w_{i,d}\bmod q,\,q-a w_{i,d}\bmod q)<q\}.
\]

An assignment of one digit per coordinate has no denominator-`q` witness if
and only if the selected masks cover `Z_q`.  It is `(13,199,14)`-improper if
and only if this cover condition holds and it fails every Definition-2.1 gcd
properness condition.  Thus the fixed-base fiber question is exactly the
multiple-choice cover CSP: select one of fourteen masks in each of thirteen
groups, cover all `q` times, and avoid the gcd condition.

The solver stores a partial digit assignment and its union mask.  It branches
only on a currently uncovered time `a`, considering every assignment
`(i,d)` with unassigned coordinate `i` and `a in D_{i,d}`.  Every full covering
assignment must make one such choice, so this branching is exhaustive.  It
also prunes only in either of these proved cases:

1. Some uncovered time is covered by no option of an unassigned coordinate;
   then no extension can cover that time.
2. For a prime factor `r in {2,7}` of 14, twelve already assigned lifted
   speeds are divisible by `r`; then omitting the remaining coordinate gives
   the gcd properness condition in every extension, so that branch contains no
   improper tuple.
3. Let `U` be the presently uncovered times. For each unassigned coordinate
   `i`, let `m_i` be the greatest number of points of `U` covered by one of
   its fourteen masks. If `sum_i m_i < |U|`, no assignment of the remaining
   coordinates can cover `U`, because its total new coverage is at most that
   sum. This is an upper bound even though mask overlaps make it loose.

When the union mask is full before all coordinates are assigned, choose for
each remaining coordinate a digit whose lifted speed is coprime to 14 whenever
possible.  Such a digit exists: multiplication by 199 is invertible modulo
14 and the fourteen digits traverse all residue classes modulo 14.  If the
assigned coordinates have not already reached twelve multiples of either 2
or 7, this completion fails the gcd condition and is a directly checked SAT
witness.  Otherwise rule 2 already pruned it.

Consequently a returned `UNSAT` exhausts every permitted digit assignment and
proves that this base representative is absent from `F_1(13,199,14)`.  A
returned `SAT` includes a digit vector and is verified by direct evaluation of
Definition 2.1.  A node or time cap returns `CAP`, which makes no mathematical
claim and retains the base representative.

A deterministic greedy pass may precede the exhaustive search, but it only
supplies a candidate digit vector. It is accepted only after the same direct
improperness test and it never supplies an UNSAT prune or changes the branch
space.
