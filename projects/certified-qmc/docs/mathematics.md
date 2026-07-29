# Mathematical freeze

Date: 2026-07-29

## 1. Certified object

The Phase-0 engine certifies the product-weight, \(\beta=0\) case of
the shift-averaged unanchored Sobolev formula
\[
 e^2(z,N)=-1+\frac1N\sum_{k=0}^{N-1}
 \prod_{j=1}^d
 \left(1+\gamma_jB_2(\{kz_j/N\})\right),
\tag{1}
\]
where
\[
 B_2(x)=x^2-x+\frac16.
\]
This is equation (5.13) of Dick--Kuo--Sloan after selecting the
unanchored value \(\beta=0\).

The engine calls (1) the `DKS2013-eq5.13-beta0-product-B2`
convention. This name appears in every certificate.

## 2. Why the result is rational

Let \(r\equiv kz_j\pmod N\), \(0\le r<N\). Then
\[
 B_2(r/N)=
 \frac{6r^2-6rN+N^2}{6N^2}.
\tag{2}
\]
If \(\gamma_j=a_j/b_j\) is in lowest terms, then
\[
 1+\gamma_jB_2(r/N)
\]
has denominator dividing \(6b_jN^2\). Consequently the reduced
denominator of (1) divides
\[
 D(N,\gamma)
 =N\prod_{j=1}^d(6b_jN^2)
 =6^dN^{2d+1}\prod_{j=1}^db_j.
\tag{3}
\]

The proposal's shorter expression \(6^dN^{2d+1}\) is correct only
when every normalized weight is integral. Certificate replay verifies
the divisibility in (3).

## 3. Normalization boundary

The Fourier series identity is
\[
 B_2(x)=\frac1{2\pi^2}
 \sum_{h\in\mathbb Z\setminus\{0\}}
 \frac{e^{2\pi ihx}}{h^2}.
\]
Some Korobov conventions therefore use \(2\pi^2B_2\). Absorbing that
factor into \(\gamma_j\) changes what a stated weight means. Phase 0
does not accept a convention-free weight file: a future importer must
declare and convert its source convention explicitly.

The proposed polynomial-in-\(\pi^2\) mode is deferred until a source
format and exact coefficient semantics are frozen.

## 4. Independent reduction check

The generic shift-invariant RKHS expression contains a double sum over
point pairs. For a rank-1 rule, each modular difference \(i-k\) occurs
exactly \(N\) times, reducing it to (1). The implementation keeps an
independent \(O(N^2d)\) double-sum oracle and compares it to the
single-sum engine on small instances. This guards the bridge rather
than merely retesting the same loop.

## 5. Forced CBC symmetry

Because \(B_2(x)=B_2(1-x)\), replacing a candidate component \(z\) by
\(N-z\) leaves every score unchanged. Therefore an unquotiented CBC
search has structural exact ties. Phase 0 searches the representatives
\[
 \min(z,N-z),\qquad z\in(\mathbb Z/N\mathbb Z)^\times.
\]
The proposal's raw expectation that fewer than \(0.1\%\) of comparisons
need tie handling was not meaningful before this quotient. Cycle 009
now freezes a new, measurable predicate after the quotient: fewer than
\(0.1\%\) of the deterministic tournament comparisons may escalate
through double-double and Arb to exact CRT. Exact post-quotient
equalities count in that rate and are also reported separately.

## 6. Corrected reference-scale arithmetic

Taking logarithms in the master denominator (3) gives the exact design
term
\[
 \log_2 D
 =d\log_2 6+(2d+1)\log_2N
   +\sum_{j=1}^d\log_2\operatorname{den}(\gamma_j).
\tag{4}
\]
Thus rational-weight denominators are not optional headroom. For
\(\gamma_j=j^{-2}\),
\[
 \sum_{j=1}^d\log_2\operatorname{den}(\gamma_j)
 =2\sum_{j=1}^d\log_2j
 =2\log_2(d!).
\tag{5}
\]
At \(d=50\), this contributes approximately 428.416 bits. This
reconciles the rough integral-weight estimate near 1,810 bits with the
proved Cycle-009 budgets: 2,162 product bits for the final candidate
difference and 2,176 for the final merit. The latter bounds include
the numerator magnitude as well as the master denominator.

For integral normalized weights, \(N=2^{20}\), and \(d=100\), (3) has
bit length
\[
 \operatorname{bitlen}\!\left(N(6N^2)^{100}\right)=4279.
\]
Representing that denominator alone needs at least 70 distinct 62-bit
moduli or 139 distinct 31-bit moduli. The proposal's 4,743-bit/77-prime
figure is a safe-looking overestimate but is not the exact consequence
of its stated formula.

More importantly, denominator bits do not by themselves bound the
balanced integer reconstructed when comparing two candidate scores.
A proved numerator/difference bound is required before the CRT prime
schedule can be frozen. That derivation is a Phase-1 gate.

## 7. What a certificate proves

A `VERIFIED` core certificate proves:

- the input was interpreted in the named convention;
- the exact reduced fraction equals (1);
- its denominator divides (3);
- the exact sequence of product summands has the recorded SHA-256;
- deterministic replay reproduces the complete payload.

It does not prove:

- a bound for a particular integrand;
- optimality of the generating vector;
- correctness of an upstream table beyond the vendored components;
- any randomized confidence statement;
- any production-scale performance claim.
