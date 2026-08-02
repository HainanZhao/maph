# Cycle 186 working ledger: actual-curve convexity grid exclusion

## Starting point (CONJECTURED)

Let `z=exp(2*pi/Delta)`, `a<b<c`, `q=b-a`, `p=c-b`, and
`r=p+q`.  The true shifted slopes have strict weighted convexity

```text
C_curve = p*z^a + q*z^c - r*z^b > 0.
```

For rational shifted approximants `B_i/U_i=z^i+e_i`, form the cleared
rational difference

```text
R = p*B_a/U_a + q*B_c/U_c - r*B_b/U_b.
```

If `R!=0`, then `|R|>=1/(U_a U_b U_c)`.  If its propagated error is `E`, a
strict sandwich `E<C_curve` and `C_curve+E<1/(U_aU_bU_c)` is contradictory:
the first inequality makes `R>0`, and the second makes it a nonzero rational
smaller than its denominator grid.  This would exclude all such triples
without assuming they are arithmetic progressions.

The main falsifier is scale: the required sandwich may constrain only tiny
label windows, leaving enough sparse labels for critical mass.  No population
claim is made until the exact envelope and an explicit frozen-box substitution
are replayed.

## Log

- 2026-08-02: opened after the Cycle 185 shifted-convention correction. No
  executable derivation has run. The intended input is actual exponential
  convexity, not mass/capacity-only additive combinatorics.

