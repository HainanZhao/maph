# Cycle 019 — uniform Engine-A theorem

## Statement

Let \(K\) be real quadratic and let
\(\mathfrak m=\mathfrak f\infty_2\). Suppose every character in the
exact Fourier support of \(1-R\) has order at most two. For each
supported quadratic character \(\chi\), let \(L_\chi/K\) be its
quadratic ray field, \(I_\chi\) the exact relative-unit index, and
\(u_\chi\) a positive relative unit completing the image of
\(\mathcal O_K^\times\) in the free unit lattice of \(L_\chi\).
Then

\[
 L'_S(0,\chi)=
 E_\chi\,
 \frac{h_{L_\chi}}{h_K}
 \frac{w_K}{w_{L_\chi}}
 \frac{2}{I_\chi}\log|u_\chi|,
\]

where \(E_\chi\) is the exact product of the imprimitive Euler factors
at zero. If an omitted Euler factor vanishes, that character contributes
zero to the first derivative. Fourier inversion therefore expresses
every differenced derivative as a rational linear combination of
logarithms of explicitly computed relative units. Clearing the exact
denominators proves a packet of algebraic units/radicals.

## Why this is uniform

The proof is the analytic class-number formula applied to
\(\zeta_{L_\chi}/\zeta_K\), followed by exact ray-character Fourier
inversion. The relative regulator identity is uniform:

\[
 \frac{R_{L_\chi}}{R_K}=\frac{2}{I_\chi}\log|u_\chi|.
\]

In rank two, \(I_\chi\) is obtained exactly from the unit-coordinate
lattice. If the embedded fundamental unit of \(K\) has coordinate
vector \((a,b)\) in a fundamental-unit basis of \(L_\chi\), the
saturation/index contribution is \(\gcd(a,b)\), with the oriented
complement selected by Bézout and the required real embedding.

Thus the theorem is single and uniform. What remains case-dependent is
finite verification data—class numbers, character conductors, Euler
factors, unit coordinates, and orientation—not a new proof.

## Boundary

The 5,459 structural A rows have not all been promoted. Empty-support
rows must first be collapsed to the trivial packet, duplicate
quadratic fields must be deduplicated, and every nontrivial row must
emit the exact index/orientation record above. The A bulk is therefore
a verification campaign under this theorem, not 5,459 independent
arguments.
