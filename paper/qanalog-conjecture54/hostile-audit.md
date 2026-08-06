# Hostile proof audit

Audit date: 2026-08-06 UTC.

## Claim under attack

`PROVED`: the sufficient direction of Connelly--Ito--Martinez--Shevchenko--
Yang Conjecture 5.4 holds for all `k >= 1` and `r >= 2`.

## Failure modes checked

1. **The recursion could have an off-by-one spacer.** Expanding both sides
   confirms

   ```text
   [a+r]_q[b+1]_(q^r)
     = q^r[a]_q[b]_(q^r) + [a+r(b+1)]_q.
   ```

   Independently, the complementary exponent pairs have weights exactly
   `0,...,a+r(b+1)-1`, with neither a gap nor a duplicate.

2. **A sum of unimodal terms need not be unimodal.** The proof does not use
   that false statement. It verifies a common center at every step: if the
   old degree is `E`, both new summands have support endpoints summing to
   `E+2r`. The closure lemma applies only after this equality is checked.

3. **Translation might destroy symmetry.** The translated old polynomial is
   padded by `r` zeros at both ends inside the new degree range. Its support
   is `[r,E+r]`, whose endpoints sum to the new degree `E+2r`.

4. **The allocation could create a zero q-integer.** This cannot occur in the
   induction branch: `r` divides none of the final `a_i`, so
   `a_i-r floor(a_i/r)` lies in `{1,...,r-1}`. Any smaller allocation also
   leaves a positive base length.

5. **The divisibility disjunct might be silently omitted.** It is handled
   separately by
   `[rs]_q=[r]_q[s]_(q^r)`. Multiplication by `[r]_q` converts the symmetric
   unimodal coefficient sequence in `q^r` into length-`r` constant blocks,
   after which ordinary product closure applies.

6. **The theorem might accidentally claim necessity.** The abstract,
   theorem discussion, reproducibility section, README, and verification
   record all restrict the claim to sufficiency. The source's example
   `([3]_q)^4[2]_(q^4)` is retained as a passing regression outside the
   inequality.

7. **The named result might already have changed.** The exact primary source
   text of Conjecture 5.4 was checked in arXiv:2605.12822v1, Section 5.2. A
   bounded arXiv/API and source-repository audit through 2026-08-06 found no
   later primary record resolving it. No universal priority claim is made.

## Exact regression evidence

`OBSERVED`: CPython 3.12.3 checked the recursion by two constructions for
1,680 triples `(a,b,r)`, then reconstructed and directly multiplied 15,163
admissible non-divisible instances across `2 <= r <= 6`, `1 <= k <= 4`, and
lengths at most 12. Every identity, center, symmetry, and unimodality check
passed. The universal claim rests on the proof, not this finite corpus.

Audit outcome: no surviving defect in the promoted claim.
