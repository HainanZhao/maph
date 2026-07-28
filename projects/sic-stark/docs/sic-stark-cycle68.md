# SIC--Stark research cycle 68: fixed-point divisibility as the north-star lemma

## Five-cycle conclusion

Cycles 64--67 changed the dimension-six proof target substantially:

1. even-dimensional Weyl wrap signs reduce the defect to thirteen
   signed Zauner representatives;
2. the singular \(q\)-gamma orders and gamma factors cancel exactly;
3. the nonsingular characteristic requires a moving-argument
   Euler--Maclaurin half-power;
4. after that correction the full defect is \(O(n^{-2})\), not
   \(O(n^{-1})\); and
5. the defect divided by the distance to the RM fixed point converges to
   a finite derivative packet.

The full dimension-six theorem is not yet proved.  The new evidence
isolates a much smaller analytic statement than the mixed-signature
Stark algebraicity conjecture.

## Fixed-point divisibility proposal

Let \(K_d(\tau)\) denote the off-shell ghost matrix reconstructed from
the convention-matched Shintani--Faddeev characteristic cocycles, and
let \(A_d=L_d^3\).  The natural general target is:

> **Fixed-point divisibility.**  In a one-sided neighborhood of an RM
> fixed point \(\beta_d\), every entry of
> \[
> K_d(\tau)^2-K_d(\tau)
> \]
> is divisible, in the local meromorphic ring, by
> \[
> A_d\tau-\tau.
> \]

Since \(A_d\beta_d=\beta_d\), this would immediately give

\[
 K_d(\beta_d)^2=K_d(\beta_d).
\]

Together with the exceptional zero-characteristic normalization and
nonvanishing, this is precisely the rank-one idempotent/TCC mechanism.

For dimension six,

\[
 A=\begin{pmatrix}115&-24\\24&-5\end{pmatrix}
\]

and the normalized defect packet computed in cycle 67 is the numerical
first derivative predicted by this lemma.

## Cycle-69 correction

Cycle 69 proves that, for the dimension-six stabilizer,

\[
 A\tau-\tau
 =-24\frac{\tau^2-5\tau+1}{24\tau-5}
\]

has a simple zero at \(\beta\).  Thus it generates the same local ideal as
\(\tau-\beta\).  Divisibility of a holomorphic defect entry by
\(A\tau-\tau\) is therefore equivalent to its vanishing at \(\beta\).

The proposal below remains a useful reformulation, but it is not a weaker
route around TCC or the primitive special-value identity.

## Why the formulation remains useful

The divisibility statement:

- uses only local cocycle analysis near the real multiplication point;
- does not require proving algebraicity of the mixed-signature Stark
  unit;
- is directly phrased in the finite Weyl algebra underlying TCC; and
- has a plausible uniform formulation in \(d\).

It aligns with the finite Weyl formulation of the north-star goal, but
proving it in dimension six has exactly the same constant-term content as
proving TCC.

## Concrete next proof program

For the thirteen dimension-six representatives:

1. write the defect coefficient as a finite sum of products of
   characteristic cocycles;
2. substitute the complete residue-class expansion, including the
   \(q\)-gamma and moving half-power terms;
3. group terms in signed Zauner triples;
4. prove cancellation of the constant term;
5. bound the remaining term by \(C|A\tau-\tau|\).

The cyclic pentagon identity may help with step 4 only after lifting both the
order-\(n\) cyclic phase and the level-six Weyl phase to a common root
system and matching its coefficient constraints.  Without that parameter
match, it merely repackages the missing identity.

## Theorem status

\[
\boxed{\text{Dimension six remains open, but its analytic boundary is
now a thirteen-equation local divisibility problem.}}
\]

This is the strongest and most generalizable formulation reached in the
five cycles.
