# P7-3 — fixed-ray coloured Fourier diagonalization and completion barrier

## Boundary and outcome

PROVED: at one fixed finite ray modulus \(\mathfrak f\), the complete
ray-class character group gives an exact unitary Fourier diagonalization of
the common-ideal Gram matrix. It also gives an exact coloured cubic trace and
coloured additive-energy identity for a selected joint \((\chi,t)\) sample.
The transform itself has no norm loss, and the selected Gram trace remains
positive semidefinite.

PROVED: the actual primitive/partial sample is represented after that
transform by a generally non-diagonal orthogonal projection. Completing it
to all characters can introduce a sharp factor

\[
 \kappa_{\mathfrak f}(W):=
 \frac{|X(\mathfrak f)|\,|\pi_t W|}{|W|}\in[1,|X(\mathfrak f)|],
\]

and a trace-monotonicity comparison loses the diagonal cancellation on which
the Guth--Maynard cubic argument relies. Fibrewise height separation alone
does not bound \(\kappa_{\mathfrak f}(W)\) by a subpower.

PROVED: a coloured energy identity removes one formal character sum, but
fibrewise separation alone still permits its maximal cubic scale. These are
scoped algebraic/combinatorial statements. They prove no P7 large-value,
zero-density, detector, or prime-ideal theorem, and do not rule out a new
coloured primitive cubic estimate.

This is research-stage source/algebra/replay work only. No hostile audit is
initiated.

## Fixed-modulus coloured Gram and cubic trace

Fix \(\mathfrak f\), write

\[
 G=\operatorname{Cl}(\mathfrak f),\qquad X=\widehat G,
 \qquad H=|G|=|X|,
\]

and retain the P7 zero extension. Thus only ideals coprime to
\(\mathfrak f\) enter the following formulas. Let \(c(\mathfrak a)\) be one
common coefficient function and put

\[
 u(\mathfrak a)=|c(\mathfrak a)|^2w(N\mathfrak a/N)^2.
\]

For a finite selected sample \(W\subset X\times\mathbb R\), define the
coloured Fourier sum

\[
 \mathcal R_W(g;v)=
 \sum_{(\chi,t)\in W}\chi(g)v^{it}
 \qquad(g\in G,\ v>0).
\]

The common-ideal Gram kernel is

\[
 K_{xy}=\sum_{\mathfrak a}u(\mathfrak a)
 \chi_x(\mathfrak a)\overline{\chi_y(\mathfrak a)}
 (N\mathfrak a)^{i(t_x-t_y)}.
\]

PROVED: summing the labels first gives the exact coloured cubic identity

\[
\begin{aligned}
 \operatorname{tr}(K^3)=\sum_{\mathfrak a,\mathfrak b,\mathfrak c}
 u(\mathfrak a)u(\mathfrak b)u(\mathfrak c)
 &\mathcal R_W([\mathfrak a][\mathfrak c]^{-1};
                  N\mathfrak a/N\mathfrak c)\\
 &\times\mathcal R_W([\mathfrak b][\mathfrak a]^{-1};
                  N\mathfrak b/N\mathfrak a)\\
 &\times\mathcal R_W([\mathfrak c][\mathfrak b]^{-1};
                  N\mathfrak c/N\mathfrak b).
\end{aligned}
\]

There is no \(H\)-factor in this algebraic regrouping. The prior P7-3
labelled-ideal trace is recovered by expanding the three \(\mathcal R_W\)'s.
The replay verifies the identity on a formal exact
\(G=\mathbb Z/2\mathbb Z\) model with two distinct ideals of the same class
and unequal fibres.

## Complete-group diagonalization and the primitive selection projector

Let \(\mathcal T\) be a finite time grid and first use every character in
\(X\). For the full design matrix \(M\), indexed by
\(X\times\mathcal T\) and ideals, use the unitary character Fourier transform

\[
 U_{g,\chi}=H^{-1/2}\overline{\chi(g)}.
\]

PROVED: character orthogonality gives

\[
 (UM)_{(g,t),\mathfrak a}
 =H^{1/2}c(\mathfrak a)w(N\mathfrak a/N)
   (N\mathfrak a)^{it}\mathbf1_{[\mathfrak a]=g}.
\]

Hence, with \(C_g\) the time Gram matrix formed only from ideals in ray class
\(g\),

\[
 U(MM^*)U^*=H\bigoplus_{g\in G}C_g.
\]

For a selected sample \(W\), let \(A_t=\{\chi:(\chi,t)\in W\}\), let
\(P_W\) be row selection before the transform, and set \(B=UP_WU^*\). Its
exact entries are

\[
 B_{(g,t),(h,s)}=\mathbf1_{t=s}\frac1H
 \sum_{\chi\in A_t}\chi(hg^{-1}),
\]

and therefore

\[
 \operatorname{tr}(K_W^3)
 =H^3\operatorname{tr}\!\left[
 B\Bigl(\bigoplus_{g\in G}C_g\Bigr)B\right]^3.
\]

PROVED: \(B\) is an orthogonal projection. Thus the entire selected trace
is nonnegative, and compression does not create a sign problem at that
level. However, \(B\) is diagonal in the ray-class variable if and only if
each \(A_t\) is either empty or all of \(X\). This follows by Fourier
inversion: all nonidentity Fourier coefficients of \(\mathbf1_{A_t}\) vanish
only when that indicator is constant.

The selected P7 labels are primitive exact-conductor characters, generally a
proper subset of \(X\), and primitive labels are not a character group.
Consequently, even a sample containing every primitive character at a fixed
time generally has a non-diagonal \(B\). Replacing it by the full ambient
group is algebraically legitimate only as a completion/compression device;
it does not turn the newly added imprimitive rows into large values.

When \(W=X\times S\) with \(S\) globally separated, \(B\) is block diagonal
and the identity becomes

\[
 \operatorname{tr}(K_W^3)=H^3\sum_{g\in G}
 \operatorname{tr}\bigl(C_{g,S}^3\bigr).
\]

PROVED: at the diagonal scale this has no residual character loss. If every
ray class has mass \(N/H\) and \(|S|=r\), then the diagonal cubic term is

\[
 H^3\cdot H\cdot r(N/H)^3=HrN^3=|W|N^3,
\]

exactly the standard total-sample normalization. A new ideal-class
Poisson/affine estimate would still be required for the off-diagonal terms.

## Coloured additive energy and its sharp fibre-spacing limit

For integral discretized times, define

\[
 E^{=}_{\rm col}(W)=
 \#\{(x_1,x_2,x_3,x_4)\in W^4:
 t_1+t_2=t_3+t_4,\ 
 \chi_1\chi_2=\chi_3\chi_4\}.
\]

PROVED: complete-character Parseval gives

\[
 E^{=}_{\rm col}(W)=\frac1H\sum_{g\in G}\int_0^1
 \left|\sum_{(\chi,t)\in W}\chi(g)e(t\theta)\right|^4d\theta.
\]

For real times, let \(E^\Delta_{\rm col}(W)\) use
\(|t_1+t_2-t_3-t_4|\le\Delta\) with the same colour equation. If each
individual character fibre is \(\delta\)-separated, then

\[
 E^\Delta_{\rm col}(W)\le
 \left(\left\lfloor\frac{2\Delta}{\delta}\right\rfloor+1\right)|W|^3.
\]

Indeed, after \(x_1,x_2,x_3\) are fixed, the colour of \(x_4\) is fixed and
its time lies in one interval of length \(2\Delta\).

This cubic bound is sharp in its exponent. For \(W=X\times\{0\}\), every
fibre has one point, but

\[
 E^{=}_{\rm col}(W)=H^3=|W|^3.
\]

More generally, for \(W=X\times\{1,\ldots,r\}\),

\[
 E^{=}_{\rm col}(W)=H^3\frac{2r^3+r}{3}.
\]

The \(H^{-1}\) Parseval average is exactly cancelled by coherent mass in the
identity ray class. Thus fibrewise spacing alone cannot give a fixed power
saving over maximal coloured energy. This is a barrier only to a
coloured-energy-only replacement of the Guth--Maynard \(S_3\) argument; it
does not exclude the complete-group block route above or another
character-aware method.

The pinned Guth--Maynard refined bound contains

\[
 T^2|W|^{3/2}+TN|W|^{1/2}E(W)^{1/2}.
\]

PROVED: substituting the permitted maximal scale
\(E^\Delta_{\rm col}(W)\asymp|W|^3\) gives the maximal-energy term
\(TN|W|^2\); no fixed energy saving follows from fibrewise spacing. No
numerical P7 density-exponent loss is asserted, because P7 has no detector,
coloured \(S_3\), or conductor/height transfer theorem yet.

## Completion factor and the trace-cancellation barrier

The smallest full-character completion using precisely the observed time
projection has \(|X|\,|\pi_tW|\) rows. Its exact relative size is the
\(\kappa_{\mathfrak f}(W)\) displayed in the boundary. It equals \(1\) for
a colour-complete sample and can equal \(H\) even if every fibre contains
just one globally separated point: take

\[
 W=\{(\chi_j,3j):j\in\mathbb Z/H\mathbb Z\}.
\]

PROVED: mere trace positivity cannot remove this completion factor after the
source's diagonal cancellation. In the exact diagonal model
\(A=N I_m\), select \(R\) of \(m=\kappa R\) rows. The selected cubic excess
is identically zero,

\[
 \operatorname{tr}((N I_R)^3)-
 \frac{[\operatorname{tr}(N I_R)]^3}{R^2}=0.
\]

If one instead bounds the first trace by its completed value, while retaining
the selected denominator, the excess is

\[
 mN^3-\frac{(RN)^3}{R^2}=(\kappa-1)RN^3.
\]

Thus the benign compression inequality
\(\operatorname{tr}((PAP)^3)\le\operatorname{tr}(A^3)\) reintroduces an
uncancelled diagonal term. A route that completes to all characters and then
invokes the uncoloured trace estimate needs
\(\kappa_{\mathfrak f}(W)=T^{o(1)}\), or a new selected-side trace estimate;
the former is not implied by fibrewise spacing.

## Dyadic conductor shell

PROVED: for the selected \(\mathbb Q(i)\) shell,

\[
 |X(\mathfrak f)|=|\operatorname{Cl}(\mathfrak f)|\le N\mathfrak f\le2Q.
\]

Since \(\mathbb Z[i]\) is a PID, nonzero ideals of norm at most \(X\) are
unit orbits of nonzero Gaussian integers in the radius-\(\sqrt X\) disk.
The elementary lattice bound gives fewer than \(6Q\) ideals of norm at most
\(2Q\) for \(Q\ge8\). Hence

\[
 \sum_{Q<N\mathfrak f\le2Q}|X(\mathfrak f)|\le12Q^2.
\]

There are two distinct potential losses.

- PROVED: fixed-modulus full-character completion has
  \(\kappa_{\mathfrak f}(W_{\mathfrak f})\le2Q\), so its total completed row
  count can be \(2Q\) times the selected count.
- PROVED: forgetting both character and conductor labels before a global
  separation extraction can face \(O(Q^2)\) simultaneous colour fibres in a
  bounded height interval. Fibrewise separation does not turn this into a
  subpower of \(T\) without an additional conductor--height restriction.

The fixed-modulus Fourier groups cannot diagonalize the cross-conductor part
of the original cubic trace. With \(K\) the full selected Gram matrix, the
exact remaining term is

\[
 \mathcal X_\times(W;c)=
 \operatorname{tr}(K^3)-
 \sum_{\mathfrak f}\operatorname{tr}(K_{W_{\mathfrak f}}^3).
\]

It is generally signed and has no common character group. Inflating all
characters to a common multiple changes the frozen zero extensions, exactly
as recorded in the preceding P7-3 result.

## Fixed-character fallback

PROVED conditional on the displayed large-value hypotheses: for one fixed
primitive \(\chi\), norm collapse gives

\[
 D_\chi(t)=\sum_{N<n\le2N}A_\chi(n)n^{it},\qquad
 |A_\chi(n)|\le a_{\mathbb Q(i)}(n)\le\tau(n).
\]

Let \(\Delta_N=\max_{N<n\le2N}\tau(n)\) and
\(b_{\chi,n}=A_\chi(n)/\Delta_N\). If \(W_\chi\subset[0,T]\) is
one-separated and \(|D_\chi(t)|\ge V\) on \(W_\chi\), the pinned
Guth--Maynard Theorem 1.1 applied to threshold \(V/\Delta_N\) gives

\[
\begin{aligned}
 |W_\chi|\ll T^{o(1)}\bigl(&
 N^2\Delta_N^2V^{-2}
 +N^{18/5}\Delta_N^4V^{-4}\\
 &+TN^{12/5}\Delta_N^4V^{-4}\bigr).
\end{aligned}
\]

P7-1 proved that if \(N\le T^C\) for fixed \(C\), then
\(\Delta_N^4=T^{o(1)}\). Thus this becomes the ordinary
Guth--Maynard three-term bound for each fibre, with a subpower loss.

Let

\[
 \mathcal F_{\rm prim}(Q)=
 \sum_{Q<N\mathfrak f\le2Q}
 \#\{\chi:\chi\text{ has exact finite conductor }\mathfrak f\}.
\]

PROVED: direct summation of the preceding per-character inequality gives

\[
 \sum_{\mathfrak f,\chi}|W_\chi|
 \ll \mathcal F_{\rm prim}(Q)T^{o(1)}
 \left(N^2V^{-2}+N^{18/5}V^{-4}+TN^{12/5}V^{-4}\right),
\]

provided every selected fibre satisfies the same stated hypotheses. Since
\(\mathcal F_{\rm prim}(Q)\le\sum_{\mathfrak f}|X(\mathfrak f)|\le12Q^2\),
the exact family-cardinality multiplier in this fallback is
\(\mathcal F_{\rm prim}(Q)\), with the displayed elementary \(12Q^2\)
uniform bound.

This \(Q^2\) bound is not a lower bound for every possible joint method. It
is, however, unavoidable in the character-by-character summation just
written: each nonnegative per-fibre right-hand side is summed once for every
primitive character. If \(Q=T^\vartheta\), its crude uniform form carries a
\(T^{2\vartheta}\) factor and is not a \(T^{o(1)}\) loss for fixed
\(\vartheta>0\). If \(Q=T^{o(1)}\), the family multiplier is subpower, but
that conductor--height restriction is not part of frozen P7.

PROVED: this fallback is an automatic application of P7-1 plus the pinned
integer Guth--Maynard theorem, not a new Hecke theorem. It has no P7 density
or detector consequence until a detector supplies the per-fibre large values,
their common \(N,T,V\) ranges, and the needed conductor/height relation.

## Conditional reduction and the missing statistic

PROVED conditional reduction: suppose a new primitive coloured fixed-modulus
estimate supplies, with selected-side diagonal cancellation retained,

\[
 S_{3,\mathfrak f}\ll T^{o(1)}\left(
 T^2R_{\mathfrak f}^{3/2}+
 TN R_{\mathfrak f}^{1/2}E_{\mathfrak f}^{1/2}\right),
\]

where \(R_{\mathfrak f}=|W_{\mathfrak f}|\) and \(E_{\mathfrak f}\) is a
valid coloured energy. If the cross-conductor contribution admits the same
source-shaped control, then Cauchy--Schwarz gives

\[
 \sum_{\mathfrak f}R_{\mathfrak f}^{3/2}\le R^{3/2},\qquad
 \sum_{\mathfrak f}R_{\mathfrak f}^{1/2}E_{\mathfrak f}^{1/2}
 \le R^{1/2}\left(\sum_{\mathfrak f}E_{\mathfrak f}\right)^{1/2}.
\]

At this formal homogeneous \(S_3\) level, summing dyadic moduli need not
insert a separate number-of-moduli factor. This is not a proof of the
assumed fixed-modulus or cross-conductor estimate.

CONJECTURED: the primary missing analytic statistic is the selected-side
coloured primitive cubic excess

\[
 \mathfrak G_{\mathfrak f}(W;c)=
 \operatorname{tr}(K_{W_{\mathfrak f}}^3)-
 \frac{[\operatorname{tr}(K_{W_{\mathfrak f}})]^3}{|W_{\mathfrak f}|^2},
\]

together with a bound for \(\mathcal X_\times(W;c)\). A successful P7-3
transfer must bound these using a colour-aware affine/Poisson argument in
terms of \(E^\Delta_{\rm col}\), a cross-character local-height statistic,
and the exact primitive projector—without completion factor \(\kappa\) or a
signed-projector triangle inequality. Neither the pinned integer
Guth--Maynard theorem nor the P7-2 L2 Hecke large sieve supplies that bound.

## Replay

~~~sh
cd /root/projects/maph/projects/guth-maynard-zero-density
python3 proof/build_p7_fixed_ray_colour_diagonalization_v1.py --check
python3 -m unittest tests/test_p7_fixed_ray_colour_diagonalization_v1.py -v
~~~

The sealed replay uses only exact integer/Fraction finite checks, validates
the pinned sources and predecessor artifacts, and enforces a strict
60-second / 256 MiB resource contract. It emits observed wall time and peak
RSS for each replay; those measurements are not part of the deterministic
sealed bytes.
