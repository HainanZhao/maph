# SIC bridge extraction

Recorded: 2026-07-31 UTC

## Universal supplied-tuple layer

The dimension-four and dimension-five proofs use the same exact
arithmetic once a positive stabilizer
\(A=(\begin{smallmatrix}a&b\\c&d\end{smallmatrix})\) and a lifted
characteristic \(\boldsymbol r=(r_1,r_2)^T\) are supplied:

\[
\Psi(A)=\Phi(A)-3\,\operatorname{sgn}(c(a+d)),
\]

\[
t_A(\boldsymbol r)=\frac12\left\{
(c-d+1)r_1+(-a+b+1)r_2-cd r_1^2
+2(a-1)d r_1r_2-(a-2)b r_2^2\right\},
\]

and the Kopp multiplier has exponent

\[
-\Psi(A)/12-t_A(\boldsymbol r)\pmod{\mathbf Z}.
\]

This arithmetic is implemented independently in `src/cocycle.py`.
It replays:

- the dimension-four values \(\Psi=0\), \(t=1/4\), total exponent
  \(3/4\);
- the dimension-five value \(\Psi=3\) and all 24 positive-lift
  identities \(t=(p^2-4pq+q^2)/5\);
- the archived invariant values \(0,9,0\) for the dimension-seven
  discriminant-8, dimension-seven discriminant-32, and dimension-eight
  discriminant-5 stabilizers.

## Non-universal inputs

The formulas do not construct their own inputs. Across the anchors,
those inputs arise differently:

- dimension 4: a singled-out identity ray class and characteristic
  \((0,1/4)\);
- dimension 5: the SIC form supplies the characteristic, while a
  positivity inequality selects an integral lift separately for each
  of 24 classes;
- dimension 7, discriminant 32: a determinant-two conductor-lowering
  map produces two preimages before the inverse ray map and gcd
  reduction;
- dimension 8, discriminant 45: the relevant phase information passes
  through a three-factor conductor-lowering dictionary and two distinct
  CM characters;
- dimension 8, discriminant 5: phase selection uses a six-factor
  continued-fraction cocycle and exact sign audit.

Thus the common object is a supplied-tuple evaluator, not a canonical
map from a ray character to one tuple.
