# A two-spacer aligned-center recursion

Date: 2026-08-07 UTC.

## Outcome

**PROVED.** The one-spacer aligned-center recursion extends to a useful
two-spacer sufficiency theorem. The second summand is not a single bracket;
it is a product with one remaining spacer, and is therefore closed by the
proved one-spacer criterion.

This is successor research to the aligned-center paper. It is not used to
merge that paper with the width-four q-Fibonomial paper.

## Theorem

Let `r,s >= 2`, `k >= 1`, and let `a_1,...,a_k,b,c` be positive integers.
Suppose there are integers `d_1,...,d_k` such that

\[
0\le d_i\le \left\lfloor\frac{a_i-1}{r}\right\rfloor,
\qquad \sum_{i=1}^k d_i=b-1.
\tag{1}
\]

Put `alpha_i=a_i-r d_i`. If either

\[
c\le 1+\sum_{i=1}^k\left\lfloor\frac{\alpha_i}{s}\right\rfloor,
\tag{2}
\]

or there is an index `h` with `d_h=0` and `s | a_h`, then

\[
\prod_{i=1}^k[a_i]_q\,[b]_{q^r}\,[c]_{q^s}
\]

is symmetric and unimodal.

The same statement holds after interchanging `(b,r)` with `(c,s)`.

## Proof

Choose any word of length `b-1` in which the letter `i` occurs `d_i`
times. Start with ordinary lengths `alpha_i` and spacer length one. The base
polynomial is

\[
Q_1(q)=\prod_i[\alpha_i]_q[c]_{q^s}.
\]

Condition (2) makes this symmetric unimodal by the proved one-spacer
criterion. Under the divisibility alternative, the fixed factor `[a_h]_q`
is present in the base and in every later correction because `d_h=0`, so the
divisibility branch of that criterion applies instead.

Suppose the current `r`-spacer length is `j`, the selected ordinary length is
`x`, and `B(q)` is the product of all other current ordinary factors. The
one-spacer identity, multiplied by the untouched `s`-spacer, gives

\[
[x+r]_qB(q)[j+1]_{q^r}[c]_{q^s}
=q^r[x]_qB(q)[j]_{q^r}[c]_{q^s}
 +[x+r(j+1)]_qB(q)[c]_{q^s}.
\tag{3}
\]

The first summand is a translate of the previous two-spacer polynomial. The
second is a one-spacer product. Under (2), every ordinary length in this
second summand is at least its base value `alpha_i`; hence

\[
\sum_i\left\lfloor\frac{\text{current length}_i}{s}\right\rfloor
\ge \sum_i\left\lfloor\frac{\alpha_i}{s}\right\rfloor\ge c-1,
\]

so the one-spacer criterion applies. Under the divisibility alternative, the
unchanged factor `[a_h]_q` supplies the required multiple of `s`.

It remains to verify the common center. If the previous degree is

\[
E=(x-1)+\deg B+r(j-1)+s(c-1),
\]

then the new degree is `E+2r`. The translated first summand has support
`[r,E+r]`, whose endpoints sum to `E+2r`, while the second summand has degree

\[
x+r(j+1)-1+\deg B+s(c-1)=E+2r.
\]

Thus the summands in (3) are symmetric unimodal about the same center. Their
sum is symmetric unimodal. Iterating the selected word reconstructs every
`a_i` and the spacer `[b]_(q^r)`, proving the theorem.

## Allocation-free quantitative corollary

A convenient sufficient condition is

\[
\sum_i\left\lfloor\frac{a_i-1}{r}\right\rfloor\ge b-1
\tag{4}
\]

and

\[
\sum_i a_i-r(b-1)\ge s(c-1)+k(s-1).
\tag{5}
\]

Indeed, (4) permits an allocation satisfying (1). For every such allocation,
`sum alpha_i=sum a_i-r(b-1)`. Since

\[
\left\lfloor\frac{x}{s}\right\rfloor
\ge\frac{x-(s-1)}s,
\]

(5) implies (2). This is an explicit gap-absorption bound. The swapped
version gives a second sufficient region.

## Claim boundary and falsifier

The theorem gives sufficient conditions, not a characterization. It does not
prove that every two-spacer product is unimodal, nor does it by itself settle
width five. A falsifier would be an instance satisfying (1) and (2), or the
stated fixed divisibility alternative, whose direct coefficient sequence is
not symmetric unimodal or disagrees with the recursion.

Exact bounded checks are implemented in
`discovery/two_spacer_aligned_recursion_check.py`; they are regression
evidence, not premises of the proof.

