# A hybrid multi-spacer aligned-center sufficiency criterion

Date: 2026-08-07 UTC.

Status: **PROVED** as a standalone future-topic result. This is W3 output and
does not enter either existing manuscript.

## Theorem

Let `k>=1`, `s>=1`; let `a_1,...,a_k` and `b_1,...,b_s` be positive
integers; and let `r_1,...,r_s>=1`. Suppose there is a matrix of nonnegative
integers `d_(j,i)` such that

\[
\sum_{i=1}^k d_{j,i}=b_j-1\qquad(1\le j\le s)
\tag{1}
\]

and

\[
\alpha_i:=a_i-\sum_{j=1}^s r_jd_{j,i}\ge1
\qquad(1\le i\le k).
\tag{2}
\]

Then

\[
\prod_{i=1}^k[a_i]_q\prod_{j=1}^s[b_j]_{q^{r_j}}
\]

is symmetric and unimodal.

No coprimality assumption on the spacer steps is needed.  The statement also
allows `r_j=1`; in that case the corresponding spacer is simply another
ordinary bracket.  For example, when `k=s=1` and `r_1=1`, the displayed
condition is `b_1<=a_1`, which is consistent with interchanging the two
ordinary brackets.

## Hybrid theorem

Before applying the matrix theorem, one may choose disjoint sets of spacer
indices `J` and ordinary-factor indices `I`, together with a bijection
`phi:J -> I`, such that

\[
r_j\mid a_{\phi(j)}\qquad(j\in J).
\tag{H}
\]

Delete each paired spacer and ordinary factor.  If the allocation-matrix
hypotheses (1)--(2) hold for the residual product, then the original product
is symmetric unimodal.  Empty residual products are allowed.

Indeed, for every pair in (H), writing `a_i=r_j e` and `z=q^{r_j}` gives

\[
[a_i]_q[b_j]_{q^{r_j}}
 =[r_j]_q\bigl([e]_z[b_j]_z\bigr)\big|_{z=q^{r_j}},
\]

which is symmetric unimodal.  The pairs are disjoint, so these standalone
factors are symmetric unimodal: the coefficients of the unimodal product
`[e]_z[b_j]_z` are repeated in consecutive blocks of length `r_j` after
substitution and multiplication by `[r_j]_q`.  The pairs and the residual
matrix-certified factor partition the original product.  Closure of
symmetric unimodality under products completes the argument.  This is the
only interaction between divisibility absorption and allocation; no consumed
ordinary-factor column remains in the matrix.

For one spacer this hybrid statement recovers both branches of the proved
one-spacer criterion: use (H) when some `r` divides an `a_i`; otherwise
`floor((a_i-1)/r)=floor(a_i/r)`, so matrix feasibility is equivalent to
`b<=1+sum_i floor(a_i/r)`.

## Proof

Induct on the number `s` of spacers. The case `s=0` is a product of ordinary
q-integers. For `s>=1`, first subtract the allocations for spacer 1:

\[
a_i^{(0)}=a_i-r_1d_{1,i}.
\]

Condition (2) shows that the remaining rows of the same matrix certify the
induction hypothesis for

\[
\prod_i[a_i^{(0)}]_q\prod_{j=2}^s[b_j]_{q^{r_j}}.
\]

This is the base at first-spacer length one. Reconstruct the `b_1-1`
increments in any order realizing the first row of the matrix. If the
selected current ordinary length is `x`, the current first-spacer length is
`c`, `B(q)` is the product of the other ordinary factors, and `R(q)` is the
product of spacers `2,...,s`, then

\[
[x+r_1]_qB(q)[c+1]_{q^{r_1}}R(q)
=q^{r_1}[x]_qB(q)[c]_{q^{r_1}}R(q)
 +[x+r_1(c+1)]_qB(q)R(q). \tag{3}
\]

The first summand is the translated previous polynomial. In the second
summand, every ordinary length is at least its base value `a_i^(0)`; using
the unchanged remaining allocation rows therefore still leaves all final
lengths positive. The induction hypothesis makes this correction term
symmetric unimodal.

If the old degree is `E`, both summands in (3), padded to the new support,
have center `(E+2r_1)/2`: the translated old support is
`[r_1,E+r_1]`, and direct degree calculation gives `E+2r_1` for the
correction. Their sum is symmetric unimodal. Iteration reconstructs the first
spacer and all ordinary lengths, completing the induction.

## Quantitative corollary

Let

\[
L=\sum_{j=1}^s r_j(b_j-1).
\]

If some ordinary length `a_i>=L+1`, assign every spacer increment to that
factor. Conditions (1)--(2) hold, so the product is symmetric unimodal. In
particular, the stronger condition `min_i a_i>=L+1` suffices.

This additive weighted-demand bound is sharper than a bound involving the
product of the spacer steps.

## Claim boundary

The allocation condition is sufficient, not necessary. The theorem does not
assert that every multi-spacer product is unimodal. It does show that the
two-spacer obstruction from symmetry alone is not essential once a smooth
ordinary factor can absorb the total spacer demand.

The unqualified phrase "generalizes the one-spacer sufficiency theorem" is
accurate only for the hybrid theorem.  The bare matrix theorem generalizes
the inequality branch and omits the divisibility branch.  For instance,
`[2]_q[b]_(q^2)=[2b]_q` is unimodal for every `b`, whereas the one-column
matrix condition holds only for `b=1`.

The smallest adversarial families make the non-necessity visible.  For
`[a]_q[2]_(q^2)[2]_(q^3)`, the matrix activates at `a=6`; exact coefficients
are non-unimodal at `a=1,4`, unimodal at `a=2,3,5`, and unimodal throughout
the checked tail `6<=a<=15`.  Thus its eventual threshold misses the true
tail threshold `a=5` by one (with two additional isolated true cases below
it).  For repeated steps `[a]_q[2]_(q^2)[2]_(q^2)`, the matrix activates at
`a=5`, while `a=2` is already unimodal.  This gap is the price of assigning
every spacer increment against worst-case smooth-factor capacity.

With no smooth factor, adjoining the neutral factor `[1]_q` shows that
`[2]_(q^2)[2]_(q^3)=1+q^2+q^3+q^5` fails (2), as it must.  More generally,
if a nontrivial spacer step `r_j` exceeds `sum_i(a_i-1)`, its row cannot be
funded, so the matrix theorem is silent.

For the stable width-five residue map, exact checking of every injective
bracket decomposition gives the following coverage modulo 60:

- matrix only: `2,3,4,7,8,14,23,24,26,29,31,32,41,47,49,51,53,54`;
- divisibility absorption only: no class (three nontrivial spacers but only
  two smooth factors remain);
- hybrid: the same 18 classes as matrix only.

The other 24 decomposable classes and all 18 classes without an injective
bracket decomposition are not reached.  Consequently this criterion does
not subsume the width-five theorem; the restricted-partition kernel remains
essential for 42 of the 60 stable classes and provides the single uniform
proof for all classes.

Exact recursive checks are in
`discovery/multi_spacer_aligned_recursion_check.py`. They are regression
evidence, not premises of the induction.  Exact adversarial and width-five
coverage checks are in
`experiments/multi_spacer_adversarial_and_width5_overlap.py`.
