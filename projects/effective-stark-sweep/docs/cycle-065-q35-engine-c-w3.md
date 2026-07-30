# Cycle 065 — first generic Engine-C W3 theorem

**Claim tag:** `VERIFIED`

The first generic Engine-C closure is complete.

For \(K=\mathbb Q(\sqrt{35})\), the primitive modulus with finite HNF
`[[8,4],[0,4]]` and norm 32 has two independent linear-reinduction
routes, over \(\mathbb Q(\sqrt{-10})\) and
\(\mathbb Q(\sqrt{-14})\).  Each has \(e=2\), \(|S|=3\), the exact
selected quartic character, a certified primitive \(L'\) target, and
the same isolated anti-unit orbit.

The exact normal-closure bridge identifies the separator prime
\(5\), proves that the selected cyclic generator is its Frobenius,
checks the dihedral relation with complex conjugation, and emits the
four Artin-labeled positive norms.  Both routes give the identical
packet polynomial
\[
\begin{aligned}
x^8&-38904x^7+905404x^6+62136x^5-873210x^4\\
   &\quad+62136x^3+905404x^2-38904x+1.
\end{aligned}
\]
The polynomial generates the frozen real selector field; the two
route computations share no unit-lattice or normal-closure
intermediate.

## Normalization formulas

Put \(\ell_g=\log|g\varepsilon|_{\rm ord}\).  The class-log formula
and its inverse are
\[
\zeta'_S(0,g)=-\frac2e\ell_g,
\qquad
\ell_g=-\frac e2\zeta'_S(0,g).
\]
For the primitive quartic convention
\(\overline{\psi(\sigma)}=-i\), anti-unit symmetry gives
\[
L'_S(0,\psi)=-\frac4e(\ell_1-i\ell_\sigma),
\qquad
\ell_1-i\ell_\sigma=-\frac e4L'_S(0,\psi).
\]
Thus \(2/e\) and \(4/e\) are forward coefficients; \(-e/2\) and
\(-e/4\) are inverse recovery coefficients.  The \(e=2\) Paper-II
class-log anchor cannot by itself distinguish \(2/e\) from the
unsigned inverse magnitude \(e/2\).  RQ-000458 supplies the
nontrivial \(e=4\) cross-route normalization check, while the present
two-base case validates the generic direct-\(L'\), orbit, and bridge
path.

## Root reality

The exact bridge proves that the four Artin-labeled norm classes are
fixed by the chosen conjugation.  Arb evaluation at every compatible
normal-field embedding matches them bijectively to the four real
roots of the packet polynomial.  The remaining four roots form two
nonreal conjugate pairs, so the packet has signature \([4,2]\).

This is the first mixed-signature packet produced by the generic
Engine-C tranche.  It is not the first mixed-signature packet in the
full proved corpus: the prior B packets and RQ-000458 already have
mixed signature.  The root audit is
`artifacts/engine-c-packet-root-reality-v1.json`.

The frozen member audit transports this primitive packet separately
to RQ-001280 (norm 32) and RQ-001297 (norm 64).  Both are `VERIFIED`.
The earlier Cycle-060 boundary remains preserved as the pre-generic-W3
state.

Seal: `artifacts/engine-c-w3-tranche-01-verified-v1.json`.
