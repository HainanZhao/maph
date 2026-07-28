# SIC--Stark research cycle 57: the dimension-seven field collapse

## Outcome

The finite dimension-seven cancellation is now exact.

The sixteen Zauner-orbit values split into three signed class
polynomials:

\[
\begin{aligned}
H(T)={}&T^{24}-8T^{23}+6T^{22}+100T^{21}-336T^{20}
 +264T^{19}+834T^{18}-2980T^{17}\\
&+5038T^{16}-5748T^{15}+5084T^{14}-4060T^{13}
 +3611T^{12}+\cdots+1,\\
P_+(T)={}&T^4-2T^3-5T^2-2T+1,\\
P_-(T)={}&T^4-4T^3+4T^2-4T+1.
\end{aligned}
\]

The twelve real roots of \(H\) are exactly the twelve signed
nonquadratic overlap representatives.  The positive real roots of
\(P_+\) and \(P_-\) give the remaining four representatives.  Exact
subfield tests place both quartic fields inside the field defined by
\(H\).

The field \(H\) has degree \(24\) over \(\mathbf Q\).  Its compositum
with \(\mathbf Q(\zeta_{56})\) has degree only \(48\), not the naive
multiquadratic degree.  Its degree-\(12\) intersection is selected
exactly: the inclusion of
\(\mathbf Q(\zeta_{56}+\zeta_{56}^{-1})\) whose generator lies in
\((1.98,1.99)\) is isolated by Sturm's theorem, and the two images of
that generator are required to agree in the compositum.  This replaces
the former numerical component choice.  The resulting compositum is
the already known normal closure of the one-place Stark field, and
also satisfies the exact compatibility
\[
 \sqrt2=\zeta_{56}^{7}+\zeta_{56}^{-7}.
\]

Inside this single degree-\(48\) field, exact Weyl reconstruction gives,
for each of the two formal shifts,

\[
\operatorname{Tr}K=1,\qquad K^2=K,
\]

and all \(441\) rank-two minors vanish.  Thus both shifted matrices have
rank exactly one.  The computation is reproduced by
`scripts/dimension_seven_exact_tcc.gp`.

## Analytic-to-algebraic progress

The squared overlaps have the reciprocal relative polynomial

\[
\begin{aligned}
P(X)={}&X^{16}-(37+28\sqrt2)X^{15}
 +(1212+854\sqrt2)X^{14}\\
&-(20685+14630\sqrt2)X^{13}+\cdots+1.
\end{aligned}
\]

It factors over \(\mathbf Q(\sqrt2)\) with degrees \(2,2,12\).  Exact
field comparisons identify these factors with the two quadratic
conductor-lowered ray fields and the full one-place ray-\(14\) field.
Sturm certificates isolate all sixteen real roots.

Arb interval integration certifies the eight independent positive
Shintani values against the designated roots.  At tolerance
\(10^{-10}\), the maximum logarithmic error is below
\(5.9\cdot10^{-11}\).

For the full normal closure:

\[
\operatorname{Gal}(N/K)\simeq C_6\times C_2\times C_2,
\qquad
N^{[\operatorname{Gal}(N/\mathbf Q),\operatorname{Gal}(N/\mathbf Q)]}
\simeq\mathbf Q(\zeta_{56}).
\]

Over \(k=\mathbf Q(\sqrt{-7})\), the extension is abelian with conductor

\[
\mathfrak c=\mathfrak p_2^3\bar{\mathfrak p}_2^3\mathfrak p_7
=
\begin{pmatrix}56&32\\0&8\end{pmatrix}.
\]

Auditing all \(32\) ideal divisors of \(\mathfrak c\) gives the safe
Shintani exponent

\[
m=16128.
\]

Here Shintani's factor
\(w(\mathfrak d)=\#\{\epsilon\in\mathcal O_k^\times:
\epsilon\equiv1\pmod{\mathfrak d}\}\) is computed from the ideal
congruence for every divisor.  It equals \(2\), rather than \(1\), for
the trivial divisor and three divisors supported to first order above
\(2\).  Correcting these three nontrivial cases changes their individual
clearing exponents but leaves the least common multiple \(16128\)
unchanged.  The real \(X\)-to-\(Y\) induction adds no hidden product of
indices: along nested moduli the ray-order ratios telescope.

With the tightened Arb bound,

\[
16128\epsilon<9.5\cdot10^{-7},
\]

well below Voutier's height gap
\(5.22\cdot10^{-5}\) for degrees \(3\) through \(24\).

## Machinery assessed

The successful proof stack is:

1. conductor lowering and exact ray groups;
2. Shintani's index-two theorem through the imaginary quadratic field
   \(\mathbf Q(\sqrt{-7})\);
3. Arb interval quadrature with explicit endpoint and tail bounds;
4. Sturm root isolation;
5. Voutier height rigidity;
6. exact subfield embeddings and Galois conjugates;
7. a degree-\(48\) compositum certificate for the Weyl reconstruction.

Other possible tools were considered:

- unit-log lattices and regulator bounds can replace Voutier when the
  safe exponent becomes too large;
- group-ring annihilators can compress the Shintani denominator audit;
- Baker-type linear-form bounds are available but unnecessarily heavy;
- a direct multivariate Gröbner certificate is possible, but the
  degree-\(48\) field collapse makes it inferior here.

## Artin bridge

The label ambiguity is also closed.  The split prime above \(17\) with ray
log \([1,0]\) acts by automorphism \(5\) in PARI's exact
`nfgaloisconj` list, while the split prime above \(41\) with ray log
\([0,1]\) acts by automorphism \(10\).  Local Frobenius congruences identify
both automorphisms exactly.

An additional exact check constructs the one-place ray-\(14\) field from
class field theory, retains its labeled copy of \(\sqrt2\) through
`rnfequation`, and finds all \(12\) isomorphisms from \(H\) to that
field.  Every one preserves the labeled base field.  Thus the
Frobenius calculation is attached to the intended extension over
\(\mathbf Q(\sqrt2)\), not merely to an abstract degree-\(24\) field.

The projection from the ray-\(14\) group to the ray-\(7\) group is

\[
  C_6\times C_2\longrightarrow C_6,\qquad
  (a,b)\longmapsto 2a+3b.
\]

For each of the twelve nonquadratic characteristic representatives, the
class of its ray-\(7\) factor equals the base class plus this projection of
the ray-\(14\) class.  Applying the two exact Frobenius generators sends the
base root \(2.429812\ldots\) into the rational isolating interval assigned
to that characteristic.  The two quadratic strata are similarly labeled:
class \(0\) gives the large root and class \(1\) its reciprocal small root.
The complete calculation is
`scripts/dimension_seven_artin_labels.gp`.

Consequently, height rigidity identifies the entire analytic packet with
the exact signed roots used by the finite certificate.  The finite
compositum selection, base-field labeling, and both TCC shifts now have
exact certificates.  The remaining work is exposition and adversarial
audit of the Shintani denominator argument, not a missing mathematical
construction.
