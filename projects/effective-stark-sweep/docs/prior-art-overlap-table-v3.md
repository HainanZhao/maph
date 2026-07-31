# Prior-art overlap table — exact object controls v3

This successor preserves `prior-art-overlap-table-v2.md`.  It adds four
exact field-containment controls, not an identification of Stark units,
packets, or theorem hypotheses.

## Dummit--Sands--Tangedal (2003)

In *Stark's conjecture in multi-quadratic extensions, revisited*, JTNB
15 (2003), 83--97, Theorem 2 proves the refined equality `St'` for
every multiquadratic extension and Theorem 4 proves the full Stark
conjecture for every biquadratic extension.  Theorems 1 and 3 give
further full-conjecture cases subject to their stated conditions on
the set `S`, distinguished place, and extension.

This is theorem-class antecedence for a quadratic Engine-A quotient
only after an exact row-level comparison of extension, `S`, place,
normalization, and claimed component.  The census has not run that
map, so it claims neither automatic coverage nor priority from DST.

## Roblot (2013)

In *Index formulae for Stark units and their solutions*, Pacific J.
Math. 266 (2013), 391--422, Theorem 5.5 treats quadratic extensions,
Theorem 6.1 cyclic quartic extensions, and Theorem 7.1 cyclic sextic
extensions under its additional hypotheses.  The H taxonomy tests the
exact weak-coverage predicates for Theorem 7.1.  Its 1,079 full
weak-coverage rows are an exact finite-range count, not a new proof of
Roblot's theorem or an Artin-labelled packet identification.

## Cohen--Roblot (2000): exact Hilbert/ray object controls

Cohen--Roblot's object is the Hilbert class field: the maximal abelian
extension unramified at all finite and infinite places.  The present
objects are one-place ray fields with nontrivial finite modulus.  A
common base field therefore establishes neither object equality nor a
Stark-unit comparison.

The following exact controls enumerate the degree-four subfields of a
frozen ray normal closure and test each against the stated Hilbert
biquadratic polynomial using PARI `nfisisom`.

| base | selected case | normal-closure degree | degree-four subfields | Hilbert-field matches | conclusion |
|---|---|---:|---:|---:|---|
| Q(sqrt(35)) | RQ-001262 | 32 | 11 | 1 | contained |
| Q(sqrt(42)) | RQ-001569 | 16 | 7 | 1 | contained |
| Q(sqrt(51)) | RQ-001894 | 16 | 7 | 0 | not contained |
| Q(sqrt(186)) | RQ-007519 | 16 | 7 | 1 | contained |

Thus containment is mixed even across these four deliberately selected
controls: three positive and one negative.  This is a PROVED exact
subfield statement for the four frozen normal closures only.  It does
not say that containment should hold for other census rows, and it does
not compare a Stark unit, a packet, an Artin label, or the hypotheses
of a Cohen--Roblot construction.

## Claim boundary

This table records primary-source theorem boundaries and four exact
field-object controls.  No prior-work object equality,
theorem-hypothesis match, or packet overlap is claimed without its own
case-level replay artifact.
