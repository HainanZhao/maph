# DST / Cohen--Roblot comparison table — background v1

**Status:** started; object-level comparison perimeter frozen, exact
subfield comparisons still pending.

The results paper and census paper must distinguish three notions:
same base field, same theorem class, and the same class-field object.
Only the last is a numerical/algebraic packet overlap.

## Cohen--Roblot

Cohen--Roblot compute Hilbert class fields \(H_k/k\), unramified at
all finite and infinite places, for real quadratic discriminants below
2000.  Their Stark-unit construction assumes the rank-one
conjecture, while the resulting field is verified independently.
Our promoted objects are one-place ray fields with nontrivial finite
modulus, so none is the same class-field object.  The base-field
comparison is:

| base discriminant | promoted sweep bases | Cohen--Roblot entry | object-level verdict |
|---:|---|---|---|
| 5, 8, 24, 28, 33, 56, 57, 77 | \(\sqrt5,\sqrt2,\sqrt6,\sqrt7,\sqrt{33},\sqrt{14},\sqrt{57},\sqrt{77}\) | class number 1 | no nontrivial Hilbert packet to compare |
| 140 | \(\sqrt{35}\) | class number 2, \(L_k=\mathbb Q(\sqrt5)\) | different modulus; exact containment check queued |
| 168 | \(\sqrt{42}\), e=6 tranche | class number 2, \(L_k=\mathbb Q(\sqrt2)\) | different modulus; exact containment check queued |
| 204 | \(\sqrt{51}\), e=6 tranche | class number 2, \(L_k=\mathbb Q(\sqrt3)\) | different modulus; exact containment check queued |
| 744 | \(\sqrt{186}\), e=6 tranche | class number 2, \(L_k=\mathbb Q(\sqrt2)\) | different modulus; exact containment check queued |

Primary source:
H. Cohen and X.-F. Roblot, *Computing the Hilbert class field of real
quadratic fields*, Math. Comp. 69 (2000), 1229--1244,
DOI `10.1090/S0025-5718-99-01111-4`.

## Dummit--Sands--Tangedal

| source | proved/computed zone | overlap with this project | paper treatment |
|---|---|---|---|
| DST 1997 | numerical Stark-unit computations over totally real cubic base fields | no base-degree or object-level overlap | computational precedent only |
| DST 2003 | refined Stark equality for abelian groups of exponent 2; full theorem for biquadratic and many related cases | theorem-class overlap with Engine A's quadratic characters; no coverage of the order-6 or order-10 packets as complete packets | Engine A is not advertised as a historical-first result; exact hypothesis alignment is required before counting any A occurrence as new |

Primary sources:

- D. Dummit, J. Sands, B. Tangedal, *Computing Stark units for
  totally real cubic fields*, Math. Comp. 66 (1997), 1239--1267,
  DOI `10.1090/S0025-5718-97-00852-1`.
- D. Dummit, J. Sands, B. Tangedal, *Stark's conjecture in
  multi-quadratic extensions, revisited*, JTNB 15 (2003), 83--97,
  DOI `10.5802/jtnb.388`.

## Remaining exact work

1. For discriminants 140, 168, 204, and 744, test whether the
   Cohen--Roblot Hilbert field is an exact subfield of each promoted
   ray-field normal closure and record the embedding polynomial.
2. Align DST 2003's \(S\), absolute-value normalization, and refined
   equality with the uniform Engine-A theorem before the A bulk is
   described as confirmation, extension, or disjoint.
3. Extend this table from promoted cases to every census-v5 occurrence
   only after the A bulk and occurrence transports close.

No agreement is promoted in this v1 table; it is a scoped comparison
inventory.
