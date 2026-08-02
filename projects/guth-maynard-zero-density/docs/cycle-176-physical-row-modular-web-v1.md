# Cycle 176: physical-row numerator-divisor web

## Claim boundary

`PROVED`: aggregate affine eligibility has an exact physical-row incidence
classification. At a nonzero source row `h`, a complete state is integral
exactly when its cross-edge numerator `a` divides `h`; hence only `tau(|h|)`
distinct numerator groups can be eligible. Low row reuse, common nondividing
numerator multiplicity, distinct-numerator avoidance, and gcd energy are all
labelled alternatives.

No actual row-reuse lower bound, eligible mass, target packet, recurrence,
density, or interval gain is proved.

## Physical rather than private coordinates

Cycle 175 represented integrality in a fibre as a class `n=n0 mod m`. At a
physical row `h=h0+r n`, this condition is simply

```text
a | h.                                                (1)
```

Thus it can be aggregated across states only after retaining the physical
row label `(beta,ell,h,j)`. For every incidence retain `(state_id,a,q,K)` and
its range/capacity labels. A range-valid incidence is eligible exactly when
(1) holds.

## Exact incidence alternatives

Freeze a codegree threshold `D>=2`. Rows of degree below `D` form the
physical-support-separation bank. At a high-reuse row, let `A(h)` be its
distinct numerator set. Then

```text
#{a in A(h):a|h} <= tau(|h|).                         (2)
```

The complete row ledger retains numerator multiplicities, the divisor set in
(2), the distinct avoidance count, and

```text
G(h)=sum_(a!=a' in A(h)) gcd(a,a')^2/(a a').          (3)
```

Consequently any high-reuse row is recorded without loss as eligible/range
mass, a common nondividing-numerator group, a distinct numerator-avoidance
web, or its frozen gcd-energy statistic. This is a classifier, not a claim
that any alternative is quantitatively large.

## Why reuse is indispensable

For arbitrarily many states, assign each one a distinct odd physical row and
numerator two. Every state then has codegree one and avoids divisibility.
Therefore state mass, even together with individual Cycle-175 discrepancy,
cannot create an aggregate covering principle without actual physical-row
reuse.

## Consequence

The remaining bridge is an actual exponential/fibre incidence theorem: force
reused physical rows, or prove that the support-separation, common-numerator,
distinct-avoidance, or gcd-energy web itself has quantitative structure.
