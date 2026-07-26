# Stage 8: challenge the conjecture and its entropy heuristic

## Cycle 1 — search for an actual counterexample

### Assumption challenged

The reciprocal-threshold conjecture may be a finite-range illusion. The
previous searches were linear in \(t\), so large prime-power examples were
mostly inaccessible.

### Work

The new exact routine `search_near_multiple_via_smallest_box` enumerates the
smallest Lucas digit box, keeps only values divisible by the complementary
factor \(u_p\), and tests those multipliers in every other prime base. Unit
tests cross-check it against exhaustive near-multiple analysis for every
prime predecessor \(M<100\).

For the kernel \(2\cdot3\cdot5\):

- exponent cube \(1\leq\alpha,\beta,\gamma\leq15\);
- box limit 500,000;
- 400 cases completely resolved;
- 46,721 compatible candidate multipliers tested;
- no witness found;
- largest completely resolved \(M\) was \(2,187,000,000\).

Additional barely-supercritical kernels were searched with box limit
200,000:

| Prime kernel | Complete exponent cases | Compatible candidates | Witnesses |
|---|---:|---:|---:|
| \(2,3,7,41\) | 72 | 638 | 0 |
| \(2,3,11,13\) | 90 | 504 | 0 |
| \(2,5,7,11,13\) | 36 | 140 | 0 |

These are finite exact searches and do not establish the conjecture.

## Cycle 2 — challenge raw box entropy

### Assumption challenged

Perhaps the interval length times the product of box densities,
\[
E(M)=\left\lfloor\frac{M-1}{2}\right\rfloor
\prod_{p\mid M}\frac{|\mathcal T_p|}{Q_p},
\]
acts like a deterministic expected number of witnesses.

### Falsification

It does not. Two known witness cases have
\[
E(2088)=\frac{182525}{1546823547}
\approx1.18\cdot10^{-4},
\]
and
\[
E(36138)=
\frac{1591805254400}{768805988386795389}
\approx2.07\cdot10^{-6}.
\]
Despite these values being far below \(1\), the respective witnesses
\(t=13\) and \(t=4\) exist.

The digit boxes are strongly arithmetically correlated with the short
integer interval. An independence heuristic may guide experiments, but it
cannot prove absence.

## Cycle 3 — isolate the real bottleneck

Large boxes often contain very few multiples of their complementary factor.
Examples:

- \(M=2088\): a box of size 1,024 leaves 3 compatible multipliers and one
  full witness;
- \(M=36138\): a box of size 139,968 leaves 5 compatible multipliers and one
  full witness;
- \(M=63150\): a box of size 559,872 leaves 9 compatible multipliers and no
  witness;
- \(M=1806\): the smallest box has size 84 but leaves no positive compatible
  multiplier.

Proposition 21 expresses this divisibility-filtered count exactly as a
roots-of-unity sum of a digit-box polynomial. The nontrivial character
terms, rather than raw entropy, govern the sparsity.

## Strategic conclusion

The reciprocal-threshold conjecture survived the new adversarial search,
but two proposed proof shortcuts did not:

1. no fixed digit depth works;
2. raw box entropy does not exclude witnesses.

The next plausible analytic target is a character-sum statement:

> Use negative defect to force enough cancellation, or a sufficiently
> unfavorable residue bias, in at least one digit-box polynomial.

Because witnesses also occur when defect is positive, any such estimate
must use the sign of the defect in an essential way rather than merely the
size of \(M\) or the number of digits.

**Later correction:** Stage 9 falsifies the proposed one-box cancellation
target at \(M=2952450\). The decisive character interaction can be genuinely
multi-base.
