# Stage 9: from one-box bias to genuine multi-base interaction

## Cycle 1 — expose an exact symmetry

Proposition 22 proves that every Lucas digit box is invariant under
\[
b\longmapsto A_p-b.
\]
For compatible multipliers this is
\[
t\longmapsto M-1-t.
\]
When \(M\) is even, the total compatible count in a box is exactly twice
the positive half-interval count plus the endpoint pair. This both explains
and independently checks the half-range search.

## Cycle 2 — challenge the single-box cancellation target

### Assumption challenged

Perhaps negative reciprocal defect forces a large nontrivial character sum
in at least one box, leaving very few compatible multiples.

### Falsification

For
\[
M=2\cdot3^{10}\cdot5^2=2952450,
\]
the reciprocal defect is \(-1\). Its pivot base is \(3\), with:

\[
|\mathcal D_3|=419904,\qquad u_3=50.
\]
The entropy main term predicts
\[
\frac{419904}{50}=8398.08
\]
compatible values, while the exact count is \(8390\). The relative
discrepancy is less than \(0.1\%\), yet there is no common witness.

In the positive-defect witness example \(M=36138\), the same calculation
predicts about \(11.62\) values and gives exactly \(12\). One of its five
positive half-interval candidates survives every other base.

Therefore negative defect does not force strong cancellation in a single
box. The obstruction can arise only after bases interact.

## Cycle 3 — challenge pairwise sufficiency

### Assumption challenged

Perhaps every supercritical cover is already certified by two prime bases.

### Falsification

At
\[
M=4500=2^2\cdot3^2\cdot5^3,
\]
each pair has a surviving multiplier:

\[
\begin{array}{c|c}
\text{bases}&\text{survivor}\\ \hline
\{2,3\}&2\\
\{2,5\}&71\\
\{3,5\}&123
\end{array}
\]

but no multiplier passes all three. The same three-way phenomenon occurs
at \(M=2400\).

Define the **Lucas cover degree** \(\lambda(M)\) to be the smallest number
of prime bases whose pass sets already have empty intersection. An
exhaustive scan of reciprocal-supercritical \(M\leq10000\) found:

| \(\lambda(M)\) | Count |
|---:|---:|
| 1 | 243 |
| 2 | 176 |
| 3 | 2 |

The degree-three examples are \(M=2400,4500\). No common witness was found.
This is a finite computational observation.

## Cycle 4 — move Fourier analysis to the full intersection

Proposition 23 gives an exact Fourier expansion for the witness count
\[
W(M)=\sum_{t=1}^{\lfloor(M-1)/2\rfloor}
\prod_{p\mid M}1_{\mathcal T_p}(t).
\]
Its zero-frequency term is the box-entropy heuristic. All other terms mix
frequencies from one or more prime bases.

The examples now establish a hierarchy:

1. one-base character bias is insufficient;
2. pairwise intersections are sometimes insufficient;
3. genuine three-base interaction can be decisive.

This suggests grouping the Fourier expansion by **support size**—the number
of bases with nonzero frequency. The Lucas cover degree measures the
set-theoretic counterpart of that interaction order.

## Next repetition

The next assumptions to challenge are:

1. Is \(\lambda(M)\leq3\) for all reciprocal-supercritical \(M\), or do
   four-way obstructions occur?
2. Does negative defect force a low-support Fourier certificate even when
   it does not force one-box cancellation?
3. Can the reciprocal identity itself select a small subset of prime bases
   with an empty pass intersection?

Finding a degree-four example would prevent another premature simplification.
Proving a universal degree bound would reduce the global conjecture to
low-dimensional digit interactions.
