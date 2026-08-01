# Cycle 128 — quadratic deleted-prime cover theorem

## Headline outcomes

`PROVED` — Let `K` be real quadratic and let the one-place modulus
`m = f infinity_2` be in the quadratic-support regime.
For every supported character `chi`, write `chi^circ` for its
primitive quadratic character and

\[
  \mathcal D_\chi=
  \{\mathfrak p:\mathfrak p\mid\mathfrak f,
     \mathfrak p\nmid\mathfrak f_\chi\}.
\]

Then the following are equivalent:

1. `X_A = 1` for every ray class `A`;
2. `L'_m(0,chi) = 0` for every supported `chi`;
3. `E_chi = 0` for every supported `chi`;
4. every supported `chi` has a deleted prime in `D_chi` with
   primitive-character value `+1`.

Thus packet triviality is exactly a deleted split-prime cover of the
supported characters.  It can be decided from conductors and exact
local character values before class-number, regulator, or unit
computations.

`PROVED` — In the frozen 1,560-row quadratic corpus, the exact export
has 2,232 supported character occurrences, 1,516 deleted-prime
occurrences, 699 trivial local values, and 672 zero Euler products.
The cover holds on exactly 346 rows and agrees with the exact packet
polynomial `x - 1` on every row, with zero character-level and row-level
classification errors.  The 346 rows split as 296 one-support and 50
two-support rows.

`PROVED` — The tempting claim that four supported quadratic characters
prevent total degeneracy is false.  The preregistered expanded-range
search finds the exact counterexample

\[
 K=\mathbb Q(\sqrt7),\qquad
 \mathfrak f=[42,0;0,6],\qquad N\mathfrak f=252.
\]

Its ray group is `C6 x C2 x C2`, its sign log is `(3,1,0)`, and each
of its four supported characters has a deleted prime with
primitive-character value `+1`.  All four Euler products
therefore vanish.  This example is outside the frozen census and does
not change any 8,200-row count.

## Proof

For a supported quadratic character,

\[
 E_\chi=\prod_{\mathfrak p\in\mathcal D_\chi}
 (1-\chi^\circ(\mathfrak p)).
\]

At each deleted prime the primitive character is unramified and has
value `+1` or `-1`.  The product vanishes exactly when one value is
`+1`.  The remaining factor in the explicit quadratic derivative
formula is nonzero: class numbers and indices are positive and the
oriented relative-unit logarithm is positive.  Hence
`L'_m(0,chi) = 0` exactly when `E_chi = 0`.
Exact Fourier inversion gives packet-one from vanishing of every
supported derivative, while character orthogonality gives the converse.

This is a consequence of the already proved uniform quadratic formula.
The equivalence supplies the decision form used by this census: it
isolates the exact local work needed to recognize the value-one
sub-stratum. No priority claim is made.

## Failed coarse patterns preserved

`OBSERVED` — Every preregistered simplification weaker than the cover
criterion has counterexamples in the frozen corpus.

| candidate | false positive | false negative | least relevant counterexample |
|---|---:|---:|---|
| at least one deleted prime | 579 | 0 | RQ-000013 |
| at least one split deleted occurrence | 257 | 0 | RQ-000089 |
| every character has some deleted prime | 437 | 0 | RQ-000013 |
| number of split occurrences at least support size | 8 | 0 | RQ-001359 |
| every deleted occurrence is split | 43 | 106 | RQ-000161 / RQ-000355 |
| one support and some split deleted prime | 0 | 50 | RQ-000644 |

RQ-001359 explains why counts alone fail: its two split deleted-prime
occurrences both kill the same supported character, while the other
character survives.  Among the 50 all-zero two-support rows, only 18
have one common killing prime ideal, 28 have one common underlying
rational prime, and 22 require different rational primes.  The cover is
therefore character-labelled data, not an unlabeled prime count.

## Provenance containment and replay

The first proof audit failed because the expanded-search amendment had
been appended to the original preregistration after the feature export,
invalidating its recorded hash.  No result was promoted.  The original
file was restored byte-for-byte, the amendment was separated, and v2
analysis/search artifacts were replayed.  The superseded v1 discovery
records remain preserved.

Replay from the project root:

```text
python3 discovery/run_q_euler_local_feature_export.py
python3 discovery/analyze_q_euler_patterns.py
python3 discovery/search_q_four_support_counterexample.py
python3 proof/audit_q_euler_deleted_prime_cover.py
```

The principal exact feature export took 12.61 seconds wall time with
56,276 KiB peak RSS.  The expanded counterexample search terminated in
4.15 seconds after 394 selected moduli and thirteen four-support rows,
with 62,076 KiB peak RSS.  The sealed proof record is
`artifacts/q-euler-deleted-prime-cover-theorem-v1.json`.
