# Cycle 178 normalization correction: ordered cross-label mass

## Correction

The Cycle-178 extraction record uses

```text
U_cross = sum_(ell != ell') N_ell N_ell'
        = T^2-sum_ell N_ell^2.
```

`PROVED`: this is the **ordered** distinct-label mass.  The light-fibre bound
in that record is therefore exactly

```text
U_cross >= T(T-2R),
```

and, for `X>=256` and `T>=X^(16/25)`, it gives
`U_cross>=X^(32/25)/2`.  If an unordered convention is wanted instead, put

```text
U_unordered=sum_(ell<ell')N_ell N_ell'=U_cross/2;
```

then all displayed lower bounds for that different statistic are halved.

## Effect

No mathematical conclusion, threshold, or claim boundary of
`cycle-178-diagonal-aware-fibre-extraction-v1` changes: its formula already
uses the ordered sum.  This correction makes the normalization explicit in
the immutable record and prevents later use of the ordered constant for an
unordered statistic.

The mentor checkpoint recommended this refinement before commit.  Its
falsifier is a light count vector violating either the ordered identity or
the factor-two unordered conversion.
