# Cycle 2, Stream B, Route A v2: application closure

## Outcome and boundary

`PROVED`: the two external blockers in Stream B Route A v1 are closed for the
published Guth--Maynard §13.1 transfer.  Maynard--Pratt supplies the precise
Type-II containment and Montgomery supplies the discrete mean-value branch.
The source conventions, multiplicity conversion, support preparation, and
all asymptotic losses are recorded in a separately replayable v2 artifact.

This does not re-prove Guth--Maynard's large-values theorem or zero-density
theorem, and claims no improved exponent.  Route A v1 is retained unchanged.

## Closed transfers

- `PROVED` — MP's detector, threshold, dyadic range, (eta)-cutoff, and
  ([T,2T]) positive-height convention agree with GM exactly.  MP Lemma 23
  makes each GM-complement-of-Type-I zero Type II; Lemma 24 gives
  (T^{2(1-sigma)}(\log T)^{O(1)}) in the full Stream-B range.

- `PROVED` — HSW's frozen Riemann--von Mangoldt bound yields an
  (O(\log(T+2))) unit-strip count by subtracting two endpoint bounds.  The
  Bui--Heath-Brown source explicitly fixes multiplicity.  Thus MP's
  location-based convention can lose at most one logarithm, which is already
  within MP's stated logarithmic loss.  Conjugation gives the two-sided count
  from the positive-height dyadic estimate.

- `PROVED` — GM's smooth beta-dependent cutoff is uniform, its Fourier tail
  is rapidly decreasing, and the multiplicity-inclusive strip bound supplies
  the 1-separated extraction.  Original and powered detector coefficients,
  coefficient-one normalization, and boundedly many dyadic support blocks
  incur only explicitly retained (T^{o(1)}) losses.

- `PROVED` — Montgomery's Theorem 1 (printed p. 335, frozen scan p. 348)
  applies to arbitrary complex coefficients at separated points in an
  arbitrary real interval.  Reflect the GM ordinates and use an enclosing
  interval, giving (delta\ge1).  With
  (sum|c_m|^2\le N^{k+o(1)}), its bound yields
  
  \[
  |W|\le T^{o(1)}\bigl(N^{2k-2k\sigma}+TN^{k-2k\sigma}\bigr),
  \]
  exactly the two GM mean-value terms.

Every displayed (o(1)) is a finite product of logarithmic, fixed-(k)
divisor, and source-`lessapprox` losses.  For a requested epsilon the replay
allocates epsilon/20 to each, so no finite-(T) exponent equality is claimed.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/audit_cycle2_stream_b_route_a_v2.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_b_route_a_v2.py -v
```
