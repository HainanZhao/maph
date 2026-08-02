# Cycle 50: prime-monomial support correlations factor through the original kernel

## Claim boundary

`PROVED`: for every fixed `s` and harmonic order `m>s`, the distinct support
of `F_(m,s)=K(t)^sK(mt)` has an exact correlation kernel

```text
G_(m,s)(h)=K(mh) H_s(h),                             (1)
```

where `H_s` is the complete homogeneous degree-`s` symmetric polynomial in
the prime phases. For `s=3,4`, `H_s` is an explicit fixed combination of
`K(h),...,K(sh)`. A phase-aligned Halász--Montgomery argument reduces large
values of `F_(m,s)` to row sums of this factored difference kernel.

`OBSERVED`: bounding those difference-kernel row sums is open. The finitely
many orders `2<=m<=s` are not covered by the injective factorization. No
`AMPR_s`, `LCAM_s`, density, or interval gain is proved.

## 1. Unique-factorization support theorem

Write a label as

```text
n=q^m p_1...p_s.
```

If `m>s`, any prime other than `q` occurs with exponent at most `s`, while
`q` occurs with exponent at least `m`. Hence `n` uniquely identifies `q` and
then the unordered multiset `{p_1,...,p_s}`. Consequently the number of
distinct labels is exactly

```text
M binomial(M+s-1,s)=X^(s+1+o(1)).                    (2)
```

The coefficient attached to a multiset is its number of orderings. It stays
between one and the Cycle 39 constant, so its square norm is also
`X^(s+1+o(1))`.

## 2. Exact support correlation

Let `z_p=p^(-ih)` and let `h_s(z)` be the sum of all degree-`s` monomials
with nondecreasing prime indices. Summing every distinct support label once
gives

```text
sum_(n in supp F_(m,s)) n^(-ih)=K(mh)h_s(z).         (3)
```

Writing `P_j=K(jh)`, Newton's identities give

```text
H_3(h)=(P_1^3+3P_1P_2+2P_3)/6,

H_4(h)=(P_1^4+6P_1^2P_2+3P_2^2
        +8P_1P_3+6P_4)/24.                          (4)
```

The identities were checked exactly on four rational alphabets of sizes one
through four. Equation (3), however, follows algebraically for every finite
prime set; the finite checks are replay diagnostics, not proof by sampling.

## 3. Large-value reduction

Let `S_(m,s)` be the distinct support and `a_n` the bounded positive
coefficient of `F_(m,s)`. Suppose `T` is a row set of size `R` with
`|F_(m,s)(t)|>=V_m`. Phase alignment and Cauchy--Schwarz give

```text
R^2 V_m^2
 <=(sum_n|a_n|^2)
   [R|S_(m,s)|
    +sum_(t!=u)|G_(m,s)(t-u)|].                      (5)
```

For `m>s`, insert (1) into (5). Equivalently,

```text
R V_m^2
 <=X^(s+1+o(1))
   [X^(s+1)+max_t sum_(u!=t)|K(m(t-u))H_s(t-u)|].    (6)
```

This is a substantial compression: the former coefficient-pair measure over
labels near `X^(s+m)` is replaced by a fixed-degree polynomial in the
original prime kernel evaluated only on row differences.

## 4. New engine and exceptions

`CONJECTURED` difference-kernel estimate (`DK_s`): after dyadic selection in
`m` and `V_m`, the aggregate off-diagonal in (5) is no larger than its
diagonal contribution up to `X^o(1)` on the hollow separated row sets.

The orders `m=2,3` for `s=3` and `m=2,3,4` for `s=4` permit more than one
candidate high-exponent prime and require separate finite collision
polynomials. Since there are only `O_s(1)` such orders, they do not carry the
`X^(3/10)` harmonic-range factor, but they cannot be silently discarded.

## Gate effect

The row--ratio discrepancy gate is replaced by the more concrete
`FACTORED_DIFFERENCE_KERNEL_DK4_PLUS_SMALL_M_OPEN`. Cycle 48 remains the
structured AP-row input; Cycle 50 supplies the exact kernel on which a
general separated-row theorem can act.
