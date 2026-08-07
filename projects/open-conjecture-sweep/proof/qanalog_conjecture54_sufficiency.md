# Sufficient direction of Conjecture 5.4

## Claim boundary

`PROVED`: Let `r >= 2`, `k >= 1`, and let `a_1,...,a_k,b` be positive
integers. If some `r | a_i`, or if

```text
b <= 1 + sum_i floor(a_i/r),
```

then

```text
product_i [a_i]_q [b]_(q^r)
```

is symmetric and unimodal.

This is the full sufficient direction of Connelly--Ito--Martinez--
Shevchenko--Yang, Conjecture 5.4, and is stronger than the `k=r=4` slice in
`GOAL.md`. It does **not** assert necessity when `k >= 4` and `r >= 4`.
Indeed, the source gives the unimodal polynomial `([3]_q)^4[2]_(q^4)` as a
counterexample to necessity.

## Aligned-center recursion

For all positive `a,b,r`,

```text
[a+r]_q [b+1]_(q^r)
  = q^r [a]_q [b]_(q^r) + [a+r(b+1)]_q.             (1)
```

`PROVED` (algebraic route): use

```text
[a+r]_q = [r]_q + q^r[a]_q,
[b+1]_(q^r) = 1 + q^r[b]_(q^r),
(q^r-1)[b]_(q^r) = q^(rb)-1.
```

After subtracting `q^r[a]_q[b]_(q^r)`, the remaining terms are

```text
[r]_q[b+1]_(q^r) + q^(r(b+1))[a]_q
  = [r(b+1)]_q + q^(r(b+1))[a]_q
  = [a+r(b+1)]_q.
```

`PROVED` (independent coefficient route): the left side counts pairs

```text
(x,j),  0 <= x < a+r,  0 <= j <= b,
```

with weight `x+rj`. The pairs with `x<a` and `j>=1` give the shifted first
summand on the right. The complementary pairs have either `j=0`, or `x>=a`
and `j>=1`; their weights occur exactly once and fill the consecutive interval
from `0` through `a+r(b+1)-1`. They give the second summand.

## Induction

The product of nonnegative symmetric unimodal polynomials is symmetric
unimodal. A translate `q^sF(q)` is understood with zero coefficients outside
its support; it remains symmetric unimodal about its translated center.
Sums of nonnegative symmetric unimodal coefficient sequences with a common
center are again symmetric unimodal.

If `r | a_i`, write

```text
[a_i]_q = [r]_q [a_i/r]_(q^r).
```

Then `[a_i]_q[b]_(q^r)` is symmetric unimodal, as is its product with the
remaining ordinary `q`-integers. This proves the first disjunct.

Now suppose no `a_i` is divisible by `r`, and put `c_i=floor(a_i/r)`. Choose
integers `d_i` with

```text
0 <= d_i <= c_i,   sum_i d_i = b-1.
```

Such a choice exists by the assumed inequality. Set
`a_i^(0)=a_i-rd_i`; every base length is positive because `r` does not divide
`a_i`. At spacer length one, the base polynomial is simply
`product_i[a_i^(0)]_q`, hence is symmetric unimodal.

Starting from the base, perform the `sum d_i=b-1` allocated steps. At a step,
increase one current length `a` to `a+r` and the current spacer length `c` to
`c+1`. If `B(q)` denotes the product of all other current ordinary
`q`-integers, (1) gives

```text
[a+r]_q B(q)[c+1]_(q^r)
 = q^r [a]_q B(q)[c]_(q^r)
   + [a+r(c+1)]_q B(q).                            (2)
```

By induction the first summand is a translate of a symmetric unimodal
polynomial. The second is a product of ordinary `q`-integers, so it is
symmetric unimodal. If the old degree is

```text
E = (a-1) + deg B + r(c-1),
```

then the new degree is `E+2r`. The support endpoints of the first summand sum
to `E+2r`, while the degree of the second summand is

```text
a+r(c+1)-1 + deg B = E+2r.
```

Thus both summands in (2) have the same center, `(E+2r)/2`; their sum is
symmetric unimodal. Iterating reconstructs the requested final lengths and
spacer, proving the claim.

## Exact replay

Run:

```sh
python3 proof/qanalog_conjecture54_sufficiency.py
```

The standard-library replay checks (1) by direct polynomial multiplication
and by the independent pair partition, reconstructs bounded instances through
the aligned-center induction, compares every recursive polynomial with direct
multiplication, checks symmetry/unimodality and center alignment at every
step, and preserves the source's non-necessity example as a scope regression.
The bounded rows are regression evidence only; the universal proof is the two
derivations of (1) and the induction above.
