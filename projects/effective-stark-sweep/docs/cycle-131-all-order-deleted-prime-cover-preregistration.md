# Cycle 131 — all-order deleted-prime cover implication

Recorded: 2026-08-01 UTC, before computing any higher-order local
character features.

## Objective and claim boundary

Prove and test the one-way extension of the deleted-prime cover
criterion to every finite-order supported ray character.  The proposed
statement is:

> If, for every character in the differenced Fourier support, some
> prime deleted from the selected modulus has primitive-character value
> one, then the differenced packet is identically one.

This is a one-way statement. No converse is proposed outside the
quadratic-support regime, and no nonvanishing assertion for a
higher-order primitive derivative is in scope.

The proof route is the imprimitive identity
\[
 L_{\mathfrak m}(s,\chi)=L(s,\chi^\circ)
 \prod_{\mathfrak p\in\mathcal D_\chi}
 (1-\chi^\circ(\mathfrak p)N\mathfrak p^{-s}),
\]
followed by differentiation at zero and exact Fourier inversion.  A
value one in the product forces both its value and derivative at zero
to vanish because the primitive rank-one factor already vanishes at
zero.  The discovery export may check the local cover predicate only;
it never identifies a packet value or supplies a converse.

## Frozen population and fields

- Population: all 2,704 rows in the frozen H stratum, selected by
  `support_orders` containing an order greater than two in
  `artifacts/w1-full-census-v1.json`.
- Per supported finite-order character: ray coordinates, character
  order, primitive conductor and ray-group coordinates, and every
  deleted prime's HNF, norm, exponent, and primitive-character phase
  in rational-log form.
- Positive local event: phase has denominator one, equivalently
  primitive-character value exactly one.
- No packet polynomials, numerical values, case-order selection, or
  post-result predicates may enter the theorem or the finite screen.

## Gates

1. The exporter must exactly reproduce each selected row's ray group,
   sign log, and supported-character orders from the frozen W1 record.
2. Every deleted prime must be unramified for the recovered primitive
   character; a failed conductor gate halts that row and is retained.
3. The audit must recompute the cover predicate from the full export,
   report every covered row, and separately report RQ-000692.
4. The theorem is promoted only through the symbolic Euler-product and
   Fourier-inversion proof; the H count is a finite `OBSERVED` corollary.

## Resources and stop rule

Run one deterministic PARI/GP 2.15.4 export with a 60-minute wall cap
and 6 GiB resident-memory cap.  A per-row 120-second cap preserves a
row as `TOOL_FAILURE` rather than dropping it.  Stop after the full
audit, or after a repeated tool failure is recorded and the affected
finite corollary is withheld.
