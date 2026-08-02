# Cycle 60: E11 contractions are an exact coordinate-ANOVA decomposition

## Claim boundary

`PROVED`: the tuple-energy density associated with phase-aligned rows has an
exact orthogonal Hoeffding/ANOVA decomposition over the powered prime and the
`s` ordinary prime coordinates. Centering a coordinate replaces its edge
phase by `p^(-ih)-k(h)`; averaging it contributes `k(h)`. The fully centered
component is exactly the Cycle-56 edge-cumulant field, and its squared norm is
the complete Hilbert quadratic form from Cycle 57.

For `s=3,4` there are respectively 16 and 32 subset components, grouped into
8 and 10 symmetry types. These fixed counts cause no exponent loss.

This is an identity, not a lower bound for a nonconstant component. It proves
no restriction estimate, `AMPR_s`, density gain, or interval gain.

## Exact decomposition

For row weights `z_t`, define

```text
S(q,p_1,...,p_s)
  = sum_t z_t q^(-imt) product_(j=1)^s p_j^(-it),
E=|S|^2.
```

Let `A_j` average in coordinate `j` and `D_j=I-A_j`. The operators are
commuting self-adjoint orthogonal projections. For every subset `J` of the
`s+1` coordinates, set

```text
E_J = product_(j in J)D_j product_(j notin J)A_j E.
```

Then

```text
E=sum_J E_J,
<E_J,E_L>=0  for J!=L,
||E||_2^2=sum_J||E_J||_2^2.                         (1)
```

Writing `h=t-u`, one coordinate phase in `E` is `p^(-ih)`. Therefore

```text
A[p^(-ih)]=k(h),
D[p^(-ih)]=p^(-ih)-k(h)=w_h(p).                     (2)
```

The powered coordinate has the identical formula with `h` replaced by
`mh`. Thus each component is explicitly

```text
E_J = sum_(t,u) z_t conj(z_u)
      product_(centered coordinates) w_(c_j h)(p_j)
      product_(averaged coordinates) k(c_j h),       (3)
```

where `c_0=m` and every ordinary `c_j=1`.

## Distinguished components

The constant component is

```text
E_empty=sum_(t,u)z_t conj(z_u)k(mh)k(h)^s
       = average_(q,p_1,...,p_s)|S|^2.               (4)
```

The full interaction is

```text
E_all(q,p_1,...,p_s)
 =sum_(t,u)z_t conj(z_u)w_(mh)(q)product_j w_h(p_j).
```

If edges `e=(t,u)` have `omega_e=z_t conj(z_u)`, Cycle 56 gives

```text
||E_all||_2^2
 =sum_(e,f)omega_e conj(omega_f)
   C_m(h_e,h_f)C(h_e,h_f)^s.                        (5)
```

This is the exact weighted quadratic form requested after Cycle 59. Cycle
57 represents the same object as a Hilbert-valued Dirichlet polynomial on
the collapsed labels `q^m p_1...p_s`.

## Routing dichotomy

Subtracting the constant component in (1) gives

```text
||E-E_empty||_2^2=sum_(J nonempty)||E_J||_2^2.       (6)
```

Consequently, if the tuple-energy variance is large, some nonconstant
component has the same exponent, since there are at most 31 of them. Its
subset `J` states exactly which prime coordinates have genuinely contracted.
This is E11's rigorous routing rule.

If the variance is small, `E` is nearly constant across prime tuples. That
case cannot be discarded: it is a new **flat-energy inverse branch**. Large
mean detector response plus small energy variance says that almost every
prime tuple sees essentially the same phase-aligned row energy. A theorem
must either exclude this using the actual logarithms or exploit it to build a
second detector.

## Revised analytic targets

`CONJECTURED`:

1. **ANOVA restriction branch:** bound every nonconstant component at its
   coordinate-cardinality scale, with the full interaction using the Cycle
   57 Hilbert coefficients. The combined bound must save `>3/50` in the
   complete quadratic form, not only on its diagonal.
2. **Flat-energy inverse branch:** show that near constancy of `|S|^2` over
   prime tuples is incompatible with the hollow separated row set, or forces
   two-scale logarithmic recurrence/detector surgery.

The first branch is finite—16 components for `s=3`, 32 for `s=4`—and each
component has an explicit centered/averaged coordinate signature.

## Gate effect

The live gate becomes
`ANOVA_COMPONENT_RESTRICTION_OR_FLAT_ENERGY_INVERSE_OPEN`.
