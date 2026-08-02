# Cycle 52: a large support correlation forces two-scale prime recurrence

## Claim boundary

`PROVED`: uniformly for fixed `s` and every `m>=2`, the Cycle 51 distinct-
support correlation satisfies

```text
G_(m,s)(h)=K(mh)K(h)^s/s!+O_s(M^s).                 (1)
```

Thus every correlation within a fixed power less than one of the maximal
`M^(s+1)` scale forces simultaneous large values of `K(h)` and `K(mh)`.

`OBSERVED`: no theorem yet forces enough row differences into this large-
correlation regime, and no additive-structure theorem has been applied. No
`ADK_s`, `AMPR_s`, `LCAM_s`, density, or interval gain is promoted.

## 1. Top support stratum

The support labels with `s+1` distinct primes have exponent partition

```text
(m,1,...,1).
```

Summing ordered choices of `q,p_1,...,p_s` with all indices distinct and
dividing by `s!` gives their support correlation. Replacing the distinct sum
by the unrestricted product `K(mh)K(h)^s` introduces only tuples with a
collision among `s+1` indices. There are `O_s(M^s)` such tuples.

Every remaining support partition has at most `s` distinct primes. The
number of such assignments is also `O_s(M^s)`. For `m>s` the list is indexed
by partitions of `s`; for `2<=m<=s` there are only finitely many values of
`m`, so the constant remains dependent only on `s`. This proves (1) uniformly
in the growing harmonic range.

At `h=0`, (1) reconciles with

```text
|supp F_(m,s)|=M binomial(M+s-1,s)
               =M^(s+1)/s!+O_s(M^s)
```

in the stable range, while Cycle 51 supplies the same leading stratum for
the small orders.

## 2. Quantitative inverse statement

Write

```text
|K(h)|=M X^(-alpha),    |K(mh)|=M X^(-beta).
```

If fixed `0<=eta<1` and

```text
|G_(m,s)(h)|>=M^(s+1)X^(-eta),                       (2)
```

then the error in (1) is smaller by `X^(1-eta-o(1))`, and

```text
s alpha+beta<=eta+o(1).                              (3)
```

In particular `alpha<=eta/s+o(1)` and `beta<=eta+o(1)`. For `s=4`, the
Cycle 48 threshold `eta=7/50` forces

```text
|K(h)|>=M X^(-7/200-o(1)),
|K(mh)|>=M X^(-7/50-o(1)).                           (4)
```

These are much nearer full recurrence than the original
`X^(7/10)=M X^(-3/10)` row threshold.

## 3. Difference-set engine

Insert (1) into Cycle 50's phase-aligned inequality. If the diagonal term
does not control a large-value row class, the off-diagonal forces many
weighted differences `h=t-u` satisfying (2), and hence (3). The analytic
program becomes:

1. convert the large off-diagonal sum into a popular-difference graph;
2. use (3) to label popular edges by two-scale near-full prime recurrences;
3. extract an approximate progression or a low-rank generalized progression;
4. apply Cycle 48 to the progression branch and a genuine nonlattice
   difference estimate to the remaining branch.

Steps 1--4 are proposed research, not deductions of this cycle.

## Gate effect

The all-harmonic kernel is self-dual at its top stratum. The live gate is
`POPULAR_TWO_SCALE_DIFFERENCES_TO_STRUCTURE_OPEN`, with exact inverse
thresholds supplied by (3).
