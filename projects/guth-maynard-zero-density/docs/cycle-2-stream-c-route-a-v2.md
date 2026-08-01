# Cycle 2, Stream C, Route A v2: external-input closure

## Outcome and claim boundary

`PROVED`: the three external-input blockers retained by Route A v1 are now
closed for the published Guth--Maynard §13.2 deduction.  The v2 record pins a
published fixed-height explicit formula, Huxley's original logarithmic-loss
near-one density estimate, and a multiplicity-compatible local zero count.
It also closes the small-height gap in the Ford zero-free input.

This is not a new density theorem or a new short-interval result.  In
particular, it does not improve Guth--Maynard's (17/30) uniform or (2/15)
almost-all exponents.  Those conclusions still rely on their published
zero-density theorem.

Route A v1 is preserved at
`artifacts/cycle-2-stream-c-route-a-v1.json`; this is a separate v2 artifact.

## Closure record

1. `PROVED` — Near one, use Huxley's original (1.9), as independently
   transcribed and source-checked in `literature-ledger-classical-inputs.md`:
   
   \[
   N(s,T)\ll T^{3(1-s)/(3s-1)}(\log T)^{44},\qquad 3/4\le s\le1.
   \]

   The source convention is two-sided height, matching GM.  On (s\ge4/5),
   (3/(3s-1)\le15/7<30/13), with exact coefficient gap (15/91).  More
   sharply, ((15/7)/(30/13)=13/14).  Therefore at the GM truncation range
   (T\le x^{13/30-o(1)}), Huxley supplies a fixed power margin
   (x^{-1/14+o(1)}), and its ((\log T)^{44}) loss is harmless throughout
   the VK strip.  GM's own theorem covers the remaining range.

2. `PROVED` — Cully-Hugill--Johnston, *International Journal of Number
   Theory* 19 (2023), Theorem 1.2, has been pinned as arXiv:2111.10001v5
   (source SHA-256 `53f5380061ab371849f4805deed7884b887134cc586fbeec18f2ab444cb84953`).
   It gives, at every height satisfying
   \(\max\{51,\log x\}<T<(x^\alpha-2)/2\),
   
   \[
   \psi(x)=x-\sum_{|\gamma|\le T}\frac{x^\rho}{\rho}
      +O^*\!\left(M\frac{x\log x}{T}\right).
   \]

   With (alpha=1/2), GM's selected (T) is admissible eventually.  Apply
   it at (x) and (x+y) with the same (T), then subtract: this yields the
   required half-open interval formula with a stronger error than GM's
   (x(\log x)^3/T).

3. `PROVED` — The same published source's Lemma `plus1minus1lem` gives
   (N(t+1)-N(t-1)<\log t) for (t>1).  The contour proof uses this count in
   its zero sums.  Ford's paper explicitly declares that zero sums count
   multiplicities.  Thus the unit-strip count is compatible with the GM
   pair expansion.  Since
   \(Re(1+z+\overline\rho)\ge1\) for (Re z\ge0), summing the resulting
   (O(\log T)) counts over unit strips at harmonic distance gives
   (O((\log T)^2)), exactly the needed pair-kernel loss.

4. `PROVED` — Ford's Theorem 5 covers (|t|\ge3).  Platt--Trudgian's
   rigorous interval-arithmetic verification gives (eta=1/2) for all
   nontrivial zeros with (|\gamma|\le3\cdot10^{12}).  The ranges overlap,
   so no low-height interval is omitted.

The separately pinned 2024 Cully-Hugill--Johnston II source is useful as an
independent zero-sum cross-check.  `OBSERVED` scope warning: its new theorem
only provides *some* (T^*\in[T,2T]), so it cannot replace the fixed-height
input above.

## Replay

```sh
python3 projects/guth-maynard-zero-density/proof/replay_cycle2_stream_c_route_a_v2.py
python3 -m unittest projects/guth-maynard-zero-density/tests/test_cycle2_stream_c_route_a_v2.py -v
```

The replay checks every frozen source hash, exact Huxley coefficient margin,
source declarations, prior-artifact hash, and its canonical artifact hash.
